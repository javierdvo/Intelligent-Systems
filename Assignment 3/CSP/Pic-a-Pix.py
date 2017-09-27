import numpy as np
from aima import csp



class PicPix(csp.CSP):
    def __init__(self):
        variables = list(range(1, 26))
        variablesMat = np.reshape(variables, (5, 5))
        neighbours = {}
        for key in variables:
            listNeighbours = list(np.append(variablesMat[int(int(key - 1) / 5)][0:5:1],
                                                (variablesMat.transpose()[int(int(key - 1) % 5)][0:5:1])))
            listNeighbours.remove(key)
            listNeighbours.remove(key)
            neighbours[key] = set(listNeighbours)
        dic=list()
        for a in list("RGYN"):
            for b in list("54321"):
                for c in list("12345"):
                    dic.append(a+b+c)
        csp.CSP.__init__(self,variables,csp.UniversalDict(list(dic)),neighbours,self.PicPixConstraintOld)

    def display(self, assignment):
        array = np.zeros((5, 5))
        for var in range(25):
            for val in {"R", "G", "Y", "N"}:
                if (var == assignment.get(val)):
                    array[int(var / 5)][int(var % 5)] = var
    def PicPixConstraint(self,A,a,B,b):
        row=int((A-1)/5)
        col=(A-1)%5
        if a[0] == 'R':
            index = 0
        if a[0] == 'G':
            index = 1
        if a[0] == 'Y':
            index = 2
        if a[0] == 'N':
            index = 3
        maxCol = 0
        maxRow = 0
        for vals in self.neighbours:
            if(a==b):
                if( abs(A-B)<5):
                    maxRow+=1
                else:
                    maxCol+=1
        if( maxCol>challengeColoursColumn[col][index] or maxRow>challengeColoursRow[row][index]): #Checks for global total and avoids
            return False
        if (a==b) and (abs(A-B)==1 or abs(A-B)==5):# Checks for adjacency and avoids same colour
            return False
        return True
    #return csp.CSP(variables, list("RGYN"), neighbours, PicPixConstraint)


    def PicPixConstraintOld(self,A, a, B, b):
        row = int((A - 1) / 5)
        col = (A - 1) % 5
        if a[0] == 'R':
            index = 0
        if a[0] == 'G':
            index = 1
        if a[0] == 'Y':
            index = 2
        if a[0] == 'N':
            index = 3
        # print("Var A " + str(A) + " val " + str(a) + " Neighbour B " + str(B) + " val " + str(b))
        # print("Row "+str(row)+" Col "+str(col))

        if (a[0] != "N"):
            if (b[0] != "N"):  # these two ensure a and b do not have the same "order", thus ensuring numbers don't repeat.
                if (a[2] == b[2]):
                    return False
            if (int(a[2]) > challengeColoursColumn[col][index] or int(a[2]) > challengeColoursRow[row][
                index]):  # this ensures the total number is never passed twice
                return False
            if (int(a[1]) > min(maxLengthColumn[col][index],
                                maxLengthRow[row][index])):  # this ensures no block oversteps the maximum block length
                return False
            if (a[0] == b[0] and b != "N"):
                if b[1] == '1' and a[2] == b[2] and (abs(A - B) == 1 or abs(
                            A - B) == 5):  # Ensures that there is no block on proximity and that they are assigned the same "Block"
                    return False
                elif (int(a[1]) == int(b[1]) - 1) and a[1:2] != b[
                                                                1:2]:  # Checks for block continuity and avoids multiple duos.
                    return True
            if (int(a[2]) <= challengeColoursColumn[col][index] and int(a[2]) <= challengeColoursRow[row][
                index]):  # Ensures that values can be put if they are still some spots left
                return True
        if (a[0] == "N"):
            if (a == b):
                return False
            if (int(a[1]) <= challengeColoursColumn[col][3] and int(a[1]) <= challengeColoursRow[row][
                3]):  # Ensures only the maximum available blank spaces
                return False



challengeColoursRow = [[2, 0, 0, 3], [1, 1, 1, 2], [4, 0, 0, 1], [3, 1, 0, 1], [2, 0, 0, 3]]
challengeColoursColumn = [[2, 0, 0, 3], [1, 1, 1, 2], [4, 0, 0, 1], [3, 1, 0, 1], [2, 0, 0, 3]]
maxLengthRow=[[2,0,0],[1,1,1],[2,0,0],[1,1,0],[2,0,0]]
maxLengthColumn=[[2,0,0],[1,1,1],[2,0,0],[1,1,0],[2,0,0]]
game = PicPix()




print(csp.backtracking_search(game))
print(game.nassigns)

