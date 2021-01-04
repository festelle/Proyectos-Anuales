import sys
import os
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QTimer, QRect
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QFont, QColor
import random
import time
from parametros import (DURACION_MUSICA, VELOCIDAD_FLECHA, PATH_FLECHAS, \
      PROB_NORMAL, PROB_FLECHA_X2, PROB_FLECHA_DORADA, PROB_FLECHA_HIELO, \
         PUNTOS_FLECHA, VELOCIDAD_FLECHA_BACKUP, PATH_RANKING, ALTO_FLECHA, ALTO_CAPTURA)


#EN ESTE ARCHIVO SE ENCUENTRA EL FRONT END DE LAS VENTANAS DE INICIO, RESUMEN, RANKING,
#ADEMÁS ESTÁ LA FUNCIÓN QUE CREA UN THREAD CON EL COMPORTAMIENTO DE UNA FLECHA.

class ventana_Inicio(QWidget):
    #señales para esconder la ventana (cuando se juegue) y actualizarla (advertencia y ranking)
    senal_esconder = pyqtSignal()
    senal_actualizar = pyqtSignal(str)
    senal_mostrar = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.init_gui()
        self.senal_procesar = None #manda orden a logica para comenzar juego o mostrar ranking
        self.senal_esconder.connect(self.hide)
        self.senal_actualizar.connect(self.actualizar_pantalla)
        self.senal_mostrar.connect(self.volver_a_inicio)

    def init_gui(self):
        #Se crea la ventana inicial
        self.setWindowTitle('DCCumbia')
        self.setGeometry(100, 100, 300, 300)
        self.labelNombre = QLabel('Nombre jugador:', self)
        self.editNombre = QLineEdit('', self)
        self.editNombre.resize(100, 20)
        self.labelAdvertencia = QLabel('', self)
        #Se crea y conecta el botón para jugar y botón para ver ranking
        self.botonJugar = QPushButton('&Jugar', self)
        self.botonJugar.resize(self.botonJugar.sizeHint())
        self.botonJugar.clicked.connect(self.boton_clickeado)

        self.botonRanking = QPushButton('&Ver Ranking', self)
        self.botonRanking.resize(self.botonRanking.sizeHint())
        self.botonRanking.clicked.connect(self.boton_clickeado)
        #Se hacen layouts para ordenar mejor la información
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.labelNombre)
        hbox.addWidget(self.editNombre)
        hbox.addWidget(self.botonJugar)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.labelAdvertencia)
        vbox.addWidget(self.botonRanking)
        self.setLayout(vbox)
    
    def boton_clickeado(self):
        #Se manda una tupla forma (orden, mensaje) =  orden: 0:Nombre   1: Ranking
        sender = self.sender()
        if sender == self.botonJugar:
            nombre = self.editNombre.text()
            self.senal_procesar.emit((0,nombre))
        else:
            self.senal_procesar.emit((1,'mostrar ranking'))
            
    def actualizar_pantalla(self, mensaje):
        self.labelAdvertencia.setText(mensaje)
    
    def volver_a_inicio(self):
        self.editNombre.setText('')
        self.show()

