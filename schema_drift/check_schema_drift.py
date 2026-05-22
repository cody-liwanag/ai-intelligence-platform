import json
from datetime import datetime

import duckdb


DB_PATH = "warehouse/duckdb/platform.duckdb"


def load_schema_contract(contract_path):

    with open(contract_path, "r") as file:
        contract = json.load(file)

    return contract


def get_next_drift_run_id(conn):

    result = conn.execute("""
        SELECT COALESCE(MAX(drift_run_id), 0) + 1
        FROM metadata.schema_drift_runs
    """).fetchone()

    return result[0]


def check_schema_drift(df, contract_path):

    conn = duckdb.connect(DB_PATH)

    contract = load_schema_contract(contract_path)

    source_name = contract["source_name"]
    expected_columns = contract["columns"]

    actual_columns = {
        column_name: str(dtype)
        for column_name, dtype in df.dtypes.items()
    }

    drift_run_id = get_next_drift_run_id(conn)

    missing_columns = []
    unexpected_columns = []
    datatype_mismatches = []

    print(f"Checking schema drift for {source_name}...")

    for column_name, column_contract in expected_columns.items():

        expected_type = column_contract["expected_type"]
        required = column_contract["required"]

        if column_name not in actual_columns:

            severity = "CRITICAL" if required else "WARNING"

            missing_columns.append({
                "column_name": column_name,
                "expected_type": expected_type,
                "actual_type": None,
                "severity": severity
            })

        else:

            actual_type = actual_columns[column_name]

            if actual_type != expected_type:

                datatype_mismatches.append({
                    "column_name": column_name,
                    "expected_type": expected_type,
                    "actual_type": actual_type,
                    "severity": "WARNING"
                })

    for column_name, actual_type in actual_columns.items():

        if column_name not in expected_columns:

            unexpected_columns.append({
                "column_name": column_name,
                "expected_type": None,
                "actual_type": actual_type,
                "severity": "WARNING"
            })

    drift_events = []

    for drift in missing_columns:
        drift_events.append({"drift_type": "MISSING_COLUMN", **drift})

    for drift in unexpected_columns:
        drift_events.append({"drift_type": "UNEXPECTED_COLUMN", **drift})

    for drift in datatype_mismatches:
        drift_events.append({"drift_type": "DATATYPE_MISMATCH", **drift})

    for event in drift_events:

        conn.execute("""
            INSERT INTO metadata.schema_drift_results
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            drift_run_id,
            source_name,
            event["column_name"],
            event["drift_type"],
            event["expected_type"],
            event["actual_type"],
            event["severity"],
            datetime.now()
        ])

    critical_issue_count = sum(
        1
        for event in drift_events
        if event["severity"] == "CRITICAL"
    )

    status = "PASSED" if critical_issue_count == 0 else "FAILED"

    conn.execute("""
        INSERT INTO metadata.schema_drift_runs
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        drift_run_id,
        datetime.now(),
        source_name,
        status,
        len(expected_columns),
        len(actual_columns),
        len(missing_columns),
        len(unexpected_columns),
        len(datatype_mismatches)
    ])

    conn.close()

    print(
        f"Schema drift check completed for {source_name}: {status} "
        f"({len(drift_events)} drift events found)"
    )

    if status == "FAILED":
        raise Exception(f"Critical schema drift detected for {source_name}")