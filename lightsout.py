#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'nombre del estudiante'


from busquedas import *
import copy

class Lights_out(ProblemaBusqueda):
#----------------------------------------------------------------------------
# Problema 2 (25 puntos): Completa la clase para el problema de lights out
#
#----------------------------------------------------------------------------
    """
    Problema del jueguito "Ligths out".

    La idea del juego es el apagar o prender todas las luces.
    Al seleccionar una casilla, la casilla y sus casillas adjacentes cambian
    (si estan prendidas se apagan y viceversa). El juego consiste en una matriz
    de 5 X 5, cuyo estado puede ser apagado 0 o prendido 1. Por ejemplo el estado

       (0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0)

    corresponde a:

    ---------------------
    |   |   | X |   |   |
    ---------------------
    | X | X |   |   | X |
    ---------------------
    |   |   | X | X |   |
    ---------------------
    | X |   | X |   | X |
    ---------------------
    |   |   |   |   |   |
    ---------------------
    
    Las acciones posibles son de elegir cambiar una luz y sus casillas adjacentes, por lo que la accion es
    un número entre 0 y 24.

    Para mas información sobre el juego, se puede consultar

    http://en.wikipedia.org/wiki/Lights_Out_(game)

    """
    def __init__(self, pos_inicial):
        # ¡El formato y lo que lleva la inicialización de 
        # la super hay que cambiarlo al problema!
        self. meta=tuple([0 for i in range(25)])
        super(Lights_out, self).__init__(pos_inicial, lambda s0: s0 == self.meta)

        #raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones_legales(self, estado):
        '''
        Debido a que es un cuadro 5 x 5 hay 25 acciones legales.  
        Por lo tanto, se regresa un numero entre 0 y 24.
        '''
     
        return range(25)
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
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
       
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def costo_local(self, estado, accion):
        #Por cada accion que realise. Sea cual sea. El costo es 1
        return 1
        #raise NotImplementedError('Hay que hacerlo de tarea')

    @staticmethod
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
        return cadena

#-------------------------------------------------------------------------------------------------
# Problema 3 (25 puntos): Desarrolla una política admisible. 
#-------------------------------------------------------------------------------------------------



