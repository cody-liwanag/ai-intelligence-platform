CREATE OR REPLACE TABLE marts.ai_ecosystem_intelligence AS


-- ============================================
-- SEMANTIC TOPIC NORMALISATION
-- ============================================

WITH ecosystem_raw AS (

    SELECT

        CASE

            WHEN LOWER(TRIM(search_topic)) IN (
                'llm',
                'large language model'
            )
                THEN 'large language models'

            WHEN LOWER(TRIM(search_topic)) IN (
                'rag',
                'retrieval augmented generation'
            )
                THEN 'retrieval augmented generation'

            ELSE LOWER(TRIM(search_topic))

        END AS topic,

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


jobs_raw AS (

    SELECT

        CASE

            WHEN LOWER(TRIM(search_topic)) IN (
                'llm',
                'large language model'
            )
                THEN 'large language models'

            WHEN LOWER(TRIM(search_topic)) IN (
                'rag',
                'retrieval augmented generation'
            )
                THEN 'retrieval augmented generation'

            ELSE LOWER(TRIM(search_topic))

        END AS topic,

        snapshot_date,

        estimated_market_demand,
        total_job_postings,

        avg_salary_min,
        avg_salary_max,

        unique_companies,
        unique_locations

    FROM marts.ai_job_market_summary

),


pricing_raw AS (

    SELECT

        CASE

            WHEN LOWER(TRIM(search_topic)) IN (
                'llm',
                'large language model'
            )
                THEN 'large language models'

            WHEN LOWER(TRIM(search_topic)) IN (
                'rag',
                'retrieval augmented generation'
            )
                THEN 'retrieval augmented generation'

            ELSE LOWER(TRIM(search_topic))

        END AS topic,

        total_models,

        avg_input_price,
        avg_output_price,

        avg_context_window

    FROM marts.ai_model_pricing_summary

),


-- ============================================
-- SOURCE DOMAIN AGGREGATION
-- ============================================

ecosystem AS (

    SELECT

        topic,
        snapshot_date,

        MAX(github_repo_count)
            AS github_repo_count,

        MAX(github_avg_stars)
            AS github_avg_stars,

        MAX(github_max_stars)
            AS github_max_stars,

        MAX(github_language_diversity)
            AS github_language_diversity,

        SUM(hf_model_count)
            AS hf_model_count,

        MAX(hf_avg_downloads)
            AS hf_avg_downloads,

        MAX(hf_avg_likes)
            AS hf_avg_likes,

        MAX(hf_pipeline_diversity)
            AS hf_pipeline_diversity,

        MAX(ecosystem_signal_score)
            AS ecosystem_signal_score

    FROM ecosystem_raw

    GROUP BY

        topic,
        snapshot_date

),


jobs AS (

    SELECT

        topic,
        snapshot_date,

        MAX(estimated_market_demand)
            AS estimated_market_demand,

        SUM(total_job_postings)
            AS total_job_postings,

        AVG(avg_salary_min)
            AS avg_salary_min,

        AVG(avg_salary_max)
            AS avg_salary_max,

        MAX(unique_companies)
            AS unique_companies,

        MAX(unique_locations)
            AS unique_locations

    FROM jobs_raw

    GROUP BY

        topic,
        snapshot_date

),


pricing AS (

    SELECT

        topic,

        SUM(total_models)
            AS pricing_model_count,

        AVG(avg_input_price)
            AS avg_input_price,

        AVG(avg_output_price)
            AS avg_output_price,

        AVG(avg_context_window)
            AS avg_context_window

    FROM pricing_raw

    GROUP BY

        topic

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
            p.pricing_model_count,
            0
        ) AS pricing_model_count,

        COALESCE(
            p.avg_input_price,
            0
        ) AS avg_input_price,

        COALESCE(
            p.avg_output_price,
            0
        ) AS avg_output_price,

        COALESCE(
            p.avg_context_window,
            0
        ) AS avg_context_window

    FROM ecosystem e

    LEFT JOIN jobs j

        ON e.topic = j.topic
       AND e.snapshot_date = j.snapshot_date

    LEFT JOIN pricing p

        ON e.topic = p.topic

),


