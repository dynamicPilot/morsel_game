"""
QWidget Class for game method

"""
import random

import config as conf

from tail_preparing import TailsData

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog, QGridLayout, QSizePolicy, QApplication, QScrollArea, QMessageBox)
from PyQt5.QtGui import QFont, QPixmap

class NewGame(QWidget):
    def __init__(self, players):
        super().__init__()
        self.players = players
        self.initUI()
        
    def initUI(self):

        #self.showFullScreen()

        # set path variables
        self.path_to_icon = conf.icons_folder_path
        self.path_to_tail = conf.tail_folder_path

        self.tails_data = TailsData()
        self.tails = self.tails_data.tails
        self.game_desk = None

        # set game flow control variables
        self.active_player = None
        self.rest_player = None
        self.game_over = None

        # set global style sheets for buttons
        self.add_tail_btn_style = ["QPushButton {background: transparent; border: none; color: 'white'}", "QPushButton:pressed {background-color: #181e1a; border-radius: 2px; color: 'white'} QPushButton {background-color: #1b3522; border-radius: 2px; color: 'white'}"]

        # set QWidget style
        self.setStyleSheet("background-color:white;")

        #set window params
        self.setGeometry(25, 40, 1900, 1000)
        self.setWindowTitle('Carcassonne')

        v_layout = QVBoxLayout()

        #self.quit_btn = QPushButton('Quit')
        #self.quit_btn.clicked.connect(QtCore.QCoreApplication.quit)
        #v_layout.addWidget(self.quit_btn)

        header_label = QLabel('CARCASSONNE', self, margin = 10)
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        header_label.setFont(QFont("Calisto MT", 30, QFont.Bold))
        header_label.adjustSize()
        v_layout.addWidget(header_label)
        
        h_box = QHBoxLayout()

        self.create_player_desk('player1')
        h_box.addWidget(self.players['player1']['desk'])

        self.create_game_desk()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(QtCore.Qt.AlignCenter)
        scroll_area.setWidget(self.game_desk)

        #scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        h_box.addWidget(scroll_area)

        #h_box.addStretch(1)

        self.create_player_desk('player2')
        h_box.addWidget(self.players['player2']['desk'])

        v_layout.addLayout(h_box)
        v_layout.addStretch(1)

        btn_h_box = QHBoxLayout()
        btn_h_box.addStretch(1)

        start_button_style = "QPushButton:pressed {background-color: #504e53; border-radius: 2px; color: 'white'} QPushButton {background-color: #534a63; border-radius: 2px; color: 'white'}"

        self.start_game_btn = QPushButton('Start Game', self)
        self.start_game_btn.setFont(QFont("Century", 15, QFont.Bold))
        self.start_game_btn.setStyleSheet(start_button_style)
        self.start_game_btn.setMinimumSize(QtCore.QSize(150, 50))
        btn_h_box.addWidget(self.start_game_btn)
        self.start_game_btn.clicked.connect(self.start_game)

        end_button_style = "QPushButton:pressed {background-color: #504e53; border-radius: 2px; color: 'white'} QPushButton {background-color: #534a63; border-radius: 2px; color: 'white'}"

        self.end_game_btn = QPushButton('End Game', self)
        self.end_game_btn.setFont(QFont("Century", 15, QFont.Bold))
        self.end_game_btn.setStyleSheet(end_button_style)
        self.end_game_btn.setMinimumSize(QtCore.QSize(150, 50))
        btn_h_box.addWidget(self.end_game_btn)
        self.end_game_btn.clicked.connect(QtCore.QCoreApplication.quit)

        btn_h_box.addStretch(1)
        
        v_layout.addLayout(btn_h_box)

        self.setLayout(v_layout)
        
    def create_game_desk(self):
        self.game_desk = QWidget()
        self.game_desk.setContentsMargins(5, 5, 5, 5)
        self.game_desk.setStyleSheet("background-color:white; border-style: outset; border-color:'black'; border-width: 2px; border-radius: 5px;")
        desk_width = conf.tail_size*conf.game_grid_width
        desk_height = conf.tail_size*conf.game_grid_height
        self.game_desk.setMinimumSize(QtCore.QSize(desk_width, desk_height))
        self.game_desk.setMaximumSize(QtCore.QSize(desk_width, desk_height))
        self.game_grid = [[{'widget': None, 'empty': True, 'tail': None} for i in range(conf.game_grid_width)] for j in range(conf.game_grid_height)]

        grid = QGridLayout()
        grid.setSpacing(5)

        # create empty game grid
        for col in range(conf.game_grid_width):
            for row in range(conf.game_grid_height):
                tail_widget = self.create_tail_container()
                self.game_grid[row][col]['widget'] = tail_widget
                grid.addWidget(tail_widget, row, col, QtCore.Qt.AlignCenter)
        
        # set start tail
        self.set_tail_to_container(self.game_grid[conf.start_tail_position[0]][conf.start_tail_position[0]]['widget'], self.tails[0]['name'])

        self.game_desk.setLayout(grid)


    def create_tail_container(self, tail_size = conf.tail_size):
        tail_container_label = QLabel()
        tail_container_label.setStyleSheet("background-color: #ebebeb; border-style: outset; border-color: #5b5c5b; border-width: 1px; border-radius: 2px;")
        tail_container_label.setAlignment(QtCore.Qt.AlignCenter)
        tail_container_label.setMinimumSize(QtCore.QSize(tail_size, tail_size))
        tail_container_label.setMaximumSize(QtCore.QSize(tail_size, tail_size))
        return tail_container_label

    def set_tail_to_container(self, tail_container_label, tail_img_name, tail_size = conf.tail_size):
        tail_pixmap = QPixmap(f'{self.path_to_tail}/{tail_img_name}.png')
        tail_pixmap = tail_pixmap.scaledToHeight(tail_size)
        tail_container_label.setPixmap(tail_pixmap)
        tail_container_label.setAlignment(QtCore.Qt.AlignCenter)

    def create_player_desk(self, player_key):
        player_desk = QWidget()
        player_desk.setStyleSheet("background-color:white; border-style: outset; border-color:'black'; border-width: 2px; border-radius: 5px;")
        player_desk.setMinimumSize(QtCore.QSize(250, 800))
        player_desk.setMaximumSize(QtCore.QSize(250, 950))
        player_desk.setContentsMargins(5, 5, 5, 5)
        player_name = self.players[player_key]['name']
        
        v_box = QVBoxLayout()
        
        player_label = QLabel(player_name, self, margin = 10)
        player_label.setAlignment(QtCore.Qt.AlignCenter)
        player_label.setFont(QFont("Century", 15, QFont.Bold))
        player_label.adjustSize()
        v_box.addWidget(player_label, alignment=QtCore.Qt.AlignCenter)
        
        player_icon_label = QLabel()
        player_icon_pixmap = QPixmap(f'{self.path_to_icon}/{self.players[player_key]["color"]}_circle.png')
        player_icon_pixmap = player_icon_pixmap.scaledToHeight(50)
        player_icon_label.setPixmap(player_icon_pixmap)
        player_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        player_icon_label.adjustSize()
        v_box.addWidget(player_icon_label, alignment=QtCore.Qt.AlignCenter)
        
        tail_widget = self.create_tail_container(conf.player_tail_size)
        tail_widget.adjustSize()
        v_box.addWidget(tail_widget, alignment=QtCore.Qt.AlignCenter)
        v_box.addStretch(1)

        #add_tail_btn_style = "QPushButton:pressed {background-color: #181e1a; border-radius: 2px; color: 'white'} QPushButton {background-color: #1b3522; border-radius: 2px; color: 'white'}"

        add_tail_btn = QPushButton('Add Tail', self)
        add_tail_btn.setFont(QFont("Century", 10, QFont.Bold))
        add_tail_btn.setStyleSheet(self.add_tail_btn_style[0])
        add_tail_btn.setEnabled(False)
        add_tail_btn.setMinimumSize(QtCore.QSize(100, 50))
        v_box.addWidget(add_tail_btn, alignment=QtCore.Qt.AlignCenter)

        if player_key == "player1":
            add_tail_btn.clicked.connect(self.add_new_tail_to_player1)
        else:
            add_tail_btn.clicked.connect(self.add_new_tail_to_player2)
        v_box.addStretch(1)
        
        player_desk.setLayout(v_box)
        
        # add widget to players dictionary
        self.players[player_key]['desk'] = player_desk
        self.players[player_key]['tail_widget'] = tail_widget
        self.players[player_key]['add_tail_btn'] = add_tail_btn


    def start_game(self):
        self.tails = self.tails_data.tails
        self.tails = self.tails[1:]
        random.shuffle(self.tails)
        players_list = ['player1', 'player2']
        random.shuffle(players_list)
        self.active_player = players_list[0]
        self.rest_player = players_list[1]
        print(self.active_player)
        self.game_over = False
        self.make_add_tail_button_visible()
        self.start_game_btn.setEnabled(False)


    # make visible active player 'Add Tail' button
    def make_add_tail_button_visible(self):
        active_button = self.players[self.active_player]['add_tail_btn']
        active_button.setStyleSheet(self.add_tail_btn_style[1])
        active_button.setEnabled(True)

        rest_button = self.players[self.rest_player]['add_tail_btn']
        rest_button.setStyleSheet(self.add_tail_btn_style[0])
        rest_button.setEnabled(False)


    def add_new_tail_to_player1(self):
        if len(self.tails) > 0:
            tail = self.tails.pop(0)
            tail_name = tail['name']
            tail_widget = self.players['player1']['tail_widget']
            self.set_tail_to_container(tail_widget, tail_name, conf.player_tail_size)
        else:
            self.game_over = True
            self.game_over_state()

    def add_new_tail_to_player2(self):
        if len(self.tails) > 0:
            tail = self.tails.pop(0)
            tail_name = tail['name']
            tail_widget = self.players['player2']['tail_widget']
            self.set_tail_to_container(tail_widget, tail_name, conf.player_tail_size)
        else:
            self.game_over = True
            self.game_over_state()

    def game_over_state(self):
        if self.game_over:
            self.start_game_btn.setEnabled(True)
            mes_text = "Game is over!"
            mes = QMessageBox()
            mes.setWindowTitle('Message')
            mes.setText(mes_text)
            mes.exec()
            




