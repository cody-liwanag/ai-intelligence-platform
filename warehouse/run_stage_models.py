import duckdb

from config.paths import (
    DUCKDB_PATH,
    STAGE_SQL_DIR
)


def run_stage_models():

    conn = duckdb.connect(str(DUCKDB_PATH))

    stage_sql_files = sorted(
        STAGE_SQL_DIR.glob("*.sql")
    )

    for sql_file_path in stage_sql_files:

        print(f"Running stage model: {sql_file_path.name}")

        with open(sql_file_path, "r") as file:

            stage_sql = file.read()

        conn.execute(stage_sql)

    conn.close()

    print("Stage models built successfully")