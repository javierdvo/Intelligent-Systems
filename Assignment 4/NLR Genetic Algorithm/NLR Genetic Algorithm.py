import numpy as np
import bitarray as ba
import scipy as sp
dataX = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
dataY = np.array([26, -1, 4, 20, 0, -2, 19, 1, -4, 19])


def function(x, phi):  # Function to be adjusted
    return phi[0] / np.power(x, 2) + phi[1] * np.power(np.e, phi[2] / x) + phi[3] * np.sin(x)


def goalFunction(fi):  # Goal test to minimize
    return np.sum(abs(dataY - fi))


def makeChromosome(phi):  # Takes 4 numbers and creates the bit array chromosome representation
    chromosome = ba.bitarray(16)  # Initializes to a 16 length bit array
    chromosome[12:16] = ba.bitarray(format(phi[3], '04b'))  # Formats each number as a 4-bit array and assigns it
    chromosome[8:12] = ba.bitarray(format(phi[2], '04b'))
    chromosome[4:8] = ba.bitarray(format(phi[1], '04b'))
    chromosome[0:4] = ba.bitarray(format(phi[0], '04b'))
    return chromosome


def makeInts(chromosome):  # Takes a chromosome bit array and generates the 4 integers from it
    a = int(chromosome[0:4].to01(),2)  # Converts the bit array segment for each number into a string of 1s and 0s and then using the base 2 converts to integers
    b = int(chromosome[4:8].to01(), 2)
    c = int(chromosome[8:12].to01(), 2)
    d = int(chromosome[12:16].to01(), 2)
    return np.array([a, b, c, d],int)


def crossOver(parent1, parent2, crossover):  # Crossover mechanism from 2 parents generates two kids
    child1 = ba.bitarray(16)  # Inits to 16 length and assigns each part.
    child1[0:crossover * 4] = parent1[
                              0:crossover * 4]  # Times 4 to select the number where it will make the crossover (So a1,a2,a3,a4)
    child1[crossover * 4:16] = parent2[crossover * 4:16]
    child2 = ba.bitarray(16)
    child2[0:crossover * 4] = parent2[0:crossover * 4]
    child2[crossover * 4:16] = parent1[crossover * 4:16]
    return child1, child2


def mutateOne(human):  # Mutates one random bit
    xmen = ba.bitarray.copy(human)
    index = int(np.ceil(np.random.rand(1) * 15))  # sets the index which will be flipped
    xmen[index] != xmen[index]  # flips it
    return xmen


def mutateMultiple(xmen):  # Mutates the chromosome. Can flip from 1 to 4 different bits
    dimensions = int(np.ceil(np.random.rand(1) * 4))  # randomly selects the amount of bits to flip
    mutations = np.asarray(np.ceil(np.random.rand(dimensions) * 15),
                           int)  # makes an array of the indices which will be flipped
    xmen = np.array(xmen)
    xmen[mutations] = np.invert(xmen[mutations])
    return ba.bitarray(list(xmen))

#print(sp.optimize.minimize(goalFunction(function(dataX)),[3,5,2,13],method='Newton-CG'))
# Init
limit = [5,7,10] #Especially 5 tends to not find a solution in 10000 iterations.
iterlimit = 10000 #So that the 300 iterations can actually run in plausible time. An ideal solution would be to have just one run on 100000 for example
fitness = np.zeros((16))
normFitness = np.zeros((16))
sexrand = [0.10, 0.25, 0.5, 0.75, 1] #Reproduction chance
xmenrand = [0.10, 0.20, 0.30, 0.40, 0.50] #Mutation chance
bestSolution=np.zeros(4)
bestError=10000
avg=np.zeros(30)
avgiter=np.zeros(30)


for k in range(0,30):#Runs the different algorithms, and the different parameters
    for l in range(0,10):#Runs 10 times each algorithm for an average
        chromosomes = list()
        for i in range(0, 16):
            phi = np.asarray(np.ceil(np.random.rand(4) * 15), int)
            chromosomes.append(makeChromosome(phi))
            fitness[i] = goalFunction(function(dataX, phi))
        j = 0
        if k%10>4:
            print("\nSolving the equation with a genetic algorithm using the multiple mutations function, with parameters:")
        else :
            print("\nSolving the equation with a genetic algorithm using the single mutation function, with parameters:")
        print("Reproduction Probability: " + str(sexrand[k % 5]))
        print("Mutation Probability: " + str(xmenrand[k % 5]))
        print("Minimum Limit: " + str(limit[int(k / 10)]))
        print("Starting Chromosomes:")
        for z in chromosomes :
            print(str(z.to01()))


        while j<iterlimit and not any(limit[int(k/10)] > fitness):
            invertedFitness=max(fitness)-fitness
            normFitness = invertedFitness / sum(invertedFitness)
            parentPairs = list()
            newGen = list()
            for i in range(0, 16):
                index = np.random.choice(16, p=normFitness)
                parentPairs.append(chromosomes[index])
            for i in range(0, 8):
                if np.random.rand(1) < sexrand[k%5]:
                    crosspoint = int(np.ceil(np.random.rand(1) * 3))
                    child1, child2 = crossOver(parentPairs[i * 2], parentPairs[i * 2 + 1], crosspoint)
                    if np.random.rand(1) < xmenrand[k%5]:
                        if k/10<5:
                            child1 = mutateMultiple(child1)
                        else:
                            child1 = mutateOne(child1)
                    if np.random.rand(1) < xmenrand[k%5]:
                        if k/10 < 5:
                            child2 = mutateMultiple(child2)
                        else:
                            child2 = mutateOne(child2)
                    newGen.append(child1)
                    newGen.append(child2)
                else:
                    newGen.append(parentPairs[i * 2])
                    newGen.append(parentPairs[i * 2 + 1])
            for i in newGen:
                phi=makeInts(i)
                fitness[i] = goalFunction(function(dataX, phi))
            j += 1
        index=fitness.argmin()
        solution=makeInts(newGen[index])
        error=fitness[index]
        if error<bestError:
            bestError=error
            bestSolution=solution
        print("\nBest Chromosome:" +str(newGen[index].to01()))
        print("Final Phi: "+str(solution))
        print("Final Min. Error Value: "+str(fitness[index]))
        print("Iterations: "+str(j))
        avg[k]+=error
        avgiter[k]+= j
for k in range (0,3):
    for j in range(0,5):
        print("\nAverage Min Value using the single mutation function and the following parameters:")
        print("Reproduction Probability: " + str(sexrand[j]))
        print("Mutation Probability: " + str(xmenrand[j]))
        print("Minimum Limit: " + str(limit[k]))
        print("Average Min Value: " + str(avg[k*10+j]/10))
        print("Average Iterations: " + str(avgiter[k * 10 + j] / 10))
    for j in range(0, 5):
        print("\nAverage Min Value using the multiple mutations function and the following parameters:")
        print("Reproduction Probability: " + str(sexrand[j]))
        print("Mutation Probability: " + str(xmenrand[j]))
        print("Minimum Limit: " + str(limit[k]))
        print("Average Min Value: " + str(avg[k*10+j+5]/10))
        print("Average Iterations: " + str(avgiter[k * 10 + j] / 10))

print("\nBest Chromosome through all iterations:" + str(makeChromosome(bestSolution).to01()))
print("Best Phi: " + str(bestSolution))
print("Best Min. Error Value: " + str(bestError))
