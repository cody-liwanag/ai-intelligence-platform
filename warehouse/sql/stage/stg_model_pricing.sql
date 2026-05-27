CREATE OR REPLACE TABLE stage.stg_model_pricing AS

SELECT

    TRIM(provider_name) AS provider_name,

    TRIM(model_name) AS model_name,

    CAST(
        input_price_per_million
        AS DOUBLE
    ) AS input_price_per_million,

    CAST(
        output_price_per_million
        AS DOUBLE
    ) AS output_price_per_million,

    CAST(
        context_window
        AS BIGINT
    ) AS context_window,

    TRIM(model_family) AS model_family,

    pricing_source,

    CAST(
        pricing_snapshot_date
        AS TIMESTAMP
    ) AS pricing_snapshot_date,

    search_topic,

    CURRENT_TIMESTAMP AS staged_at

FROM raw.model_pricing;