import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from spectralClustering import SpectralClustering

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

if __name__ == '__main__':
    # Ask the user to choose the dataset
    dataset_choice = input("Which dataset do you want to apply spectral clustering to? Enter 1 for real graph or 2 for synthetic graph: ")

    if dataset_choice == '1':
        # Real graph
        graph_file = '../data/example1.dat'
        G = load_graph(graph_file, weight=False)
    elif dataset_choice == '2':
        # Synthetic graph
        graph_file = '../data/example2.dat'
        G = load_graph(graph_file, weight=True)
    else:
        print("Invalid choice. Please enter 1 or 2.")
        exit()

    print('The size of the graph is {}.'.format(G.size()))

    # Visualize the original graph
    nx.draw(G, node_size=8)
    plt.title('Original Graph')
    plt.show()

    # Perform spectral clustering
    spectralClustering = SpectralClustering(
        G=G,
    )

    classes, fiedler, adjacency_matrix = spectralClustering.compute_clusters()

    # Display results and visualizations
    print('The classes are {}.'.format(classes))
    print('The Fiedler vector is {}.'.format(fiedler))
    print('The adjacency matrix is {}.'.format(adjacency_matrix))

    # Plot Fiedler vector
    plt.plot(np.sort(fiedler))
    plt.xlabel("Node")
    plt.ylabel("Eigenvector")
    plt.title('Sorted Fiedler Vector')
    plt.show()

    # Plot adjacency matrix
    plt.spy(adjacency_matrix);
    plt.title('Adjacency Matrix')
    plt.show()

    # Visualize the graph with node colors representing clusters
    nx.draw(G, node_size=8, node_color=classes)
    plt.title('Graph with Cluster Assignments')
    plt.show()


