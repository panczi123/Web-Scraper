from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk

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

# wczytaj tekst z pliku
with open('summary_input.txt', 'r') as file:
    text = file.read()

# print(stopWords)

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

sentenceValue = getsentenceValue()

def getsumValues():
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue))
    return average

average = getsumValues()

# print(average)

# # maks 1.4
# summary = ''
# for sentence in sentences:
#     if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.1 * average)):
#         # print(sentence)
#         summary += " " + sentence


# # zapisz podsumowanie do pliku
# with open('summary_output.txt', 'w') as file:
#     file.write(summary)

# sortuj zdania według ich wartości
sorted_sentences = sorted(sentenceValue.items(), key=lambda kv: kv[1], reverse=True)

# wybierz 10 zdań o najwyższej wartości
top_sentences = sorted_sentences[:5]

# utwórz listę z wybranych zdań
top_sentences_list = [sentence for sentence, value in top_sentences]

# utwórz podsumowanie z wybranych zdań w oryginalnej kolejności
summary = ' '.join([sentence for sentence in sentences if sentence in top_sentences_list])

# zapisz podsumowanie do pliku
with open('summary_output.txt', 'w') as file:
    file.write(summary)
