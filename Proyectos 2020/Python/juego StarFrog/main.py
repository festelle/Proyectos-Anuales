import pygame
import random
import numpy
import math
import time

# Siempre se pone esto al inicio
pygame.init()

# Ventana
screenwidth = 1200
screenheight = 645
# La pantalla de mi computador es 1360*765
win = pygame.display.set_mode((screenwidth, screenheight))
# win = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
# icon = pygame.image.load('Pixel art gali 1.png')
# pygame.display.set_icon(icon)
# Nombre de la ventana
pygame.display.set_caption("star Frog")
pygame.display.set_icon(pygame.image.load('imagenes\sprites\mirando1.png').convert_alpha())

# Cargar las imágenes
fondoNoche = pygame.image.load('imagenes/obj/fondo noche.png').convert()

imgLuna = pygame.image.load('imagenes/obj/luna.png').convert()
imgLuna.set_colorkey((51, 25, 149))

imgBanca = pygame.image.load('imagenes/obj/banca.png').convert()
imgBanca.set_colorkey((51, 25, 149))

''' 
imgNubes = [pygame.image.load('imagenes/Nubes/Nube 1.png').convert(),
            pygame.image.load('imagenes/Nubes/Nube 2.png').convert(),
            pygame.image.load('imagenes/Nubes/Nube 3.png').convert(),
            pygame.image.load('imagenes/Nubes/Nube 4.png').convert(),
            pygame.image.load('imagenes/Nubes/Nube 5.png').convert(),
            pygame.image.load('imagenes/Nubes/Nube 6.png').convert()] 

for nube in imgNubes:
    nube.set_colorkey((254, 254, 254)) '''

imgHistoria1 = [pygame.image.load('imagenes/historias/historia1/historia1-1.png').convert(),
                pygame.image.load('imagenes/historias/historia1/historia1-2.png').convert()]

imgHistoria2 = [pygame.image.load('imagenes/historias/historia2/historia2-1.png').convert(),
                pygame.image.load('imagenes/historias/historia2/historia2-2.png').convert(),
                pygame.image.load('imagenes/historias/historia2/historia2-3.png').convert()]

imgDialogo = pygame.image.load('imagenes\historias\historia1\dialogo.png').convert()
imgDialogo = pygame.transform.scale(imgDialogo, (510, 150))
imgDialogo.set_colorkey((255, 0, 0))

imgEstrellaPequena = pygame.image.load('imagenes/obj/estrella pequeña.png').convert()
imgEstrellaMediana = pygame.image.load('imagenes/obj/estrella mediana.png').convert()

imgAvion = pygame.image.load('imagenes/obj/avion.png').convert()
imgAvion.set_colorkey((51, 25, 149))
imgAvion = pygame.transform.scale(imgAvion, (64, 64))

#Imagenes mirando arriba
imgMirando1 = pygame.image.load('imagenes\sprites\mirando1.png').convert_alpha()
#imgMirando1.set_colorkey((51, 25, 149))
#imgMirando = pygame.transform.scale(imgMirando, (64, 64))
imgMirando2 = pygame.image.load('imagenes\sprites\mirando2.png').convert_alpha()

imgPlataforma = pygame.image.load('imagenes\obj\plataforma.png').convert_alpha()
imgPlataforma2 = pygame.image.load('imagenes\obj\plataforma2.png').convert_alpha()
imgPlataforma3 = pygame.image.load('imagenes\obj\plataforma3.png').convert_alpha()

imgPlayAgain = pygame.image.load('imagenes\obj\mensaje perdido.png').convert_alpha()
imgPlayAgain = pygame.transform.scale(imgPlayAgain, (510, 270))

letraPlayAgain = pygame.image.load('imagenes\obj\play again.png').convert_alpha()

letraNo = pygame.image.load('imagenes\obj\letra_no.png').convert_alpha()

letraYes = pygame.image.load('imagenes\obj\yes.png').convert_alpha()

letraStart = pygame.image.load('imagenes\obj\start.png').convert()
letraStart.set_colorkey((23, 39, 183))


boundaries = 10


class spritesheet:
    def __init__(self, filename, cols, rows):
        self.sheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect.width / cols)
        h = self.cellHeight = int(self.rect.height / rows)
        hw, hh = self.cellCenter = (int(w / 2), int(h / 2))

        self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.totalCellCount)])
        self.handle = list([
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h), ])

    def draw(self, surface, cellIndex, x, y, handle=0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellIndex])


