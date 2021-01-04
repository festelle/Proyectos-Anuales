from abc import ABC, abstractmethod
import parametros as p
import random
from abstractClass import Delegacion, deporte

# En este archivo estarán los objetos que son necesarios para la tarea

#IEEEsparta y DCCrotona heredan de delegación
class IEEEsparta(Delegacion):
    def __init__(self, entrenador, equipo, medallas, dinero):
        super().__init__(entrenador, equipo, medallas, dinero)
        #Se sobreescriben los atributos para poder cumplir las restricciones de cada delegación
        self.nombreDelegacion = 'IEEEsparta'
        self.excelenciaYRespeto = round(random.uniform(0.4,0.8), 2)
        self.implementosDeportivos = round(random.uniform(0.3,0.7),2)
        self.implementosMedicos = round(random.uniform(0.2,0.6), 2)
        self.habilidadEspecial = True
        #Se especifica que cuando se pierde la moral disminuye el doble
        self.disminucionMoral = 2

    def utilizarHabilidadEspecial(self, delegacionEnemiga, campeonato):
        if self.habilidadEspecial:
            self.habilidadEspecial = False
            print('\n\"Desde lo lejos se escucha un grito\"\nHabilidad especial usada')
            for deportista in self.equipo:
                deportista.moral = 100
            self.moral = 100
            print('Ahora todos tus deportistas tienen su moral al máximo')
        else:
            print('\nYa usaste la habilidad especial')
            

class DCCrotona(Delegacion):
    def __init__(self, entrenador, equipo, medallas, dinero):
        super().__init__(entrenador, equipo, medallas, dinero)
        #Se sobreescriben los atributos para poder cumplir las restricciones de cada delegación
        self.nombreDelegacion = 'DCCrotona'
        self.excelenciaYRespeto = round(random.uniform(0.3,0.7),2)
        self.implementosDeportivos = round(random.uniform(0.2,0.6),2)
        self.implementosMedicos = round(random.uniform(0.4,0.8), 2) 
        self.habilidadEspecial = True
        self.disminucionMoral = 1
        self.aumentoMoral = 2
        self.pagarPorLesion = 2
    
    def utilizarHabilidadEspecial(self, delegacionEnemiga, campeonato):
        if self.habilidadEspecial:
            #Como no hubo ninguna competencia para esta medalla, se eligen al azar los deportistas
            #que serán afectados (para ambas delegaciones)
            d1 = self.equipo[random.randint(0,len(self.equipo)-1)]
            d2 = delegacionEnemiga.equipo[random.randint(0,len(delegacionEnemiga.equipo)-1)]
            d1.moral += 20 * self.aumentoMoral
            d2.moral -= 10 * delegacionEnemiga.disminucionMoral
            delegacionEnemiga.excelenciaYRespeto -= 0.02
            self.excelenciaYRespeto += 1
            self.dinero += 100
            campeonato.medallero[self.nombreDelegacion] += 1
            self.medallas += 1
            print('\n¡Obtuviste una medalla de oro!\n La excelencia y respeto aumentó\n')
        else:
            print('\nYa usaste la habilidad')
        

