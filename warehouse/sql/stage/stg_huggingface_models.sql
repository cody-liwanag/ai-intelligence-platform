CREATE OR REPLACE TABLE stage.stg_huggingface_models AS

SELECT

    search_topic,

    model_id,

    author,

    CAST(downloads AS BIGINT) AS downloads,

    CAST(likes AS BIGINT) AS likes,

    pipeline_tag,

    CAST(last_modified AS TIMESTAMP) AS last_modified,

    CAST(private AS BOOLEAN) AS private,

    gated,

    CURRENT_TIMESTAMP AS staged_at

FROM raw.huggingface_models;