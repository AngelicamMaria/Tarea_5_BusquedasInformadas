#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
busquedas.py
------------

Clases y algoritmos necesarios para desarrollar agentes de búsquedas en entornos determinísticos
conocidos discretos completamente observables

"""

__author__ = 'juliowaissman'

from collections import deque
import heapq


class ProblemaBusqueda(object):

    """
    Clase genérica de un problema de búsqueda.

    Todo problema de búsqueda debe de tener:
        a) Un estado inicial
        b) Una función que diga si un estado es una meta o no
        c) Un método que obtenga las acciones legales en cada estado
        d) Un método que calcule cual es es siguiente estado
        e) Una función de costo local

    """

    def __init__(self, s0, meta):
        """
        Inicializa el problema de búsqueda

        @param s0: Una tupla con un estado válido del problema (estado inicial).
        @param meta: Una función meta(s) --> bool, donde meta(s) devuelve True solo
        si el estado s es un estado objetivo.

        """
        def es_meta(estado):
            self.num_nodos += 1
            return meta(estado)
        self.es_meta = es_meta

        self.s0 = s0
        self.num_nodos = 0  # Solo para efectos medición

    def acciones_legales(self, estado):
        """
        Lista de acciones legales en un estado dado.

        @param estado: Una tupla con un estado válido.

        @return: Una lista de acciones legales.

        """
        raise NotImplementedError("No implementado todavía.")

    def sucesor(self, estado, accion):
        """
        Estado sucesor

        @param estado: Una tupla con un estado válido.
        @param accion: Una acción legal en el estado.

        @return: Una tupla con el estado sucesor de estado cuando de aplica la acción accion.

        """
        raise NotImplementedError("No implementado todavía.")

    def costo_local(self, estado, accion):
        """
        Calcula el costo de realizar una acción en un estado.

        @param estado: Una tupla con un estado válido.
        @param accion: Una acción legal en estado.

        @return: Un número positivo con el costo de realizar la acción en el estado.
        """
        return 1


class Nodo(object):

    """
    Clase para implementar un árbol como estructura de datos.

    """

    def __init__(self, estado, accion=None, padre=None, costo_local=0):
        """
        Inicializa un nodo como una estructura

        """
        self.estado = estado
        self.accion = accion
        self.padre = padre
        self.costo = 0 if not padre else padre.costo + costo_local
        self.profundidad = 0 if not padre else padre.profundidad + 1

    def expande(self, pb):
        """
        Expande un nodo en todos sus posibles nodos hijos de acuero al problema pb

        @param pb: Un objeto de una clase heredada de ProblemaBusqueda

        @return: Una lista de posibles nodos sucesores

        """
        return [Nodo(pb.sucesor(self.estado, a), a, self, pb.costo_local(self.estado, a))
                for a in pb.acciones_legales(self.estado)]

    def lista_acciones(self):
        """
        Lista de acciones desde la raiz a este nodo.

        @return: Una lista desde la primer acción hasta la última

        """
        return [] if not self.padre else self.padre.lista_acciones() + [self.accion]

    def lista_estados(self):
        """
        Lista de estados desde la raiz a este nodo.

        @return: Una lista desde el estado del nodo raiz hasta este nodo

        """
        return [self.estado] if not self.padre else self.padre.lista_estados() + [self.estado]

    def __str__(self):
        acciones = self.lista_acciones()
        estados = self.lista_estados()
        return ("Costo: " + str(self.costo) +
                "\nProfundidad: " + str(self.profundidad) +
                "\nTrayectoria:\n" +
                "".join(["en %s hace %s\n" % (str(e), str(a)) for (e, a) in zip(estados[:-1], acciones)]) +
                "para terminar en " + str(estados[-1]))


def busqueda_ancho(problema):
    """
    Búsqueda a lo ancho para un problema de búsquedas dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    if problema.es_meta(problema.s0):
        return Nodo(problema.s0)

    frontera = deque([Nodo(problema.s0)])
    visitados = {problema.s0}

    while frontera:
        nodo = frontera.popleft()
        for hijo in nodo.expande(problema):
            if hijo.estado in visitados:
                continue
            if problema.es_meta(hijo.estado):
                hijo.nodos_visitados = problema.num_nodos
                return hijo
            frontera.append(hijo)
            visitados.add(hijo.estado)
    return None


