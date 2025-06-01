import pandas as pd
import os
import json

def combine_and_clean_datasets(data1, data2, data3):
    combined = pd.concat([data1, data2, data3], ignore_index=True)
    combined.dropna(subset=["prompt", "response"], inplace=True)
    combined.drop_duplicates(inplace=True)
    return combined

if __name__ == "__main__":
    # Load datasets
    data1 = pd.read_csv("data/combined_data.csv")
    data2 = pd.read_json("data/ucsd26_cleaned_dataset.json")
    data3 = pd.read_json("data/skin_diseases_chatbot_data.json")

    # Combine and clean
    final_data = combine_and_clean_datasets(data1, data2, data3)

    # Save the cleaned data
    os.makedirs("data", exist_ok=True)
    output_path = "data/skin_Diseases_chatbot_final_data.json"
    final_data.to_json(output_path, orient="records", indent=2, force_ascii=False)

    print(f"Final cleaned dataset saved to {output_path}")
    print(f"Number of samples: {len(final_data)}")
