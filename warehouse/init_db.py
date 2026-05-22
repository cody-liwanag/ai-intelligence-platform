import duckdb
from config.paths import DUCKDB_PATH

def initialise_database():
    conn = duckdb.connect(DUCKDB_PATH)

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