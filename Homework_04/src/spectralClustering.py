import networkx as nx
import numpy as np
from scipy import linalg
from sklearn.cluster import KMeans

def load_graph(file: str, weight: bool = False) -> nx.Graph:
    """
    Takes a file containing edges in a graph and outputs the graph in the form of a networkx class.
    """
    if weight:
        return nx.read_weighted_edgelist(
            path=file,
            delimiter=','
        )
    else:
        return nx.read_edgelist(
            path=file,
            delimiter=','
        )

class SpectralClustering:
    """
    Implementation of the spectral clustering algorithm.
    """
    def __init__(self, G: nx.Graph):
        """
        Initialize the spectral clustering algorithm.

        Parameters:
        - G: nx.Graph, the input graph
        """
        self.G = G

    def compute_clusters(self):
        """
        Compute clusters using spectral clustering algorithm.

        Returns:
        - result: array, cluster assignments
        - fiedler: array, Fiedler vector
        - adjacency_matrix: array, adjacency matrix of the graph
        """

        # Convert graph to adjacency matrix
        A = nx.convert_matrix.to_numpy_array(self.G)

        # Degree matrix
        D = np.diagflat(np.sum(A, axis=1))

        # Normalized Laplacian matrix
        D_inv = np.linalg.inv(np.sqrt(D))
        L = D_inv @ A @ D_inv

        # Eigenvalue decomposition
        values, vectors = linalg.eigh(L)

        # Optimal number of clusters using the Fiedler vector
        k = np.argmin(np.ediff1d(values[::-1])) + 1

        print('The optimal number of clusters is {}.'.format(k))

        # Selecting the bottom k eigenvectors
        X = vectors[:, -k:]

        # Normalizing the rows of X
        Y = X / np.linalg.norm(X, axis=1, keepdims=True)

        # KMeans clustering in the reduced space
        result = KMeans(n_clusters=k, n_init=10).fit(Y).labels_

        # Fiedler vector computation using the second smallest eigenvalue of D - A
        _, vectors = linalg.eigh(D - A)
        return result, vectors[:, 1], A
