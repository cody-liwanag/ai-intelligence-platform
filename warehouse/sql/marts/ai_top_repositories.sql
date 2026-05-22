CREATE OR REPLACE TABLE marts.ai_top_repositories AS

WITH ranked_repositories AS (

    SELECT

        search_topic,

        repo_id,

        repo_name,

        full_name,

        description,

        stars,

        forks,

        language,

        repo_age_days,

        updated_timestamp,

        repo_url,

        DATE_DIFF('day', updated_timestamp::DATE, CURRENT_DATE) AS days_since_update,

        ROW_NUMBER() OVER (
            PARTITION BY search_topic
            ORDER BY stars DESC
        ) AS topic_rank

    FROM stage.stg_github_repositories

)

SELECT

    search_topic,

    topic_rank,

    repo_id,

    repo_name,

    full_name,

    description,

    stars,

    forks,

    language,

    repo_age_days,

    days_since_update,

    repo_url,

    CURRENT_TIMESTAMP AS mart_generated_at

FROM ranked_repositories

WHERE topic_rank <= 10;