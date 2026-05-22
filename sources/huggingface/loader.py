import duckdb

from config.paths import DUCKDB_PATH


def load_huggingface_models(dataframe):

    connection = duckdb.connect(str(DUCKDB_PATH))

    connection.execute(
        """
        CREATE SCHEMA IF NOT EXISTS raw
        """
    )

    connection.register(
        "huggingface_dataframe",
        dataframe
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE raw.huggingface_models AS

        SELECT *
        FROM huggingface_dataframe
        """
    )

    connection.close()

    print(
        "Loaded Hugging Face models into raw.huggingface_models"
    )