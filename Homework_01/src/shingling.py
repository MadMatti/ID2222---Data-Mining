import functools


class shingling:
    def __init__(self, k):
        self.k = k
        self.shingling_dict = dict()
        self.shinglings_count = 0        