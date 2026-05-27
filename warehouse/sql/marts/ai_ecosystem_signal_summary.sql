CREATE OR REPLACE TABLE marts.ai_ecosystem_signal_summary AS

WITH github_summary AS (

    SELECT

        search_topic,

        CURRENT_DATE AS snapshot_date,

        COUNT(*) AS github_repo_count,

        AVG(stars) AS github_avg_stars,

        MAX(stars) AS github_max_stars,

        COUNT(DISTINCT language) AS github_language_diversity

    FROM stage.stg_github_repositories

    GROUP BY
        search_topic

),

huggingface_summary AS (

    SELECT

        search_topic,

        CURRENT_DATE AS snapshot_date,

        COUNT(*) AS hf_model_count,

        AVG(downloads) AS hf_avg_downloads,

        AVG(likes) AS hf_avg_likes,

        COUNT(DISTINCT pipeline_tag) AS hf_pipeline_diversity

    FROM stage.stg_huggingface_models

    GROUP BY
        search_topic

)

SELECT

    COALESCE(
        github_summary.search_topic,
        huggingface_summary.search_topic
    ) AS search_topic,

    CURRENT_DATE AS snapshot_date,

    github_repo_count,

    github_avg_stars,

    github_max_stars,

    github_language_diversity,

    hf_model_count,

    hf_avg_downloads,

    hf_avg_likes,

    hf_pipeline_diversity,

    ROUND(

        (
            COALESCE(github_avg_stars, 0) * 0.4
        )

        +

        (
            COALESCE(hf_avg_downloads, 0) * 0.0001 * 0.4
        )

        +

        (
            (
                COALESCE(github_repo_count, 0)
                +
                COALESCE(hf_model_count, 0)
            ) * 0.2
        ),

        2

    ) AS ecosystem_signal_score,

    CURRENT_TIMESTAMP AS mart_generated_at

FROM github_summary

FULL OUTER JOIN huggingface_summary

    ON github_summary.search_topic =
       huggingface_summary.search_topic;