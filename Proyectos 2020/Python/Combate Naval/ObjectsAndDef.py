from parametros import NUM_BARCOS
from parametros import RADIO_EXP
from tablero import print_tablero
import random

# Función que agrega los puntajes de los juegos.
# Se hizo con ayuda de información de la página:
# https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
def saveScore(nombre, puntaje):
    puntajes = open("puntajes.txt", 'a')
    puntajes.write("\n" + nombre + "," + str(puntaje))

# Función que imprime los 5 mejores puntajes
def rankingPuntajes():
    puesto = 1
    archivo = open("puntajes.txt", "rt")
    lineas = archivo.readlines()
    historiaPuntajes = []
    for linea in lineas:
        fila = linea.strip().split(',')
        historiaPuntajes.append(fila)

    # Esta linea para poder ordenar los puntajes fue sacada de:
    # https://www.afternerd.com/blog/python-sort-list/
    historiaPuntajes.sort(key=lambda x: int(x[1]), reverse=True)
    for puntaje in historiaPuntajes:
        if puesto < 6:
            print(puesto, ")", puntaje[0] + ": ", puntaje[1])
            puesto += 1
        else:
            break

# Clase del juego.
class game(object):
    global NUM_BARCOS
    global RADIO_EXP

    def __init__(self, filas, cols, apodo):

        self.apodo = apodo
        self.filas = int(filas)
        self.cols = int(cols)
        self.turnoJugador = True
        self.run = True
        self.listaFilas = []
        self.tableroJugador = []
        self.barcosPuestosJugador = 0
        self.tableroEnemigo = []
        self.barcosPuestosEnemigo = 0
        self.bombasDisponibles = ["[0] Regular", "[1] Bomba cruz*", "[2] Bomba X*",
                                  "[3] Bomba diamante*"]
        self.barcosEnemigosHundidos = 0
        self.barcosJugadorHundidos = 0
        self.rendirse = False
        self.salirPrograma = False
        self.barcosAcertados = 0
        self.filaAtacar = 0
        self.colAtacar = 0
        self.filaAtaqueOponente = 0
        self.colAtaqueOponente = 0
        self.sePuedeAtacar = False
        self.puntaje = 0
        # Diccionarios para traducir letras a números y viceversa
        self.convertToNumber = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7,
                                "I": 8, "J": 9, "K": 10,
                                "L": 11, "M": 12, "N": 13, "O": 14}
        self.convertToLetter = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H",
                                8: "I", 9: "J", 10: "K",
                                11: "L", 12: "M", 13: "N", 14: "O"}

        # Se crea el tablero del jugador
        for j in range(self.filas):
            self.listaFilas = []
            for i in range(self.cols):
                self.listaFilas.append(' ')
            self.tableroJugador.append(self.listaFilas)
        # Se ponen los barcos en el tablero del jugador
        while self.barcosPuestosJugador < NUM_BARCOS:
            a = random.randint(0, self.filas - 1)
            b = random.randint(0, self.cols - 1)
            if self.tableroJugador[a][b] == " ":
                self.tableroJugador[a][b] = "B"
                self.barcosPuestosJugador += 1

        # Se crea el tablero del oponente
        for j in range(self.filas):
            self.listaFilas = []
            for i in range(self.cols):
                self.listaFilas.append(' ')
            self.tableroEnemigo.append(self.listaFilas)
        # Se ponen los barcos en el tablero enemigo
        while self.barcosPuestosEnemigo < NUM_BARCOS:
            a = random.randint(0, self.filas - 1)
            b = random.randint(0, self.cols - 1)
            if self.tableroEnemigo[a][b] == " ":
                self.tableroEnemigo[a][b] = "B"
                self.barcosPuestosEnemigo += 1

    def running(self):
        # Loop que controla el juego, cuando se quiera salir de este self.run = False
        while self.run:
            if self.turnoJugador:
                # Menu del juego
                print("\n-- Menu de Juego -- \n")
                print("Turno: Jugador")
                print_tablero(self.tableroEnemigo, self.tableroJugador)
                print("\nSeleccione una opción:")
                print(" [0] Rendirse \n [1] Lanzar una bomba \n [2] Salir del programa")
                seleccion = input("Ingresa tu elección (0, 1 ó 2):  ")
                while seleccion != '0' and seleccion != '1' and seleccion != '2':
                    print('por favor, elige una opción válida')
                    seleccion = input("Ingresa tu elección (0, 1 ó 2):  ")
                if seleccion == '0':
                    # Rendirse
                    self.rendirse = True
                    self.GameOver()

                if seleccion == '1':
                    # Disparar una bala
                    print("\n¡A la carga capitán!")
                    print('Qué tipo de bomba quieres lanzar?: ')
                    for i in self.bombasDisponibles:
                        print(i)
                    if len(self.bombasDisponibles) > 1:
                        print('*Solo puedes usar una de estas bombas una vez por juego')
                    eleccion = input('¿Cuál quieres usar? ')
                    while not eleccion.isdigit() or not 0 <= int(eleccion) <= len(
                            self.bombasDisponibles) - 1:
                        eleccion = input('Por favor, elige una bomba válida')
                    # Cuando se usa una de las balas especiales, se eliminan de las opciones
                    if eleccion == '1' or eleccion == '2' or eleccion == '3':
                        self.bombasDisponibles = ['[0] Regular']
                    self.bombas(eleccion)

                if seleccion == '2':
                    # Salir del programa
                    self.salirPrograma = True
                    self.GameOver()
                    break
            elif not self.turnoJugador:
                # Turno del oponente
                print("-- Menu de Juego -- \n")
                print("Turno: Oponente")
                # Se elige al azar las casillas a atacar, pero no se pueden repetir
                self.filaAtaqueOponente = random.randint(0, self.filas - 1)
                self.colAtaqueOponente = random.randint(0, self.cols - 1)
                while self.tableroJugador[self.filaAtaqueOponente][self.colAtaqueOponente] == "X" or \
                        self.tableroJugador[self.filaAtaqueOponente][self.colAtaqueOponente] == "F":
                    self.filaAtaqueOponente = random.randint(0, self.filas - 1)
                    self.colAtaqueOponente = random.randint(0, self.cols - 1)
                print("Tu oponente atacó a la casilla (" + str(self.filaAtaqueOponente) + "," + str(
                    self.convertToLetter[self.colAtaqueOponente] + ")"))

                if self.tableroJugador[self.filaAtaqueOponente][self.colAtaqueOponente] == "B":
                    self.tableroJugador[self.filaAtaqueOponente][self.colAtaqueOponente] = "F"
                    print_tablero(self.tableroEnemigo, self.tableroJugador)
                    self.barcosJugadorHundidos += 1
                    print("Tu oponente le dio a un barco tuyo!\n")
                    self.GameOver()
                    if self.barcosJugadorHundidos < NUM_BARCOS:
                        print("\nEs el turno del oponente de nuevo")
                        input("\nIngresa cualquier tecla para continuar ")
                elif self.tableroJugador[self.filaAtaqueOponente][self.colAtaqueOponente] == " ":
                    self.tableroJugador[self.filaAtaqueOponente][self.colAtaqueOponente] = "X"
                    print_tablero(self.tableroEnemigo, self.tableroJugador)
                    print("Tu oponente falló!")
                    self.turnoJugador = True
                    print('\nEs tu turno!')
                    input("Ingresa cualquier tecla para continuar ")

    def bombas(self, eleccion):
        # Este while sirve para que el jugador solo pueda atacar a casillas nuevas en cada turno
        self.sePuedeAtacar = False
        while not self.sePuedeAtacar:
            print("\n¿A qué casilla enemiga debemos atacar?")
            print_tablero(self.tableroEnemigo, self.tableroJugador)
            print("\nIngresa la coordenada de la forma \"Columna(letra), Fila(numero)\"")
            self.coordenadaAtacar = input("Ingresa la coordenada:")
            self.coordenadaAtacar = self.coordenadaAtacar.replace(" ", "")
            self.coordenadaAtacar = self.coordenadaAtacar.split(",")

            if len(self.coordenadaAtacar) != 2 or not self.coordenadaAtacar[1].isdigit():
                print("\n\nPor favor, elige una coordenada válida")
            elif self.convertToNumber.get(self.coordenadaAtacar[0], "Inexiste") == "Inexiste":
                print("\n\nPor favor, elige una coordenada válida")
            else:
                self.filaAtacar = int(self.coordenadaAtacar[1])
                self.colAtacar = self.coordenadaAtacar[0]
            
                if not 0<=self.filaAtacar < self.filas or not 0<=self.convertToNumber[
                        self.colAtacar] < self.cols:
                    print("\n\nPor favor, elige una coordenada válida")

                else:
                    col = self.convertToNumber[self.colAtacar]
                    # Solo cuando se elija una casilla que no se ha atacado, se podrá seguir
                    if self.tableroEnemigo[self.filaAtacar][col] == "X" or self.tableroEnemigo[
                            self.filaAtacar][col] == "F":
                        print("\n\nEsta casilla ya fue atacada, por favor elige otra") 
                    
                    else:
                        self.sePuedeAtacar = True

        if eleccion == "0":
            # Bomba regular
            # Si le da a un barco, se reemplaza la B por F y se repite el turno
            if self.tableroEnemigo[int(self.filaAtacar)][
                    int(self.convertToNumber[self.colAtacar])] == "B":
                self.tableroEnemigo[int(self.filaAtacar)][
                    int(self.convertToNumber[self.colAtacar])] = "F"
                self.barcosEnemigosHundidos += 1
                print_tablero(self.tableroEnemigo, self.tableroJugador)
                print("¡Acertaste a un barco!\n")
                self.GameOver()
                if self.barcosEnemigosHundidos < NUM_BARCOS:
                    print("Tienes otro turno")
                    input("\nIngresa cualquier tecla para pasar al siguiente turno")
            else:
                self.tableroEnemigo[int(self.filaAtacar)][
                    int(self.convertToNumber[self.colAtacar])] = "X"
                self.turnoJugador = False
                print_tablero(self.tableroEnemigo, self.tableroJugador)
                print("Fallaste :(!")
                print("\nLe toca a tu oponente")
                input("\nIngresa cualquier tecla para pasar al siguiente turno ")

        elif eleccion == '1':
            # Bomba cruz
            self.barcosAcertados = 0
            # Este for sirve para agregar a todos los cuadros que se ven afectados horizontalmente
            for cell in range(-RADIO_EXP, RADIO_EXP - 1):
                col = int(self.convertToNumber[self.colAtacar])  # columna a atacar
                row = int(self.filaAtacar)  # fila a atacar
                # Atacar la columna
                if 0 <= int(col + 1 + cell) < self.cols:
                    if self.tableroEnemigo[row][col + 1 + cell] == "B":

                        self.tableroEnemigo[row][col + 1 + cell] = "F"
                        self.barcosEnemigosHundidos += 1
                        self.barcosAcertados += 1
                    elif self.tableroEnemigo[row][col + 1 + cell] == "F":
                        pass
                    else:
                        self.tableroEnemigo[row][col + 1 + cell] = "X"

                # Ahora se hace para la fila atacada
                if 0 <= int(row + 1 + cell) < self.filas:

                    if self.tableroEnemigo[row + 1 + cell][col] == "B":

                        self.tableroEnemigo[row + 1 + cell][col] = "F"
                        self.barcosEnemigosHundidos += 1
                        self.barcosAcertados += 1
                    elif self.tableroEnemigo[row + 1 + cell][col] == "F":
                        pass
                    else:
                        self.tableroEnemigo[row + 1 + cell][col] = "X"

            # Si le da a barcos, tiene otro turno
            if self.barcosAcertados > 0:
                print_tablero(self.tableroEnemigo, self.tableroJugador)
                print("¡Acertaste a", self.barcosAcertados, "barco(s)!")
                if self.barcosEnemigosHundidos >= NUM_BARCOS:
                    self.GameOver
                else:
                    input("Tienes otro turno\nIngresa cualquier botón para continuar")
            else:
                print_tablero(self.tableroEnemigo, self.tableroJugador)
                print("No acertaste a ningún barco :(")
                self.turnoJugador = False
                input("Es turno de tu oponente\nIngresa cualquier tecla para continuar")
        elif eleccion == '2':
            # Bomba X
            self.barcosAcertados = 0
            # Este for sirve para agregar a todos los cuadros que se ven afectados en cada diagonal

            for cell in range(-RADIO_EXP, RADIO_EXP - 1):
                col = int(self.convertToNumber[self.colAtacar])
                row = int(self.filaAtacar)
                if 0 <= int(col + 1 + cell) < self.cols and 0 <= int(row + 1 + cell) < self.filas:
                    # Se ataca la primera diagonal
                    if self.tableroEnemigo[row + 1 + cell][col + 1 + cell] == "B":

                        self.tableroEnemigo[row + 1 + cell][col + 1 + cell] = "F"
                        self.barcosEnemigosHundidos += 1
                        self.barcosAcertados += 1
                    elif self.tableroEnemigo[row + 1 + cell][col + 1 + cell] == "F":
                        pass
                    else:
                        self.tableroEnemigo[row + 1 + cell][col + 1 + cell] = "X"

                # Se ataca la segunda diagonal
                if 0 <= int(col + 1 + cell) < self.cols and 0 <= int(row - 1 - cell) < self.filas:

                    if self.tableroEnemigo[row - 1 - cell][col + 1 + cell] == "B":

                        self.tableroEnemigo[row - 1 - cell][col + 1 + cell] = "F"
                        self.barcosEnemigosHundidos += 1
                        self.barcosAcertados += 1
                    elif self.tableroEnemigo[row - 1 - cell][col + 1 + cell] == "F":
                        pass
                    else:
                        self.tableroEnemigo[row - 1 - cell][col + 1 + cell] = "X"
            # Si le da a un barco, tiene otro turno
            if self.barcosAcertados > 0:
                print_tablero(self.tableroEnemigo, self.tableroJugador)
                print("¡Acertaste a", self.barcosAcertados, "barco(s)!")
                if self.barcosEnemigosHundidos >= NUM_BARCOS:
                    self.GameOver
                else:
                    input("Tienes otro turno\nIngresa cualquier botón para continuar")
            else:
                print_tablero(self.tableroEnemigo, self.tableroJugador)
                print("No acertaste a ningún barco :(")
                self.turnoJugador = False
                input("Es turno de tu oponente\nIngresa cualquier tecla para continuar")
            pass
        elif eleccion == '3':
            # Bomba diamante
            self.barcosAcertados = 0
            # Con estos for, primero (con el de adentro) se eliminan las casillas horizontalmente
            # y después se repite el proceso cada vez con menos en las filas afectadas.
            for verticalCell in range(RADIO_EXP):
                for cell in range(-RADIO_EXP + verticalCell, RADIO_EXP - 1 - verticalCell):
                    col = int(self.convertToNumber[self.colAtacar])
                    row = int(self.filaAtacar)
                    if 0 <= int(
                            col + 1 + cell) < self.cols and 0 <= row - verticalCell < self.filas:

                        if self.tableroEnemigo[int(self.filaAtacar) - verticalCell][
                                col + 1 + cell] == "B":

                            self.tableroEnemigo[int(self.filaAtacar) - verticalCell][
                                col + 1 + cell] = "F"
                            self.barcosEnemigosHundidos += 1
                            self.barcosAcertados += 1
                        elif self.tableroEnemigo[int(self.filaAtacar) - verticalCell][
                                col + 1 + cell] == "F":
                            pass
                        else:
                            self.tableroEnemigo[int(self.filaAtacar) - verticalCell][
                                col + 1 + cell] = "X"

                    if 0 <= int(
                            col + 1 + cell) < self.cols and 0 <= row + verticalCell < self.filas:

                        if self.tableroEnemigo[int(self.filaAtacar) + verticalCell][
                                col + 1 + cell] == "B":

                            self.tableroEnemigo[int(self.filaAtacar) + verticalCell][
                                col + 1 + cell] = "F"
                            self.barcosEnemigosHundidos += 1
                            self.barcosAcertados += 1
                        elif self.tableroEnemigo[int(self.filaAtacar) + verticalCell][
                                col + 1 + cell] == "F":
                            pass
                        else:
                            self.tableroEnemigo[int(self.filaAtacar) + verticalCell][
                                col + 1 + cell] = "X"

            if self.barcosAcertados > 0:
                print_tablero(self.tableroEnemigo, self.tableroJugador)
                print("¡Acertaste a", self.barcosAcertados, "barco(s)!")
                if self.barcosEnemigosHundidos >=NUM_BARCOS:
                    self.GameOver()
                else:
                    input("Tienes otro turno\nIngresa cualquier botón para continuar")
            else:
                print_tablero(self.tableroEnemigo, self.tableroJugador)
                print("No acertaste a ningún barco :(")
                self.turnoJugador = False
                input("Es turno de tu oponente\nIngresa cualquier tecla para continuar")
            pass

    def GameOver(self):
        # Se calcula el puntaje
        self.puntaje = max(0, self.filas * self.cols * NUM_BARCOS * (
                self.barcosEnemigosHundidos - self.barcosJugadorHundidos))
        # Se revisa si el jugador ganó, perdió o se rindió
        if self.barcosJugadorHundidos >= NUM_BARCOS:
            print('\n\nGAME OVER \nPerdiste :( \nPuntaje:', self.puntaje)
            self.run = False
            saveScore(self.apodo, self.puntaje)
            input("\n\nIngresa cualquier botón para volver al menu principal ")
        elif self.barcosEnemigosHundidos >= NUM_BARCOS:
            print('\n\nGAME OVER \nGANASTE! \nPuntaje:', self.puntaje)
            self.run = False
            saveScore(self.apodo, self.puntaje)
            input("\n\nIngresa cualquier botón para volver al menu principal ")
        elif self.rendirse:
            print('\n\nGAME OVER \nTe rendiste. \nPuntaje:', self.puntaje)
            self.run = False
            saveScore(self.apodo, self.puntaje)
            input("\n\nIngresa cualquier botón para volver al menu principal ")
        elif self.salirPrograma:
            print('\n\nGAME OVER \nSaliste del juego. \n')
            self.run = False