class thread_flechas(QThread):
    senal_actualizar = pyqtSignal(QLabel, int, int)
    senal_cambiar_color = pyqtSignal(int)
    senal_reiniciar_combo = pyqtSignal()
    #posicion_x: qué carril es limite_y: hasta qué altura va a "bajar" (en verdad subir)
    def __init__(self, parent, posicion_x, limite_y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo_flecha = random.uniform(0,1) #tipo de flecha que será
        #Dependiendo del tipo de flecha, se entrega la imagen a usar
        self.imagen_flecha = 0
        if self.tipo_flecha <= PROB_NORMAL:
            self.tipo_flecha = 'flecha normal'
            self.imagen_flecha = 5
            self.puntaje_a_obtener = 1
        elif PROB_NORMAL <self.tipo_flecha <= PROB_FLECHA_X2 + PROB_NORMAL:
            self.tipo_flecha = 'flecha X2'
            self.imagen_flecha = 1
            self.puntaje_a_obtener = 2
        elif PROB_NORMAL + PROB_FLECHA_X2 <self.tipo_flecha <= PROB_FLECHA_DORADA + PROB_NORMAL +\
                 PROB_FLECHA_X2:
            self.tipo_flecha = 'flecha dorada'
            self.imagen_flecha = 2
            self.puntaje_a_obtener = 10
        elif PROB_NORMAL+PROB_FLECHA_X2+PROB_FLECHA_DORADA <self.tipo_flecha <= 1:
            self.tipo_flecha = 'flecha hielo'
            self.imagen_flecha = 6
            self.puntaje_a_obtener = 1

        #Se crea la imagen dependiendo del carril de la flecha
        if posicion_x ==7:
            ruta_flecha = os.path.join(PATH_FLECHAS,f'left_{self.imagen_flecha}')
        elif posicion_x == 7+ALTO_CAPTURA:
            ruta_flecha = os.path.join(PATH_FLECHAS,f'up_{self.imagen_flecha}')
        elif posicion_x == 7+ALTO_CAPTURA*2:
            ruta_flecha = os.path.join(PATH_FLECHAS,f'down_{self.imagen_flecha}')
        elif posicion_x == 7+ALTO_CAPTURA*3:
            ruta_flecha = os.path.join(PATH_FLECHAS,f'right_{self.imagen_flecha}')

        self.flecha = QLabel(parent)
        self.flecha.setGeometry(posicion_x,100,ALTO_FLECHA,ALTO_FLECHA)
        self.flecha.setPixmap(QPixmap(ruta_flecha))
        self.flecha.setScaledContents(True)
        self.flecha.setVisible(True)
        
        self.posicion_x = posicion_x
        self.limite_y = limite_y
        self.pausar_flecha = False
        self.__posicion = (self.posicion_x, 100)
        #escondida es para saber si dar puntaje o no en caso de que se apriete la tecla
        self.escondida = False
        #Boolenao para que no se emtan muchas señales despues de que se termine el contacto
        self.ya_cambio_color = False
        #Se crea timer para bajar la velocidad en caso de la flecha de hielo
        self.timer_bajar_velocidad = QTimer(self)
        self.timer_bajar_velocidad.setInterval(DURACION_MUSICA * 0.2)
        self.timer_bajar_velocidad.timeout.connect(self.congelar_flechas)
        self.flechas_congeladas = False
        self.contador_congelacion = 0

        self.flecha.show()
        self.start() #Se comienza el thread

    @property
    def posicion(self): 
        return self.__posicion
    @posicion.setter
    def posicion(self,valor): #Cada vez que haya un cambio se llamará al juego para mover la flecha
        self.__posicion = valor
        self.senal_actualizar.emit(self.flecha, *self.posicion)
        
    def run(self):
        while self.posicion[1] < self.limite_y:

            if not self.pausar_flecha:
                
                time.sleep(0.1)
                #Comportamiento depende del tipo de flecha
                if self.tipo_flecha == 'flecha normal':
                    nuevo_y = self.posicion[1]+VELOCIDAD_FLECHA/10
                    self.posicion = (self.posicion_x, nuevo_y)
                elif self.tipo_flecha == 'flecha X2':
                    nuevo_y = self.posicion[1]+VELOCIDAD_FLECHA/10
                    self.posicion = (self.posicion_x, nuevo_y)
                elif self.tipo_flecha == 'flecha dorada':
                    nuevo_y = self.posicion[1]+VELOCIDAD_FLECHA/10 * 1.5
                    self.posicion = (self.posicion_x, nuevo_y)
                elif self.tipo_flecha == 'flecha hielo':
                    nuevo_y = self.posicion[1]+VELOCIDAD_FLECHA/10
                    self.posicion = (self.posicion_x, nuevo_y)
                    self.descongelar_flechas() #función para bajar la velocidad de las flechas
                
                #Se revisa si hay contacto con cuadrado de carril
                if  516-ALTO_FLECHA<= self.posicion[1]<= 516+ALTO_CAPTURA and not self.escondida:
                    self.senal_cambiar_color.emit(self.posicion_x)
                    
                #Si hubo contacto y por primera vez no hay, se vuelve a cambiar el color del carril
                elif self.posicion[1] > 516+ ALTO_CAPTURA and not self.ya_cambio_color:
                    self.senal_cambiar_color.emit(self.posicion_x+1)
                    self.ya_cambio_color = True
                    self.escondida = True
                    self.senal_reiniciar_combo.emit()
                #En caso de que ya presionaron la tecla para eliminar la flecha, se vuelve el color
                elif self.escondida and not self.ya_cambio_color:
                    self.senal_cambiar_color.emit(self.posicion_x+1)
                    self.ya_cambio_color = True


                
            
            elif self.pausar_flecha:
                pass


    def congelar_flechas(self):
        global VELOCIDAD_FLECHA
        VELOCIDAD_FLECHA = VELOCIDAD_FLECHA/2
        self.flechas_congeladas = True

    def descongelar_flechas(self): #descongela las flechas después de un tiempo definido
        global VELOCIDAD_FLECHA
        global DURACION_MUSICA
        if self.flechas_congeladas:
            self.contador_congelacion += 1
            #Se agrega alcance para que no se termine el thread antes de que se descongele
            self.limite_y += 100 
            if self.contador_congelacion >= DURACION_MUSICA * 0.2 * 10:
                self.limite_y = self.posicion[1]
                VELOCIDAD_FLECHA = VELOCIDAD_FLECHA * 2
                self.flechas_congeladas = False


class ventana_resumen(QWidget):
    senal_mandar_ranking = pyqtSignal()
    senal_mostrar_resumen = pyqtSignal( int, int, int, int, int) 
    #(puntaje acumulado, puntaje ronda, combo max, pasos fallados, porcentaje aprob)
    senal_nombre = pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()
        self.nombre = ''
        self.puntaje_acumulado = 0

        self.senal_nombre.connect(self.definir_nombre)
        self.senal_mostrar_resumen.connect(self.actualizar_ventana)
        self.senal_esconder_juego = None #manda señal a ventana Juego para que se esconda
        self.senal_reiniciar_logica_juego = None #señala a logicaJuego reiniciar todos parametros
        self.senal_menu_inicio = None #señal para mostrar al ventana de inicio
        self.senal_siguiente_ronda = None #senal a logica juego para reiniciar algunos parámetros
        self.senal_escribir_ranking = None #senal a su backend para guardar el puntaje.
        self.senal_mandar_ranking.connect(self.mandar_ranking)
        
    def init_gui(self):
        #Se crea la ventana
        self.setWindowTitle('Resumen partida DCCumbia')
        self.setGeometry(100, 100, 300, 300)
        self.labelNombre = QLabel(f'Jugador: ', self)
        self.label_acumulado = QLabel(f'Puntaje acumulado: ', self)
        self.label_puntaje = QLabel(f'Puntaje ronda:', self)
        self.label_combo = QLabel(f'Combo máximo:', self)
        self.label_fallados = QLabel(f'Pasos fallados:', self)
        self.label_aprobacion = QLabel(f'% Aprobación:', self)
        self.label_juzgar = QLabel(f'Felicidades! Puedes pasar a la siguiente ronda', self)
        

        #Se crea y conecta el botón para jugar y para salir
        self.botonJugar = QPushButton('&Jugar', self)
        self.botonJugar.resize(self.botonJugar.sizeHint())
        self.botonJugar.clicked.connect(self.pasar_siguiente_ronda)

        self.botonSalir = QPushButton('&Salir', self)
        self.botonSalir.resize(self.botonSalir.sizeHint())
        self.botonSalir.clicked.connect(self.closeEvent)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.botonJugar)
        hbox.addWidget(self.botonSalir)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.labelNombre)
        vbox.addWidget(self.label_acumulado)
        vbox.addWidget(self.label_puntaje)
        vbox.addWidget(self.label_combo)
        vbox.addWidget(self.label_fallados)
        vbox.addWidget(self.label_aprobacion)
        vbox.addWidget(self.label_juzgar)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def definir_nombre(self, nombre):
        self.nombre = nombre #Cada vez que se cambia el nombre se reinicia todo
        self.puntaje_acumulado = 0
        self.senal_reiniciar_logica_juego.emit()
        
    def closeEvent(self, a0):
        #Si se quiere salir se guarda el puntaje
        self.senal_escribir_ranking.emit(self.nombre, self.puntaje_acumulado)
        self.puntaje_acumulado = 0
        self.senal_reiniciar_logica_juego.emit()
        self.senal_menu_inicio.emit()
        self.senal_esconder_juego.emit()
        self.close()

    def pasar_siguiente_ronda(self):
        self.senal_siguiente_ronda.emit()
        self.hide()

    def mandar_ranking(self):
        self.senal_escribir_ranking.emit(self.nombre, self.puntaje_acumulado)

    def actualizar_ventana(self,puntaje, max_combos, pasos_fallados, aprobacion, APROBACION_NECESARIA):
        
        self.puntaje_acumulado += puntaje
        
        self.labelNombre.setText(f'Jugador: {self.nombre}')
        self.label_acumulado.setText(f'Puntaje acumulado: {self.puntaje_acumulado}')
        self.label_puntaje.setText(f'Puntaje ronda: {puntaje}')
        self.label_combo.setText(f'Combo máximo: {max_combos}')
        self.label_fallados.setText(f'Pasos fallados: {pasos_fallados}')
        self.label_aprobacion.setText(f'% Aprobación: {aprobacion}')
    
        if aprobacion >= APROBACION_NECESARIA:
            self.label_juzgar.setText(f'Felicidades! Puedes pasar a la siguiente ronda')
            self.botonJugar.setEnabled(True)
        elif aprobacion < APROBACION_NECESARIA:
            self.label_juzgar.setText(f'No alcanzaste la aprobación mínima y te echaron!')
            self.botonJugar.setEnabled(False)

        self.show()

