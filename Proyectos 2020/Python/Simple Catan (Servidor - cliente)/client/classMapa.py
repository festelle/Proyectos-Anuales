from generador_grilla import GeneradorGrillaHexagonal
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout,\
     QVBoxLayout, QComboBox, QProgressBar)
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
import random
import os

#Se importan los archivos que contienen información importante
with open('grafo.json',) as file:
    datos_grafo = json.load(file)

with open('parametros.json',) as file:
    parametros = json.load(file)


#Función para poder agregar imágenes fácilmente    
def agregar_imagen(ventana, ubicacion, x , y , width, height):
    ventana.label = QLabel(ventana)
    ventana.label.setGeometry(x,y,width,height)
    pixeles = QPixmap(ubicacion)
    ventana.label.setPixmap(pixeles)
    ventana.label.setScaledContents(True)
    return ventana.label




#Se genera una clase nodo con la info pedida en el enunciado e info extra para facilitar
#la representación en el mapa y las acciones a hacer.
class Nodo:
    
    def __init__(self, id):
        self.id = id
        self.estado_actual = 'libre'
        self.dueño = None
        self.vecinos = []
        self.tipos_hexagonos = []
        self.color = None
        
    def agregar_vecino(self, nodo):
        self.vecinos.append(nodo)
        
    def __repr__(self):
        texto = f"[{self.id}]"
        return texto

#Se genera una clase hexágono con la info importante
class hexagono():
    def __init__(self, tipo, num_ficha):
        self.tipo = tipo #De qué materia está hecho (arcilla, madera, trigo)
        self.num_ficha = num_ficha 
        self.path_imagen = None
        self.nodos = []
    

