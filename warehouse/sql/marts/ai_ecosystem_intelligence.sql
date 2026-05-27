CREATE OR REPLACE TABLE marts.ai_ecosystem_intelligence AS

WITH ecosystem AS (

    SELECT

        LOWER(search_topic) AS topic,

        snapshot_date,

        github_repo_count,
        github_avg_stars,
        github_max_stars,
        github_language_diversity,

        hf_model_count,
        hf_avg_downloads,
        hf_avg_likes,
        hf_pipeline_diversity,

        ecosystem_signal_score

    FROM marts.ai_ecosystem_signal_summary

),

jobs AS (

    SELECT

        LOWER(search_topic) AS topic,

        snapshot_date,

        total_job_postings,
        avg_salary_min,
        avg_salary_max,
        unique_companies,
        unique_locations

    FROM marts.ai_job_market_summary

),

pricing AS (

    SELECT

        LOWER(search_topic) AS topic,

        provider_name,

        total_models,
        avg_input_price,
        avg_output_price,
        avg_context_window

    FROM marts.ai_model_pricing_summary

),

combined AS (

    SELECT

        e.topic,

        e.snapshot_date,

        e.github_repo_count,
        e.github_avg_stars,
        e.github_max_stars,
        e.github_language_diversity,

        e.hf_model_count,
        e.hf_avg_downloads,
        e.hf_avg_likes,
        e.hf_pipeline_diversity,

        e.ecosystem_signal_score,

        COALESCE(j.total_job_postings, 0)
            AS total_job_postings,

        COALESCE(j.avg_salary_min, 0)
            AS avg_salary_min,

        COALESCE(j.avg_salary_max, 0)
            AS avg_salary_max,

        COALESCE(j.unique_companies, 0)
            AS unique_companies,

        COALESCE(j.unique_locations, 0)
            AS unique_locations,

        COALESCE(AVG(p.avg_input_price), 0)
            AS avg_input_price,

        COALESCE(AVG(p.avg_output_price), 0)
            AS avg_output_price,

        COALESCE(AVG(p.avg_context_window), 0)
            AS avg_context_window,

        COALESCE(SUM(p.total_models), 0)
            AS pricing_model_count

    FROM ecosystem e

    LEFT JOIN jobs j
        ON e.topic = j.topic
       AND e.snapshot_date = j.snapshot_date

    LEFT JOIN pricing p
        ON e.topic = p.topic

    GROUP BY

        e.topic,
        e.snapshot_date,

        e.github_repo_count,
        e.github_avg_stars,
        e.github_max_stars,
        e.github_language_diversity,

        e.hf_model_count,
        e.hf_avg_downloads,
        e.hf_avg_likes,
        e.hf_pipeline_diversity,

        e.ecosystem_signal_score,

        j.total_job_postings,
        j.avg_salary_min,
        j.avg_salary_max,
        j.unique_companies,
        j.unique_locations

),

scored AS (

    SELECT

        *,

        LEAST(100, github_repo_count * 2)
            AS oss_volume_score,

        LEAST(100, github_avg_stars / 100)
            AS oss_popularity_score,

        LEAST(100, hf_avg_downloads / 10000)
            AS model_adoption_score,

        LEAST(100, hf_avg_likes / 50)
            AS model_engagement_score,

        LEAST(100, total_job_postings * 5)
            AS commercial_demand_score,

        LEAST(100, avg_output_price * 10)
            AS pricing_pressure_score

    FROM combined

)

SELECT

    topic,

    snapshot_date,

    github_repo_count,
    github_avg_stars,
    github_max_stars,
    github_language_diversity,

    hf_model_count,
    hf_avg_downloads,
    hf_avg_likes,
    hf_pipeline_diversity,

    total_job_postings,
    avg_salary_min,
    avg_salary_max,
    unique_companies,
    unique_locations,

    avg_input_price,
    avg_output_price,
    avg_context_window,
    pricing_model_count,

    ecosystem_signal_score,

    ROUND(
        (oss_volume_score * 0.40)
      + (oss_popularity_score * 0.40)
      + (model_engagement_score * 0.20),
        2
    ) AS oss_momentum_score,

    ROUND(
        (model_adoption_score * 0.60)
      + (model_engagement_score * 0.40),
        2
    ) AS model_strength_score,

    commercial_demand_score,

    pricing_pressure_score,

    ROUND(
        (commercial_demand_score * 0.40)
      + (model_adoption_score * 0.30)
      + (oss_volume_score * 0.30),
        2
    ) AS commercial_strength_score,

    ROUND(
        (
            (oss_volume_score + model_adoption_score)
            / 2
        ) - commercial_demand_score,
        2
    ) AS hype_risk_score,

    ROUND(
        model_adoption_score
        - pricing_pressure_score,
        2
    ) AS efficiency_score,

    ROUND(
        (ecosystem_signal_score * 0.35)
      + (commercial_demand_score * 0.35)
      + (model_adoption_score * 0.30),
        2
    ) AS ecosystem_maturity_score,

    CASE

        WHEN commercial_demand_score >= 60
         AND model_adoption_score >= 50
         AND oss_volume_score >= 50

            THEN 'Mature Commercial Ecosystem'

        WHEN (
            (oss_volume_score + model_adoption_score)
            / 2
        ) >= 60
         AND commercial_demand_score < 25

            THEN 'High Hype / Low Demand'

        WHEN commercial_demand_score >= 50
         AND model_adoption_score < 30

            THEN 'Commercial Demand Ahead of Adoption'

        WHEN pricing_pressure_score >= 60
         AND model_adoption_score < 40

            THEN 'Expensive Weak Adoption'

        WHEN oss_volume_score >= 40
         AND commercial_demand_score >= 30

            THEN 'Emerging Opportunity'

        ELSE 'Niche / Early Signal'

    END AS ecosystem_classification,

    CURRENT_TIMESTAMP
        AS mart_generated_at

FROM scored

WHERE topic IS NOT NULL;