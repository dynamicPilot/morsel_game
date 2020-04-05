"""
QWidget Class for game method

"""
import random

import config as conf

from tail_preparing import TailsData
from drag_drop_labels import DragLabel, DropLabel

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

        self.active_tail = None
        self.active_desk_id = None
        self.game_desk_id = None
        
        self.game_state = None

        # set global style sheets for buttons
        self.add_tail_btn_style = ["QPushButton {background: transparent; border: none; color: 'white'}", "QPushButton:pressed {background-color: #181e1a; border-radius: 2px; color: 'white'} QPushButton {background-color: #1b3522; border-radius: 2px; color: 'white'}"]
        self.reset_tail_btn_style = ["QPushButton {background: transparent; border: none; color: 'white'}", "QPushButton:pressed {background-color: #9f7224; border-radius: 2px; color: 'white'} QPushButton {background-color: #9f7224; border-radius: 2px; color: 'white'}"]
        self.set_tail_btn_style = ["QPushButton {background: transparent; border: none; color: 'white'}", "QPushButton:pressed {background-color: #2f395a; border-radius: 2px; color: 'white'} QPushButton {background-color: #2f395a; border-radius: 2px; color: 'white'}"]
        

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
        self.game_grid = [[{'widget': None, 'tail': None, 'player': None, 'active': False, 'transform': 0} for i in range(conf.game_grid_width)] for j in range(conf.game_grid_height)]

        grid = QGridLayout()
        grid.setSpacing(5)

        # create empty game grid
        for col in range(conf.game_grid_width):
            for row in range(conf.game_grid_height):
                self.game_desk_id = (row, col)
                tail_widget = self.create_tail_container()
                self.game_grid[row][col]['widget'] = tail_widget
                grid.addWidget(tail_widget, row, col, QtCore.Qt.AlignCenter)
        
        # set start tail
        self.set_tail_to_container(self.game_grid[conf.start_tail_position[0]][conf.start_tail_position[0]]['widget'], self.tails[0]['name'])
        self.game_grid[conf.start_tail_position[0]][conf.start_tail_position[0]]['tail'] = self.tails[0]['number']

        self.game_desk.setLayout(grid)


    def create_tail_container(self, tail_size = conf.tail_size, is_drag = False):
        if not is_drag:
            tail_container_label = DropLabel(self, self.game_desk_id, self.game_grid)
        else:
            tail_container_label = DragLabel(self)

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
        
        player_icon_label = QLabel(self)
        player_icon_pixmap = QPixmap(f'{self.path_to_icon}/{self.players[player_key]["color"]}_circle.png')
        player_icon_pixmap = player_icon_pixmap.scaledToHeight(50)
        player_icon_label.setPixmap(player_icon_pixmap)
        player_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        player_icon_label.adjustSize()
        v_box.addWidget(player_icon_label, alignment=QtCore.Qt.AlignCenter)
        v_box.addStretch(1)
        
        tail_widget = self.create_tail_container(conf.player_tail_size, True)
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

        reset_tail_btn = QPushButton('Reset Tail', self)
        reset_tail_btn.setFont(QFont("Century", 10, QFont.Bold))
        reset_tail_btn.setStyleSheet(self.reset_tail_btn_style[0])
        reset_tail_btn.setEnabled(False)
        reset_tail_btn.setMinimumSize(QtCore.QSize(100, 50))
        v_box.addWidget(reset_tail_btn, alignment=QtCore.Qt.AlignCenter)

        set_tail_btn = QPushButton('Set Tail', self)
        set_tail_btn.setFont(QFont("Century", 10, QFont.Bold))
        set_tail_btn.setStyleSheet(self.set_tail_btn_style[0])
        set_tail_btn.setEnabled(False)
        set_tail_btn.setMinimumSize(QtCore.QSize(100, 50))
        v_box.addWidget(set_tail_btn, alignment=QtCore.Qt.AlignCenter)

        if player_key == "player1":
            add_tail_btn.clicked.connect(self.add_new_tail_to_player1)
            reset_tail_btn.clicked.connect(self.reset_new_tail_to_player1)
            set_tail_btn.clicked.connect(self.set_new_tail_to_player1)
        else:
            add_tail_btn.clicked.connect(self.add_new_tail_to_player2)
            reset_tail_btn.clicked.connect(self.reset_new_tail_to_player2)
            set_tail_btn.clicked.connect(self.set_new_tail_to_player2)
        v_box.addStretch(1)
        
        player_desk.setLayout(v_box)
        
        # add widget to players dictionary
        self.players[player_key]['desk'] = player_desk
        self.players[player_key]['tail_widget'] = tail_widget
        self.players[player_key]['add_tail_btn'] = add_tail_btn
        self.players[player_key]['reset_tail_btn'] = reset_tail_btn
        self.players[player_key]['set_tail_btn'] = set_tail_btn


    def start_game(self):
        self.tails = self.tails_data.tails
        self.tails = self.tails[1:]
        random.shuffle(self.tails)
        players_list = ['player1', 'player2']
        random.shuffle(players_list)
        self.active_player = players_list[0]
        self.rest_player = players_list[1]
        self.game_over = False
        self.game_state = 'add new'
        self.make_player_button_visible()
        self.start_game_btn.setEnabled(False)

        for col in range(conf.game_grid_width):
            for row in range(conf.game_grid_height):
                if col != conf.start_tail_position[0] and row != conf.start_tail_position[0]:
                    self.game_grid[row][col]['transform'] = 0
                    self.game_grid[row][col]['tail'] = None
                    self.game_grid[row][col]['player'] = None
                    self.game_grid[row][col]['active'] = False
                    self.game_grid[row][col]['widget'].clear()



    # make visible active player 'Add Tail' and other buttons
    def make_player_button_visible(self):
        add_new_active_button = self.players[self.active_player]['add_tail_btn']
        add_new_active_button.setStyleSheet(self.add_tail_btn_style[1])
        add_new_active_button.setEnabled(True)

        reset_new_active_button = self.players[self.active_player]['reset_tail_btn']
        reset_new_active_button.setStyleSheet(self.reset_tail_btn_style[1])
        reset_new_active_button.setEnabled(True)

        set_new_active_button = self.players[self.active_player]['set_tail_btn']
        set_new_active_button.setStyleSheet(self.set_tail_btn_style[1])
        set_new_active_button.setEnabled(True)

        add_new_rest_button = self.players[self.rest_player]['add_tail_btn']
        add_new_rest_button.setStyleSheet(self.add_tail_btn_style[0])
        add_new_rest_button.setEnabled(False)

        reset_new_rest_button = self.players[self.rest_player]['reset_tail_btn']
        reset_new_rest_button.setStyleSheet(self.reset_tail_btn_style[0])
        reset_new_rest_button.setEnabled(False)

        set_new_rest_button = self.players[self.rest_player]['set_tail_btn']
        set_new_rest_button.setStyleSheet(self.set_tail_btn_style[0])
        set_new_rest_button.setEnabled(False)


    def add_new_tail_to_player1(self):
        if len(self.tails) > 0 and self.game_state == 'add new':
            tail = self.tails.pop(0)
            self.active_tail = tail
            tail_name = tail['name']
            tail_widget = self.players['player1']['tail_widget']
            self.set_tail_to_container(tail_widget, tail_name, conf.player_tail_size)
            self.game_state = 'reset'
        elif len(self.tails) <= 0:
            self.game_over = True
            self.game_over_state()
        else:
            return

    def add_new_tail_to_player2(self):
        if len(self.tails) > 0 and self.game_state == 'add new':
            tail = self.tails.pop(0)
            self.active_tail = tail
            tail_name = tail['name']
            tail_widget = self.players['player2']['tail_widget']
            self.set_tail_to_container(tail_widget, tail_name, conf.player_tail_size)
            self.game_state = 'reset'
        elif len(self.tails) <= 0:
            self.game_over = True
            self.game_over_state()
        else:
            return

    def set_new_tail_to_player1(self):
        
        if self.game_state == 'reset':

            # Set active desk widget
            self.set_active_desk_id()
            tail_check = self.check_tail_location()
            if tail_check:
                self.game_state == 'set'
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['active'] = False
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['tail'] = self.active_tail['number']
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['player'] = self.active_player
                self.next_turn()
            else:
                self.reset_new_tail_to_player1()

    def set_new_tail_to_player2(self):

        if self.game_state == 'reset':

            # Set active desk widget
            self.set_active_desk_id()
            tail_check = self.check_tail_location()
            if tail_check:
                self.game_state == 'set'
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['active'] = False
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['tail'] = self.active_tail['number']
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['player'] = self.active_player
                self.next_turn()
            else:
                self.reset_new_tail_to_player2()

    def check_tail_location(self):
        print(self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['transform'])
        self.transform_tail_sides()
        row = self.active_desk_id[0]
        col = self.active_desk_id[1]
        top_tail_edge = self.active_tail['top']
        bot_tail_edge = self.active_tail['bot']
        right_tail_edge = self.active_tail['right']
        left_tail_edge = self.active_tail['left']
        none_sides = 0

        # neighbor tails check
        if row > 0:
            if self.game_grid[row-1][col]['tail'] is not None:
                tail_number = self.game_grid[row-1][col]['tail']
                top_neighbor_tail_edge = self.tails_data.tails[int(tail_number)]['bot']
                if top_neighbor_tail_edge != top_tail_edge:
                    self.display_message("Top side is incorrect.")
                    print(top_neighbor_tail_edge, top_tail_edge)
                    return False
            else:
                none_sides += 1
        if row < conf.game_grid_height-1:
            if self.game_grid[row+1][col]['tail'] is not None:
                tail_number = self.game_grid[row+1][col]['tail']
                bot_neighbor_tail_edge = self.tails_data.tails[int(tail_number)]['top']
                if bot_neighbor_tail_edge != bot_tail_edge:
                    self.display_message("Bottom side is incorrect.")
                    print(bot_neighbor_tail_edge, bot_tail_edge)
                    return False
            else:
                none_sides += 1
        if col > 0:
            if self.game_grid[row][col-1]['tail'] is not None:
                tail_number = self.game_grid[row][col-1]['tail']
                left_neighbor_tail_edge = self.tails_data.tails[int(tail_number)]['right']
                if left_neighbor_tail_edge != left_tail_edge:
                    self.display_message("Left side is incorrect.")
                    print(left_neighbor_tail_edge, left_tail_edge)
                    return False
            else:
                none_sides += 1
        if col < conf.game_grid_width-1:
            if self.game_grid[row][col+1]['tail'] is not None:
                tail_number = self.game_grid[row][col+1]['tail']
                right_neighbor_tail_edge = self.tails_data.tails[int(tail_number)]['left']
                if right_neighbor_tail_edge != right_tail_edge:
                    self.display_message("Right side is incorrect.")
                    print(right_neighbor_tail_edge, right_tail_edge)
                    return False
            else:
                none_sides += 1
        
        if none_sides == 4:
            self.display_message("Your tail does not have got a neighbor.")     
            return False

        print("Accept!")
        return True

    def transform_tail_sides(self):
        rotate_number = self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['transform'] % 4

        while (rotate_number > 0):
            top_tail_edge = self.active_tail['top']

            self.active_tail['top'] = self.active_tail['left']
            self.active_tail['left'] = self.active_tail['bot']
            self.active_tail['bot'] = self.active_tail['right']
            self.active_tail['right'] = top_tail_edge

            rotate_number-=1

        self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['transform'] = 0

    def set_original_tail_sides(self):
        tail_number = self.active_tail['number']
        self.active_tail = self.tails_data.tails[int(tail_number)]

    def next_turn(self):

        if len(self.tails) > 0:
            self.active_player, self.rest_player = self.rest_player, self.active_player
            self.game_state = 'add new'
            self.make_player_button_visible()
        else:
            self.game_over = True
            self.game_over_state()


    def reset_new_tail_to_player1(self):

        if self.game_state == 'reset':
            self.set_active_desk_id()
            self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['widget'].clear()
            self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['active'] = False
            self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['transform'] = 0
            self.set_original_tail_sides()
            
            tail_widget = self.players['player1']['tail_widget']
            tail_name = self.active_tail['name']
            self.set_tail_to_container(tail_widget, tail_name, conf.player_tail_size)
        else:
            return
        

    def reset_new_tail_to_player2(self):

        if self.game_state == 'reset':
            self.set_active_desk_id()
            self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['widget'].clear()
            self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['active'] = False
            self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['transform'] = 0
            self.set_original_tail_sides()
            
            tail_widget = self.players['player2']['tail_widget']
            tail_name = self.active_tail['name']
            self.set_tail_to_container(tail_widget, tail_name, conf.player_tail_size)
        else:
            return
        
    def set_active_desk_id(self):
        for col in range(conf.game_grid_width):
            for row in range(conf.game_grid_height):
                if self.game_grid[row][col]['active'] == True:
                    self.active_desk_id = [row, col]
                    return

    def game_over_state(self):
        if self.game_over:
            self.start_game_btn.setEnabled(True)
            self.display_message('Game is Over!')


    def display_message(self, text):
        mes = QMessageBox()
        mes.setFont(QFont("Century", 10))
        mes.setWindowTitle('Message')
        mes.setMinimumSize(QtCore.QSize(200, 100))
        mes.setText(text)
        mes.exec()
            




