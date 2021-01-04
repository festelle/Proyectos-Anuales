from abc import ABC, abstractmethod
import parametros as p
import random
import os
#En este archivo están las clases abstractas necesarias para después ser heredadas
class Delegacion(ABC):
    def __init__(self, entrenador, equipo, medallas, dinero):
        super().__init__()
        self.nombreDelegacion = '' #str
        self.entrenador = entrenador #str
        self.equipo = equipo #list
        self.medallas = int(medallas)
        self.morales = 0
        for i in equipo:
            self.morales += int(i.moral)
        self.__moral = round(int(self.morales/len(equipo)), 2)
        self.dinero = int(dinero)
        #Estos atributos se tienen que sobreescribir
        self.__implementosDeportivos = 0
        self.__excelenciaYRespeto = 0
        self.__implementosMedicos = 0
        self.disminucionMoral = 1
        self.aumentoMoral = 1
        self.pagarPorLesion = 1

    @property
    def moral(self):
        return self.__moral
    @moral.setter
    def moral(self, p):
        if p >= 100:
            self.__moral = 100
        elif p<=0:
            self._moral = 0
        else:
            self.__moral = p

    @property
    def implementosDeportivos(self):
        return self.__implementosDeportivos
    @implementosDeportivos.setter
    def implementosDeportivos(self,p):
        if p >= 1.0:
            self.__implementosDeportivos = 1.0
        elif p < 0:
            self.__implementosDeportivos = 0
        elif p < 1.0:
            self.__implementosDeportivos = p

    @property
    def excelenciaYRespeto(self):
        return self.__excelenciaYRespeto
    @excelenciaYRespeto.setter
    def excelenciaYRespeto(self,p):
        if p >= 1.0:
            self.__excelenciaYRespeto = 1.0
        elif p < 0:
            self.__excelenciaYRespeto = 0
        elif p < 1.0:
            self.__excelenciaYRespeto = p

    @property
    def implementosMedicos(self):
        return self.__implementosMedicos
    @implementosMedicos.setter
    def implementosMedicos(self,p):
        if p >= 1.0:
            self.__implementosMedicos = 1.0
        elif p < 0:
            self.__implementosMedicos = 0
        elif p < 1.0:
            self.__implementosMedicos = p

    def ficharDeportistas(self, deportista, dictDeportistas):
        #Para todas las funciones donde hayan ciertas restricciones, primero se revisa que
        #se cumplan todas las restricciones, si se cumplen la función es hecha, si no, se 
        #avisa que no se puede realizar la acción
        if self.moral > 20 and self.dinero >= int(deportista.precio):
            self.equipo.append(deportista)
            self.dinero -= int(deportista.precio)
            del dictDeportistas[deportista.nombre]
            print(f'\n{deportista.nombre} fichado exitosamente\n')

    def entrenarDeportistas(self, deportista):
        if self.nombreDelegacion == 'IEEEsparta':
            aumentoEntrenamiento = 1.7
        else:
            aumentoEntrenamiento = 1
        if self.dinero >= 30:
            deportista.moral += 1
            deportista.entrenar(aumentoEntrenamiento)
            self.dinero -= 30

    def sanarLesiones(self, deportista):
        if deportista.lesionado and self.dinero>=(30*self.pagarPorLesion):
            self.dinero -= (30*self.pagarPorLesion)
            probabilidad = round(min (1, max(0,(deportista.moral*(
                self.implementosMedicos+self.excelenciaYRespeto)/200))),1)
            aleatorio = random.uniform(0,1)
            if aleatorio <= probabilidad:
                deportista.lesionado = False
                print(f'\n{deportista.nombre} se ha sanado!')
                input('Ingresa cualquier tecla para volver ')
            else:
                print('\nSe hizo lo que se pudo, pero tu deportista no pudo sanar')
                input('Ingresa cualquier tecla para volver ')
        elif self.dinero<30*self.pagarPorLesion:
            print(f'\nTe faltan {self.dinero-(30*self.pagarPorLesion)} DCCoins')
            input('Ingresa cualquier tecla para volver ')
        elif not deportista.lesionado:
            print('\nEste deportista no está lesionado')
            input('Ingresa cualquier tecla para volver ')


    def comprarTecnologia(self):
        #Se revisa si tiene suficiente dinero, si lo tiene, se da la elección de la tecnología
        #y se mejora
        if self.dinero >=20:
            print('\n¿Qué tecnologías quieres mejorar?')
            print('\n[0] Implementos Deportivos\n[1] Implementos médicos\n[2] Volver')
            seleccion= input('Ingresa tu opción: ')
            while not seleccion.isdigit or not 0<=int(seleccion)<=2:
                seleccion = input('Ingresa una opción válida ')
            seleccion = int(seleccion)
            if seleccion == 0:
                self.implementosDeportivos = round(1.1 * self.implementosDeportivos,2)
                self.dinero -= 20
                input('Tecnología mejorada\nIngresa cualquier tecla para volver')
            elif seleccion == 1:
                self.implementosMedicos = round(1.1* self.implementosMedicos,2)
                self.dinero -= 20
                input('Tecnología mejorada\nIngresa cualquier tecla para volver')
            else:
                pass
        else:
            input('No tienes suficiente dinero\nIngresa cualquier tecla para volver ')

    @abstractmethod
    def utilizarHabilidadEspecial(self):
        pass

