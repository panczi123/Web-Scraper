import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import utils

def initialize_nltk():
    # Download stopwords and tokenizer data
    nltk.download('stopwords')
    nltk.download('punkt')

def get_stopwords():
    european_languages = [
        'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 
        'italian', 'norwegian', 'portuguese', 'russian', 'spanish', 'swedish'
    ]

    stopWords = set()
    # Add stopwords for languages to the set
    for lang in european_languages:
        stopWords.update(stopwords.words(lang))

    # Add Polish stopwords from a custom file
    with open('stopwords-pl.txt', 'r') as f:
        polish_stopwords = f.read().splitlines()
    stopWords.update(polish_stopwords)

    return stopWords

def get_sentence_value(sentences, freqTable):
    sentence_value = {}
    # Calculate the value of each sentence based on word frequency
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += freq
                else:
                    sentence_value[sentence] = freq
    return sentence_value

def get_sum_values(sentence_value):
    sumValues = 0
    # Sum the values of all sentences
    for sentence in sentence_value:
        sumValues += sentence_value[sentence]

    # Calculate the average sentence value
    average = int(sumValues / len(sentence_value))
    return average

def generate_summary(df_sentences, stopWords):
    df_summary = pd.DataFrame(columns=["Company", "Link", "Summary"])

    for i in range(len(df_sentences)):
        row = df_sentences.iloc[i]
        company = row['Company']
        link = row['Link']
        text = row['Text']

        words = word_tokenize(text)
        freqTable = {}
        # Create a frequency table of words in the text
        for word in words:
            word = word.lower()
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

        sentences = sent_tokenize(text)
        # Calculate the value of each sentence
        sentence_value = get_sentence_value(sentences, freqTable)
        average = get_sum_values(sentence_value)

        # Sort sentences by their value in descending order
        sorted_sentences = sorted(sentence_value.items(), key=lambda kv: kv[1], reverse=True)
        # Select the top 2 sentences
        top_sentences = sorted_sentences[:1]
        top_sentences_list = [sentence for sentence, value in top_sentences]

        # Create a summary by joining the top sentences
        summary = ' '.join([sentence for sentence in sentences if sentence in top_sentences_list])

        # Add the summary to the dataframe
        df_summary = pd.concat([df_summary, pd.DataFrame({"Company": [company], "Link": [link], "Summary": [summary]})], ignore_index=True)

    df_summary = df_summary[["Company", "Link", "Summary"]]
    df_summary.to_csv('summary.csv', index=False)
    return df_summary

def summarize_texts(parent_links, child_links, parent_sentences, child_sentences):
    initialize_nltk()
    stopWords = get_stopwords()
    
    df_sentences = pd.DataFrame(columns=["Company", "Link", "Text"])
    df_links = pd.read_csv('csv_links.csv')

    for i in range(len(parent_links)):
        parent_link = parent_links[i]
        company_name = df_links.iloc[i]['Company name']
        parent_text = parent_sentences[i]

        # Combine child sentences that belong to the current parent link
        child_texts = ' '.join(
            [child_sentences[j] for j in range(len(child_links[i])) 
             if child_links[i][j] in child_links[i] and child_sentences[j] is not None]
        )

        # Combine parent and child texts, ensuring unique words only
        combined_text = parent_text + ' ' + child_texts
        combined_text = ' '.join(list(dict.fromkeys(combined_text.split())))

        # Add the combined text to the dataframe
        df_sentences = pd.concat(
            [df_sentences, pd.DataFrame({"Company": [company_name], "Link": [parent_link], "Text": [combined_text]})], 
            ignore_index=True
        )
    
    # Generate the summary from the combined texts
    df_summary = generate_summary(df_sentences, stopWords)
    return df_summary
