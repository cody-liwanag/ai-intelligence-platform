import duckdb
from datetime import datetime

DB_PATH = "~/projects/ai-intelligence-platform/warehouse/duckdb/platform.duckdb"

def log_ingestion_run(
        source_name, 
        status,
        rows_loaded,
        raw_file_path,
        error_message=None
):
    
    conn = duckdb.connect(DB_PATH)

    run_id = int(datetime.now().timestamp())

    conn.execute("""
                 INSERT INTO metadata.ingestion_runs
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
                 [
                     run_id,
                     source_name,
                     datetime.now(),
                     status,
                     rows_loaded,
                     raw_file_path,
                     error_message
                 ])
    
    conn.close()