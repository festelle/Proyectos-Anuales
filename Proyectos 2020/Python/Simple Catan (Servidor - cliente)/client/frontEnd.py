import sys
import os
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QTimer, QRect, QObject
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout,\
     QVBoxLayout, QComboBox, QProgressBar)
from PyQt5.QtGui import QPixmap
import json
from classMapa import class_mapa
from classMapa import agregar_imagen
import random

#Se importan los parámetros
with open('parametros.json',) as file:
    json_deserializado = json.load(file)
path_sprites = json_deserializado['path sprites']


class ventana_juego(QWidget):
    senal_comenzar_juego = pyqtSignal(str)
    senal_actualizar_mapa = pyqtSignal(object)
    senal_actualizar_jugadores = pyqtSignal(list)
    senal_habilitar_turno = pyqtSignal()
    senal_juego_terminado = pyqtSignal(tuple)
    senal_cerrar_ventana_juego = pyqtSignal()
    senal_actualizar_turno = pyqtSignal(str)
    senal_permitir_acciones = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.senal_comenzar_juego.connect(self.comenzar_juego)
        self.senal_esconder_sala = None
        self.senal_actualizar_mapa.connect(self.actualizar_mapa)
        self.senal_actualizar_jugadores.connect(self.actualizar_jugadores)
        self.senal_habilitar_turno.connect(self.habilitar_turno)
        self.senal_permitir_acciones.connect(self.permitir_acciones)
        self.senal_juego_terminado.connect(self.juego_terminado)
        self.mapa = None
        self.jugador = None
        self.jugadores_ya_creados = False
        self.senal_accion_jugador = None
        self.senal_ventana_final = None
        self.senal_cerrar_ventana_juego.connect(self.close)
        self.senal_actualizar_turno.connect(self.actualizar_turno)

        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle('DCColonos')
        self.setGeometry(100, 100, 800, 600)
        
        self.casilla1 = QLabel('', self)
        self.casilla1.setGeometry(545,10,260,580)
        self.casilla1.setStyleSheet("background-color: lightblue")

        self.labels_hexagonos = class_mapa().crear_base_mapa(self)

        #Se crean labels para los números de cada hexágono
        self.labels_numeros = []
        for i in range(len(self.labels_hexagonos)):
            label = QLabel('numero', self)
            label.setGeometry(0,0,40,40)
            label.setAlignment(Qt.AlignCenter)
            self.labels_numeros.append(label)

        #Se crean labels de base para cada jugador (4 jugadores max)
        self.info_jugadores = {} #dict con key cada jugador y con value una lista
        #de la forma [label_nombre, label_puntaje, lista labels materiales, jugador]

        self.label_nombre_propio = QLabel('JUGADOR', self)
        self.label_nombre_propio.setGeometry(10,500,200,30)
        self.puntaje_propio = QLabel('---', self)
        self.puntaje_propio.setGeometry(160,500,200,30)
        self.info_jugadores['jugador'] = [self.label_nombre_propio, self.puntaje_propio]

        self.label_jugador1 = QLabel('--', self)
        self.label_jugador1.setGeometry(550,60,200,30)
        self.puntaje_jugador1 = QLabel('---', self)
        self.puntaje_jugador1.setGeometry(700,60,200,30)
        self.info_jugadores['enemigo 1'] = [self.label_jugador1, self.puntaje_jugador1]

        self.label_jugador2 = QLabel('--', self)
        self.label_jugador2.setGeometry(550,200,200,30)
        self.puntaje_jugador2 = QLabel('---', self)
        self.puntaje_jugador2.setGeometry(700,200,200,30)
        self.info_jugadores['enemigo 2'] = [self.label_jugador2, self.puntaje_jugador2]

        self.label_jugador3 = QLabel('--', self)
        self.label_jugador3.setGeometry(550,340,200,30)
        self.puntaje_jugador3 = QLabel('---', self)
        self.puntaje_jugador3.setGeometry(700,340,200,30)
        self.info_jugadores['enemigo 3'] = [self.label_jugador3, self.puntaje_jugador3]

        #Se agregan las imágenes y labels de materia prima para cada jugador
        self.materias_jugadores = {}
        for jugador in self.info_jugadores.keys():
            nombre = self.info_jugadores[jugador][0] #Nombre es el label donde va el nombre
            self.imagen_arcilla = agregar_imagen(self, os.path.join(path_sprites,\
                'Materias_primas','carta_arcilla'), nombre.x(), nombre.y() + 40, 40, 60)
            self.label_arcilla = QLabel('--', self)
            self.label_arcilla.setGeometry(nombre.x()+50,nombre.y()+40,30,30)

            self.imagen_madera = agregar_imagen(self, os.path.join(path_sprites,\
                'Materias_primas','carta_madera'), nombre.x() + 80, nombre.y() + 40, 40, 60)
            self.label_madera = QLabel('--', self)
            self.label_madera.setGeometry(nombre.x()+130,nombre.y()+40,30,30)

            self.imagen_trigo = agregar_imagen(self, os.path.join(path_sprites,\
                'Materias_primas','carta_trigo'), nombre.x() + 160, nombre.y() + 40, 40, 60)
            self.label_trigo = QLabel('--', self)
            self.label_trigo.setGeometry(nombre.x()+210,nombre.y()+40,30,30)

            #Se agrega una lista a la info de cada jugador con los labels respectivos
            self.info_jugadores[jugador].append([self.label_arcilla, self.label_madera,\
                 self.label_trigo])
        
        #Se muestra las imágenes de los dados y botón para interactuar
        self.imagen_dado1 = agregar_imagen(self, os.path.join(path_sprites, 'Dados', 'dado_1'),\
            490, 540, 50, 50)
        self.imagen_dado2 = agregar_imagen(self, os.path.join(path_sprites, 'Dados', 'dado_1'),\
            435, 540, 50, 50)
        self.boton_dados = QPushButton('&Rodar dados', self)
        self.boton_dados.setGeometry(435, 500, 80, 30)
        self.boton_dados.clicked.connect(self.rodar_dados)
        self.boton_dados.setEnabled(False)
        #Se muestra botón para poder pasar turno en caso de que no se quiera hacer nada
        self.boton_terminar_turno = QPushButton('&Terminar turno', self)
        self.boton_terminar_turno.setGeometry(435, 10, 80, 30)
        self.boton_terminar_turno.clicked.connect(self.terminar_turno)
        self.boton_terminar_turno.setEnabled(False)
        #Se dibujan los nodos del mapa
        self.label_nodos = class_mapa().dibujar_nodos(self)
        #Se agrega label para mostrar el jugador que tiene el turno actual
        self.label_turno = QLabel('turno: ---', self)
        self.label_turno.setGeometry(10,10,200,30)

        #Se agrega selector para poder comprar una choza
        self.label_compra = QLabel('Comprar una choza:', self)
        self.label_compra.setGeometry(550,445,100,30)
        self.selector_choza = QComboBox(self)
        self.selector_choza.move(650,450)
        self.selector_choza.show()
        #Botón para poder comprar una choza
        self.boton_comprar_choza = QPushButton('&Comprar choza', self)
        self.boton_comprar_choza.setGeometry(560, 480, 150, 30)
        self.boton_comprar_choza.clicked.connect(self.comprar_choza)
        self.boton_comprar_choza.setEnabled(False)

        #Se agrega selector para poder comprar una carretera
        self.label_compra_carretera = QLabel('Comprar carretera:', self)
        self.label_compra_carretera.setGeometry(550,525,100,30)
        self.selector_carretera = QComboBox(self)
        self.selector_carretera.move(650,530)
        #Botón para poder comprar una choza
        self.boton_comprar_carretera = QPushButton('&Comprar carretera', self)
        self.boton_comprar_carretera.setGeometry(560, 560, 150, 30)
        #self.boton_comprar_carretera.clicked.connect(self.comprar_carretera)
        self.boton_comprar_carretera.setEnabled(False)

        #Se agrega selector para poder comprar una carretera
        self.label_intercambiar = QLabel('Intercambiar con:', self)
        self.label_intercambiar.setGeometry(250,475,100,30)
        self.selector_intercambiar = QComboBox(self)
        self.selector_intercambiar.move(350,480)
        #Botón para poder comprar una choza
        self.boton_intercambiar = QPushButton('&Intercambiar', self)
        self.boton_intercambiar.setGeometry(260, 505, 150, 30)
        #self.boton_intercambiar.clicked.connect(self.intercambiar)
        self.boton_intercambiar.setEnabled(False)

        #Se agrega botón para comprar cartas
        self.boton_comprar_carta = QPushButton('&Comprar carta', self)
        self.boton_comprar_carta.setGeometry(260, 560, 150, 30)
        #self.boton_comprar_carta.clicked.connect(self.comprar_carta)
        self.boton_comprar_carta.setEnabled(False)

        



    def comenzar_juego(self, username):
        self.show()
        self.senal_esconder_sala.emit()
        self.username = username
    
    def actualizar_mapa(self, mapa):
        #Actualiza los nodos (mostrando chozas de sus dueños si está ocupado)
        #Actualiza los hexágonos y el selector de nodos disponibles para comprar
        self.mapa = mapa
        self.mapa.actualizar_nodos(self.label_nodos)
        self.mapa.agregar_hexagonos(self, self.labels_hexagonos, self.labels_numeros)
        self.actualizar_selector_choza()

        
    def actualizar_selector_choza(self):
        #Agrega los nodos que el jugador puede comprar teniendo en cuenta la
        #restricción de que dos chozas no pueden estar juntas
        self.selector_choza.clear()
        for id_nodo in self.mapa.nodos.keys():
            agregar = True
            if self.mapa.nodos[id_nodo].estado_actual == 'libre':
                if self.jugador is not None:
                    for nodo_jugador in self.jugador.chozas_nodos.values():
                        for vecino in nodo_jugador.vecinos:
                            if vecino.id == id_nodo:
                                agregar = False
                if agregar:
                    self.selector_choza.addItem(id_nodo)
        
        if self.selector_choza.count() == 0:
            self.boton_comprar_choza.setEnabled(False)
    
    def actualizar_turno(self, nombre):
        #Muestra el nuevo jugador que tiene el turno
        self.label_turno.setText(f'turno: {nombre}')

    def actualizar_jugadores(self, lista_jugadores):
        #Se elimina la info de jugadores que actualmente estaba guardada
        for info_jugador in self.info_jugadores.keys():
            if len(self.info_jugadores[info_jugador]) >= 4:
                self.info_jugadores[info_jugador].pop()

        #Se vuelve a poner cada nombre e info en el caso de que alguien se haya desconectado
        for jugador in lista_jugadores:
            if jugador.username == self.username:
                self.jugador = jugador
                self.actualizar_selector_choza()
                
                label_nombre = self.info_jugadores['jugador'][0]
                label_nombre.setText(f'{self.username} ({jugador.color})')
                label_puntaje = self.info_jugadores['jugador'][1]
                label_puntaje.setText(f'PUNTAJE: {jugador.puntos_victoria}')
                self.info_jugadores['jugador'].append(jugador)
                #Se cambian los labels del jugador
                self.info_jugadores['jugador'][2][0].setText(f'x {jugador.arcilla}')
                self.info_jugadores['jugador'][2][1].setText(f'x {jugador.madera}')
                self.info_jugadores['jugador'][2][2].setText(f'x {jugador.trigo}')

            else:
                if len(self.info_jugadores['enemigo 1']) < 4:
                    label_nombre = self.info_jugadores['enemigo 1'][0]
                    label_nombre.setText(f'{jugador.username} ({jugador.color})')
                    label_puntaje = self.info_jugadores['enemigo 1'][1]
                    label_puntaje.setText(f'PUNTAJE: {jugador.puntos_victoria}')
                    self.info_jugadores['enemigo 1'].append(jugador)
                    #Se cambian los labels de materia prima
                    self.info_jugadores['enemigo 1'][2][0].setText(f'x {jugador.arcilla}')
                    self.info_jugadores['enemigo 1'][2][1].setText(f'x {jugador.madera}')
                    self.info_jugadores['enemigo 1'][2][2].setText(f'x {jugador.trigo}')
                
                elif len(self.info_jugadores['enemigo 2']) < 4:
                    label_nombre = self.info_jugadores['enemigo 2'][0]
                    label_nombre.setText(f'{jugador.username} ({jugador.color})')
                    label_puntaje = self.info_jugadores['enemigo 2'][1]
                    label_puntaje.setText(f'PUNTAJE: {jugador.puntos_victoria}')
                    self.info_jugadores['enemigo 2'].append(jugador)

                    self.info_jugadores['enemigo 2'][2][0].setText(f'x {jugador.arcilla}')
                    self.info_jugadores['enemigo 2'][2][1].setText(f'x {jugador.madera}')
                    self.info_jugadores['enemigo 2'][2][2].setText(f'x {jugador.trigo}')

                elif len(self.info_jugadores['enemigo 3']) < 4:
                    label_nombre = self.info_jugadores['enemigo 3'][0]
                    label_nombre.setText(f'{jugador.username} ({jugador.color})')
                    label_puntaje = self.info_jugadores['enemigo 3'][1]
                    label_puntaje.setText(f'PUNTAJE: {jugador.puntos_victoria}')
                    self.info_jugadores['enemigo 3'].append(jugador)

                    self.info_jugadores['enemigo 3'][2][0].setText(f'x {jugador.arcilla}')
                    self.info_jugadores['enemigo 3'][2][1].setText(f'x {jugador.madera}')
                    self.info_jugadores['enemigo 3'][2][2].setText(f'x {jugador.trigo}')

        #Si alguien se desconecta, se cambia la etiqueta
        if len(lista_jugadores) == 1:
            if 'enemigo 1' in self.info_jugadores:
                self.info_jugadores['enemigo 1'][0].setText('---')
            if 'enemigo 2' in self.info_jugadores:
                self.info_jugadores['enemigo 2'][0].setText('---')
            if 'enemigo 3' in self.info_jugadores:
                self.info_jugadores['enemigo 3'][0].setText('---')

        if len(lista_jugadores) == 2:
            if 'enemigo 2' in self.info_jugadores:
                self.info_jugadores['enemigo 2'][0].setText('---')
            if 'enemigo 3' in self.info_jugadores:
                self.info_jugadores['enemigo 3'][0].setText('---')
        if len(lista_jugadores) == 3:
            if 'enemigo 1' in self.info_jugadores:
                self.info_jugadores['enemigo 3'][0].setText('---')


        #Si hay menos de 4 jugadores o alguien se haya desconectado, se elimina
        if not self.jugadores_ya_creados:
            if len(self.info_jugadores['enemigo 1']) < 4:
                del self.info_jugadores['enemigo 1']
                del self.info_jugadores['enemigo 2'] 
                del self.info_jugadores['enemigo 3']
            elif len(self.info_jugadores['enemigo 2']) < 4:
                del self.info_jugadores['enemigo 2'] 
                del self.info_jugadores['enemigo 3']
            elif len(self.info_jugadores['enemigo 3']) < 4:
                del self.info_jugadores['enemigo 3']
        
        self.jugadores_ya_creados = True
    
    def habilitar_turno(self):
        #Una vez que es el turno del jugador, se habilita el botón de dados para que juegue
        self.boton_dados.setEnabled(True)
        
    def rodar_dados(self, materia_suficiente):
        #Se eligen números al azar, se muestra el resultado
        dado1 = random.randint(1,6)
        dado2 = random.randint(1,6)
        resultado = dado1 + dado2
        pixmap1 = QPixmap(os.path.join(path_sprites, 'Dados', f'dado_{dado1}'))
        pixmap2 = QPixmap(os.path.join(path_sprites, 'Dados', f'dado_{dado2}'))
        self.imagen_dado1.setPixmap(pixmap1)
        self.imagen_dado2.setPixmap(pixmap2)
        #Se manda el resultado al backEnd
        accion = ('rodar dados', resultado)
        self.senal_accion_jugador.emit(accion)
        self.boton_dados.setEnabled(False)

    def permitir_acciones(self, habilitar_compra_choza):
        #Se habilitan las opciones que tiene el jugador una vez llegue la señal
        #que indica si está habilitado para comprar una choza o no
        self.boton_terminar_turno.setEnabled(True)
        if habilitar_compra_choza:
            self.boton_comprar_choza.setEnabled(True)
    
    def comprar_choza(self):
        #Se manda la señal para procesar la compra y se termina el turno
        id_nodo = str(self.selector_choza.currentText())
        self.senal_accion_jugador.emit(('comprar choza', id_nodo))
        self.terminar_turno()

    def terminar_turno(self):
        #Se deshabilita todos los botones de acción que tiene el jugador
        self.boton_dados.setEnabled(False)
        self.boton_terminar_turno.setEnabled(False)
        self.boton_comprar_choza.setEnabled(False)
        self.senal_accion_jugador.emit(('turno terminado', ))
    
    def juego_terminado(self, tupla):
        #Se desactiva todo y manda señal para mostrar la ventana final
        self.terminar_turno()
        self.senal_ventana_final.emit(tupla)
        







            
        

        

    
