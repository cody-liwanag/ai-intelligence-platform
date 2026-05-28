from dotenv import load_dotenv

load_dotenv()

import os
import time
import requests
import pandas as pd


ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
ADZUNA_COUNTRY = os.getenv("ADZUNA_COUNTRY", "gb")


AI_SEARCH_TOPICS = [
    "artificial intelligence",
    "machine learning",
    "large language model",
    "llm",
    "generative ai",
    "retrieval augmented generation",
    "rag",
    "ai agents",
]


def extract_jobs():

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:

        raise ValueError(
            "Missing ADZUNA_APP_ID or ADZUNA_APP_KEY environment variable"
        )

    all_records = []

    for topic in AI_SEARCH_TOPICS:

        print(f"Fetching jobs for topic: {topic}")

        url = (
            f"https://api.adzuna.com/v1/api/jobs/"
            f"{ADZUNA_COUNTRY}/search/1"
        )

        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "results_per_page": 50,
            "what": topic,
            "content-type": "application/json",
        }

        MAX_RETRIES = 3

        for attempt in range(MAX_RETRIES):

            try:

                response = requests.get(
                    url,
                    params=params,
                    timeout=30,
                )

                response.raise_for_status()

                break

            except requests.exceptions.RequestException as e:

                print(f"Jobs API request failed: {e}")

                if attempt < MAX_RETRIES - 1:

                    wait_time = 2 ** attempt

                    print(f"Retrying in {wait_time} seconds...")

                    time.sleep(wait_time)

                else:

                    raise

        data = response.json()

        jobs = data.get("results", [])

        total_results = data.get("count", 0)

        print(
            f"Estimated total market demand "
            f"for {topic}: {total_results}"
        )

        for job in jobs:

            company = job.get("company") or {}

            location = job.get("location") or {}

            category = job.get("category") or {}

            all_records.append(
                {
                    "search_topic": topic,

                    "estimated_market_demand":
                        total_results,

                    "job_id":
                        job.get("id"),

                    "job_title":
                        job.get("title"),

                    "company_name":
                        company.get("display_name"),

                    "location_name":
                        location.get("display_name"),

                    "category_label":
                        category.get("label"),

                    "contract_type":
                        job.get("contract_type"),

                    "created_at":
                        job.get("created"),

                    "salary_min":
                        job.get("salary_min"),

                    "salary_max":
                        job.get("salary_max"),

                    "salary_is_predicted":
                        job.get("salary_is_predicted"),

                    "redirect_url":
                        job.get("redirect_url"),

                    "source_platform":
                        "adzuna",
                }
            )

    dataframe = pd.DataFrame(all_records)

    print(f"Extracted {len(dataframe)} job rows")

    return dataframe