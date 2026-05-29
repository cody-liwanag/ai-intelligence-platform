import duckdb

from sqlalchemy import create_engine

from config.paths import DUCKDB_PATH


POSTGRES_URI = (
    "postgresql+psycopg2://analytics:analytics"
    "@localhost:5433/ai_intelligence_serving"
)


def get_mart_tables(duck_conn):

    mart_tables = duck_conn.execute("""

        SELECT table_name

        FROM information_schema.tables

        WHERE table_schema = 'marts'

        ORDER BY table_name

    """).fetchall()

    return [row[0] for row in mart_tables]


def publish_marts_to_postgres():

    print("\n" + "=" * 60)
    print("PUBLISHING MARTS TO POSTGRES")
    print("=" * 60)

    duck_conn = duckdb.connect(DUCKDB_PATH)

    pg_engine = create_engine(POSTGRES_URI)

    mart_tables = get_mart_tables(duck_conn)

    print(f"Discovered {len(mart_tables)} mart tables")

    for table_name in mart_tables:

        print("\n" + "-" * 60)
        print(f"Publishing mart: {table_name}")
        print("-" * 60)

        df = duck_conn.execute(f"""

            SELECT *

            FROM marts.{table_name}

        """).fetchdf()

        df.to_sql(
            name=table_name,
            con=pg_engine,
            schema="public",
            if_exists="replace",
            index=False
        )

        print(
            f"Published {len(df)} rows "
            f"to public.{table_name}"
        )

    duck_conn.close()

    print("\n" + "=" * 60)
    print("ALL MARTS PUBLISHED SUCCESSFULLY")
    print("=" * 60)