from sources.github.extractor import extract as extract_github
from sources.github.loader import load as load_github


SOURCES = [
    {
        "source_name": "github_repositories",
        "extractor": extract_github,
        "loader": load_github,
        "contract_path": "sources/github/contract.json",
        "raw_file_prefix": "github"
    }
]
