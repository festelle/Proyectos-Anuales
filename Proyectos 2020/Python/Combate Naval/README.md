# Tarea 00: DCCombate Naval :school_satchel:


## Consideraciones generales :octocat:

El código está completo y no presenta fallas o partes faltantes.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Inicio del programa: Hecha completa
* Flujo del juego: Hecha completa
* Término del juego: Hecha completa
* Archivos: Hecha completa
* General: Hecha completa

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```mainLoop.py```. Se debe tener en cuenta que todos los archivos (incluidos los entregados para la tarea) deben estar en la misma carpeta para que pueda correr sin problemas


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```función "randint()"```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```ObjectsAndDef```: Contiene a la clase ```game``` y a la función ```rankingPuntajes``` 
2. ```parametros```: Entregado junto a la tarea, contiene los dos parámetros a usar en esta tarea (```NUM_BARCOS``` y ```RADIO_EXP```)
3. ```tablero```: Entregado junto a la tarea, contiene la función ```print_tablero```, que fue usada.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Si el jugador está en medio de una partida y sale del programa, solo se le entrega una partida que dice "GAME OVER, Saliste del juego", Pero no se guarda su puntaje. Esto es porque al salir del juego se considera que al jugador no le importa su puntaje, solo quiere terminar de jugar. Si le importara guardar el puntaje, primero se rendiría y después saldría del juego.


-------


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. [Código 1](https://www.afternerd.com/blog/python-sort-list/) : esta linea ordena los puntajes escrito en el archivo "puntajes.txt" de mayor a menor. Está implementado en el archivo <ObjectsandDef.py> en la línea <26>



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
