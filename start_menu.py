"""
QWidget Class for start menu method

"""
import config as conf
from game import NewGame


from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog, QGridLayout, QSizePolicy)
from PyQt5.QtGui import QFont, QPixmap

class StartMenu(QWidget):
    def __init__(self, players):
        super().__init__()
        self.players = players
        self.initUI()
        
    def initUI(self):

        # set path variables
        self.path_to_icon = conf.icons_folder_path
        

        # set QWidget style
        self.setStyleSheet("background: transparent;")
        #self.setStyleSheet("background-image:icons/red_men.png;")
        #self.setStyleSheet("background-image: url(icons/wooden_back.png);")

        v_layout = QVBoxLayout()

        label_style = "color: '#f4ddc8';"

        header_label = QLabel('MORSEL', self, margin = 10)
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        header_label.setFont(QFont("Calisto MT", 20, QFont.Bold))
        header_label.setStyleSheet(label_style)
        header_label.adjustSize()
        v_layout.addWidget(header_label)

        description_label = QLabel('Game for two players.\nBased on the original "Carcassonne" board game by Claus-Urgen Berde.\nNot for commertial use.', self, margin = 3)
        description_label.setAlignment(QtCore.Qt.AlignCenter)
        description_label.setFont(QFont("Lucida Calligraphy", 10)) #Lucida Calligraphy
        description_label.setStyleSheet(label_style)
        description_label.adjustSize()
        v_layout.addWidget(description_label)

        grid = QGridLayout()
        grid.setSpacing(10)

        player_1_label = QLabel('Player 1', self, margin = 10)
        player_1_label.setFont(QFont("Century", 15, QFont.Bold))
        player_1_label.setStyleSheet(label_style)
        player_1_label.adjustSize()
        grid.addWidget(player_1_label, 0, 0, QtCore.Qt.AlignCenter)

        player_2_label = QLabel('Player 2', self, margin = 10)
        player_2_label.setFont(QFont("Century", 15, QFont.Bold))
        player_2_label.setStyleSheet(label_style)
        player_2_label.adjustSize()
        grid.addWidget(player_2_label, 0, 1, QtCore.Qt.AlignCenter)

        player_1_icon_label = QLabel()
        player_1_icon_pixmap = QPixmap(f'{self.path_to_icon}/{self.players["player1"]["color"]}_logo.png')
        player_1_icon_pixmap = player_1_icon_pixmap.scaledToHeight(150)
        player_1_icon_label.setPixmap(player_1_icon_pixmap)
        player_1_icon_label.adjustSize()
        grid.addWidget(player_1_icon_label, 1, 0, QtCore.Qt.AlignCenter)

        player_2_icon_label = QLabel()
        player_2_icon_pixmap = QPixmap(f'{self.path_to_icon}/{self.players["player2"]["color"]}_logo.png')
        player_2_icon_pixmap = player_2_icon_pixmap.scaledToHeight(150)
        player_2_icon_label.setPixmap(player_2_icon_pixmap)
        player_2_icon_label.adjustSize()
        grid.addWidget(player_2_icon_label, 1, 1, QtCore.Qt.AlignCenter)
        
        v_layout.addLayout(grid)
        v_layout.addStretch(1)

        q_button_style = "QPushButton:pressed {background-color: #958475; border-radius: 2px; color: '#f4ddc8'} QPushButton {background-color: #423b35; border-radius: 2px; color: '#f4ddc8'}"

        h_box = QHBoxLayout()
        h_box.addStretch(1)

        self.start_btn = QPushButton('Start New Game', self)
        self.start_btn.setFont(QFont("Century", 15, QFont.Bold))
        self.start_btn.setStyleSheet(q_button_style)
        self.start_btn.setMinimumSize(QtCore.QSize(200, 50))
        h_box.addWidget(self.start_btn)
        self.start_btn.clicked.connect(self.start_new_game)
        h_box.addStretch(1)
        v_layout.addLayout(h_box)
        
        self.setLayout(v_layout)
        
            
    def start_new_game(self):
        self.players['player1']['score'] = 0
        self.players['player2']['score'] = 0
        self.new_game_window = NewGame(self.players)
        self.new_game_window.show()


