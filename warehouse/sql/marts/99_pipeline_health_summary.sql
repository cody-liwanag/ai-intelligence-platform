CREATE OR REPLACE TABLE marts.pipeline_health_summary AS

WITH latest_quality_run AS (

    SELECT
        quality_run_id,
        run_timestamp,
        status AS quality_status,
        total_checks,
        passed_checks,
        failed_checks
    FROM metadata.quality_runs
    ORDER BY quality_run_id DESC
    LIMIT 1

),

latest_schema_drift_run AS (

    SELECT
        drift_run_id,
        run_timestamp,
        source_name,
        status AS schema_drift_status,
        expected_column_count,
        actual_column_count,
        missing_column_count,
        unexpected_column_count,
        datatype_mismatch_count
    FROM metadata.schema_drift_runs
    ORDER BY drift_run_id DESC
    LIMIT 1

),

latest_ingestion_run AS (

    SELECT
        source_name,
        status AS ingestion_status,
        rows_loaded,
        raw_file_path,
        run_timestamp AS ingestion_run_timestamp,
        error_message
    FROM metadata.ingestion_runs
    ORDER BY run_timestamp DESC
    LIMIT 1

)

SELECT

    CURRENT_TIMESTAMP AS health_generated_at,

    latest_ingestion_run.source_name,
    latest_ingestion_run.ingestion_status,
    latest_ingestion_run.rows_loaded,
    latest_ingestion_run.raw_file_path,
    latest_ingestion_run.ingestion_run_timestamp,
    latest_ingestion_run.error_message,

    latest_schema_drift_run.drift_run_id,
    latest_schema_drift_run.schema_drift_status,
    latest_schema_drift_run.expected_column_count,
    latest_schema_drift_run.actual_column_count,
    latest_schema_drift_run.missing_column_count,
    latest_schema_drift_run.unexpected_column_count,
    latest_schema_drift_run.datatype_mismatch_count,

    latest_quality_run.quality_run_id,
    latest_quality_run.quality_status,
    latest_quality_run.total_checks,
    latest_quality_run.passed_checks,
    latest_quality_run.failed_checks,

    CASE
        WHEN latest_ingestion_run.ingestion_status = 'SUCCESS'
         AND latest_schema_drift_run.schema_drift_status = 'PASSED'
         AND latest_quality_run.quality_status = 'PASSED'
        THEN 'HEALTHY'
        ELSE 'UNHEALTHY'
    END AS overall_pipeline_health

FROM latest_ingestion_run

CROSS JOIN latest_schema_drift_run

CROSS JOIN latest_quality_run;