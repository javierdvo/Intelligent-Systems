import numpy as np
dataX=np.array([2,4,6,8,10,12,14,16,18,20])
dataY=np.array([26,-1,4,20,0,-2,19,1,-4,19])

def function(x,phi): #Function to be adjusted
    return phi[0]/np.power(x,2) + phi[1]*np.power(np.e,phi[2]/x)+phi[3]*np.sin(x)

def goalFunction(fi): #Goal test to minimize
    return np.sum(abs(dataY-fi))

def makeChromosome():
    return bitArray
