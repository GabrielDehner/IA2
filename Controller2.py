import Clases2 as cl
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
    #show()

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


def ejecutar_metodos_s_c_a(lista_clusters, Z, dimension, colors):
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

        # print(cluster1, "  ", cluster2, " dist: ", distancia_minima)
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

       # dibujar_clusters(lista_clusters.contenedor)

    """plt.ylabel('Distancia')
    plt.xlabel('N° Cluster')
    max_d = int(Z[len(Z)-1][2]+3)
    dendrogram(
        Z,
        leaf_rotation=90.,
        leaf_font_size=8.,
        show_contracted=True
    )
    plt.axhline(y=max_d, c='k')
    plt.show()"""
    lista_clusters.imprimir_lista()
    return lista_clusters, Z
ejecutar_metodos_s_c_a

def graficar_cantidad_clusters(tamanio_inicial_clusters, tamanio_deseado, contenedor):

    #el tamanio inicial -1= todos los individuales pj 10
    #si quiero 6, son  10-6=4 iteraciones se necesitan
    #cantidad de iteraciones = tamanio_inicial_clusters - tamanio_deseado
    #poner en true los que se quieren graficar
    #habilitar hasta tamanio inicial -1  mas la cantidad de iteraciones. pero desde tam inicial-1 hasta cant de iteraciones
    #guardar esos clusters y desabilitar los cluster que coincidan con los puntos (o sea tam del contenedor=1)

    cantidad_iteraciones = tamanio_inicial_clusters - tamanio_deseado

    tope = tamanio_inicial_clusters + cantidad_iteraciones
    #print("cant it ", cantidad_iteraciones)
    #print("tope ", tope)
    #print("tam des ", tamanio_deseado)
    #print("tam ini ", tamanio_inicial_clusters)
    for i in range(len(contenedor)):
        if i < tope:
            contenedor[i].habilitado = True
        else:
            contenedor[i].habilitado = False
        if contenedor[i].cluster_dependiente >= (tamanio_deseado-1) and contenedor[i].cluster_dependiente < tope:
            contenedor[i].habilitado = False
    #dibujar_clusters(contenedor)
    print("----------ww-")
    print("----------Clusters pedidos------")
    #for i in range(len(contenedor)):
     #   print(contenedor[i].id_cluster, " ", contenedor[i].habilitado)
    dibujar_clusters(contenedor)
    show()

    for i in range(len(contenedor)):
        if contenedor[i].habilitado:
            print(contenedor[i].id_cluster)


graficar_cantidad_clusters

def graficar_cantidad_elementos(cantidad_elementos, contenedor):
    salir = False
    for i in range(len(contenedor)):
        contenedor[i].habilitado = False
    i=0
    while(i < len(contenedor) and not(salir)):
        if len(contenedor[i].lista_puntos) <= cantidad_elementos:
            contenedor[i].habilitado = True
        else:
            salir = True
        i+=1


    dibujar_clusters(contenedor)
    show()


graficar_cantidad_elementos


def graficar_dendograma(Z):
    plt.ylabel('Distancia')
    plt.xlabel('N° Cluster')
    max_d = int(Z[len(Z) - 1][2] + 3)
    dendrogram(
        Z,
        leaf_rotation=90.,
        leaf_font_size=8.,
        show_contracted=True
    )
    plt.axhline(y=max_d, c='k')
    plt.show()
graficar_dendograma


