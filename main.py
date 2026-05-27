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

    print("\n" + "=" * 60)
    print(f"STARTING SOURCE PIPELINE: {source_name}")
    print("=" * 60)

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

        print(f"\nSUCCESS: {source_name}")
        print(f"Rows loaded: {rows_loaded}")
        print(f"Raw file: {raw_file_path}")

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

        print(f"\nFAILED SOURCE: {source_name}")

        raise


def main():

    try:

        initialise_database()

        source_results = []

        failed_sources = []

        for source_config in SOURCES:

            try:

                source_result = run_source(source_config)

                source_results.append(source_result)

            except Exception as e:

                source_name = source_config["source_name"]

                print("\n" + "-" * 60)
                print(
                    f"PIPELINE CONTINUING DESPITE FAILURE: "
                    f"{source_name}"
                )
                print("-" * 60)

                print(e)

                failed_sources.append(source_name)

        if failed_sources:

            print("\n" + "=" * 60)
            print("WARNING: SOME SOURCES FAILED")
            print("=" * 60)

            for failed_source in failed_sources:

                print(f"- {failed_source}")

        print("\n" + "=" * 60)
        print("BUILDING STAGE MODELS")
        print("=" * 60)

        run_stage_models()

        print("\n" + "=" * 60)
        print("BUILDING MART MODELS")
        print("=" * 60)

        run_mart_models()

        print("\n" + "=" * 60)
        print("RUNNING QUALITY CHECKS")
        print("=" * 60)

        run_quality_checks()

        print("\n" + "=" * 60)
        print("PUBLISHING MARTS TO POSTGRES")
        print("=" * 60)

        publish_marts_to_postgres()

        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception as e:

        print(f"\nPIPELINE FAILED: {str(e)}")

        raise


if __name__ == "__main__":

    main()