class personaje(object):
    def __init__(self, x, y, width, height):
        self.x_original = x
        self.x = x
        self.y = y
        self.y_original = y
        self.yinicial = y
        self.yinicialoriginal = y
        self.yreal = y
        self.height = height
        self.width = width
        # El self.jumpcount puede actuar como "gravedad", controla el tiempo que dura el salto
        self.jumpCount = 47
        self.moduloJump = -0.006
        self.jumpCountInicial = self.jumpCount
        self.vel = 5
        self.debesaltar = False
        self.debecaminar = True
        self.subiendo = False
        self.moverse = True
        self.final = False #Se activa cuando gana

        self.sprite_aterrizando = False


        #Para controlar la animación de salto
        filename, cols, rows = "imagenes\sprites\sprite_salto.png", 25, 1
        self.sheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect.width / cols)
        h = self.cellHeight = int(self.rect.height / rows)
        hw, hh = self.cellCenter = (int(w / 2), int(h / 2))

        self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.totalCellCount)])
        self.handle = list([
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h), ])
        
        self.index = 0
        self.contador = 0

        self.animacion_caminando = spritesheet('imagenes\sprites\Frog-Man.png',5,4)
        self.index_caminando = 0
        self.contador_caminando = 0

        self.debe_mirar = False
        self.frames_mirando = 0

        #Animacion mirando hacia arriba
        filename = 'imagenes\sprites\Frog-Man.png'
        self.sheet_mirando = pygame.image.load(filename).convert_alpha()
        self.dialogo_aparecido = 0
        self.frames_para_aparecer = 0
    
    def reiniciar(self):
        self.x = self.x_original
        self.y = self.y_original
        self.yinicial = self.y_original
        self.yinicialoriginal = self.y_original
        self.yreal = self.y_original
        # El self.jumpcount puede actuar como "gravedad", controla el tiempo que dura el salto
        self.jumpCount = 47
        self.moduloJump = -0.006
        self.jumpCountInicial = self.jumpCount
        self.vel = 5
        self.debesaltar = False
        self.debecaminar = True
        self.subiendo = False
        self.moverse = True
        self.final = False #Se activa cuando gana

        self.sprite_aterrizando = False


        #Para controlar la animación de salto
        filename, cols, rows = "imagenes\sprites\sprite_salto.png", 25, 1
        self.sheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect.width / cols)
        h = self.cellHeight = int(self.rect.height / rows)
        hw, hh = self.cellCenter = (int(w / 2), int(h / 2))

        self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.totalCellCount)])
        self.handle = list([
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h), ])
        
        self.index = 0
        self.contador = 0

        self.animacion_caminando = spritesheet('imagenes\sprites\Frog-Man.png',5,4)
        self.index_caminando = 0
        self.contador_caminando = 0

        self.debe_mirar = False
        self.frames_mirando = 0

        #Animacion mirando hacia arriba
        filename = 'imagenes\sprites\Frog-Man.png'
        self.sheet_mirando = pygame.image.load(filename).convert_alpha()
        self.dialogo_aparecido = 0
        self.frames_para_aparecer = 0
    
    
    def draw(self, win):
        # Hitbox
        #pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)

        #Sprite de salto

        if self.debesaltar:
            win.blit(self.sheet, (self.x + 18 + self.handle[4][0], self.y + self.handle[4][1] + 10), \
                self.cells[self.index % self.totalCellCount])
            
            self.contador += 1
            if self.contador >= 4:
                self.index += 1
                self.contador = 0
        
        elif self.debecaminar:
            self.animacion_caminando.draw(win, \
                self.index_caminando % self.animacion_caminando.totalCellCount, self.x, self.y+14, 4)
            self.contador_caminando += 1
            if self.contador_caminando >= 6:
                self.index_caminando += 1
                if self.index_caminando > 10:
                    self.index_caminando = 1
                self.contador_caminando = 0
        
        elif self.debe_mirar:
            if self.frames_mirando < 10:
                win.blit(imgMirando1, (self.x + 18 + self.handle[4][0], self.y + self.handle[4][1] + 14))
                self.frames_mirando += 1
            else:
                win.blit(imgMirando2, (self.x + 18 + self.handle[4][0], self.y + self.handle[4][1] + 14))

                imgDialogo.set_alpha(self.dialogo_aparecido)    
                win.blit(imgDialogo, (280,5*80))

                letraStart.set_alpha(self.dialogo_aparecido)
                win.blit(letraStart, (970,580))

                
                if self.dialogo_aparecido <= 255 and self.frames_para_aparecer > 100:
                    self.dialogo_aparecido += 1
                
                self.frames_para_aparecer += 1

    def moverseIzquierda(self):
        if self.x >= 10:
            self.x -= self.vel

    def moverseDerecha(self):
        if self.x <= screenwidth - self.width - 10:
            self.x += self.vel

    def saltar(self):
        if self.debesaltar:
            if self.jumpCount > 0:
                if not self.subiendo:
                    self.index, self.contador = 0, 0 #Reinicia el sprite
                self.subiendo = True
                if self.moverse:
                    self.y += (self.jumpCount ** 2) * self.moduloJump
                self.jumpCount -= 1

            elif self.jumpCount <= 0:
                self.subiendo = False
                self.y -= (self.jumpCount ** 2) * self.moduloJump
                self.jumpCount -= 1

            if self.y >= self.yinicialoriginal:
                self.jumpCount = self.jumpCountInicial