-- ============================================
-- NORMALISED SOURCE SCORES
-- ============================================

scored AS (

    SELECT

        *,

        -- OSS Visibility Index
        -- Uses stars + language diversity, but avoids raw repo count dominance.
        ROUND(

            LEAST(

                100,

                LEAST(
                    70,
                    (
                        LN(
                            1 + GREATEST(github_avg_stars, 0)
                        )
                        /
                        LN(1 + 100000)
                    ) * 70
                )

                +

                LEAST(
                    30,
                    github_language_diversity * 3
                )

            ),

            2

        ) AS oss_visibility_score,


        -- Model Adoption Index
        -- Hugging Face downloads are highly skewed, so log scaling is more believable.
        ROUND(

            LEAST(

                100,

                (
                    LN(
                        1 + GREATEST(hf_avg_downloads, 0)
                    )
                    /
                    LN(1 + 100000)
                ) * 100

            ),

            2

        ) AS model_adoption_score,


        -- Engagement Index
        -- Secondary signal only; used for detail, not core classification.
        ROUND(

            LEAST(

                100,

                (
                    LN(
                        1 + GREATEST(hf_avg_likes, 0)
                    )
                    /
                    LN(1 + 5000)
                ) * 100

            ),

            2

        ) AS engagement_score,


        -- Commercial Demand Index
        -- Uses Adzuna estimated market demand, not returned sample rows.
        -- 1000+ estimated jobs would approach maximum signal.
        ROUND(

            LEAST(

                100,

                GREATEST(
                    estimated_market_demand,
                    0
                ) / 10.0

            ),

            2

        ) AS commercial_demand_score,


        -- Pricing Pressure Index
        -- Kept conservative because pricing data can be sparse/noisy.
        ROUND(

            LEAST(

                100,

                (
                    LN(
                        1 + GREATEST(avg_output_price, 0)
                    )
                    /
                    LN(1 + 100)
                ) * 100

            ),

            2

        ) AS pricing_pressure_score

    FROM combined

),


-- ============================================
-- SEMANTIC INTELLIGENCE SCORES
-- ============================================

final AS (

    SELECT

        *,

        -- Overall ecosystem maturity
        ROUND(

            (
                commercial_demand_score * 0.40
            )

            +

            (
                model_adoption_score * 0.35
            )

            +

            (
                oss_visibility_score * 0.25
            ),

            2

        ) AS ecosystem_maturity_score,


        -- Commercial viability
        ROUND(

            (
                commercial_demand_score * 0.65
            )

            +

            (
                model_adoption_score * 0.35
            ),

            2

        ) AS commercial_strength_score,


        -- Hype risk
        -- Hype = excess OSS visibility not sufficiently backed by
        -- commercial demand or real model adoption.
        ROUND(

            LEAST(

                100,

                GREATEST(

                    0,

                    (
                        oss_visibility_score * 0.65
                    )

                    -

                    (
                        commercial_demand_score * 0.55
                    )

                    -

                    (
                        model_adoption_score * 0.35
                    )

                )

            ),

            2

        ) AS hype_risk_score,


        -- Adoption efficiency
        ROUND(

            LEAST(

                100,

                GREATEST(

                    0,

                    model_adoption_score
                    - (pricing_pressure_score * 0.30)

                )

            ),

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

        WHEN ecosystem_maturity_score >= 65
         AND commercial_strength_score >= 55

            THEN 'Mature Commercial Ecosystem'

        WHEN commercial_demand_score >= 60
         AND model_adoption_score < 35

            THEN 'Commercial Demand Ahead of Adoption'

        WHEN hype_risk_score >= 15
         AND commercial_demand_score < 50

            THEN 'High Hype / Weak Commercialization'

        WHEN ecosystem_maturity_score >= 45

            THEN 'Emerging Ecosystem'

        WHEN efficiency_score >= 60

            THEN 'Efficient High Adoption'

        ELSE 'Niche / Early Signal'

    END AS ecosystem_classification,

    CURRENT_TIMESTAMP
        AS mart_generated_at

FROM final;