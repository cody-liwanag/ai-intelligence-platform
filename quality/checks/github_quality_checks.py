GITHUB_QUALITY_CHECKS = [

    {
        "check_name": "raw_github_repo_id_not_null",

        "table_name": "raw.github_repositories",

        "sql": """
            SELECT COUNT(*)
            FROM raw.github_repositories
            WHERE repo_id IS NULL
        """
    },

    {
        "check_name": "raw_github_search_topic_not_null",

        "table_name": "raw.github_repositories",

        "sql": """
            SELECT COUNT(*)
            FROM raw.github_repositories
            WHERE search_topic IS NULL
        """
    },

    {
        "check_name": "raw_github_no_negative_stars",

        "table_name": "raw.github_repositories",

        "sql": """
            SELECT COUNT(*)
            FROM raw.github_repositories
            WHERE stars < 0
        """
    },

    {
        "check_name": "raw_github_no_negative_forks",

        "table_name": "raw.github_repositories",

        "sql": """
            SELECT COUNT(*)
            FROM raw.github_repositories
            WHERE forks < 0
        """
    },

    {
        "check_name": "stage_github_row_count_gt_zero",

        "table_name": "stage.stg_github_repositories",

        "sql": """
            SELECT COUNT(*)
            FROM stage.stg_github_repositories
        """,

        "expected_result": "GREATER_THAN_ZERO"
    },

    {
        "check_name": "mart_ai_topic_summary_unique_topic_snapshot",

        "table_name": "marts.ai_topic_summary",

        "sql": """
            SELECT COUNT(*)

            FROM (

                SELECT
                    search_topic,
                    snapshot_date,
                    COUNT(*) AS duplicate_count

                FROM marts.ai_topic_summary

                GROUP BY
                    search_topic,
                    snapshot_date

                HAVING COUNT(*) > 1

            )
        """
    }
]