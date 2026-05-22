import duckdb
from config.paths import DUCKDB_PATH

def load(df):

    conn = duckdb.connect(DUCKDB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw.github_repositories (
            search_topic VARCHAR,
            repo_id BIGINT,
            repo_name VARCHAR,
            full_name VARCHAR,
            description VARCHAR,
            stars INTEGER,
            forks INTEGER,
            language VARCHAR,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            repo_url VARCHAR
        )
    """)

    conn.register("source_df", df)

    conn.sql("""
        INSERT INTO raw.github_repositories
        SELECT *
        FROM source_df AS source
        WHERE NOT EXISTS (
            SELECT 1
            FROM raw.github_repositories AS target
            WHERE target.repo_id = source.repo_id
              AND target.search_topic = source.search_topic
        )
    """)

    rows_loaded = conn.execute("""
        SELECT COUNT(*)
        FROM raw.github_repositories
    """).fetchone()[0]

    conn.close()

    print("Total rows in raw.github_repositories:", rows_loaded)

    return rows_loaded
