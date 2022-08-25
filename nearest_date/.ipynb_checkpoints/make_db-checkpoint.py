import sqlite3
import pandas as pd

def make_example_tables():
    conn = sqlite3.connect("nearest_date.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            day DATE NOT NULL UNIQUE,
            temp INTEGER
        )
    ;""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game (
            day DATE NOT NULL UNIQUE,
            outcome CHAR(1)
        )
    ;""")

    cursor.execute("""
        INSERT OR IGNORE INTO weather(day, temp)
        VALUES
            ('2022-07-13',80),
            ('2022-07-17',90),
            ('2022-07-20',85),
            ('2022-07-30',80),
            ('2022-08-01',77),
            ('2022-08-04',70),
            ('2022-08-10',68),
            ('2022-08-12',74),
            ('2022-08-17',65),
            ('2022-08-22',71)
    ;""")

    cursor.execute("""
        INSERT OR IGNORE INTO game(day, outcome)
        VALUES
            ('2022-07-11','W'),
            ('2022-07-16','W'),
            ('2022-07-20','L'),
            ('2022-07-27','L'),
            ('2022-07-31','L'),
            ('2022-08-05','W'),
            ('2022-08-09','L'),
            ('2022-08-13','L'),
            ('2022-08-14','W'),
            ('2022-08-20','W'),
            ('2022-08-22','L')
    ;""")

    #add an "old date" and the current date to weather table with no temp value
    #these dates are just to complete the bounds

    print("Weather Data")
    table = pd.read_sql("SELECT * FROM weather", conn)
    print(table.to_string(index=False))

    print("\nGame Data: W is a Win, L is a Loss")
    table = pd.read_sql("SELECT * FROM game", conn)
    print(table.to_string(index=False))

    cursor.execute("COMMIT;")