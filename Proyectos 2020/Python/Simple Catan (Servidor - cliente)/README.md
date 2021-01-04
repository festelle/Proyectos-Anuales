# Tarea 03: DCCColonos :school_satchel:


## Consideraciones generales :octocat:

Se implementó una versión simple del juego. Todo lo relacionado con el servidor y cliente (logs, envío de mensajes, construcción de mapa, etc) está implementado, sin embargo, no se implementaron las siguientes partes del juego:

* Construcción de carreteras.
* Cartas de desarrollo
* Intercambio de cartas con otros jugadores
* Redirección a sala de espera cuando el juego termina

A parte de estos puntos, se implementó todo lo pedido. Además, se agregó una ventana inicial, donde se puede apretar el botón "jugar" para empezar la conexión con el servidor. Esto se hizo porque considero que es una buena forma de evitar conexiones accidentales por abrir sin querer el programa (pensando en cuando el juego sea masivo)

Tal como se pidio, hay dos carpetas creadas, client y server, que no tienen ningun tipo de contacto entre si.

Por ultimo, es muy importante tener en cuenta que **tiene que haber una copia de los archivos grafo.json y generador_grilla.py dentro de cada carpeta (client y server) para que puedan correr sin problemas. Además, la carpeta de sprites debe estar dentro de la carpeta client**

### Cosas implementadas y no implementadas :white_check_mark: :x:


* Networking: Hecha completa
* Arquitectura cliente servidor: Hecha completa, con la excepción que si un cliente se desonecta mientras es su turno el juego se queda estancado (pero si se desconecta mientras no es su turno sigue funcionando perfectamente)
* Manejo de bytes: Hecha completa
* Interfaz gráfica:
    * Sala de juego: No se implementó la ventana para cambiar recursos
    * Fin de la partida: se da la opción de salir pero no de dirigirse a la sala de espera
    * No se implementó el mecanismo de la carta monopolio
* Grafo: 
    * Funcionalidades: No se implementó la construcción de carreteras, por lo que no se verifica si se cumplen las restricciones de construcción de carretera ni se calcula la más larga
* Reglas DCColonos:
    * Turno: No se implementa ni la carta de punto de victoria ni la de Monopolio, tampoco se implementa el intercambio con jugadores ni los puntos extras por el jugador con la carretera más larga
* General: 
    * Generador de Mazos: No se implementó


## Ejecución :computer:
Los módulos principales de la tarea a ejecutar son:  
1. Para el servidor: 'main.py', que está en la carpeta titulada 'server'
2. Para los clientes: 'main.py', que está en la carpeta titulada 'client'


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:


1. ```random```:  ``` choice(), sample(), randint()```, para poder escoger al azar entre una lista y tener los resultados de los dados
2. ```faker```: ```Faker()```, para la creación de nombres
3. ```pickle```: Envìo de info entre server y client
4. ```json```: Envìo de info entre server y client
5. ```time```: ```sleep```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes (sin contar los archivos main.py del cliente y server):

Para el cliente:
1. ```frontEnd.py``` y ```frontEnd2.py```: Contiene la interfaz grafica del cliente.

2.  ```cliente.py```: Contiene tanto la conexiòn con el servidor como el backEnd de la interfaz grafica.
3. ```parametros.json```: Contiene los parametros.


Para el servidor:
1.  ```servidor.py```: Contiene la clase Server() que se encarga de controlar y liderar las conexiones hechas con los clientes.
2. ```parametros.json```: Contiene los parametros.

Para ambos (hay una copia de los siguientes archivos en ambas carpetas):
1. ```claseJugador.py```: Contiene a la clase jugador(), que instancia a los diferentes jugadores.
2. ```classMapa.py```: Contiene las clases Nodos(), hexagonos() y class_mapa(), que, en el frontEnd se encargan de graficar el mapa completo y en el servidor se encarga de controlar la informaciòn del mapa

Además, se creó el archivo ```.gitignore```, que ggnora los archivos pedidos en el enunciado.

**Recordar que tiene que haber una copia de los archivos grafo.json y generador_grilla.py dentro de cada carpeta (client y server) para que puedan correr sin problemas. Además, la carpeta de sprites debe estar dentro de la carpeta client**

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Se puede jugar con solo 1 jugador si así se desea (si se pone el parametro de "CANTIDAD_JUGADORES_PARTIDA" = 1). Esto es porque en el enunciado se deja claro que se debe jugar hasta alcanzar una cierta cantidad de puntos, y nunca se dice que tiene que haber un mínimo de jugadores. 



PD: **Por favor, no olvidar que hay que agregar una copia de los archivos grafo.json y generador_grilla.py dentro de cada carpeta (client y server) para que puedan correr sin problemas. También recordar de poner la carpeta sprites dentro de la carpeta client.**

Archivos que deberían haber en cada carpeta:

Carpeta client:
* sprites (carpeta) (DEBE SER AGREGADA)
* generador_grilla.py (DEBE SER AGREGADO)
* grafo.json (DEBE SER AGREGADO)
* claseJugador.py
* classMapa.py
* cliente.py
* frontEnd.py
* frontEnd2.py
* main.py
* parametros.json

Carpeta server:
* generador_grilla.py (DEBE SER AGREGADO)
* grafo.json (DEBE SER AGREGADO)
* claseJugador.py
* classMapa.py
* main.py
* parametros.json
* servidor.py


-------





## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. [ejemplos.ipynb de semana 14](https://github.com/IIC2233/contenidos/blob/master/semana-14/3-ejemplos.ipynb): El código de server.py y client.py se basó en el último ejemplo ('ejemplo completo: servidor con manejo de múltiples clientes en forma concurrente'). Sin embargo, se modificó casi completamente, por lo que ya no tienen mucho en común. Por esta misma razón, no se puede decir exactamente qué lineas son parte del código del ejemplo



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
