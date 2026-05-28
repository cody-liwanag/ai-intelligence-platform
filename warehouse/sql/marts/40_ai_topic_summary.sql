CREATE TABLE IF NOT EXISTS marts.ai_topic_summary (

    search_topic VARCHAR,

    snapshot_date DATE,

    repository_count INTEGER,

    average_stars DOUBLE,

    max_stars INTEGER,

    average_forks DOUBLE,

    average_repo_age_days DOUBLE,

    language_diversity INTEGER,

    mart_generated_at TIMESTAMP

);


DELETE FROM marts.ai_topic_summary
WHERE snapshot_date = CURRENT_DATE;


INSERT INTO marts.ai_topic_summary

SELECT

    search_topic,

    CURRENT_DATE AS snapshot_date,

    COUNT(*) AS repository_count,

    AVG(stars) AS average_stars,

    MAX(stars) AS max_stars,

    AVG(forks) AS average_forks,

    AVG(repo_age_days) AS average_repo_age_days,

    COUNT(DISTINCT language) AS language_diversity,

    CURRENT_TIMESTAMP AS mart_generated_at

FROM stage.stg_github_repositories

GROUP BY
    search_topic,
    snapshot_date;