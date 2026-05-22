from datetime import datetime
from pathlib import Path


def save_raw_parquet(df, source_prefix):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    output_dir = Path(f"data/raw/{source_prefix}")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{source_prefix}_{timestamp}.parquet"

    df.to_parquet(output_path, index=False)

    print(f"Raw Parquet saved: {output_path}")

    return str(output_path)