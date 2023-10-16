import TSPtoADJ as tsp


if __name__ == '__main__':
    # importing the XML file
    weights = tsp.read_tsplib('assets/burma14.xml')

    # printing the weights matrix
    tsp.print_matrix(weights)

