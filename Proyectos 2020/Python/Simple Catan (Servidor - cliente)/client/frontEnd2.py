import sys
import os
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QTimer, QRect, QObject
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout,\
     QVBoxLayout, QComboBox, QProgressBar)
from PyQt5.QtGui import QPixmap, QFont
import json
from classMapa import class_mapa
from classMapa import agregar_imagen
import random

#Se guardan los parámetros
with open('parametros.json',) as file:
    json_deserializado = json.load(file)

class ventana_inicio(QWidget):
    senal_mostrar_inicio = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.init_gui()
        self.senal_entrar_sala = None
        self.username = None

        self.senal_mostrar_inicio.connect(self.show)
    
    def init_gui(self):
        self.setWindowTitle('DCColonos')
        self.setGeometry(100, 100, 300, 300)
        #Se pone el fondo
        self.imagen = QLabel(self)
        self.imagen.setGeometry(0,0,300,300)
        ruta_imagen = os.path.join(path_sprites,'Otros\Logo_fondo.png')
        pixeles = QPixmap(ruta_imagen)
        self.imagen.setPixmap(pixeles)
        self.imagen.setScaledContents(True)
        #Se crea y conecta el botón para entrar a sala de espera
        self.botonJugar = QPushButton('&Jugar', self)
        self.botonJugar.setGeometry(100,125,100,50)
        self.botonJugar.clicked.connect(self.boton_clickeado)
    
    def boton_clickeado(self):
        #Se manda señal para solicitar entrar al socket del server
        self.senal_entrar_sala.emit()
        self.hide()

class ventana_rechazo(QWidget):
    #Si el server rechaaza la conexión, se muetra esta ventana
    senal_rechazo = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.senal_rechazo.connect(self.show)
        self.senal_mostrar_inicio = None
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('DCColonos')
        self.setGeometry(100, 100, 300, 300)

        self.advertencia = QLabel('El servidor está lleno', self)
        self.advertencia.setGeometry(10,10,200,100)
        #Se crea y conecta el botón para volver a ventana de inicio
        self.botonVolver = QPushButton('&Volver', self)
        self.botonVolver.setGeometry(100,125,100,50)
        self.botonVolver.clicked.connect(self.boton_clickeado)

        vbox = QVBoxLayout()
        vbox.addWidget(self.advertencia)
        vbox.addWidget(self.botonVolver)
    
    def boton_clickeado(self):
        self.hide()
        self.senal_mostrar_inicio.emit()

class sala_espera(QWidget):
    senal_mostrar_sala = pyqtSignal()
    senal_esconder_sala = pyqtSignal()
    senal_actualizar_usernames = pyqtSignal(str, list)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.username = None
        self.usernames = []
        self.puestos = []
        self.senal_actualizar_usernames.connect(self.actualizar_usernames)
        self.senal_mostrar_sala.connect(self.show)
        self.senal_esconder_sala.connect(self.hide)

        self.senal_mostrar_juego = None

        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('DCColonos')
        self.setGeometry(100, 100, 400, 600)
        #Se agrega una imagen
        self.imagen = QLabel(self)
        self.imagen.setGeometry(0,0,400,200)
        ruta_imagen = os.path.join(path_sprites,'Otros\Logo_fondo.png')
        pixeles = QPixmap(ruta_imagen)
        self.imagen.setPixmap(pixeles)
        self.imagen.setScaledContents(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.imagen)
        #Se agregan labels para mostrar jugadores conectados (max de 30)
        for i in range(30):
            self.puesto = QLabel('', self)
            self.puesto.setGeometry(0,i*20+200,200,20)
            vbox.addWidget(self.puesto)
            self.puestos.append(self.puesto)
    
    def actualizar_usernames(self, username, usernames):
        #Cuando recibe esta señal es porque un jugador se conectó o desconectó, se actualiza
        self.username, self.usernames = username, usernames
        for i in range(30):
            self.puestos[i].setText('')

        for i in range(len(self.usernames)):
            if self.usernames[i] == self.username:
                self.puestos[i].setText(self.usernames[i]+' (tú)')
            else:
                self.puestos[i].setText(self.usernames[i])


