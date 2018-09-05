from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn import datasets
import numpy as np

X = np.array([[1, 2],
              [5, 8],
              [1.5, 1.8],
              [8, 8],
              [1, 0.6],
              [9, 11]])
print(X)
print("----------------------\n\n\n")

Z = linkage(X, 'single')
#for i in range(len(Z)):
    #Z[i][3]=0

print (Z)


plt.ylabel('Distancia')
max_d = 20
dendrogram(
        Z,
        leaf_rotation=90.,
        leaf_font_size=8.,
        show_contracted=True
    )
plt.axhline(y=max_d, c='k')
plt.show()