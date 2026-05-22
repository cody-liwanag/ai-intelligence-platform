from datetime import datetime
import os 

def save_raw_parquet(df, source_name):
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    folder_path = f"data/raw/{source_name}"

    os.makedirs(folder_path, exist_ok=True)

    file_path = f"{folder_path}/{source_name}_{timestamp}.parquet"

    df.to_parquet(file_path, index=False)

    print(f"Raw Parquet Saved: {file_path}")

    return file_path