import socket
import threading
from faker import Faker
import json
import time
import random
from claseJugador import jugador
import pickle
import classMapa

#Se usará la librería faker para crear nombres
fake = Faker()

#Se traspasan los datos de parámetros
with open('parametros.json',) as file:
    parametros = json.load(file)

class Server:
    def __init__(self, port, host):
        print("Inicializando servidor...")

        self.host = host
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()
        self.accept_connections()
        self.jugadores = {} #dict {socket: jugador}
        self.partida_empezada = False
        self.jugadores_max = parametros['CANTIDAD_JUGADORES_PARTIDA']
        self.mapa = None
        self.colores_disponibles = ['azul','roja','verde', 'violeta']
        self.jugando = False
        self.ganador = None
        self.puntos_victoria_finales = int(parametros['PUNTOS_VICTORIA_FINALES'])
        self.orden_turnos = []

    def bind_and_listen(self):
        #Enlaza el socket creado con el host y puerto indicado.
        
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen(parametros['CANTIDAD_JUGADORES_PARTIDA']) 
        #Cantidad max de clientes a conectar
        print(f"Servidor escuchando en {self.host}:{self.port}...")
        print('\nLOGS:\n\n')

    def accept_connections(self):
        #Inicia el thread que aceptará clientes.
        
        thread = threading.Thread(target=self.accept_connections_thread)
        self.aceptando_jugadores = True
        thread.start()

    def accept_connections_thread(self): #Thread que acepta los clientes
        while True:
            #Si todavía no hay suficientes jugadores, se acepta la conexión
            if self.aceptando_jugadores:
            
                client_socket, address = self.socket_server.accept()
                listening_client_thread = threading.Thread(
                    target=self.listen_client_thread,
                    args=(client_socket, ),
                    daemon=False) 
                listening_client_thread.start()
                
                #Se revisa si ya está el límite de personas:
                if len(self.jugadores) >= self.jugadores_max:
                    self.aceptando_jugadores = False
                    time.sleep(1)
                    print('>> Comenzando partida\n')
                    #Se crea un thread para comenzar el juego, así se puede seguir escuchando
                    #conexiones nuevas
                    comenzar_juego_thread = threading.Thread(
                        target=self.comenzar_juego,
                        args=(),
                        daemon=False) 
                    comenzar_juego_thread.start()
            
            elif not self.aceptando_jugadores:
                #Se acepta momentaneamente la conexión para avisar que el server está lleno
                #Después, el propio cliente corta la conexión
                client_socket, address = self.socket_server.accept()
                mensaje = ('rechazo', 'Servidor lleno')
                self.send(mensaje, client_socket)
                print('>> Cliente rechazado, servidor lleno\n')
    
    @staticmethod
    def send(value, sock):
        #Envía mensajes hacia algún socket cliente.

        #Se transforma el mensaje a un string, se codifica y se extrae el largo
        stringified_value = str(value)
        msg_bytes = stringified_value.encode("utf-8")
        #Se utiliza big endian para el largo general
        msg_length = len(msg_bytes).to_bytes(4, byteorder='big') 
        
        #Se rellena con 0s una copia del mensaje hasta que queden bloques de 60 bytes
        msg_rellenado = bytearray(msg_bytes)
        while len(msg_rellenado) % 60 != 0:
            msg_rellenado.extend(b'\x00')

        #Se crea el mensaje final agregando bloques numerados cada 60 bytes
        msg_final = bytearray()
        num_chunk = 0
        for i in range(0, len(msg_rellenado), 60):
            num_chunk += 1
            #Se agrega el número de bloque y utiliza little endian para transformalo a bytes
            msg_final += num_chunk.to_bytes(4, byteorder='little')
            #Se agrega el chunk
            chunk = bytearray(msg_rellenado[i:i+60])
            msg_final += chunk
      
        #Se manda el msg_final que ya está completamente codificado junto al largo original
        sock.send(msg_length + msg_final)

    def repartir_objetos_iniciales(self):
        #A cada socket se le reparte los objetos y chozas
        for skt in self.jugadores.keys():
            nodos_libres = []
            #Se crea una lista con los nodos disponibles
            for nodo in self.mapa.nodos.values():
                if nodo.estado_actual == 'libre':
                    nodos_libres.append(nodo)

            #Se entregan dos chozas iniciales a los jugadores
            nodos_permitidos = False
            #TAL COMO SE PIDE EN EL ENUNCIADO, NO PUEDEN HABER DOS CHOZAS DE UN JUGADOR JUNTAS
            #Se eligen 2 nodos al azar hasta que salga un par que no sea vecino
            while not nodos_permitidos:
                nodos_agregar = random.sample(nodos_libres, 2 )
                if nodos_agregar[1] not in nodos_agregar[0].vecinos:
                    nodos_permitidos = True

            #Se agregan los nodos para cada jugador
            for nodo in nodos_agregar:
                nodo.estado_actual = 'ocupado'
                nodo.dueño = self.jugadores[skt].username
                nodo.color = self.jugadores[skt].color
                self.jugadores[skt].chozas_nodos[nodo.id] = nodo
                self.jugadores[skt].puntos_victoria += 1
                #Se suman los materiales iniciales del jugador
                for tipo in nodo.tipos_hexagonos:
                    if tipo == 'arcilla':
                        self.jugadores[skt].arcilla += parametros["GANANCIA_MATERIA_PRIMA"]
                    elif tipo == 'madera':
                        self.jugadores[skt].madera += parametros["GANANCIA_MATERIA_PRIMA"]
                    elif tipo == 'trigo':
                        self.jugadores[skt].trigo += parametros["GANANCIA_MATERIA_PRIMA"]

            #Se registra lo entregado al jugador
            nodos_de_jugador = list(self.jugadores[skt].chozas_nodos.keys())
            print(f'>> Chozas entregadas a {self.jugadores[skt].username}: {nodos_de_jugador}')
            print(f'>> A {self.jugadores[skt].username} se le dio:\
                {self.jugadores[skt].arcilla} arcilla(s),\
                {self.jugadores[skt].madera} madera(s), \
                 {self.jugadores[skt].trigo} trigo(s)\n')
    
    def actualizar_mapa(self):
        #Se manda la instancia de mapa más actual a todos los clientes para que la actualicen
        if self.mapa is None:
            self.mapa = classMapa.class_mapa()
            self.mapa.crear_hexagonos()
            
        mensaje = ("actualizar mapa",pickle.dumps(self.mapa))
        #Se registra que se actualiza el mapa
        print('>> Se actualiza el mapa de todos los jugadores\n')
        for skt in self.jugadores.keys():
            self.send(mensaje, skt)
  
    def actualizar_usernames(self):
        #Envía la orden para actualizar las personas en espera (en forma de tupla)
        nombres = []
        for instancia_jugador in self.jugadores.values():
            nombres.append(instancia_jugador.username)

        orden = ("usernames", nombres)
        for skt in self.jugadores.keys():
            self.send(orden, skt) 
    
    def actualizar_jugadores(self):
        #Manda una lista con las instancias de jugadores a todos los clientes
        lista_serializada = []
        for instancia_jugador in self.jugadores.values():
            jugador_serializado = pickle.dumps(instancia_jugador)
            lista_serializada.append(jugador_serializado)
        
        print('>> Se actualizan las instancias de jugadores en todos los clientes\n')
        for skt in self.jugadores.keys():
            mensaje = ('actualizar jugadores', lista_serializada)
            self.send(mensaje, skt)
        
    def actualizar_turno(self, nombre):
        #Se actualiza la persona que está de turno actualmente
        for skt in self.jugadores.keys():
            mensaje = ("actualizar turno", nombre)
            self.send(mensaje, skt)

    def comenzar_juego(self):

        if self.mapa is None:
            self.actualizar_mapa()
        self.repartir_objetos_iniciales()
        self.orden_turnos = list(self.jugadores.keys()) #Se define el orden de los turnos
        
        for skt in self.jugadores.keys():
            orden = ("comenzar juego", "") #Se manda la orden de comenzar el juego a todos
            self.send(orden, skt)
        
        #Se comienza el loop del juego principal
        self.juego()
    
    def juego(self):
        #loop principal del juego
        self.jugando = True
        
        while self.jugando:

            for skt in self.orden_turnos:
                #Todos los turnos se empiezan actualizando mapa y jugadores
                self.actualizar_jugadores()
                self.actualizar_mapa()
                #Se registra en el server el cambio de turno
                print(f'>> Turno de {self.jugadores[skt].username}\n')
                self.actualizar_turno(self.jugadores[skt].username)
                self.send(("turno",""), skt)

                self.accion_jugador = False
                #Mientras no se reciba el mensaje de que el jugador hizo una acción, se espera
                #LA ACCION ES PROCESADA EN LA FUNCION DE LISTEN
                while not self.accion_jugador:
                    pass
                #Se revisa si hay un ganador
                for instancia in self.jugadores.keys():
                    if self.jugadores[instancia].puntos_victoria >= self.puntos_victoria_finales:
                        #Si hay un ganador se envía el mensaje a todos los sockets
                        self.jugando = False
                        self.ganador = self.jugadores[instancia].username
                        #Se crea una lista con los jugadores y ordena según puntaje
                        lugares = list(self.jugadores.values())
                        lugares.sort(key = lambda x: x.puntos_victoria, reverse = True)
                        #Ahora se transforma en una lista con solo los nombres
                        lugares = [j.username + ' ('+ str(j.puntos_victoria) + ' puntos)' \
                            for j in lugares]

                        print(f'>> Juego terminado. Ganador: {self.ganador}')

                        for skt in self.jugadores.keys():
                            #Se manda mensaje de que la partida terminó junto a puestos
                            mensaje = ('juego terminado', self.ganador, lugares)
                            self.send(mensaje, skt)
                            self.jugando = False

    def listen_client_thread(self, client_socket):
        #Es ejecutado como thread que escuchará a un cliente en particular.
        #Primero se le asigna un nombre al usuario
        username = fake.name()
        #También se le asigna un color de entre 4 opciones
        color = random.choice(self.colores_disponibles)

        #Se crea la instancia jugador que se mete al dict de jugadores con el socket como key
        self.jugadores[client_socket] = jugador(username)
        self.jugadores[client_socket].color = color
        self.colores_disponibles.remove(color)

        #Se manda el primer mensaje al cliente, en donde se le asigna su username
        self.send(("username", username), client_socket)
        print(f"\n>> {username} se ha conectado\n")
        #Se actualiza la sala de espera
        self.actualizar_usernames()

        conectado = True
        while conectado:
            try:
                #Se revisa el largo del mensaje a recibir
                response_bytes_length = client_socket.recv(4)
                #Se tranforma a un int mediante big endian
                response_length = int.from_bytes(response_bytes_length, byteorder='big')

                #Se crea un bytearray donde se guardará la respuesta
                response = bytearray()

                #Se reciben bytes en chunks
                bytes_recibidos = 0
                while bytes_recibidos < response_length:
                    #Se revisa si hay que recibir un bloque completo o solo parte
                    read_length = min(64, response_length - bytes_recibidos + 4)
                    chunk = client_socket.recv(read_length)
                    #El chunk se separa en el num de bloque (se usa little endian) y el mensaje
                    num_chunk = int.from_bytes(chunk[:3], byteorder='little')
                    
                    #Se agrega el chunk que contiene el mensaje
                    chunk_a_agregar = bytearray(chunk[4:])
                    response.extend(chunk_a_agregar)

                    bytes_recibidos += read_length - 4
                
                #Se recibe el resto del mensaje (los 0s finales) solo si hay.
                if 60 * num_chunk-response_length > 0:
                    ceros = client_socket.recv(60 * num_chunk - response_length)

                #Los mensajes recibidos siempre serán tuplas.
                mensaje = eval(response.decode('utf-8'))

                #Ahora se desarrollan acciones dependiendo de la orden recibida
                if mensaje[0] == 'dados rodados':
                    resultado = mensaje[3]
                    print(f'>> {mensaje[2]} lanzó los dados. Resultado: {resultado}\n')
                    #Se imprimen los logs en el servidor
                    logs = mensaje[4]
                    if logs != []:
                        for log in logs:
                            print('>>',log)
                    #Se deserializa a los jugadores
                    jugadores_serializados = mensaje[1]
                    jugadores = []
                    for jugador_serializado in jugadores_serializados:
                        jugador_deserializado = pickle.loads(jugador_serializado)
                        jugadores.append(jugador_deserializado)

                    #Se debe pasar de una lista a un dict de jugadores, además se hace un log
                    #si se le entregó alguna materia a un jugador
                    nuevo_dict_jugadores= {}
                    actualizar = False 
                    for skt in self.jugadores:
                        for instancia_jugador in jugadores:
                            if instancia_jugador.username == self.jugadores[skt].username:
                                nuevo_dict_jugadores[skt] = instancia_jugador
                                if instancia_jugador.arcilla > self.jugadores[skt].arcilla:
                                    dif = instancia_jugador.arcilla - self.jugadores[skt].arcilla
                                    print(f'>> Entregado a {instancia_jugador.username} \
                                        {dif} arcilla(s) debido a tener choza(s) en el hexágono\n')
                                    actualizar = True
                                if instancia_jugador.madera > self.jugadores[skt].madera:
                                    dif = instancia_jugador.madera - self.jugadores[skt].madera
                                    print(f'>> Entregado a {instancia_jugador.username} \
                                        {dif} madera(s) debido a tener choza(s) en el hexágono\n')
                                    actualizar = True
                                if instancia_jugador.trigo > self.jugadores[skt].trigo:
                                    dif = instancia_jugador.trigo - self.jugadores[skt].trigo
                                    print(f'>> Entregado a {instancia_jugador.username} \
                                        {dif} trigo(s) debido a tener choza(s) en el hexágono\n')
                                    actualizar = True
                                break
                    #Se actualizan las instancias de jugadores en todos los clientes
                    self.jugadores = nuevo_dict_jugadores
                    #booleano que indica si algún jugador tuvo un cambio para actualizarlo
                    if actualizar:
                        self.actualizar_jugadores()
                
                elif mensaje[0] == 'choza comprada': 
                    #Se registra en el server
                    id_nodo = mensaje[2]
                    nombre = self.jugadores[client_socket].username
                    print(f'>> {nombre} compró la choza ubicada en {id_nodo}\n')
                    
                    #Se deserializan los jugadores
                    jugadores_serializados = mensaje[1]
                    jugadores = []
                    for jugador_serializado in jugadores_serializados:
                        jugador_deserializado = pickle.loads(jugador_serializado)
                        jugadores.append(jugador_deserializado)

                    #Se debe pasar de una lista a un dict de jugadores
                    nuevo_dict_jugadores= {}
                    for skt in self.jugadores:
                        for instancia_jugador in jugadores:
                            if instancia_jugador.username == self.jugadores[skt].username:
                                nuevo_dict_jugadores[skt] = instancia_jugador
                    #Se actualizan las instancias de jugadores
                    self.jugadores = nuevo_dict_jugadores

                    #Ahora se le da la choza, en el backEnd del cliente se le cobró
                    #Se cambia la info del nodo comprado y actualiza el mapa
                    self.mapa.nodos[id_nodo].estado_actual = 'ocupado'
                    self.mapa.nodos[id_nodo].dueño = self.jugadores[client_socket].username
                    self.mapa.nodos[id_nodo].color = self.jugadores[client_socket].color
                    #Se agrega el nodo al dict del jugador
                    self.jugadores[client_socket].chozas_nodos[id_nodo] = self.mapa.nodos[id_nodo]

                elif mensaje[0] == 'turno terminado':
                    #Se registra el turno terminado y actualiza lo necesario
                    print(f'>> Turno de {self.jugadores[client_socket].username} terminado\n')
                    self.accion_jugador = True

            except ConnectionResetError:
                #Si hay un problema de conexión, se registra que el cliente se desconectó
                #y se elimina de todas las listas y dicts.

                print(f'\n>> {self.jugadores[client_socket].username} se ha desconectado\n')
                
                self.jugadores.pop(client_socket, None)
                        
                self.actualizar_jugadores()
                self.actualizar_mapa()
                self.orden_turnos.remove(client_socket)
                conectado = False
                    

