CREATE OR REPLACE TABLE marts.ai_ecosystem_intelligence AS


-- ============================================
-- ECOSYSTEM SIGNALS
-- ============================================

WITH ecosystem AS (

    SELECT

        LOWER(search_topic)
            AS topic,

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


-- ============================================
-- JOB MARKET SIGNALS
-- ============================================

jobs AS (

    SELECT

        LOWER(search_topic)
            AS topic,

        snapshot_date,

        estimated_market_demand,

        total_job_postings,

        avg_salary_min,
        avg_salary_max,

        unique_companies,
        unique_locations

    FROM marts.ai_job_market_summary

),


-- ============================================
-- PRICING SIGNALS
-- ============================================

pricing AS (

    SELECT

        LOWER(search_topic)
            AS topic,

        total_models,

        avg_input_price,
        avg_output_price,

        avg_context_window

    FROM marts.ai_model_pricing_summary

),


-- ============================================
-- CROSS-SOURCE FUSION
-- ============================================

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

        COALESCE(
            j.estimated_market_demand,
            0
        ) AS estimated_market_demand,

        COALESCE(
            j.total_job_postings,
            0
        ) AS total_job_postings,

        COALESCE(
            j.avg_salary_min,
            0
        ) AS avg_salary_min,

        COALESCE(
            j.avg_salary_max,
            0
        ) AS avg_salary_max,

        COALESCE(
            j.unique_companies,
            0
        ) AS unique_companies,

        COALESCE(
            j.unique_locations,
            0
        ) AS unique_locations,

        COALESCE(
            AVG(p.avg_input_price),
            0
        ) AS avg_input_price,

        COALESCE(
            AVG(p.avg_output_price),
            0
        ) AS avg_output_price,

        COALESCE(
            AVG(p.avg_context_window),
            0
        ) AS avg_context_window,

        COALESCE(
            SUM(p.total_models),
            0
        ) AS pricing_model_count

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

        j.estimated_market_demand,
        j.total_job_postings,
        j.avg_salary_min,
        j.avg_salary_max,
        j.unique_companies,
        j.unique_locations

),


-- ============================================
-- NORMALIZED SCORING
-- ============================================

scored AS (

    SELECT

        *,

        -- OSS ecosystem visibility
        LEAST(
            100,
            github_language_diversity * 10
        ) AS oss_visibility_score,

        -- Adoption strength
        LEAST(
            100,
            hf_avg_downloads / 3000
        ) AS model_adoption_score,

        -- Community engagement
        LEAST(
            100,
            hf_avg_likes / 25
        ) AS engagement_score,

        -- Commercial demand
        LEAST(
            100,
            estimated_market_demand / 25
        ) AS commercial_demand_score,

        -- Cost pressure
        LEAST(
            100,
            avg_output_price * 10
        ) AS pricing_pressure_score,

        -- Ecosystem normalization
        LEAST(
            100,
            ecosystem_signal_score / 100
        ) AS ecosystem_signal_normalized

    FROM combined

),


-- ============================================
-- SEMANTIC INTELLIGENCE
-- ============================================

final AS (

    SELECT

        *,

        -- Overall ecosystem maturity
        ROUND(

            (
                commercial_demand_score * 0.45
            )

            +

            (
                model_adoption_score * 0.35
            )

            +

            (
                ecosystem_signal_normalized * 0.20
            ),

            2

        ) AS ecosystem_maturity_score,

        -- Commercial viability
        ROUND(

            (
                commercial_demand_score * 0.50
            )

            +

            (
                model_adoption_score * 0.30
            )

            +

            (
                engagement_score * 0.20
            ),

            2

        ) AS commercial_strength_score,

        -- Hype detection
        ROUND(

            oss_visibility_score
            - (model_adoption_score * 0.50),

            2

        ) AS hype_risk_score,

        -- Adoption efficiency
        ROUND(

            model_adoption_score
            - pricing_pressure_score,

            2

        ) AS efficiency_score

    FROM scored

)


-- ============================================
-- FINAL CLASSIFICATION OUTPUT
-- ============================================

SELECT

    *,

    CASE

        WHEN ecosystem_maturity_score >= 45
         AND commercial_strength_score >= 40

            THEN 'Mature Commercial Ecosystem'

        WHEN ecosystem_maturity_score >= 30

            THEN 'Emerging Ecosystem'

        WHEN hype_risk_score >= 20

            THEN 'High Hype / Weak Commercialization'

        WHEN efficiency_score >= 20

            THEN 'Efficient High Adoption'

        ELSE 'Niche / Early Signal'

    END AS ecosystem_classification,

    CURRENT_TIMESTAMP
        AS mart_generated_at

FROM final;