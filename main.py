# main.py

from scripts.load_datasets import load_dataset1, load_dataset2
from scripts.preprocess_dataset2 import preprocess_dataset2
from scripts.scrape_dermnetnz import scrape_dermnetnz
from scripts.clean_data import combine_and_clean_datasets
from scripts.save_and_upload import save_dataset, upload_to_s3


def main():
    print("[1/5] Loading datasets...")
    data1 = load_dataset1()
    data2_raw = load_dataset2()

    print("[2/5] Preprocessing Dataset 2...")
    data2 = preprocess_dataset2(data2_raw)

    print("[3/5] Scraping DermNetNZ...")
    data3 = scrape_dermnetnz()

    print("[4/5] Combining and cleaning datasets...")
    final_data = combine_and_clean_datasets(data1, data2, data3)

    print("[5/5] Saving and uploading final dataset...")
    final_path = "data/skin_Diseases_chatbot_final_data.json"
    save_dataset(final_data, final_path)
    upload_to_s3(final_path)

    print("All steps completed successfully!")


if __name__ == "__main__":
    main()
