from sources.github.extractor import extract as extract_github
from sources.github.loader import load as load_github
from sources.huggingface.extractor import extract_huggingface_models
from sources.huggingface.loader import load_huggingface_models


SOURCES = [
    {
        "source_name": "github_repositories",
        "extractor": extract_github,
        "loader": load_github,
        "contract_path": "sources/github/contract.json",
        "raw_file_prefix": "github"
    },
    
    {
    "source_name": "huggingface_models",
    "extractor": extract_huggingface_models,
    "loader": load_huggingface_models,
    "contract_path": "sources/huggingface/contract.json",
    "raw_file_prefix": "huggingface_models"
    }
]
