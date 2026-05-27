import duckdb

from datetime import datetime

from config.paths import DUCKDB_PATH

from quality.checks.github_quality_checks import (
    GITHUB_QUALITY_CHECKS
)

from quality.checks.huggingface_quality_checks import (
    HUGGINGFACE_QUALITY_CHECKS
)

from quality.checks.jobs_quality_checks import (
    JOBS_QUALITY_CHECKS
)

from quality.checks.pricing_quality_checks import (
    PRICING_QUALITY_CHECKS
)


QUALITY_CHECKS = (
    GITHUB_QUALITY_CHECKS
    + HUGGINGFACE_QUALITY_CHECKS
    + JOBS_QUALITY_CHECKS
    + PRICING_QUALITY_CHECKS
)


def run_quality_checks():

    conn = duckdb.connect(str(DUCKDB_PATH))

    result = conn.execute("""

        SELECT COALESCE(MAX(quality_run_id), 0) + 1

        FROM metadata.quality_runs

    """).fetchone()

    quality_run_id = result[0]

    passed_checks = 0
    failed_checks = 0

    print("Running data quality checks...")

    for check in QUALITY_CHECKS:

        check_name = check["check_name"]

        print(f"Running quality check: {check_name}")

        try:

            result = conn.execute(
                check["sql"]
            ).fetchone()[0]

            expected_result = check.get(
                "expected_result",
                "ZERO"
            )

            if expected_result == "ZERO":

                status = (
                    "PASSED"
                    if result == 0
                    else "FAILED"
                )

            elif expected_result == "GREATER_THAN_ZERO":

                status = (
                    "PASSED"
                    if result > 0
                    else "FAILED"
                )

            else:

                status = "FAILED"

            error_message = None

        except Exception as error:

            result = -1

            status = "FAILED"

            error_message = str(error)

        if status == "PASSED":

            passed_checks += 1

        else:

            failed_checks += 1

        conn.execute("""

            INSERT INTO metadata.quality_results (

                quality_run_id,
                check_name,
                table_name,
                status,
                failed_row_count,
                check_timestamp,
                error_message

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)

        """, [

            quality_run_id,
            check_name,
            check["table_name"],
            status,
            result,
            datetime.now(),
            error_message

        ])

        print(f"{status}: {check_name}")

    overall_status = (
        "PASSED"
        if failed_checks == 0
        else "FAILED"
    )

    conn.execute("""

        INSERT INTO metadata.quality_runs (

            quality_run_id,
            run_timestamp,
            status,
            total_checks,
            passed_checks,
            failed_checks

        )

        VALUES (?, ?, ?, ?, ?, ?)

    """, [

        quality_run_id,
        datetime.now(),
        overall_status,
        len(QUALITY_CHECKS),
        passed_checks,
        failed_checks

    ])

    conn.close()

    print(

        f"Quality checks completed: "

        f"{overall_status} "

        f"({passed_checks}/{len(QUALITY_CHECKS)} passed)"

    )

    if overall_status == "FAILED":

        raise Exception(
            "Data quality checks failed"
        )