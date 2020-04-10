"""
QWidget Class for final window method

"""
import config as conf

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog, QGridLayout, QSizePolicy)
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QBrush

class GameOver(QWidget):
    def __init__(self, players):
        super().__init__()
        self.players = players
        self.winner = []
        self.initUI()
        
    def initUI(self):

        # set path variables
        self.path_to_icon = conf.icons_folder_path
        self.set_winner_player()
        
        # set QWidget style
        self.setGeometry(850, 300, 500, 500)
        self.setWindowTitle('Morsel')
        self.setWindowIcon(QIcon(f'{self.path_to_icon}/blue_logo.png'))

        pixmap = QPixmap(f'{self.path_to_icon}/wooden_back0.png')
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)


        v_layout = QVBoxLayout()

        label_style = "color: '#f4ddc8';"

        header_label = QLabel('MORSEL', self, margin = 10)
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        header_label.setFont(QFont("Calisto MT", 20, QFont.Bold))
        header_label.setStyleSheet(label_style)
        header_label.adjustSize()
        v_layout.addWidget(header_label)

        if len(self.winner) == 1:
            winner_icon_label = QLabel()
            winner_1_icon_pixmap = QPixmap(f'{self.path_to_icon}/{self.players[self.winner[0]]["color"]}_logo.png')
            winner_1_icon_pixmap = winner_1_icon_pixmap.scaledToHeight(150)
            winner_icon_label.setAlignment(QtCore.Qt.AlignCenter)
            winner_icon_label.setPixmap(winner_1_icon_pixmap)
            winner_icon_label.adjustSize()
            v_layout.addWidget(winner_icon_label)

            label_text = f'{self.players[self.winner[0]]["name"]} wins!!!'

        else:
            win_grid = QGridLayout()
            win_grid.setSpacing(10)

            winner_1_icon_label = QLabel()
            winner_1_icon_pixmap = QPixmap(f'{self.path_to_icon}/{self.players[self.winner[0]]["color"]}_logo.png')
            winner_1_icon_pixmap = winner_1_icon_pixmap.scaledToHeight(150)
            winner_1_icon_label.setPixmap(winner_1_icon_pixmap)
            winner_1_icon_label.adjustSize()
            win_grid.addWidget(winner_1_icon_label, 0, 0, QtCore.Qt.AlignCenter)

            winner_2_icon_label = QLabel()
            winner_2_icon_pixmap = QPixmap(f'{self.path_to_icon}/{self.players[self.winner[1]]["color"]}_logo.png')
            winner_2_icon_pixmap = winner_2_icon_pixmap.scaledToHeight(150)
            winner_2_icon_label.setPixmap(winner_2_icon_pixmap)
            winner_2_icon_label.adjustSize()
            win_grid.addWidget(winner_2_icon_label, 0, 1, QtCore.Qt.AlignCenter)
            v_layout.addLayout(win_grid)

            label_text = 'Call it a tie...'

        winner_label = QLabel(label_text, self, margin = 3)
        winner_label.setAlignment(QtCore.Qt.AlignCenter)
        winner_label.setFont(QFont("Lucida Calligraphy", 16)) #Lucida Calligraphy
        winner_label.setStyleSheet(label_style)
        winner_label.adjustSize()
        v_layout.addWidget(winner_label)

        grid = QGridLayout()
        grid.setSpacing(10)

        player_1_label = QLabel('Player 1', self, margin = 10)
        player_1_label.setFont(QFont("Century", 14, QFont.Bold))
        player_1_label.setStyleSheet(label_style)
        player_1_label.adjustSize()
        grid.addWidget(player_1_label, 0, 0, QtCore.Qt.AlignCenter)

        player_2_label = QLabel('Player 2', self, margin = 10)
        player_2_label.setFont(QFont("Century", 14, QFont.Bold))
        player_2_label.setStyleSheet(label_style)
        player_2_label.adjustSize()
        grid.addWidget(player_2_label, 0, 1, QtCore.Qt.AlignCenter)

        player_1_score_label = QLabel(f'{int(self.players["player1"]["score"])}', self, margin = 10)
        player_1_score_label.setFont(QFont("Century", 14, QFont.Bold))
        player_1_score_label.setStyleSheet(label_style)
        player_1_score_label.adjustSize()
        grid.addWidget(player_1_score_label, 1, 0, QtCore.Qt.AlignCenter)

        player_2_score_label = QLabel(f'{int(self.players["player2"]["score"])}', self, margin = 10)
        player_2_score_label.setFont(QFont("Century", 14, QFont.Bold))
        player_2_score_label.setStyleSheet(label_style)
        player_2_score_label.adjustSize()
        grid.addWidget(player_2_score_label, 1, 1, QtCore.Qt.AlignCenter)
        
        v_layout.addLayout(grid)
        v_layout.addStretch(1)
       
        self.setLayout(v_layout)
        
            
    def set_winner_player(self):
        if int(self.players['player1']['score']) > int(self.players['player2']['score']):
            self.winner.append('player1')
        elif int(self.players['player1']['score']) < int(self.players['player2']['score']):
            self.winner.append('player2')
        else:
            self.winner.append('player1')
            self.winner.append('player2')




