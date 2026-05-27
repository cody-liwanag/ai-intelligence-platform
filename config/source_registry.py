from sources.github.extractor import extract as extract_github
from sources.github.loader import load as load_github
from sources.huggingface.extractor import extract_huggingface_models
from sources.huggingface.loader import load_huggingface_models
from sources.jobs.extractor import extract_jobs
from sources.jobs.loader import load_raw_jobs_data
from sources.pricing.extractor import extract_pricing_models
from sources.pricing.loader import load_raw_pricing_data



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
    },

    {
    "source_name": "jobs",

    "extractor": extract_jobs,

    "loader": load_raw_jobs_data,

    "contract_path": "sources/jobs/contract.json",

    "raw_file_prefix": "jobs"
    },

    {
    "source_name": "pricing_models",

    "extractor": extract_pricing_models,

    "loader": load_raw_pricing_data,

    "contract_path":
        "sources/pricing/contract.json",

    "raw_file_prefix":
        "pricing_models"
    }

]
