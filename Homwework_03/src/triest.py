from typing import Set, FrozenSet, DefaultDict
from scipy.stats import bernoulli
import random


class TriestBase:

    def __init__(self, file: str, M: int, verbose: bool = False):
        self.file = file
        self.M = M
        self.verbose = verbose
        self.S: Set[FrozenSet[int]] = set()
        self.t = 0
        self.tau = 0
        self.edge_triangles = DefaultDict(int)

    def get_edge(self, row) -> FrozenSet[int]:
        # Split the line and return the two edges as a frozenset

        return frozenset([int(node) for node in row.split()])

    @property
    def xi_norm(self) -> float:
        # Define the xi factor when exceeding the memory limit M

        return max(1.0, ((self.t * (self.t-1) * (self.t-2)) / (self.M * (self.M-1) * (self.M-2))))

    def sample_edge(self, t: int) -> bool:
        # Determine if a new edge can be inserted in memory or if it exceeds the memory limit M.
        # If the memory limit is exceeded, the edge is sampled with a probability of M/t and another edge is removed

        if t <= self.M:
            return True
        elif bernoulli.rvs(p = (self.M / t)):
            edge_to_remove = random.choice(list(self.S))
            self.S.remove(edge_to_remove)
            self.update_counters(edge_to_remove, decrement=True)
            return True
        else:
            return False

    def update_counters(self, edge: FrozenSet[int], decrement: bool) -> None:
        # Updates the triangle count based on the edge and its neighbours.

        common_neighbourhood = set.intersection(*[
        {node for link in self.S if vertex in link for node in link if node != vertex}
        for vertex in edge
        ])

        change = -1 if decrement else +1
        for vertex in common_neighbourhood:
            self.tau += change
            self.edge_triangles[vertex] += change

            for node in edge:
                self.edge_triangles[node] += change

    def run(self) -> float:
        # Run the TRIEST algorithm

        if self.verbose:
            print("Running TRIEST-BASE algorithm with M = {}".format(self.M))

        with open(self.file, "r") as f:
            # print the len of the file
            for row in f:
                edge = self.get_edge(row)
                self.t += 1

                if self.verbose and self.t % 1000 == 0:
                    print("Processing the {}-th element in the stream".format(self.t))

                if self.sample_edge(self.t):
                    self.S.add(edge)
                    self.update_counters(edge, decrement=False)

                if self.verbose and self.t % 1000 == 0:
                    print("Current estimate triangle count: {}".format(self.xi_norm * self.tau))

        return self.xi_norm * self.tau