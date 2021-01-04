# Tarea 1: DCCumbre Olímpica :school_satchel:




Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

El programa funciona tal como debería, exceptuando que cuando se quiere crear otra simulación sin salir del programa primero, los deportistas disponibles para fichar no son actualizados, por lo que aparecen menos opciones

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Programación Orientada a Objetos: Hecha completa
* Partidas: Hecha completa, pero presenta un fallo:

    * Crear partida: cuando se crea una segunda simulación, no se reinicia el diccionario de deportistas, por lo que si se fichó alguno anteriormente ya no está disponible (he tratado de encontrar la falla pero no la veo :cry:)
* Acciones: Hecha completa 
* Consola: Hecha completa
* Manejo de arhivos: Hecha completa

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```mainLoop.py```. Además se debe tener en cuenta:
* Todos los archivos .py deben estar en la misma carpeta
* En el archivo ```parámetros.py``` se debe indicar el path para los archivos ```delegaciones.csv``` y ```deportistas.csv```, además de indicar dónde se quiere crear el archivo ```resultados.txt``` (si es que todavía no existe)


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```funciones randint() y uniform()```
2. ```abc```: ``` ABC y abstract method``` 
3. ```os```
4. ```beautifultable```: ```función Beautifultable()```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```Diccionarios```: Se transforman los archivos .csv en diccionarios para poder trabajar con ellos. Se usan los diccionarios ```DCCrotonaInicial e IEEEsparta``` ,```dictDeportistas```
2. ```abstractClass```: Contiene las clases abstractas ```Delegacion```, ```deporte```, además de función ```escribirBitacora()```
3. ```Objetos```: Contiene todos los objetos necesarios (esto es, todos los deportes, deportistas y delegaciones), con excepción de la clase ```campeonato```
4. ```classCampeonato```: Contiene la clase campeonato, que combina las clases creadas en Objetos para poder realizar la simulación.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Se pueden elegir deportistas que estén lesionados para que compitan en una carrera. Este supuesto se hizo pensando en que si un día una delegación tuviera a todos sus deportistas lesionados y no tuviera suficiente DCCoins para sanar a uno, entonces el campeonato se quedaría estancado en ese día. Además, en la historia deportiva ya han habido casos de deportistas lesionados participando (se puede ver casos así en este [video](https://www.youtube.com/watch?v=sLjBQ38ZQSg)) (aunque en este programa, el que participen lesionados significa que van a perder).
2. Al haber diferentes instrucciones sobre qué días son de entrenamiento y qué días competencia, en este programa los días pares (partiendo desde el 0) son entrenamiento y los días impares de competencia
3. Los nombres del usuario y rival pueden ser iguales, sin embargo, no pueden contener mayúsculas (como lo dice el enunciado). Tiene sentido que dos personas distintas compartan el mismo nombre.
4. TODOS los números decimales están redondeados al segundo decimal, con excepción de los que el enunciado piden que estén redondeados a 1 decimal. Esto es porque así las probabilidades van a tener más sentido al ser 100 opciones distintas en vez de que fueran solo 10 (en el caso de redondearlos a 1 decimal).

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. [Archivo 'Path' de la semana 00](https://github.com/IIC2233/contenidos/blob/master/semana-00/3-paths.ipynb): Este hace \<lo que hace> y está implementado en el archivo <Diccionarios.py> en las líneas 11-16 , 16-41. Lee y separa los archivos .csv en lista de listas para poder trabajar con ellos
2. [Archivo 'Path' de la semana 00](https://github.com/IIC2233/contenidos/blob/master/semana-00/3-paths.ipynb)


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/contenidos/blob/master/semana-00/3-paths.ipynb).