def main():
    colors = None
    ruta = None
    print("Ingrese si desea en R2(2) o R3(3): ")
    dimension = input()
    #print("Ingrese si desea Single (S), Complete(C) o Average (A) link: ")
    #metodo = input()


    if dimension == "2":
        colors = [["g.", "F"], ["r.", "T"], ["b.", "T"], ["y.", "T"], ["c.", "T"]]
    else:
        colors = [["green", "F"], ["red", "T"], ["blue", "T"], ["yellow", "T"], ["cyan", "T"]]

    ruta = "archivo" + str(dimension) + "d.csv"
    datos = open(ruta, "r")
    datos_csv = csv.reader(datos)
    i=0
    lista_clusters_single = cl.Lista_Cluster(int(dimension), "S")
    lista_clusters_complete = cl.Lista_Cluster(int(dimension), "C")
    lista_clusters_average = cl.Lista_Cluster(int(dimension), "A")

    almacen = []
    for almacen in datos_csv:
        x_s = cl.Cluster(i, colors[0][0], int(dimension))
        x_c = cl.Cluster(i, colors[0][0], int(dimension))
        x_a = cl.Cluster(i, colors[0][0], int(dimension))
        x_s.aniadir_punto(i, almacen)
        x_c.aniadir_punto(i, almacen)
        x_a.aniadir_punto(i, almacen)
        lista_clusters_single.aniadir_cluster(x_s)
        lista_clusters_complete.aniadir_cluster(x_c)
        lista_clusters_average.aniadir_cluster(x_a)
        i=i+1
    datos.close()
    tamanio_inicial_clusters = len(lista_clusters_single.contenedor)
    Z_single=[]
    Z_complete=[]
    Z_average=[]

    #lista_clusters.imprimir_lista()


    colors_scatter = ["green", "red", "blue", "yellow", "cyan"]
    print("-----------------------------------------------------------------------------------")
    lista_clusters_single, Z_single = ejecutar_metodos_s_c_a(lista_clusters_single, Z_single, dimension, colors)
    print("-----------------------------------------------------------------------------------")
    lista_clusters_complete, Z_complete = ejecutar_metodos_s_c_a(lista_clusters_complete, Z_complete, dimension, colors)
    print("-----------------------------------------------------------------------------------")
    lista_clusters_average, Z_average = ejecutar_metodos_s_c_a(lista_clusters_average, Z_average, dimension, colors)

    #dibujar_clusters(lista_clusters_single.contenedor)
    #dibujar_clusters(lista_clusters_complete.contenedor)
    #dibujar_clusters(lista_clusters_average.contenedor)

    print("Ingrese la cantidad de clusters a mostrar: ")
    tamanio_deseado = int(input())
    graficar_cantidad_clusters(tamanio_inicial_clusters, tamanio_deseado, lista_clusters_single.contenedor)
    graficar_cantidad_clusters(tamanio_inicial_clusters, tamanio_deseado, lista_clusters_complete.contenedor)
    graficar_cantidad_clusters(tamanio_inicial_clusters, tamanio_deseado, lista_clusters_average.contenedor)

    print("Ingrese la cantidad máxima de elementos en un cluster: ")
    cantidad_elementos = int(input())
    graficar_cantidad_elementos(cantidad_elementos, lista_clusters_single.contenedor)
    graficar_cantidad_elementos(cantidad_elementos, lista_clusters_complete.contenedor)
    graficar_cantidad_elementos(cantidad_elementos, lista_clusters_average.contenedor)

    print("Graficar Dendograma")
    graficar_dendograma(Z_single)
    graficar_dendograma(Z_complete)
    graficar_dendograma(Z_average)




main()


##weka

##Para mejorar el tp
#Mostrar de acuerdo a la cantidad de clusters que quiere el usuario
    #Usar Controller1 para ver como se llegaria a 3 clusters pj..
    #En cada iteracion se aniade un punto a un cluster
    #https://link.ubnt.com/
    #https://link.ubnt.com/#ap.device.antennaGain=25&ap.device.channelWidth=20&ap.device.eirp=50&ap.device.frequency=5600&ap.device.name=PowerBeam%205AC%20Gen2&ap.height=12&ap.location.lat=-27.24126805845993&ap.location.lng=-56.03444878007815&coverageCpeHeight=12&coverageRadius=20000&mapTypeId=terrain&version=1.0.2