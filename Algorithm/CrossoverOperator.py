import numpy as np
from Algorithm.helperFunctions import *
class CrossoverOperator:
    def __init__(self, parent1, parent2, crossoverType,RNG_Seed=42):
        self.parent1 = parent1
        self.parent2 = parent2
        self.crossoverType = crossoverType

        # DEFINE A NUMPY RANDOM NUMBER GENERATOR FOR THE ALGORITHM TO USE
        self.RNG_Seed = RNG_Seed
        self.RNG = np.random.default_rng(seed=self.RNG_Seed)

    def processCrossover(self):
        if self.crossoverType == 'orderedCrossover':
            return self.orderedCrossover(self.parent1, self.parent2)
        elif self.crossoverType == 'cycleCrossover':
            return self.cycleCrossover(self.parent1, self.parent2)
        else:
            raise Exception('Invalid Crossover Operator/n Valid options are orderedCrossover and cycleCrossover')


    def orderedCrossover(self, parent1, parent2):
        """
        This algorithm takes the two parents and randomly slices both of them at a specific point in the array. The right
        hand side (RHS) split points are swapped between parents and the remainder (LHS subset) are taken and ordered
        according to the original order of the other respective parent
        :param parent1:
        :param parent2:
        :return: child1:
        :return: child2:
        """
        # Generate random crossover point
        crossoverPoint = self.RNG.choice(len(parent1))

        # SPLIT BOTH PARENTS ACCORDING TO XOVER POINT
        parent1_leftSplit = parent1[:crossoverPoint] # get left hand side slice
        parent2_leftSplit = parent2[:crossoverPoint]

        parent1_rightSplit = parent1[crossoverPoint:]  # get right hand side slice
        parent2_rightSplit = parent2[crossoverPoint:]

        # SWAP THE SECOND SECTIONS OF EACH PARENT WITH EACH OTHER
        parent1_rightSwap = parent2_rightSplit
        parent2_rightSwap = parent1_rightSplit

        # FOR BOTH PARENTS
        # SUBTRACT THE REMAINING SUBSET FROM THE ORIGINAL PARENT

        parent1_subsetRemainder = [x for x in parent1 if not x in parent1_rightSwap]
        parent2_subsetRemainder = [x for x in parent2 if not x in parent2_rightSwap]

        # ORDER THIS SUBTRACTED SUBSET ACCORDING TO THE ORDER OF THE ORIGINAL RESP. PARENT
        sortAccording(parent1_subsetRemainder, parent1, len(parent1_subsetRemainder), len(parent1))
        sortAccording(parent2_subsetRemainder, parent2, len(parent2_subsetRemainder),
                                            len(parent2))

        # CONCATENATE THE LEFT HAND SIDE AND NEW RIGHT HAND SIDE OF EACH PARENT TO RESULT IN THE RESP. CHILD
        child1 = np.concatenate([parent1_subsetRemainder, parent1_rightSwap], axis=0 )
        child2 = np.concatenate([parent2_subsetRemainder, parent2_rightSwap], axis=0)

        # CHECK THAT EACH CHILD IS A VALID POPULATION MEMBER (I.E. A PERMUTATION OF SUBSET [1:len(D)]
        checkPermutation(parent1, child1)
        checkPermutation(parent2, child2)


        return child1, child2

    # DEFINE THE METHOD THAT IMPLEMENTS THE CYCLE CROSSOVER ALGORITHM
    def cycleCrossover(self, parent1, parent2):
        """
        The Cycle Crossover operator identifies a number of so-called cycles between two parent chromosomes.
        Then, to form Child 1, cycle one is copied from parent 1, cycle 2 from parent 2, cycle 3 from parent 1, and so on.

        This Algorithm has been adapted from this Forum Answer (DATE ACCESSED: 21 OCT 2023):
        https://codereview.stackexchange.com/questions/226179/easiest-way-to-implement-cycle-crossover
        :param parent1:
        :param parent2:
        :return: child1:
        :return: child2:
        """
        # SET THE PARENT ARRAYS TO LIST FOR THIS ALGORITHM
        parent1 = parent1.tolist()
        parent2 = parent2.tolist()
        # INITIALISE CYCLES ARRAY AND SET cycle_no TO 1
        cycles = [-1] * len(parent1)
        cycle_no = 1
        cyclestart = (i for i, v in enumerate(cycles) if v < 0) # cyclestart is a generator that
        # returns the next place for a cycle to start.

        for pos in cyclestart:

            # WHILST THE CYCLE NUMBER OF PARENT ELEMENT IS UNDEFINED (= -1) FIND THE CORRESPONDING CYCLE
            while cycles[pos] < 0:
                cycles[pos] = cycle_no
                pos = parent1.index((parent2[pos]))

            cycle_no += 1
        # print('Cycles: ', cycles)

        # GENERATE THE OFFSPRING BY INSERTING ALTERNATING CYCLES TO EACH CHILD
        child1 = np.array([parent1[i] if n % 2 else parent2[i] for i, n in enumerate(cycles)])
        child2 = np.array([parent2[i] if n % 2 else parent1[i] for i, n in enumerate(cycles)])

        # CHECK THAT EACH CHILD IS A VALID POPULATION MEMBER (I.E. A PERMUTATION OF SUBSET [1:len(D)]
        checkPermutation(parent1, child1)
        checkPermutation(parent2, child2)

        return child1, child2