
# Explicación diagrama de clases :school_satchel:

0. Este programa en total contiene 11 clases, de las cuales:
    * 2 son abstractas
    * 6 son subclases
    * 3 son clases normales

Clases abstractas: 

 1. Delegación: Crear el concepto general de delegación. Tiene el abstract method "Utilizar Habilidad" que, al ser una habilidad diferente para cada delegación, es necesario que se llene por separado. Para todo atributo que tenga que estar dentro de un rango, se usa un getter y setter para mantenerlos acotados.
    De esta clase abstracta se crean dos subclases:
    * DCCrotona e IEEEsparta: Son las delegaciones que participan. Es necesario sobreescribir ciertos atributos que son diferentes dependiendo de la delegación. Además, para cada delegación se sobreescribe el método abstracto de "utilizarHabilidadEspecial", además de que heredan todos los getter y setter para mantener acotados los atributos.
    Además, presenta la siguiente relación: 
    * Relación de agregación con la clase deportista: Esto es porque cada delegación necesita un mínimo de 5 deportistas para empezar la competencia.

 2. Deporte: Concepto general de deporte, tiene el método abstracto calcularGanador, que varía de acuerdo al deporte.
    De esta clase abstracta se crean 4 subclases:
    * atletismo, ciclismo, gimnasia y natacion:  Para cada uno de estos deportes se sobreescribe el atributo de riesgo y el método abstracto de "calcularGanador"

Clases que no son abstractas ni heredan de otra clase:

3.  deportista: Recibe atributos, de los cuales algunos están acotados, por lo que se usan getter y setters. Tiene 2 métodos.

4. Campeonato: Junta información de muchas clases para poder simular el campeonato.
    Presenta las siguientes relaciones:
    * Relación de composición con cada uno de los 4 deportes: Para que el campeonato pueda existir, se necesita que los 4 deportes esté, presentes, por otro lado, no tiene sentido crear un deporte si es que no va a estra presente en el campeonato.
    * Relación de agregación con clase "deportista": para realizar el campeonato, se necesitan deportistas, sin embargo, la clase de deportista es usar en más clases, por lo que la vida de la clase campeonato no afecta su vida.
    * Relación de agregación con DCCrotona e IEEEsparta: Se necesitan de ambas delegaciones para poder realizar la competencia, pero estas delegaciones son usadas en otras clases además de esta, por lo que su tiempo de vida es independiente al tiempo de vida de la clase campeonato.

5. menu: En esta clase se encuentran los 3 menus principales como funciones (menu de inicio, menu principal y menu de       entrenador). Debido a la gran cantidad de atributos que necesita, presenta las siguientes relaciones:
    * Relación de agregación con DCCrotona e IEEEsparta: El mennu necesita estas clases para poder transformar lo elegido por el usuario en clases que puedan relacionarse con la clase campeonato. Es agregación porque estas dos clases son necesarias en otras clases más, por lo que sus tiempos de vida es independiente al de menu.
    * Relación de composición con campeonato: El menu se comunica continuamente con la clase campeonato para poder realizar todas las acciones. Es composición porque la clase campeonato es usada exclusivamente en esta clase, por lo que si menu dejara de existir, campeonato tampoco sería de utilidad.