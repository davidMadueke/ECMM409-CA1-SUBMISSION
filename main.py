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

    # David = Algorithm.EA('assets/burma14.xml', 5, 5, RNG_Seed=26)
    # test = David.population_init()
    # print('Initial Population ', test)
    #
    # David.tournamentSelection(test)
    #
    # testParent1 = test[1][0]
    # testParent2 = test[1][4]
    #
    # # print('Parent1: ', testParent1, " , Parent2: ", testParent2)
    #
    # Madueke = Algorithm.CrossoverOperator(testParent1, testParent2,'cycleCrossover', RNG_Seed=42)
    # child1, child2 = Madueke.processCrossover()
    #
    #
    # # print('Child1: ', child1, " , Child2: ", child2)
    #
    # Chukwuemeka = Algorithm.MutationOperator(child2,'insert',RNG_Seed=49,multiSwapAmount=20)
    # mutatedChild = Chukwuemeka.processMutation()
    #
    # # print('Child2 before mutation: ', child2)
    # # print('Child2 after mutation: ', mutatedChild)
    #
    # Favour = Algorithm.Replacement(test, David.adjacency_matrix(), child1, mutatedChild,'FIFO',RNG_Seed=54,replacement_FIFOindex=4)
    # FIFOindex,newPopulation = Favour.applyReplacement()
    #
    # print('new Population ', newPopulation)
    # print('FIFO index ', FIFOindex)

############
    David = Algorithm.EA('assets/burma14.xml',
                         100,
                         50,
                         RNG_Seed=34,
                         crossoverType='orderedCrossover',
                         mutationType='inversion',
                         replacementType='FIFO',
                         terminationCriterion=100)
    David.setMultiSwapAmount(20)
    selectedTour, selectedTourFitness = David.applyEA()
    print('Final Optimal Tour ', selectedTour)
    print('Its associated Fitness: ', selectedTourFitness)