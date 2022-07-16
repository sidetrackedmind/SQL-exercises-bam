# See European Soccer Game Analysis from https://www.projectpro.io/article/sql-database-projects-for-data-analysis-to-practice/565
# Kaggle data set: https://www.kaggle.com/code/dimarudov/data-analysis-using-sql/data

import sqlite3
import pandas as pd
conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

table = pd.read_sql("""SELECT *
                        FROM sqlite_master
                        WHERE type='table';""", conn)
print(table)
