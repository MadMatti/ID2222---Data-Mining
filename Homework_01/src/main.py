import pandas as pd
import string
from shingling import Shingling
from compareSets import CompareSets
from minHashing import MinHashing
from compareSignatures import CompareSignatures

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))

    return text

def load_data():
    fake_news = pd.read_csv('../data/Fake.csv')
    true_news = pd.read_csv('../data/True.csv')

    fake_news['text'] = fake_news['text'].apply(preprocess)
    true_news['text'] = true_news['text'].apply(preprocess)

    return fake_news, true_news

def main():
    fake_news, true_news = load_data()

    print(fake_news.head())
    print(true_news.head())

    shingling = Shingling(10)
    shingComparator = CompareSets()
    minHashing = MinHashing(50)
    Sigcomparator = CompareSignatures()

    for i in range(10):
        for j in range(10):
            shing1 = shingling.shingling(fake_news.iloc[i]['text'])
            shing2 = shingling.shingling(true_news.iloc[j]['text'])
            print(shingComparator.jaccard_similarity(shing1, shing2))
            signature1 = minHashing.minhas_signatures(shing1)
            signature2 = minHashing.minhas_signatures(shing2)
            print(Sigcomparator.similarity(signature1, signature2))

if __name__ == '__main__':
    main()