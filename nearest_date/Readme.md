## Ben updates
- I added a file `make_db_with_added_dates.py` which is the same as `make_db.py` except it inserts 2 extra dates to the weather table.
- I added two notebooks
    - `pandas_nearest_option` - is using the pandas `index.get_indexer` function to solve the prompt
    - `sqlite_query_option` - is using a sqlite query with CTEs (and 2 extra dates) to solve the prompt
- I added a `requirements.txt` file. To reproduce the notebooks you can run `pip install -r requirements.txt` in a new virtual environment. There are some extra requirements but there's pretty small. I just copied requirements from https://github.com/simonw/datasette.io because I knew they used sqlite/python.