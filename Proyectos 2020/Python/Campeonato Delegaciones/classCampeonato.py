
from Objetos import IEEEsparta, atletismo, ciclismo, gimnasia, natacion
from beautifultable import BeautifulTable
import random
from abstractClass import escribirBitacora

#En este archivo está la clase campeonato, que junta la mayoría de las clases hechas anteriormente
# para poder simular el campeonato.

class campeonato():
    def __init__(self,*args):
        super().__init__()
        self.diaActual = 0
        self.medallero = {"DCCrotona": 0, "IEEEsparta": 0}
        self.medallasUsuario = {'atletismo':0,'ciclismo':0,'gimnasia':0,'natacion':0}
        self.medallasRival = {'atletismo':0,'ciclismo':0,'gimnasia':0,'natacion':0}
    
    def realizarCompetencia(self, usuario, rival):
        #Primero se muestra el nivel de la moral
        self.diaActual += 1
        print('\n******* DIA DE COMPETENCIAS *******')
        self.calcularNivelMoralDelegaciones(usuario,rival)

        equipoUsuario = {'atletismo':'','ciclismo':'','gimnasia':'','natacion':''}
        equipoRival = {'atletismo':'','ciclismo':'','gimnasia':'','natacion':''}

        #Se debe elegir qué deportista participará. 
        for deporte in equipoUsuario:
            print(f'\n¿Qué deportista quieres que participe en {deporte}?')
            for i in range(len(usuario.equipo)):
                if usuario.equipo[i].lesionado:
                    print(f'[{i}] {usuario.equipo[i].nombre} (lesionado)')
                else:
                    print(f'[{i}] {usuario.equipo[i].nombre}')
            seleccion = input('\nIngresa el deportista: ')
            while not seleccion.isdigit() or not 0<=int(seleccion)<len(usuario.equipo):
                seleccion = input('Ingresa una opción válida: ')
            equipoUsuario[deporte] = usuario.equipo[int(seleccion)]

            #Ahora se seleccionan al azar los deportistas para el rival
            seleccionRival = random.randint(0,len(rival.equipo)-1)
            equipoRival[deporte] = rival.equipo[seleccionRival]
        print(f'\n**** Participantes ****\n\nDelegación{usuario.nombreDelegacion}:')
        for deporte in equipoUsuario:
            print(f'{deporte}: {equipoUsuario[deporte].nombre}')
        print(f'\nDelegación{rival.nombreDelegacion}:')
        for deporte in equipoRival:
            print(f'{deporte}: {equipoRival[deporte].nombre}')
        input('\nIngresa cualquier tecla para comenzar las competencias')
        print(f'\n ********** RESULTADOS DIA {self.diaActual} **********')

        #Para cada deporte se calcula el ganador, se premia al deportista y su delegación
        # y se escribe el resultado en la bitácora
        ganadorAtletismo = atletismo().calcularGanador(equipoUsuario['atletismo'],\
            equipoRival['atletismo'],usuario, rival)

        if ganadorAtletismo == equipoUsuario['atletismo']:
            self.premiarDeportistasYDelegaciones(equipoUsuario['atletismo'],equipoRival[
                'atletismo'],usuario,rival)
            escribirBitacora(self.diaActual,'Atletismo',equipoUsuario[
                'atletismo'].nombre,usuario.nombreDelegacion)
            self.medallasUsuario['atletismo'] += 1

        elif ganadorAtletismo == equipoRival['atletismo']:
            self.premiarDeportistasYDelegaciones(equipoRival['atletismo'],equipoUsuario[
                'atletismo'],rival,usuario)

            escribirBitacora(self.diaActual,'Atletismo',equipoRival[
                'atletismo'].nombre,rival.nombreDelegacion)
            self.medallasRival['atletismo'] += 1

        else: #Empate
            escribirBitacora(self.diaActual,'Atletismo','EMPATE','---')

        
        ganadorCiclismo = ciclismo().calcularGanador(equipoUsuario['ciclismo'],equipoRival[
            'ciclismo'],usuario, rival)

        if ganadorCiclismo == equipoUsuario['ciclismo']:
            self.premiarDeportistasYDelegaciones(equipoUsuario['ciclismo'],equipoRival[
                'ciclismo'],usuario,rival)
            escribirBitacora(self.diaActual,'Ciclismo',equipoUsuario[
                'ciclismo'].nombre,usuario.nombreDelegacion)
            self.medallasUsuario['ciclismo'] += 1

        elif ganadorCiclismo == equipoRival['ciclismo']:
            self.premiarDeportistasYDelegaciones(equipoRival['ciclismo'],equipoUsuario[
                'ciclismo'],rival,usuario)
            escribirBitacora(self.diaActual,'Ciclismo',equipoRival[
                'ciclismo'].nombre,rival.nombreDelegacion)
            self.medallasRival['ciclismo'] += 1

        else:
            escribirBitacora(self.diaActual,'Ciclismo','EMPATE','---')


        ganadorGimnasia = gimnasia().calcularGanador(equipoUsuario['gimnasia'],equipoRival[
            'gimnasia'],usuario, rival)

        if ganadorGimnasia == equipoUsuario['gimnasia']:
            self.premiarDeportistasYDelegaciones(equipoUsuario['gimnasia'],equipoRival[
                'gimnasia'],usuario,rival)
            escribirBitacora(self.diaActual,'Gimnasia',equipoUsuario[
                'gimnasia'].nombre,usuario.nombreDelegacion)
            self.medallasUsuario['gimnasia'] += 1

        elif ganadorGimnasia == equipoRival['gimnasia']:
            self.premiarDeportistasYDelegaciones(equipoRival['gimnasia'],equipoUsuario[
                'gimnasia'],rival,usuario)
            escribirBitacora(self.diaActual,'Gimnasia',equipoRival[
                'gimnasia'].nombre,rival.nombreDelegacion)
            self.medallasRival['gimnasia'] += 1

        else:
            escribirBitacora(self.diaActual,'Gimnasia','EMPATE','---')


        ganadorNatacion = natacion().calcularGanador(equipoUsuario['natacion'],equipoRival[
            'natacion'],usuario, rival)

        if ganadorNatacion == equipoUsuario['natacion']:
            self.premiarDeportistasYDelegaciones(equipoUsuario['natacion'],equipoRival[
                'natacion'],usuario,rival)
            escribirBitacora(self.diaActual,'Natacion',equipoUsuario[
                'natacion'].nombre,usuario.nombreDelegacion)
            self.medallasUsuario['natacion'] += 1

        elif ganadorNatacion == equipoRival['natacion']:
            self.premiarDeportistasYDelegaciones(equipoRival['natacion'],equipoUsuario[
                'natacion'],rival,usuario)
            escribirBitacora(self.diaActual,'Natacion',equipoRival[
                'natacion'].nombre,rival.nombreDelegacion)
            self.medallasRival['natacion'] += 1

        else:
            escribirBitacora(self.diaActual,'Gimnasia','EMPATE','---')

        input('Ingresa cualquier tecla para avanzar al siguiente día ')
        self.diaActual += 1
        #Cuando se avanza al siguiente día, se vuelven a mostrar las morales
        print('\n******* DIA DE ENTRENAMIENTO *******')
        self.calcularNivelMoralDelegaciones(usuario, rival)

    
    def premiarDeportistasYDelegaciones(self, d1, d2, delegacion1, delegacion2):
        d1.moral += 20 * delegacion1.aumentoMoral
        d2.moral -= 10 * delegacion2.disminucionMoral
        delegacion2.excelenciaYRespeto -= 0.02
        delegacion1.excelenciaYRespeto += 1
        delegacion1.dinero += 100
        delegacion1.medallas += 1
        self.medallero[delegacion1.nombreDelegacion] += 1

    def calcularNivelMoralDelegaciones(self,usuario, rival):
        sumaMorales = 0
        for deportista in usuario.equipo:
            sumaMorales += deportista.moral
        usuario.moral = round(sumaMorales/len(usuario.equipo),2)

        sumaMorales = 0
        for deportista in rival.equipo:
            sumaMorales += deportista.moral
        rival.moral = round(sumaMorales/len(rival.equipo),2)
        
        print(f'\n----- MORAL DE CADA DELEGACION -----          Día: {self.diaActual}')
        print(f'\nMoral {usuario.nombreDelegacion} (tú): {usuario.moral}')
        print(f'Moral {rival.nombreDelegacion}: {rival.moral}')

        input('\nIngresa cualquier tecla para continuar ')

    
    def mostrarEstadoDelegacion(self, IEE, DCC):
        print('\n**** ESTADO DE LAS DELEGACIONES Y DEPORTISTAS ****')
        print('--------------------------------------------------')
        print(f'\nIEEEsparta\nEntrenador: {IEE.entrenador}\nMoral del equipo: {IEE.moral}')
        print(f'Medallas: {IEE.medallas}\nDinero: {IEE.dinero}\
            \nExcelencia y Respeto: {IEE.excelenciaYRespeto}\
            \nImplementos Deportivos: {IEE.implementosDeportivos}\
            \nImplementos Médicos: {IEE.implementosMedicos}')
        print('\nEquipo deportivo')
        
        #Se crea una tabla donde estén todos los datos de los deportistas usando el módulo
        #beautifultable, función Beautifultable
        tabla = BeautifulTable()
        for i in IEE.equipo:
            tabla.rows.append([i.nombre, i.moral,i.velocidad, i.resistencia, i.flexibilidad, str(
                i.lesionado)])

        tabla.columns.header = [
            'Nombre deportista','Moral','Velocidad','Resistencia','Flexibilidad','Lesión']

        print(tabla)
        print('\n***************************************************')
        print(f'\nDCCrotona\nEntrenador: {DCC.entrenador}\nMoral del equipo: {DCC.moral}')
        print(f'Medallas: {DCC.medallas}\nDinero: {DCC.dinero}\
            \nExcelencia y Respeto: {DCC.excelenciaYRespeto}\
            \nImplementos Deportivos: {DCC.implementosDeportivos}\
            \nImplementos Médicos: {DCC.implementosMedicos}')
        print('\nEquipo deportivo')

        tabla = BeautifulTable()
        for i in DCC.equipo:
            tabla.rows.append([
                i.nombre, i.moral, i.velocidad, i.resistencia, i.flexibilidad, str(i.lesionado)])
        tabla.columns.header = [
            'Nombre deportista','Moral','Velocidad','Resistencia','Flexibilidad','Lesión']
        print(tabla)
        print('--------------------------------------------------')
        print(f'\nMedallero:                             Día: {self.diaActual}')
        t = BeautifulTable()
        t.rows.append([self.medallasUsuario['atletismo'],self.medallasRival['atletismo']])
        t.rows.append([self.medallasUsuario['ciclismo'],self.medallasRival['ciclismo']])
        t.rows.append([self.medallasUsuario['gimnasia'],self.medallasRival['gimnasia']])
        t.rows.append([self.medallasUsuario['natacion'],self.medallasRival['natacion']])
        t.rows.header= ['Atletismo','Ciclismo','Gimnasia','Natacion']
        t.columns.header = [IEE.nombreDelegacion, DCC.nombreDelegacion]

        print(t)

        input('\nIngresa cualquier tecla para volver al menú ')
    

