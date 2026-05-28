CREATE OR REPLACE TABLE marts.ai_job_market_summary AS

SELECT

    search_topic,

    snapshot_date,

    MAX(estimated_market_demand)
        AS estimated_market_demand,

    COUNT(DISTINCT job_id)
        AS total_job_postings,

    AVG(salary_min)
        AS avg_salary_min,

    AVG(salary_max)
        AS avg_salary_max,

    COUNT(DISTINCT company_name)
        AS unique_companies,

    COUNT(DISTINCT location_name)
        AS unique_locations,

    CURRENT_TIMESTAMP
        AS mart_generated_at

FROM stage.stg_jobs

GROUP BY

    search_topic,
    snapshot_date;