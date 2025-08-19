import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

df = pd.read_excel('Input.xlsx')

output_dir = 'Extracted_Data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    print(f"Scraping URL ID: {url_id} | URL: {url}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        article_title_element = soup.find('h1')
        if not article_title_element:
            article_title_element = soup.find('h2')
        if not article_title_element:
            article_title_element = soup.find('h3')
        if not article_title_element:
            article_title_element = soup.find('h4')

        article_title = article_title_element.get_text(strip=True) if article_title_element else "Title Not Found"

        article_body_element = soup.find('div', class_='td-post-content')
        if not article_body_element:
            article_body_element = soup.find('div', class_='entry-content')
        if not article_body_element:
            article_body_element = soup.find('article')

        if article_body_element:
            paragraphs = article_body_element.find_all('p')
            article_body = "\n".join([p.get_text(strip=True) for p in paragraphs])
        else:
            article_body = "Body Content Not Found"

        full_article_text = f"{article_title}\n\n{article_body}"

        output_filename = os.path.join(output_dir, f'{url_id}.txt')

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(full_article_text)

        print(f"Successfully saved: {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"  -> Failed to fetch URL {url_id}: {e}")
    except Exception as e:
        print(f"  -> An error occurred while processing {url_id}: {e}")

print("\nWeb scraping complete.")

