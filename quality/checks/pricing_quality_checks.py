PRICING_QUALITY_CHECKS = [

    {
        "check_name":
            "raw_pricing_model_name_not_null",

        "table_name":
            "raw.model_pricing",

        "sql": """

            SELECT COUNT(*)

            FROM raw.model_pricing

            WHERE model_name IS NULL

        """
    },

    {
        "check_name":
            "stage_pricing_row_count_gt_zero",

        "table_name":
            "stage.stg_model_pricing",

        "sql": """

            SELECT COUNT(*)

            FROM stage.stg_model_pricing

        """,

        "expected_result":
            "GREATER_THAN_ZERO"
    }
]