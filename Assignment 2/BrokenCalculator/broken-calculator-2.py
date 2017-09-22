# -*- coding: utf-8 -*-
"""

@author:
A01202564 Javier de Velasco Oriol
A01746968 German Alamilla Peralta
"""
import os
import time

import numpy #Import numpy para
import psutil

from aima.search import (  # Bases para construcción de problemas
    Problem
)
from aima.search import (  # Algoritmos de búsqueda no informada
    breadth_first_search,
    depth_first_graph_search,
    depth_limited_search, iterative_deepening_search,
    uniform_cost_search
)
from aima.search import (  # Algoritmos de búsqueda informada (heurística)
    greedy_best_first_graph_search, astar_search
)


class ProblemaResolver(Problem):
    def __init__(self, inicial=0, meta=50, level=1,c=0):
        Problem.__init__(self, inicial, meta)
        self.level = level
        self.c=c
        self.acciones = []  # acciones posibles
        # numeros permitidos depende el nivel
        if self.level == 1:
            self.numeros_permitidos = [2, 3]
        elif self.level == 2:
            self.numeros_permitidos = [5, 2]
        elif self.level == 3:
            self.numeros_permitidos = [1, 8,6]
        elif self.level == 4:
            self.numeros_permitidos = [1,2,0]
        elif self.level == 5:
            self.numeros_permitidos = [2,4,9]
        elif self.level == 6:
            self.numeros_permitidos = [2]
        for num_disponible in self.numeros_permitidos: #Delimita las acciones dependiendo del nivel, y genera tantas acciones sean posibles por cada numero. Ex, X2,X3
            if self.level == 1 or self.level==2 or self.level==4 : self.acciones.append('MULTIPLICAR ' + str(num_disponible))
            if self.level == 1 : self.acciones.append('SUMAR ' + str(num_disponible))
            if self.level == 2 or self.level == 3 or self.level == 5:self.acciones.append('RESTAR ' + str(num_disponible))
            if self.level == 3: self.acciones.append('DIVIDIR ' + str(num_disponible))
            if self.level == 4 or self.level == 6: self.acciones.append("RAIZ")
            if self.level == 5 or self.level == 6: self.acciones.append("ALCUADRADO")
            self.acciones.append('INICIAR ' + str(num_disponible))


    def actions(self, estado):  # que acciones estan permitidas de acuerdo al estado
        arreglo_acciones = []
        for accion in self.acciones:
            # Indica para cada accion en cada nivel si se agrega o no, y al igual que arriba las crea por numero
            for num_disponible in self.numeros_permitidos:
                if accion == 'MULTIPLICAR ' + str(num_disponible) and estado != 0:  # Que el estado sea diferente de 0
                    arreglo_acciones.append('MULTIPLICAR ' + str(num_disponible))
                elif accion == 'SUMAR ' + str(num_disponible) :
                    arreglo_acciones.append('SUMAR ' + str(num_disponible))
                elif accion == 'RESTAR ' + str(num_disponible) :
                    arreglo_acciones.append('RESTAR ' + str(num_disponible))
                elif accion == 'INICIAR ' + str(num_disponible) and estado == 0: #Solo puede inicializar en el primer estado
                    arreglo_acciones.append('INICIAR ' + str(num_disponible))
                elif accion == 'DIVIDIR ' + str(num_disponible) and estado > 0 and num_disponible!=0: #No divide no divide entre cero
                    arreglo_acciones.append('DIVIDIR ' + str(num_disponible))
            if accion == 'RAIZ ' and ():
                arreglo_acciones.append('RAIZ ')
            elif accion == 'ALCUADRADO ' and (self.level == 5 or self.level == 6):
                arreglo_acciones.append('ALCUADRADO ')
        return arreglo_acciones

    # Generacion del siguiente estado
    def result(self, estado, accion):
        for num_disponible in self.numeros_permitidos:
            if accion == 'MULTIPLICAR ' + str(num_disponible):
                nuevo_estado = estado * num_disponible
                return nuevo_estado
            elif accion == 'SUMAR ' + str(num_disponible):
                nuevo_estado = estado + num_disponible
                return nuevo_estado
            elif accion == 'RESTAR ' + str(num_disponible):
                nuevo_estado = estado - num_disponible
                return nuevo_estado
            elif accion == 'DIVIDIR ' + str(num_disponible):
                nuevo_estado = estado / num_disponible
                return nuevo_estado
            elif accion == 'INICIAR ' + str(num_disponible):
                nuevo_estado = estado+ num_disponible
                return nuevo_estado
        if accion == 'ALCUADRADO ':
            nuevo_estado = estado * estado
            return nuevo_estado
        elif accion == 'RAIZ ':
            nuevo_estado = numpy.sqrt(estado)
            return nuevo_estado

    def f1(self, node): #Heuristica 1 para GBFS en el Nivel 1
        diferencia = self.goal - node.state
        if diferencia == 0: #Si no hay diferencia llego al estado correcto
            return 0
        if diferencia < 2: #Si es menor a 2 la diferencia significa que es imposible llegar y hay overflow. asi que se penaliza
            return 999
        multiply_max = 0
        valor = node.state #Obtiene el valor del nodo
        if valor==0: #Si está en el estado inicial se toma el máx dividido entre 3+1 para ser admisible e inicializar
            return self.goal/max(self.numeros_permitidos)+1
        while valor * max(self.numeros_permitidos) <= self.goal - 2: # Va aumentando la cantidad de veces que le falta multiplicarse antes de pasarse, el menos dos se encuentra para evitar caer en un estado imposible
            multiply_max += 1
            valor = valor * max(self.numeros_permitidos) #Se actualiza el valor
        multiply_min = 0
        valor = node.state
        while valor * min(self.numeros_permitidos) <= self.goal - 2: #Se genera lo mismo pero para el caso del menor número posible de multiplicar (Para los casos que se puede multiplicar por el menor pero no por el mayor
            multiply_min += 1
            valor = valor * min(self.numeros_permitidos)
        if multiply_min<multiply_max: #Se obtiene el menor de los dos valores
            return multiply_min
        else:
            return multiply_max

    def f2(self, node): #Heurística 2 para GBFS en el Nivel 1
        diferencia =  self.goal- node.state
        if diferencia == 0:#Objetivo
            return 0
        if diferencia < 2:# Overshoot
            return 999
        divisions = 0
        while diferencia >= max(self.numeros_permitidos):#Checa la cantidad de veces que falta dividir la diferencia existente entre tres.
            divisions += 1
            diferencia =diferencia / max(self.numeros_permitidos)#Actualiza el valor
        return divisions



    def h1(self, node): #Heuristica 1 para Nivel 1 en A*
        diferencia=self.goal-node.state
        if diferencia==0:
            return self.c+ 0
        if diferencia<2:
            return self.c+999
        multiply_max = 0
        valor = node.state
        if valor == 0:
            return self.goal / max(self.numeros_permitidos) + 1
        while valor * max(self.numeros_permitidos) <= self.goal - 2:
            multiply_max += 1
            valor = valor * max(self.numeros_permitidos)
        multiply_min = 0
        valor = node.state
        while valor * min(self.numeros_permitidos) <= self.goal - 2:
            multiply_min += 1
            valor = valor * min(self.numeros_permitidos)
        if multiply_min < multiply_max:
            return self.c+multiply_min
        else:
            return self.c + multiply_max

    def h2(self, node):#Heuristica 2 para Nivel 1 en A*
        diferencia=self.goal-node.state
        if diferencia==0:
            return self.c+ 0
        if diferencia<2:
            return self.c+999
        divisions=0
        while diferencia>=max(self.numeros_permitidos):
            divisions+=1
            diferencia=diferencia/max(self.numeros_permitidos)
        return self.c+divisions

    def path_cost(self, c, state1, action, state2):
        return c+1

