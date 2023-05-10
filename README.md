# cqlite

Query a CSV file from the commandline

## Installation

`pipx install cqlite`

## Usage

In memory query:

```sh
cqlite <csv_file> <query>
```

e.g.

```sh
cqlite fakedata.csv "SELECT * FROM csv WHERE name LIKE '%Tommy% AND date_of_birth < '1980-01-01';"
```

Save `<csv_file>.csv as a SQLite database (<csv_file>.db):

```sh
cqlite <csv_file> --persist
```
