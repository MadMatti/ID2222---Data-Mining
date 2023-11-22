from typing import Set, FrozenSet
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

    def get_edge(self, row) -> FrozenSet[int]:
        # Split the line and return the two edges as a frozenset

        return frozenset([int(node) for node in row.split()])

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

        u, v = edge
        neighbors_u = {other_vertex for (vertex, other_vertex) in self.S if vertex == u}
        neighbors_v = {other_vertex for (vertex, other_vertex) in self.S if vertex == v}

        # Find common neighbors of u and v
        common_neighbors = neighbors_u.intersection(neighbors_v)

        # Update triangle count
        increment = -1 if decrement else 1
        self.tau += increment * len(common_neighbors)