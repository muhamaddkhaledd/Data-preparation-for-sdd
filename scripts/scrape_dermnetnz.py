import requests
from bs4 import BeautifulSoup
import string
import time
from urllib.parse import urljoin
import pandas as pd
import json
import os

def get_topic_urls(base_url="https://dermnetnz.org/topics"):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    url_list = []

    for letter in string.ascii_uppercase:
        div = soup.find('div', {'class': 'topics__wrap__grid__column', 'data-letter': letter})
        if not div:
            continue
        links = [urljoin(base_url, a['href']) for a in div.select('.topics__wrap__grid__column__list a')]
        url_list.extend(links)

    return url_list

def scrape_qa_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    qa_data = []

    h2_elements = soup.find_all('h2')

    for h2 in h2_elements:
        question = h2.text.strip()
        answer_parts = []

        current = h2.next_sibling

        while current and (not hasattr(current, 'name') or current.name != 'h2'):
            if hasattr(current, 'name'):
                if current.name == 'p':
                    answer_parts.append(current.text.strip())
                elif current.name == 'ul':
                    list_items = [f"• {li.text.strip()}" for li in current.find_all('li')]
                    answer_parts.append("\n".join(list_items))
            current = current.next_sibling

        answer = "\n\n".join([part for part in answer_parts if part])
        qa_data.append({"prompt": question, "response": answer})

    return qa_data

def clean_qa_data(qa_list):
    return [qa for qa in qa_list if qa.get('prompt') and qa.get('response') and str(qa['prompt']).strip() and str(qa['response']).strip()]

def scrape_dermnetnz():
    urls = get_topic_urls()
    all_qa = []

    for url in urls:
        try:
            all_qa.extend(scrape_qa_from_url(url))
            time.sleep(1)  # Be polite
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return pd.DataFrame(clean_qa_data(all_qa))



if __name__ == "__main__":
    df = scrape_dermnetnz()

    os.makedirs("data", exist_ok=True)

    output_path = "data/skin_diseases_chatbot_data.json"
    df.to_json(output_path, orient="records", indent=2, force_ascii=False)

    print(f"Saved {len(df)} QA pairs to {output_path}")
