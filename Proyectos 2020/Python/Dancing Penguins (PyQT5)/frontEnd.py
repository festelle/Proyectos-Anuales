import sys
import os
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QTimer, QRect
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout,\
     QVBoxLayout, QComboBox, QProgressBar)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QFont, QColor
import random
import time
from parametros import ( DURACION_MUSICA, VELOCIDAD_FLECHA, ALTO_PINGU,\
      PROB_NORMAL, PROB_FLECHA_X2, PROB_FLECHA_DORADA, PROB_FLECHA_HIELO, \
    PUNTOS_FLECHA, VELOCIDAD_FLECHA_BACKUP, CANCIONES, ALTO_FLECHA, ALTO_CAPTURA,\
         PRECIO_PINGU, PINGUINOS_NEUTROS, FLECHAS_BASICAS)

from frontEnd_2 import thread_flechas
from Clases_drap_drog import DragLabel,DropLabel,agregar_imagen,drag_imagen,crear_boton,label_texto

#EN ESTE ARCHIVO ESTÁ LA VENTANA JUEGO, QUE ES LA VENTANA PRINCIPAL DEL PROGRAMA

class ventana_juego(QWidget):
    senal_abrir_juego = pyqtSignal()
    senal_actualizar = pyqtSignal()
    senal_mover_pinguino = pyqtSignal(object)
    senal_reiniciar = pyqtSignal()
    senal_esconderse = pyqtSignal()
    senal_actualizar_combos = pyqtSignal(int, int, int)
    senal_actualizar_dinero = pyqtSignal(int)
    senal_descontar_dinero_paso_medio = pyqtSignal() #Paso medio para mandar la señal a backend
    senal_actualizar_progreso_cancion = pyqtSignal(int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.init_gui()
        #Cuando se cierre esconda la ventana de inicio, se abre esta
        self.senal_abrir_juego.connect(self.show) 
        self.senal_reiniciar.connect(self.reiniciar_parametros)
        self.senal_esconderse.connect(self.volver_inicio)
        self.senal_actualizar_combos.connect(self.actualizar_combos)
        self.senal_actualizar_dinero.connect(self.actualizar_dinero)
        self.senal_descontar_dinero_paso_medio.connect(self.descontar_dinero)
        self.senal_actualizar_progreso_cancion.connect(self.actualizar_progreso_cancion)
        self.senal_descontar_dinero = None #Manda a lógica para descontar el dinero de la compra
        self.senal_reiniciar_combo = None #Manda señal a lógica para devolver combo a 0
        self.senal_contacto_flecha = None #Manda a lógica para revisar si hay una flecha en carril
        self.senal_empezar_juego = None #Manda a lógica para que comience el timer de las flechas
        self.senal_mostrar_inicio = None #Manda a ventana inicio para que se vuelva a mostrar
        self.senal_juego_terminado = None #Manda a logica para analizar el puntaje y aprobacion
        self.senal_escribir_ranking = None #manda señal a logica resumen para guardar el puntaje
        self.senal_reiniciar_logica_juego = None #manda a logica para reiniciar los parametros
        self.senal_empezar_musica = None #manda a logica para empezar la reproduccion de la musica
        self.senal_parar_musica = None #manda a logica para parar la reproduccion de la musica
        self.senal_pausar_musica = None #manda a logica para pausar la reproduccion de la musica
        self.senal_trampa_dinero = None #Manda señal a logica para agregar dinero con el codigo
        self.senal_terminar_partida = None #señala a logica que se debe terminar la partida antes
        self.senal_parar_cronometro = None #manda señal a logica para parar el cronometro
        self.senal_volver_cronometro = None #manda señal a logica para reanudar el cronómetro
        #Timer encargado de crear las flechas y de controlar el tiempo
        self.flechas_creadas = 0
        self.timer_crear_flecha = QTimer(self)
        self.timer_crear_flecha.setInterval(1*1000)
        self.timer_crear_flecha.timeout.connect(self.creador_de_flechas)
        self.flechas = []
        #variables que controlan si se aprieta una tecla
        self.a_presionada = False
        self.w_presionada = False
        self.s_presionada = False
        self.d_presionada = False
        #Se agregan booleanos de teclas para poder saber cuándo se usa un código trampa
        self.tecla_m = False 
        self.tecla_o = False
        self.tecla_n = False
        self.tecla_i = False
        #Variable para la pista de baile
        self.pinguinos_en_pista = 0
        #variable que define la duraión de la música
        self.duracion_musica = 0

    def init_gui(self):
        global ALTO_PINGU
        #Se crea la ventana inicial
        self.setWindowTitle('DCCumbia')
        self.setGeometry(100, 100, 800, 600)
        #Se agrega la imagen de fondo
        ruta_imagen_fondo = os.path.join('sprites','fondos','fondo.png')
        self.fondo = agregar_imagen(self, ruta_imagen_fondo, 180,100,460,520)
        #Se agregan los fondos para las flechas
        self.casillas = []
        self.casilla1 = QLabel('', self)
        self.casilla1.setGeometry(5,516,ALTO_CAPTURA,ALTO_CAPTURA)
        self.casilla1.setStyleSheet("background-color: blue")
        self.casillas.append(self.casilla1)
        self.casilla2 = QLabel('', self)
        self.casilla2.setGeometry(5+ALTO_CAPTURA,516,ALTO_CAPTURA,ALTO_CAPTURA)
        self.casilla2.setStyleSheet("background-color: blue")
        self.casillas.append(self.casilla2)
        self.casilla3 = QLabel('', self)
        self.casilla3.setGeometry(5+ALTO_CAPTURA*2,516,ALTO_CAPTURA,ALTO_CAPTURA)
        self.casilla3.setStyleSheet("background-color: blue")
        self.casillas.append(self.casilla3)
        self.casilla4 = QLabel('', self)
        self.casilla4.setGeometry(5+ALTO_CAPTURA*3,516,ALTO_CAPTURA,ALTO_CAPTURA)
        self.casilla4.setStyleSheet("background-color: blue")
        self.casillas.append(self.casilla4)
        #Se agregan las flechas y label que explica los botones de cada una
        self.flecha1 = agregar_imagen(self, FLECHAS_BASICAS[0], 7,520,34,34)
        self.flecha2 = agregar_imagen(self, FLECHAS_BASICAS[1], 7+44,520,34,34)
        self.flecha3 = agregar_imagen(self, FLECHAS_BASICAS[2], 7+44*2,520,34,34)
        self.flecha4 = agregar_imagen(self, FLECHAS_BASICAS[3], 7+44*3,520,34,34)
        self.letras = QLabel('  A    W    S    D',self)
        self.letras.setFont(QFont('Arial', 15))
        self.letras.move(15,565)
        #Botón para empezar a jugar
        self.boton_juego = crear_boton('&Iniciar Juego', self, 700, 20, self.empezar_timer)
        #Se crea botón para volver al menu principal
        self.boton_salir = crear_boton('&Salir', self, 700,60,self.closeEvent)
        #botón para pausar
        self.boton_pausar = crear_boton('&Pausar', self, 50,60,self.pausar_juego)
        self.boton_pausar.setEnabled(False)
        self.juego_pausado = False
        #Se crea labels que llevará el tiempo del nivel, combo actual y máximo
        self.contador_puntaje = label_texto('TIEMPO:\n0',self,12,50,5,100,50)
        self.combo_actual = label_texto('combo actual: 0',self,10,200,30,150,20)
        self.combo_maximo = label_texto('combo máximo: 0', self,10,200,60,150,20)

        #barras de progreso con sus respectivas labels
        self.label_progreso = label_texto('Progreso:', self, 10, 370,30,100,20)
        self.barra_progreso_cancion = QProgressBar(self)
        self.barra_progreso_cancion.setGeometry(450,30,100,20)
        self.barra_progreso_cancion.setAlignment(Qt.AlignCenter)

        self.label_aprobacion = label_texto('Aprobación:', self, 10, 370,60,100,20)
        self.barra_aprobacion = QProgressBar(self)
        self.barra_aprobacion.setGeometry(450,60,100,20)
        self.barra_aprobacion.setAlignment(Qt.AlignCenter)

        #Se agrega el selector de dificultad
        self.selector_dificultad = QComboBox(self)
        self.selector_dificultad.move(600,20)
        self.selector_dificultad.show()
        self.selector_dificultad.addItem('Principiante')
        self.selector_dificultad.addItem('Aficionado')
        self.selector_dificultad.addItem('Maestro cumbia')

        self.selector_musica = QComboBox(self)
        self.selector_musica.move(600,60)
        self.selector_musica.show()
        for cancion in CANCIONES:
            self.selector_musica.addItem(cancion)

        #Se agregan los objetos en la zona de tienda
        self.titulo_tienda= QLabel('TIENDA',self)
        self.titulo_tienda.setFont(QFont('Arial', 15))
        self.titulo_tienda.move(685,120)
        self.label_dinero = QLabel('Dinero: 0', self)
        self.label_dinero.setFont(QFont('Arial', 10))
        self.label_dinero.setGeometry(655,170, 300, 30)
        self.label_precio= QLabel('Precio pinguirin: 500',self)
        self.label_precio.setFont(QFont('Arial', 10))
        self.label_precio.move(665,200)
        self.label_advertencia=QLabel('',self)
        self.label_advertencia.setFont(QFont('Arial', 10)) #Se muestra la advertencia
        self.label_advertencia.setGeometry(650,520,140,60) #en caso de que no hayan pinguirines
        
        self.pinguino_amarillo=drag_imagen(self,PINGUINOS_NEUTROS[0],650,250,ALTO_PINGU,ALTO_PINGU)
        self.pinguino_celeste=drag_imagen(self,PINGUINOS_NEUTROS[1],720,250,ALTO_PINGU,ALTO_PINGU)
        self.pinguino_morado=drag_imagen(self,PINGUINOS_NEUTROS[2],650,350,ALTO_PINGU,ALTO_PINGU)
        self.pinguino_rojo=drag_imagen(self, PINGUINOS_NEUTROS[3], 720,350,ALTO_PINGU,ALTO_PINGU)
        self.pinguino_verde=drag_imagen(self,PINGUINOS_NEUTROS[4], 650,450,ALTO_PINGU,ALTO_PINGU)
        self.label_pinguinos = [self.pinguino_rojo, self.pinguino_amarillo, self.pinguino_celeste,\
             self.pinguino_morado, self.pinguino_verde]   
        self.drop_labels = []
        for j in range(3): #Se crea el grid con los posibles lugares para dejar a los pinguinos
            for i in range(4):
                self.drop_label = DropLabel(self, self.senal_descontar_dinero_paso_medio)
                self.drop_label.setGeometry(250+i*ALTO_PINGU,375+j*ALTO_PINGU,ALTO_PINGU,ALTO_PINGU)
                self.drop_labels.append(self.drop_label)

    def paintEvent(self,e):  #Se dibujan cuadrados de fondo
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.cyan, Qt.SolidPattern))
        painter.drawRect(4,100,172,495,)
        painter.drawRect(4+640,100,152,495,)
        painter.drawRect(0,4,800,88,) 

    def keyPressEvent(self, event):
        texto = event.text().lower()
        if self.boton_pausar.isEnabled(): #Si se puede pausar, se asume que se está jugando
            if texto == 'p': #se pausa
                self.pausar_juego()
            #Se revisa si se quiere usar el código para parar la partida
            if texto == 'n':
                self.tecla_n = True
            elif texto == 'i' and self.tecla_n and not self.tecla_i:
                self.tecla_i = True
            elif texto == 'v' and self.tecla_i and self.tecla_n:
                print('código activado')
                self.tecla_n = False
                self.tecla_i = False
                self.senal_terminar_partida.emit()
            else:
                self.tecla_n = False
                self.tecla_i = False

        if not self.juego_pausado: #Si el juego no está pausado, se reciben estos eventos
            if texto =='a' and not self.a_presionada:
                self.senal_contacto_flecha.emit(self.flechas, texto)
                self.a_presionada = True
            if texto =='w' and not self.w_presionada:
                self.senal_contacto_flecha.emit(self.flechas, texto)
                self.w_presionada = True
            if texto =='s' and not self.s_presionada:
                self.senal_contacto_flecha.emit(self.flechas, texto)
                self.s_presionada = True
            if texto =='d' and not self.d_presionada:
                self.senal_contacto_flecha.emit(self.flechas, texto)
                self.d_presionada = True

    def keyReleaseEvent(self, event): 
        texto = event.text().lower()
          #Se pide que cada vez se levante la tecla para
        if not self.juego_pausado:    #poder volver a presionarla
            if texto =='a' and self.a_presionada and not event.isAutoRepeat():
                self.a_presionada = False
            if texto =='w' and self.w_presionada and not event.isAutoRepeat():
                self.w_presionada = False
            if texto =='s' and self.s_presionada and not event.isAutoRepeat():
                self.s_presionada = False
            if texto =='d' and self.d_presionada and not event.isAutoRepeat():
                self.d_presionada = False
        #Se revisa si se quiere usar el código de trampa de dinero
        if texto == 'm':
            self.tecla_m = True
        elif texto == 'o' and self.tecla_m and not self.tecla_o:
            self.tecla_o = True
        elif texto == 'n' and self.tecla_o and self.tecla_m:
            self.tecla_m = False
            self.tecla_o = False
            self.senal_trampa_dinero.emit()
        else:
            self.tecla_m = False
            self.tecla_o = False
    
    def closeEvent(self, a0): #Se sale del juego, guarda el puntaje, reinicia los parámtros
        self.reiniciar_parametros()
        for pingu in self.drop_labels:
            pingu.clear()
        self.label_dinero.setText('Dinero: 0')
        for pingu in self.label_pinguinos:
            pingu.dinero += PRECIO_PINGU
        self.pinguinos_en_pista = 0
        self.hide()
        self.senal_mandar_ranking.emit()
        self.senal_mostrar_inicio.emit()
        self.senal_reiniciar_logica_juego.emit()
    
    def actualizar_flechas(self, flecha, x, y):
        flecha.move(x, y) #Actualiza el lugar donde se muestra la flecha
    def reiniciar_combo(self):
        self.senal_reiniciar_combo.emit()
    def actualizar_dinero(self, dinero):
        self.label_dinero.setText(f'Dinero: {dinero}')
        for pingu in self.label_pinguinos:
            pingu.dinero = dinero

    def descontar_dinero(self):
        self.senal_descontar_dinero.emit()
        self.pinguinos_en_pista += 1 #Se suma un pinguino a la pista

    def actualizar_combos(self, combo_actual, combo_maximo, aprobacion):
        self.combo_actual.setText(f'Combo actual: {combo_actual}')
        self.combo_maximo.setText(f'Combo máximo: {combo_maximo}')
        self.barra_aprobacion.setValue(aprobacion) #También se actualiza la barra de aprobación
    
    def empezar_timer(self):
        global DURACION_MUSICA
        if self.pinguinos_en_pista <= 0:
            self.label_advertencia.setText('ADVERTENCIA\nAl menos\n1 pinguirin debe bailar!')
        else:
            #envía la orden a backend para que empiece el juego, con dificultad seleccionada
            if self.selector_dificultad.currentText() == 'Principiante':
                DURACION_MUSICA = 30
                self.duracion_musica = 30
                self.tiempo_entre_flechas = 1
                self.aprobacion_necesaria = 30
                self.pasos_maximos = 1
            elif self.selector_dificultad.currentText() == 'Aficionado':
                DURACION_MUSICA = 45
                self.duracion_musica = 45
                self.tiempo_entre_flechas = 0.75
                self.aprobacion_necesaria = 50
                self.pasos_maximos = 2
            elif self.selector_dificultad.currentText() == 'Maestro cumbia':
                DURACION_MUSICA = 60
                self.duracion_musica = 60
                self.tiempo_entre_flechas = 0.5
                self.aprobacion_necesaria = 70
                self.pasos_maximos = 3
            self.contador_puntaje.setText(f'TIEMPO:\n{self.duracion_musica}') #actualiza el tiempo
            self.label_advertencia.setText('')
            self.boton_juego.setEnabled(False) #Se desactivan todos los botones,se activa pausa
            self.selector_dificultad.setEnabled(False)
            self.selector_musica.setEnabled(False)
            self.boton_pausar.setEnabled(True)
            self.senal_empezar_musica.emit(self.selector_musica.currentText())

            self.timer_crear_flecha.setInterval(self.tiempo_entre_flechas*1000)

            self.senal_empezar_juego.emit(self.flechas, self.timer_crear_flecha,\
                self.segundos_pasados, self.duracion_musica)
        
    def creador_de_flechas(self):
        if self.contador_puntaje.text() != 'TIEMPO:\n0':
            pasos_a_crear = random.randint(1, self.pasos_maximos)
            for i in range(pasos_a_crear): #Depende de la dificultad número de flechas max a crear
                flecha_a_crear=random.choice([7,7+ALTO_CAPTURA,7+ALTO_CAPTURA*2,7+ALTO_CAPTURA*3])
                nueva_flecha = thread_flechas(self, flecha_a_crear , 600 )
                nueva_flecha.senal_actualizar.connect(self.actualizar_flechas)
                nueva_flecha.senal_cambiar_color.connect(self.cambiar_color_carril)
                nueva_flecha.senal_reiniciar_combo.connect(self.reiniciar_combo)
                self.flechas.append(nueva_flecha)
                self.flechas_creadas += 1
        else:#Si el tiempo lleegó a 0, se para el juego
            if self.flechas[-1].escondida: #Se mandan señales para analizar partida y reiniciar
                self.timer_crear_flecha.stop()
                self.senal_juego_terminado.emit(self.flechas_creadas, self.aprobacion_necesaria)
                self.boton_salir.setEnabled(False)
                self.senal_parar_musica.emit()
                
    def cambiar_color_carril(self,numero):
        for i in range(4):
            if numero == 7+ ALTO_CAPTURA * i:
                self.casillas[i].setStyleSheet("background-color: red")
            elif numero == 8 + ALTO_CAPTURA*i:
                self.casillas[i].setStyleSheet("background-color: blue")
           
    def actualizar_progreso_cancion(self, tiempo_pasado, porcentaje_cancion):
        self.contador_puntaje.setText(str(f'TIEMPO:\n{tiempo_pasado}'))
        self.barra_progreso_cancion.setValue(porcentaje_cancion)

    def pausar_juego(self):
        if not self.juego_pausado: #Si no está pasuada, se pausa
            self.juego_pausado = True
            self.boton_pausar.setText('Reanudar')
            if self.timer_crear_flecha.isActive(): #Se paran los timers
                self.timer_crear_flecha.stop()
            self.senal_parar_cronometro.emit() #Se manda señal a backend para pausar allá

            for flecha in self.flechas:
                if flecha.isRunning():
                    flecha.pausar_flecha = True
        elif self.juego_pausado: #Si está pausado, se despausa
            self.boton_pausar.setText('Pausar')
            self.juego_pausado = False
            self.timer_crear_flecha.start()
            self.senal_volver_cronometro.emit()
            for flecha in self.flechas:
                if flecha.isRunning():
                    flecha.pausar_flecha = False
        self.senal_pausar_musica.emit() #Se MANDA SEÑAL para parar o reanudar la música
        
    def reiniciar_parametros(self):
        if self.timer_crear_flecha.isActive(): #Se paran todos los threads que sigan en el fondo
            self.timer_crear_flecha.stop()
            self.senal_parar_cronometro.emit()
        for flecha in self.flechas:
            if flecha.isRunning():
                flecha.posicion = (flecha.posicion_x, flecha.limite_y) #Se teermina el thread
                flecha.flecha.hide()
        self.flechas_creadas = 0
        self.flechas = []
        self.segundos_pasados = 0
        self.boton_juego.setEnabled(True) #Se permite volver a jugar y elegir la dificultad
        self.boton_salir.setEnabled(True)
        self.selector_dificultad.setEnabled(True)
        self.selector_musica.setEnabled(True)
        self.boton_pausar.setEnabled(False)
        self.barra_aprobacion.setValue(0)
        self.barra_progreso_cancion.setValue(0)
        self.boton_pausar.setEnabled(False)
        self.boton_pausar.setText('Pausar')
        self.juego_pausado = False
        self.contador_puntaje.setText('TIEMPO:\n0')
        self.casilla1.setStyleSheet("background-color: blue")
        self.casilla2.setStyleSheet("background-color: blue")
        self.casilla3.setStyleSheet("background-color: blue")
        self.casilla4.setStyleSheet("background-color: blue")
        self.combo_actual = QLabel(f'combo actual: 0',self)
        self.combo_maximo = QLabel(f'combo máximo: 0',self)

    def volver_inicio(self): #clase para volver a inicio desde menu resultados
        self.reiniciar_parametros()
        self.pinguinos_en_pista = 0
        for pingu in self.drop_labels:
            pingu.clear()
        self.senal_reiniciar_logica_juego.emit()
        self.hide()
    
    
        

        
        
 





        





        