class plataforma(object):
    def __init__(self, x, y, width, vel):
        self.x = x
        self.y = y
        self.yOriginal = y
        self.vel = vel
        self.width = width
        self.height = 20

        self.tocando = False
        self.vecesTocado = 0
        self.contacto = False
        self.imgplataformaGenerada = pygame.transform.scale(imgPlataforma, (self.width, 20))
        self.imgplataforma2Generada = pygame.transform.scale(imgPlataforma2, (self.width, 20))
        self.imgplataforma3Generada = pygame.transform.scale(imgPlataforma3, (self.width, 20))


    def draw(self, win):
        # Hitbox
        self.y = self.yOriginal - camaraDeRana.cambio
        #pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)
        if self.vecesTocado == 0:
            win.blit(self.imgplataformaGenerada, (self.x,self.y))
        elif self.vecesTocado == 1:
            win.blit(self.imgplataforma2Generada, (self.x,self.y))
        elif self.vecesTocado >= 2:
            win.blit(self.imgplataforma3Generada, (self.x,self.y))
        
    def movimiento(self):
        self.y = self.yOriginal - camaraDeRana.cambio
        self.x += self.vel
        if self.x <= boundaries or self.x >= screenwidth - self.width - boundaries:
            self.vel = self.vel * -1

    def contactoArriba(self):
        self.y = self.yOriginal - camaraDeRana.cambio
        # Esta parte controla el contacto con la rana
        if rana.x + rana.width >= self.x and self.x + self.width >= rana.x:

            # Caso en el que está por encima
            if self.y - self.height - (rana.y + rana.height) <= 10 and self.y - self.height - (
                    rana.y + rana.height) >= -10 and not rana.subiendo:

                self.contacto = True
                rana.jumpCount = rana.jumpCountInicial
                self.tocando = True
                if rana.debesaltar:
                    self.vecesTocado += 1

                if self.vecesTocado >= 3:
                    self.x = 10000
                    self.vel = 0

            else:
                self.contacto = False
        else:
            self.contacto = False
            self.y = self.yOriginal - camaraDeRana.cambio