class deportista():
    def __init__(self, nombre, velocidad, resistencia, flexibilidad, moral, lesionado, precio):
        super().__init__()
        self.nombre = nombre
        self.__velocidad = int(velocidad)
        self.__resistencia = int(resistencia)
        self.__flexibilidad = int(flexibilidad)
        self.__moral = int(moral)
        self.lesionado = lesionado
        self.delegacion = ''
        if self.lesionado == 'True':
            self.lesionado = True
        elif self.lesionado == 'False':
            self.lesionado = False
        self.precio = precio
    @property
    def velocidad(self):
        return self.__velocidad
    @velocidad.setter
    def velocidad(self,p):
        if p > 100:
            self.__velocidad = 100
        elif p < 0:
            self.__velocidad = 0
        else:
            self.__velocidad = p

    @property
    def resistencia(self):
        return self.__resistencia
    @resistencia.setter
    def resistencia(self,p):
        if p > 100:
            self.__resistencia = 100
        elif p < 0:
            self.__resistencia = 0
        else:
            self.__resistencia = p

    @property
    def flexibilidad(self):
        return self.__flexibilidad
    @flexibilidad.setter
    def flexibilidad(self,p):
        if p > 100:
            self.__flexibilidad = 100
        elif p < 0:
            self.__flexibilidad = 0
        else:
            self.__flexibilidad = p
    
    @property
    def moral(self):
        return self.__moral
    @moral.setter
    def moral(self,p):
        if p > 100:
            self.__moral = 100
        elif p < 0:
            self.__moral = 0
        else:
            self.__moral = p

    def entrenar(self, aumentoEntrenamiento):
        #Primero se elige el atributo a entrenar, si no está al máximo se entrena,
        #si está al máximo se avisa de esto.
        print('\n¿Qué atributo entrenar?')
        print('\n[0]Velocidad\n[1]Resistencia\n[2]Flexibilidad')
        atributoAEntrenar = input('Elige un atributo: ')
        while not atributoAEntrenar.isdigit() or not 0<= int(atributoAEntrenar) <=2:
            atributoAEntrenar = input('Elige un atributo válido: ')
        if atributoAEntrenar == '0' and self.velocidad < 100:
            self.velocidad += p.PUNTOS_ENTRENAMIENTO * aumentoEntrenamiento
            if self.velocidad >=100:    self.velocidad = 100
            print(f'Velocidad de {self.nombre} aumentada a: {self.velocidad}')
        elif atributoAEntrenar == '1' and self.resistencia < 100:
            self.resistencia += p.PUNTOS_ENTRENAMIENTO * aumentoEntrenamiento
            if self.resistencia >=100:    self.resistencia = 100
            print(f'Resistencia de {self.nombre} aumentada a: {self.resistencia}')
        elif atributoAEntrenar == '2' and self.flexibilidad < 100:
            self.flexibilidad += p.PUNTOS_ENTRENAMIENTO * aumentoEntrenamiento
            if self.flexibilidad >=100:    self.flexibilidad = 100
            print(f'Flexibilidad de {self.nombre} aumentada a: {self.flexibilidad}')
        else:
            print('\nEste atributo ya está al máximo')
        
    def lesionarse(self, riesgo):
        #Se calcula la probabilidad para ver si se lesiona o no
        valorAleatorio = round(random.uniform(0,1),2)
        if valorAleatorio<= riesgo:
            print(self.nombre, 'se lesionó')
            self.lesionado = True      






class atletismo(deporte):
    def __init__(self):
        super().__init__(False, 0.2)
        self.riesgo = 0.2


    def calcularGanador(self, d1, d2, delegacion1, delegacion2):
        print('\nATLETISMO:')
        validez = self.validezCompetencia(d1,d2,delegacion1,delegacion2)
        #Para todos los deportes: Si ambos son válidos, se calculan los puntajes de la forma 
        #dicha en el enunciado, pero si hay alguno o ambos no son válidos para competir,
        #se asignan los puntajes de modo que se refleje eso.
        if validez == 'valido':
            puntaje1 = max(p.PUNTAJE_MINIMO, 0.55*d1.velocidad+0.2*d1.resistencia+0.25*d1.moral)
            puntaje2 = max(p.PUNTAJE_MINIMO, 0.55*d2.velocidad+0.2*d2.resistencia+0.25*d2.moral)
        elif validez == d1:
            puntaje1 = 1
            puntaje2 = 0
        elif validez == d2:
            puntaje1 = 0
            puntaje2 = 1
        elif validez == 'empate':
            puntaje1 = 0
            puntaje2 = 0

        if puntaje1 > puntaje2:
            print(F'\nGANADOR ATLETISMO: {d1.nombre}\n')
            return d1
        elif puntaje2 > puntaje1:
            print(F'\nGANADOR ATLETISMO: {d2.nombre}\n')
            return d2
        elif puntaje1 == puntaje2:
            print(F'\nGANADOR ATLETISMO: EMPATE\n')
            return 'empate'
        

