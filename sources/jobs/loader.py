import duckdb

from config.paths import DUCKDB_PATH


def load_raw_jobs_data(dataframe):

    conn = duckdb.connect(str(DUCKDB_PATH))

    conn.execute("""
    
        CREATE SCHEMA IF NOT EXISTS raw
    
    """)

    conn.register(
        "jobs_dataframe",
        dataframe
    )

    conn.execute("""

        CREATE OR REPLACE TABLE raw.jobs AS

        SELECT *
        FROM jobs_dataframe

    """)

    total_rows = conn.execute("""

        SELECT COUNT(*)
        FROM raw.jobs

    """).fetchone()[0]

    conn.close()

    print(
        f"Loaded {total_rows} rows into raw.jobs"
    )

    return total_rows