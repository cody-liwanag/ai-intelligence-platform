import duckdb
from config.paths import DUCKDB_PATH

def run_stage_models():

    conn = duckdb.connect(DUCKDB_PATH)

    with open("warehouse/sql/stage/stg_github_repositories.sql", "r") as file:
        stage_sql = file.read()

    conn.execute(stage_sql)

    conn.close()

    print("Stage Models Built Successfully")