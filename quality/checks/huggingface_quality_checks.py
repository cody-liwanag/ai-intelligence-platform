HUGGINGFACE_QUALITY_CHECKS = [

    {
        "check_name": "raw_hf_model_id_not_null",

        "table_name": "raw.huggingface_models",

        "sql": """
            SELECT COUNT(*)
            FROM raw.huggingface_models
            WHERE model_id IS NULL
        """
    },

    {
        "check_name": "raw_hf_search_topic_not_null",

        "table_name": "raw.huggingface_models",

        "sql": """
            SELECT COUNT(*)
            FROM raw.huggingface_models
            WHERE search_topic IS NULL
        """
    },

    {
        "check_name": "raw_hf_no_negative_downloads",

        "table_name": "raw.huggingface_models",

        "sql": """
            SELECT COUNT(*)
            FROM raw.huggingface_models
            WHERE downloads < 0
        """
    },

    {
        "check_name": "raw_hf_no_negative_likes",

        "table_name": "raw.huggingface_models",

        "sql": """
            SELECT COUNT(*)
            FROM raw.huggingface_models
            WHERE likes < 0
        """
    },

    {
        "check_name": "stage_hf_row_count_gt_zero",

        "table_name": "stage.stg_huggingface_models",

        "sql": """
            SELECT COUNT(*)
            FROM stage.stg_huggingface_models
        """,

        "expected_result": "GREATER_THAN_ZERO"
    }
]