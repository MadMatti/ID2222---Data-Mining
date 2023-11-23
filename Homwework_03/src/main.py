from Homwework_03.src.triest_improved import TriestImproved
from triest import TriestBase
import matplotlib.pyplot as plt


def main():
    # path='../data/facebook_combined.txt'
    # M = [1000, 5000, 10000, 20000, 30000]
    # iterations = 10
    # estimations_list = []
    # true_number_of_triangles = 1612010 # for fb dataset
    #
    # for m in M:
    #     estimations = []
    #     for i in range(iterations):
    #         print("Running iteration {} with M = {}".format(i, m))
    #         triest_base = TriestBase(file=path, M=m, verbose=True)
    #         estimated_triangles = triest_base.run()
    #         estimations.append(estimated_triangles)
    #     estimations_list.append(estimations)
    #
    # plt.figure(figsize=(10, 6))
    # for i in range(len(M)):
    #     plt.scatter([M[i]]*iterations, estimations_list[i])
    # plt.plot([M[0], M[-1]], [true_number_of_triangles, true_number_of_triangles], color='red', label='True number of triangles')
    # plt.xlabel('Reservoir size M')
    # plt.ylabel('Estimated number of triangles')
    # plt.title('Estimation of the number vs size of the reservoir M')
    # plt.legend()
    # plt.show()
    #
    # plt.figure(figsize=(10, 6))
    # for i in range(len(M)):
    #     plt.scatter([M[i]]*iterations, estimations_list[i])
    # plt.plot([M[0], M[-1]], [true_number_of_triangles, true_number_of_triangles], color='red', label='True number of triangles')
    # plt.xlabel('Reservoir size M')
    # plt.ylabel('Estimated number of triangles')
    # plt.title('Estimation of the number vs size of the reservoir M')
    # plt.ylim(15e5, 175e4)
    # plt.legend()
    # plt.show()

    TriestImproved(file="../data/facebook_combined.txt", M=30000).run()


if __name__ == "__main__":
    main()
