import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

##Tener semillas iniciales como clusters iniciales se quieran
##Este es el single


def calculo_distancia_minima(matriz_centroides, matriz_datos):
    #print("mc: ", matriz_centroides, "\t md: ", matriz_datos)
    distancia = -5
    centroide = -5
    for i in range (len(matriz_centroides)):
        distancia_calculada = (((matriz_centroides[i][0]-matriz_datos[0])**2)+((matriz_centroides[i][1]-matriz_datos[1])**2))**(1/2)
        if distancia==-5:
            distancia = distancia_calculada
            centroide = matriz_centroides[i][2]
        else:
            if distancia_calculada<distancia:
                distancia = distancia_calculada
                centroide = matriz_centroides[i][2]
    return centroide
calculo_distancia_minima

def calculo_distancia_minima_sin_mismo(matriz_datos, fila_actual):
    #print("mc: ", matriz_centroides, "\t md: ", matriz_datos)
    distancia = -5
    centroide = -5
    cluster = 0;
    for i in range (len(matriz_datos)):
        if fila_actual[2]!=matriz_datos[i][2]:
            distancia_calculada = (((fila_actual[0]-matriz_datos[i][0])**2)+((fila_actual[1]-matriz_datos[i][1])**2))**(1/2)
            if distancia==-5:
                distancia = distancia_calculada
                centroide = matriz_datos[i][2]
            else:
                if distancia_calculada<distancia:
                    distancia = distancia_calculada
                    cluster = matriz_datos[i][2]
    return (cluster, distancia)
calculo_distancia_minima_sin_mismo

def single_link_closest(matriz_centroides, matriz_datos, informacion_clusters):
#comparar un punto con todos los demas que sean de otro cluster
#ir guardando la distancia y elegir la menor entre todos los clusters
#
    arbol_centroide = []
    j=0
    matriz_datos = np.insert(matriz_datos, 3,np.zeros((1,len(matriz_datos))),axis=1)
    for i in range(len(matriz_datos)):
        #if informacion_clusters[i][1]==-1:.
        matriz_datos[i][2], matriz_datos[i][3] = calculo_distancia_minima_sin_mismo(matriz_datos, matriz_datos[i])

    distancia=0
    clus=0
    for i in range(len(informacion_clusters)):
        for j in range (len(matriz_datos)):
            if matriz_datos[j][2]==informacion_clusters[i][0]:
                if distancia==0:
                    clus = matriz_datos[j][3]
                else:
                    if matriz_datos[j][3]<distancia:
                        distancia = matriz_datos[j][3]
                        clus = matriz_datos[j][2]

        # el arbol debe tener, numero de cluster al q pertenece y numero con el que se deberia agrupar
        arbol_centroide.append([0] * 2)
        arbol_centroide[i][0] = int(informacion_clusters[i][0])
        arbol_centroide[i][1] = int(clus)
    return (matriz_centroides, matriz_datos, arbol_centroide)
single_link_closest

def no_dependencia_repetida(dependencia_repetida, index):
    ret = True
    if len(dependencia_repetida)>0:
        for i in range(len(dependencia_repetida)):
            if index==dependencia_repetida[i]:
                ret = False
    return ret
no_dependencia_repetida

