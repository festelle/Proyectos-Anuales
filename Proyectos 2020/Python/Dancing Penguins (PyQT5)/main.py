from frontEnd import *
from backEnd import *
from frontEnd_2 import *
import sys
import os
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush

if __name__ == '__main__':
    app = QApplication([])
    
    ventanaInicio = ventana_Inicio()
    logicaInicio = logica_inicio()
    #S conecta front end y back end de inicio
    ventanaInicio.senal_procesar = logicaInicio.senal_procesar
    logicaInicio.senal_esconder = ventanaInicio.senal_esconder
    logicaInicio.senal_actualizar = ventanaInicio.senal_actualizar


    
    ventanaJuego = ventana_juego()
    logicaJuego = logica_juego()
    #Se conecta front y back end de juego

    logicaInicio.senal_abrir_juego = ventanaJuego.senal_abrir_juego

    
    ventanaJuego.senal_contacto_flecha = logicaJuego.senal_contacto_flecha
    ventanaJuego.senal_empezar_juego = logicaJuego.senal_empezar_juego
    ventanaJuego.senal_mostrar_inicio = ventanaInicio.senal_mostrar
    ventanaJuego.senal_juego_terminado = logicaJuego.senal_juego_terminado
    ventanaJuego.senal_reiniciar_combo = logicaJuego.senal_reiniciar_combo
    ventanaJuego.senal_reiniciar_logica_juego = logicaJuego.senal_reiniciar_logica_juego
    ventanaJuego.senal_empezar_musica = logicaJuego.senal_empezar_musica
    ventanaJuego.senal_parar_musica = logicaJuego.senal_parar_musica
    ventanaJuego.senal_pausar_musica = logicaJuego.senal_pausar_musica
    ventanaJuego.senal_descontar_dinero = logicaJuego.senal_descontar_dinero
    ventanaJuego.senal_parar_cronometro = logicaJuego.senal_parar_cronometro
    ventanaJuego.senal_volver_cronometro = logicaJuego.senal_volver_cronometro
    ventanaJuego.senal_terminar_partida = logicaJuego.senal_terminar_partida
    ventanaJuego.senal_trampa_dinero = logicaJuego.senal_trampa_dinero

    logicaJuego.senal_reiniciar = ventanaJuego.senal_reiniciar
    logicaJuego.senal_actualizar_combos = ventanaJuego.senal_actualizar_combos
    logicaJuego.senal_actualizar_dinero = ventanaJuego.senal_actualizar_dinero
    logicaJuego.senal_actualizar_progreso_cancion = ventanaJuego.senal_actualizar_progreso_cancion
    
    


    ventanaResumen = ventana_resumen()
    logicaResumen = logica_resumen()
    #Se conecta fron End y backEnd de resumen
    logicaInicio.senal_nombre = ventanaResumen.senal_nombre

    logicaJuego.senal_mostrar_resumen = ventanaResumen.senal_mostrar_resumen
    ventanaJuego.senal_mandar_ranking = ventanaResumen.senal_mandar_ranking

    ventanaResumen.senal_menu_inicio = ventanaInicio.senal_mostrar
    ventanaResumen.senal_siguiente_ronda = logicaJuego.senal_siguiente_ronda
    ventanaResumen.senal_esconder_juego = ventanaJuego.senal_esconderse
    ventanaResumen.senal_escribir_ranking = logicaResumen.senal_escribir_ranking
    ventanaResumen.senal_reiniciar_logica_juego = logicaJuego.senal_reiniciar_logica_juego

    #ventana ranking
    ventanaRanking = ventana_ranking()

    logicaInicio.senal_mostrar_ranking = ventanaRanking.senal_mostrar_ranking


    ventanaInicio.show()
    sys.exit(app.exec_())