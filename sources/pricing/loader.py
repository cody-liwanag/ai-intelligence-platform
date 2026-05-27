import duckdb

from config.paths import DUCKDB_PATH


def load_raw_pricing_data(dataframe):

    conn = duckdb.connect(
        str(DUCKDB_PATH)
    )

    conn.execute("""

        CREATE SCHEMA IF NOT EXISTS raw

    """)

    conn.register(
        "pricing_dataframe",
        dataframe
    )

    conn.execute("""

        CREATE OR REPLACE TABLE raw.model_pricing AS

        SELECT *
        FROM pricing_dataframe

    """)

    total_rows = conn.execute("""

        SELECT COUNT(*)

        FROM raw.model_pricing

    """).fetchone()[0]

    conn.close()

    print(
        f"Loaded {total_rows} rows into raw.model_pricing"
    )

    return total_rows