def main():
    datos = open("archivo.csv", "r")
    datos_csv = csv.reader(datos)
    matriz_datos=[]
    i=0
    for cab1, cab2 in datos_csv:
        #print ("c1-----> ", cab1, " \tc2----> ", cab2)
        matriz_datos.append([0]*2)
        matriz_datos[i][0] = float(cab1)
        matriz_datos[i][1] = float(cab2)
        i=i+1
    datos.close()
    matriz_datos = np.array(matriz_datos)
    i=0
    centroides_ini = open("centroides.csv", "r")
    centroides_ini_csv = csv.reader(centroides_ini)
    matriz_centroides=[]
    for col1, col2 in centroides_ini_csv:
        #print("c1-----> ", col1, " \tc2----> ", col2)
        matriz_centroides.append([0]*3)
        matriz_centroides[i][0] = float(col1)
        matriz_centroides[i][1] = float(col2)
        matriz_centroides[i][2] = int(i)
        i=i+1
    centroides_ini.close()
    i=0
    matriz_centroides = np.array(matriz_centroides)

    informacion_clusters =[]

    for i in range(len(matriz_centroides)):
        informacion_clusters.append([0]*2)
        #una columna de numero de cluster y otra de dependencia de cluster
        informacion_clusters[i][0]= int(matriz_centroides[i][2])
        informacion_clusters[i][1]= -1
        #-1 es equivalente a null para saber que no depende de nada

    #print(informacion_clusters)


    colors = ["g.", "r.", "b.", "y.", "c."]
    colors_scatter = ["green", "red", "blue", "yellow", "cyan"]

    ###################Algoritmo generico para clustering inicio######################
    ##calculo de distancia para asignar a centroide correspondiente
    ##calcular distancias hacia los centroides y luego asignar al mas cercano
    clusters = len(matriz_centroides)


    matriz_datos = np.insert(matriz_datos, 2,np.zeros((1,len(matriz_datos))),axis=1)


    for i in range(len(matriz_datos)):
        centroide = calculo_distancia_minima(matriz_centroides, matriz_datos[i])
        matriz_datos[i][2]=centroide
        plt.plot(matriz_datos[i][0], matriz_datos[i][1], colors[int(centroide)], markersize=10)

    plt.plot(0, 0, colors[0], marker="")
    plt.plot(50, 50, colors[0], marker="")

    for i in range(len(matriz_centroides)):
        plt.scatter(matriz_centroides[i][0], matriz_centroides[i][1],c=colors_scatter[int(matriz_centroides[i][2])], marker="*", s=150, linewidths=5, zorder=10)
        #colors[int(matriz_centroides[i][2])],
        #plt.scatter(10, 5, marker="*", s=150, linewidths=5, zorder=10)

    plt.show()
    #print(matriz_datos)


    #######Single Link
    #al arbol se lo podria meter directamente en la matriz de centroide asi se reutiliza siempre
    #hasta q quede en una jerarquia
    matriz_centroides, matriz_datos, arbol_centroide = single_link_closest(matriz_centroides, matriz_datos, informacion_clusters)

    #mientras haya mas de uno con -1 en informacion_cluster
    band = 1
    while band:
        dependencia_repetida = []
        for i in range(len(arbol_centroide)):
            for j in range(len(arbol_centroide)):
                if arbol_centroide[i][0]==arbol_centroide[j][1] and arbol_centroide[j][0]==arbol_centroide[i][1]:
                    if no_dependencia_repetida(dependencia_repetida, i):
                        #agregar un cluster padre y no hay que mirar arriba cuando se repita pq van a ser dos
                        informacion_clusters.append([0]*2)
                        informacion_clusters[len(informacion_clusters) - 1][0]= len(informacion_clusters) - 1
                        informacion_clusters[len(informacion_clusters) - 1][1]=-1
                        informacion_clusters[i][1] = len(informacion_clusters) - 1
                        informacion_clusters[j][1] = len(informacion_clusters) - 1
                        dependencia_repetida.append([0]*1)
                        dependencia_repetida[len(dependencia_repetida) - 1] = j
                        ##ESTOY HACIENDO MAL, PQ COMPARO CON EL PUNTO, DEBO COMPARAR CON LOS PUNTOS MAS CERCANOS
                        ##ENTRE PARES DE PUNTOS DE CONJUNTOS DISTINTOS

        ##a la matriz de datos hacerla dependiente del ultimo clustering si es distinto a -1
        #print(matriz_datos)
        for i in range(len(matriz_datos)):
            if informacion_clusters[int(matriz_datos[i][2])][1]!=-1:
                matriz_datos[i][2]= informacion_clusters[int(matriz_datos[i][2])][1]
        #print(matriz_datos)
        print("arbol centroide: ",arbol_centroide)
        print("------------")
        print("info clust: ",informacion_clusters)



        for i in range(len(matriz_datos)):
            color=int(matriz_datos[i][2])
            if int(matriz_datos[i][2])>= len(colors):
                color = len(colors)- matriz_datos[i][2]
                #ver bien esto del color para q no se repita un color ya usado
            plt.plot(matriz_datos[i][0], matriz_datos[i][1], colors[color], markersize=10)

        plt.plot(0, 0, colors[0], marker="")
        plt.plot(50, 50, colors[0], marker="")
        plt.show()
        cont=0
        for i in range(len(informacion_clusters)):
            if informacion_clusters[i][1]==-1:
                cont=cont+1
                #print(cont)
        if cont <= 1:
            band = 0
        #print(band)

        matriz_centroides, matriz_datos, arbol_centroide = single_link_closest(matriz_centroides, matriz_datos,
                                                                               informacion_clusters)
        print("---------\n\n")
        #print(arbol_centroide)
        #print("------------")
        #print(informacion_clusters)

main()
