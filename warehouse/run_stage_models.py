import duckdb

DB_PATH = "~/projects/ai-intelligence-platform/warehouse/duckdb/platform.duckdb"

def run_stage_models():

    conn = duckdb.connect(DB_PATH)

    with open("warehouse/sql/stage/stg_github_repositories.sql", "r") as file:
        stage_sql = file.read()

    conn.execute(stage_sql)

    conn.close()

    print("Stage Models Built Successfully")