def despliega_solucion(nodo_meta): #Imprime la informacion de la solución
    acciones = nodo_meta.solution()
    nodos = nodo_meta.path()
    print("Secuencia de Nodos :"+str(nodos))
    print('Desglose de Solución:')
    print('Estado:', nodos[0].state)
    for na in range(len(acciones)):
        print('Acción: '+ str(acciones[na]))
        print('Estado:', nodos[na + 1].state)
    print("Costo "+str(len(nodos)-1)) #\hack


# -------------------------------------------------------------------


LevelGoals=[6,15,50,9999,1,-10,10.5] #Objetivos de la búsqueda, los últimos tres fallan ya que son imposibles


Method=["Breadth First Search","Depth First Graph Search", "Depth Limited Search to 6",
        "Iterative Deepening Search", "Greedy Best First Graph Search Heuristic 1",
        " A Star Search Heuristic 1", "Greedy Best First Graph Search Heuristic 2",
        " A Star Search Heuristic 2","Uniform Cost Search"]

for k in range(9):#Recorre los 9 distintos métodos
        for i in range(4): #En los primeros 4
            process = psutil.Process(os.getpid())
            print("\nSolución del Nivel 1 mediante búsqueda "+ Method[k])
            print("Meta: " + str(LevelGoals[i])+"\n")
            t0 = time.clock() #Pre Timing
            prob1 = ProblemaResolver(0, LevelGoals[i],1)
            if k==0:
                meta1 = breadth_first_search(prob1)
            elif k==1 and (i!=0 and i!=2): #6 y 50 en DFS hacen overshoot y como es DFS nunca deja de multiplicar
                meta1 = depth_first_graph_search(prob1)
            elif k == 2:
                meta1 = depth_limited_search(prob1,13) #13 de límite si llega con el 9999
            elif k == 3:
                meta1 = iterative_deepening_search(prob1)
            elif k == 4:
                meta1 = greedy_best_first_graph_search(prob1,prob1.f1)
            elif k == 5:
                meta1 = astar_search(prob1,prob1.h1)
            elif k == 6:
                meta1 = greedy_best_first_graph_search(prob1,prob1.f2)
            elif k == 7:
                meta1 = astar_search(prob1,prob1.h2)
            elif k==8:
                meta1=uniform_cost_search(prob1)
            if meta1:
                t1 = time.clock()#Timing final
                despliega_solucion(meta1)
                print( "Tiempo:" + str(t1-t0))
            else:
                print("Falla: no se encontró una solución")

