import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

##Tener semillas iniciales como clusters iniciales se quieran
##Este es el single

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
        print("c1-----> ", col1, " \tc2----> ", col2)
        matriz_centroides.append([0]*3)
        matriz_centroides[i][0] = float(col1)
        matriz_centroides[i][1] = float(col2)
        matriz_centroides[i][2] = int(i)
        i=i+1
    centroides_ini.close()
    i=0
    matriz_centroides = np.array(matriz_centroides)

    #print (a)

    #print(matriz_datos)
    #print("--------------")
    #print(X)
    print(matriz_centroides)
    colors = ["g.", "r.", "c.", "y."]

    for i in range(len(matriz_datos)):
        plt.plot(matriz_datos[i][0], matriz_datos[i][1], colors[0], markersize=10)
        plt.plot(0, 0, colors[0], marker="")

    for i in range(len(matriz_centroides)):
        plt.scatter(matriz_centroides[i][0], matriz_centroides[i][1], marker="*", s=150, linewidths=5, zorder=10)
        #plt.scatter(10, 5, marker="*", s=150, linewidths=5, zorder=10)

    plt.show()

main()