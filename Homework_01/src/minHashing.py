import random

class MinHashing:

    def __init__(self, numHashes):
        self.num_hashes = numHashes
        self.max_value = 2 ** 32 - 1
        self.max_shingle_id = 2 ** 20 - 1
        self.hash_functions = [
            (random.randint(1, self.max_shingle_id), random.randint(1, self.max_shingle_id))
            for _ in range(numHashes)
        ]

    def hash_value(self, x, a, b):
        return (a * x + b) % self.max_value

    def minhas_signatures(self, shingle_set):
        """
        :param shingle_set: set of hashed shinglings from a document
        :return: signature of the document
        """
        signature = [float('inf')] * self.num_hashes

        for shingle in shingle_set:
            for i, (a,b) in enumerate(self.hash_functions):
                hash_val = self.hash_value(shingle, a, b)
                if hash_val < signature[i]:
                    signature[i] = hash_val

        return signature
    

        
