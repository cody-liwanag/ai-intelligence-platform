import duckdb
from sqlalchemy import create_engine
from config.paths import DUCKDB_PATH

POSTGRES_URI = (
    "postgresql+psycopg2://analytics:analytics"
    "@localhost:5433/ai_intelligence_serving"
)


MART_TABLES = [
    "ai_topic_summary",
    "ai_top_repositories",
    "pipeline_health_summary"
]


def publish_marts_to_postgres():

    duck_conn = duckdb.connect(DUCKDB_PATH)

    pg_engine = create_engine(POSTGRES_URI)

    for table_name in MART_TABLES:

        print(f"Publishing mart to Postgres: {table_name}")

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

        print(f"Published {len(df)} rows to public.{table_name}")

    duck_conn.close()

    print("All marts published to Postgres successfully")