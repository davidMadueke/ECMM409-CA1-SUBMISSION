import numpy as np

from costFunction import *
import copy

class Replacement:
    def __init__(self, population, adj_mat, child1, child2, replacementType, RNG_Seed=42, replacement_FIFOindex=0):
        """
        CONSTRUCTOR METHOD FOR Replacement CLASS. THESE ALGORITHMS ARE BASED ON (Eiben et al. Introduction to
        Evolutionary Computing pg 88 - 89).
        :param population:
        :param adj_mat: The Adjacency Matrix representing the TSP
        :param child1:
        :param child2:
        :param replacementType: Valid options are: FIFO, Random, ReplaceWorst, Elitism, RoundRobin, muPlusLambda
        :param RNG_Seed: The seed integer used for the pseudo random number generator numpy object
        :param replacement_FIFOindex: The index (for iterative applications of Replace) used to track the FIFO replacement Algorithm
        """
        self.population = population
        self.adj_mat = adj_mat
        self.child1 = child1
        self.child2 = child2

        self.replacementType = replacementType
        self.replacementTypeDict = {'Random':self.random,
                                    'FIFO': self.fifo,
                                    'ReplaceWorst': self.replaceWorst,
                                    'Elitism': self.elitism,
                                    'RoundRobin': self.roundRobin,
                                    'muPlusLambda': self.muPlusLambda} # a dictionary of all valid functions

        # DEFINE A NUMPY RANDOM NUMBER GENERATOR FOR THE ALGORITHM TO USE
        self.RNG_Seed = RNG_Seed
        self.RNG = np.random.default_rng(seed=self.RNG_Seed)

        self.FIFOindex = replacement_FIFOindex # used for the FIFO replacement strategy


    def applyReplacement(self):

        if self.replacementType in self.replacementTypeDict:
            return self.replacementTypeDict[self.replacementType](self.population, self.child1, self.child2)
        else:
            raise Exception("Invalid Replacement Function ( " + self.replacementType + " ).\n Valid options are ",
                            [key for key in self.replacementTypeDict])

    # DEFINE THE METHOD TO IMPLEMENT FIFO AGE BASED REPLACEMENT
    def fifo(self,population, child1, child2):
        """
        This algorithm randomly selects one of the children and replaces one of the original members of the population in
        a first in first out (FIFO) manner

        :param population: The initial Population before replacement. It is a 2D Array that takes the form
                                array[array[FitnessScore], array[TourVector]]
        :param child1: First Offspring generated by Crossover and Mutation Stages
        :param child2: Second Offspring generated by Crossover and Mutation Stages
        :return: newPopulation - A 2D Array that takes the form array[array[FitnessScore], array[TourVector]]
        """
        # COPY CONTENTS OF OLD POPULATION TO NEW POPULATION
        newPopulation = copy.deepcopy(population)
        # RANDOMLY SELECT ONE OF THE OFFSPRING
        candidateChild = self.RNG.choice([child1,child2])

        # CALCULATE FITNESS FUNCTION OF THIS CHILD
        candidateChildFitness = cost(self.adj_mat,candidateChild,len(self.adj_mat))


        # REPLACE THE FIFOindex -th POPULATION MEMBER WITH candidateChild
        newPopulation[0][self.FIFOindex] = candidateChildFitness
        newPopulation[1][self.FIFOindex] = candidateChild

        # CHECK TO VERIFY THAT FIFOindex HAS NOT REACHED population_size, IF SO THEN REINITIALISE IT
        if self.FIFOindex == len(population[0])-1:
            self.FIFOindex = 0
        else:
            self.FIFOindex += 1

        return self.FIFOindex, newPopulation

    # DEFINE THE METHOD THAT IMPLEMENTS A SINGLE GENERATION AGE BASED RANDOM REPLACEMENT
    def random(self,population,child1,child2):
        """
        For this algorithm, two members of the initial population are to be randomly selected for replacement by the
        respective two children

        :param population: The initial Population before replacement. It is a 2D Array that takes the form
                                array[array[FitnessScore], array[TourVector]]
        :param child1: First Offspring generated by Crossover and Mutation Stages
        :param child2: Second Offspring generated by Crossover and Mutation Stages
        :return: newPopulation - A 2D Array that takes the form array[array[FitnessScore], array[TourVector]]
        """
        # COPY CONTENTS OF OLD POPULATION TO NEW POPULATION
        newPopulation = copy.deepcopy(population)

        # CALCULATE FITNESS FUNCTION OF THE TWO CHILDREN
        child1Fitness = cost(self.adj_mat,child1,len(self.adj_mat))
        child2Fitness = cost(self.adj_mat,child2,len(self.adj_mat))

        # RANDOMLY SELECT TWO PARENTS IN population TO BE REPLACED BY THE OFFSPRING
        replacementIndices = self.RNG.choice(len(population[0]), 2, replace=False)

        # SET EACH CHILD TO BE THE VALUES FOR THE INDICES IN replacementIndices WITHIN population
        newPopulation[0][replacementIndices[0]] = child1Fitness
        newPopulation[1][replacementIndices[0]] = child1

        newPopulation[0][replacementIndices[1]] = child2Fitness
        newPopulation[1][replacementIndices[1]] = child2

        return newPopulation

    # DEFINE THE METHOD THAT IMPLEMENTS THE FITNESS BASED replaceWorst REPLACEMENT STRATEGY
    def replaceWorst(self,population, child1, child2):
        """
        Here, this algorithm selects the worst two performing populations members and replaces them with the offspring set
        :param population: The initial Population before replacement. It is a 2D Array that takes the form
                                array[array[FitnessScore], array[TourVector]]
        :param child1: First Offspring generated by Crossover and Mutation Stages
        :param child2: Second Offspring generated by Crossover and Mutation Stages
        :return: newPopulation - A 2D Array that takes the form array[array[FitnessScore], array[TourVector]]
        """
        # COPY CONTENTS OF OLD POPULATION TO NEW POPULATION
        newPopulation = copy.deepcopy(population)

        # SORT ELEMENTS OF POPULATION BASED ON FITNESS AND SELECT LAST TWO ELEMENTS
        replacementCandidates = np.array([np.unique(newPopulation[0])[-1], np.unique(newPopulation[0])[-2]])
        # we are selecting last two elements as they have the worst fitness (highest score)

        # FIND THE CORRESPONDING INDICES FOR THESE FITNESS ELEMENTS
        # IF THERE ARE MORE THAN ONE INDEX WITH THE SAME RESP. FITNESS, TAKE THE FIRST ONE (WLOG)
        replacementCandidate1 = np.argwhere(newPopulation[0]==replacementCandidates[0]).flatten()[0]
        replacementCandidate2 = np.argwhere(newPopulation[0]==replacementCandidates[1]).flatten()[0]
        # given np.argwhere() returns an ndarray, we are flattening it and taken the resultant first element

        # SET THE VALUES OF replacementCandidate INDICES IN POPULATION TO BE THE OFFSPRING
        newPopulation[0][replacementCandidate1] = cost(self.adj_mat,child1, len(child1))
        newPopulation[0][replacementCandidate2] = cost(self.adj_mat, child2, len(child2)) # Find fitnesses of Children

        newPopulation[1][replacementCandidate1] = child1
        newPopulation[1][replacementCandidate2] = child2

        return newPopulation

    # DEFINE THE METHOD THAT IMPLEMENTS THE FITNESS BASED elitism REPLACEMENT STRATEGY
    def elitism(self,population, child1, child2):
        """
        A METHOD THAT IMPLEMENTS THE FITNESS BASED elitism REPLACEMENT STRATEGY.
        This scheme is commonly used in conjunction with age-based
        and stochastic fitness-based replacement schemes, to prevent the loss of the
        current fittest member of the population. In essence a trace is kept of the
        current fittest member, and it is always kept in the population. Thus, if it is
        chosen in the group to be replaced, and none of the offspring being inserted
        into the population has equal or better fitness, then it is kept and one of the
        offspring is discarded. (Eiben and Smith, 2015)

        :param population: The initial Population before replacement. It is a 2D Array that takes the form
                                array[array[FitnessScore], array[TourVector]]
        :param child1: First Offspring generated by Crossover and Mutation Stages
        :param child2: Second Offspring generated by Crossover and Mutation Stages
        :return: newPopulation - A 2D Array that takes the form array[array[FitnessScore], array[TourVector]]
        """
        # COPY CONTENTS OF OLD POPULATION TO NEW POPULATION
        newPopulation = copy.deepcopy(population)

        # FIND THE INDEX OF THE POPULATION MEMBER WITH THE BEST FITNESS
        bestParents = list(np.where(newPopulation[0] == (np.min(newPopulation[0])))[
                                      0])  # find and return all instances with the lowest fitness
        # Note we also have to add list(...[0]) syntax as np.where returns a tuple of (array[], any) in this case

        # IF THERE ARE MORE THAN 1 CHROMOSOME WITH THE BEST FITNESS, THEN RANDOMLY SELECT ONE OF THEM
        selectedBestParentIndex = self.RNG.choice(bestParents)
        selectedBestParent = population[1][selectedBestParentIndex]

        # APPLY PARTS OF THE random REPLACEMENT ALGORITHM TO FIND THE INDICES TO REPLACE
        # CALCULATE FITNESS FUNCTION OF THE TWO CHILDREN
        child1Fitness = cost(self.adj_mat, child1, len(self.adj_mat))
        child2Fitness = cost(self.adj_mat, child2, len(self.adj_mat))

        # CREATE A POPULATION MATRIX OF JUST THE OFFSPRING
        offspringPopulation = np.zeros((2, len(population)), dtype=object)
        offspringPopulation[0][0], offspringPopulation[0][1] = child1Fitness, child2Fitness
        offspringPopulation[1][0], offspringPopulation[1][1] = child1, child2

        # RANDOMLY SELECT TWO PARENTS IN population TO BE REPLACED BY THE OFFSPRING
        replacementIndices = self.RNG.choice(len(population[0]), 2, replace=False)


        # CHECK THAT IF selectedBestParent IS CHOSEN THEN IT ISNT REPLACED UNLESS ONE OF THE CHILDREN HAS A BETTER FITNESS
        if selectedBestParentIndex in replacementIndices:
            # DEDUCE THE OTHER REPLACEMENT INDEX
            notSelectedBestParentIndex = replacementIndices[replacementIndices != selectedBestParentIndex].item()

            # DEDUCE THE BEST OFFSPRING OUT OF THE TWO CHILDREN
            bestOffspringindex = list(np.where(offspringPopulation[0] == (np.min(offspringPopulation[0])))[0])[0]
            bestOffspringFitness = offspringPopulation[0][bestOffspringindex]
            bestOffspring = offspringPopulation[1][bestOffspringindex]

            # CHECK THAT THE BEST FIT OFFSPRING IS OR ISNT BETTER THAN selectedBestParent
            if population[0][selectedBestParentIndex] >= bestOffspringFitness:
                newPopulation[0][selectedBestParentIndex] = bestOffspringFitness # Replace bestParent with bestOffspring
                newPopulation[1][selectedBestParentIndex] = bestOffspring

                # REPLACE THE OTHER PARENT WITH THE OTHER OFFSPRING (THE WORSE ONE)
                notBestOffspringFitness = np.delete(offspringPopulation[0], bestOffspringindex).item()
                notBestOffspring = np.delete(offspringPopulation[1], bestOffspringindex).item()

                newPopulation[0][notSelectedBestParentIndex] = notBestOffspringFitness
                newPopulation[1][notSelectedBestParentIndex] = notBestOffspring
                return newPopulation

            # DISCARD RANDOMLY ONE OF THE OFFSPRING
            randomOffSpringIndex = self.RNG.choice(2) # 2 is chosen given that there are only 2 offspring

            newPopulation[0][notSelectedBestParentIndex] = offspringPopulation[0][randomOffSpringIndex]
            newPopulation[1][notSelectedBestParentIndex] = offspringPopulation[1][randomOffSpringIndex]
            return  newPopulation

        # OTHERWISE RETURN THE SAME newPopulation AS IN THE random ALGORITHM CASE
        # SET EACH CHILD TO BE THE VALUES FOR THE INDICES IN replacementIndices WITHIN population
        newPopulation[0][replacementIndices[0]] = child1Fitness
        newPopulation[1][replacementIndices[0]] = child1

        newPopulation[0][replacementIndices[1]] = child2Fitness
        newPopulation[1][replacementIndices[1]] = child2

        return newPopulation

    # DEFINE A METHOD THAT IMPLEMENTS THE ROUND ROBIN FITNESS BASED REPLACEMENT ALGORITHM
    def roundRobin(self,population, child1, child2, roundRobinSize=10):
        """
        The method works by holding pairwise tournament competitions in round-robin format,
        where each individual is evaluated against q others randomly chosen from the merged parent and offspring populations.
        For each comparison, a “win” is assigned if the individual is better than its opponent.
        After finishing all tournaments, the μ individuals with the greatest number of wins are selected.
        Typically, q = 10 is recommended in Evolutionary Pro-gramming.

        :param population:
        :param child1: First Offspring generated by Crossover and Mutation Stages
        :param child2: Second Offspring generated by Crossover and Mutation Stages
        :param roundRobinSize: The size of the round-robin tournament generated
        :return: newPopulation - A 2D Array that takes the form array[array[FitnessScore], array[TourVector]]
        """
        # APPLY AN INITIAL CHECK TO MAKE SURE THAT roundRobinSize IS < len(population)
        if roundRobinSize > len(population):
            Exception('Size of Round Robin Tournament ', roundRobinSize, ' is not less than or equal to the population, '
                      , len(population))
        # INITIALISE A NEW POPULATION ARRAY
        newPopulation = copy.deepcopy(population)

        # GENERATE THE ROUND ROBIN TOURNAMENT

        ## COMBINE population AND OFFSPRING INTO A TOTAL POOL
        populationAndOffspring = copy.deepcopy(population).tolist()

        ### CALCULATE FITNESS FUNCTION OF THE TWO CHILDREN
        child1Fitness = cost(self.adj_mat, child1, len(self.adj_mat))
        child2Fitness = cost(self.adj_mat, child2, len(self.adj_mat))

        children = np.array([child1, child2])
        childrenFitness = np.array([child1Fitness,child2Fitness])
        for i in range(2):
            populationAndOffspring[1].append(children[i])
            populationAndOffspring[0].append(childrenFitness[i])


        ## SELECT AT RANDOM roundRobinSize NUMBER OF TOURNAMENT PLAYERS
        tournamentindices = self.RNG.choice(len(populationAndOffspring[0]),roundRobinSize,replace=False)
        tournament = np.zeros((3, roundRobinSize), dtype=object) # There is a 3rd column to count number of wins each
        # player has
        for i in range(roundRobinSize):
            tournament[1][i] = populationAndOffspring[1][tournamentindices[i]]
            tournament[0][i] = populationAndOffspring[0][tournamentindices[i]]
        # HOLD THE ROUND ROBIN TOURNAMENT COMPARING EACH i AND j IN THE tournament ARRAY
        for i in range(roundRobinSize):
            for j in range(roundRobinSize):
                if tournament[0][i] < tournament[0][j]:
                    tournament[2][i] += 1 # Add 1 to Tournament score for ith element if it is lower than jth element

        # APPLY SIMILAR SUB ALGORITHM TO replaceWorst IN ORDER TO FIND THE population

        # SORT ELEMENTS OF tournament BASED ON TOURNAMENT SCORE AND SELECT LAST len(population) ELEMENTS
        tournamentVictorsSorted = np.array([np.sort(tournament[2])[-(i+1)] for i in range(len(tournament[2]+1))])
        # we are selecting last len(population) elements as they have the highest tournament scores
        # we are also using 1 indexing for the for loop list comprehension

        # FIND THE CORRESPONDING INDICES FOR THESE TOURNAMENT SCORE ELEMENTS
        # IF THERE ARE MORE THAN ONE INDEX WITH THE SAME RESP. TOURNAMENT SCORE, TAKE THE FIRST ONE (WLOG)

        tournamentVictorsIndices = []
        duplicateCounter = 0
        for i in range(len(tournamentVictorsSorted)):
            placeholder = np.argwhere(tournament[2] == tournamentVictorsSorted[i]).flatten()
            if len(placeholder) == 1:
                tournamentVictorsIndices.append(placeholder[0])
            else:
                tournamentVictorsIndices.append(placeholder[duplicateCounter])
                if duplicateCounter == len(placeholder) - 1:
                    duplicateCounter = 0
                else:
                    duplicateCounter += 1

        # given np.argwhere() returns an ndarray, we are flattening it and taken the resultant first element

        # ADD THE RESULTANT VALUES FOR THE TOURNAMENT VICTORS TO newPopulation
        for i in range(len(tournamentVictorsIndices)):
            newPopulation[0][i] = tournament[0][tournamentVictorsIndices[i]]
            newPopulation[1][i] = tournament[1][tournamentVictorsIndices[i]]
        print('New Population: ', newPopulation)

        return newPopulation

    # DEFINE THE METHOD THAT IMPLEMENTS THE muPlusLambda ALGORITHM
    def muPlusLambda(self,population, child1, child2):
        """
        " In general [the mu + lambda algortihm], it refers to the case where the
        set of offspring and parents are merged and ranked according to (estimated)
        fitness, then the top μ are kept to form the next generation. " - (Eiben et al., 2015)

        :param population:
        :param child1: First Offspring generated by Crossover and Mutation Stages
        :param child2: Second Offspring generated by Crossover and Mutation Stages
        :return: newPopulation - A 2D Array that takes the form array[array[FitnessScore], array[TourVector]]
        """
        # COPY CONTENTS OF OLD POPULATION TO NEW POPULATION
        newPopulation = copy.deepcopy(population)

        # MERGE OFFSPRING AND INITIAL POPULATION
        populationAndOffspring = copy.deepcopy(population).tolist()

        ## CALCULATE FITNESS FUNCTION OF THE TWO CHILDREN
        child1Fitness = cost(self.adj_mat, child1, len(self.adj_mat))
        child2Fitness = cost(self.adj_mat, child2, len(self.adj_mat))

        children = [child1, child2]
        childrenFitness = [child1Fitness, child2Fitness]

        for i in range(2):
            populationAndOffspring[1].append(children[i])
            populationAndOffspring[0].append(childrenFitness[i])


        # ORDER THIS MERGED POPULATION BASED ON THEIR FITNESS (BEST TO WORST)
        # SORT ELEMENTS OF tournament BASED ON TOURNAMENT SCORE AND SELECT LAST len(population) ELEMENTS
        populationAndOffspringSorted = np.array([np.sort(populationAndOffspring[0])[i]
                                                 for i in range(len(populationAndOffspring[1]))])
        # we are selecting last len(population) elements as they have the highest tournament scores

        # SET newPopulation TO BE THE BEST (population_size) NUMBER OF MEMBERS

        ## FIND THE CORRESPONDING INDICES FOR THESE TOURNAMENT SCORE ELEMENTS
        ### IF THERE ARE MORE THAN ONE INDEX WITH THE SAME RESP. TOURNAMENT SCORE, TAKE THE FIRST ONE (WLOG)
        bestPopulationAndOffspringIndices = []
        duplicateCounter = 0
        for i in range(len(population[0])):
            placeholder = np.argwhere(populationAndOffspring[0] == populationAndOffspringSorted[i]).flatten()
            if len(placeholder) == 1:
                bestPopulationAndOffspringIndices.append(placeholder[0])
            else:
                bestPopulationAndOffspringIndices.append(placeholder[duplicateCounter])
                if duplicateCounter == len(placeholder) - 1:
                    duplicateCounter = 0
                else:
                    duplicateCounter += 1
        # given np.argwhere() returns an ndarray, we are flattening it and taken the resultant first element

        # ADD THE RESULTANT VALUES FOR THE TOURNAMENT VICTORS TO newPopulation
        for i in range(len(bestPopulationAndOffspringIndices)):
            newPopulation[0][i] = populationAndOffspring[0][bestPopulationAndOffspringIndices[i]]
            newPopulation[1][i] = populationAndOffspring[1][bestPopulationAndOffspringIndices[i]]

        return newPopulation