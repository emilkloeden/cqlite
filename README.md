# CQL

Query a CSV file from the commandline

## Usage

In memory query:

```py
python cql.py <csv_file> <query>
```

e.g.

```py
python cql.py fakedata.csv "SELECT * FROM csv WHERE name LIKE '%Tommy% AND date_of_birth < '1980-01-01';"
```

Save csv file as SQLite database:

```py
python cql.py <csv_file> --persist
```

Alternatively you can directly query an existing sqlite db file (with a .sqlite or .db extension).
```py
python cql.py fakedata.db "SELECT * FROM my_table_name WHERE name LIKE '%Tommy% AND date_of_birth < '1980-01-01';"
```
