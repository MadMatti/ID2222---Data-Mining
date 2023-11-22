import os
import time
import matplotlib.pyplot as plt

from apriori import AprioriAlgorithm
from association import AssociationRules


def format_itemset(itemset):
    return ", ".join(map(str, sorted(itemset)))


def main_itemsets():
    path = os.path.dirname(os.getcwd())
    data_path = os.path.join(path, "data", "T10I4D100K.dat")
    apiroi = AprioriAlgorithm(data_path)
    min_support = 500

    # Initialize lists to store times and lengths
    total_times = []  # Sum of candidate_times and frequent_times
    frequent_lengths = []  # Length of frequent items
    lengths = []

    frequent_singletons = apiroi.find_frequent_singletons(s=min_support)
    print(f"Frequent Singletons: {len(frequent_singletons)}")
    print(
        {
            format_itemset(k): frequent_singletons[k]
            for k in list(frequent_singletons)[:10]
        }
    )

    i = 2
    while frequent_singletons:
        start_time_candidate = time.time()
        candidate_item_sets = apiroi.generate_candidate_item_sets(
            frequent_singletons.keys(), i
        )
        candidate_time = time.time() - start_time_candidate

        start_time_frequent = time.time()
        filtered_frequent_item_sets = apiroi.filter_frequent_item_sets(
            candidate_item_sets, i, s=min_support
        )
        frequent_time = time.time() - start_time_frequent

        # Append sum of times and length
        total_times.append(candidate_time + frequent_time)
        frequent_lengths.append(len(filtered_frequent_item_sets))
        lengths.append(i)

        print(f"Candidate Item Sets of length {i}: {len(candidate_item_sets)}")
        print(f"Frequent Item Sets of length {i}: {len(filtered_frequent_item_sets)}")

        i += 1
        frequent_singletons = filtered_frequent_item_sets

    # Plotting Total Time
    plt.figure(figsize=(10, 5))
    plt.plot(
        lengths,
        total_times,
        label="Total Time (To generate Candidate + Frequent Item Sets)",
    )
    plt.xlabel("Item Set Length")
    plt.ylabel("Time (seconds)")
    plt.title("Total Time vs Item Set Length")
    plt.xticks(lengths)
    plt.legend()
    plt.show()

    # Plotting Length of Frequent Items
    plt.figure(figsize=(10, 5))
    plt.plot(
        lengths, frequent_lengths, label="Length of Frequent Items", color="orange"
    )
    plt.xlabel("Item Set Length")
    plt.ylabel("Length of Frequent Items")
    plt.title("Length of Frequent Items vs Item Set Length")
    plt.xticks(lengths)
    plt.legend()
    plt.show()


def main_rules():
    path = os.path.dirname(os.getcwd())
    data_path = os.path.join(path, "data", "T10I4D100K.dat")
    apiroi = AprioriAlgorithm(data_path)
    min_support = 1000
    transactions = apiroi.read_dataset(data_path)

    total_times = []  # Sum of candidate_times and frequent_times
    rules_lengths = []  # Length of frequent items
    lengths = []

    frequent_singletons = apiroi.find_frequent_singletons(s=min_support)

    i = 2
    while frequent_singletons:
        candidate_item_sets = apiroi.generate_candidate_item_sets(
            frequent_singletons.keys(), i
        )

        filtered_frequent_item_sets = apiroi.filter_frequent_item_sets(
            candidate_item_sets, i, s=min_support
        )

        rules_generator = AssociationRules(
        transactions, filtered_frequent_item_sets, min_support=1000, min_confidence=0.8
        )
        start_time = time.time()
        rules = rules_generator.generate_rules()
        total_time = time.time() - start_time

        # Append sum of times and length
        total_times.append(total_time)
        rules_lengths.append(len(rules))
        lengths.append(i)

        print(f"Rules with itemsets of length {i}: {len(rules)}")
        for rule in rules[:10]:
            antecedent, consequent, support, confidence = rule
            formatted_antecedent = format_itemset(antecedent)
            formatted_consequent = format_itemset(consequent)
            print(
                f"Rule: {formatted_antecedent} -> {formatted_consequent}, Support: {support}, Confidence: {confidence}"
            )

        i += 1
        frequent_singletons = filtered_frequent_item_sets

    # Plotting Total Time
    plt.figure(figsize=(10, 5))
    plt.plot(lengths, total_times, label="Total Time (To generate Rules)")
    plt.xlabel("Item Set Length")
    plt.ylabel("Time (seconds)")
    plt.title("Total Time vs Item Set Length")
    plt.xticks(lengths)
    plt.legend()
    plt.show()

    # Plotting Length of Rules
    plt.figure(figsize=(10, 5))
    plt.plot(lengths, rules_lengths, label="Length of Rules", color="orange")
    plt.xlabel("Item Set Length")
    plt.ylabel("Length of Rules")
    plt.title("Length of Rules vs Item Set Length")
    plt.xticks(lengths)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main_itemsets()
    # main_rules()
