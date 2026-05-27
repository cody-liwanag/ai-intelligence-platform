JOBS_QUALITY_CHECKS = [

    {
        "check_name": "raw_jobs_job_id_not_null",

        "table_name": "raw.jobs",

        "sql": """

            SELECT COUNT(*)

            FROM raw.jobs

            WHERE job_id IS NULL

        """
    },

    {
        "check_name": "stage_jobs_row_count_gt_zero",

        "table_name": "stage.stg_jobs",

        "sql": """

            SELECT COUNT(*)

            FROM stage.stg_jobs

        """,

        "expected_result": "GREATER_THAN_ZERO"
    },
]
