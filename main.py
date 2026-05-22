from warehouse.init_db import initialise_database
from warehouse.run_stage_models import run_stage_models
from warehouse.run_mart_models import run_mart_models

from quality.run_quality_checks import run_quality_checks
from schema_drift.check_schema_drift import check_schema_drift
from storage.raw_parquet import save_raw_parquet
from serving.postgres_publisher import publish_marts_to_postgres

from metadata.logger import log_ingestion_run
from config.source_registry import SOURCES


def run_source(source_config):
    source_name = source_config["source_name"]
    extractor = source_config["extractor"]
    loader = source_config["loader"]
    contract_path = source_config["contract_path"]
    raw_file_prefix = source_config["raw_file_prefix"]

    print(f"Starting source pipeline: {source_name}")

    raw_file_path = None
    rows_loaded = 0

    try:
        df = extractor()

        raw_file_path = save_raw_parquet(
            df=df,
            source_prefix=raw_file_prefix
        )

        check_schema_drift(
            df=df,
            contract_path=contract_path
        )

        rows_loaded = loader(df)

        log_ingestion_run(
            source_name=source_name,
            status="SUCCESS",
            rows_loaded=rows_loaded,
            raw_file_path=raw_file_path
        )

        print(
            f"Completed source pipeline: {source_name}. "
            f"Rows loaded: {rows_loaded}. "
            f"Raw file: {raw_file_path}"
        )

        return {
            "source_name": source_name,
            "rows_loaded": rows_loaded,
            "raw_file_path": raw_file_path
        }

    except Exception as e:
        log_ingestion_run(
            source_name=source_name,
            status="FAILED",
            rows_loaded=rows_loaded,
            raw_file_path=raw_file_path,
            error_message=str(e)
        )

        print(f"Source pipeline failed: {source_name}")
        raise


def main():
    try:
        initialise_database()

        source_results = []

        for source_config in SOURCES:
            source_result = run_source(source_config)
            source_results.append(source_result)

        run_stage_models()

        run_mart_models()

        run_quality_checks()

        publish_marts_to_postgres()

        print("Pipeline completed successfully")

    except Exception as e:
        print(f"Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()