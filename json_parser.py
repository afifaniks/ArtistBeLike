import json
import nltk
# Checking resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
     
from nltk.corpus import stopwords
import re

file_path = 'data/nicki-minaj-data.json'
with open(file_path) as file:
    data = json.load(file)
    lyrics = ""

    for d in range(len(data)):
        for k in data[d]:
            lyrics += str(data[d][k])

    lyrics = re.sub(r"\(.*?\)", "", lyrics)
    lyrics = re.sub(",", " ", lyrics)

    allWords = nltk.tokenize.word_tokenize(lyrics)
    allWordDist = nltk.FreqDist(w.lower() for w in allWords)

    print([word for word in allWordDist])

    # stopwords = stopwords.words('english')
    # print(stopwords)
    # allWordExceptStopDist = nltk.FreqDist(w.lower() for w in allWords if w not in stopwords)
    #
    # for word in allWordExceptStopDist:
    #     print(word)

