import numpy as np
import TSPtoADJ as tsp
import costFunction
import Algorithm


if __name__ == '__main__':
    # # importing the XML file
    # weights = tsp.read_tsplib('assets/burma14.xml')
    #
    # # printing the weights matrix
    # tsp.print_matrix(weights)
    #
    # # Test costFunction for tour [1,2,3,4,5,6,7,8...,58] for brazil
    # tour_vec = np.array(range(0, len(weights)))
    # print(costFunction.cost(weights, tour_vec, len(weights)))

    David = Algorithm.EA('assets/burma14.xml', 10, 2, RNG_Seed=10)
    David.population_init()

