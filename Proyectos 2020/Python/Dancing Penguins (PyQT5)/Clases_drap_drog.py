import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
import os 
from parametros import PRECIO_PINGU

#EN ESTE ARCHIVO SE CREAN CLASES QUE HEREDAN DE QLABEL HECHAS ESPECIALMENTE PARA PODER ARRASTRAR LA
#IMAGEN DE LOS PINGUINOS A LA PISTA DE BAILE.
#ADEMÁS, SE CREAN FUNCIONES QUE FACILITAN LA LECTURA DE LOS OTROS ARCHIVOS.

class DragLabel(QLabel):
    global PRECIO_PINGU
    def __init__(self, *args):
        super().__init__(*args)
        self.__dinero = 0
    
    @property
    def dinero(self):
        return self.__dinero
    @dinero.setter
    def dinero(self, valor):
        if valor <= 0:
            self.__dinero = 0
        else:
            self.__dinero = valor
        

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.dinero >= PRECIO_PINGU:
            self.drag_start_position = event.pos()
 
    def mouseMoveEvent(self, event):
        if not(event.buttons() & Qt.LeftButton):
            return
        elif self.dinero >= PRECIO_PINGU:
            drag = QDrag(self)
            mimedata = QMimeData()
            mimedata.setImageData(self.pixmap().toImage())
            drag.setMimeData(mimedata)
            # createing the dragging effect
            pixmap = QPixmap(self.size()) # label size
            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            painter.end()
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)
 
class DropLabel(QLabel):
    def __init__(self, pantalla, *args):
        super().__init__(pantalla, *args)
        self.setAcceptDrops(True)
        
 
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage() and not self.pixmap():
            
            event.acceptProposedAction()
 
    def dropEvent(self, event):
        pos = event.pos()
        
        text = event.mimeData().imageData()
        self.senal_descontar_dinero.emit()
        text = QPixmap.fromImage(text)
        self.setPixmap(text)
        
        self.setScaledContents(True)
        event.acceptProposedAction()




#FUNCIONES PARA FACILITAR LA LECTURA DEL CÓDIGO: Disminuir el número de lineas a escribir.
#Se crea una función para agregar imágenes para no tener que poner las mismas lineas siempre

def agregar_imagen(ventana, ubicacion, x , y , width, height):
    ventana.label = QLabel(ventana)
    ventana.label.setGeometry(x,y,width,height)
    pixeles = QPixmap(ubicacion)
    ventana.label.setPixmap(pixeles)
    ventana.label.setScaledContents(True)
    return ventana.label


#una función para agregar labels que pueden ser arrastradas
def drag_imagen(ventana, ubicacion, x , y , width, height):
    ventana.label = DragLabel(ventana)
    ventana.label.setGeometry(x,y,width,height)
    pixeles = QPixmap(ubicacion)
    ventana.label.setPixmap(pixeles)
    ventana.label.setScaledContents(True)
    return ventana.label

#función que crea botón
def crear_boton(texto, ventana, posicion_x, posicion_y, funcion ):
    boton = QPushButton(texto, ventana)
    boton.resize(boton.sizeHint())
    boton.move(posicion_x, posicion_y)
    boton.clicked.connect(funcion)
    return boton

#función que crea un label con texto
def label_texto(texto, ventana, tamaño_letra, x, y, width, length):
    label = QLabel(texto,ventana)
    label.setFont(QFont('Arial', tamaño_letra))
    label.setGeometry(x,y,width,length)
    return label



    
