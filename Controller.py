import Clases as cl
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

#x = cl.Cluster(1, 'red').tamanio_lista()
def dibujar_clusters(contenedor_clusters):
    for i in range(len(contenedor_clusters)):
        for j in range(contenedor_clusters[i].tamanio_lista()):
            plt.plot(contenedor_clusters[i].lista_puntos[j][1], contenedor_clusters[i].lista_puntos[j][2], contenedor_clusters[i].color, markersize=10)
    plt.plot(0, 0, "g.", marker="")
    plt.plot(10, 10, "g.", marker="")
    plt.show()
dibujar_clusters

def main():
    colors = [["g.", "T"], ["r.", "F"], ["b.", "F"], ["y.", "F"], ["c.", "F"]]
    datos = open("archivo.csv", "r")
    datos_csv = csv.reader(datos)
    i=0
    lista_clusters = cl.Lista_Cluster()
    for col1, col2 in datos_csv:
        x = cl.Cluster(i, colors[0][0])
        x.aniadir_punto(i, float(col1), float(col2))
        lista_clusters.aniadir_cluster(x)
        i=i+1
    datos.close()

    #lista_clusters.imprimir_lista()


    colors_scatter = ["green", "red", "blue", "yellow", "cyan"]

    dibujar_clusters(lista_clusters.contenedor)
    cluster1, cluster2, distancia_minima = lista_clusters.armar_cluster()
    #Crear un nuevo cluster con id correspondiente a len(lista_cluster,contenedor)
    #el color deberia se una matriz con usados
    #Buscar cluster 1, 2, deshabilitarlos, poner dependencia,
    #aniadir todos los puntos del cluster 1 y 2 al nuevo cluster

    x = cl.Cluster(i, colors[0][0])
    x.aniadir_punto(i, float(col1), float(col2))
    lista_clusters.aniadir_cluster(x)





main()
