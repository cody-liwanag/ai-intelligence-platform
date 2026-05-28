CREATE OR REPLACE TABLE stage.stg_jobs AS

SELECT

    LOWER(TRIM(search_topic))
        AS search_topic,

    estimated_market_demand,

    job_id,

    LOWER(TRIM(job_title))
        AS job_title,

    LOWER(TRIM(company_name))
        AS company_name,

    LOWER(TRIM(location_name))
        AS location_name,

    LOWER(TRIM(category_label))
        AS category_label,

    contract_type,

    CAST(created_at AS TIMESTAMP)
        AS created_at,

    salary_min,

    salary_max,

    salary_is_predicted,

    redirect_url,

    source_platform,

    CURRENT_DATE
        AS snapshot_date

FROM raw.jobs;