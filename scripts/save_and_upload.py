# scripts/save_and_upload.py

import boto3
import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # Load AWS credentials from .env

def save_dataset(df, path):
    df.to_json(path, orient="records", indent=4)

def upload_to_s3(file_path, bucket_name="skin-diseases-chatbot-dataset"):

    s3_file_key = "skin_Diseases_chatbot_final_data111.json"
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    s3.upload_file(file_path, bucket_name, s3_file_key)
    print(f"Uploaded {file_path} to S3 bucket '{bucket_name}' as '{s3_file_key}'")


if __name__ == "__main__":
    # File paths
    input_path = Path(__file__).resolve().parent.parent / "data" / "skin_Diseases_chatbot_final_data.json"
    output_path = input_path  # Optional: can save a cleaned copy again if needed

    # Load data
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
    else:
        # Upload to S3
        upload_to_s3(output_path)
