import duckdb
from datetime import datetime

from config.paths import DUCKDB_PATH

def log_ingestion_run(
    source_name,
    status,
    rows_loaded,
    raw_file_path,
    error_message=None
):

    conn = duckdb.connect(DUCKDB_PATH)

    conn.execute("""
        INSERT INTO metadata.ingestion_runs (
            source_name,
            status,
            rows_loaded,
            raw_file_path,
            run_timestamp,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        source_name,
        status,
        rows_loaded,
        raw_file_path,
        datetime.now(),
        error_message
    ])

    conn.close()

    print(f"Logged ingestion run for {source_name}: {status}")