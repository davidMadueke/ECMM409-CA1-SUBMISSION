import numpy as np


def cost(adj_mat, tour_vec, num_cities):
    D = np.array(adj_mat)
    C = np.array(tour_vec)
    running_cost = 0
    for i in range(0, num_cities-2):
        running_cost += D[C[i]][C[i+1]] + D[C[num_cities-1]][C[0]]
    return running_cost
