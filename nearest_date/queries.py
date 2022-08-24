# The goal of this exercise is to demonstrate a "nearest date" join.
# From the database constructed in make_db.py, for every game, I want to find
# the nearest date for which we have weather data and report that data.
# Then we can do things like determine is wins or losses are more common
# on warm days, for example.

import sqlite3
import pandas as pd
conn = sqlite3.connect("nearest_date.sqlite")
cursor = conn.cursor()

# Find the weather for the nearest day to the target date for which we have data.
# This only works for a single target date
def nearest_date(target_date, print_result = False):
    result = pd.read_sql("""
        SELECT *, ABS(JULIANDAY('{0}')-JULIANDAY(day)) AS diff 
        FROM weather
        ORDER BY diff
        LIMIT 1
    ;""".format(target_date), conn)
    if print_result:
        print( "The closest record to {0} is {1}, on which the temperature was {2}.".format(target_date, result["day"][0], result["temp"][0]) )
    return [result["day"][0], result["temp"][0]]
    
# Get the weather for each game, as determined by the weather data for the nearest date to the date of a game for which we have data.
# I would like to know how to do this in a single query, if that can be done and is desirable.
# Instead, we perform a separate query for every game.
# For this toy database it doesn't matter, but if we had millions of rows in the game and weather tables, what would be the best solution?
def get_weather():
    result = pd.read_sql("""
        SELECT * FROM game
    ;""", conn)
    
    nearest_days = [
        nearest_date(result["day"][i])
    for i in range(len(result))]
    result["nearest_day"] = [nearest_days[i][0] for i in range(len(nearest_days))]
    result["temperature"] = [nearest_days[i][1] for i in range(len(nearest_days))]
    
    return result

print(get_weather())