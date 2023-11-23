from typing import Tuple, Callable, Set, DefaultDict, FrozenSet
from collections import defaultdict
from scipy.stats import bernoulli
from functools import reduce
import random


def _get_edge(line: str) -> FrozenSet[int]:
    return frozenset([int(vertex) for vertex in line.split()])


class TriestImproved:
    def __init__(self, file: str, M: int):
        self.file: str = file
        self.M: int = M
        self.S: Set[FrozenSet[int]] = set()
        self.t: int = 0
        self.tau_vertices: DefaultDict[int, float] = defaultdict(float)
        self.tau: float = 0

    @property
    def eta(self) -> float:
        return max(1.0, ((self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1)))

    def _update_counters(
        self, operator: Callable[[float, float], float], edge: FrozenSet[int]
    ) -> None:
        common_neighbourhood: Set[int] = reduce(
            lambda a, b: a & b,
            [
                {
                    node
                    for link in self.S
                    if vertex in link
                    for node in link
                    if node != vertex
                }
                for vertex in edge
            ],
        )

        for vertex in common_neighbourhood:
            self.tau += operator(self.eta, 0)
            self.tau_vertices[vertex] += operator(self.eta, 0)

            for node in edge:
                self.tau_vertices[node] += operator(self.eta, 0)

    def _sample_edge(self, t: int) -> bool:
        if t <= self.M:
            return True
        elif bernoulli.rvs(p=self.M / t):
            edge_to_remove: FrozenSet[int] = random.choice(list(self.S))
            self.S.remove(edge_to_remove)
            return True
        else:
            return False

    def run(self) -> float:
        with open(self.file, "r") as f:
            for line in f:
                edge = _get_edge(line)
                self.t += 1

                if self.t % 1000 == 0:
                    print("Currently sampling element {} in the stream.".format(self.t))

                self._update_counters(lambda x, y: x + y, edge)

                if self._sample_edge(self.t):
                    self.S.add(edge)

                if self.t % 1000 == 0:
                    print(
                        "The current estimate for the number of triangles is {}.".format(
                            self.tau
                        )
                    )

            return self.tau
