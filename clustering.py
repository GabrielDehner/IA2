import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
def main():
    m = open("archivo.csv", "r")
    m_csv = csv.reader(m)
    p=[0]*2
    a=[]
    i=0
    for cab1, cab2 in m_csv:
        print ("c1-----> ", cab1, " \tc2----> ", cab2)
        a.append([0]*2)
        a[i][0] = float(cab1)
        a[i][1] = float(cab2)
        i=i+1
    m.close()
    #print (a)
    a = np.array(a)
    i=0

    X = np.array([[1, 2],
                  [5, 8],
                  [1.5, 1.8],
                  [8, 8],
                  [1, 0.6],
                  [9, 11]])
    print(a)
    #print("--------------")
    #print(X)
    colors = ["g.", "r.", "c.", "y."]

    for i in range(len(a)):
        plt.plot(a[i][0], a[i][1], colors[0], markersize=10)
        plt.plot(0, 0, colors[0], marker="")

    plt.show()

main()