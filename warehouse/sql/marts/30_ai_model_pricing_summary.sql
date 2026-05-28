CREATE OR REPLACE TABLE marts.ai_model_pricing_summary AS

SELECT

    search_topic,

    provider_name,

    COUNT(*) AS total_models,

    AVG(
        input_price_per_million
    ) AS avg_input_price,

    AVG(
        output_price_per_million
    ) AS avg_output_price,

    AVG(
        context_window
    ) AS avg_context_window,

    CURRENT_TIMESTAMP AS mart_generated_at

FROM stage.stg_model_pricing

GROUP BY

    search_topic,
    provider_name;