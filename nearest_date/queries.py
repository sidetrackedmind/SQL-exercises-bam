# The goal of this exercise is to demonstrated a "nearest date" join.
# From the database constructed in make_db.py, for every game, I want to find
# the nearest date for which we have weather data and report that data.
# Then we can do things like determine is wins or losses are more common
# on warm days, for example.

import sqlite3
import pandas as pd
conn = sqlite3.connect("nearest_date.sqlite")
cursor = conn.cursor()

def nearest_date(target_date):
    result = pd.read_sql("""
        SELECT *, ABS(JULIANDAY('{0}')-JULIANDAY(day)) AS diff 
        FROM weather
        ORDER BY diff
        LIMIT 1
    ;""".format(target_date), conn)
    return "The closest record to {0} is {1}, on which the temperature was {2}.".format(target_date, result["day"][0], result["temp"][0])
    
print(nearest_date('2022-09-02'))