from datetime import datetime
from pathlib import Path
from csv import reader
import sqlite3
from typing import Optional
from rich.console import Console
from rich.table import Table
import typer

# TODO: Remove all the SQLi opportunities!


def construct_create_table_stmt(table_name: str, headers: list[str]) -> str:
    num_headers = len(headers)
    if num_headers == 0:
        raise ValueError("Cannot create an empty table")

    stmt = f"CREATE TABLE {table_name} (\n"
    for i, h in enumerate(headers):
        name_, type_ = h
        if not type_:
            type_ = str
        if type_ == str:
            stmt += f"[{name_}] TEXT"
        elif type_ == float:
            stmt += f"[{name_}] FLOAT"
        elif type_ == int:
            stmt += f"[{name_}] INT"
        elif type_ == datetime.date:
            stmt += f"[{name_}] DATE"
        if i != num_headers - 1:
            stmt += ","
        stmt += "\n"

    stmt += ");"
    return stmt


def construct_insert_stmts(
    table_name: str, headers, rows: list[list[str]]
) -> list[str]:
    return [construct_insert_stmt(table_name, headers, row) for row in rows]


def construct_insert_stmt(table_name: str, headers, row: list[str]):
    row_with_types = []
    for i, c in enumerate(row):
        if headers[i][1] == datetime.date:
            row_with_types.append(
                datetime.strftime(datetime.strptime(c, "%d/%m/%Y"), "%Y-%m-%d")
            )
        else:
            row_with_types.append(c)

    stmt = f"""INSERT INTO {table_name} VALUES ({','.join([f"'{c}'" for c in row_with_types])});"""
    return stmt


def rotate_n_rows(rows, n):
    rows = rows[:n]
    return list(zip(*rows[::-1]))


# def is_type(col, type_cast):
#     try:
#         return all([type_cast(datum) for datum in col])
#     except ValueError:
#         return False


def is_float(col):
    try:
        return all([not float(datum).is_integer() for datum in col])
    except ValueError:
        return False


def is_int(col):
    try:
        return all([float(datum).is_integer() for datum in col])
    except ValueError:
        return False


def is_date(col):
    try:
        return all([datetime.strptime(datum, "%d/%m/%Y") for datum in col])
    except ValueError:
        return False


# TODO implement datetime parsing


def guess_types(cols):
    types = []
    for col in cols:
        val = None
        if is_float(col):
            val = float
        elif is_int(col):
            val = int
        elif is_date(col):
            val = datetime.date
        types.append(val)
    return types


def load_csv_file(file_path: Path):
    try:
        with file_path.open("r") as f:
            csvreader = reader(f)
            headers = next(csvreader)
            header_names = [
                c.strip().replace(" ", "_").replace("-", " ") for c in headers
            ]
            rows = list(csvreader)
            cols = rotate_n_rows(rows, 8)
            types = guess_types(cols)
            headers = list(zip(header_names, types))
            return headers, rows
    except FileNotFoundError as e:
        raise


def populate_database(conn, cur, name, headers, rows):
    cur.execute(f"DROP TABLE IF EXISTS {name};")
    conn.commit()
    try:
        stmt = construct_create_table_stmt(name, headers)
        cur.execute(stmt)
        conn.commit()
    except ValueError:
        raise

    stmts = construct_insert_stmts(name, headers, rows)
    for stmt in stmts:
        cur.execute(stmt)
    conn.commit()

    return conn, cur


def print_results(results, headers, name):
    table = Table(*headers, title=name)
    for row in results:
        table.add_row(*[str(c) for c in row])

    console = Console()
    console.print(table)


def execute_query(cur, query: str):
    results = cur.execute(query)
    result_headers = [c[0] for c in cur.description]
    return results, result_headers


def main(
    path_to_csv: str,
    query: Optional[str] = typer.Argument(None),
    persist: bool = typer.Option(False, help="Save input to sqlite file."),
):
    file_path = Path(path_to_csv)
    name = file_path.stem
    headers, rows = load_csv_file(file_path)

    if persist:
        db_path = file_path.parent / f"{name}.db"
        conn = sqlite3.connect(db_path)
    else:
        conn = sqlite3.connect(":memory:")
    # conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    conn, cur = populate_database(conn, cur, name, headers, rows)

    if query:
        results, result_headers = execute_query(cur, query)
        print_results(results, result_headers, name)


if __name__ == "__main__":
    typer.run(main)
