import numpy as np
from costFunction import *
from Algorithm.adj_mat import *
from Algorithm.CrossoverOperator import *
from Algorithm.MutationOperator import *
from Algorithm.Replacement import *

class EA:
    # INITIALISE ALGORITHM CONSTRUCTOR
    def __init__(self, TSP, populationSize, tournamentSize, mutationType='singleSwap', crossoverType='crossoverWithFix', RNG_Seed=42,replacementType = 'FIFO', terminationCriterion=10000):

        self.TSP = TSP
        self.populationSize = populationSize
        self.tournamentSize = tournamentSize
        self.mutationType = mutationType
        self.crossoverType = crossoverType

        # DEFINE A NUMPY RANDOM NUMBER GENERATOR FOR THE ALGORITHM TO USE
        self.RNG_Seed = RNG_Seed
        self.RNG = np.random.default_rng(seed=self.RNG_Seed)

    # DEFINE THE FUNCTION FOR CONVERTING TSPLIB XML TO EQUIVALENT ADJACENCY MATRIX
    def adjacency_matrix(self):
        return adj_mat(self.TSP)

    # DEFINE THE FUNCTION THAT RETURNS AN ARRAY OF ARRAYS REPRESENTING EACH INITIAL POPULATION MEMBER
    def population_init(self):
        D = self.adjacency_matrix() # construct the adjacency matrix

        # CONSTRUCT A 2D ARRAY OF SIZE populationSize WITH THE SECOND COLUMN
        # BEING A 1 x (size of D) VECTOR OF RANDOMLY GENERATED INTEGERS FROM 0 TO (size of D)-1
        # AND THE FIRST COLUMN BEING ITS ASSOCIATED FITNESS FUNCTION

        population = np.zeros((2, self.populationSize), dtype=object)  # initialise population array with 2 columns and
        # populationSize number of rows

        for i in range(self.populationSize):
            population[1][i] = self.RNG.permutation(range(len(D)))  # Construct second column Tour Vector
            population[0][i] = cost(D,population[1][i],len(D)) # Evaluate fitness of this member
        return population



