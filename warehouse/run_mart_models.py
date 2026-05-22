import duckdb

from config.paths import (
    DUCKDB_PATH,
    MART_SQL_DIR
)


def run_mart_models():

    conn = duckdb.connect(str(DUCKDB_PATH))

    mart_sql_files = sorted(
        MART_SQL_DIR.glob("*.sql")
    )

    for sql_file_path in mart_sql_files:

        print(f"Running mart model: {sql_file_path.name}")

        with open(sql_file_path, "r") as file:

            mart_sql = file.read()

        conn.execute(mart_sql)

    conn.close()

    print("Mart models built successfully")