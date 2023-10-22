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
        self.replacementTypeDict = {'Random':self.random,'FIFO': self.fifo} # a dictionary of all valid functions

        # DEFINE A NUMPY RANDOM NUMBER GENERATOR FOR THE ALGORITHM TO USE
        self.RNG_Seed = RNG_Seed
        self.RNG = np.random.default_rng(seed=self.RNG_Seed)

        self.FIFOindex = replacement_FIFOindex


    def applyReplacement(self):

        if self.replacementType in self.replacementTypeDict:
            return self.replacementTypeDict[self.replacementType](self.population, self.child1, self.child2)
        else:
            raise Exception("Invalid Replacement Function ( " + self.replacementType + " ).\n Valid options are ",
                            [key for key in self.replacementTypeDict])

    # DEFINE THE METHOD TO IMPLEMENT FIFO AGE BASED REPLACEMENT
    def fifo(self,population, child1, child2):

        # COPY CONTENTS OF OLD POPULATION TO NEW POPULATION
        newPopulation = copy.deepcopy(population)
        # RANDOMLY SELECT ONE OF THE OFFSPRING
        candidateChild = self.RNG.choice([child1,child2])

        # CALCULATE FITNESS FUNCTION OF THIS CHILD
        candidateChildFitness = cost(self.adj_mat,candidateChild,len(self.adj_mat))
        # print('Candidate Child ', candidateChild, ' and its fitness: ', candidateChildFitness) # For debugging purposes

        # REPLACE THE FIFOindex -th POPULATION MEMBER WITH candidateChild
        newPopulation[0][self.FIFOindex] = candidateChildFitness
        newPopulation[1][self.FIFOindex] = candidateChild

        # CHECK TO VERIFY THAT FIFOindex HAS NOT REACHED population_size, IF SO THEN REINITIALISE IT
        if self.FIFOindex == len(population[0])-1:
            self.FIFOindex = 0
        else:
            self.FIFOindex += 1

        return self.FIFOindex, newPopulation

    # DEFINE THE METHOD THAT IMPLEMENTS A SINGLE GENERATION AGE BASED REPLACEMENT
    def random(self,population,child1,child2):
        # FIND THE INDEX IN INITIAL
        return 0