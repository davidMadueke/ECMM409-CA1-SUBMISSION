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
        self.terminationCriterion = terminationCriterion
        self.mutationType = mutationType
        self.crossoverType = crossoverType
        self.replacementType = replacementType

        # DEFINE A NUMPY RANDOM NUMBER GENERATOR FOR THE ALGORITHM TO USE
        self.RNG_Seed = RNG_Seed
        self.RNG = np.random.default_rng(seed=self.RNG_Seed)

        # FOR MULTI SWAP MUTATION OPERATOR
        self.multiSwapAmount = 5

        # FOR FIFO REPLACEMENT FUNCTION
        self.replacement_FIFOindex = 0

    # SET MUTATION OPERATOR multiSwapAmount CONSTRUCTOR METHOD
    def setMultiSwapAmount(self, value=5):
        self.multiSwapAmount = value

    # DEFINE THE FUNCTION FOR CONVERTING TSPLIB XML TO EQUIVALENT ADJACENCY MATRIX
    def adjacency_matrix(self):
        return adj_mat(self.TSP)

    # DEFINE THE FUNCTION THAT RETURNS AN ARRAY OF ARRAYS REPRESENTING EACH INITIAL POPULATION MEMBER
    def population_init(self):
        """
         CONSTRUCT A 2D ARRAY OF SIZE populationSize WITH THE SECOND COLUMN
         BEING A 1 x (size of D) VECTOR OF RANDOMLY GENERATED INTEGERS FROM 0 TO (size of D)-1
        AND THE FIRST COLUMN BEING ITS ASSOCIATED FITNESS FUNCTION
        """
        D = self.adjacency_matrix() # construct the adjacency matrix

        population = np.zeros((2, self.populationSize), dtype=object)  # initialise population array with 2 columns and
        # populationSize number of rows

        for i in range(self.populationSize):
            population[1][i] = self.RNG.permutation(range(len(D)))  # Construct second column Tour Vector
            population[0][i] = cost(D,population[1][i],len(D)) # Evaluate fitness of this member
        return population

    # DEFINE THE METHOD THAT PERFORMS TOURNAMENT SELECTION
    def tournamentSelection(self, population):
        # CHOOSE N RANDOM CHROMOSOMES FROM population (WITHOUT ANY DUPLICATE CHOICES)
        tournament = self.RNG.choice(population, self.tournamentSize, replace=False, axis=1)
        # print(tournament) # FOR DEBUGGING PURPOSES

        # USE THE CALCULATED FITNESS FUNCTIONS TO FIND THE BEST CANDIDATE CHROMOSOME
        tournamentFitness = tournament[0]
        tournament_Victors = list(np.where(tournamentFitness==(np.min(tournamentFitness)))[0]) # find and return all instances with the lowest fitness
        # Note we also have to add list(...[0]) syntax as np.where returns a tuple of (array[],) in this case

        # if len(tournament_Victors) >= 2:
        #     print('tournament victors ',tournament_Victors) # FOR DEBUGGING PURPOSES

        # IF THERE ARE MORE THAN 1 CHROMOSOME WITH THE LOWEST FITNESS, THEN RANDOMLY SELECT ONE OF THEM
        selectedParentIndex = self.RNG.choice(tournament_Victors)
        # print('Selected Parent Index: ',selectedParentIndex) # FOR DEBUGGING PURPOSES
        selectedParent = tournament[1][selectedParentIndex]

        # print('Selected Parent: ', selectedParent) # FOR DEBUGGING PURPOSES
        return selectedParent

    # DEFINE THE METHOD THAT APPLIES THE ALGORITHM
    def applyEA(self):
        # INITIALISE POPULATION MATRIX WITH ASSOCIATED FITNESS FUNCTIONS IN FIRST COLUMN
        population = self.population_init()

        # INITIALISE ANY RECURRING INDICES AND CONSTANTS
        FIFOindex = self.replacement_FIFOindex

        # LOOP OVER THIS SUPER-ALGORITHM UP TO terminationCriterion TIMES
        for i in range(self.terminationCriterion + 1):
            # PERFORM TOURNAMENT SELECTION TWICE TO GET TWO PARENTS
            parentA = self.tournamentSelection(population)
            parentB = self.tournamentSelection(population)


            # APPLY A SINGLE POINT CROSSOVER TO THE TWO PARENTS TO GET TWO CHILDREN childC and childD RESP.
            crossover = CrossoverOperator(parentA, parentB, self.crossoverType, self.RNG_Seed) # create crossover object
            childC, childD = crossover.processCrossover()

            # APPLY A MUTATION OPERATOR TO THE TWO CHILDREN TO GET TWO MUTATED CHILDREN childE and childF RESP.
            mutationC = MutationOperator(
                np.array(childC,dtype=np.int8),
                self.mutationType,
                multiSwapAmount=self.multiSwapAmount,
                RNG_Seed=self.RNG_Seed)
            mutationD = MutationOperator(
                np.array(childD,dtype=np.int8),
                self.mutationType,
                multiSwapAmount=self.multiSwapAmount,
                RNG_Seed=self.RNG_Seed)

            childE = mutationC.processMutation()
            childF = mutationD.processMutation()


            # APPLY A REPLACEMENT FUNCTION (CHECK IF IT IS FIFO AS IT HAS DIFFERENT RETURN VALUES)
            replacement = Replacement(population,
                                      self.adjacency_matrix(),
                                      childE, childF,
                                      self.replacementType,
                                      RNG_Seed=self.RNG_Seed,
                                      replacement_FIFOindex=FIFOindex)
            if self.replacementType == 'FIFO':
                FIFOindex, updatedPopulation = replacement.applyReplacement()
            else:
                updatedPopulation = replacement.applyReplacement()

        # EVALUATE WHICH TOUR HAS THE LOWEST FITNESS AFTER THE ITERATIONS HAVE FINISHED
        finalPopulationFitness = updatedPopulation[0]
        finalPopulation_Victors = np.where(
            finalPopulationFitness == (np.min(finalPopulationFitness)))  # find and return all instances with the lowest fitness

        # IF THERE ARE MORE THAN 1 CHROMOSOME WITH THE LOWEST FITNESS, THEN RANDOMLY SELECT ONE OF THEM
        selectedTourIndex = self.RNG.choice(finalPopulation_Victors)
        selectedTour = updatedPopulation[1][selectedTourIndex]
        selectedTourFitness = updatedPopulation[0][selectedTourIndex]

        # CHECK THAT THE FINAL TOUR IS VALID (I.E. A PERMUTATION OF SUBSET [1:len(D)]
        # checkPermutation(selectedTour, np.arange(len(population[1][0])))

        return selectedTour.item(), selectedTourFitness




