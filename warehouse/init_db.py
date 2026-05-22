import duckdb

DB_PATH = "~/projects/ai-intelligence-platform/warehouse/duckdb/platform.duckdb"

def initialise_database():
    conn = duckdb.connect(DB_PATH)

    conn.execute("""
                 CREATE SCHEMA IF NOT EXISTS raw;
                 """)
    
    conn.execute("""
                 CREATE SCHEMA IF NOT EXISTS stage;
                 """)
    
    conn.execute("""
                 CREATE SCHEMA IF NOT EXISTS marts;
                 """)
    
    conn.execute("""
                 CREATE SCHEMA IF NOT EXISTS metadata;
                 """)
    
    with open("warehouse/ddl/init_metadata.sql", "r") as file:
        metadata_sql = file.read()

    conn.execute(metadata_sql)

    conn.close()

    print("Database initialised successfully")