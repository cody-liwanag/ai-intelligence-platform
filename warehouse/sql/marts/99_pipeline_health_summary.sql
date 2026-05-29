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

    QUALIFY ROW_NUMBER() OVER (

        ORDER BY quality_run_id DESC

    ) = 1

),


latest_ingestion_runs AS (

    SELECT

        source_name,
        status AS ingestion_status,
        rows_loaded,
        raw_file_path,
        run_timestamp AS ingestion_run_timestamp,
        error_message

    FROM metadata.ingestion_runs

    QUALIFY ROW_NUMBER() OVER (

        PARTITION BY source_name
        ORDER BY run_timestamp DESC

    ) = 1

),


latest_schema_drift_runs AS (

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

    QUALIFY ROW_NUMBER() OVER (

        PARTITION BY source_name
        ORDER BY run_timestamp DESC

    ) = 1

)


SELECT

    CURRENT_TIMESTAMP
        AS health_generated_at,

    i.source_name,

    i.ingestion_status,
    i.rows_loaded,
    i.raw_file_path,
    i.ingestion_run_timestamp,
    i.error_message,

    d.drift_run_id,

    COALESCE(
        d.schema_drift_status,
        'NOT_RUN'
    ) AS schema_drift_status,

    COALESCE(
        d.expected_column_count,
        0
    ) AS expected_column_count,

    COALESCE(
        d.actual_column_count,
        0
    ) AS actual_column_count,

    COALESCE(
        d.missing_column_count,
        0
    ) AS missing_column_count,

    COALESCE(
        d.unexpected_column_count,
        0
    ) AS unexpected_column_count,

    COALESCE(
        d.datatype_mismatch_count,
        0
    ) AS datatype_mismatch_count,

    q.quality_run_id,
    q.quality_status,
    q.total_checks,
    q.passed_checks,
    q.failed_checks,

    CASE

        WHEN

            i.ingestion_status = 'SUCCESS'

            AND

            COALESCE(
                d.schema_drift_status,
                'PASSED'
            ) = 'PASSED'

            AND

            q.quality_status = 'PASSED'

        THEN 'HEALTHY'

        ELSE 'UNHEALTHY'

    END AS overall_pipeline_health

FROM latest_ingestion_runs i

LEFT JOIN latest_schema_drift_runs d

    ON i.source_name = d.source_name

CROSS JOIN latest_quality_run q;