class montonDePlataformas(object):
    def __init__(self, PlataformasACrear):
        self.platforms = []
        self.altura = 400
        self.nroDePlataforma = 0
        self.PlataformasACrear = PlataformasACrear
        self.PlataformasACrear_original = PlataformasACrear
        self.distanciaEntrePlataformas = 200
        self.x = random.randint(150, 150)
        self.velF = 3
        self.velI = 1
        self.anchoInicial = 100
        self.anchoFinal = 200
        self.menosAnchoInicial = 0
        self.menosAnchoFinal = 0
        self.masVelInicial = 0
        self.masVelFinal = 0
        self.i = 1
        self.velocidadMaximaFinal = 5
        self.velocidadInicialFinal = 3
        self.anchoMaximoFinal = 100
        self.anchoMinimoFinal = 50

        for i in range(4):
            self.platforms.append((plataforma(random.randint(50, screenheight - 250), self.altura,
                                              random.randint(self.anchoInicial - self.menosAnchoInicial,
                                                             self.anchoFinal - self.menosAnchoFinal),
                                              random.choice([-1, 1]) * random.randint(
                                                  self.velI + self.masVelInicial,
                                                  self.velF + self.masVelFinal)),
                                   self.nroDePlataforma))
            self.altura -= self.distanciaEntrePlataformas
            self.nroDePlataforma += 1
    
    def reiniciar(self):
        self.platforms = []
        self.altura = 400
        self.nroDePlataforma = 0
        self.PlataformasACrear = self.PlataformasACrear_original
        self.distanciaEntrePlataformas = 200
        self.x = random.randint(150, 150)
        self.velF = 3
        self.velI = 1
        self.anchoInicial = 100
        self.anchoFinal = 200
        self.menosAnchoInicial = 0
        self.menosAnchoFinal = 0
        self.masVelInicial = 0
        self.masVelFinal = 0
        self.i = 1
        self.velocidadMaximaFinal = 5
        self.velocidadInicialFinal = 3
        self.anchoMaximoFinal = 100
        self.anchoMinimoFinal = 50

        for i in range(4):
            self.platforms.append((plataforma(random.randint(50, screenheight - 250), self.altura,
                                              random.randint(self.anchoInicial - self.menosAnchoInicial,
                                                             self.anchoFinal - self.menosAnchoFinal),
                                              random.choice([-1, 1]) * random.randint(
                                                  self.velI + self.masVelInicial,
                                                  self.velF + self.masVelFinal)),
                                   self.nroDePlataforma))
            self.altura -= self.distanciaEntrePlataformas
            self.nroDePlataforma += 1

    def draw(self, win):

        for platform in self.platforms:

            platform[0].draw(win)
            platform[0].movimiento()
            platform[0].contactoArriba()
            if platform[0].vecesTocado >= 3 or platform[0].y >= 700:
                self.platforms.remove(platform)
                if self.nroDePlataforma < self.PlataformasACrear:
                    self.platforms.append((plataforma(random.randint(50, screenheight - 250), self.altura,
                                                      random.randint(self.anchoInicial - self.menosAnchoInicial,
                                                                     self.anchoFinal - self.menosAnchoFinal),
                                                      random.choice([-1, 1]) * random.randint(
                                                          self.velI + self.masVelInicial,
                                                          self.velF + self.masVelFinal)),
                                           self.nroDePlataforma))
                    self.altura -= self.distanciaEntrePlataformas
                    self.nroDePlataforma += 1
                    if self.nroDePlataforma == 10 * self.i:


                        if self.masVelFinal + self.velF < self.velocidadMaximaFinal:
                            self.masVelFinal += 1
                        elif self.masVelInicial + self.velI < self.velocidadInicialFinal:
                            self.masVelInicial += 1

                        if self.anchoFinal - self.menosAnchoFinal - 25 >= self.anchoMaximoFinal:
                            self.menosAnchoFinal += 25

                        if 100 - self.menosAnchoInicial - 10 >= self.anchoMinimoFinal:
                            self.menosAnchoInicial += 10
                        self.i += 1



class historia(object):
    def __init__(self, imagenes, nroImagenes):
        self.mostrando = True
        self.imagenes = imagenes
        self.imagenes_originales = self.imagenes
        self.i = 0
        self.numero = nroImagenes
        self.numero_original = nroImagenes
        self.desaparecer = False
        self.aparecer = False
        self.j = 255
        self.a = 0
        self.imagen_lista = False
        self.imagen_cargada = False
    
    def reiniciar(self):
        self.mostrando = True
        self.i = 0
        self.imagenes = self.imagenes_originales
        for imagen in self.imagenes:
            imagen.set_alpha(255)
        self.numero = self.numero_original
        self.desaparecer = False
        self.aparecer = False
        self.j = 255
        self.a = 0
        self.imagen_lista = False

    def draw(self, win):
        win.blit(self.imagenes[self.i], (0, 0))

    def pasarimagen(self):
        if not self.desaparecer:
            self.imagenes[self.i].set_alpha(0)
            self.i += 1


        if self.i == self.numero:
            self.desaparecer = True
            self.mostrando = False

    def desapareciendo(self, win):
        # .set_alpha sirve para controlar la opacidad de la imagen
        if self.desaparecer and self.i == len(self.imagenes):
            self.imagenes[self.numero - 1].set_alpha(self.j)  # 0 is fully transparent and 255 fully opaque.
            self.j -= 10
            if self.j <= 0:
                self.desaparecer = False
                animacion1.mostrando = True

            win.blit(self.imagenes[self.numero - 1], (0, 0))
    
    def apareciendo_imagen(self, win):
        self.imagenes[0].set_alpha(self.a)                
        win.blit(self.imagenes[0], (0,0))

        self.a += 2
        if self.a >= 255:
            self.imagen_lista = True
            self.imagen_cargada = True



