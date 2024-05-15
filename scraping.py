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


# Odczytaj plik csv
df = pd.read_csv('csv_links.csv')

# Pobierz linki z kolumny "Website"
parent_links = df['Website'].tolist()

print(parent_links)

# lista linków
child_links = []
parent_sentences = [] 

#rozszerzenia, które są usuwanie z listy linków
extensions = ['.jpg','.jpeg','png','gif','.bmp','.tiff','.ico','.jfif','.webp','.svg','.mp3','.wav','.ogg','.flac','.aac','.m4a','.mp4','.avi','.mkv','.flv','.mov','.wmv']

def remove_shit_links(shit_links, extensions):
    return [shit_link for shit_link in shit_links if not any(shit_link.endswith(ext) for ext in extensions)]

# odpowiednie wiadomości przy procesowaniu
for plink in parent_links:
    # print(f"Przetwarzanie strony: {website}")
    try:
        req = Request(plink)
        html_page = urlopen(req)

        # przegladanie piękną zupą strony używajac lxml
        soup = BeautifulSoup(html_page, "lxml")

        # lista linków dla konkretnej strony
        #parent zdania
        # url of the website 
        parent_sentences_str = utils.get_sentences(plink)
        parent_sentences.append(parent_sentences_str)

        child_link_temp = []

        # wyszukiwanie na stronach "a" i href ------
        for link in soup.findAll('a'):
            href = link.get('href')

            # dodawanie adresu strony jeśli pobrany został adres względny
            if href and href.strip():
                full_url = urljoin(plink, href)
                # sprawdzanie czy adres jest prawidłowy czy to nie jakiś syf
                if urlparse(full_url).netloc:
                    child_link_temp.append(full_url)

        child_link_temp = remove_shit_links(child_link_temp, extensions)

        # dodajemy listę linków do głównej listy
        child_links.append(list(set(child_link_temp)))

    except urllib.error.HTTPError as e:
        print(f"Błąd podczas otwierania strony: {plink}")
        print(f"Kod błędu: {e.code}, wiadomość: {e.reason}")


# ista list, gdzie każda podlista zawiera unikalne linki z konkretnej strony i usuwanie duplikatów
#links = [list(dict.fromkeys(website_links)) for website_links in links]

# print(links)


# # sprawdzanie linków tylko z 1 listy
# for link in links[0]:
#         print(link)

# # pokazywnie wszystkich linków w kolumnie
# for sub_link in links:
#     for link in sub_link:
#         print(link)

# print(parent_links[1])
# print(child_links[1])
child_sentences = []
for chlink in child_links:
     for subchlink in chlink:
        print(f"------------------------{subchlink}-------------------")
        child_sentences_str = utils.get_sentences(subchlink)
        child_sentences.append(child_sentences_str)

# print(len(parent_links))
# print(len(parent_sentences))
# print(len(child_links))
# print(len(child_sentences))


# Tworzenie pustej ramki danych
df_sentences = pd.DataFrame()

# Iterowanie po wszystkich linkach nadrzędnych i ich linkach podrzędnych
for i in range(len(parent_links)):
    parent_link = parent_links[i]
    child_links_list = child_links[i]

    # Pobieranie zdań z linku nadrzędnego
    parent_sentences_str = utils.get_sentences(parent_link)

    # Pobieranie zdań z każdego linku podrzędnego
    child_sentences_str_list = [utils.get_sentences(subchlink) for subchlink in child_links_list]

    # Łączenie zdań z linku nadrzędnego i linków podrzędnych
    all_sentences = [parent_sentences_str] + child_sentences_str_list

    # Dodawanie zdań do ramki danych
    df_sentences[parent_link] = pd.Series(all_sentences)

    import pandas as pd

# Tworzenie pustej ramki danych
df_sentences = pd.DataFrame()

# Iterowanie po wszystkich linkach nadrzędnych i ich linkach podrzędnych
for i in range(len(parent_links)):
    parent_link = parent_links[i]
    child_links_list = child_links[i]

    # Pobieranie zdań z linku nadrzędnego
    parent_sentences_str = utils.get_sentences(parent_link)

    # Pobieranie zdań z każdego linku podrzędnego
    child_sentences_str_list = [utils.get_sentences(subchlink) for subchlink in child_links_list]

    # Łączenie zdań z linku nadrzędnego i linków podrzędnych
    all_sentences = [parent_sentences_str] + child_sentences_str_list

    # Dodawanie zdań do ramki danych
    df_sentences[parent_link] = pd.Series(all_sentences)

    df_sentences = df_sentences.fillna("")

# Zapisywanie ramki danych do pliku CSV
#df_sentences.to_csv("sentences.csv", index=False)

# Zapisywanie ramki danych do pliku Excel
#df_sentences.to_excel("sentences.xlsx", index=False)

# Pobierz stopwords dla wszystkich europejskich języków obsługiwanych przez NLTK
european_languages = ['danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'norwegian', 'portuguese', 'russian', 'spanish', 'swedish']

nltk.download('stopwords')
nltk.download('punkt')

stopWords = set()
for lang in european_languages:
    stopWords.update(stopwords.words(lang))

# Dodaj polskie stopwords wczytane z pliku
with open('stopwords-pl.txt', 'r') as f:
    polish_stopwords = f.read().splitlines()
stopWords.update(polish_stopwords)

# Tworzenie nowej ramki danych do przechowywania linków nadrzędnych i ich podsumowań
df_summary = pd.DataFrame(columns=["Company", "Link", "Summary"])

# Iterowanie po każdej kolumnie w df_sentences
for i in range(len(df_sentences.columns)):
    column = df_sentences.columns[i]

    # Łączenie wszystkich zdań w kolumnie w jeden ciąg
    text = " ".join(df_sentences[column].dropna())

    # Tokenizacja słów
    words = word_tokenize(text)

    # Tworzenie tabeli częstości dla słów
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    # Tokenizacja zdań
    sentences = sent_tokenize(text)

    # Obliczanie wartości dla każdego zdania
    sentenceValue = getsentenceValue()

    # Obliczanie średniej wartości zdań
    average = getsumValues()

    # Sortowanie zdań według ich wartości
    sorted_sentences = sorted(sentenceValue.items(), key=lambda kv: kv[1], reverse=True)

    # Wybieranie 5 zdań o najwyższej wartości
    top_sentences = sorted_sentences[:5]

    # Tworzenie listy z wybranych zdań
    top_sentences_list = [sentence for sentence, value in top_sentences]

    # Tworzenie podsumowania z wybranych zdań w oryginalnej kolejności
    summary = ' '.join([sentence for sentence in sentences if sentence in top_sentences_list])

    # Dodawanie linku nadrzędnego i jego podsumowania do df_summary
    #df_summary = df_summary.append({"Link": column, "Summary": summary}, ignore_index=True)`
    
    
    df = pd.read_csv('csv_links.csv')
    company_names = df['Company name'].tolist()

    df_summary = pd.concat([df_summary, pd.DataFrame({"Company": [company_names[i]], "Link": [column], "Summary": [summary]})], ignore_index=True)

    # Dodawanie nazwy firmy, linku nadrzędnego i jego podsumowania do df_summary
    #df_summary = df_summary.append({"Company": company_names[i], "Link": column, "Summary": summary}, ignore_index=True)

# Zmiana kolejności kolumn w df_summary
df_summary = df_summary[["Company", "Link", "Summary"]]

# Zapisywanie df_summary do pliku .csv i .xlsx
df_summary.to_csv("summary.csv", index=False)
df_summary.to_excel("summary.xlsx", index=False)

 