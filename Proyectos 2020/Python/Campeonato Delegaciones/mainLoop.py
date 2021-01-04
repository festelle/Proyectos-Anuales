
import Objetos as o
from Diccionarios import DCCrotonaInicial, IEEEspartaInicial, dictDeportistas, dictDeportistaNuevo
from classCampeonato import campeonato
from parametros import DIAS_COMPETENCIA

#En este archivo se dejará la clase menú, después se correrá un objeto hecho de esta clase y
# con esto se correrá todo el juego



class menu():
    def __init__(self, campeonatoOficial, DIAS_COMPETENCIA, DCCrotonaInicial, IEEEspartaInicial, dictDeportistas):

        self.menuInicio_run = True
        self.menuPrincipal_run = True
        self.menuEntrenador_run = True
        self.nombreUsuario = ''
        self.nombreRival = ''
        self.delegacionUsuario = ''
        self.rival = ''
        self.usuario = ''
        self.campeonatoOficial = campeonatoOficial
        self.DIAS_COMPETENCIA = DIAS_COMPETENCIA
        self.DCCrotonaInicial = DCCrotonaInicial
        self.IEEEspartaInicial = IEEEspartaInicial
        self.dictDeportistas = dictDeportistas

    def inicio(self):
        self.menuInicio_run = True
        #Mientras no se salga del juego, se seguirá repitiendo este loop
        while self.menuInicio_run:
            print('\n**** MENU DE INICIO ****')
            print('elige una opción: \n[0] Comenzar una partida nueva \n[1]Salir del programa')
            menuInicio_seleccion = input('Ingresa tu opción: ')
            while menuInicio_seleccion!= '0' and menuInicio_seleccion!= '1':
                print('por favor, elige una opción válida')
                menuInicio_seleccion = input('Ingresa tu opción: ')
            
            if menuInicio_seleccion == '0': #Comenzar partida nueva
                print('\nElige un nombre de usuario y nombre de rival (carácteres alfanuméricos)')
                self.nombreUsuario = input('Nombre de usuario: ')
                self.nombreRival = input('Nombre de tu rival: ')
                while not self.nombreUsuario.isalnum() or not self.nombreRival.isalnum():
                    print('\npor favor, elige nombres con caracteres alfanuméricos')
                    self.nombreUsuario = input('Nombre de usuario: ')
                    self.nombreRival = input('Nombre de tu rival: ')
                self.nombreRival = self.nombreRival.lower()
                self.nombreUsuario = self.nombreUsuario.lower()
                print('\n¿Qué delegación quieres ser?\n[0]DCCrotona\n[1]IEEEsparta')
                self.delegacionUsuario = input('Ingresa tu elección: ')
                while self.delegacionUsuario != '0' and self.delegacionUsuario != '1':
                    self.delegacionUsuario = input('Por favor, elige una opción válida:')
                if self.delegacionUsuario == '0': #Eligió DCCrotona
                    self.usuario = o.DCCrotona(self.nombreUsuario,self.DCCrotonaInicial[
                        'Equipo'],self.DCCrotonaInicial['Medallas'],self.DCCrotonaInicial['Dinero'])
                    self.rival = o.IEEEsparta(self.nombreRival,self.IEEEspartaInicial[
                        'Equipo'],self.IEEEspartaInicial['Medallas'],self.IEEEspartaInicial['Dinero'])
                else: #Eligió IEEEsparta
                    self.rival = o.DCCrotona(self.nombreUsuario,self.DCCrotonaInicial['Equipo'],
                        self.DCCrotonaInicial['Medallas'],self.DCCrotonaInicial['Dinero'])
                    self.usuario = o.IEEEsparta(self.nombreRival,self.IEEEspartaInicial['Equipo'],
                        self.IEEEspartaInicial['Medallas'],self.IEEEspartaInicial['Dinero'])
                #Una vez que pasa al siguiente menú, ya se tiene hecha la delegación propia y rival.
                self.principal()

            elif menuInicio_seleccion == '1':
                self.menuInicio_run = False

    def principal(self): #Menú principal
        self.menuPrincipal_run = True
        while self.menuPrincipal_run:
            print(f'\n**** MENU PRINCIPAL ****             Día:{self.campeonatoOficial.diaActual}')
            print('Bienvenido,', self.nombreUsuario)
            print('[0]Menú entrenador\n[1]Simular competencias\n[2]Mostrar estado\
                \n[3]Salir del programa\n[4]Volver al menú de inicio (empezar de nuevo)')
            menuPrincipal_seleccion = input('Ingresa tu decisión: ')
            while not menuPrincipal_seleccion.isdigit() or  not 0 <= int(
                    menuPrincipal_seleccion) <= 4:
                menuPrincipal_seleccion = input('Elige una opción válida: ')
            menuPrincipal_seleccion = int(menuPrincipal_seleccion)
            if menuPrincipal_seleccion == 0:
                self.entrenador() #Se manda al menu entrenador
            elif menuPrincipal_seleccion == 1:
                self.campeonatoOficial.realizarCompetencia(self.usuario,self.rival)
                #Se revisa si el campeonato ya terminó 
                self.finalizarCampeonato()
            elif menuPrincipal_seleccion == 2:
                if self.delegacionUsuario == '0': #Eligió Crotona
                    self.campeonatoOficial.mostrarEstadoDelegacion(self.rival, self.usuario)
                else: #Eligió IEEEsparta (el orden de entrada para esta función importa)
                    self.campeonatoOficial.mostrarEstadoDelegacion(self.usuario, self.rival)
            elif menuPrincipal_seleccion == 3: #Se sale del programa
                self.menuPrincipal_run = False
                self.menuInicio_run = False
                
            elif menuPrincipal_seleccion == 4: #Se vuelve a iniciar
                self.menuPrincipal_run = False
    
    def entrenador(self): #Menú entrenador
        self.menuEntrenador_run = True
        while self.menuEntrenador_run:
            print(f'\n**** MENU ENTRENADOR ****      Dinero: {self.usuario.dinero}')
            print('[0]Fichar\n[1]Entrenar\n[2]Sanar\n[3]Comprar Tecnología')
            print('[4]Usar habilidad especial\n[5]Volver al menu anterior\n[6]Salir del programa')
            seleccion = input('Ingresa tu opción: ')
            while not seleccion.isdigit() or not 0<= int(seleccion) <=6:
                seleccion = input('Elige una opción válida: ')
            seleccion = int(seleccion)
            if seleccion == 0: #Fichar deportista
                if self.usuario.moral > 20: #Cumple condición de moral?
                    print('-- Deportistas disponibles --')
                    dictComprasDisponibles = {}
                    nro = 0
                    for i in self.dictDeportistas: #Se imprime los posibles deportistas a fichar
                        dictComprasDisponibles[nro] = i
                        print(f'[{nro}] {i}  Precio:{self.dictDeportistas[i].precio}')
                        nro += 1
                    print(f'[{nro}] Volver al menú')
                    deportistaAComprar = input('¿Qué deportista quieres fichar?: ')
                    while not deportistaAComprar.isdigit() or not 0<= int(deportistaAComprar)<=nro:
                        deportistaAComprar = input('Ingresa una opción válida: ')
                    if int(deportistaAComprar) == nro: #Volver al menú anterior
                        pass
                    else:
                        #Se revisa si el usuario tiene suficiente dinero para comprarlo
                        precio = int(self.dictDeportistas[dictComprasDisponibles[
                            int(deportistaAComprar)]].precio)
                        if int(self.usuario.dinero) >= precio:
                            #Se compra el deportista
                            deportistaAComprar = self.dictDeportistas[dictComprasDisponibles[
                                int(deportistaAComprar)]]
                            self.usuario.ficharDeportistas(deportistaAComprar,self.dictDeportistas)
                            input('Ingresa cualquier tecla para volver al menú ')
                        else: #Si no alcanza el dinero, se devuelve al menu anterior
                            print('\nNo tienes suficiente dinero')
                            print(f'dinero disponible: {self.usuario.dinero}')
                            input('Ingresa cualquier tecla para volver ')
                else: #Si la moral es baja, devuelve al menu anterior
                    print('\nLa moral de tu equipo es demasiado baja')
                    print(f'moral mínima: 20.1     moral de tu equipo:{self.usuario.moral}')
                    input('Ingresa cualquier tecla para volver ')

            elif seleccion == 1: #Entrenar deportista
                if self.usuario.dinero >= 30:
                    print('\n¿A qué deportista quieres entrenar?\n')
                    #Se imprimen las opciones
                    for i in range(len(self.usuario.equipo)):
                        print(f'[{i}] {self.usuario.equipo[i].nombre}')
                    print('[99] Volver al menú')
                    seleccion = input('\nIngresa tu selección: ')
                    while not seleccion.isdigit() or not 0<= int(seleccion) < len(
                            self.usuario.equipo) and not seleccion == '99':
                        seleccion = input('Elige una opción válida: ')
                    seleccion = int(seleccion)
                    if seleccion == 99: #Devolverse al menu anterior
                        pass
                    else:
                        #Se entrena el deportista
                        self.usuario.entrenarDeportistas(self.usuario.equipo[seleccion])
                        input('Ingresa cualquier tecla para regresar al menú ')
                else:
                    input('No tienes suficiente dinero \nIngresa cualquier tecla para volver ')

            elif seleccion == 2: #Sanar deportista
                print('')
                for i in range(len(self.usuario.equipo)):
                    if self.usuario.equipo[i].lesionado:
                        print(f'[{i}] {self.usuario.equipo[i].nombre} (Lesionado)')
                    else:
                        print(f'[{i}] {self.usuario.equipo[i].nombre}')
                seleccion = input('\n¿A quién quieres sanar? ')
                while not seleccion.isdigit() or not 0 <= int(seleccion) <= len(
                        self.usuario.equipo):
                    seleccion = input('Ingresa una opción válida ')
                seleccion = int(seleccion)
                #Se sana al deportista elegido (en la función se revisa si cumple las condiciones)
                self.usuario.sanarLesiones(self.usuario.equipo[seleccion])
                
            elif seleccion == 3: #Comprar tecnología
                self.usuario.comprarTecnologia()

            elif seleccion == 4: #Utilizar habilidad especial
                self.usuario.utilizarHabilidadEspecial(self.rival, self.campeonatoOficial)
                input('Ingresa cualquier tecla para volver ')

            elif seleccion == 5: #Volver al menu anterior
                self.menuEntrenador_run = False

            elif seleccion == 6: #Salir del programa
                self.menuEntrenador_run = False
                self.menuInicio_run = False
                self.menuPrincipal_run = False
    

    def finalizarCampeonato(self):
        #Revisa si ya pasaron los días necesarios para que el campeonato termine
        #Si es así, imprime los resultados y anuncia el ganador
        if self.campeonatoOficial.diaActual >= self.DIAS_COMPETENCIA:
            self.menuEntrenador_run = False
            self.menuPrincipal_run = False
            print('\n\n---------- RESULTADOS CAMPEONATO ----------\n')
            print('Medallas:')
            
            for i in self.campeonatoOficial.medallero:
                print(f'{i}: {self.campeonatoOficial.medallero[i]}')
            
            if self.campeonatoOficial.medallero['DCCrotona'] > self.campeonatoOficial.medallero['IEEEsparta']:
                ganador = 'DCCrotona'
            
            elif self.campeonatoOficial.medallero['DCCrotona'] < self.campeonatoOficial.medallero['IEEEsparta']:
                ganador = 'IEEEsparta'
            
            else:
                ganador = 'EMPATE'
            print(f'\n\n\n      ----DELEGACION GANADORA----\n              {ganador}    ')

            if self.usuario.nombreDelegacion == ganador:
                print('\n¡Felicidades, tu delegación ganó el campeonato!')
            elif self.rival.nombreDelegacion == ganador:
                print('\n¡Qué mal!, tu delegación perdió el campeonato :(')
            else:
                print('\nUn empate, no es un resultado ni muy bueno ni muy malo')

            #Da la opción de realizar otra simulación o salir
            print('\n\n[0]Realizar otra simulación\n[1]Salir del programa')
            sel = input('\nIngresa tu eleccion: ')
            while not sel.isdigit() or not 0<= int(sel)<=1:
                sel = input('Elige una opción válida')

            if sel == '0': #Se crea otra simulación
                self.campeonatoOficial.diaActual = 0
                print('\Creando otra simulación\n')
                nuevosDict = dictDeportistaNuevo()
                DCCrotonaInicial = nuevosDict[0]
                IEEEspartaInicial = nuevosDict[1]
                dictDeportistas = nuevosDict[2]
                campeonatoOficial = campeonato('chao')
                menu(campeonatoOficial, DIAS_COMPETENCIA, DCCrotonaInicial, IEEEspartaInicial, \
                nuevosDict[2])
                
            elif sel == '1': #Se sale del juego
                print('\nSaliendo del juego..\n')
                self.menuInicio_run = False
                

            
            
            

campeonatoOficial = campeonato('hola')
#Se crea el juego 

juego = menu(campeonatoOficial, DIAS_COMPETENCIA, DCCrotonaInicial, IEEEspartaInicial, \
    dictDeportistas)
juego.inicio()