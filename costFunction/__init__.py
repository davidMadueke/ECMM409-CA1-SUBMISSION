import numpy as np


def cost(adj_mat, tour_vec, num_cities):
    # Make into arrays the Adjacency Matrix and tour Vector
    D = np.array(adj_mat)
    C = np.array(tour_vec)

    # Initialise the running cost to be 0
    running_cost = 0

    # Compute the sum using the formula given
    # (NOTE: Because Python is zero indexed this is reflected in the for loop)
    for i in range(0, num_cities-2):
        running_cost += D[C[i]][C[i+1]] + D[C[num_cities-1]][C[0]]
    return running_cost