def busqueda_profundo(problema, max_profundidad=None):
    """
    Búsqueda a lo profundo para un problema de búsquedas dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param max_profundidad: Máxima profundidad de búsqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    frontera = deque([Nodo(problema.s0)])
    visitados = {problema.s0: 0}

    while frontera:
        nodo = frontera.pop()
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        if max_profundidad is not None and max_profundidad == nodo.profundidad:
            continue
        for hijo in nodo.expande(problema):
            # or visitados[hijo.estado] > hijo.profundidad:
            if hijo.estado not in visitados:
                frontera.append(hijo)
                visitados[hijo.estado] = hijo.profundidad
    return None


def busqueda_profundidad_iterativa(problema, max_profundidad=10000):
    """
    Búsqueda por profundidad iterativa dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param max_profundidad: Máxima profundidad de búsqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    for profundidad in xrange(1, max_profundidad):
        resultado = busqueda_profundo(problema, profundidad)
        if resultado is not None:
            return resultado
    return None


def busqueda_costo_uniforme(problema):
    """
    Búsqueda por costo uniforme

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    frontera = []
    heapq.heappush(frontera, (0, Nodo(problema.s0)))
    visitados = {problema.s0: 0}

    while frontera:
        (_, nodo) = heapq.heappop(frontera)
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        for hijo in nodo.expande(problema):
            if hijo.estado not in visitados or visitados[hijo.estado] > hijo.costo:
                heapq.heappush(frontera, (hijo.costo, hijo))
                visitados[hijo.estado] = hijo.costo
    return None

#-------------------------------------------------------------------------------------------------
#
# Problema 1 (25 puntos): Desarrolla el método de búsqueda de A* siguiendo las especificaciones 
# de la función pruebalo con el 8 puzzle (ocho_puzzle.py) antes de hacerlo en el Lights_out que es 
# mucho más dificl (en el archivo se incluyen las heurísticas del 8 puzzle y el resultado esperado)
#
#-------------------------------------------------------------------------------------------------

def busqueda_A_estrella(problema, heuristica):
    """
    #Búsqueda A*

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param heuristica: Una funcion de heuristica, esto es, una función heuristica(nodo), la cual devuelva
                       un número mayor o igual a cero con el costo esperado desde nodo hasta un nodo 
                       objetivo.

    @return Un objeto tipo Nodo con la estructura completa
    """
    frontera = []
    nodo = Nodo(problema.s0)
    heapq.heappush(frontera,(0 +heuristica(nodo)))
    heapq.heappush(frontera, (0 + heuristica(nodo), nodo))
    visitados = {problema.s0: 0}
    prueba=0
    j = 0 
    t = 0 
    while frontera and prueba<10000:
        heapq.heappop(frontera)
        prueba=prueba+1
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            bonito(nodo.estado)
            return nodo, problema.num_nodos, nodo.costo
        for hijo in nodo.expande(problema):
            #print "Estado : ",hijo.estado
            if(prueba==10000 and j ==0):
                print "estado del hijo10 mil"
                j = j +10001
                bonito(hijo.estado)
            if hijo.estado not in visitados or visitados[hijo.estado] > hijo.costo:
                heapq.heappush(frontera, (hijo.costo + heuristica(hijo), hijo))   
                visitados[hijo.estado] = hijo.costo
    return nodo, problema.num_nodos, nodo.costo
def sucesor(estado, accion):
        estado3 = list(estado)
        if estado3[accion] == 0:
            estado3[accion] = 1
        else:
            estado3[accion]=0

        #Numero de arriba y abajo
        if (accion-5)> -1:
            #print 'Segundo if'
            if estado3[accion-5]== 0:
                estado3[accion-5]=1
            else:
                estado3[accion-5]=0
        if (accion+5)< 25:
            #print 'Tercer if'
            if estado3[accion+5]== 0:
                estado3[accion+5]=1
            else:
                estado3[accion+5]=0
        #Derecha y izquerda
        if accion !=4 and accion !=9 and accion !=14 and  accion !=19 and accion !=24:
            #print 'Cuarto if'
            if estado3[accion+1]== 0:
                estado3[accion+1]=1
            else:
                estado3[accion+1]=0
            
        if accion!=0 and  accion !=5 and accion !=10 and accion !=15 and accion !=20:
            #print 'Quinto if'
            if estado3[accion-1]== 0:
                estado3[accion-1]=1
            else:
                estado3[accion-1]=0
        
        return tuple(estado3)   
def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        cadena = "---------------------\n"
        for i in range(5):
            for j in range(5):
                if estado[5 * i + j]:
                    cadena += "| X "
                else:
                    cadena += "|   "
            cadena += "|\n---------------------\n"
        print cadena
        #return cadena