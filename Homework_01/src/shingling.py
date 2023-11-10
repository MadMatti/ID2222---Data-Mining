import functools


class Shingling:
    def __init__(self, k=10):
        self.k = k
        self.shingling_dict = dict()
        self.shinglings_count = 0

    # Performs hashing of a single shingle
    def hash(self, shingling):
        hash_value = hash(shingling)

        if hash_value not in self.shingling_dict:
            self.shingling_dict[hash_value] = self.shinglings_count
            self.shinglings_count += 1
        return self.shingling_dict[hash_value]

    @functools.lru_cache() # Caches to optimize performances
    def shingling(self, text):
        result = set()

        for i in range(len(text) - self.k):
            shingle = text[i:i + self.k]
            result.add(self.hash(shingle))

        return result
