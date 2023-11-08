import pandas as pd
import string
from shingling import Shingling
from compareSets import CompareSets
from minHashing import MinHashing
from compareSignatures import CompareSignatures
import numpy as np
import lsh
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
    LSH = lsh.LSH()

    for i in range(10):
        for j in range(10):
            shing1 = shingling.shingling(fake_news.iloc[i]['text'])
            shing2 = shingling.shingling(true_news.iloc[j]['text'])
            print(shingComparator.jaccard_similarity(shing1, shing2))
            signature1 = minHashing.minhas_signatures(shing1)
            signature2 = minHashing.minhas_signatures(shing2)
            print(Sigcomparator.similarity(signature1, signature2))
            signatures = [signature1, signature2]
            band = 40
            threshold = 0.5  # (1/40)^(1/5) = 0.478
            pairs = LSH.findSimilarPairs(signatures, band, threshold)
            print(pairs)

    all_documents = true_news['text'].values
    n_documents = [10, 100, 500, 1000, 2000, 3000, 4000, 5000]
    generator = np.random.default_rng(seed=42)

    # compare n documents with each other
    for n in n_documents:
        documents = generator.choice(all_documents, n)
        print('number of documents:', n)
        tokens =   [shingling.shingling(document) for document in documents]
        n = len(tokens)
        similarity_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                similarity_matrix[i, j] = shingComparator.jaccard_similarity(tokens[i], tokens[j])

        print(similarity_matrix)

    # compare n documents with each other to find similar pairs using LSH
    for n in n_documents:
        documents = generator.choice(all_documents, n)
        print('number of documents:', n)
#         get tokens for all documents
        tokens = [shingling.shingling(document) for document in documents]
        min_hashing = MinHashing(500)
        signatures = [min_hashing.minhas_signatures(token) for token in tokens]
        band = 40
        threshold = 0.5  # (1/40)^(1/5) = 0.478
        pairs = LSH.findSimilarPairs(signatures, band, threshold)
        print(pairs)


if __name__ == '__main__':
    main()