class animacion(object):
    def __init__(self, x):
        self.x = x
        self.x_original = x
        self.mostrando = False
        self.i = 0
        self.velocidad = 2
        self.espera = 0
        self.llegado = False

    def reiniciar(self):
        self.x = self.x_original
        self.mostrando = False
        self.i = 0
        self.velocidad = 2
        self.espera = 0
        self.llegado = False

    def mostrar(self):
        if rana.x < self.x + 10 and not self.llegado:
            rana.x += self.velocidad
        elif rana.x >= self.x + 10 or self.llegado:
            if not self.llegado:
                rana.x -= 20
            self.llegado = True
            
            rana.debe_mirar = True
            rana.debecaminar = False
            self.espera += 1
            '''
            if self.espera > 300:
                rana.debe_mirar = False
                rana.debesaltar = True
                self.mostrando = False '''
                


class estrellas(object):

    def __init__(self, Img, numEstrellas, y2):
        self.numEstrellas = numEstrellas
        self.numEstrellas_original = numEstrellas
        self.estrellasImg = Img
        self.estrellasX = []
        self.estrellasY = []
        self.dibujarlas = False
        self.vel = 4000
        self.desdeDonde = 0
        self.hastaDonde = y2
        # 0 si no aparece, 1 si aparece
        self.aparecerEstrella = []
        for i in range(self.numEstrellas):
            self.aparecerEstrella.append(0)

        for i in range(self.numEstrellas):
            self.estrellasX.append(random.randint(1, 1200))
            self.estrellasY.append(random.randint(-20000 - camaraDeRana.cambio, 600 - camaraDeRana.cambio))

        self.sumatoriaparaestrellas = 0
    
    def reiniciar(self):
        self.numEstrellas = self.numEstrellas_original
        self.estrellasX = []
        self.estrellasY = []
        self.dibujarlas = False
        self.vel = 4000
        self.desdeDonde = 0
        # 0 si no aparece, 1 si aparece
        self.aparecerEstrella = []
        for i in range(self.numEstrellas):
            self.aparecerEstrella.append(0)

        for i in range(self.numEstrellas):
            self.estrellasX.append(random.randint(1, 1200))
            self.estrellasY.append(random.randint(-20000 - camaraDeRana.cambio, 600 - camaraDeRana.cambio))

        self.sumatoriaparaestrellas = 0

    def draw(self, win, desdecuando):
        # AQUI SE DEFINE DESDE CUANDO APARECEN
        if camaraDeRana.cambio <= -desdecuando:
            self.dibujarlas = True
        if self.dibujarlas:
            for i in range(self.numEstrellas):
                if self.sumatoriaparaestrellas // self.vel == i:
                    self.aparecerEstrella[i] = 1
                    if i < (self.numEstrellas):
                        self.aparecerEstrella[i + 1] = 1
                    if i < self.numEstrellas - 1:
                        self.aparecerEstrella[i + 2] = 1
                    if i < self.numEstrellas - 2:
                        self.aparecerEstrella[i + 3] = 1

                if self.aparecerEstrella[i] == 1:
                    win.blit(self.estrellasImg, (self.estrellasX[i], self.estrellasY[i] - camaraDeRana.cambio / 2))
                else:
                    self.sumatoriaparaestrellas += 1
                if self.estrellasY[i] >= screenheight:
                    del self.estrellasX[i]
                    del self.estrellasY[i]


