"""
Compute similar pairs of documents using LSH.
"""

from typing import List


class LSH:
    def findSimilarPairs(self, signatures, band, threshold):
        similarPairsSet = set()
        segmentSize = len(signatures[0]) // band

        def hashSegment(segment: List[int]) -> int:
            return "-".join([str(i) for i in segment])

        for i in range(band):
            bucket = dict()
            for j, signature in enumerate(signatures):
                # we thrown away the last segment if it is not full
                segmentHash = hashSegment(signature[i * segmentSize: (i + 1) * segmentSize])
                if segmentHash not in bucket:
                    bucket[segmentHash] = []
                bucket[segmentHash].append(j)
            for _, v in bucket.items():
                if len(v) > 1:
                    for i in range(len(v)):
                        for j in range(i + 1, len(v)):
                            similarPairsSet.add((v[i], v[j]))
        return list(similarPairsSet) 