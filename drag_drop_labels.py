import config as conf

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog, QGridLayout, QSizePolicy, QApplication, QScrollArea, QMessageBox)
from PyQt5.QtGui import QFont, QDrag, QPixmap, QPainter, QImage, QTransform

class DragLabel(QLabel):

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not(event.buttons() & QtCore.Qt.LeftButton):
            return
        
        drag = QDrag(self)
 
        mime_data = QtCore.QMimeData()
        pixmap_data = self.pixmap()
        mime_data.setImageData(pixmap_data.toImage())
        drag.setMimeData(mime_data)

        # createing the dragging effect
        pixmap = QPixmap(self.size()) # label size
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()

        self.clear()

        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)

class DropLabel(QLabel):
    def __init__(self, parent, game_desk_id, game_grid):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.game_desk_id = game_desk_id
        self.game_grid = game_grid


    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage():
            self.game_grid[self.game_desk_id[0]][self.game_desk_id[1]]['active'] = True
            print("active true: ", self.game_desk_id)
            tail = QPixmap.fromImage(QImage(event.mimeData().imageData()))
            self.setPixmap(tail)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton: 
            tail = self.pixmap()
            transf = QTransform()
            transf.rotate(90)
            rotated = tail.transformed(transf, mode=QtCore.Qt.SmoothTransformation)
            self.setPixmap(rotated)
            self.game_grid[self.game_desk_id[0]][self.game_desk_id[1]]['transform'] += 1






