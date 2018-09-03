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

def calculo_distancia_minima_sin_mismo(matriz_centroides, matriz_datos, uno_mismo):
    #print("mc: ", matriz_centroides, "\t md: ", matriz_datos)
    distancia = -5
    centroide = -5
    for i in range (len(matriz_datos)):
        if matriz_datos[i][2]!=uno_mismo:
            distancia_calculada = (((matriz_centroides[0]-matriz_datos[i][0])**2)+((matriz_centroides[1]-matriz_datos[i][1])**2))**(1/2)
            if distancia==-5:
                distancia = distancia_calculada
                centroide = matriz_datos[i][2]
            else:
                if distancia_calculada<distancia:
                    distancia = distancia_calculada
                    centroide = matriz_datos[i][2]
    return centroide
calculo_distancia_minima_sin_mismo

def single_link_closest(matriz_centroides, matriz_datos):

    arbol_centroide = []

    for i in range(len(matriz_centroides)):
        distancia_minima = calculo_distancia_minima_sin_mismo(matriz_centroides[i], matriz_datos,i)

        arbol_centroide.append([0] * 2)
        arbol_centroide[i][0] = int(i)
        arbol_centroide[i][1] = int(distancia_minima)
    return (matriz_centroides, matriz_datos, arbol_centroide)
single_link_closest

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
    matriz_centroides, matriz_datos, arbol_centroide = single_link_closest(matriz_centroides, matriz_datos)
    for i in range(len(arbol_centroide)):
        for j in range(len(arbol_centroide)):
            if arbol_centroide[i][0]==arbol_centroide[j][1] and arbol_centroide[j][0]==arbol_centroide[i][1]:
                #agregar un cluster padre
                informacion_clusters.append([0]*2)
                informacion_clusters[len(informacion_clusters) - 1][0]= len(informacion_clusters) - 1
                informacion_clusters[len(informacion_clusters) - 1][1]=-1
                informacion_clusters[i][1] = len(informacion_clusters) - 1
                informacion_clusters[j][1] = len(informacion_clusters) - 1

    ##a la matriz de datos hacerla dependiente del ultimo clustering si es distinto a -1
    print(matriz_datos)
    for i in range(len(matriz_datos)):
        if informacion_clusters[int(matriz_datos[i][2])][1]!=-1:
            matriz_datos[i][2]= informacion_clusters[int(matriz_datos[i][2])][1]
    print("------------")
    print(matriz_datos)
    print(arbol_centroide)



    for i in range(len(matriz_datos)):
        plt.plot(matriz_datos[i][0], matriz_datos[i][1], colors[int(matriz_datos[i][2])], markersize=10)

    plt.plot(0, 0, colors[0], marker="")
    plt.plot(50, 50, colors[0], marker="")
    plt.show()
main()
