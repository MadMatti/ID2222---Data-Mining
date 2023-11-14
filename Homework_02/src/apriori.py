from collections import defaultdict, Counter
from typing import List, Set, Dict, FrozenSet
from itertools import combinations

class AprioriAlgorithm:
    def __init__(self, file: str):
        self.baskets = self.read_dataset(file)

    def read_dataset(self, file: str) -> List[Set[int]]:
        with open(file, "r") as f:
            return [{int(item_id) for item_id in line.split()} for line in f.read().splitlines()]

    def find_frequent_singletons(self, s=1) -> Dict[FrozenSet[int], int]:
        item_to_support = Counter(item for basket in self.baskets for item in basket)
        return {frozenset([item]): support for item, support in item_to_support.items() if support > s}

    def generate_candidate_item_sets(self, precedent_item_sets: List[FrozenSet[int]], item_set_length: int) -> Set[FrozenSet[int]]:
        return {item_set_left | item_set_right
                for item_set_left in precedent_item_sets
                for item_set_right in precedent_item_sets
                if len(item_set_left | item_set_right) == item_set_length}

    def filter_frequent_item_sets(self, candidate_item_sets: Set[FrozenSet[int]], item_set_length: int, s: int = 1) -> Dict[FrozenSet[int], int]:
        item_set_to_support = Counter(frozenset(item_set)
                                      for basket in self.baskets
                                      for item_set in combinations(basket, item_set_length)
                                      if frozenset(item_set) in candidate_item_sets)
        return {item_set: support for item_set, support in item_set_to_support.items() if support > s}

