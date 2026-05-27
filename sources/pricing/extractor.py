import time
import requests
import pandas as pd


OPENROUTER_MODELS_URL = (
    "https://openrouter.ai/api/v1/models"
)


def classify_search_topic(model_name):

    model_name = model_name.lower()

    if "embed" in model_name:
        return "retrieval augmented generation"

    if "agent" in model_name:
        return "ai agents"

    return "llm"


def extract_pricing_models():

    print(
        "Extracting model pricing data..."
    )

    MAX_RETRIES = 3

    for attempt in range(MAX_RETRIES):

        try:

            response = requests.get(
                OPENROUTER_MODELS_URL,
                timeout=30
            )

            response.raise_for_status()

            break

        except requests.exceptions.RequestException as e:

            print(
                f"Pricing API request failed: {e}"
            )

            if attempt < MAX_RETRIES - 1:

                wait_time = 2 ** attempt

                print(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                raise

    data = response.json()

    models = data.get(
        "data",
        []
    )

    all_records = []

    for model in models:

        pricing = model.get(
            "pricing",
            {}
        )

        all_records.append({

            "provider_name": model.get(
                "id",
                ""
            ).split("/")[0],

            "model_name": model.get("id"),

            "input_price_per_million":

                pricing.get("prompt"),

            "output_price_per_million":

                pricing.get("completion"),

            "context_window":

                model.get("context_length"),

            "model_family":

                model.get("architecture", {})
                .get("modality"),

            "pricing_source":

                "openrouter",

            "pricing_snapshot_date":

                pd.Timestamp.now(),

            "search_topic":

                classify_search_topic(
                    model.get("id", "")
                )
        })

    dataframe = pd.DataFrame(
        all_records
    )

    print(
        f"Extracted {len(dataframe)} pricing rows"
    )

    return dataframe