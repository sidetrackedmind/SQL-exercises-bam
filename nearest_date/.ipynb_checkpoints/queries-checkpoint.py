# The goal of this exercise is to demonstrate a "nearest date" join.
# From the database constructed in make_db.py, for every game, I want to find
# the nearest date for which we have weather data and report that data.
# Then we can do things like determine is wins or losses are more common
# on warm days, for example.

import sqlite3
import pandas as pd
conn = sqlite3.connect("nearest_date.sqlite")
cursor = conn.cursor()

def get_weather():
    result = pd.read_sql("""
                with sorted_weather as (
                SELECT
                *
                FROM
                WEATHER
                ORDER BY day
                )
                , weather_day_bounds as (
                SELECT 
                    day as lower_bound_day,
                    lead(day) over (order by day) as upper_bound_day
                FROM 
                    sorted_weather
                )
                , upper_lower_diff as (
                SELECT
                    game.day,
                    game.outcome,
                    weather.lower_bound_day,
                    weather.upper_bound_day,
                    abs(julianday(game.day)-julianday(weather.lower_bound_day)) as lower_bound_diff,
                    abs(julianday(game.day)-julianday(weather.upper_bound_day)) as upper_bound_diff
                FROM
                    game
                LEFT JOIN
                    weather_day_bounds weather
                ON
                    game.day > weather.lower_bound_day and game.day <= weather.upper_bound_day
                    )
                , get_winning_day as (
                    SELECT
                        day, outcome,
                        case when lower_bound_diff=upper_bound_diff then lower_bound_day
                        when lower_bound_diff<upper_bound_diff then lower_bound_day
                        when upper_bound_diff<lower_bound_diff then upper_bound_day
                        else lower_bound_day
                        end as winning_weather_day
                    FROM
                        upper_lower_diff
                )
                SELECT
                    gwd.day, gwd.outcome, gwd.winning_weather_day, w.temp
                FROM
                    get_winning_day gwd
                LEFT JOIN
                    WEATHER w
                ON
                    gwd.winning_weather_day = w.day""", conn)
    
    return result

print(get_weather())