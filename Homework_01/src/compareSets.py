class CompareSets:

    def jaccard_similarity(self, set1, set2):
        """
        :param set1: set of hashed shinglings from document 1
        :param set2: set of hashed shinglings from document 2
        :return: jaccard similarity of the two sets
        """
        return len(set1.intersection(set2)) / len(set1.union(set2))