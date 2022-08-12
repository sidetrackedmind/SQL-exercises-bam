# See European Soccer Game Analysis from https://www.projectpro.io/article/sql-database-projects-for-data-analysis-to-practice/565
# Kaggle data set: https://www.kaggle.com/code/dimarudov/data-analysis-using-sql/data

import sqlite3
import pandas as pd
conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

table = pd.read_sql("""SELECT *
                        FROM sqlite_master
                        WHERE type='table';""", conn)
table_names = table["tbl_name"].to_list()[1:]

tables = {}
column_names = {}
column_lengths = {}
for i in range(len(table_names)):
    query = "SELECT * FROM {0} LIMIT 1".format(table_names[i])
    tables[table_names[i]] = pd.read_sql(query, conn)
    column_names[table_names[i]] = tables[table_names[i]].columns.to_list()
    col_names = column_names[table_names[i]]
    column_lengths[table_names[i]] = max( [len(col_names[i]) for i in range(len(col_names))] )
    column_lengths[table_names[i]] = max( column_lengths[table_names[i]], len(table_names[i]) )
    
################## Format display of columns

def display_columns():
    max_length = max([ len(column_names[key]) for key in column_names ]) # Should be 115.
    padded_table_names = [ table_names[i]+" "*(column_lengths[table_names[i]] - len(table_names[i])) for i in range(len(table_names)) ]
    print("   ".join(padded_table_names))

    dividers = [ "="*column_lengths[table_names[i]] for i in range(len(table_names)) ]
    print("===".join(dividers))
    for i in range(max_length):
        columns = [ " "*column_lengths[table_names[j]] for j in range(len(table_names)) ]
        for j in range(len(table_names)):
            if len(column_names[table_names[j]]) > i:
                columns[j] = column_names[table_names[j]][i] + " "*(column_lengths[table_names[j]] - len(column_names[table_names[j]][i]) )
        print(" | ".join(columns))
display_columns()