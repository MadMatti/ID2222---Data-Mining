import functools


class shingling:
    def __init__(self, k):
        self.k = k
        self.shingling_dict = dict()
        self.shinglings_count = 0

    # Performs hashing of a single shingle
    def hash(self, shingling):
        hash_value = hash(shingling)

        if hash_value not in self._shingling_to_int:
            self._shingling_to_int[hash_value] = self._shingling_number
            self._shingling_number += 1
        return self._shingling_to_int[hash_value]

    def shingling(self, text):
        result = set()

        for i in range(len(text) - self.k + 1):
            shingle = text[i:i + self.k]
            result.add(self.hash(shingle))

        return result