class ventana_ranking(QWidget):
    senal_mostrar_ranking = pyqtSignal(list)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()
        self.senal_mostrar_ranking.connect(self.actualizar_rankings)

    def init_gui(self):
        #Se crea la ventana
        self.setWindowTitle('Ranking DCCumbia')
        self.setGeometry(100, 100, 300, 300)
        self.label_titulo = QLabel('ranking DCCumbia', self)
        #Se crean 5 puestos para el top5
        self.label_1 = QLabel('', self)
        self.label_2 = QLabel('', self)
        self.label_3 = QLabel('', self)
        self.label_4 = QLabel('', self)
        self.label_5 = QLabel('', self)
        self.puestos = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5]

        self.botonSalir = QPushButton('&Volver', self)
        self.botonSalir.resize(self.botonSalir.sizeHint())
        self.botonSalir.clicked.connect(self.close)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_titulo)
        vbox.addStretch(1)
        for label in self.puestos:
            vbox.addWidget(label)
        vbox.addStretch(1)
        vbox.addWidget(self.botonSalir)
        self.setLayout(vbox)
    
    def actualizar_rankings(self,puntajes_ordenados):
        puesto = 0
        for puntaje in puntajes_ordenados:
            if puntaje != ['','']: #Si puntaje no es vacío, se muestra
                self.puestos[puesto].setText(f'{puntaje[1]}: {puntaje[0]}')
                puesto += 1
            else:
                self.puestos[puesto].setText('')
        if self.puestos[0].text()=='':
            self.puestos[0].setText('No hay puntajes guardados :(')
        self.show()
        

        


    
    




