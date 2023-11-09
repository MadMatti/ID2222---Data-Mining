import pandas as pd
import string
import time
import matplotlib.pyplot as plt
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
    execution_times_jaccard = []
    execution_times_lsh = []

    for i in range(10):
        for j in range(10):
            shing1 = shingling.shingling(fake_news.iloc[i]['text'])
            shing2 = shingling.shingling(true_news.iloc[j]['text'])
            print(shingComparator.jaccard_similarity(shing1, shing2))
            signature1 = minHashing.minhas_signatures(shing1)
            signature2 = minHashing.minhas_signatures(shing2)
            print(Sigcomparator.similarity(signature1, signature2))

    all_documents = true_news['text'].values
    n_documents = [10, 100, 500, 1000, 5000]
    generator = np.random.default_rng(seed=42)

    # compare n documents with each other
    start = time.time()
    for n in n_documents:
        documents = generator.choice(all_documents, n)
        print('number of documents:', n)
        tokens =   [shingling.shingling(document) for document in documents]
        n = len(tokens)
        similarity_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                similarity_matrix[i, j] = shingComparator.jaccard_similarity(tokens[i], tokens[j])
        end = time.time()
        execution_times_jaccard.append(end - start)
        print(f"Jaccard Execution time for {n} documents:", end - start)
        print(similarity_matrix)

    # compare n documents with each other to find similar pairs using LSH
    start = time.time()
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
        end = time.time()
        execution_times_lsh.append(end - start)
        print(f"LSH Execution time for {n} documents:", end - start)
        print(pairs)

    # Plot the execution times
    plt.figure(figsize=(10, 5))
    plt.plot(n_documents, execution_times_jaccard, label="Jaccard")
    plt.plot(n_documents, execution_times_lsh, label="LSH")
    plt.xlabel("Number of Documents")
    plt.ylabel("Execution Time (s)")
    plt.title("Execution Time vs Number of Documents")
    plt.legend()
    plt.grid(True)
    plt.show()

#     band size vs number of similar pairs
    band_sizes = [20, 40, 60, 80]  # Different band sizes to test
    n = 100  # Number of documents
    documents = generator.choice(all_documents, n)
    tokens = [shingling.shingling(document) for document in documents]
    min_hashing = MinHashing(500)
    signatures = [min_hashing.minhas_signatures(token) for token in tokens]
    threshold = 0.5  # (1/40)^(1/5) = 0.478
    n_pairs = []
    for band in band_sizes:
        pairs = LSH.findSimilarPairs(signatures, band, threshold)
        n_pairs.append(len(pairs))
    plt.figure(figsize=(10, 5))
    plt.plot(band_sizes, n_pairs)
    plt.xlabel("Band Size")
    plt.ylabel("Number of Similar Pairs")
    plt.title("Band Size vs Number of Similar Pairs")
    plt.grid(True)
    plt.show()





if __name__ == '__main__':
    main()