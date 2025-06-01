import os
import zipfile

import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
from datasets import load_dataset

def load_dataset1():
    print("Downloading Kaggle dataset...")
    download_dir = kagglehub.dataset_download("muhammadareebkhan/skin-disease-medical-text-data-for-fine-tuning")
    zip_path = os.path.join(download_dir, "skin-disease-medical-text-data-for-fine-tuning.zip")
    extracted_csv_path = os.path.join(download_dir, "combined_data.csv")

    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extract("combined_data.csv", download_dir)
    else:
        print("Zip file not found, assuming CSV is already extracted.")

    try:
        data = pd.read_csv(extracted_csv_path, encoding='utf-8', engine='python', on_bad_lines='warn')
    except UnicodeDecodeError:
        data = pd.read_csv(extracted_csv_path, encoding='latin1', engine='python', on_bad_lines='warn')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        raise

    return data[["prompt", "response"]]


def load_dataset2():
    dataset = load_dataset('UCSD26/medical_dialog', name="processed.en", trust_remote_code=True)
    return dataset["train"]

if __name__ == "__main__":
    data1 = load_dataset1()
    print(data1.head())

    data2_train = load_dataset2()
    print(f"Dataset2 train size: {len(data2_train)}")
