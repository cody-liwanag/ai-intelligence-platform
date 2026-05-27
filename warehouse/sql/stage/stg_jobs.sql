CREATE OR REPLACE TABLE stage.stg_jobs AS

SELECT

    search_topic,

    CAST(job_id AS VARCHAR) AS job_id,

    TRIM(job_title) AS job_title,

    TRIM(company_name) AS company_name,

    TRIM(location_name) AS location_name,

    TRIM(category_label) AS category_label,

    contract_type,

    CAST(created_at AS TIMESTAMP) AS created_at,

    CAST(salary_min AS DOUBLE) AS salary_min,

    CAST(salary_max AS DOUBLE) AS salary_max,

    salary_is_predicted,

    redirect_url,

    source_platform,

    CURRENT_TIMESTAMP AS staged_at

FROM raw.jobs;