import numpy
import numpy as np
from Algorithm.helperFunctions import *

class MutationOperator:
    def __init__(self, child, mutationType, multiSwapAmount=5, RNG_Seed=42):
        self.child = child
        self.mutationType = mutationType
        self.multiSwapAmount = multiSwapAmount

        # DEFINE A NUMPY RANDOM NUMBER GENERATOR FOR THE ALGORITHM TO USE
        self.RNG_Seed = RNG_Seed
        self.RNG = np.random.default_rng(seed=self.RNG_Seed)

        self.mutationTypeDict = {'singleSwap': self.singleSwap,
                                    'multiSwap': self.multiSwap,
                                    'inversion': self.inversion,
                                    'insert': self.insert,
                                    'scramble': self.scramble}  # a dictionary of all valid functions

    def processMutation(self):
        if self.mutationType in self.mutationTypeDict:
            return self.mutationTypeDict[self.mutationType](self.child)
        else:
            raise Exception("Invalid Replacement Function ( " + self.mutationType + " ).\n Valid options are ",
                            [key for key in self.mutationTypeDict])

    # DEFINE THE METHOD THAT IMPLEMENTS THE SINGLE SWAP ALGORITHM
    def singleSwap(self, child):
        # COPY CONTENTS OF child TO NEW mutatedChild ARRAY
        mutatedChild = np.zeros(len(child),dtype=np.int8) # Have to initialise like this as python does not support
        # constant variables
        mutatedChild += child

        # GENERATE A 2 DISTINCT ELEMENT RANDOM SUBSET FROM THE SET OF INTEGERS UP TO |child| - 1
        mutationIndices = self.RNG.choice(len(child),2, replace=False)
        # print('point 1: ', child[mutationIndices[0]],' ', 'point 2: ', child[mutationIndices[1]])
        # print('Mutation Indices: ', mutationIndices)


        np.put(mutatedChild, mutationIndices, [child[mutationIndices[1]], child[mutationIndices[0]]])

        # APPLY PERMUTATION CONTINUITY CHECK BETWEEN CHILD AND MUTATED CHILD
        checkPermutation(child, mutatedChild)

        return mutatedChild

    # DEFINE THE MULTISWAP METHOD AS SUCCESSIVE ITERATIONS OF SINGLE SWAP UP TO multiSwapAmount TIMES
    def multiSwap(self, child):
        # COPY CONTENTS OF child TO NEW mutatedChild ARRAY
        mutatedChild = np.zeros(len(child), dtype=np.int8)
        mutatedChild += child

        for i in range(self.multiSwapAmount):
            # PERFORM THE SAME ALGORITHM USED IN SINGLE SWAP
            mutationIndices = self.RNG.choice(len(child), 2, replace=False)

            # print('point 1: ', mutatedChild[mutationIndices[0]],' ', 'point 2: ', mutatedChild[mutationIndices[1]])
            # print('Mutation Indices: ', mutationIndices) # For Debugging Purposes

            np.put(mutatedChild, mutationIndices, [mutatedChild[mutationIndices[1]], mutatedChild[mutationIndices[0]]])
            # print('Mutated Child iteration ', i, ': ', mutatedChild) # For debugging Purpose

            # APPLY PERMUTATION CONTINUITY CHECK BETWEEN CHILD AND MUTATED CHILD
            checkPermutation(child, mutatedChild)

        return mutatedChild

    # DEFINE THE METHOD THAT IMPLEMENTS THE INVERSION ALGORITHM
    def inversion(self, child):
        # COPY CONTENTS OF child TO NEW mutatedChild ARRAY
        mutatedChild = np.zeros(len(child), dtype=np.int8)
        mutatedChild += child

        # GENERATE TWO RANDOM POSITIONS IN THE CHROMOSOME TO GENERATE A CONTIGUOUS SUBSET
        mutationIndices = self.RNG.choice(len(child), 2, replace=False)
        # print('mutation Indices ', mutationIndices) #For debugging purposes

        # ORDER THIS ARRAY OF INDEXES FROM SMALLEST TO LARGEST
        sortedMutationIndices = np.sort(mutationIndices)
        # print('Sorted Mutation Indices ', sortedMutationIndices) # For debugging purposes

        # GENERATE THE CHROMOSOME SUBSET FROM THE CHILD
        childSubset = mutatedChild[sortedMutationIndices[0]:sortedMutationIndices[1]+1] #The slice operator is 1 indexed
        # print('Subset: ', childSubset) #For debugging purposes

        # REVERSE THE ORDER OF THIS SUBSET
        childSubsetReversed = childSubset[::-1]
        # print('Subset Reversed: ', childSubsetReversed) # For debugging purposes

        # REPLACE THIS REVERSED SUBSET WITH THE ORIGINAL SUBSET WITHIN THE CHILD
        mutatedChild[sortedMutationIndices[0]:sortedMutationIndices[1]+1] = childSubsetReversed

        # APPLY PERMUTATION CONTINUITY CHECK BETWEEN CHILD AND MUTATED CHILD
        checkPermutation(child, mutatedChild)

        return mutatedChild

    # DEFINE THE SCRAMBLE MUTATION THAT IS SIMILAR TO THE INVERSION ALGORITHM BUT THE SUBSET IS SCRAMBLED
    def scramble(self, child):
        mutatedChild = np.zeros(len(child), dtype=np.int8)
        mutatedChild += child
        # print(child)

        # GENERATE TWO RANDOM POSITIONS IN THE CHROMOSOME TO GENERATE A CONTIGUOUS SUBSET
        mutationIndices = self.RNG.choice(len(child)+1, 2, replace=False) # chose len(child)+1 to permute entire child
        # print('mutation Indices ', mutationIndices) #For debugging purposes

        # ORDER THIS ARRAY OF INDEXES FROM SMALLEST TO LARGEST
        sortedMutationIndices = np.sort(mutationIndices)
        # print('Sorted Mutation Indices ', sortedMutationIndices) # For debugging purposes

        # GENERATE THE CHROMOSOME SUBSET FROM THE CHILD
        childSubset = mutatedChild[sortedMutationIndices[0]:sortedMutationIndices[1]+1] #The slice operator is 1 indexed
        # print('Subset: ', childSubset) #For debugging purposes

        # PERMUTE THE ELEMENTS OF THE SUBSET
        childSubsetPermuted = self.RNG.permutation(childSubset)
        # print('Subset Permuted: ', childSubsetPermuted) # For debugging purposes

        # REPLACE THIS SCRAMBLED SUBSET WITH THE ORIGINAL SUBSET WITHIN THE CHILD
        mutatedChild[sortedMutationIndices[0]:sortedMutationIndices[1]+1] = childSubsetPermuted

        # APPLY PERMUTATION CONTINUITY CHECK BETWEEN CHILD AND MUTATED CHILD
        checkPermutation(child, mutatedChild)

        return mutatedChild

    # DEFINES THE METHOD THAT IMPLEMENTS THE INSERT MUTATION ALGORITHM
    def insert(self, child):
        mutatedChild = np.zeros(len(child), dtype=np.int8)
        mutatedChild += child

        # GENERATE TWO RANDOM POSITIONS IN THE CHROMOSOME TO GENERATE A CONTIGUOUS SUBSET
        mutationIndices = self.RNG.choice(len(child), 2,
                                          replace=False)  # chose len(child)+1 to permute entire child
        print('mutation Indices ', mutationIndices)  # For debugging purposes

        # ORDER THIS ARRAY OF INDEXES FROM SMALLEST TO LARGEST
        sortedMutationIndices = np.sort(mutationIndices)
        # print('Sorted Mutation Indices ', sortedMutationIndices)  # For debugging purposes

        # DEFINE A RANGE ARRAY THAT WILL PERFORM THE INSERTION
        # THIS SUB-ALGORITHM WAS TAKEN FROM Divakar's STACK OVERFLOW answer
        # https://stackoverflow.com/questions/40332763/inplace-changing-position-of-an-element-in-array-by-shifting-others-forward-nu
        range_array = np.arange(child.size)

        # STORE THE SECOND INDEX IN A TEMPORARY ARRAY
        tmp_index_array = mutatedChild[sortedMutationIndices[1]]

        # SET THE VALUES OF mutatedChild (NOT EQUAL TO [INDEX 1]+1) = VALUES (NOT EQUAL TO INDEX 2)
        mutatedChild[range_array != (sortedMutationIndices[0])] = mutatedChild[range_array != sortedMutationIndices[1]]

        # SET THE VALUE OF mutatedChild at [INDEX 1]+1 TO BE tmp_index_array
        mutatedChild[sortedMutationIndices[0]] = tmp_index_array

        # APPLY PERMUTATION CONTINUITY CHECK BETWEEN CHILD AND MUTATED CHILD
        checkPermutation(child, mutatedChild)

        print('original child ', child, ' mutated child ', mutatedChild)

        return mutatedChild