import pandas as pd

def preprocess_dataset2(train_data):
    data_list = []

    for sample in train_data:
        description = sample["description"]
        doctor_response = next((utt for utt in sample["utterances"] if utt.lower().startswith("doctor:")), None)

        if doctor_response:
            doctor_response = doctor_response.replace("doctor:", "").strip()

        data_list.append({
            "prompt": description,
            "response": doctor_response
        })

    return pd.DataFrame(data_list)

if __name__ == "__main__":
    from load_datasets import load_dataset2
    train_data = load_dataset2()
    data2 = preprocess_dataset2(train_data)
    print(data2.head())
