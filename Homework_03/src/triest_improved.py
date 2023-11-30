from typing import Set, FrozenSet
from collections import defaultdict
from scipy.stats import bernoulli
import random


class TriestImproved:
    """
    Implementation of the Triest improved algorithm for estimating the number of triangles in a graph.
    """

    def __init__(self, file: str, M: int, verbose: bool = True):
        self.file = file
        self.M = M
        self.verbose = verbose
        self.S: Set[FrozenSet[int]] = set()
        self.t = 0
        self.tau = 0
        self.tau_vertices = defaultdict(int)

    def get_edge(self, line: str) -> FrozenSet[int]:
        # Split the line and return the two edges as a frozenset

        return frozenset([int(vertex) for vertex in line.split()])

    @property
    def eta(self) -> float:
        return max(1.0, ((self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1)))

    def sample_edge(self, t: int) -> bool:
        # Determine if a new edge can be inserted in memory or if it exceeds the memory limit M.
        # If the memory limit is exceeded, the edge is sampled with a probability of M/t and another edge is removed
        # The difference wrt to Base is that the counter are always updated not only when the edge is sampled

        if t <= self.M:
            return True
        elif bernoulli.rvs(p=self.M / t):
            edge_to_remove = random.choice(list(self.S))
            self.S.remove(edge_to_remove)
            return True
        else:
            return False

    def update_counters(self, edge: FrozenSet[int]) -> None:
        # Updates the triangle count based on the edge and its neighbours. Similar to base implementation

        common_neighbourhood = set.intersection(*[
            {
                node
                for link in self.S if vertex in link
                for node in link if node != vertex
            }
            for vertex in edge
        ])

        for vertex in common_neighbourhood:
            self.tau += self.eta
            self.tau_vertices[vertex] += self.eta

            for node in edge:
                self.tau_vertices[node] += self.eta

    def run(self) -> float:
        if self.verbose:
            print("Running TRIEST-IMPROVED algorithm with M = {}.".format(self.M))

        with open(self.file, 'r') as f:

            for line in f:
                edge = self.get_edge(line)
                self.t += 1

                if self.verbose and self.t % 10000 == 0:
                    print("Processing the {}-th element in the stream".format(self.t))

                # Update the counters regardless of the sampling
                self.update_counters(edge)

                if self.sample_edge(self.t):
                    self.S.add(edge)

                if self.verbose and self.t % 1000 == 0:
                    print("Current estimate triangle count: {}".format(self.tau))

            return self.tau
