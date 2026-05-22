.PHONY: help run init quality publish drift clean reset up down


help:
	@echo "Available commands:"
	@echo ""
	@echo "  make run       - Run full pipeline"
	@echo "  make init      - Initialize DuckDB metadata tables"
	@echo "  make quality   - Run quality checks"
	@echo "  make publish   - Publish marts to Postgres"
	@echo "  make drift     - Run schema drift checks"
	@echo "  make up        - Start Docker services"
	@echo "  make down      - Stop Docker services"
	@echo "  make clean     - Remove Python cache files"
	@echo "  make reset     - Reset DuckDB database"


run:
	python main.py


init:
	python -m warehouse.init_db


quality:
	python -m quality.run_quality_checks


publish:
	python -m serving.postgres_publisher


drift:
	python -m schema_drift.check_schema_drift


up:
	docker compose up -d


down:
	docker compose down


clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete


reset:
	rm -f warehouse/duckdb/platform.duckdb
