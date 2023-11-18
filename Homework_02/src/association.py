from collections import defaultdict, Counter
from typing import List, Set, Dict, FrozenSet, Tuple
from itertools import combinations
from tqdm import tqdm

class AssociationRules:

    def __init__(self, transactions: List[Set[int]], frequent_itemsets: Dict[FrozenSet[int], int], min_support: int, min_confidence: float):
        self.transactions = transactions
        self.frequent_itemsets = frequent_itemsets
        self.min_support = min_support
        self.min_confidence = min_confidence

    def calculate_support(self, itemset: FrozenSet[int]) -> float:
        return sum(1 for transaction in self.transactions if itemset.issubset(transaction))

    def generate_rules(self) -> List[Tuple[FrozenSet[int], FrozenSet[int], float, float]]:
        ass_rules = []

        for itemset in tqdm(self.frequent_itemsets):
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent

                    rule_support = self.calculate_support(itemset)
                    # if antecedent in self.frequent_itemsets:
                    antecedent_support = self.calculate_support(antecedent)
                    confidence = rule_support / antecedent_support if antecedent_support > 0 else 0
                    if rule_support >= self.min_support and confidence >= self.min_confidence:
                            ass_rules.append((antecedent, consequent, rule_support, confidence))

        return ass_rules



    