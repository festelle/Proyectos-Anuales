
from Objetos import deportista
from parametros import pathDelegacionCsv, pathDeportistasCsv
#En este archivo se guardarán las listas hechas a partir de los archivos deportistas y delegaciones
#Los paths usados para abrir el archivo están en parámetros

#Al final se crean 3 diccionarios: DCCrotonaInicial e IEEEsparta, que contiene los datos iniciales
# de cada delegación, y dictDeportistas, sus llaves son los nombres de los deportistas y el
#valor asociado a cada llave es el objeto deportista

with open(pathDelegacionCsv, 'rt') as archivo:
    lineas = archivo.readlines()
delegacionesIniciales = []
for linea in lineas:
    fila = linea.strip().split(',')
    delegacionesIniciales.append(fila)

#Al poder estar en diferente orden, se hace un diccionario
delegacionInicial1 = {}
delegacionInicial2 = {}
for i in range(len(delegacionesIniciales[0])):
    delegacionInicial1[delegacionesIniciales[0][i]] = delegacionesIniciales[1][i]
    delegacionInicial2[delegacionesIniciales[0][i]] = delegacionesIniciales[2][i]

if delegacionInicial1['Delegacion'] == 'IEEEsparta':
    IEEEspartaInicial = delegacionInicial1
    DCCrotonaInicial = delegacionInicial2
else:
    IEEEspartaInicial = delegacionInicial2
    DCCrotonaInicial = delegacionInicial1

IEEEspartaInicial['Equipo'] =  IEEEspartaInicial['Equipo'].split(';')
DCCrotonaInicial['Equipo'] = DCCrotonaInicial['Equipo'].split(';')


with open(pathDeportistasCsv, 'rt') as archivo:
    lineas = archivo.readlines()
tablero = []
for linea in lineas:
    fila = linea.strip().split(',')
    tablero.append(fila)

tableroNuevo = []
listaAuxiliar = []
for fila in tablero:
    for col in fila:
        listaAuxiliar.append(col.strip())
    tableroNuevo.append(listaAuxiliar)
    listaAuxiliar = []
tablero = tableroNuevo
diccionarioAuxiliar = {}
dictDeportistas = {}
for j in range(len(tablero)):
    for i in range(len(tablero[0])):
        diccionarioAuxiliar[tablero[0][i]] = tablero[j][i]
    nombre = diccionarioAuxiliar['nombre']
    dictDeportistas[nombre] = diccionarioAuxiliar
    diccionarioAuxiliar = {}

del dictDeportistas['nombre']



#Se transforman los diccionarios importados en objetos deportista
for i in dictDeportistas:
    dictDeportistas[i] = deportista(dictDeportistas[i]['nombre'], dictDeportistas[i]['velocidad'],
     dictDeportistas[i]['resistencia'],dictDeportistas[i]['flexibilidad'],
     dictDeportistas[i]['moral'],dictDeportistas[i]['lesionado'],dictDeportistas[i]['precio'])

#Se agregan los objetos iniciales de cada delegación y eliminan del dictDeportistas
listEquipos = []
for i in IEEEspartaInicial['Equipo']:
    listEquipos.append(dictDeportistas[i])
    del dictDeportistas[i]
IEEEspartaInicial['Equipo'] = listEquipos
listEquipos = []
for i in DCCrotonaInicial['Equipo']:
    listEquipos.append(dictDeportistas[i])
    del dictDeportistas[i]
DCCrotonaInicial['Equipo'] = listEquipos

#Ya se tienen los datos de forma que se puedan trabajar



#Función para poder volver a tener los diccionarios desde 0 en caso que se quieraa hacer
#otra simulación

def dictDeportistaNuevo():

    #Se crean 3 diccionarios: DCCrotonaInicial e IEEEsparta, que contiene los datos iniciales
    # de cada delegación, y dictDeportistas, sus llaves son los nombres de los deportistas y el
    #valor asociado a cada llave es el objeto deportista

    with open(pathDelegacionCsv, 'rt') as archivo:
        lineas = archivo.readlines()
    delegacionesIniciales = []
    for linea in lineas:
        fila = linea.strip().split(',')
        delegacionesIniciales.append(fila)

    #Al poder estar en diferente orden, se hace un diccionario
    delegacionInicial1 = {}
    delegacionInicial2 = {}
    for i in range(len(delegacionesIniciales[0])):
        delegacionInicial1[delegacionesIniciales[0][i]] = delegacionesIniciales[1][i]
        delegacionInicial2[delegacionesIniciales[0][i]] = delegacionesIniciales[2][i]

    if delegacionInicial1['Delegacion'] == 'IEEEsparta':
        IEEEspartaInicial = delegacionInicial1
        DCCrotonaInicial = delegacionInicial2
    else:
        IEEEspartaInicial = delegacionInicial2
        DCCrotonaInicial = delegacionInicial1

    IEEEspartaInicial['Equipo'] =  IEEEspartaInicial['Equipo'].split(';')
    DCCrotonaInicial['Equipo'] = DCCrotonaInicial['Equipo'].split(';')


    with open(pathDeportistasCsv, 'rt') as archivo:
        lineas = archivo.readlines()
    tablero = []
    for linea in lineas:
        fila = linea.strip().split(',')
        tablero.append(fila)

    tableroNuevo = []
    listaAuxiliar = []
    for fila in tablero:
        for col in fila:
            listaAuxiliar.append(col.strip())
        tableroNuevo.append(listaAuxiliar)
        listaAuxiliar = []
    tablero = tableroNuevo
    diccionarioAuxiliar = {}
    dictDeportistas = {}
    for j in range(len(tablero)):
        for i in range(len(tablero[0])):
            diccionarioAuxiliar[tablero[0][i]] = tablero[j][i]
        nombre = diccionarioAuxiliar['nombre']
        dictDeportistas[nombre] = diccionarioAuxiliar
        diccionarioAuxiliar = {}

    del dictDeportistas['nombre']



    #Se transforman los diccionarios importados en objetos deportista
    for i in dictDeportistas:
        dictDeportistas[i] = deportista(dictDeportistas[i]['nombre'], dictDeportistas[i]['velocidad'],
        dictDeportistas[i]['resistencia'],dictDeportistas[i]['flexibilidad'],
        dictDeportistas[i]['moral'],dictDeportistas[i]['lesionado'],dictDeportistas[i]['precio'])

    #Se agregan los objetos iniciales de cada delegación y eliminan del dictDeportistas
    listEquipos = []
    for i in IEEEspartaInicial['Equipo']:
        listEquipos.append(dictDeportistas[i])
        del dictDeportistas[i]
    IEEEspartaInicial['Equipo'] = listEquipos
    listEquipos = []
    for i in DCCrotonaInicial['Equipo']:
        listEquipos.append(dictDeportistas[i])
        del dictDeportistas[i]
    DCCrotonaInicial['Equipo'] = listEquipos

    return [DCCrotonaInicial,IEEEspartaInicial,dictDeportistas]

    #Ya se tienen los datos de forma que se puedan trabajar