def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN PLATICADA DE PORQUÉ CREES QUE
    LA HEURÍSTICA ES ADMISIBLE

    """
    costo_total=i = j = 0
    for j in range(25): #Las acciones
        nodo.estado=sucesor(nodo.estado,j) #A sucesor se envia el estado actual mas la accion.
        for i in range(25):#Recorrido del tablero
            if nodo.estado[i]==1:
                costo_total = costo_total+1
        i = 0
    return costo_total
    ''' 
    --------------------------
    |1/25|1/25|1/25|1/25|1/25|
    --------------------------
    |1/25|1/25|1/25|1/25|1/25|
    --------------------------
    |1/25|1/25|1/25|1/25|1/25|
    --------------------------
    |1/25|1/25|1/25|1/25|1/25|
    --------------------------
    |1/25|1/25|1/25|1/25|1/25|
    --------------------------
    La cantidad de luces encendidas en el tablero, seria el costo total del costo.
    Debido a que son 25 cuadros en el Tableo, enconces cada uno de los cuadros representa una 1/25 parte del total
    Mientras el costo_total sea mas cercano a 1: Tiene muchos focos encendidos, (mas de la mitad).
    Mientras el costo_total sea mas cercano a 0: Tiene muchos focos apagados, (menos de la mitad).
    Si el costo total es 1 (por accion): Es que todo el tablero esta encendido.
    Si el costo_total es 0(por accion): Es decir que todo el tablero esta apagado.

    El costo total estara entre 0 y 1, y esto es por solo una accion.
    '''

    return costo_total

#-------------------------------------------------------------------------------------------------
# Problema 4 (25 puntos): Desarrolla otra política admisible. 
# Analiza y di porque piensas que es (o no es) dominante una respecto otra política
#-------------------------------------------------------------------------------------------------
def h_2(nodo):
    """
    Siguendo con lo de tomar en cuentra los 25 cuadros.
    Si se realisa una ccion sobre un cuadro elejido,  se toma encuenta los cuadros que se veran afectados. 
    Los afectados:
        Si se apagan: no se toma encuenta.
        Si se enciende: Se toma encuenta. 
    Ejemplo:
    Si un cuadro central(#8) esta encendido y se le quiere apagar (o encender), se revisa los cuadros: 7, 9, 3, 13
    Si con apagar el foco #8:
        Si se apagan los cuadros afectados, la huristica no cuenta nada. 
        Si se encienden los cuados afectados, la huristica los tomara encuenta. 

    Asi que la huristica cuenta los cuadros que se veran afectados con la accion.
    Esta heuristica tiene como objetivo decir la accion mas efectiva para que se apagen mas cuadros.
    Con cada cuadro prendido que este revisado se suma 2.5, incluyendo el cuadro, pero este suma 1.
    """
    costo_total=0
    i = 0
    for i in range(25): #25 acciones
        nodo.estado=sucesor(nodo.estado,i) #se envia para sacar el sucesor con la primera accion
        if nodo.estado[i]==1:
            costo_total=costo_total+1
        if (i+5)<25: #con esto, quiere decir que tiene un cuadro abajo.
            if nodo.estado[i]==1:
                costo_total=costo_total+ 2.5
        if (i-5)>-1: #con esto se revisa el cuadro de arriba
            if nodo.estado[i]==1:
                costo_total=costo_total+2.5
        if i!=0 and i!=5 and i!=10 and i!=15 and i!=10: #con esto se dice que no es cuadro de las columnas 0 y 4
            if nodo.estado[i-1]==1:
                costo_total = costo_total+2.5
        if i!=4 and i!=9 and i!=14 and i!=19 and i!=24: #con esto se dice que no es cuadro de las columnas 0 y 4
            if nodo.estado[i+1]==1:
                costo_total = costo_total+2.5      

    return costo_total
'''
Cual heuristica es mejor?
Bueno... 

Con h1:
    Se toman encuenta los cuadros del tablero encendidos con cada accion realisada. 
    Regresa la cantidad de cuadros encendidos de todo el tablero por todas las acciones.
Con h2:
    Se toman en cuenta solo los cuadros afectados 
    Regresa la cantidad de cuadros encendido por cada accion ignorando el resto del tablero.

Uno regresa la suma de todo el cuadro. Lo que puede llegar  tener una suma grande. Mientras menos grande 
sea el costo quiere decir que tiene menos luces encendidas.
El otro regresa solamente los cuadros afectados por la accion. Mientras menos grande sea el costo quiere decir
que las acciones encendieron pocas luces. 

Asi que pienso que la heuristica 2, es mejor. Ya que tomar en cuenta las acciones que prenden menos luces, seria veneficioso
Claro, pensando que el cuadro selecionando se enciende o apaga.
'''

def prueba_clase():
    """
    Prueba la clase Lights_out
    
    """
    
    pos_ini = (0, 1, 0, 1, 0,
               0, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a0 =  (1, 0, 0, 1, 0,
               1, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a4 =  [1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1]

    pos_a24 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 0,
               0, 0, 0, 0, 0)

    pos_a15 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 1, 0,
               1, 0, 0, 0, 0)

    pos_a12 = (1, 0, 0, 0, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 0, 1,
               1, 1, 0, 1, 0,
               1, 0, 0, 0, 0)


    entorno = Lights_out(pos_ini)

    assert entorno.acciones_legales(pos_ini) == range(25)
    entorno.sucesor(pos_ini, 0)
    entorno.sucesor(pos_a0, 4)
    entorno.sucesor(pos_a4, 24)
    entorno.sucesor(pos_a24, 15)
    entorno.sucesor(pos_a15, 12)
    costo_total = 0 
    pos_a = (1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1)
    j = i = 0
    for j in range(25): #Las acciones
        pos_a=entorno.sucesor(pos_a,j) #A sucesor se envia el estado actual mas la accion.
        for i in range(25):#Recorrido del tablero
            if pos_a[i]==1:
                costo_total = costo_total+0.04
    
    costo_total=0
    j = i = 0
    pos_a = (1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1)

def prueba_busqueda(pos_inicial, metodo, heuristica=None, max_prof=None):
    """
    Prueba un método de búsqueda para el problema del ligths out.

    @param pos_inicial: Una tupla con una posicion inicial
    @param metodo: Un metodo de búsqueda a probar
    @param heuristica: Una función de heurística, por default None si el método de búsqueda no requiere heuristica
    @param max_prof: Máxima profundidad para los algoritmos de DFS y IDS.

    @return nodo: El nodo solución

    """
    if heuristica:
        return metodo(Lights_out(pos_inicial), heuristica)
    elif max_prof:
        return metodo(Lights_out(pos_inicial), max_prof)
    else:
        return metodo(Lights_out(pos_inicial))


def compara_metodos(pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución de varios métodos de búsqueda

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla de la función
    """
    #n1 = prueba_busqueda(pos_inicial, busqueda_ancho)
    #n2 = prueba_busqueda(pos_inicial, busqueda_profundidad_iterativa)
    #n3 = prueba_busqueda(pos_inicial, busqueda_costo_uniforme)
    
    
    
    print '\n\n' + '-' * 50
    print 'Método'.center(10) + 'Costo de la solucion'.center(20) + 'Nodos explorados'.center(20)
    #print '-' * 50
    #print 'BFS'.center(10) + str(n1.costo).center(20) + str(n1.nodos_visitados)
    #print 'IDS'.center(10) + str(n2.costo).center(20) + str(n2.nodos_visitados)
    #print 'UCS'.center(10) + str(n3.costo).center(20) + str(n3.nodos_visitados)
    n4, nodosss,costo1 = prueba_busqueda(pos_inicial, busqueda_A_estrella, heuristica_1)
    print 'A* con h1'.center(10) + str(costo1).center(20) + str(nodosss)
    #print str(n4.nodos_visitados)
    n5, nodosss2,costo2 = prueba_busqueda(pos_inicial, busqueda_A_estrella, heuristica_2)
    print 'A* con h2'.center(10) + str(costo2).center(20) + str(nodosss2)
    #print ''
    #print '-' * 50 + '\n\n'
    
    
def comparacion(estado1, estado2):
    for i in range(25):
        if estado1[i]!= estado2[i]:
            print 'Es diferente en: ', i
            return False
    return True
def Imprimir_Estado(estadoI):
    i = 0
    k = 5
    for j in range(5):
        print estadoI[i:k]
        i = i + 5
        k = k + 5
def NO_Igual(estado1, estado2):
    print 'No igual'
    print '-------------------'
    Imprimir_Estado( estado1)
    print '-------------------'
    Imprimir_Estado( estado2)
    print '-------------------'
    return
if __name__ == "__main__":

    print "Antes de hacer otra cosa vamos a verificar medianamente la clase Lights_out"
    prueba_clase()

    # Tres estados iniciales interesantes
    diagonal = (0, 0, 0, 0, 1,
                0, 0, 0, 1, 0,
                0, 0, 1, 0, 0,
                0, 1, 0, 0, 0,
                1, 0, 0, 0, 0)

    simetria = (1, 0, 1, 0, 1,
                1, 0, 1, 0, 1,
                0, 0, 0, 0, 0,
                1, 0, 1, 0, 1,
                1, 0, 1, 0, 1)

    problemin = (0, 1, 0, 1, 0,
                 0, 0, 1, 1, 0,
                 0, 0, 0, 1, 1,
                 0, 0, 1, 1, 1,
                 0, 0, 0, 1, 1)
    print"\n\nVamos a ver como funcionan las búsquedas para un estado inicial \n"
    Lights_out.bonito(diagonal)
    compara_metodos(diagonal, h_1, h_2)
    '''
    print u"\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(simetria)
    compara_metodos(simetria, h_1, h_2)
    
    print u"\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(problemin)
    compara_metodos(problemin, h_1, h_2)
    '''
