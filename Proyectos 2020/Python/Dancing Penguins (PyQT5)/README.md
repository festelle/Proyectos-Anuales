# Tarea 2: DCCumbia :school_satchel:



**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

Se implementó todas las funcionalidades pedidas en el enunciado, con excepción de que los pinguirines bailaran (la tienda funciona perfectamente, se pueden arrastrar pinguirines a la pista de baile y dejarlos ahí pero estos no bailan, quizás son muy tímidos). A parte de esto, el programa funciona sin fallas.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Ventana Inicio: Hecha completa
* Ventana de ranking: Hecha completa
* Ventana de Juego:
    * Generales: Hecha completa 
    * Fase pre-ronda: Hecha completa
    * Fase de ronda: Hecha completa
    * Fase de post-ronda: Hecha completa
* Mecánicas de juego: 
    * Pingüirin: pinguirines no bailan
    * Flechas: No se identifica si un paso combinado es correcto o no. Se toman como flechas separadas.
*Funcionalidades Extra: Hecha completamente
* General: Hecha completa.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Todos los otros archivos (```frontEnd.py```, ```frontEnd_2.py```,```backEnd.py```, ```clases_drap_drog.py```, ```parametros.py```) deben estar en la misma carpeta que ```main.py```. 
Antes de correr el programa, se deben actualizar los parámetros en caso de que los sprites se encuentren en un path diferente.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: Usada para unir el path hacia los diferentes sprites y canciones usados
2. ```PyQt5```: Usada para crear la interfaz gráfica
3. ```time```: Se usó el módulo sleep(), para poder actualizar las flechas.
4. ```random```: se uaron los módulo uniform y randint.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```frontEnd.py```: Contiene a ```ventana_juego()```, la clase ás larga, centrada en el aspecto de la ventana de juego
2. ```frontEnd_2.py```: Contiene los aspectos de front end de las ventana de inicio, ventana de ranking y ventana de resumen del juego. 
3. ```backEnd.py```: Contiene la lógica para cada ventana.
4. ```clases_drap_drog.py```: Contiene clases necesarias para poder arrastrar pinguirines a la pista de baile. Además, contiene funciones que ayudan a facilitar la comprensión de todos los archivos.
5. ```parametros.py```: Contiene todos los parámetros utilizados. Esto incluye path a archivos.

## Supuestos y consideraciones adicionales :thinking:
Al revisar, hay que tener en cuenta que:

 * Para que no se pueda comprar nada en la tienda mientras se juega, cada vez que parte una partida, se le quita todo el dinero al jugador, pero al terminar la partida se le devuelve el dinero inicial y se le suma lo que ganó. 

 * No se pudo implementar que los pinguirines bailen. Por esto, se prefirió entregar el juego donde se mueve la imagen del pinguirin, y aesta se le trata como un label, sin entregar el thread incompleto que se trató de crear, con el fin de simplificar la corrección.


-------


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. [Ej semana 10](https://github.com/IIC2233/contenidos/blob/master/semana-10/1-pyqt-qthreads.ipynb): La clase thread_flechas presente en el archivo ```frontEnd_2.py```fue basada en este código. lo que hace es generar imágenes al azar en una ventana

2. [PyQt5 Tutorial](https://learndataanalysis.org/create-label-to-label-drag-and-drop-effect-pyqt5-tutorial/): Este código se usó como base para las clases DragLabel y DropLabel, presentes en el archivo ```clases_drap_drog.py```. Tienen como fin crear label que puedan ser movidas de un lugar a otro.



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
