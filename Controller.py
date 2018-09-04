import Clases as cl
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

#x = cl.Cluster(1, 'red').l
def dibujar_clusters(contenedor_clusters):
    for i in range(len(contenedor_clusters)):
        #si esta habilitado
        if contenedor_clusters[i].habilitado:
            for j in range(contenedor_clusters[i].tamanio_lista()):
                plt.plot(contenedor_clusters[i].lista_puntos[j][1], contenedor_clusters[i].lista_puntos[j][2], contenedor_clusters[i].color, markersize=10)
    plt.plot(0, 0, "g.", marker="")
    plt.plot(10, 10, "g.", marker="")
    plt.show()
dibujar_clusters

def buscar_color(colors):
    no_salir = False
    i=0
    color="X"
    while(i < len(colors) and not no_salir):
        if colors[i][1]== "T":
            color=colors[i][0]
            colors[i][1]= "F"
            no_salir = True
        i+=1
    if color=="X":
        color = "g."
    return color, colors
buscar_color

def aniadir_puntos_de_cluster(x, cluster):
    for i in range(len(cluster.lista_puntos)):
        x.aniadir_punto(cluster.lista_puntos[i][0], cluster.lista_puntos[i][1], cluster.lista_puntos[i][2])
    return x
aniadir_puntos_de_cluster

def main():
    colors = [["g.", "F"], ["r.", "T"], ["b.", "T"], ["y.", "T"], ["c.", "T"]]
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
    h=0
    print(colors)
    while(h<4):
        cluster1, cluster2, distancia_minima = lista_clusters.armar_cluster()
        #Crear un nuevo cluster con id correspondiente a len(lista_cluster,contenedor)
        #el color deberia se una matriz con usados
        #aniadir todos los puntos del cluster 1 y 2 al nuevo cluster
        color_posible, colors = buscar_color(colors)
        #print (color_posible)
        x = cl.Cluster(len(lista_clusters.contenedor), color_posible)

        print(cluster1, "  ", cluster2, " dist: ", distancia_minima)
        x = aniadir_puntos_de_cluster(x, lista_clusters.buscar_cluster_por_id(cluster1))
        x = aniadir_puntos_de_cluster(x, lista_clusters.buscar_cluster_por_id(cluster2))
        #print("hola")
        #print(x.lista_puntos)
        #Buscar cluster 1, 2, deshabilitarlos, poner dependencia,
        lista_clusters.aniadir_cluster(x)
        lista_clusters.buscar_cluster_por_id(cluster1).habilitado = False
        lista_clusters.buscar_cluster_por_id(cluster2).habilitado = False
        lista_clusters.buscar_cluster_por_id(cluster1).cluster_dependiente = x.id_cluster
        lista_clusters.buscar_cluster_por_id(cluster2).cluster_dependiente = x.id_cluster

        dibujar_clusters(lista_clusters.contenedor)
        #cluster1, cluster2, distancia_minima = lista_clusters.armar_cluster()
        #print(cluster1, "  ", cluster2, " dist: ", distancia_minima)
        print (colors)
        h+=1

main()
