import duckdb
from datetime import datetime
from config.paths import DUCKDB_PATH

QUALITY_CHECKS = [
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
        "check_name": "raw_github_unique_repo_topic",
        "table_name": "raw.github_repositories",
        "sql": """
            SELECT COUNT(*)
            FROM (
                SELECT
                    repo_id,
                    search_topic,
                    COUNT(*) AS duplicate_count
                FROM raw.github_repositories
                GROUP BY
                    repo_id,
                    search_topic
                HAVING COUNT(*) > 1
            )
        """
    },
    {
        "check_name": "stage_github_row_count_greater_than_zero",
        "table_name": "stage.stg_github_repositories",
        "sql": """
            SELECT
                CASE
                    WHEN COUNT(*) = 0 THEN 1
                    ELSE 0
                END
            FROM stage.stg_github_repositories
        """
    },
    {
        "check_name": "mart_ai_topic_summary_row_count_greater_than_zero",
        "table_name": "marts.ai_topic_summary",
        "sql": """
            SELECT
                CASE
                    WHEN COUNT(*) = 0 THEN 1
                    ELSE 0
                END
            FROM marts.ai_topic_summary
        """
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


def get_next_quality_run_id(conn):

    result = conn.execute("""
        SELECT COALESCE(MAX(quality_run_id), 0) + 1
        FROM metadata.quality_runs
    """).fetchone()

    return result[0]


def run_quality_checks():

    conn = duckdb.connect(DUCKDB_PATH)

    quality_run_id = get_next_quality_run_id(conn)

    total_checks = len(QUALITY_CHECKS)
    passed_checks = 0
    failed_checks = 0

    print("Running data quality checks...")

    for check in QUALITY_CHECKS:

        check_name = check["check_name"]
        table_name = check["table_name"]
        check_sql = check["sql"]

        try:
            failed_row_count = conn.execute(check_sql).fetchone()[0]

            if failed_row_count == 0:
                status = "PASSED"
                passed_checks += 1
                error_message = None
            else:
                status = "FAILED"
                failed_checks += 1
                error_message = f"Check failed with {failed_row_count} failing rows"

            conn.execute("""
                INSERT INTO metadata.quality_results
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                quality_run_id,
                check_name,
                table_name,
                status,
                failed_row_count,
                datetime.now(),
                error_message
            ])

            print(f"{status}: {check_name}")

        except Exception as e:

            failed_checks += 1

            conn.execute("""
                INSERT INTO metadata.quality_results
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                quality_run_id,
                check_name,
                table_name,
                "ERROR",
                None,
                datetime.now(),
                str(e)
            ])

            print(f"ERROR: {check_name} - {str(e)}")

    overall_status = "PASSED" if failed_checks == 0 else "FAILED"

    conn.execute("""
        INSERT INTO metadata.quality_runs
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        quality_run_id,
        datetime.now(),
        overall_status,
        total_checks,
        passed_checks,
        failed_checks
    ])

    conn.close()

    print(
        f"Quality checks completed: {overall_status} "
        f"({passed_checks}/{total_checks} passed)"
    )

    if overall_status == "FAILED":
        raise Exception("Data quality checks failed")