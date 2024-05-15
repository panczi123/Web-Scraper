from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from urllib.parse import urljoin, urlparse
import utils
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk

def getsentenceValue():
    sentenceValue = dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    return sentenceValue

def getsumValues():
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    average = int(sumValues / len(sentenceValue))
    return average


df = pd.read_csv('csv_links.csv')
parent_links = df['Website'].tolist()

print(parent_links)

#list of links
child_links = []
parent_sentences = [] 

extensions = ['.jpg','.jpeg','png','gif','.bmp','.tiff','.ico','.jfif','.webp','.svg','.mp3','.wav','.ogg','.flac','.aac','.m4a','.mp4','.avi','.mkv','.flv','.mov','.wmv']

def remove_shit_links(shit_links, extensions):
    return [shit_link for shit_link in shit_links if not any(shit_link.endswith(ext) for ext in extensions)]

for plink in parent_links:
    try:
        req = Request(plink)
        html_page = urlopen(req)

        soup = BeautifulSoup(html_page, "lxml")

        parent_sentences_str = utils.get_sentences(plink)
        parent_sentences.append(parent_sentences_str)

        child_link_temp = []

        for link in soup.findAll('a'):
            href = link.get('href')

            if href and href.strip():
                full_url = urljoin(plink, href)
                # sprawdzanie czy adres jest prawidłowy czy to nie jakiś syf
                if urlparse(full_url).netloc:
                    child_link_temp.append(full_url)

        child_link_temp = remove_shit_links(child_link_temp, extensions)

        child_links.append(list(set(child_link_temp)))

    except urllib.error.HTTPError as e:
        print(f"PAGE ERROR {plink}")
        print(f"Error code: {e.code}, message: {e.reason}")


child_sentences = []
for chlink in child_links:
     for subchlink in chlink:
        print(f"------------------------{subchlink}-------------------")
        child_sentences_str = utils.get_sentences(subchlink)
        child_sentences.append(child_sentences_str)

df_sentences = pd.DataFrame()

for i in range(len(parent_links)):
    parent_link = parent_links[i]
    child_links_list = child_links[i]

    parent_sentences_str = utils.get_sentences(parent_link)

    child_sentences_str_list = [utils.get_sentences(subchlink) for subchlink in child_links_list]

    all_sentences = [parent_sentences_str] + child_sentences_str_list

    df_sentences[parent_link] = pd.Series(all_sentences)

df_sentences = pd.DataFrame()

for i in range(len(parent_links)):
    parent_link = parent_links[i]
    child_links_list = child_links[i]

    parent_sentences_str = utils.get_sentences(parent_link)

    child_sentences_str_list = [utils.get_sentences(subchlink) for subchlink in child_links_list]

    all_sentences = [parent_sentences_str] + child_sentences_str_list

    df_sentences[parent_link] = pd.Series(all_sentences)

    df_sentences = df_sentences.fillna("")

european_languages = ['danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'norwegian', 'portuguese', 'russian', 'spanish', 'swedish']

nltk.download('stopwords')
nltk.download('punkt')

stopWords = set()
for lang in european_languages:
    stopWords.update(stopwords.words(lang))

with open('stopwords-pl.txt', 'r') as f:
    polish_stopwords = f.read().splitlines()
stopWords.update(polish_stopwords)

df_summary = pd.DataFrame(columns=["Company", "Link", "Summary"])

for i in range(len(df_sentences.columns)):
    column = df_sentences.columns[i]

    text = " ".join(df_sentences[column].dropna())

    words = word_tokenize(text)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = getsentenceValue()
    average = getsumValues()
    sorted_sentences = sorted(sentenceValue.items(), key=lambda kv: kv[1], reverse=True)
    top_sentences = sorted_sentences[:5]

    top_sentences_list = [sentence for sentence, value in top_sentences]

    summary = ' '.join([sentence for sentence in sentences if sentence in top_sentences_list])

    df = pd.read_csv('csv_links.csv')
    company_names = df['Company name'].tolist()

    df_summary = pd.concat([df_summary, pd.DataFrame({"Company": [company_names[i]], "Link": [column], "Summary": [summary]})], ignore_index=True)

df_summary = df_summary[["Company", "Link", "Summary"]]

df_summary.to_csv("summary.csv", index=False)
df_summary.to_excel("summary.xlsx", index=False)

 
