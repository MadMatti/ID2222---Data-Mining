import os
from apriori import AprioriAlgorithm
from association import AprioriAssociation

def format_itemset(itemset):
    return ', '.join(map(str, sorted(itemset)))

def main():
    path = os.path.dirname(os.getcwd())
    data_path = os.path.join(path, 'data', 'T10I4D100K.dat')
    apiroi = AprioriAlgorithm(data_path)
    min_support = 100
    max_item_set_length = 5

    frequent_singletons = apiroi.find_frequent_singletons(s=min_support)
    print(f"Frequent Singletons: {len(frequent_singletons)}")
    # Print the first 10 frequent singletons
    print({format_itemset(k): frequent_singletons[k] for k in list(frequent_singletons)[:10]})


    candidate_item_sets = apiroi.generate_candidate_item_sets(frequent_singletons.keys(), 2)
    print(f"Candidate Item Sets: {len(candidate_item_sets)}")
    print([format_itemset(itemset) for itemset in candidate_item_sets][:10])


    filtered_frequent_item_sets = apiroi.filter_frequent_item_sets(candidate_item_sets, 2, s=min_support)
    print(f"Frequent Item Sets: {len(filtered_frequent_item_sets)}")
    for item_set, support in [(format_itemset(iter[0]), iter[1]) for iter in filtered_frequent_item_sets.items()][:10]: 
        print(f"Item Set: {item_set}, Support: {support}")


    for i in range(3, max_item_set_length + 1):
        candidate_item_sets = apiroi.generate_candidate_item_sets(filtered_frequent_item_sets.keys(), i)
        print([format_itemset(itemset) for itemset in candidate_item_sets][:10])

        filtered_frequent_item_sets = apiroi.filter_frequent_item_sets(candidate_item_sets, i, s=min_support)
        print(f"Frequent Item Sets of length {i}: {len(filtered_frequent_item_sets)}")
        for item_set, support in [(format_itemset(iter[0]), iter[1]) for iter in filtered_frequent_item_sets.items()][:10]:
            print(f"Item Set: {item_set}, Support: {support}")


def main_rules():
    path = os.path.dirname(os.getcwd())
    data_path = os.path.join(path, 'data', 'T10I4D100K.dat')
    apiroi = AprioriAlgorithm(data_path)
    min_support = 100
    transactions = apiroi.read_dataset(data_path)

    frequent_singletons = apiroi.find_frequent_singletons(s=min_support)
    candidate_item_sets = apiroi.generate_candidate_item_sets(frequent_singletons.keys(), 2)
    filtered_frequent_item_sets = apiroi.filter_frequent_item_sets(candidate_item_sets, 2, s=min_support)

    rules_generator = AprioriAssociation(transactions, filtered_frequent_item_sets, min_support=100, min_confidence=0.7)
    rules = rules_generator.generate_rules()

    for rule in rules:
        antecedent, consequent, support, confidence = rule
        formatted_antecedent = format_itemset(antecedent)
        formatted_consequent = format_itemset(consequent)
        print(f"Rule: {formatted_antecedent} -> {formatted_consequent}, Support: {support}, Confidence: {confidence}")


if __name__ == '__main__':
    # main()
    main_rules()
