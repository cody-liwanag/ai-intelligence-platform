import time 
import requests
import pandas as pd


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


def extract():

    all_records = []

    url = "https://api.github.com/search/repositories"

    for topic in AI_SEARCH_TOPICS:

        print(f"Fetching topic: {topic}")

        params = {
            "q": topic,
            "sort": "stars",
            "order": "desc",
            "per_page": 50
        }

        MAX_RETRIES = 3

        for attempt in range(MAX_RETRIES):

            try:

                response = requests.get(
                    url,
                    params=params,
                    timeout=30
                )

                response.raise_for_status()

                break

            except requests.exceptions.RequestException as e:

                print(f"GitHub API request failed: {e}")

                if attempt < MAX_RETRIES - 1:

                    wait_time = 2 ** attempt

                    print(f"Retrying in {wait_time} seconds...")

                    time.sleep(wait_time)

                else:

                    raise

        data = response.json()

        repositories = data.get("items", [])

        print(f"Repositories returned for {topic}: {len(repositories)}")

        for repo in repositories:

            all_records.append({
                "search_topic": topic,
                "repo_id": repo.get("id"),
                "repo_name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "description": repo.get("description"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count"),
                "language": repo.get("language"),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "repo_url": repo.get("html_url")
            })

    if not all_records:

        raise Exception("No records returned from GitHub API")

    df = pd.DataFrame(all_records)

    print("Records by topic:")

    print(df["search_topic"].value_counts())

    return df