class CompareSignatures:

    def similarity(self, sig1, sig2):
        """
        :param sig1: signature 1
        :param sig2: signature 2
        :return: similarity of the two signatures
        """
        return sum(s1 == s2 for s1, s2 in zip(sig1, sig2)) / len(sig1)