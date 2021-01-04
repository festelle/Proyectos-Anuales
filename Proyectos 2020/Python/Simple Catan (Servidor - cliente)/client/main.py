import frontEnd
import frontEnd2
import cliente
import sys
import os
from PyQt5.QtWidgets import QApplication

import json

with open('parametros.json',) as file:

    json_deserializado = json.load(file)

host = json_deserializado["host"]
port = json_deserializado["port"]


if __name__ == '__main__':
    app = QApplication([])
    
    ventanaInicio = frontEnd2.ventana_inicio()  
    logica = cliente.Client(port, host)
    #Se conecta front end y back end de inicio
    ventanaInicio.senal_entrar_sala = logica.senal_entrar_sala

    ventanaRechazo = frontEnd2.ventana_rechazo()
    #Se conectan las señales de la ventana de rechazo
    ventanaRechazo.senal_mostrar_inicio = ventanaInicio.senal_mostrar_inicio
    logica.senal_rechazo= ventanaRechazo.senal_rechazo

    salaEspera = frontEnd2.sala_espera()
    #Se conectan las señales de la sala de espera
    salaEspera.senal_entrar_sala = logica.senal_entrar_sala
    logica.senal_mostrar_sala = salaEspera.senal_mostrar_sala
    logica.senal_actualizar_usernames = salaEspera.senal_actualizar_usernames

    ventanaJuego = frontEnd.ventana_juego()
    #Se conectan las señales de la ventana de juego
    ventanaJuego.senal_esconder_sala = salaEspera.senal_esconder_sala
    logica.senal_comenzar_juego = ventanaJuego.senal_comenzar_juego
    logica.senal_actualizar_mapa = ventanaJuego.senal_actualizar_mapa
    logica.senal_actualizar_jugadores = ventanaJuego.senal_actualizar_jugadores
    logica.senal_habilitar_turno = ventanaJuego.senal_habilitar_turno
    ventanaJuego.senal_accion_jugador = logica.senal_accion_jugador
    logica.senal_juego_terminado = ventanaJuego.senal_juego_terminado
    logica.senal_actualizar_turno = ventanaJuego.senal_actualizar_turno
    logica.senal_permitir_acciones = ventanaJuego.senal_permitir_acciones

    ventanaFinal = frontEnd2.ventana_final()
    #Se conectan las señales de la ventana final
    ventanaJuego.senal_ventana_final = ventanaFinal.senal_ventana_final
    ventanaFinal.senal_cerrar_ventana_juego = ventanaJuego.senal_cerrar_ventana_juego
    
    ventanaDesconexion = frontEnd2.ventana_desconexion()
    #Se conectan las señales de la ventana de desconexión
    logica.senal_desconexion = ventanaDesconexion.senal_desconexion
    ventanaDesconexion.senal_cerrar_ventana_juego = ventanaJuego.senal_cerrar_ventana_juego


    
    ventanaInicio.show()
    sys.exit(app.exec_())