#Esta clase contiene el grafo NO DIRIGIDO creado a partir de los nodos
class class_mapa:
    def __init__(self):
        self.nodos = {}
        self.hexagonos = {}

    #Función creada para servidor, donde se ordenan los nodos en un dict
    def crear_nodos(self):
        
        #Se crean las instancias de nodos
        nodos_a_crear = datos_grafo['nodos']
        for nodo_crear in nodos_a_crear.keys():
            nodo = Nodo(nodo_crear)
            self.nodos[nodo_crear] = nodo

        #Se agregan los vecinos a cada nodo
        for nodo_creado in nodos_a_crear.keys():
            vecinos = nodos_a_crear[nodo_creado]
            for vecino in vecinos:
                self.nodos[nodo_creado].agregar_vecino(self.nodos[vecino])
        
        #Con esto, ya se tienen los nodos en un dict, con su id como llave y su instancia como value
    
    #Función hecha para servidor, crea las instancias hexágonos, junto a sus datos importantes
    def crear_hexagonos(self):
        #Primero se crean las instancias de nodos si no se han creado
        if self.nodos == {}:
            self.crear_nodos()
        #En total hay 10 hexagonos
        self.hexagonos = {}
        self.arcilla = 0
        self.madera = 0
        self.trigo = 0
        materias = ['arcilla', 'madera', 'trigo']
        numeros = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
        #Se crean 10 hexágonos con una materia prima y un número elegidos al azar
        for i in range(10):
            tipo = random.choice(materias)
            numero = random.choice(numeros)
            self.hexagonos[i] = hexagono(tipo, numero)

            #Se controla que cada materia prima salga un min de 3 veces.
            #Al ser 10 hexágonos, habrán 3, 3 y 4 materias primas de cada tipo
            if tipo == 'arcilla':
                self.arcilla += 1
                if self.arcilla >= 3 and len(materias) > 1:
                    materias.remove('arcilla')
                    
            elif tipo == 'madera':
                self.madera += 1
                if self.madera >= 3 and len(materias) > 1:
                    materias.remove('madera')
                    
            elif tipo == 'trigo':
                self.trigo += 1
                if self.trigo >= 3 and len(materias) > 1:
                    materias.remove('trigo')

            numeros.remove(numero)

            #Se agregan los nodos que componen a este hexagono
            for id_nodo in datos_grafo["hexagonos"][f'{i}']:
                self.hexagonos[i].nodos.append(self.nodos[id_nodo])
                self.nodos[id_nodo].tipos_hexagonos.append(self.hexagonos[i].tipo)

        return self.hexagonos
    
    #Funcion hecha exclusivamente para el front end, grafica los nodos
    def dibujar_nodos(self, ventana):
        if self.nodos == {}:
            self.crear_nodos()
        self.label_nodos = {}
        
        for id_nodo in posicion_nodos.keys():
            nodo = QLabel(f'{id_nodo}', ventana)
            nodo.move(posicion_nodos[str(id_nodo)][0],posicion_nodos[str(id_nodo)][1])
            self.label_nodos[str(id_nodo)] = nodo

        return self.label_nodos
    
    #Función exclusiva para frontEnd, actualiza las chozas puestas en el mapa
    def actualizar_nodos(self, lista_label_nodos):
        for id_nodo in lista_label_nodos:
            if self.nodos[id_nodo].estado_actual == 'ocupado':
                #Se agrega la imagen de la chozza del color del jugador
                path = os.path.join(parametros["path sprites"], "Construcciones", \
                    f"choza_{self.nodos[id_nodo].color}")
                label_nodo = lista_label_nodos[id_nodo]
                pixeles = QPixmap(path)
                label_nodo.setPixmap(pixeles)
                label_nodo.setScaledContents(True)
                label_nodo.resize(20, 20)

                
    #Función exclusiva para frontEnd, cambia las imágenes iniciales a las del mapa final
    def agregar_hexagonos(self, ventana, lista_hexagonos, labels_numeros):
        path_imagenes = os.path.join(parametros["path sprites"],'Materias_primas')
        #Primero se le entrega el path de la imagen que está en parámetros de cliente
        for i in self.hexagonos:
            tipo = self.hexagonos[i].tipo

            if tipo == 'arcilla':
                self.hexagonos[i].path_imagen = os.path.join(path_imagenes,'hexagono_arcilla')                
            elif tipo == 'madera':
                self.hexagonos[i].path_imagen = os.path.join(path_imagenes,'hexagono_madera')
            elif tipo == 'trigo':
                self.hexagonos[i].path_imagen = os.path.join(path_imagenes,'hexagono_trigo')
                
        #Se posicionan las imágenes de los hexágonos
        i = 0
        for label_hexagono in lista_hexagonos:
            pixeles = QPixmap(self.hexagonos[i].path_imagen)
            label_hexagono.setPixmap(pixeles)
            i += 1
        
        for i in range(len(labels_numeros)):
            labels_numeros[i].setText(str(self.hexagonos[i].num_ficha))
            labels_numeros[i].move(lista_hexagonos[i].x()+50,lista_hexagonos[i].y()+50)
            labels_numeros[i].setStyleSheet("background-color: lightblue")

    #Para frontEnd, crea labels iniciales en el init y devuelve una lista de estos labels
    #para que después se puedan cambiar por las imágenes finales
    def crear_base_mapa(self, ventana):
        #Se posicionan las imágenes de los hexágonos
        self.label_imagenes = []
        self.coordenadas = []
        path_imagen = os.path.join(parametros["path sprites"],'Otros','Logo_simple.png')
        
        label_0 = agregar_imagen(ventana, path_imagen, 65,65,120,110)
        self.label_imagenes.append(label_0)
        self.coordenadas.append((65,65))
        label_1 = agregar_imagen(ventana, path_imagen, 65+120+90,65,120,110)
        self.label_imagenes.append(label_1)
        self.coordenadas.append((65+120+90,65))

        label_2 = agregar_imagen(ventana, path_imagen, 65+105,65+60,120,110)
        self.label_imagenes.append(label_2)
        self.coordenadas.append((65+105,65+60))
        label_3 = agregar_imagen(ventana, path_imagen, 65+105+120+90,65+60,120,110)
        self.label_imagenes.append(label_3)
        self.coordenadas.append((65+105+120+90,65+60))

        label_4 = agregar_imagen(ventana, path_imagen, 65,65+120,120,110)
        self.label_imagenes.append(label_4)
        self.coordenadas.append((65,65+120))
        label_5 = agregar_imagen(ventana, path_imagen, 65+120+90,65+120,120,110)
        self.label_imagenes.append(label_5)
        self.coordenadas.append((65+120+90,65+120))

        label_6 = agregar_imagen(ventana, path_imagen, 65+105, 65+120+60, 120,110)
        self.label_imagenes.append(label_6)
        self.coordenadas.append((65+105, 65+120+60))
        label_7 = agregar_imagen(ventana, path_imagen, 65+120+90+105, 65+120+60, 120,110)
        self.label_imagenes.append(label_7)
        self.coordenadas.append((65+120+90+105, 65+120+60))

        label_8 = agregar_imagen(ventana, path_imagen, 65, 65+120+120, 120,110)
        self.label_imagenes.append(label_8)
        self.coordenadas.append((65, 65+120+120))
        label_9 =  agregar_imagen(ventana, path_imagen, 65+120+90, 65+120+120, 120,110)
        self.label_imagenes.append(label_9)
        self.coordenadas.append((65+120+90, 65+120+120))
    
        return self.label_imagenes


#Se crea la grilla 
grilla = GeneradorGrillaHexagonal(70)

#Se crea el dict con la posición de los nodos de las mapas.
posicion_nodos = grilla.generar_grilla(datos_grafo["dimensiones_mapa"], 50, 50)