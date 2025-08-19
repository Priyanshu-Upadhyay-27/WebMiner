import os
import re
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
nltk.download('punkt_tab')

try:
    df_input = pd.read_excel('Input.xlsx')
except FileNotFoundError:
    print("Error: 'Input.xlsx' not found. Please place it in the same directory.")
    exit()

try:
    stop_words_files = [
        'StopWords_Auditor.txt', 'StopWords_Currencies.txt', 'StopWords_DatesandNumbers.txt',
        'StopWords_Generic.txt', 'StopWords_GenericLong.txt', 'StopWords_Geographic.txt', 'StopWords_Names.txt'
    ]
    stop_words = set()
    for file in stop_words_files:
        with open(os.path.join('StopWords', file), 'r') as f:
            stop_words.update(f.read().splitlines())
except FileNotFoundError:
    print("Error: Make sure the 'StopWords' directory and its files are present.")
    exit()

try:
    with open('MasterDictionary/positive-words.txt', 'r') as f:
        positive_words = set(f.read().splitlines())
    with open('MasterDictionary/negative-words.txt', 'r') as f:
        negative_words = set(f.read().splitlines())
except FileNotFoundError:
    print("Error: Make sure the 'MasterDictionary' directory and its files are present.")
    exit()


def count_syllables(word):
    word = word.lower()

    vowels = "aeiouy"
    syllable_count = 0
    if word and word[0] in vowels:
        syllable_count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i - 1] not in vowels:
            syllable_count += 1

    if word.endswith('e'):
        syllable_count -= 1

    return max(1, syllable_count)


def count_personal_pronouns(text):
    pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, re.I)
    return len(pronouns)

results = []

for index, row in df_input.iterrows():
    url_id = row['URL_ID']
    print(f"Analyzing URL_ID: {url_id}")

    try:
        with open(f'Extracted_Data/{url_id}.txt', 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"  -> File not found for URL_ID: {url_id}. Skipping.")
        continue

    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    cleaned_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    word_count = len(cleaned_words)
    sentence_count = len(sentences)

    if word_count == 0 or sentence_count == 0:
        print(f"  -> No valid words found for {url_id}. Skipping calculations.")
        continue

    # 1. POSITIVE SCORE
    positive_score = sum(1 for word in cleaned_words if word in positive_words)
    #2. NEGATIVE SCORE
    negative_score = sum(1 for word in cleaned_words if word in negative_words)

    # 3. POLARITY SCORE
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    # 4. SUBJECTIVITY SCORE
    subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)

    # 5. AVG SENTENCE LENGTH and 8. AVG NUMBER OF WORDS PER SENTENCE
    avg_sentence_length = len(words) / sentence_count

    # 6. PERCENTAGE OF COMPLEX WORDS and 9. COMPLEX WORD COUNT
    complex_word_count = sum(1 for word in cleaned_words if count_syllables(word) > 2)
    percentage_complex_words = complex_word_count / word_count

    # 7. FOG INDEX
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # 10. WORD COUNT
    word_count = len(cleaned_words)

    # 11. SYLLABLE PER WORD
    total_syllables = sum(count_syllables(word) for word in cleaned_words)
    syllable_per_word = total_syllables / word_count

    # 12. PERSONAL PRONOUNS
    personal_pronouns = count_personal_pronouns(text)

    # 13. AVG WORD LENGTH
    total_chars = sum(len(word) for word in cleaned_words)
    avg_word_length = total_chars / word_count

    article_data = {
        'URL_ID': url_id,
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_sentence_length,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllable_per_word,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }
    results.append(article_data)

df_results = pd.DataFrame(results)

df_output = pd.merge(df_input, df_results, on='URL_ID', how='left')

output_columns_order = [
    'URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
    'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS',
    'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT',
    'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
]

df_output = df_output[output_columns_order]

output_filename = 'Output Data Structure.xlsx'
df_output.to_excel(output_filename, index=False)

print(f"\nText analysis complete. Output saved to '{output_filename}'.")