from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Warehouse

WAREHOUSE_DIR = PROJECT_ROOT / "warehouse"

DUCKDB_DIR = WAREHOUSE_DIR / "duckdb"

DUCKDB_PATH = DUCKDB_DIR / "platform.duckdb"

SQL_DIR = WAREHOUSE_DIR / "sql"

STAGE_SQL_DIR = SQL_DIR / "stage"

MART_SQL_DIR = SQL_DIR / "marts"

DDL_DIR = WAREHOUSE_DIR / "ddl"


# Sources

SOURCES_DIR = PROJECT_ROOT / "sources"


# Storage

STORAGE_DIR = PROJECT_ROOT / "storage"

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# Quality

QUALITY_DIR = PROJECT_ROOT / "quality"


# Metadata

METADATA_DIR = PROJECT_ROOT / "metadata"


# Logs

LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(exist_ok=True)


# Contracts

CONTRACTS_DIR = SOURCES_DIR