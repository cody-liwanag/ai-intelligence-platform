CREATE TABLE IF NOT EXISTS metadata.ingestion_runs (
    run_id BIGINT,
    source_name VARCHAR,
    run_timestamp TIMESTAMP,
    status VARCHAR,
    rows_loaded INTEGER,
    raw_file_path VARCHAR,
    error_message VARCHAR
);

CREATE TABLE IF NOT EXISTS metadata.ingestion_state (
    source_name VARCHAR,
    last_successful_run TIMESTAMP,
    last_cursor VARCHAR,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS metadata.quality_runs (
    quality_run_id BIGINT,
    run_timestamp TIMESTAMP,
    status VARCHAR,
    total_checks INTEGER,
    passed_checks INTEGER,
    failed_checks INTEGER
);

CREATE TABLE IF NOT EXISTS metadata.quality_results (
    quality_run_id BIGINT,
    check_name VARCHAR,
    table_name VARCHAR,
    status VARCHAR,
    failed_row_count INTEGER,
    check_timestamp TIMESTAMP,
    error_message VARCHAR
);

CREATE TABLE IF NOT EXISTS metadata.schema_drift_runs (
    drift_run_id BIGINT,
    run_timestamp TIMESTAMP,
    source_name VARCHAR,
    status VARCHAR,
    expected_column_count INTEGER,
    actual_column_count INTEGER,
    missing_column_count INTEGER,
    unexpected_column_count INTEGER,
    datatype_mismatch_count INTEGER
);

CREATE TABLE IF NOT EXISTS metadata.schema_drift_results (
    drift_run_id BIGINT,
    source_name VARCHAR,
    column_name VARCHAR,
    drift_type VARCHAR,
    expected_type VARCHAR,
    actual_type VARCHAR,
    severity VARCHAR,
    check_timestamp TIMESTAMP
);
