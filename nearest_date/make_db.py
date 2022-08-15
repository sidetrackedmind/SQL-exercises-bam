import sqlite3
import pandas as pd
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
        ('2022-08-13',80),
        ('2022-08-17',90),
        ('2022-08-20',85),
        ('2022-08-30',80),
        ('2022-09-01',77),
        ('2022-09-04',70),
        ('2022-09-10',68),
        ('2022-09-12',74),
        ('2022-09-17',65),
        ('2022-09-22',71),
        ('2022-09-29',70)
;""")

cursor.execute("""
    INSERT OR IGNORE INTO game(day, outcome)
    VALUES
        ('2022-08-11','W'),
        ('2022-08-16','W'),
        ('2022-08-20','L'),
        ('2022-08-27','L'),
        ('2022-08-31','L'),
        ('2022-09-05','W'),
        ('2022-09-09','L'),
        ('2022-09-13','L'),
        ('2022-09-14','W'),
        ('2022-09-20','W'),
        ('2022-09-22','L'),
        ('2022-09-30','W')
;""")

print("Weather Data")
table = pd.read_sql("SELECT * FROM weather", conn)
print(table.to_string(index=False))

print("\nGame Data: W is a Win, L is a Loss")
table = pd.read_sql("SELECT * FROM game", conn)
print(table.to_string(index=False))

cursor.execute("COMMIT;")