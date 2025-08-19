
---

# 📰 Text Analysis and Web Scraping Tool

A Python-based project that combines **web scraping** and **text analysis** into a modular pipeline. It extracts clean article content from a list of URLs, performs advanced text analysis on them, and generates a consolidated Excel report with 13 key metrics, including **sentiment analysis, readability scores, and word statistics**.

---

## 🚀 Features

* **Web Scraping**

  * Extracts article titles and body text using `requests` + `BeautifulSoup`.
  * Adapts to multiple website structures (`<article>`, `<div class="entry-content">`, etc.).
  * Handles errors gracefully with retry logic for failed URLs.

* **Text Analysis**

  * Uses **NLTK** for preprocessing, tokenization, and stopword filtering.
  * Computes **13 linguistic and readability metrics**, including:

    * Sentiment (using Master Dictionary)
    * Gunning Fog Index (readability)
    * Word, sentence, and character statistics
  * Ensures clean, structured data for accurate results.

* **Output Generation**

  * Merges results with the original `Input.xlsx`.
  * Exports a clean, structured Excel file `Output Data Structure.xlsx`.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+

* **Libraries:**

  * `pandas`
  * `openpyxl`
  * `requests`
  * `beautifulsoup4`
  * `lxml`
  * `nltk`

* **NLTK Data Packages:**

  * `punkt`

---

## 📂 Project Structure

```
📦 text-analysis-web-scraping
 ┣ 📂 extracted_articles/       # Scraped article texts (auto-generated)
 ┣ 📂 master_dictionary/        # Dictionary for sentiment scoring
 ┣ 📂 stop_words/               # Stop words list
 ┣ 📜 Input.xlsx                # Input with URL list
 ┣ 📜 scrape_articles.py        # Web scraping module
 ┣ 📜 text_analysis.py          # Text analysis module
 ┣ 📜 Output Data Structure.xlsx # Final consolidated output
 ┣ 📜 README.md                 # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/text-analysis-web-scraping.git
   cd text-analysis-web-scraping
   ```

2. **Create virtual environment (recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install pandas openpyxl requests beautifulsoup4 lxml nltk
   ```

4. **Download NLTK data**

   ```python
   import nltk
   nltk.download('punkt')
   ```

---

## ▶️ Usage

1. **Run Web Scraper** (saves articles in `extracted_articles/`)

   ```bash
   python scrape_articles.py
   ```

2. **Run Text Analysis** (creates final Excel output)

   ```bash
   python text_analysis.py
   ```

3. **Check Output**

   * Final results will be available in:

     ```
     Output Data Structure.xlsx
     ```

---

## 📊 Example Workflow

* Input: `Input.xlsx` containing URLs.
* Output: `Output Data Structure.xlsx` with added metrics like sentiment, readability, and word stats.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit pull requests.

---

## 📜 License

This project is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License
**.

---
