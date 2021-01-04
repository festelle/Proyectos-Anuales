import os
###parámetros usados a lo largo de la tarea

#Se crea un parámetro de duración de música que cambia de acuerdo a la selección,
#esto es porque no se encontró forma de pasarle argumentos a un QTIMER
DURACION_MUSICA = 30

VELOCIDAD_FLECHA = 88
#Este backup es usado en el caso de que se cambie el valor de velocidad flecha
VELOCIDAD_FLECHA_BACKUP = VELOCIDAD_FLECHA


#Se pone la probabilidad de aparición de cada flecha
PROB_NORMAL = 0.8
PROB_FLECHA_X2 = 0.1
PROB_FLECHA_DORADA = 0.05
PROB_FLECHA_HIELO = 0.05
#La cantidad de puntos que da una flecha normal
PUNTOS_FLECHA = 1

#Tamaño de las flechas a caer y tamaño de la zona de captura.
ALTO_FLECHA = 33
ALTO_CAPTURA = 42



#lista con path a las diferentes canciones.
CANCIONES = {'cancion_1': os.path.join('songs','cancion_1.wav'),
 'cancion_2': os.path.join('songs','cancion_2.wav')}

#path donde se quiere crear (o está) el archivo ranking, en este caso se guardará en la misma
# carpeta donde está el archivo
PATH_RANKING = os.path.join('ranking.txt')

#Alto y precio de los pinguinos que se pueden comprar
ALTO_PINGU = 75
PRECIO_PINGU = 500

#Path a las diferentes imágenes de los pinguinos

RUTAS_PINGUINOS = [os.path.join('sprites', 'pinguirin_amarillo'),\
                    os.path.join('sprites', 'pinguirin_celeste') ,\
                    os.path.join('sprites', 'pinguirin_morado') ,\
                    os.path.join('sprites', 'pinguirin_rojo') ,\
                    os.path.join('sprites', 'pinguirin_verde')]

PINGUINOS_NEUTROS = [os.path.join('sprites', 'pinguirin_amarillo', 'amarillo_neutro.png'),\
                    os.path.join('sprites', 'pinguirin_celeste', 'celeste_neutro.png') ,\
                    os.path.join('sprites', 'pinguirin_morado', 'morado_neutro.png') ,\
                    os.path.join('sprites', 'pinguirin_rojo', 'rojo_neutro.png') ,\
                    os.path.join('sprites', 'pinguirin_verde', 'verde_neutro.png')]


#Path a las imágenes de las flechas básicas a usar

FLECHAS_BASICAS = [os.path.join('sprites','flechas','left_5'),\
                 os.path.join('sprites','flechas','up_5'),\
                 os.path.join('sprites','flechas','down_5'),\
                 os.path.join('sprites','flechas','right_5')]


#Path hacia la carpeta donde se encuentran todas las imágenes de las flechas
PATH_FLECHAS = os.path.join('sprites','flechas')



#Cantidad de dinero a ganar al usar el código de trampa
DINERO_TRAMPA = 500


