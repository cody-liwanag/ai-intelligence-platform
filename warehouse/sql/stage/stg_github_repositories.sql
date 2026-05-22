CREATE OR REPLACE TABLE stage.stg_github_repositories AS

SELECT 

    repo_id,
    search_topic,
    LOWER(repo_name) AS repo_name,
    full_name,
    description,
    
    stars,
    forks,

    language,

    CAST(created_at AS TIMESTAMP) AS created_timestamp,
    CAST(updated_at AS TIMESTAMP) AS updated_timestamp,

    DATE_DIFF(
        'day',
        CAST(created_at AS DATE),
        CURRENT_DATE
    ) AS repo_age_days,

    repo_url,

    CURRENT_TIMESTAMP as model_loaded_at

FROM raw.github_repositories;