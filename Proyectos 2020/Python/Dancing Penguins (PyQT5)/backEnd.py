
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QTimer
from parametros import PUNTOS_FLECHA, VELOCIDAD_FLECHA, PATH_RANKING, CANCIONES,\
     ALTO_CAPTURA, ALTO_FLECHA, PRECIO_PINGU, DINERO_TRAMPA
import os
from qtpy.QtMultimedia import QSound, QMediaPlaylist, QMediaPlayer, QMediaContent


#eN ESTE ARCHIVO ESTÁ EL BACKEND PARA LAS VENTANAS INICIO, JUEGO Y RESUMEN 

class logica_inicio(QObject):
    senal_procesar = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.senal_actualizar = None
        self.senal_procesar.connect(self.procesar_input)
        self.senal_abrir_juego = None
        self.senal_esconder = None
        self.senal_actualizar = None
        self.senal_nombre = None
        self.nombre = ''
        self.senal_mostrar_ranking = None
        
    def procesar_input(self, nombre):
        if nombre[0] == 0:
            if nombre[1].isalnum(): #si nombre cumple la condición
                if self.senal_abrir_juego:
                    self.nombre = nombre[1] #guarda el nombre
                    self.senal_abrir_juego.emit() #abre juego
                    self.senal_esconder.emit()
                    self.senal_nombre.emit(self.nombre)
            else: #Si nombre no es alnum, se pide otro nombre
                self.senal_actualizar.emit('Elige un nombre de usuario válido.')
        
        elif nombre[0] == 1:
            #Si el mensaje emitido pide los ranking, se imprimen en ventana ranking
            if nombre[1] == 'mostrar ranking':
                #Se extraen los puntajes guardados en el archivo
                if not os.path.isfile(PATH_RANKING): #Si no existe se crea el archivo
                    with open(PATH_RANKING, 'w') as archivo:
                        pass
                with open(PATH_RANKING, "rt") as archivo:
                    lineas = archivo.readlines()
                tablero = []
                for linea in lineas:
                    fila = linea.strip().split(',')
                    tablero.append(fila)
                for puntaje in tablero:
                    puntaje[0] = int(puntaje[0])
                #Se ordenan los puntajes
                tablero.sort(key = lambda x: x[0], reverse = True)

                while len(tablero) < 5: #Si hay menos de 5 puntajes, se rellena
                    tablero.append(['',''])
                while len(tablero) > 5: #si hya más de 5 puntajes, se dejan solo los top5
                    tablero.pop(-1)

                self.senal_mostrar_ranking.emit(tablero)