#Clase abstracta de deporte
class deporte(ABC):
    def __init__(self, implementoONo, riesgo):
        super().__init__()
        self.implemento = implementoONo
        self.__riesgo = int(riesgo)
    @property
    def riesgo(self):
        return self.__riesgo
    @ riesgo.setter
    def riesgo(self,p):
        if p > 1:
            self.__riesgo = 1
        elif p < 0:
            self.__riesgo = 0
        else:
            self.__riesgo = p

    def validezCompetencia(self, deportista1, deportista2, delegacion1, delegacion2):
        #Se empieza asumiendo que ningún deportista es válido para competir
        valido1 = False
        valido2 = False
        #Dependiendo de si el deporte necesita implementos se ve si es válido
        if self.implemento:
            #Primero se revisa si la delegación 1 cumple con los requisitos
            if (str(type(deportista1))=='<class \'Objetos.deportista\'>') and not  \
                deportista1.lesionado and delegacion1.implementosDeportivos > p.NIVEL_IMPLEMENTOS:

                print(f'{deportista1.nombre}({delegacion1.nombreDelegacion}) puede participar')
                valido1 = True

            #Despues se revisa si la delegación 2 cumple los requisitos
            if (str(type(deportista2))=='<class \'Objetos.deportista\'>') and not \
                deportista2.lesionado and delegacion2.implementosDeportivos > p.NIVEL_IMPLEMENTOS:

                print(f'{deportista2.nombre} ({delegacion2.nombreDelegacion}) puede participar')
                valido2 = True
        
        #Se hace lo mismo acá, pero es en el caso que no se necesiten implementos
        elif not self.implemento:
            if (str(type(deportista1))=='<class \'Objetos.deportista\'>') and not \
                deportista1.lesionado:

                print(f'{deportista1.nombre} ({delegacion1.nombreDelegacion}) puede participar')
                valido1 = True

            if (str(type(deportista2))=='<class \'Objetos.deportista\'>') and not \
                deportista2.lesionado:

                print(f'{deportista2.nombre} ({delegacion2.nombreDelegacion}) puede participar')
                valido2 = True

        #Ahora se ve si es válida, si no es válida se ve si hay un ganador o es un empate
        if valido1 and valido2:
            return 'valido'
        elif valido1 and not valido2:
            print(f'{deportista2.nombre} ({delegacion2.nombreDelegacion}) no puede participar')
            return deportista1

        elif not valido1 and valido2:
            print(f'{deportista1.nombre} ({delegacion1.nombreDelegacion}) no puede participar')
            return deportista2

        elif not valido1 and not valido2:
            print(f'Ningún deportista cumple con las condiciones para participar')
            return 'empate'
    

    @abstractmethod
    def calcularGanador(self, deportista1, deportista2):
        pass


#Esta función escribe los resultados de ccada deporte. Como comienza por atletismo,
# cada vez que tenga que escribir el reultado de este deporte lo toma como un nuevo día.
def escribirBitacora(dia, competencia, nombreDeportista, nombreDelegacion):

    
    if competencia == 'Atletismo':

        texto = (f'\n\n***************************************************\
            \nDia: {dia}\n\nCompetencia:{competencia}\nDelegacion ganadora:{nombreDelegacion}\
        \nDeportista ganador: {nombreDeportista}\n')

    else:
        texto = (f'\nCompetencia:{competencia}\nDelegacion ganadora:{nombreDelegacion}\
        \nDeportista ganador: {nombreDeportista}\n')

    #Si el archivo es nuevo o está totalmente en blanco, entonces se pone un encabezado
    with open(p.pathResultados, "a") as archivo:
        if os.stat(p.pathResultados).st_size == 0:
            archivo.write(' ***** RESULTADOS DIA A DIA DCCUMBRE OLIMPICA *****')

        archivo.write(texto)