class estrellaFugaz(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imagenes = []
        self.coordenadas = []
        self.coordenadasADibujar = []
        self.i = 0
        self.j = 0
        self.total = 0
        self.limite = 45
        self.bajada = 0
        self.ultimoY = y

        while self.i < self.limite:
            self.coordenadas.append((self.x, self.y))
            self.y += (self.i ** 2) * rana.moduloJump
            self.i += 1

    def dibujar(self, win):

        self.j += 1

        if self.j % 6 == 0 and self.coordenadas:
            self.coordenadasADibujar.append(self.coordenadas[-1])
            del self.coordenadas[-1]

        for coordenada in self.coordenadasADibujar:
            win.blit(imgEstrellaPequena, (coordenada[0], coordenada[1] - self.bajada - camaraDeRana.cambio / 2))
            self.ultimoY = coordenada[1] - self.bajada - camaraDeRana.cambio / 2

        self.bajada -= 0.1


class montonEstrellasFugaces(object):
    def __init__(self, nro, y):
        self.estrellasFugaces = []
        self.nro = nro
        self.nro_original = nro
        self.dibujarEstrellasFugaces = False
        # self.y define cuándo comienzan las estrellas
        self.y = y
        self.y_original = y
        self.sd = 1000

        for i in range(self.nro):
            # Para el range de y se tiene que hacer la siguiente ecuación: ? + camaraDeRana/2 = -y que se quiere -> ? = -(y+camaraDeRana/2)
            self.estrellasFugaces.append(estrellaFugaz(random.randint(0, 1200),
                                                       numpy.random.normal(-self.sd * 3.3,
                                                                           self.sd)))

            # En vez de random randint se puede poner una distribución normal numpy.random.normal(-self.y+1100+camaraDeRana.cambio/2, 1100, size=None)
            # Random random.randint(-self.y + camaraDeRana.cambio / 2,-self.y + 2200 + camaraDeRana.cambio / 2)))
    def reiniciar(self):
        self.estrellasFugaces = []
        self.nro = self.nro_original
        self.dibujarEstrellasFugaces = False
        # self.y define cuándo comienzan las estrellas
        self.y = self.y_original
        self.sd = 1000

        for i in range(self.nro):
            # Para el range de y se tiene que hacer la siguiente ecuación: ? + camaraDeRana/2 = -y que se quiere -> ? = -(y+camaraDeRana/2)
            self.estrellasFugaces.append(estrellaFugaz(random.randint(0, 1200),
                                                       numpy.random.normal(-self.sd * 3.3,
                                                                           self.sd)))
    def draw(self, win):
        if -camaraDeRana.cambio > -self.y:
            self.dibujarEstrellasFugaces = True
        elif -camaraDeRana.cambio > self.y + 1000:
            self.dibujarEstrellasFugaces = False

        if self.dibujarEstrellasFugaces:
            for fugaz in self.estrellasFugaces:
                fugaz.dibujar(win)


class objetosEnElCIelo(object):
    def __init__(self):
        self.avionDibujar = False
        self.avionY = -200
        self.avionAparecer = 1000
        self.avionCamara = 0
        self.xAvion = 500
        self.yOvni = 2000
        self.yNubes = 500
    
    def reiniciar(self):
        self.avionDibujar = False
        self.avionY = -200
        self.avionAparecer = 1000
        self.avionCamara = 0
        self.xAvion = 500
        self.yOvni = 2000
        self.yNubes = 500

    def draw(self, win):
        if -camaraDeRana.cambio > self.avionAparecer and self.xAvion <= 1200 and not self.avionDibujar:
            self.avionDibujar = True
            self.avionCamara = camaraDeRana.cambio
        elif self.avionDibujar and self.xAvion <= 1250:
            win.blit(imgAvion, (self.xAvion, self.avionY - (camaraDeRana.cambio - self.avionCamara) / 2))
            self.xAvion += 0.5


class camara(object):
    def __init__(self):
        self.ydeCambio = 150

        # Es 120 con rana.jumpcoiunt = 50
        self.cambio = 0
        self.limite = 8000

    def reiniciar(self):
        self.ydeCambio = 150
        # Es 120 con rana.jumpcoiunt = 50
        self.cambio = 0
        self.limite = 8000

    def movimientoCamara(self):
        if rana.y <= self.ydeCambio and rana.subiendo and -self.cambio < self.limite:
            rana.moverse = False
            self.cambio += (rana.jumpCount ** 2) * rana.moduloJump
            rana.yinicialoriginal = rana.yreal - self.cambio

        else:

            rana.moverse = True


rana = personaje(185, screenheight - 40 - 40, 48, 24)
camaraDeRana = camara()

# estrellas(imagenestrella, numero de estrellas)
estrellapequeña = estrellas(imgEstrellaPequena, 10000, -20000)
estrellamediana = estrellas(imgEstrellaMediana, 400, -20000)
estrellasFugaces = montonEstrellasFugaces(100, -3000)

# plataforma(self, x, y, width, vel)
generarPlataformas = montonDePlataformas(200)
# Se crea la instacnia de objetos
objetos = objetosEnElCIelo()
historia1 = historia(imgHistoria1, 2)
historia2 = historia(imgHistoria2, 2)
historia2.mostrando = False
animacion1 = animacion(700)



# Función que dibuja todos los objetos, personajes, etc en cada momento
def redrawGameWindow():
    global altura
    global nroDePlataforma
    if not historia1.mostrando and not historia2.imagen_lista:
        camaraDeRana.movimientoCamara()
        win.blit(fondoNoche, (0, screenheight - 22000 - camaraDeRana.cambio/2))
        # Luna

        estrellapequeña.draw(win, 100)
        estrellamediana.draw(win, 100)
        estrellasFugaces.draw(win)
        objetos.draw(win)

        win.blit(imgLuna, (200, -2000 - camaraDeRana.cambio / 2))
        # plataforma, dibujo y movimiento
        if not animacion1.mostrando and not historia1.desaparecer:
            generarPlataformas.draw(win)

        rana.draw(win)
        rana.saltar()
        win.blit(imgBanca, (677, 582 - camaraDeRana.cambio))

        # Este se pone al final para que la imagen de la historia se fade out
        if historia1.desaparecer:
            historia1.desapareciendo(win)
        
        if historia2.mostrando:
            historia2.apareciendo_imagen(win)

    elif historia1.mostrando:
        historia1.draw(win)

    elif historia2.imagen_lista:
        historia2.draw(win)

    
    if resultado == 'perdiste':
        win.blit(imgPlayAgain, (600-255,325-135))


# mainloop
run = True
resultado = None
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()
while run:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    # Dentro de este for vienen las acciones que se deben apretar solo 1 vez y se reinician cuando se apretan de nuevo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if resultado == 'perdiste' or resultado == 'ganaste':
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_y:
                    rana = personaje(185, screenheight - 40 - 40, 48, 24)
                    camaraDeRana.reiniciar()
                    estrellapequeña.reiniciar()
                    estrellamediana.reiniciar()
                    estrellasFugaces.reiniciar()
                    # plataforma(self, x, y, width, vel)
                    generarPlataformas.reiniciar()
                    # Se crea la instacnia de objetos
                    objetos.reiniciar()
                    historia1.reiniciar()
                    historia1.mostrando = True
                    historia2.reiniciar()
                    historia2.mostrando = False
                    animacion1.reiniciar()
                    resultado = None
                    frames = 0

                elif event.key == pygame.K_n:
                    run = False

        if historia1.mostrando:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    historia1.pasarimagen()
                
        elif historia2.mostrando:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and historia2.imagen_cargada:
                    historia2.pasarimagen()
        elif animacion1.mostrando:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    animacion1.mostrando = False
                    rana.debe_mirar = False
                    rana.debesaltar = True
        

    if resultado is None:
        if keys[pygame.K_d]:
            rana.jumpCount = 44.5

        if keys[pygame.K_LEFT]:
            if not historia1.desaparecer and not historia1.mostrando and not animacion1.mostrando:
                rana.moverseIzquierda()

        if keys[pygame.K_RIGHT]:
            if not historia1.desaparecer and not historia1.mostrando and not animacion1.mostrando:
                rana.moverseDerecha()

        if keys[pygame.K_1]:
            run = False

        if animacion1.mostrando:
            animacion1.mostrar()
        
        if rana.y <= -rana.height:
            historia2.mostrando = True
            rana.x = 2000
            rana.final = True
            resultado = 'ganaste'
    
        elif rana.y > screenheight and resultado is None:
            resultado = 'perdiste'
    

    redrawGameWindow()
    pygame.display.update()

pygame.quit()