class logica_juego(QObject):
    senal_contacto_flecha = pyqtSignal(list, str)
    senal_empezar_juego = pyqtSignal(list, object, int, int) #AL FINAL VA EL CRONOMETRO
    senal_juego_terminado =pyqtSignal(int, int)
    senal_reiniciar_combo = pyqtSignal()
    senal_siguiente_ronda = pyqtSignal()
    senal_empezar_musica = pyqtSignal(str)
    senal_parar_musica = pyqtSignal()
    senal_pausar_musica = pyqtSignal()
    senal_descontar_dinero = pyqtSignal()
    senal_reiniciar_logica_juego = pyqtSignal()
    senal_trampa_dinero = pyqtSignal()
    senal_terminar_partida = pyqtSignal()
    senal_parar_cronometro = pyqtSignal()
    senal_volver_cronometro = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.senal_actualizar = None
        #diccionario asocia cada letra con su respectivo carril
        self.letra_carril = {'a':7,'w':7+ALTO_CAPTURA,'s':7+ALTO_CAPTURA*2,'d':7+ALTO_CAPTURA*3}
        self.senal_mostrar_resumen = None #señal a ventana resumen para qe se muestre
        self.senal_reiniciar = None #señal a su frontEnd para reiniciar los parámetros de allá
        self.senal_actualizar_combos = None #Señal a su frontEnd cambiar los labels de los combos
        self.senal_actualizar_dinero = None #Señal para frontEnd para actualizar dinero disponible
        self.senal_actualizar_progreso_cancion = None
        self.senal_actualizar_contador_tiempo = None
        self.senal_empezar_juego.connect(self.empezar_timer)
        self.senal_juego_terminado.connect(self.juego_terminado)
        self.senal_reiniciar_combo.connect(self.reiniciar_combo)
        self.senal_siguiente_ronda.connect(self.siguiente_ronda)
        self.senal_descontar_dinero.connect(self.descontar_dinero)
        self.senal_reiniciar_logica_juego.connect(self.reiniciar_logica_juego)
        self.senal_trampa_dinero.connect(self.agregar_dinero_trampa)
        self.senal_terminar_partida.connect(self.terminar_partida_antes)
        self.senal_parar_cronometro.connect(self.parar_cronometro)
        self.senal_volver_cronometro.connect(self.volver_cronometro)
        
        
        
        #Se lleva cuenta del puntaje con esta variable
        self.puntaje_obtenido = 0
        self.pasos_correctos = 0
        self.pasos_incorrectos = 0
        self.__dinero = PRECIO_PINGU
        self.dinero_backup = 0 #guarda una copia del dinero
        self.juego_andando = False #booleano que indica si está andando o no el juego

        self.flechas_normales_acertadas = 0
        self.flechas_X2_acertadas = 0
        self.flechas_doradas_acertadas = 0
        self.flechas_hielo_acertadas = 0
        #variables para guardar el combo máximo
        self.combo = 0
        self.combo_maximo = 0

        self.duracion_cancion = 0
        
        #se conecta la señal de contacto con la revision de contacto
        self.senal_contacto_flecha.connect(self.revisar_contacto)
        self.senal_empezar_musica.connect(self.reproducir_cancion)
        self.cancion = QMediaPlayer()
        self.senal_parar_musica.connect(self.parar_cancion)
        self.senal_pausar_musica.connect(self.pausar_musica)
        self.cancion_pausada = False

        self.timer_cronometro = QTimer(self)
        self.timer_cronometro.setInterval(1*1000)
        self.timer_cronometro.timeout.connect(self.cronometro)
        self.segundos_pasados = 0
        
    
    @property
    def dinero(self):
        return self.__dinero
    @dinero.setter
    def dinero(self,valor): #cada vez que se actualice el dinero, se manda la señal a frontEnd
        if valor <= 0:
            self.__dinero = 0
        else:
            self.__dinero = valor
        self.senal_actualizar_dinero.emit(self.dinero)
    
    def empezar_timer(self, flechas, timer, tiempo, duracion_cancion): #AL FINAL HAY UN CRONOMETRO
        
        flechas = [] #Se eliminan las flechas anteriores
        flechas_creadas = 0
        self.juego_andando = True
        self.dinero_backup = self.dinero
        self.dinero = 0
        timer.start() #Se repite la funcion creador de flechas
        tiempo = 0
        self.duracion_cancion = duracion_cancion
        self.timer_cronometro.start()
    
    def cronometro(self):

        tiempo_pasado = self.duracion_cancion - self.segundos_pasados
        porcentaje_cancion = self.segundos_pasados/self.duracion_cancion * 100

        self.segundos_pasados += 1

        self.senal_actualizar_progreso_cancion.emit(tiempo_pasado, porcentaje_cancion)

        #self.barra_progreso_cancion.setValue(porcentaje_cancion)
        if self.segundos_pasados > self.duracion_cancion: #cronómetro se acaba cuando se llegue a 0
            self.timer_cronometro.stop()
    def parar_cronometro(self):
        if self.timer_cronometro.isActive():
            self.timer_cronometro.stop()
    def volver_cronometro(self):
        self.timer_cronometro.start()

    def revisar_contacto(self, flechas, carril):
        #Se revisa en el carril correspondiente si hay alguna flecha que esté haciendo contacto,
        for flecha in flechas: #si hay más de una, se elimina la primera que se encuentra
            if flecha.posicion[0] == self.letra_carril[carril]:
                if  516 <= flecha.posicion[1] + ALTO_FLECHA <= 516+ALTO_CAPTURA+ ALTO_FLECHA \
                        and not flecha.escondida:
                    self.puntaje_obtenido += PUNTOS_FLECHA * flecha.puntaje_a_obtener
                    flecha.flecha.setHidden(True)
                    flecha.escondida = True
                    self.pasos_correctos += 1
                    self.combo += 1
                    #Se mide aprobación
                    if (self.pasos_correctos + self.pasos_incorrectos)>0:
                        self.aprobacion = 100 * (self.pasos_correctos - self.pasos_incorrectos)/ \
                            (self.pasos_correctos + self.pasos_incorrectos)
                    else:
                        self.aprobacion= 0

                    self.combo_maximo = max(self.combo, self.combo_maximo)
                    self.senal_actualizar_combos.emit(self.combo, self.combo_maximo, self.aprobacion)

                    if flecha.tipo_flecha == 'flecha normal':
                        self.flechas_normales_acertadas += 1
                    elif flecha.tipo_flecha == 'flecha X2':
                        self.flechas_X2_acertadas += 1
                    elif flecha.tipo_flecha == 'flecha dorada':
                        self.flechas_doradas_acertadas += 1
                    elif flecha.tipo_flecha == 'flecha hielo':
                        flecha.congelar_flechas()
                        self.flechas_hielo_acertadas += 1
                    return #Se termina la función si había una flecha en el lugar

        #Si se apretó un botón incorrectamente, se cuenta como paso incorrecto
        self.pasos_incorrectos += 1
        if (self.pasos_correctos + self.pasos_incorrectos)>0: #Se mide aprobación
            self.aprobacion = 100 * (self.pasos_correctos - self.pasos_incorrectos)/ \
                (self.pasos_correctos + self.pasos_incorrectos)
        else:
            self.aprobacion= 0
        self.combo_maximo = max(self.combo, self.combo_maximo)
        self.reiniciar_combo()
        self.senal_actualizar_combos.emit(self.combo, self.combo_maximo, self.aprobacion)
    
    def reiniciar_combo(self):
        self.combo = 0 #Si alguna flecha pasa sin ser apretada, se manda la señal para reiniciarlo
    
    def reproducir_cancion(self, cancion):
        #self.cancion = QSound(CANCIONES[cancion])
        cancion = QMediaContent(QUrl.fromLocalFile(CANCIONES[cancion])) #path a la canción
        self.cancion.setMedia(cancion)
        self.cancion.play()
    
    def parar_cancion(self):
        self.cancion.stop()

    def descontar_dinero(self):
        self.dinero -= PRECIO_PINGU
    
    def terminar_partida_antes(self):
        self.timer_cronometro.stop()
        self.senal_actualizar_progreso_cancion.emit(0, 100)

    
    
    def pausar_musica(self):
        if self.cancion_pausada:
            self.cancion.play()
            self.cancion_pausada = False
        elif not self.cancion_pausada:
            self.cancion.pause()
            self.cancion_pausada = True
    
    def agregar_dinero_trampa(self):
        #Si se está jugando, se suma al backup para que aparezca cuando termine el juego
        #Si no se está jugando, se suma directamente al dinero
        if self.juego_andando: 
            self.dinero_backup += DINERO_TRAMPA
        elif not self.juego_andando:
            self.dinero += DINERO_TRAMPA

    def juego_terminado(self, flechas_hechas, aprobacion_minima):
        #Se revisa si el último combo es el mejor
        self.combo_maximo = max(self.combo_maximo, self.combo)
        if (self.pasos_correctos + self.pasos_incorrectos)>0: #aprobación
            self.aprobacion = 100 * (self.pasos_correctos - self.pasos_incorrectos)/ \
                (self.pasos_correctos + self.pasos_incorrectos)
        else:
            self.aprobacion= 0
    
        suma_flechas = self.flechas_normales_acertadas + self.flechas_X2_acertadas * 2 + \
            10 * self.flechas_doradas_acertadas + self.flechas_hielo_acertadas
        
        self.puntaje = suma_flechas * self.combo_maximo * self.puntaje_obtenido
        self.senal_mostrar_resumen.emit(self.puntaje, self.combo_maximo, self.pasos_incorrectos,\
             self.aprobacion, aprobacion_minima)
        #Se agrega el dinero
        self.juego_andando = False #Se indica que el juego dejó de andar
        self.dinero = self.dinero_backup #Se vuelve a instaurar el valor real del dinero
        self.dinero += self.puntaje
        self.segundos_pasados = 0
        
        

    def siguiente_ronda(self):
        #Se reinician los parámetros
        self.parar_cancion()
        self.puntaje_obtenido = 0
        self.pasos_correctos = 0
        self.pasos_incorrectos = 0
        self.flechas_normales_acertadas = 0
        self.flechas_X2_acertadas = 0
        self.flechas_doradas_acertadas = 0
        self.flechas_hielo_acertadas = 0
        self.combo = 0
        self.combo_maximo = 0
        #Emite señal a frontend para reiniciar sus parámetros
        self.senal_reiniciar.emit()
        self.juego_andando = False
        self.segundos_pasados = 0
    
    def reiniciar_logica_juego(self):
        #Se reinician los parámetros
        self.parar_cancion()
        self.puntaje_obtenido = 0
        self.pasos_correctos = 0
        self.pasos_incorrectos = 0
        self.flechas_normales_acertadas = 0
        self.flechas_X2_acertadas = 0
        self.flechas_doradas_acertadas = 0
        self.flechas_hielo_acertadas = 0
        self.combo = 0
        self.combo_maximo = 0
        self.dinero = 500
        #Emite señal a frontend para reiniciar sus parámetros
        self.senal_reiniciar.emit()
        self.juego_andando = False
        self.segundos_pasados = 0
        

class logica_resumen(QObject):
    #Esta señal se va a emitir solo cuando la partida general haya terminado
    senal_escribir_ranking = pyqtSignal(str, int)
    def __init__(self):
        super().__init__()
        self.senal_escribir_ranking.connect(self.escribir_ranking)
    
    def escribir_ranking(self, nombre, puntaje_acumulado):
        #recibe una lista con los 5 mejores puntajes ya ordenados de mayor a menor
        texto = (f'{puntaje_acumulado},{nombre}\n')
        with open(PATH_RANKING, "a") as archivo:
            archivo.write(texto)



