from tkinter import *

from tkinter.ttk import *

class Ventana:
    def __init__(self, titulo, tamanio):
        self.window = Tk()
        self.window.title(titulo)
        self.window.geometry(tamanio)


ventana_principal = Ventana("Inteligencia Artificial II", "320x600")

combo = Combobox(ventana_principal.window)
combo['values'] = ("R2", "R3")
combo.current(0)
combo.grid(column=0, row=1)
etiq1 = Label(ventana_principal.window, text="Seleccione la dimension de los datos")
etiq1.grid(column=0, row=0)

combo2 = Combobox(ventana_principal.window)
combo2['values'] = ("Single-Link", "Complete-Link", "Average-Link")
combo2.current(0)
combo2.grid(column=0, row=3)
etiq2 = Label(ventana_principal.window, text="Seleccione el método de Clustering")
etiq2.grid(column=0, row=2)

etiq3 = Label(ventana_principal.window, text="Indique la cantidad de Clusters que desea obtener")
etiq3.grid(column=0, row=4)
input1 = Entry(ventana_principal.window)
input1.grid(column=0, row=5)

btn1 = Button(ventana_principal.window, text="Gráfica")
btn1.grid(column=0, row=6)

ventana_principal.window.mainloop()