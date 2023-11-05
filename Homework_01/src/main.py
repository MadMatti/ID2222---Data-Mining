import pandas as pd
import string
from shingling import Shingling
from compareSets import CompareSets

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
    result1 = shingling.shingling(fake_news['text'][0])
    result2 = shingling.shingling(true_news['text'][0])

    comparator = CompareSets()
    print(comparator.jaccard_similarity(result1, result2))

if __name__ == '__main__':
    main()