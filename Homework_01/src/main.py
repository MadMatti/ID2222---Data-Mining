import pandas as pd
import string
import time
import matplotlib.pyplot as plt
import numpy as np
from shingling import Shingling
from compareSets import CompareSets
from compareSignatures import CompareSignatures
from minHashing import MinHashing
import lsh

def preprocess(text):
    '''Do not modify this function'''
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def load_data():
    '''Do not modify this function'''
    # Load data from CSV files and preprocess text
    fake_news = pd.read_csv('../data/Fake.csv')
    true_news = pd.read_csv('../data/True.csv')

    fake_news['text'] = fake_news['text'].apply(preprocess)
    true_news['text'] = true_news['text'].apply(preprocess)

    return fake_news, true_news


def compare_documents_similarity(shingling, shingComparator, minHashing, Sigcomparator, true_news):
    # Compare the first 10 documents for Jaccard and MinHash Similarity
    for i in range(10):
        for j in range(10):
            shing1 = shingling.shingling(true_news.iloc[i]['text'])
            shing2 = shingling.shingling(true_news.iloc[j]['text'])
            print("Jaccard Similarity:", shingComparator.jaccard_similarity(shing1, shing2))
            signature1 = minHashing.minhas_signatures(shing1)
            signature2 = minHashing.minhas_signatures(shing2)
            print("Minhash Signature Similarity:", Sigcomparator.similarity(signature1, signature2))


def compare_execution_times(shingling, shingComparator, minHashing, LSH, all_documents, n_documents, generator):
    # Compare execution times for Jaccard and LSH with varying document sizes
    execution_times_jaccard = []
    execution_times_lsh = []

    for n in n_documents:
        documents = generator.choice(all_documents, n)
        print('Number of documents:', n)

        # Jaccard Similarity
        start = time.time()
        tokens = [shingling.shingling(document) for document in documents]
        similarity_matrix = np.array([[shingComparator.jaccard_similarity(tokens[i], tokens[j]) for j in range(n)] for i in range(n)])
        end = time.time()
        execution_times_jaccard.append(end - start)
        print(f"Jaccard Execution time for {n} documents:", end - start)

        # LSH Similarity
        start = time.time()
        tokens = [shingling.shingling(document) for document in documents]
        min_hashing = MinHashing(500)
        signatures = [min_hashing.minhas_signatures(token) for token in tokens]
        band = 40
        threshold = 0.5
        pairs = LSH.findSimilarPairs(signatures, band, threshold)
        end = time.time()
        execution_times_lsh.append(end - start)
        print(f"LSH Execution time for {n} documents:", end - start)
        print(pairs)

    return execution_times_jaccard, execution_times_lsh


def plot_execution_times(n_documents, execution_times_jaccard, execution_times_lsh):
    # Plot the execution times for Jaccard and LSH
    plt.figure(figsize=(10, 5))
    plt.plot(n_documents, execution_times_jaccard, label="Jaccard")
    plt.plot(n_documents, execution_times_lsh, label="LSH")
    plt.xlabel("Number of Documents")
    plt.ylabel("Execution Time (s)")
    plt.title("Execution Time vs Number of Documents")
    plt.legend()
    plt.grid(True)
    plt.show()


def compare_band_size_vs_similar_pairs(shingling, minHashing, LSH, all_documents, n, generator, band_sizes):
    # Compare band size vs number of similar pairs
    documents = generator.choice(all_documents, n)
    tokens = [shingling.shingling(document) for document in documents]
    min_hashing = MinHashing(500)
    signatures = [min_hashing.minhas_signatures(token) for token in tokens]
    threshold = 0.5
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


def main():
    fake_news, true_news = load_data()

    print("First 10 Documents Comparison:")
    shingling = Shingling(10)
    shingComparator = CompareSets()
    minHashing = MinHashing(50)
    Sigcomparator = CompareSignatures()
    compare_documents_similarity(shingling, shingComparator, minHashing, Sigcomparator, true_news)

    all_documents = true_news['text'].values
    n_documents = [10, 100, 500, 1000, 5000]
    generator = np.random.default_rng(seed=42)

    print("\nComparison of Execution Times:")
    execution_times_jaccard, execution_times_lsh = compare_execution_times(shingling, shingComparator, minHashing, lsh.LSH(), all_documents, n_documents, generator)
    plot_execution_times(n_documents, execution_times_jaccard, execution_times_lsh)

    print("\nBand Size vs Number of Similar Pairs:")
    band_sizes = [20, 40, 60, 80]
    compare_band_size_vs_similar_pairs(shingling, minHashing, lsh.LSH(), all_documents, 100, generator, band_sizes)

if __name__ == '__main__':
    main()