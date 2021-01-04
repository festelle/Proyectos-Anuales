from ObjectsAndDef import game
from ObjectsAndDef import rankingPuntajes

run = True


# Es el loop principal del juego
def menuRunning():
    global run
    
    while run:
        print("***** Menu de Inicio ***** \n Seleccione una opción: ")
        print(" [0] Iniciar una Partida \n [1] Ranking de puntajes \n [2] Salir")
        seleccion = input("Indique su opción (0, 1 ó 2):  ")

        if seleccion == "0":
            # Selección de apodo
            apodo = input("Antes de comenzar, elige un apodo: ")
            while not apodo.isalnum() or len(apodo)<5:
                print("\nElige un apodo válido o vuelve al menú principal")
                print("*Apodo válido: Sólo números y letras, de un largo mayor a 4 caracteres")
                print("\n[0] Elegir apodo \n[1] Volver al menú principal")
                seleccion = input("Indique su opción (0 ó 1): ")
                if seleccion == '0':
                    apodo = input("Elige un apodo válido: ")
                elif seleccion == '1':
                    break
                else:
                    print("\nPor favor elige una opción válida\n")

            # Seleccion de filas y columnas para el tablero
            if apodo.isalnum():
                print("\nBienvenido,", apodo, "\nPor favor, inserte el número de filas y columnas")
                filas = input("Filas (entre 3 y 15): ")
                while not filas.isdigit() or not 3 <= int(filas) <= 15:
                    filas = input(
                        'por favor escoge un número de filas válido \nFilas (entre 3 y 15): ')

                cols = input("Columnas (entre 3 y 15):  ")
                while not cols.isdigit() or not 3 <= int(cols) <= 15:
                    cols = input(
                        'por favor escoge un número de columnas válido \nColumnas (entre 3 y 15): ')

                # Enviar al juego
                juego = game(filas, cols, apodo)
                juego.run = True
                juego.running()
                if juego.salirPrograma:
                    run = False

        elif seleccion == '1':
            # Mostrar top 5 puntajees
            print("Ganadores históricos:")
            rankingPuntajes()
            seleccion = input("\nIngresa 0 para volver al menú principal:  ")
            while seleccion != '0':
                seleccion = input("\nIngresa 0 para volver al menú principal:  ")

        elif seleccion == "2":
            # Salir del juego
            run = False
        else:
            # En caso que no ingresan ninguna opción válida
            print("\nPor favor elige una opción válida\n")


menuRunning()
