import numpy as np

dataX = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
dataY = np.array([26, -1, 4, 20, 0, -2, 19, 1, -4, 19])


def function(x, phi):  # Function to be adjusted
    return phi[0] / np.power(x, 2) + phi[1] * np.power(np.e, phi[2] / x) + phi[3] * np.sin(x)


def temperatureExp(t0, k):  # Temperature Equation #1
    return t0 * np.power(0.95, k)


def temperatureProportional(t0, k):  # Temperature Equation #2
    return t0 / k


def temperatureBoltz(t0, k):  # Temperature Equation #3
    with np.errstate(divide='ignore'):
        return t0 / np.log(k)


def acceptance(delta, t):  # Acceptance function
    with np.errstate(over='ignore'):
        return 1 / (1 + np.power(np.e, delta / t))


def goalFunction(fi):  # Goal test to minimize
    return np.sum(abs(dataY - fi))


def updatePhi1(phi):  # Phi update function 1 where all have a chance to be updated
    theta = np.copy(phi)
    if np.random.rand(1) > .25:  # per variable each has a 25% chance to be updated to a new value from 0 to 15
        theta[0] = np.floor(np.random.rand(1) * 15)
    if np.random.rand(1) > .25:
        theta[1] = np.floor(np.random.rand(1) * 15)
    if np.random.rand(1) > .25:
        theta[2] = np.floor(np.random.rand(1) * 15)
    if np.random.rand(1) > .25:
        theta[3] = np.floor(np.random.rand(1) * 15)
    return theta


def updatePhi2(phi):  # Phi update function 1 where 1 value is always updated
    theta = np.copy(phi)
    a = np.random.rand(1)  # One variable gets updated to a new value from 0 to 15
    if a > .75:
        theta[0] = np.floor(np.random.rand(1) * 15)
    elif a > 0.5:
        theta[1] = np.floor(np.random.rand(1) * 15)
    elif a > 0.25:
        theta[2] = np.floor(np.random.rand(1) * 15)
    else:
        theta[3] = np.floor(np.random.rand(1) * 15)
    return theta


txt = ["Boltzmann", "Exponential", "Proportional", "First", "Second"]  # print text
avg = np.zeros((6, 5))  # avg values
bestSolution=np.zeros(4)
bestError=10000
for j in range(0, 10, 1):  # does 10 runs of each function pair to get an average
    phi0 = np.floor(np.random.rand(4) * 15)  # inits each of the 10 problems
    for k in range(1, 6, 1):  # Runs the iteration for 5 different temperatures
        for i in range(0, 6, 1):  # Runs the iteration for each algorithm
            # Init
            if i == 0 or i == 3:
                T0 = 1 / k  # Must be 1 or else it takes too many iterations for the boltzmann temperature
            else:
                T0 = int(
                    500 / k)  # Decent temperature to get a good amount of iterations on both the exponential and proportional one
            phi = np.copy(phi0)
            t = T0
            limit = 0.1  # Limit to define when the iterations will stop.
            time = 0
            result = goalFunction(function(dataX, phi))  # Starting goal evaluation function
            result2 = 0
            theta = np.copy(phi)
            print("Solving problem 1 using the " + txt[i % 3] + " temperature function and the " + txt[
                int(i / 3) + 3] + " Phi update function\n")
            print("Starting Phi: " + str(phi))
            print("Starting Min Value: " + str(result))
            print("Starting Temp: " + str(t))

            while t > limit:  # will run the annealing algorithm until temp reaches limit
                if i / 3 < 1:  # chooses which update function to use
                    theta = updatePhi1(phi)
                else:
                    theta = updatePhi2(phi)
                result2 = goalFunction(
                    function(dataX, theta))  # gets the value of the goal function using the new phi alternative
                if result2 < result:  # If value is lower, then update to this new phi
                    phi = theta
                    result = result2
                else:  # if not, then check if the probability check is passed, then update it if that is the case.
                    ran = np.random.rand(1)
                    prob = acceptance(abs(result2 - result), t)
                    if ran < prob:
                        phi = theta
                        result = result2
                time += 1
                if i % 3 == 0:  # Chooses which temperature function to use
                    t = temperatureBoltz(T0, time)
                elif i % 3 == 1:
                    t = temperatureExp(T0, time)
                elif i % 3 == 2:
                    t = temperatureProportional(T0, time)
            if result<bestError:
                bestError=result
                bestSolution=phi
            print("Final Phi: " + str(phi))
            print("Final Min Value: " + str(result))
            print("Final Temp: " + str(t))
            print("Iterations: " + str(time) + "\n")
            avg[i][k - 1] += result  # saves value for average count.
for b in range(0, 5):
    print("\nAverage Min Value for Boltzmann temperature, initial temperature: " + str(
        1 / (b + 1)) + " and first Phi update: " + str(avg[0][b] / 10))
    print("Average Min Value for Exponential temperature, initial temperature: " + str(
        500 / (b + 1)) + "  and first Phi update: " + str(avg[1][b] / 10))
    print("Average Min Value for Proportional temperature, initial temperature: " + str(
        500 / (b + 1)) + "  and first Phi update: " + str(avg[2][b] / 10))
    print("Average Min Value for Boltzmann temperature, initial temperature: " + str(
        1 / (b + 1)) + "  and second Phi update: " + str(avg[3][b] / 10))
    print("Average Min Value for Exponential temperature, initial temperature: " + str(
        500 / (b + 1)) + "  and second Phi update: " + str(avg[4][b] / 10))
    print("Average Min Value for Proportional temperature, initial temperature: " + str(
        500 / (b + 1)) + "  and second Phi update: " + str(avg[5][b] / 10))
print("\nThe best solution found was: \na1="+str(bestSolution[0])+"\na2="+str(bestSolution[1])+"\na3="+str(bestSolution[2])+"\na4="+str(bestSolution[3])+"\nWith an error of: "+str(bestError))