path_sprites = json_deserializado['path sprites']
    
class ventana_final(QWidget):
    senal_ventana_final = pyqtSignal(tuple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.init_gui()
        self.senal_ventana_final.connect(self.mostrar_ventana_final)
        self.senal_cerrar_ventana_juego = None

    
    def init_gui(self):
        self.setWindowTitle('DCColonos')
        self.setGeometry(400, 100, 300, 600)
        #Se pone el fondo
        self.imagen = QLabel(self)
        self.imagen.setGeometry(0,0,300,300)
        ruta_imagen = os.path.join(path_sprites,'Otros\Logo_fondo.png')
        pixeles = QPixmap(ruta_imagen)
        self.imagen.setPixmap(pixeles)
        self.imagen.setScaledContents(True)

        #Se crea un label que contendrá el resultado de la partida
        self.label_resultado = QLabel('RESULTADO', self)
        self.label_resultado.setGeometry(50, 50, 200, 50)
        self.label_resultado.setStyleSheet("background-color: white")
        self.label_resultado.setFont(QFont('Arial', 25))
        #label que mostrará el nombre del ganador
        self.label_ganador = QLabel('ganador: nombre ganador', self)
        self.label_ganador.setGeometry(50, 100, 200, 50)
        self.label_ganador.setStyleSheet("background-color: white")
        #botón para salir del programa
        self.botonSalir = QPushButton('&Salir', self)
        self.botonSalir.setGeometry(200,500,80,50)
        self.botonSalir.clicked.connect(self.salir)

        #Se crean los labels de los puestos
        self.label_puestos = []
        for i in range(3):
            self.lugar = QLabel('', self)
            self.lugar.setGeometry(50, 300 + 50*i, 300, 50)
            self.label_puestos.append(self.lugar)
        

    
    def salir(self):
        #Se cierran las pestañas abiertas y termina el programa
        self.senal_cerrar_ventana_juego.emit()
        self.close()
    
    def mostrar_ventana_final(self, resultado):
        #Cuando se recibe la señal, se actualizan las labels para mostrar el resultado
        #y se muestra la ventana
        self.label_resultado.setText(resultado[0])
        self.label_ganador.setText(f'ganador: {resultado[1]}')
        puestos = resultado[2]
        for i in range(len(puestos)):
            self.label_puestos[i].setText(f'lugar {i+1}: {puestos[i]}')

        self.show()

#Ventana que aparece en caso de que el servidor se desconecte
class ventana_desconexion(QWidget):
    senal_desconexion = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.init_gui()
        self.senal_desconexion.connect(self.mostrar_ventana_desconexion)
        self.senal_cerrar_ventana_juego = None

    
    def init_gui(self):
        self.setWindowTitle('DCColonos')
        self.setGeometry(400, 400, 300, 300)
        #Se pone el fondo
        self.imagen = QLabel(self)
        self.imagen.setGeometry(0,0,300,300)
        ruta_imagen = os.path.join(path_sprites,'Otros\Logo_fondo.png')
        pixeles = QPixmap(ruta_imagen)
        self.imagen.setPixmap(pixeles)
        self.imagen.setScaledContents(True)

        #Se crea un label con el problema
        self.label_resultado = QLabel('El servidor se\nha desconectado', self)
        self.label_resultado.setGeometry(10, 10, 280, 150)
        self.label_resultado.setStyleSheet("background-color: white")
        self.label_resultado.setFont(QFont('Arial', 25))
        #label que mostrará la explicación
        self.label_explicacion = QLabel('Hubo una falla inesperada, lamentamos el problema', self)
        self.label_explicacion.setGeometry(10, 160, 280, 50)
        self.label_explicacion.setStyleSheet("background-color: white")
        #botón para salir del programa
        self.botonSalir = QPushButton('&Salir', self)
        self.botonSalir.setGeometry(75,245,150,50)
        self.botonSalir.clicked.connect(self.salir)
    
    def salir(self):
        #Se cierra la ventana y termina el juego
        self.close()
    
    def mostrar_ventana_desconexion(self):
        self.show()
        #Se cierra la ventana de juego
        self.senal_cerrar_ventana_juego.emit()
        