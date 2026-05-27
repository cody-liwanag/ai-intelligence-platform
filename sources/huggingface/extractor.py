import time
import requests
import pandas as pd


HUGGINGFACE_API_URL = (
    "https://huggingface.co/api/models"
)


AI_SEARCH_TOPICS = [
    "artificial intelligence",
    "machine learning",
    "large language model",
    "llm",
    "generative ai",
    "retrieval augmented generation",
    "rag",
    "ai agents"
]


def extract_huggingface_models():

    all_records = []

    for topic in AI_SEARCH_TOPICS:

        print(
            f"Extracting Hugging Face models for topic: {topic}"
        )

        MAX_RETRIES = 3

        for attempt in range(MAX_RETRIES):

            try:

                response = requests.get(
                    HUGGINGFACE_API_URL,
                    params={
                        "search": topic,
                        "limit": 50,
                        "sort": "downloads",
                        "direction": -1
                    },
                    timeout=30
                )

                response.raise_for_status()

                break

            except requests.exceptions.RequestException as e:

                print(
                    f"Hugging Face request failed: {e}"
                )

                if attempt < MAX_RETRIES - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    raise

        models = response.json()

        for model in models:

            all_records.append({

                "search_topic":
                    topic,

                "model_id":
                    model.get("id"),

                "author":
                    model.get("author"),

                "downloads":
                    model.get("downloads") or 0,

                "likes":
                    model.get("likes") or 0,

                "pipeline_tag":
                    model.get("pipeline_tag"),

                "last_modified":
                    model.get("lastModified"),

                "private":
                    model.get("private") or 0,

                "gated":
                    model.get("gated")
            })

    dataframe = pd.DataFrame(all_records)

    print(
        f"Extracted {len(dataframe)} "
        f"Hugging Face model rows"
    )

    return dataframe