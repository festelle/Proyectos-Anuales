import socket
import threading
import sys
import os
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QTimer
import json
import pickle
import random
import ast

#Se importan los parametros como un dict
with open('parametros.json',) as file:
    parametros = json.load(file)


#Conexión a servidor y back end de cliente
class Client(QObject):

    senal_entrar_sala = pyqtSignal()
    senal_accion_jugador = pyqtSignal(tuple)

    def __init__(self, port, host):
        super().__init__()

        self.host = host
        self.port = port
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.initBackend()
        except ConnectionError:
            print('conexión terminada')

    def initBackend(self):
        #Se almacenan toda la información perteneciente a backEnd
        self.username = None
        self.senal_entrar_sala.connect(self.entrar_sala)
        self.senal_accion_jugador.connect(self.procesar_accion_jugador)

        self.senal_mostrar_sala = None
        self.senal_actualizar_usernames = None
        self.senal_actualizar_mapa = None
        self.senal_comenzar_juego = None
        self.senal_servidor_lleno = None
        self.senal_actualizar_jugadores = None
        self.senal_habilitar_turno = None
        self.senal_permitir_acciones = None
        self.senal_actualizar_turno = None
        self.senal_juego_terminado = None
        self.senal_desconexion = None
        
        self.jugadores = []
        self.jugador = None
        self.mapa = None
        self.ganancia = parametros["GANANCIA_MATERIA_PRIMA"]


    def connect_to_server(self):
        """Crea la conexión al servidor."""
        self.socket_client.connect((self.host, self.port))

    def listen(self):
        """
        Inicializa el thread que escuchará los mensajes del servidor.
        """
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def send(self, msg):
        #Envía mensajes al servidor.
        '''
        stringified_value = str(msg)
        msg_bytes = stringified_value.encode("utf-8")
        msg_length = len(msg_bytes).to_bytes(4, byteorder='big')
        
        self.socket_client.sendall(msg_length + msg_bytes) '''
        #Se pasa el value a un string que se codifica y se le extrae el largo
        stringified_value = str(msg)
        msg_bytes = stringified_value.encode("utf-8")
        msg_length = len(msg_bytes).to_bytes(4, byteorder='big') #Se usa big endian
        
        #Se rellena con 0s el mensaje hasta que queden bloques de 60 bytes
        msg_rellenado = bytearray(msg_bytes)
        while len(msg_rellenado) % 60 != 0:
            msg_rellenado.extend(b'\x00')

        #Se crea el mensaje final agregando los bloques cada 60 bytes
        msg_final = bytearray()
        num_chunk = 0
        for i in range(0, len(msg_rellenado), 60):
            num_chunk += 1
            #Se agrega el número de bloque en bytes en que se usa little endian
            msg_final += num_chunk.to_bytes(4, byteorder='little')
            #Se agrega el chunk con el mensaje
            chunk = bytearray(msg_rellenado[i:i+60])
            msg_final += chunk
    
        #Se manda el msg_final que ya está completamente codificado junto al largo original
        self.socket_client.sendall(msg_length + msg_final)

    def listen_thread(self):
        while True:
            try:
                
                #Se recibe el largo del mensaje a extraer. Se pasa a int con bigEndian
                response_bytes_length = self.socket_client.recv(4)
                response_length = int.from_bytes(response_bytes_length, byteorder='big')
                response = bytearray()
                
                #Se empieza la recepción de bytes.
                bytes_recibidos = 0
                while bytes_recibidos < response_length:
                    #Se revisa si hay que recibir un bloque completo o solo parte
                    read_length = min(64, response_length - bytes_recibidos + 4)
                    chunk = self.socket_client.recv(read_length)
                    #El chunk se separa en el num de bloque y el mensaje
                    #num de bloque se pasa a int con little endian
                    num_chunk = int.from_bytes(chunk[:3], byteorder='little')
                    
                    #Se agrega el chunk que contiene el mensaje
                    chunk_a_agregar = bytearray(chunk[4:])
                    response.extend(chunk_a_agregar)

                    bytes_recibidos += read_length - 4
                
                #Se recibe el resto del mensaje (los 0s finales) solo si hay
                if 60 * num_chunk-response_length > 0:
                    ceros = self.socket_client.recv(60 * num_chunk - response_length)

                #Los mensajes recibidos siempre serán tuplas 
                response = response.decode('utf-8')
                mensaje = eval(response)
                
                
                #Ahora se toma acción con respecto a la orden recibida.
                if self.username is None and mensaje[0] == 'username' :
                    self.username = str(mensaje[1]) #se le asigna el nombre de usuario
                    self.senal_mostrar_sala.emit() 
                    #Si entrega un username, significa que fue aceptado, por lo que entra a sala
                
                elif mensaje[0] == 'rechazo':
                    #El server ya no está aceptando conexiones, se manda señal a frontEnd
                    #y abre otro socket para volver a intentar conectarse
                    self.senal_rechazo.emit()
                    self.socket_client.close()
                    #Se crea otro socket para poder volver a intertar conectarse.
                    self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                elif mensaje[0] == 'usernames':
                    #Se actualizan los usernames para poder actualizarlos en la ventana de espera
                    self.usernames = mensaje[1]
                    self.senal_actualizar_usernames.emit(self.username, self.usernames)

                elif mensaje[0] == 'comenzar juego':
                    #Se manda señal para entrar a ventana de juego
                    self.senal_comenzar_juego.emit(self.username)
                
                elif mensaje[0] == 'actualizar mapa':
                    #Se actualiza la instancia mapa en back y front End
                    mapa = pickle.loads(mensaje[1])
                    self.mapa = mapa
                    self.senal_actualizar_mapa.emit(mapa)

                elif mensaje[0] == 'actualizar jugadores':
                    #Se actualiza la lista de jugadores 
                    jugadores = []
                    jugadores_serializados = mensaje[1]
                    for jugador in jugadores_serializados:
                        jugador_deserializado = pickle.loads(jugador)
                        jugadores.append(jugador_deserializado)
                        if jugador_deserializado.username == self.username:
                            self.jugador = jugador_deserializado
                    
                    self.jugadores = jugadores
                    #Se actualiza la info visible en la ventana en frontEnd
                    self.senal_actualizar_jugadores.emit(self.jugadores)
                
                elif mensaje[0] == 'actualizar turno':
                    #Se manda señal para que frontEnd muestre que se cambió de turno
                    nombre_turno_actual = mensaje[1]
                    self.senal_actualizar_turno.emit(nombre_turno_actual)
                
                elif mensaje[0] == "turno":
                    #Se le permite al cliente rodar dados y hacer las acciones disponibles
                    self.senal_habilitar_turno.emit()
                
                elif mensaje[0] == "juego terminado":
                    #Si el ganador es el cliente, se le manda mensaje que ganó, en otro caso perdió
                    ganador = mensaje[1]
                    lista_jugadores = mensaje[2]
                    if ganador == self.username:
                        self.senal_juego_terminado.emit(('GANASTE', 'TU', lista_jugadores))
                    else:
                        self.senal_juego_terminado.emit(('PERDISTE', ganador, lista_jugadores))

            except ConnectionResetError:
                #Si el servidor se desconecta, se manda señal para mostrar ventana de desconexión
                self.senal_desconexion.emit()
                self.socket_client.close()
                exit()
                
    def entrar_sala(self):
        try:
            self.connect_to_server()
            self.listen()
            
        except ConnectionError:
            self.socket_client.close()
            exit()
    
    def procesar_accion_jugador(self, accion):
        #En esta función se procesa las señales que llegan del frontEnd
        log = []
        if accion[0] == 'rodar dados':
            resultado = accion[1]
            #Si resultado no fue 7, se reparte las cartas a los dueños de chozas en el hexágono
            if resultado != 7:
                hexagono_elegido = None
                for hexagono in self.mapa.hexagonos.values():
                    if hexagono.num_ficha == resultado:
                        hexagono_elegido = hexagono
                
                if hexagono_elegido is not None:
                    for nodo in hexagono_elegido.nodos:
                        if nodo.estado_actual == 'ocupado':
                            for jugador in self.jugadores:
                                if jugador.username == nodo.dueño:
                                    if hexagono_elegido.tipo == 'arcilla':
                                        jugador.arcilla += self.ganancia
                                    elif hexagono_elegido.tipo == 'madera':
                                        jugador.madera += self.ganancia
                                    elif hexagono_elegido.tipo == 'trigo':
                                        jugador.trigo += self.ganancia
            
            elif resultado == 7: #número de reforma agraria
                log = []
                #Se le quita la mitad los jugadores con más de 8 cartas de materia
                for instancia in self.jugadores:
                    if instancia.arcilla + instancia.madera + instancia.trigo >= 8:
                        cartas_robadas = 0
                        cartas_robar = (instancia.arcilla + instancia.madera + instancia.trigo)/2

                        while cartas_robadas < cartas_robar:
                            tipo = random.choice(['arcilla', 'madera', 'trigo'])
                            if tipo == 'arcilla' and instancia.arcilla >= 1:
                                instancia.arcilla -= 1
                                cartas_robadas += 1
                            elif tipo == 'madera' and instancia.madera >= 1:
                                instancia.madera -= 1
                                cartas_robadas += 1
                            elif tipo == 'trigo' and instancia.trigo >= 1:
                                instancia.trigo -= 1
                                cartas_robadas += 1
                        log.append(f'A {instancia.username} se le robó {cartas_robadas} cartas')


            #Se le manda al servidor la lista de jugadores actualizados
            jugadores_serializados = []
            for jugador in self.jugadores:
                jugadores_serializados.append( pickle.dumps(jugador))

            mensaje = ('dados rodados', jugadores_serializados, self.username, resultado, log)
            self.send(mensaje)

            #Se revisa si el jugador tiene suficiente materia para comprar una choza.
            #Si tiene suficiente, se envía la señal con un True para activar el botón
            habilitar_compra_chozas = False
            if self.jugador.arcilla >= parametros["CANTIDAD_ARCILLA_CHOZA"] and \
                    self.jugador.madera >= parametros["CANTIDAD_MADERA_CHOZA"] and \
                    self.jugador.trigo >= parametros["CANTIDAD_TRIGO_CHOZA"]:
                habilitar_compra_chozas = True
            self.senal_permitir_acciones.emit(habilitar_compra_chozas)
        
        elif accion[0] == 'comprar choza':
            #Se le cobra la materia prima
            id_nodo = accion[1]
            for instancia in self.jugadores:
                if instancia.username == self.username:
                    instancia.arcilla -= parametros["CANTIDAD_ARCILLA_CHOZA"]
                    instancia.madera -= parametros["CANTIDAD_MADERA_CHOZA"]
                    instancia.trigo -= parametros["CANTIDAD_TRIGO_CHOZA"]
                    instancia.puntos_victoria += 1

            #Se envía lista de jugadores actualizados a server
            jugadores_serializados = []
            for jugador in self.jugadores:
                jugadores_serializados.append( pickle.dumps(jugador))

            mensaje = ('choza comprada', jugadores_serializados, id_nodo)
            self.send(mensaje)



        elif accion[0] == "turno terminado":
            #Se manda mensaje a server para pasar al siguiente turno
            mensaje = ('turno terminado',)
            self.send(mensaje)