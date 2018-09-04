class Cluster:
    def __init__(self, id_cluster, color):
        self.id_cluster = id_cluster
        self.lista_puntos = []
        self.cluster_dependiente = -1
        self.habilitado = True
        self.color = color
    def aniadir_punto(self, id_punto, x, y):
        self.lista_puntos.append([0]*3)
        indice = self.tamanio_lista()-1
        self.lista_puntos[indice][0] = id_punto
        self.lista_puntos[indice][1] = x
        self.lista_puntos[indice][2] = y
    def tamanio_lista(self):
        return len(self.lista_puntos)
    def buscar_punto_por_id(self, id_buscado):
        indice=-1
        i=0
        no_salir = False
        while(i < self.tamanio_lista() and not (no_salir)):
            if self.lista_puntos[i][0] == id_buscado:
                indice = i
                no_salir = True
            i+=1
        return indice

    def distancia_minima_entre_clusters(self, cluster_x):
        distancia_min = self.distancia_minima_con_cluster(cluster_x.lista_puntos[0][1], cluster_x.lista_puntos[0][2])
        for i in range(cluster_x.tamanio_lista()):
            distancia_calculada = self.distancia_minima_con_cluster(cluster_x.lista_puntos[i][1], cluster_x.lista_puntos[i][2])
            if distancia_calculada < distancia_min:
                distancia_min = distancia_calculada
                #id1, id2, distancia.. minima en este caso, alla recibe como calculada
        return self.id_cluster, cluster_x.id_cluster, distancia_min

    def distancia_minima_con_cluster(self, x, y):
        distancia_min = self.distancia_euclidiana(x, y, self.lista_puntos[0][1], self.lista_puntos[0][2])
        for i in range(self.tamanio_lista()):
            distancia_calculada = self.distancia_euclidiana(x, y, self.lista_puntos[i][1], self.lista_puntos[i][2])
            if distancia_calculada < distancia_min:
                distancia_min = distancia_calculada
        return distancia_min

    def distancia_euclidiana(self, x1, y1, x2, y2):
        return ((x1-x2)**2+(y1-y2)**2)**(1/2)

class Lista_Cluster:
    def __init__(self):
        self.contenedor = []
    def aniadir_cluster(self, cluster):
        self.contenedor.append([0] * 1)
        indice = self.tamanio_contenedor() - 1
        self.contenedor[indice] = cluster
    def tamanio_contenedor(self):
        return len(self.contenedor)

    def buscar_cluster_por_id(self, id_buscado):
        cluster = -1
        i = 0
        no_salir = False
        while (i < self.tamanio_contenedor() and not (no_salir)):
            if self.contenedor[i].id_cluster == id_buscado:
                cluster = self.contenedor[i]
                no_salir = True
            i += 1
        return cluster
    def armar_cluster(self):
        distancia_minima = -1
        cluster1 = -1
        cluster2 = -1
        for i in range(self.tamanio_contenedor()):
            ##antes del otro for, ver si el cluster esta habilitado para competir con las distancias
            if self.contenedor[i].habilitado:
                for j in range(self.tamanio_contenedor()):
                    if(i != j):
                        id1, id2, distancia_calculada = self.contenedor[i].distancia_minima_entre_clusters(self.contenedor[j])
                        if distancia_minima == -1:
                            distancia_minima = distancia_calculada
                            cluster1 = id1
                            cluster2 = id2
                        else:
                            if distancia_calculada < distancia_minima:
                                distancia_minima = distancia_calculada
                                cluster1 = id1
                                cluster2 = id2
        return cluster1, cluster2, distancia_minima
    def imprimir_lista(self):
        for i in range(self.tamanio_contenedor()):
            print(self.contenedor[i].id_cluster, " " , self.contenedor[i].lista_puntos[0][1], " " , self.contenedor[i].lista_puntos[0][2])