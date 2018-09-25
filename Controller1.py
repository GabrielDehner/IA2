import Clases1 as cl
import csv
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import dendrogram
from matplotlib import pylab
from pylab import *
#style.use("ggplot")

#x = cl.Cluster(1, 'red').l
def dibujar_clusters(contenedor_clusters):
    dimension = contenedor_clusters[0].dimension
    if dimension == 3:
        ax = plt.figure().gca(projection="3d")

    for i in range(len(contenedor_clusters)):
        #si esta habilitado
        if contenedor_clusters[i].habilitado:
            for j in range(contenedor_clusters[i].tamanio_lista()):
                if dimension == 2:
                    plt.plot(contenedor_clusters[i].lista_puntos[j][1], contenedor_clusters[i].lista_puntos[j][2], contenedor_clusters[i].color, markersize=10)
                else:
                    ax.scatter(contenedor_clusters[i].lista_puntos[j][1], contenedor_clusters[i].lista_puntos[j][2], contenedor_clusters[i].lista_puntos[j][3], c=contenedor_clusters[i].color, marker=".", s=50)

    #corregir lo de colores para 3d por scarret
    if dimension == 2:
        plt.plot(0, 0, "g.", marker="")
        plt.plot(10, 10, "g.", marker="")
    else:
        ax.scatter(0, 0, 0, c="green", marker="", s=2)
        ax.scatter(50, 50, 50, c="green", marker="", s=2)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
    show()

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
        coordenadas = []
        for j in range(len(cluster.lista_puntos[i])-1):
            coordenadas.append([0]*1)
            coordenadas[j]= cluster.lista_puntos[i][j+1]
        x.aniadir_punto(cluster.lista_puntos[i][0], coordenadas)
    return x
aniadir_puntos_de_cluster

def habilitar_colores_desocupados(color, colors):
    i=0
    no_salir = False
    while(i < len(colors) and not no_salir):
        if colors[i][0]== color and i>0:
            colors[i][1]= "T"
            no_salir = True
        i+=1
    return colors

habilitar_colores_desocupados

def terminar(contenedor):
    cont=0
    retorno = False
    for i in range(len(contenedor)):
        if contenedor[i].habilitado:
            cont+=1

    if cont <= 1:
        retorno = True
    return retorno
terminar

def matriz_para_dendograma(Z, cluster1, cluster2, distancia_minima):
    Z.append([0]*4)
    indice = len(Z) - 1
    Z[indice][0] = cluster1
    Z[indice][1] = cluster2
    Z[indice][2] = distancia_minima
    Z[indice][3] = 0

    return Z
matriz_para_dendograma

def main():
    colors = None
    ruta = None
    print("Ingrese si desea en R2(2) o R3(3): ")
    dimension = input()
    print("Ingrese si desea Single (S), Complete(C) o Average (A) link: ")
    metodo = input()

    if dimension == "2":
        colors = [["g.", "F"], ["r.", "T"], ["b.", "T"], ["y.", "T"], ["c.", "T"]]
    else:
        colors = [["green", "F"], ["red", "T"], ["blue", "T"], ["yellow", "T"], ["cyan", "T"]]

    ruta = "archivo" + str(dimension) + "d.csv"
    datos = open(ruta, "r")
    datos_csv = csv.reader(datos)
    i=0
    lista_clusters = cl.Lista_Cluster(int(dimension), metodo)
    almacen = []
    for almacen in datos_csv:
        x = cl.Cluster(i, colors[0][0], int(dimension))
        x.aniadir_punto(i, almacen)
        lista_clusters.aniadir_cluster(x)
        i=i+1
    datos.close()
    Z=[]
    #lista_clusters.imprimir_lista()


    colors_scatter = ["green", "red", "blue", "yellow", "cyan"]
    dibujar_clusters(lista_clusters.contenedor)

    while (not terminar(lista_clusters.contenedor)):
        cluster1, cluster2, distancia_minima = lista_clusters.armar_cluster()
        Z = matriz_para_dendograma(Z, cluster1, cluster2, distancia_minima)
        # Crear un nuevo cluster con id correspondiente a len(lista_cluster,contenedor)
        # el color deberia se una matriz con usados
        # aniadir todos los puntos del cluster 1 y 2 al nuevo cluster
        color_posible, colors = buscar_color(colors)
        # print (color_posible)
        x = cl.Cluster(len(lista_clusters.contenedor), color_posible, int(dimension))

        print(cluster1, "  ", cluster2, " dist: ", distancia_minima)
        x = aniadir_puntos_de_cluster(x, lista_clusters.buscar_cluster_por_id(cluster1))
        x = aniadir_puntos_de_cluster(x, lista_clusters.buscar_cluster_por_id(cluster2))
        # print("hola")
        # print(x.lista_puntos)
        # Buscar cluster 1, 2, deshabilitarlos, poner dependencia,
        lista_clusters.aniadir_cluster(x)
        lista_clusters.buscar_cluster_por_id(cluster1).habilitado = False
        lista_clusters.buscar_cluster_por_id(cluster2).habilitado = False
        lista_clusters.buscar_cluster_por_id(cluster1).cluster_dependiente = x.id_cluster
        lista_clusters.buscar_cluster_por_id(cluster2).cluster_dependiente = x.id_cluster

        # habilitar colores de los clusters deshabilitados
        colors = habilitar_colores_desocupados(lista_clusters.buscar_cluster_por_id(cluster1).color, colors)
        colors = habilitar_colores_desocupados(lista_clusters.buscar_cluster_por_id(cluster2).color, colors)

        dibujar_clusters(lista_clusters.contenedor)
        # cluster1, cluster2, distancia_minima = lista_clusters.armar_cluster()
        # print(cluster1, "  ", cluster2, " dist: ", distancia_minima)
        #print(colors)

    plt.ylabel('Distancia')
    plt.xlabel('N° Cluster')
    max_d = int(Z[len(Z)-1][2]+3)
    dendrogram(
        Z,
        leaf_rotation=90.,
        leaf_font_size=8.,
        show_contracted=True
    )
    plt.axhline(y=max_d, c='k')
    plt.show()


main()


##weka