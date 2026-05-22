import duckdb


DB_PATH = "warehouse/duckdb/platform.duckdb"


MART_SQL_FILES = [
    "warehouse/sql/marts/ai_topic_summary.sql",
    "warehouse/sql/marts/ai_top_repositories.sql",
    "warehouse/sql/marts/pipeline_health_summary.sql"
]


def run_mart_models():

    conn = duckdb.connect(DB_PATH)

    for sql_file_path in MART_SQL_FILES:

        print(f"Running mart model: {sql_file_path}")

        with open(sql_file_path, "r") as file:
            mart_sql = file.read()

        conn.execute(mart_sql)

    conn.close()

    print("Mart models built successfully")