class ciclismo(deporte):
    def __init__(self):
        super().__init__(True, 0.35)
        self.riesgo = 0.35


    def calcularGanador(self, d1, d2, delegacion1, delegacion2):
        print('\nCICLISMO:')

        d1.lesionarse(self.riesgo)
        d2.lesionarse(self.riesgo)

        validez = self.validezCompetencia(d1,d2,delegacion1,delegacion2)
        if validez == 'valido':
            puntaje1= max(p.PUNTAJE_MINIMO, 0.47*d1.velocidad+0.36*d1.resistencia+0.17*d1.flexibilidad)
            puntaje2= max(p.PUNTAJE_MINIMO, 0.47*d2.velocidad+0.36*d2.resistencia+0.17*d2.flexibilidad)
        elif validez == d1:
            puntaje1 = 1
            puntaje2 = 0
        elif validez == d2:
            puntaje1 = 0
            puntaje2 = 1
        elif validez == 'empate':
            puntaje1 = 0
            puntaje2 = 0
    
        if puntaje1 > puntaje2:
            print(F'\nGANADOR CICLISMO: {d1.nombre}\n')
            return d1
        elif puntaje2 > puntaje1:
            print(F'\nGANADOR CICLISMO: {d2.nombre}\n')
            return d2
        elif puntaje1 == puntaje2:
            print(F'\nGANADOR CICLISMO: EMPATE\n')
            return 'empate'
        
        

class gimnasia(deporte):
    def __init__(self):
        super().__init__(True, 0.3)
        self.riesgo = 0.3


    def calcularGanador(self, d1, d2, delegacion1, delegacion2):
        
        print('\nGIMNASIA:')
        d1.lesionarse(self.riesgo)
        d2.lesionarse(self.riesgo)
        validez = self.validezCompetencia(d1,d2,delegacion1,delegacion2)
        if validez == 'valido':
            puntaje1 = max(p.PUNTAJE_MINIMO, 0.5*d1.flexibilidad+0.3*d1.resistencia+0.2*d1.moral)
            puntaje2 = max(p.PUNTAJE_MINIMO, 0.45*d2.flexibilidad+0.3*d2.resistencia+0.25*d2.moral)
        elif validez == d1:
            puntaje1 = 1
            puntaje2 = 0
        elif validez == d2:
            puntaje1 = 0
            puntaje2 = 1
        elif validez == 'empate':
            puntaje1 = 0
            puntaje2 = 0

            

        if puntaje1 > puntaje2:
            print(F'\nGANADOR GIMNASIA: {d1.nombre}\n')
            return d1
        elif puntaje2 > puntaje1:
            print(F'\nGANADOR GIMNASIA: {d2.nombre}\n')
            return d2
        elif puntaje1 == puntaje2:
            print(F'\nGANADOR GIMNASIA: EMPATE\n')
            return 'empate'


class natacion(deporte):
    def __init__(self):
        super().__init__(False, 0.25)
        self.riesgo = 0.25


    def calcularGanador(self, d1, d2, delegacion1, delegacion2):
        print('\nNATACION:')
        d1.lesionarse(self.riesgo)
        d2.lesionarse(self.riesgo)
        validez = self.validezCompetencia(d1,d2,delegacion1,delegacion2)
        if validez == 'valido':

            puntaje1 = max(p.PUNTAJE_MINIMO, 0.45*d1.velocidad+0.3*d1.resistencia+0.25*d1.flexibilidad)
            puntaje2 = max(p.PUNTAJE_MINIMO, 0.45*d2.velocidad+0.3*d2.resistencia+0.25*d2.flexibilidad)
        elif validez == d1:
            puntaje1 = 1
            puntaje2 = 0
        elif validez == d2:
            puntaje1 = 0
            puntaje2 = 1
        elif validez == 'empate':
            puntaje1 = 0
            puntaje2 = 0
            
        if puntaje1 > puntaje2:
            print(F'\nGANADOR NATACION: {d1.nombre}\n')
            return d1
        elif puntaje2 > puntaje1:
            print(F'\nGANADOR NATACION: {d2.nombre}\n')
            return d2
        elif puntaje1 == puntaje2:
            print(F'\nGANADOR NATACION: EMPATE\n')
            return 'empate'

