import config as conf

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog, QGridLayout, QSizePolicy, QApplication, QScrollArea, QMessageBox)
from PyQt5.QtGui import QFont, QDrag, QPixmap, QPainter, QImage, QTransform

class DragLabel(QLabel):
    """
    Customize QLabel for Drag label for player's current tail display.
    """
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

class DragCharLabel(QLabel):
    """
    Customize QLabel for Drag label for player's chars display.
    Need: char_list_id, char_list.
    """
    def __init__(self, parent, char_list_id, char_list, game_state, player, active_player):
        super().__init__(parent)
        self.char_list_id = char_list_id
        self.char_list = char_list
        self.game_state = game_state
        self.player = player
        self.active_player = active_player

    def mousePressEvent(self, event):
        if self.active_player[0] != self.player:
            event.ignore()
            return
        if not(self.game_state[0] == 'set tail' or self.game_state[0] == 'reset char'):
            event.ignore()
            return
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = event.pos()
        
    def mouseMoveEvent(self, event):
        if self.active_player[0] != self.player:
            event.ignore()
            return
        if not(self.game_state[0] == 'set tail' or self.game_state[0] == 'reset char'):
            event.ignore()
            return
        if not(event.buttons() & QtCore.Qt.LeftButton):
            return

        print('active player ', self.active_player[0], ' player ', self.player, self.active_player[0] == self.player)
        
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

        self.clear() # clear drag label
        self.char_list[self.char_list_id]['active'] = True # set current char in char_list active

        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)

class DropLabel(QLabel):
    """
    Customize QLabel for Drop label.
    Need: game_desk_id, game_grid, game_state.
    Properties: pix_state - state of pixmap element (can be "empty", "tail", "char", "ready").
    """
    def __init__(self, parent, game_desk_id, game_grid, game_state):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.game_desk_id = game_desk_id
        self.game_grid = game_grid # common game_grid
        self.pix_state = 'empty' #"tail", "char", "ready"
        self.game_state = game_state
        self.original_tail = None
        self.original_char = None
        self.char_positions = {'top': (conf.tail_size/2-conf.char_picture_size/2, 10), 
        'right': (conf.tail_size-10-conf.char_picture_size, conf.tail_size/2 - conf.char_picture_size/2), 
        'bot': (conf.tail_size/2- conf.char_picture_size/2, conf.tail_size-10-conf.char_picture_size),
        'left': (10, conf.tail_size/2-conf.char_picture_size/2),
        'center': (conf.tail_size/2- conf.char_picture_size/2, conf.tail_size/2-conf.char_picture_size/2)}


    def dragEnterEvent(self, event):
        if self.pix_state == 'ready':
            event.ignore()
        elif self.pix_state == 'empty' and self.game_state[0] == 'reset tail':
            if event.mimeData().hasImage():
                event.accept()
            else:
                event.ignore()
        elif self.pix_state == 'char' and (self.game_state[0] == 'reset char' or self.game_state[0] == 'set tail'):
            if event.mimeData().hasImage():
                event.accept()
            else:
                event.ignore()
        elif self.pix_state == 'tail' and self.game_state[0] == 'reset tail':
            if event.mimeData().hasImage():
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasImage() and self.pix_state == "empty":
            self.game_grid[self.game_desk_id[0]][self.game_desk_id[1]]['active'] = True
            print("make active: ", self.game_desk_id)
            tail = QPixmap.fromImage(QImage(event.mimeData().imageData()))
            self.original_tail = tail
            self.setPixmap(tail)
            self.pix_state = "tail"

        if event.mimeData().hasImage() and self.pix_state == "char":
            self.original_char = QPixmap.fromImage(QImage(event.mimeData().imageData()))
            char_and_tail = QPixmap(self.size())
            painter = QPainter(char_and_tail)
            painter.drawPixmap(self.rect(), self.original_tail)
            painter.drawPixmap(self.char_positions['top'][0], self.char_positions['top'][1], self.original_char)
            painter.end()
            self.setPixmap(char_and_tail)
            self.game_grid[self.game_desk_id[0]][self.game_desk_id[1]]['char_side'] = 'top'


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton and self.pix_state == "tail": 
            tail = self.pixmap()
            transf = QTransform()
            transf.rotate(90)
            rotated = tail.transformed(transf, mode=QtCore.Qt.SmoothTransformation)
            self.original_tail = rotated
            self.setPixmap(rotated)
            self.game_grid[self.game_desk_id[0]][self.game_desk_id[1]]['transform'] += 1

        if event.button() == QtCore.Qt.RightButton and self.pix_state == "char":
            start_side = self.game_grid[self.game_desk_id[0]][self.game_desk_id[1]]['char_side']

            next_side = None
            if start_side == "top":
                next_side = "right"
            elif start_side == "right":
                next_side = "bot"
            elif start_side == "bot":
                next_side = "left"
            elif start_side == "left":
                next_side = "center"
            else:
                next_side = "top"

            char_and_tail = QPixmap(self.size())
            painter = QPainter(char_and_tail)
            painter.drawPixmap(self.rect(), self.original_tail)
            painter.drawPixmap(self.char_positions[next_side][0], self.char_positions[next_side][1], self.original_char)
            painter.end()

            self.setPixmap(char_and_tail)
            self.game_grid[self.game_desk_id[0]][self.game_desk_id[1]]['char_side'] = next_side

        else:
            return

    def reset_char(self):
        tail = QPixmap(self.size())
        painter = QPainter(tail)
        painter.drawPixmap(self.rect(), self.original_tail)
        painter.end()
        self.setPixmap(tail)

    def display_message(self, text):
        mes = QMessageBox()
        mes.setFont(QFont("Century", 10))
        mes.setWindowTitle('Message')
        mes.setMinimumSize(QtCore.QSize(200, 100))
        mes.setText(text)
        mes.exec()







