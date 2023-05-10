# cqlite

Query a CSV file from the commandline

## Installation

`pipx install cqlite`

## Usage

In memory query:

```py
cqlite <csv_file> <query>
```

e.g.

```py
cqlite fakedata.csv "SELECT * FROM csv WHERE name LIKE '%Tommy% AND date_of_birth < '1980-01-01';"
```

Save csv file as SQLite database:

```py
cqlite <csv_file> --persist
```

Alternatively you can directly query an existing sqlite db file (with a .sqlite or .db extension).

```py
cqlite fakedata.db "SELECT * FROM my_table_name WHERE name LIKE '%Tommy% AND date_of_birth < '1980-01-01';"
```
