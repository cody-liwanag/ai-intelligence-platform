from ingestion.extract.github_extract import fetch_github_repositories
from ingestion.loaders.raw_loader import load_raw_github_data
from ingestion.utils.parquet_utils import save_raw_parquet
from ingestion.utils.metadata_logger import log_ingestion_run
from warehouse.init_db import initialise_database
from warehouse.run_stage_models import run_stage_models
from warehouse.run_mart_models import run_mart_models
from serving.postgres_publisher import publish_marts_to_postgres
from quality.run_quality_checks import run_quality_checks
from schema_drift.check_schema_drift import check_github_schema_drift

def main():

    initialise_database()
    
    try:
        print("Fetching Github repository data...")

        github_df = fetch_github_repositories()
    
        print("Rows extracted:", len(github_df))

        raw_file_path = save_raw_parquet(github_df,"github")

        check_github_schema_drift(github_df)

        print("Loading data into DuckDB raw layer...")

        load_raw_github_data(github_df)

        run_stage_models()

        run_mart_models()

        run_quality_checks()

        publish_marts_to_postgres()

        log_ingestion_run(
        source_name="github",
        status="SUCCESS",
        rows_loaded=len(github_df),
        raw_file_path=raw_file_path
        )
    except Exception as e:

        print("Pipeline failed:",str(e))

        log_ingestion_run(
            source_name="Github",
            status='FAILED',
            rows_loaded=0,
            raw_file_path=None,
            error_message=str(e)
        )
if __name__ == "__main__":
    main()

    