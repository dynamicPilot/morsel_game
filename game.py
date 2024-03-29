"""
QWidget Class for game method

"""
import random

import config as conf

from tail_preparing import TailsData
from drag_drop_labels import DragLabel, DropLabel, DragCharLabel
from game_over import GameOver

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog, QGridLayout, QSizePolicy, QApplication, QScrollArea, QMessageBox)
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QBrush

class NewGame(QWidget):
    def __init__(self, players):
        super().__init__()
        self.players = players
        self.initUI()
        
    def initUI(self):
        # set path variables
        self.path_to_icon = conf.icons_folder_path
        self.path_to_tail = conf.tail_folder_path
        self.notes = conf.notes

        #set window params
        self.setGeometry(25, 40, 1900, 1000)
        self.setWindowTitle('Morsel')
        self.setWindowIcon(QIcon(f'{self.path_to_icon}/blue_logo.png'))

        #self.showFullScreen()
        pixmap = QPixmap(f'{self.path_to_icon}/wooden_back0.png')
        pixmap = pixmap.scaled(self.size())
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)

        self.tails_data = TailsData()
        self.tails = self.tails_data.tails
        self.game_desk = None

        # set game flow control variables
        self.active_player = None # active player
        self.rest_player = None # passive player
        self.active_player_link_for_labels = [self.active_player]
        
        self.game_state = ['start'] # "start" "add new tail" "reset tail" "set tail" "reset char" "set char" "set tail and char" "end"

        self.active_tail = None
        self.active_desk_id = None
        self.active_char_id = None
        self.game_desk_id = None # game_grid row and col to Qlabel Drop widget

        self.cities = []
        self.roads = []
        self.monasteries = []
        self.active_tail_chains = None
        self.active_tail_available_monastery_chains = []
        self.active_tail_available_city_chains = []
        self.active_tail_available_road_chains = []

        self.opposite_side_dict = {"top": "bot", "bot": "top", "left": "right", "right": "left"}
        self.specials_list = ['monastery', 'city_mark', 'end_point']
        
        self.player1_char_list = [{'active': False, 'tail': None, 'widget': None, 'grid_id': None} for i in range(conf.chars_number)]
        self.player2_char_list = [{'active': False, 'tail': None, 'widget': None, 'grid_id': None} for i in range(conf.chars_number)]
        self.players_char_lists = {'player1': self.player1_char_list, 'player2': self.player2_char_list}
        self.char_list_id = None

        # set global style sheets for buttons
        self.add_tail_btn_style = ["QPushButton {background: transparent; border: none; color: '#f4f4f4'}", "QPushButton:pressed {background-color: #181e1a; border-radius: 2px; color: 'white'} QPushButton {background-color: #1b3522; border-radius: 2px; color: 'white'}", "QPushButton {background-color: '#f4f4f4'; border-radius: 2px; border-color: '#5b5c5b'; color: #777474}"]
        self.reset_tail_btn_style = ["QPushButton {background: transparent; border: none; color: '#f4f4f4'}", "QPushButton:pressed {background-color: #9f7224; border-radius: 2px; color: 'white'} QPushButton {background-color: #9f7224; border-radius: 2px; color: 'white'}"]
        self.set_tail_btn_style = ["QPushButton {background: transparent; border: none; color: '#f4f4f4'}", "QPushButton:pressed {background-color: #2f395a; border-radius: 2px; color: 'white'} QPushButton {background-color: #2f395a; border-radius: 2px; color: 'white'}"]

        v_layout = QVBoxLayout()


        header_label = QLabel('MORSEL', self, margin = 12)
        header_label.setStyleSheet("QLabel {background: transparent; border: none; color:'#f4ddc8'}")
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        header_label.setFont(QFont("Calisto MT", 32, QFont.Bold))
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

        h_box.addWidget(scroll_area)

        #h_box.addStretch(1)

        self.create_player_desk('player2')
        h_box.addWidget(self.players['player2']['desk'])

        v_layout.addLayout(h_box)
        v_layout.addStretch(1)

        btn_h_box = QHBoxLayout()
        self.player_1_notes_label = QLabel()
        note_text = self.notes[self.game_state[0]][0]
        self.player_1_notes_label.setText(note_text)
        self.player_1_notes_label.setFont(QFont("Century", 12, QFont.Bold))
        self.player_1_notes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.player_1_notes_label.setStyleSheet("background: transparent; color: '#f4ddc8';")
        self.player_1_notes_label.setMinimumSize(QtCore.QSize(conf.notes_label_width, conf.notes_label_height))
        self.player_1_notes_label.setMaximumSize(QtCore.QSize(conf.notes_label_width, conf.notes_label_height))
        btn_h_box.addWidget(self.player_1_notes_label)
        self.players['player1']['note_widget'] = self.player_1_notes_label

        btn_h_box.addStretch(1)

        start_end_button_style = "QPushButton:pressed {background-color: #958475; border-radius: 2px; color: '#f4ddc8'} QPushButton {background-color: #423b35; border-radius: 2px; color: '#f4ddc8'}"

        self.start_game_btn = QPushButton('Start Game', self)
        self.start_game_btn.setFont(QFont("Century", 15, QFont.Bold))
        self.start_game_btn.setStyleSheet(start_end_button_style)
        self.start_game_btn.setMinimumSize(QtCore.QSize(150, 50))
        btn_h_box.addWidget(self.start_game_btn)
        self.start_game_btn.clicked.connect(self.start_game)

        self.end_game_btn = QPushButton('End Game', self)
        self.end_game_btn.setFont(QFont("Century", 15, QFont.Bold))
        self.end_game_btn.setStyleSheet(start_end_button_style)
        self.end_game_btn.setMinimumSize(QtCore.QSize(150, 50))
        btn_h_box.addWidget(self.end_game_btn)
        self.end_game_btn.clicked.connect(self.close)
        #self.end_game_btn.clicked.connect(QtCore.QCoreApplication.quit)

        btn_h_box.addStretch(1)
        self.player_2_notes_label = QLabel()
        note_text = self.notes[self.game_state[0]][1]
        self.player_2_notes_label.setText(note_text)
        self.player_2_notes_label.setFont(QFont("Century", 12, QFont.Bold))
        self.player_2_notes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.player_2_notes_label.setStyleSheet("background: transparent; color:'#f4ddc8';")
        self.player_2_notes_label.setMinimumSize(QtCore.QSize(conf.notes_label_width, conf.notes_label_height))
        self.player_2_notes_label.setMaximumSize(QtCore.QSize(conf.notes_label_width, conf.notes_label_height))
        btn_h_box.addWidget(self.player_2_notes_label)
        self.players['player2']['note_widget'] = self.player_2_notes_label

        v_layout.addLayout(btn_h_box)

        self.setLayout(v_layout)

    def create_game_desk(self):
        self.game_desk = QWidget()
        self.game_desk.setProperty('class', 'desk')
        self.game_desk.setContentsMargins(5, 5, 5, 5)
        self.game_desk.setStyleSheet(".desk {background-color: white; border-style: outset; border-color:'#423b35'; border-width: 2px; border-radius: 5px;}")
        desk_width = conf.tail_size*conf.game_grid_width
        desk_height = conf.tail_size*conf.game_grid_height
        self.game_desk.setMinimumSize(QtCore.QSize(desk_width, desk_height))
        self.game_desk.setMaximumSize(QtCore.QSize(desk_width, desk_height))
        self.game_grid = [[{'widget': None, 'tail': None, 'player': None, 'active': False, 'transform': 0, 'char_side': None} for i in range(conf.game_grid_width)] for j in range(conf.game_grid_height)]

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
        self.active_tail = self.tails[0]
        self.active_desk_id = [conf.start_tail_position[0], conf.start_tail_position[0]]

        # set new chains
        self.set_active_tail_chains()
        self.erase_game_flow_control_variables()
        print(self.active_tail_available_city_chains, self.active_tail_available_monastery_chains, self.active_tail_available_road_chains)

        self.game_grid[conf.start_tail_position[0]][conf.start_tail_position[0]]['widget'].pix_state = "ready"
        self.game_desk.setLayout(grid)

    def create_tail_container(self, tail_size = conf.tail_size, is_drag = False):
        if not is_drag:
            tail_container_label = DropLabel(self, self.game_desk_id, self.game_grid, self.game_state)
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
        player_desk.setObjectName('player_desk')
        player_desk.setStyleSheet("QWidget#player_desk {background-color: '#f4f4f4'; border-style: outset; border-color:'#423b35'; border-width: 2px; border-radius: 5px;}")

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
        player_icon_pixmap = QPixmap(f'{self.path_to_icon}/{self.players[player_key]["color"]}_logo.png')
        player_icon_pixmap = player_icon_pixmap.scaledToHeight(70)
        player_icon_label.setPixmap(player_icon_pixmap)
        player_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        player_icon_label.adjustSize()
        v_box.addWidget(player_icon_label, alignment=QtCore.Qt.AlignCenter)

        score_label = QLabel('0', self, margin = 7)
        score_label.setAlignment(QtCore.Qt.AlignCenter)
        score_label.setStyleSheet("background-color:white; border-style: outset; border-color:'#302f2f'; border-width: 2px; border-radius: 5px;")
        score_label.setFont(QFont("Century", 12, QFont.Bold))
        score_label.setMinimumSize(QtCore.QSize(100, 50))
        score_label.setMaximumSize(QtCore.QSize(100, 50))
        v_box.addWidget(score_label, alignment=QtCore.Qt.AlignCenter)
        
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

        add_tail_btn.clicked.connect(self.add_new_tail_to_player)
        reset_tail_btn.clicked.connect(self.reset_new_tail_to_player)
        set_tail_btn.clicked.connect(self.set_new_tail_to_player)

        v_box.addStretch(1)

        grid = QGridLayout()
        grid.setSpacing(7)

        self.char_list_id = 0
        
        row_number = int(conf.chars_number/conf.char_grid_width)

        for col in range(conf.char_grid_width):
            for row in range(row_number):
                char_widget = self.create_char_pictures(player_key)
                self.players_char_lists[player_key][self.char_list_id]['widget'] = char_widget
                grid.addWidget(char_widget, row, col, QtCore.Qt.AlignCenter)
                self.char_list_id +=1

        char_widget = self.create_char_pictures(player_key)
        self.players_char_lists[player_key][self.char_list_id]['widget'] = char_widget
        grid.addWidget(char_widget, 3, 1, QtCore.Qt.AlignCenter)
        
        v_box.addLayout(grid)
        v_box.addStretch(1)

        skip_char_btn = QPushButton('Skip Character', self)
        skip_char_btn.setFont(QFont("Century", 10, QFont.Bold))
        skip_char_btn.setStyleSheet(self.add_tail_btn_style[0])
        skip_char_btn.setEnabled(False)
        skip_char_btn.setMinimumSize(QtCore.QSize(150, 50))
        v_box.addWidget(skip_char_btn, alignment=QtCore.Qt.AlignCenter)
        skip_char_btn.clicked.connect(self.skip_char_to_player)

        reset_char_btn = QPushButton('Reset Character', self)
        reset_char_btn.setFont(QFont("Century", 10, QFont.Bold))
        reset_char_btn.setStyleSheet(self.reset_tail_btn_style[0])
        reset_char_btn.setEnabled(False)
        reset_char_btn.setMinimumSize(QtCore.QSize(150, 50))
        v_box.addWidget(reset_char_btn, alignment=QtCore.Qt.AlignCenter)
        reset_char_btn.clicked.connect(self.reset_char_to_player)

        set_char_btn = QPushButton('Set Character', self)
        set_char_btn.setFont(QFont("Century", 10, QFont.Bold))
        set_char_btn.setStyleSheet(self.set_tail_btn_style[0])
        set_char_btn.setEnabled(False)
        set_char_btn.setMinimumSize(QtCore.QSize(150, 50))
        v_box.addWidget(set_char_btn, alignment=QtCore.Qt.AlignCenter)
        set_char_btn.clicked.connect(self.set_char_to_player)

        v_box.addStretch(1)

        player_desk.setLayout(v_box)
        
        # add widget to players dictionary
        self.players[player_key]['desk'] = player_desk
        self.players[player_key]['score_label'] = score_label
        self.players[player_key]['tail_widget'] = tail_widget
        self.players[player_key]['add_tail_btn'] = add_tail_btn
        self.players[player_key]['reset_tail_btn'] = reset_tail_btn
        self.players[player_key]['set_tail_btn'] = set_tail_btn
        self.players[player_key]['skip_char_btn'] = skip_char_btn
        self.players[player_key]['reset_char_btn'] = reset_char_btn
        self.players[player_key]['set_char_btn'] = set_char_btn

    def create_char_pictures(self, player_key):

        if player_key == 'player1':
            char_container_label = DragCharLabel(self, self.char_list_id, self.player1_char_list, self.game_state, player_key, self.active_player_link_for_labels)
        else:
            char_container_label = DragCharLabel(self, self.char_list_id, self.player2_char_list, self.game_state, player_key, self.active_player_link_for_labels)

        char_container_label.setAlignment(QtCore.Qt.AlignCenter)
        char_container_label.setMinimumSize(QtCore.QSize(conf.char_picture_size, conf.char_picture_size))
        char_container_label.setMaximumSize(QtCore.QSize(conf.char_picture_size, conf.char_picture_size))
        char_pixmap = QPixmap(f'{self.path_to_icon}/{self.players[player_key]["color"]}_men.png')
        char_pixmap = char_pixmap.scaledToHeight(conf.char_picture_size)
        char_container_label.setPixmap(char_pixmap)
        char_container_label.setAlignment(QtCore.Qt.AlignCenter)
        char_container_label.setStyleSheet("background-color: #ebebeb; border-style: outset; border-color: #5b5c5b; border-width: 1px; border-radius: 2px;")
        return char_container_label

    def start_game(self):
        self.tails = self.tails_data.tails
        self.tails = self.tails[1:]
        random.shuffle(self.tails)
        players_list = ['player1', 'player2']
        random.shuffle(players_list)
        self.active_player = players_list[0]
        self.rest_player = players_list[1]
        self.active_player_link_for_labels[0] = self.active_player
        self.game_state[0] = 'add new tail'

        self.make_player_button_visible()
        self.players[self.active_player]['reset_tail_btn'].setEnabled(False) #disable reset tail button
        self.players[self.active_player]['set_tail_btn'].setEnabled(False) #disable set tail button

        self.players[self.active_player]['note_widget'].setText(self.notes[self.game_state[0]][0])
        self.players[self.rest_player]['note_widget'].setText(self.notes[self.game_state[0]][1][random.randint(0, len(self.notes[self.game_state[0]][1])-1)])
        
        self.start_game_btn.setEnabled(False)

        for col in range(conf.game_grid_width):
            for row in range(conf.game_grid_height):
                if col != conf.start_tail_position[0] and row != conf.start_tail_position[0]:
                    self.game_grid[row][col]['transform'] = 0
                    self.game_grid[row][col]['tail'] = None
                    self.game_grid[row][col]['player'] = None
                    self.game_grid[row][col]['char'] = None
                    self.game_grid[row][col]['char_side'] = None
                    self.game_grid[row][col]['active'] = False
                    self.game_grid[row][col]['widget'].clear()

    def next_turn(self):

        #self.print_active_player_chars()
        self.make_active_player_chat_button_not_active()
        self.make_active_player_chat_button_not_visible()

        if len(self.tails) > 0:
            print("\n\n---NEW TURN--\n")

            print('chains:\n')
            print('monastery ', self.monasteries)
            print('city ', self.cities)
            print('road ', self.roads)

            self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['active'] = False

            if self.active_char_id is not None:
                self.players_char_lists[self.active_player][self.active_char_id]['active'] = False

            self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['widget'].pix_state = "ready"
            self.active_player, self.rest_player = self.rest_player, self.active_player
            self.active_player_link_for_labels[0] = self.active_player
            self.game_state[0] = 'add new tail'
            self.erase_game_flow_control_variables()
            self.make_player_button_visible()
            self.players[self.active_player]['reset_tail_btn'].setEnabled(False) # disable reset tail button
            self.players[self.active_player]['set_tail_btn'].setEnabled(False) # disable set tail button

            self.players[self.active_player]['note_widget'].setText(self.notes[self.game_state[0]][0])
            self.players[self.rest_player]['note_widget'].setText(self.notes[self.game_state[0]][1][random.randint(0, len(self.notes[self.game_state[0]][1])-1)])

            print('\nACTIVE PLAYER ', self.active_player)
        else:
            self.game_over_state()

    def game_over_state(self):
        self.game_state[0] = 'game over'
        self.start_game_btn.setEnabled(True)
        self.count_scores_and_finish_chains(True)
        self.players[self.active_player]['note_widget'].setText(self.notes[self.game_state[0]][0])
        self.players[self.rest_player]['note_widget'].setText(self.notes[self.game_state[0]][1])
        self.game_over_window = GameOver(self.players)
        self.game_over_window.show()
        self.close()

    def erase_game_flow_control_variables(self):
        self.active_desk_id = None
        self.active_char_id = None
        self.active_tail_available_city_chains = []
        self.active_tail_available_road_chains = []
        self.active_tail_available_monastery_chains = []
        self.active_tail_chains = None

    # make visible active player tail buttons
    def make_player_button_visible(self):
        """
        Make active player's tail control button visible and active and rest player's button not visible and not active.
        """
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

    def make_active_player_tail_button_not_active(self):
        self.players[self.active_player]['add_tail_btn'].setEnabled(False)
        self.players[self.active_player]['reset_tail_btn'].setEnabled(False)
        self.players[self.active_player]['set_tail_btn'].setEnabled(False)

    def make_active_player_tail_button_not_visible(self):
        self.players[self.active_player]['add_tail_btn'].setStyleSheet(self.add_tail_btn_style[0])
        self.players[self.active_player]['reset_tail_btn'].setStyleSheet(self.reset_tail_btn_style[0])
        self.players[self.active_player]['set_tail_btn'].setStyleSheet(self.set_tail_btn_style[0])

    def make_active_player_chat_button_not_active(self):
        self.players[self.active_player]['skip_char_btn'].setEnabled(False)
        self.players[self.active_player]['reset_char_btn'].setEnabled(False)
        self.players[self.active_player]['set_char_btn'].setEnabled(False)

    def make_active_player_chat_button_not_visible(self):
        self.players[self.active_player]['skip_char_btn'].setStyleSheet(self.add_tail_btn_style[0])
        self.players[self.active_player]['reset_char_btn'].setStyleSheet(self.reset_tail_btn_style[0])
        self.players[self.active_player]['set_char_btn'].setStyleSheet(self.set_tail_btn_style[0])

    # make visible active player character buttons
    def make_char_button_visible(self):
        """
        Make active player's character control button visible and active and rest player's button not visible and not active.
        """
        skip_char_active_button = self.players[self.active_player]['skip_char_btn']
        skip_char_active_button.setStyleSheet(self.add_tail_btn_style[1])
        skip_char_active_button.setEnabled(True)

        reset_char_active_button = self.players[self.active_player]['reset_char_btn']
        reset_char_active_button.setStyleSheet(self.reset_tail_btn_style[1])
        reset_char_active_button.setEnabled(True)

        set_char_active_button = self.players[self.active_player]['set_char_btn']
        set_char_active_button.setStyleSheet(self.set_tail_btn_style[1])
        set_char_active_button.setEnabled(True)

        skip_char_rest_button = self.players[self.rest_player]['skip_char_btn']
        skip_char_rest_button.setStyleSheet(self.add_tail_btn_style[0])
        skip_char_rest_button.setEnabled(False)

        reset_char_rest_button = self.players[self.rest_player]['reset_char_btn']
        reset_char_rest_button.setStyleSheet(self.reset_tail_btn_style[0])
        reset_char_rest_button.setEnabled(False)

        set_char_rest_button = self.players[self.rest_player]['set_char_btn']
        set_char_rest_button.setStyleSheet(self.set_tail_btn_style[0])
        set_char_rest_button.setEnabled(False)

    def add_new_tail_to_player(self):
        if len(self.tails) > 0 and self.game_state[0] == 'add new tail':
            tail = self.tails.pop(0)
            self.active_tail = tail
            print('\nACTIVE TAIL ', self.active_tail)
            print('------------------------------------\n')
            tail_name = tail['name']
            tail_widget = self.players[self.active_player]['tail_widget']
            self.set_tail_to_container(tail_widget, tail_name, conf.player_tail_size)
            self.game_state[0] = 'reset tail'
            self.players[self.active_player]['add_tail_btn'].setEnabled(False)
            self.players[self.active_player]['add_tail_btn'].setStyleSheet(self.add_tail_btn_style[2])

            self.players[self.active_player]['reset_tail_btn'].setEnabled(True) #enable reset tail button
            self.players[self.active_player]['set_tail_btn'].setEnabled(True) #enable set tail button

            self.players[self.active_player]['note_widget'].setText(self.notes[self.game_state[0]][0])
        elif len(self.tails) <= 0:
            self.game_over_state()
        else:
            return

    def reset_new_tail_to_player(self):

        if self.game_state[0] == 'reset tail':
            self.set_active_desk_id()
            if self.active_desk_id is not None:
                try:
                    self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['widget'].clear()
                    self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['widget'].pix_state = "empty"
                    self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['active'] = False
                    self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['transform'] = 0
                    self.set_original_tail_sides()
                except TypeError:
                    pass
             
            tail_widget = self.players[self.active_player]['tail_widget']
            print(self.active_tail['name'])
            tail_name = self.active_tail['name']
            self.set_tail_to_container(tail_widget, tail_name, conf.player_tail_size)
        else:
            return

    def set_new_tail_to_player(self):
        
        if self.game_state[0] == 'reset tail':

            # Set active desk widget
            self.set_active_desk_id()
            tail_check = self.check_tail_location()
            if tail_check:
                self.game_state[0] = 'set tail'
                self.set_active_tail_chains()
                #self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['active'] = False
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['tail'] = self.active_tail['number']
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['player'] = self.active_player
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['widget'].pix_state = "char"

                self.make_char_button_visible()
                self.make_active_player_tail_button_not_active()
                self.make_active_player_tail_button_not_visible()
                self.players[self.active_player]['note_widget'].setText(self.notes[self.game_state[0]][0])
            else:
                self.reset_new_tail_to_player()

    def skip_char_to_player(self):
        if self.game_state[0] == 'reset char':
            self.reset_char_to_player()
        self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['widget'].pix_state = "ready"
        self.game_state[0] = "set tail and char"
        self.count_scores_and_finish_chains()
        self.next_turn()
    
    def reset_char_to_player(self):
        if self.game_state[0] == 'set tail':
            self.game_state[0] = 'reset char'
        
        if self.game_state[0] == 'reset char':
            self.set_active_desk_id()
            self.set_active_char_id()
            try:
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['widget'].reset_char()
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['char_side'] = None

                char_widget = self.players_char_lists[self.active_player][self.active_char_id]['widget']
                char_pixmap = QPixmap(f'{self.path_to_icon}/{self.players[self.active_player]["color"]}_men.png')
                char_pixmap = char_pixmap.scaledToHeight(conf.char_picture_size)
                char_widget.setPixmap(char_pixmap)
                char_widget.setAlignment(QtCore.Qt.AlignCenter)
                self.players_char_lists[self.active_player][self.active_char_id]['active'] = False
            except TypeError:
                return

    def set_char_to_player(self):
        print('start set char')

        print('availiable chains:')
        print('monastery ', self.active_tail_available_monastery_chains)
        print('city ', self.active_tail_available_city_chains)
        print('road ', self.active_tail_available_road_chains)


        if self.game_state[0] == 'reset char' or self.game_state[0] == 'set tail':
            self.set_active_desk_id()
            self.set_active_char_id()

            char_check = self.check_char_location()
            print('checking results... ', char_check)
            if char_check:
                self.game_state[0] == 'set tail and char'
                self.set_active_char_to_available_chains()
                self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['widget'].pix_state = "ready"
                self.players_char_lists[self.active_player][self.active_char_id]['active'] = False
                self.count_scores_and_finish_chains()
                self.next_turn()
            else:
                self.reset_char_to_player()

    def set_active_desk_id(self):
        for col in range(conf.game_grid_width):
            for row in range(conf.game_grid_height):
                if self.game_grid[row][col]['active']:
                    self.active_desk_id = [row, col]
                    return

    def set_active_char_id(self):
        for char_id in range(len(self.players_char_lists[self.active_player])):
            if self.players_char_lists[self.active_player][char_id]['active'] == True:
                self.active_char_id = char_id
                return

    def get_tail_row_col(self, tail_number):
        """
        Return row, col in game_grid for tail with tail_number.
        """
        for col in range(conf.game_grid_width):
            for row in range(conf.game_grid_height):
                if self.game_grid[row][col]['tail'] == tail_number:
                    return row, col

    def get_tail_neighbors(self, row = None, col = None):
        """
        Return dictionary:
        neighbors = {'top': None, 'right': None, 'bot': None, 'left': None}

        with each neighbor:
        neighbor = {'char_side': None, 'player': None, 'specials': [], 'tail_number': None, 'row': row, 'col': col}
        """
        neighbors = {'top': None, 'right': None, 'bot': None, 'left': None}
        if row is None:
            row = self.active_desk_id[0]
        if col is None:
            col = self.active_desk_id[1]

        # neighbor tails check
        if row > 0:
            neighbor = self.create_neighbor_dictionary(row-1, col, "bot")
            neighbors["top"] = neighbor
        if row < conf.game_grid_height-1:
            neighbor = self.create_neighbor_dictionary(row+1, col, "top")
            neighbors["bot"] = neighbor
        if col > 0:
            neighbor = self.create_neighbor_dictionary(row, col-1, "right")
            neighbors["left"] = neighbor
        if col < conf.game_grid_width-1:
            neighbor = self.create_neighbor_dictionary(row, col+1, "left")
            neighbors["right"] = neighbor

        return neighbors

    def create_neighbor_dictionary(self, row, col, side):
        """
        Create dictionary for specific neighbor.
        Need:
        - neighbor row,
        - neighbor col,
        - tail side.

        Dictionary format:
        neighbor = {'char_side': None, 'player': None, 'tail_number': None, 'row': row, 'col': col}
        """
        neighbor = {'char_side': None, 'player': None, 'tail_number': None, 'row': row, 'col': col}
        tail_number = self.game_grid[row][col]['tail']
        if tail_number is None:
            return None

        neighbor['char_side'] = self.game_grid[row][col]['char_side']
        neighbor['player'] = self.game_grid[row][col]['player']
        neighbor['tail_number'] = tail_number
        
        return neighbor
   
    def check_tail_location(self):
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
                    return False
            else:
                none_sides += 1
        if row < conf.game_grid_height-1:
            if self.game_grid[row+1][col]['tail'] is not None:
                tail_number = self.game_grid[row+1][col]['tail']
                bot_neighbor_tail_edge = self.tails_data.tails[int(tail_number)]['top']
                if bot_neighbor_tail_edge != bot_tail_edge:
                    self.display_message("Bottom side is incorrect.")
                    return False
            else:
                none_sides += 1
        if col > 0:
            if self.game_grid[row][col-1]['tail'] is not None:
                tail_number = self.game_grid[row][col-1]['tail']
                left_neighbor_tail_edge = self.tails_data.tails[int(tail_number)]['right']
                if left_neighbor_tail_edge != left_tail_edge:
                    self.display_message("Left side is incorrect.")
                    return False
            else:
                none_sides += 1
        if col < conf.game_grid_width-1:
            if self.game_grid[row][col+1]['tail'] is not None:
                tail_number = self.game_grid[row][col+1]['tail']
                right_neighbor_tail_edge = self.tails_data.tails[int(tail_number)]['left']
                if right_neighbor_tail_edge != right_tail_edge:
                    self.display_message("Right side is incorrect.")
                    return False
            else:
                none_sides += 1
        
        if none_sides == 4:
            self.display_message("Your tail does not have got a neighbor.")     
            return False

        return True

    def check_char_location(self):
        char_side = self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['char_side']
        if char_side is None:
            self.display_message('No character to set.')
            return
            
        if char_side != 'center':
            char_side_name = self.active_tail[char_side] # active tail side letter
        else:
            if not self.active_tail['monastery']: # not monastery
                self.display_message('This tail is not a monastery.\nYou can not set your character on center.')
                return False
            elif len(self.active_tail_available_monastery_chains) == 0:
                self.display_message('No free monasteries.')
                return False
            else:
                return True

        if char_side_name == 'f':
            self.display_message('You can not set your character on field.')
            return False

        if char_side_name == 'c':
            if len(self.active_tail_available_city_chains) > 0:
                if not self.check_char_location_to_set_on_active_chains(char_side, char_side_name):
                    return False
                else:
                    return True
            else:
                self.display_message('No free cities.')
                return False

        if char_side_name == 'r':
            if len(self.active_tail_available_road_chains) > 0:
                if not self.check_char_location_to_set_on_active_chains(char_side, char_side_name):
                    return False
                else:
                    return True
            else:
                self.display_message('No free roads.')
                return False

        return True

    def check_char_location_to_set_on_active_chains(self, char_side, chain_type):

        self.filter_available_chains_to_char_side(char_side, chain_type)

        if chain_type == 'r':
            check_point = [char_side, self.active_tail['number']]
            for chain_index in range(len(self.roads)):
                chain = self.roads[chain_index]
                if check_point in chain['path'] and chain_index not in self.active_tail_available_road_chains:
                    self.display_message('This road is not free.')
                    return False
            return True

        if chain_type == 'c':
            check_point = [char_side, self.active_tail['number']]
            for chain_index in range(len(self.cities)):
                chain = self.cities[chain_index]
                if check_point in chain['path'] and chain_index not in self.active_tail_available_city_chains:
                    self.display_message('This city is not free.')
                    return False
            return True

    def filter_available_chains_to_char_side(self, char_side, chain_type):
        element_to_remove = []
        check_counter = 0
        if chain_type == 'r':
            check_points = [[char_side, self.active_tail['number']]]
            for road in self.active_tail['road']:
                if char_side in road:
                    print(road)
                    for another_char_side in road:
                        if another_char_side != char_side:
                            check_points.append([another_char_side, self.active_tail['number']])

            print('filter point to check ', check_points, ' in ', self.active_tail_available_road_chains)

            for chain_index in self.active_tail_available_road_chains:
                chain = self.roads[chain_index]
                for check_point in check_points:
                    if check_point in chain['tails']:
                        check_counter += 1
                if check_counter == 0:
                    element_to_remove.append(chain_index)

            for element in element_to_remove:
                self.active_tail_available_road_chains.remove(element)

        if chain_type == 'c':
            check_points = [[char_side, self.active_tail['number']]]
            for city in self.active_tail['city']:
                if char_side in city:
                    print(city)
                    for another_char_side in city:
                        if another_char_side != char_side:
                            check_points.append([another_char_side, self.active_tail['number']])

            print('filter point to check ', check_points, ' in ', self.active_tail_available_city_chains)

            for chain_index in self.active_tail_available_city_chains:
                chain = self.cities[chain_index]
                for check_point in check_points:
                    if check_point in chain['tails']:
                        check_counter += 1
                if check_counter == 0:
                    element_to_remove.append(chain_index)

            for element in element_to_remove:
                self.active_tail_available_city_chains.remove(element)

    def count_scores_and_finish_chains(self, final=False):
        self.check_road_chains_to_finish()
        self.check_monastery_chains_to_finish()
        self.check_city_chains_to_finish()

        if final:
            for chain in self.cities:
                if not chain['closed'] and chain['active']:
                    chain['score'] = int(chain['score']/2)
                    chain['finished'] = True
                    corner_sep_tail_sides = []
                    for point in chain['path']:
                        if self.tails_data.tails[point[1]]['corner_sep'] and (point[0] not in corner_sep_tail_sides):
                            corner_sep_tail_sides.append(point[0])
                    if len(corner_sep_tail_sides) % 2 == 0:
                        print('corner sep reduce score')
                        chain['score'] -= int(len(corner_sep_tail_sides)/ 2)
            for chain in self.roads:
                if not chain['closed'] and chain['active']:
                    chain['finished'] = True
            for chain in self.monasteries :
                if not chain['closed'] and chain['active']:
                    chain['finished'] = True

        for chain in self.roads:
            if chain['finished'] and not chain['closed']:
                if len(chain['player']) == 1:
                    self.players[chain['player'][0]]['score'] += chain['score']
                if len(chain['player']) > 1:
                    player1_count = 0
                    player2_count = 0

                    for char in chain['char_ids']:
                        if char[1] == 'player1':
                            player1_count += 1
                        else:
                            player2_count += 1
                    
                    if player1_count == player2_count:
                        print('two players on road ', chain)
                        self.players['player1']['score'] += chain['score']
                        self.players['player2']['score'] += chain['score']
                    elif player1_count > player2_count:
                        self.players['player1']['score'] += chain['score']
                    else:
                        self.players['player2']['score'] += chain['score']
                
                self.return_char_from_finish_chain(chain['char_ids'])
                chain['closed'] = True
        
        for chain in self.cities:
            if chain['finished'] and not chain['closed']:
                if len(chain['player']) == 1:
                    self.players[chain['player'][0]]['score'] += chain['score']
                    chain['closed'] = True
                if len(chain['player']) > 1:
                    player1_count = 0
                    player2_count = 0

                    for char in chain['char_ids']:
                        if char[1] == 'player1':
                            player1_count += 1
                        else:
                            player2_count += 1
                    
                    if player1_count == player2_count:
                        self.players['player1']['score'] += chain['score']
                        self.players['player2']['score'] += chain['score']
                    elif player1_count > player2_count:
                        self.players['player1']['score'] += chain['score']
                    else:
                        self.players['player2']['score'] += chain['score']
                
                self.return_char_from_finish_chain(chain['char_ids'])
                chain['closed'] = True

        for chain in self.monasteries:
            if chain['finished'] and not chain['closed']: 
                if len(chain['player']) >0:
                    self.players[chain['player'][0]]['score'] += chain['score']
                    self.return_char_from_finish_chain(chain['char_ids'])
                chain['closed'] = True

        self.players['player1']['score_label'].setText(str(int(self.players['player1']['score'])))
        self.players['player2']['score_label'].setText(str(int(self.players['player2']['score'])))

    def return_char_from_finish_chain(self, char_list):
        for char_item in char_list:
            char_player = char_item[1]
            char_id = char_item[0]
            grid_id = self.players_char_lists[char_player][char_id]['grid_id']

            self.game_grid[grid_id[0]][grid_id[1]]['widget'].reset_char()
            self.game_grid[grid_id[0]][grid_id[1]]['char_side'] = None
            char_widget = self.players_char_lists[char_player][char_id]['widget']
            char_pixmap = QPixmap(f'{self.path_to_icon}/{self.players[char_player]["color"]}_men.png')
            char_pixmap = char_pixmap.scaledToHeight(conf.char_picture_size)
            char_widget.setPixmap(char_pixmap)
            char_widget.setAlignment(QtCore.Qt.AlignCenter)
            self.players_char_lists[char_player][char_id]['active'] = False
            self.players_char_lists[char_player][char_id]['tail'] = None
            self.players_char_lists[char_player][char_id]['grid_id'] = []

            print('reset char for player ', char_player, ' and id ', char_id)

    def check_road_chains_to_finish(self):
        print('Start check road chains ... ')
        for chain in self.roads:
            if len(chain['end_points']) > 1 and not chain['finished']: #and chain['active']
                chain['finished'] = True
                chain['active'] = False
                print('Finish road chain ... ', chain)

            if len(chain['end_points']) == 0 and not chain['finished']: #and chain['active']
                # check circle chain without end points
                print('Start check roads for circle chains ... ')
                lost_points = [chain['path'][-1]]
                visited_points = []
                end_points = chain['path'][:-1]
                break_mark = False

                while len(lost_points) > 0 and not break_mark and len(end_points) > 0:
                    current_point = lost_points.pop()
                    visited_points.append(current_point)
                    current_point_number = current_point[1]
                    current_point_side = current_point[0]
                    print('visited ', visited_points, 'end_points ', end_points, 'lost points ', lost_points)
                    print(f'current point number is {current_point_number}, current point side is {current_point_side}. Tail road is ', self.tails_data.tails[current_point_number]['road'])

                    if current_point in end_points:
                        print('remove end point ', current_point)
                        end_points.remove(current_point)

                    if len(self.tails_data.tails[current_point_number]['road'][0]) > 1:
                        for side in self.tails_data.tails[current_point_number]['road'][0]:
                            if side != current_point_side:
                                can_be_add_point = [side, current_point_number]
                                if can_be_add_point not in visited_points and can_be_add_point not in lost_points:
                                    lost_points.append(can_be_add_point)
                                    print('add lost point ', can_be_add_point, ' to lost_points ', lost_points)
                        print('finish look at sides of current point')

                    row, col = self.get_tail_row_col(current_point_number)
                    n_tail = self.get_tail_neighbors(row, col)[current_point_side]

                    if n_tail is None:
                        print('no neighbor')
                        break_mark =  True
                    else:
                        print(n_tail)
                        can_be_add_point = [self.opposite_side_dict[current_point_side], n_tail['tail_number']]
                        print('can be add point ', can_be_add_point, 'end points', end_points)
                        if can_be_add_point not in visited_points:
                            lost_points.append(can_be_add_point)
                            print('add lost point after n_tail', can_be_add_point)

                    print('visited end', visited_points, 'end_points ', end_points, 'lost points ', lost_points)

                print('checking... lost_points ', lost_points, ' end_points ', end_points, ' break mark ', break_mark)
                if len(end_points) == 0 and len(lost_points) == 0 and not break_mark:
                    chain['finished'] = True
                    chain['active'] = False
                    print('Finish road chain ... ', chain)

    def check_monastery_chains_to_finish(self):
        print('check monasteries chains ')
        for chain in self.monasteries:
            if len(chain['tails']) == 8 and not chain['finished']: #and chain['active']
                chain['finished'] = True
                chain['active'] = False
                print('Finish monastery chain ', chain)

    def check_city_chains_to_finish(self):
        print('Start check city chains ... ')
        lost_points = []

        for chain in self.cities:

            if not chain['finished']: #chain['active'] and
                lost_points = [chain['path'][-1]]
                visited_points = []
                end_points = []
                for point in chain['path'][:-1]:
                    if point not in end_points:
                        end_points.append(point)
                break_mark = False

                while (len(lost_points) > 0 or len(end_points) > 0) and not break_mark:

                    current_point = lost_points.pop(0)
                    visited_points.append(current_point)
                    current_point_number = current_point[1]
                    current_point_side = current_point[0]
                    print('visited ', visited_points, 'end_points ', end_points, 'lost points ', lost_points)
                    print(f'current point number is {current_point_number}, current point side is {current_point_side}. Tail city is ', self.tails_data.tails[current_point_number]['city'])

                    if current_point in end_points:
                        print('remove end point ', current_point)
                        end_points.remove(current_point)

                    if len(self.tails_data.tails[current_point_number]['city'][0]) > 1:
                        for side in self.tails_data.tails[current_point_number]['city'][0]:
                            if side != current_point_side:
                                can_be_add_point = [side, current_point_number]
                                if can_be_add_point not in visited_points and can_be_add_point not in lost_points:
                                    lost_points.append(can_be_add_point)
                                    print('add lost point ', can_be_add_point, ' to lost_points ', lost_points)
                        print('finish look at sides of current point')

                    row, col = self.get_tail_row_col(current_point_number)
                    n_tail = self.get_tail_neighbors(row, col)[current_point_side]

                    if n_tail is None:
                        print('no neighbor')
                        break_mark =  True
                    else:
                        print(n_tail)
                        can_be_add_point = [self.opposite_side_dict[current_point_side], n_tail['tail_number']]
                        print('can be add point ', can_be_add_point)
                        if can_be_add_point not in visited_points:
                            lost_points.append(can_be_add_point)
                            print('add lost point after n_tail', can_be_add_point)

                    print('visited end', visited_points, 'end_points ', end_points, 'lost points ', lost_points)

                print('checking... lost_points ', lost_points, ' end_points ', end_points, ' break mark ', break_mark)
                if len(end_points) == 0 and len(lost_points) == 0 and not break_mark:
                    chain['finished'] = True
                    chain['active'] = False
                    corner_sep_tail_sides = []
                    for point in chain['path']:
                        if self.tails_data.tails[point[1]]['corner_sep'] and (point[0] not in corner_sep_tail_sides):
                            corner_sep_tail_sides.append(point[0])
                    if len(corner_sep_tail_sides) % 2 == 0:
                        print('corner sep reduce score')
                        chain['score'] -= (2*int(len(corner_sep_tail_sides) / 2))
                    print('Finish city chain ', chain)
        
    def set_active_char_to_available_chains(self):
        print('start set char final')

        print('availiable chains:')
        print('monastery ', self.active_tail_available_monastery_chains)
        print('city ', self.active_tail_available_city_chains)
        print('road ', self.active_tail_available_road_chains)
       
        char_side = self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['char_side']
        if char_side == 'center':
            print('set char to available chains, char side: ',  self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['char_side'])
            c_index = self.active_tail_available_monastery_chains[0]
            self.monasteries[c_index]['player'].append(self.active_player)
            self.monasteries[c_index]['char_ids'].append([self.active_char_id, self.active_player])
            self.monasteries[c_index]['active'] = True
            self.players_char_lists[self.active_player][self.active_char_id]['tail'] = self.active_tail['number']
            self.players_char_lists[self.active_player][self.active_char_id]['grid_id'] = self.active_desk_id
            print(f'Char id {self.active_char_id} of {self.active_player} set in monastery chain {self.monasteries[c_index]} and tail number {self.active_tail["number"]}.')
        elif self.active_tail[char_side] == 'r' and len(self.active_tail_available_road_chains) >0:
            print('set char to available chains, char side: ',  self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['char_side'], self.active_tail[self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['char_side']])
            c_index = self.active_tail_available_road_chains[0]
            self.roads[c_index]['player'].append(self.active_player)
            self.roads[c_index]['char_ids'].append([self.active_char_id, self.active_player])
            self.roads[c_index]['active'] = True
            self.players_char_lists[self.active_player][self.active_char_id]['tail'] = self.active_tail['number']
            self.players_char_lists[self.active_player][self.active_char_id]['grid_id'] = self.active_desk_id
            print(f'Char id {self.active_char_id} of {self.active_player} set in road chain {self.roads[c_index]} and tail number {self.active_tail["number"]}.')
        elif self.active_tail[char_side] == 'c' and len(self.active_tail_available_city_chains) >0:
            print('set char to available chains, char side: ',  self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['char_side'], self.active_tail[self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['char_side']])
            c_index = self.active_tail_available_city_chains[0]
            self.cities[c_index]['player'].append(self.active_player)
            self.cities[c_index]['char_ids'].append([self.active_char_id, self.active_player])
            self.cities[c_index]['active'] = True
            self.players_char_lists[self.active_player][self.active_char_id]['tail'] = self.active_tail['number']
            self.players_char_lists[self.active_player][self.active_char_id]['grid_id'] = self.active_desk_id
            print(f'Char id {self.active_char_id} of {self.active_player} set in city chain {self.cities[c_index]} and tail number {self.active_tail["number"]}.')
        else:
            print('Player char is NOT SET.')
            return

    def set_active_tail_chains(self):
        self.active_tail_chains = []
        sides = ['top', 'right', 'bot', 'left']
        tail_key_to_check = ['city', 'road']

        # set city and road if False
        for key in tail_key_to_check:
            if not self.active_tail[key]:
                self.active_tail[key] = []
                for side in sides:
                    if self.active_tail[side] == key[0]:
                        self.active_tail[key].append([side])
            else:
                self.active_tail[key] = [self.active_tail[key]]
        
        print(self.active_tail)

        # set monastery chain
        if self.active_tail['monastery']:
            chain = ['m', self.active_tail['number'], []]
            self.active_tail_chains.append(chain)

        # set city chains
        for key in tail_key_to_check:
            if self.active_tail[key] != False and len(self.active_tail[key])>0:
                for chain_item in self.active_tail[key]:
                    print(key, key[0], chain_item)
                    chain = [key[0], [chain_item[0], self.active_tail['number']]]
                    if len(chain_item) == 1:
                        chain.append([chain_item[0], self.active_tail['number']])
                    else:
                        for item in chain_item[1:]:
                            chain.append([item, self.active_tail['number']])
                    if key == 'road':
                        if self.active_tail['end_point']:
                            chain.append(['end_point', self.active_tail['number']])
                    self.active_tail_chains.append(chain)

        print(self.active_tail_chains)
        self.join_active_taile_chains_to_chains()

    def join_active_taile_chains_to_chains(self):
        n_tails = self.get_tail_neighbors()
        
        for new_chain in self.active_tail_chains:
            chain_type = new_chain[0]
            if chain_type == 'm':
                self.create_new_monastery_chain(new_chain, n_tails)
            else:
                self.join_city_road_chain(new_chain, n_tails, chain_type)
                
        self.check_tail_for_current_monasteries_chains(self.active_tail['number'], n_tails)

    def check_tail_for_current_monasteries_chains(self, tail_number, n_tails):
        sides = ['top', 'right', 'bot', 'left']
        visited_chains = []

        for side in sides:
            n_tail = n_tails[side]
            if n_tail is not None:
                n_tail_number = n_tail['tail_number']
                for chain_index in range(len(self.monasteries)):
                    if chain_index not in visited_chains:
                        chain = self.monasteries[chain_index]
                        if chain['head'] == n_tail_number and chain['head'] != tail_number: # neighbor is a monastery
                            chain['tails'].append([side, tail_number])
                            chain['score'] += 1
                            visited_chains.append(chain_index)
                            print('set tail for current monasteries chains ', self.monasteries[chain_index]['tails'])                
                        for tail in chain['tails']: # neighbor is a monastery neighbor
                            if tail[1] == n_tail_number and tail[0]!= 'cross' and tail[0] != side and chain['head'] != tail_number:
                                chain['tails'].append(['cross', tail_number])
                                chain['score'] += 1
                                visited_chains.append(chain_index)
                                print('set tail for current monasteries chains ', self.monasteries[chain_index]['tails'])

        print('monasteries chain list')
        for item in self.monasteries:
            print(item)     
   
    def create_new_monastery_chain(self, new_chain, n_tails):
        sides = ['top', 'right', 'bot', 'left']
        row_col_to_check_additor = [[-1, 1], [1, 1], [1, -1], [-1, -1]]

        for side_index in range(len(sides)):
            side = sides[side_index]
            n_tail = n_tails[side]
            if n_tail is not None:
                n_tail_number = n_tail['tail_number']
                new_chain[2].append([self.opposite_side_dict[side], n_tail['tail_number']]) # add neighbor

            check_side = sides[side_index - 1] # check n_tail neighbor
            check_row = self.active_desk_id[0] + row_col_to_check_additor[side_index][0]
            check_col = self.active_desk_id[1] + row_col_to_check_additor[side_index][1]
            if check_row >= 0 and check_col >= 0 and check_row < conf.game_grid_height and check_col < conf.game_grid_width:
                n_tail_neighbor_to_check = self.create_neighbor_dictionary(check_row, check_col, check_side)
                if n_tail_neighbor_to_check is not None:
                    new_chain[2].append(['cross', n_tail_neighbor_to_check['tail_number']]) # add cross-neighbor
        
        print('create new chain...')
        chain_to_add = {'head': new_chain[1], 'active': False, 'player': [], 'score': len(new_chain[2]) + 1, 'finished': False, 'tails': new_chain[2], 'char_ids':[], 'closed': False}
        self.monasteries.append(chain_to_add)
        self.active_tail_available_monastery_chains.append(len(self.monasteries)-1)

        print('new monastery chain is ...', chain_to_add)

    def join_city_road_chain(self, new_chain, n_tails, chain_type):
        self.visited_sides = []
        without_neghbors = None
       
        for new_chain_point in new_chain[1:]:
            print('check point ', new_chain_point)
            new_chain_point_side = new_chain_point[0]
            if new_chain_point_side not in self.visited_sides and new_chain_point[0] != "end_point":
                self.visited_sides.append(new_chain_point_side)
                n_tail = n_tails[new_chain_point_side] # find a neighbor in this side

                if n_tail is None: # if neighbor does not exist
                    if without_neghbors is None:
                        without_neghbors = True
                else: # if neighbor exists
                    print('neighbor ', n_tail)
                    without_neghbors = False
                    n_tail_number = n_tail['tail_number']
                    print('calling function with ', n_tail_number, new_chain_point_side, chain_type)
                    chain_index, point_index = self.find_first_chain_index_point_index(n_tail_number, new_chain_point_side, chain_type)
                    except_point = new_chain_point
                    points_to_check = self.replace_point_except_point(chain_index, point_index, new_chain[1:], except_point, chain_type)
                    print('point to another check..', points_to_check)
                        
                    for check_point in points_to_check:
                        check_point_side = check_point[0]
                        if check_point_side not in self.visited_sides and check_point_side != "end_point":
                            print('check another point ', check_point_side)
                            self.visited_sides.append(check_point_side)
                            n_tail = n_tails[check_point_side]
                            print('neighbor, ', n_tail)
                            if n_tail is not None:
                                n_tail_number = n_tail['tail_number']
                                n_chain_index, n_point_index = self.find_first_chain_index_point_index(n_tail_number, check_point_side, chain_type)
                                n_except_point = [self.opposite_side_dict[check_point_side], n_tail_number]
                                self.add_neighbor_chain_to_chain(n_chain_index, chain_index, point_index, n_except_point, chain_type)
                        point_index += 1

        if without_neghbors:
            print('create new chain...')
            if chain_type == 'c':
                chain_to_add = {'path': [new_chain[1], new_chain[2]], 'active': False, 'player': [], 'score': 2, 'finished': False, 'char_ids': [], 'closed': False, 'tails': [new_chain[1]]}
                if len(new_chain)>3:
                    chain_to_add['path'].append(new_chain[3])
                if new_chain[2] not in chain_to_add['tails']:
                    chain_to_add['tails'].append(new_chain[2])
                if self.active_tail['city_mark']:
                    chain_to_add['score'] += 2
                self.cities.append(chain_to_add)
                self.active_tail_available_city_chains.append(len(self.cities)-1)
                print('new city chain is ...', chain_to_add)
            if chain_type == 'r':
                chain_to_add = {'path': [new_chain[1], new_chain[2]], 'active': False, 'player': [], 'score': 1, 'finished': False, 'char_ids': [], 'end_points': [], 'closed': False, 'tails': [new_chain[1]]}
                if new_chain[2] not in chain_to_add['tails']:
                    chain_to_add['tails'].append(new_chain[2])
                if self.active_tail['end_point']:
                    chain_to_add['end_points'].append(new_chain[3])
                self.roads.append(chain_to_add)
                self.active_tail_available_road_chains.append(len(self.roads)-1)
                print('new road chain is ...', chain_to_add)

        print('cities chain list')
        for item in self.cities:
            print(item)

        print('roads chain list')
        for item in self.roads:
            print(item)

    def find_first_chain_index_point_index(self, n_tail_number, new_chain_side_name, chain_type):
        if chain_type == 'c':
            for chain_index in range(len(self.cities)): # every chain
                for point_index in range(len(self.cities[chain_index]['path'])): # every point in chain
                    if self.cities[chain_index]['path'][point_index] == [self.opposite_side_dict[new_chain_side_name], n_tail_number]:
                        print('first chain index of n tail number ', n_tail_number, ' in ', self.cities, '..... for new chain side....', new_chain_side_name, ' is ', [chain_index, point_index])
                        return [chain_index, point_index]
        
        if chain_type == 'r':
            for chain_index in range(len(self.roads)): # every chain
                for point_index in range(len(self.roads[chain_index]['path'])): # every point in chain
                    if self.roads[chain_index]['path'][point_index] == [self.opposite_side_dict[new_chain_side_name], n_tail_number]:
                        print('first chain index of n tail number ', n_tail_number, ' in ', self.roads, '..... for new chain side....', new_chain_side_name, ' is ', [chain_index, point_index])
                        return [chain_index, point_index]

    def replace_point_except_point(self, c_index, p_index, point_list_to_add, except_point, chain_type):
        if chain_type == 'c':
            print('replace_point_except_point_city before', self.cities[c_index]['path'])
            result_list = self.cities[c_index]['path'][:p_index]
            return_list = []
            first = False

            for point in point_list_to_add:
                if point != except_point or first:
                    if point not in result_list:
                        result_list.append(point)
                        return_list.append(point)
                if point == except_point:
                    first = True

            result_list.extend(self.cities[c_index]['path'][p_index+1:])
            self.cities[c_index]['path'] = result_list
            for point in result_list:
                if point not in self.cities[c_index]['tails']:
                    self.cities[c_index]['tails'].append(point)
            if except_point not in self.cities[c_index]['tails']:
                self.cities[c_index]['tails'].append(except_point)
            self.cities[c_index]['score'] += 2
            if self.active_tail['city_mark']:
                self.cities[c_index]['score'] += 2
            if not self.cities[c_index]['active'] and c_index not in self.active_tail_available_city_chains and self.cities[c_index]['path'] != [['top', 0], ['top', 0]] and not self.cities[c_index]['finished']:
                self.active_tail_available_city_chains.append(c_index)
            print('replace_point_except_point_city after', self.cities[c_index]['path'])

        if chain_type == 'r':
            print('replace_point_except_point_road before', self.roads[c_index]['path'])
            result_list = self.roads[c_index]['path'][:p_index]
            return_list = []
            end_point = None
            first = False

            for point in point_list_to_add:
                if (point != except_point or first) and point[0] != 'end_point':
                    result_list.append(point)
                    return_list.append(point)
                if point == except_point:
                    first = True
                if point[0] == 'end_point':
                    end_point = point
                    print('find end point ', end_point)

            result_list.extend(self.roads[c_index]['path'][p_index+1:])
            self.roads[c_index]['path'] = result_list
            for point in result_list:
                if point not in self.roads[c_index]['tails']:
                    self.roads[c_index]['tails'].append(point)
            if except_point not in self.roads[c_index]['tails']:
                self.roads[c_index]['tails'].append(except_point)
            if end_point is not None:
                self.roads[c_index]['end_points'].append(end_point)
            self.roads[c_index]['score'] += 1
            if not self.roads[c_index]['active'] and c_index not in self.active_tail_available_road_chains and not self.roads[c_index]['finished']:
                self.active_tail_available_road_chains.append(c_index)
            print('replace_point_except_point_road after', self.roads[c_index]['path'])

        return return_list

    def add_neighbor_chain_to_chain(self, n_c_index, c_index, p_index, n_except_point, chain_type):
        #print(n_c_index,' neighbor chain ', self.cities[n_c_index], 'n excepr point ', n_except_point)
        #print('self chain ', self.cities[c_index])
        first = False

        if chain_type == 'c':
            print('\n\nneighbor chain ', self.cities[n_c_index], 'n excepr point ', n_except_point, ' n index ', n_c_index)
            print('self chain ', self.cities[c_index], ' self index ', c_index)
            result_list = self.cities[c_index]['path'][:p_index]
            for point in self.cities[n_c_index]['path']:
                if point != n_except_point or first:
                    if point not in result_list:
                        result_list.append(point)
                if point == n_except_point:
                    first = True

            result_list.extend(self.cities[c_index]['path'][p_index+1:])
            self.cities[c_index]['path'] = result_list

            if self.cities[n_c_index]['active']:
                self.cities[c_index]['active'] = True

            not_double_score = 0

            for n_tail in self.cities[n_c_index]['tails']:
                if n_tail not in self.cities[c_index]['tails']:
                    self.cities[c_index]['tails'].append(n_tail)
            if n_except_point not in self.cities[c_index]['tails']:
                self.cities[c_index]['tails'].append(n_except_point)
            for n_player in self.cities[n_c_index]['player']:
                if n_player not in self.cities[c_index]['player']:
                    self.cities[c_index]['player'].append(n_player)
            for n_char in self.cities[n_c_index]['char_ids']:
                if n_char not in self.cities[c_index]['char_ids']:
                    self.cities[c_index]['char_ids'].append(n_char)
                else:
                    not_double_score += 1
            if not_double_score == 0:
                self.cities[c_index]['score'] += self.cities[n_c_index]['score']

            print('add_neighbor_chain_to_chain_city', self.cities[c_index]['path'])

            if n_c_index != c_index:
                self.cities = self.cities[:n_c_index] + self.cities[n_c_index+1:]
                if c_index > n_c_index and c_index in self.active_tail_available_city_chains:
                    self.active_tail_available_city_chains.remove(c_index)
                    self.active_tail_available_city_chains.append(c_index-1)
                print('remove ', c_index, ' append ', c_index - 1, ' in ', self.active_tail_available_city_chains, ' for ', self.cities[c_index-1]['path'])

        if chain_type == 'r':
            print('\n\nneighbor chain ', self.roads[n_c_index], 'n excepr point ', n_except_point, ' n index ', n_c_index)
            print('self chain ', self.roads[c_index], ' self index ', c_index)
            result_list = self.roads[c_index]['path'][:p_index]
            for point in self.roads[n_c_index]['path']:
                if point != n_except_point or first:
                    result_list.append(point)
                if point == n_except_point:
                    first = True

            result_list.extend(self.roads[c_index]['path'][p_index+1:])
            self.roads[c_index]['path'] = result_list

            if self.roads[n_c_index]['active']:
                self.roads[c_index]['active'] = True

            print('add_neighbor_chain_to_chain_road', self.roads[c_index]['path'], c_index)
            not_double_score = 0

            for n_tail in self.roads[n_c_index]['tails']:
                if n_tail not in self.roads[c_index]['tails']:
                    self.roads[c_index]['tails'].append(n_tail)
            if n_except_point not in self.roads[c_index]['tails']:
                self.roads[c_index]['tails'].append(n_except_point)
            for n_player in self.roads[n_c_index]['player']:
                if n_player not in self.roads[c_index]['player']:
                    self.roads[c_index]['player'].append(n_player)
            for n_char in self.roads[n_c_index]['char_ids']:
                if n_char not in self.roads[c_index]['char_ids']:
                    self.roads[c_index]['char_ids'].append(n_char)
                else:
                    not_double_score += 1
            self.roads[c_index]['end_points'].extend(self.roads[n_c_index]['end_points'])
            if not_double_score == 0:
                print(self.roads[c_index]['score'], self.roads[n_c_index]['score'])
                self.roads[c_index]['score'] += self.roads[n_c_index]['score']

            print('add_neighbor_chain_to_chain_road', self.roads[c_index]['path'])


            if n_c_index != c_index:
                self.roads = self.roads[:n_c_index] + self.roads[n_c_index+1:]
                if c_index > n_c_index and c_index in self.active_tail_available_road_chains:
                    self.active_tail_available_road_chains.remove(c_index)
                    self.active_tail_available_road_chains.append(c_index-1)
                print('remove ', c_index, ' append ', c_index - 1, ' in ', self.active_tail_available_road_chains, ' for ', self.roads[c_index-1]['path'])

    def transform_tail_sides(self):
        rotation_dict = {'top': 'right', 'right': 'bot', 'bot': 'left', 'left': 'top'}
        rotate_number = self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['transform'] % 4

        print(' before rotating....', self.active_tail, 'transformation number is ', rotate_number)

        while (rotate_number > 0):

            top_tail_edge = self.active_tail['top']
            self.active_tail['top'] = self.active_tail['left']
            self.active_tail['left'] = self.active_tail['bot']
            self.active_tail['bot'] = self.active_tail['right']
            self.active_tail['right'] = top_tail_edge

            for key in ['city', 'road']:
                if self.active_tail[key] != False:
                    for i in range(len(self.active_tail[key])):
                        self.active_tail[key][i] = rotation_dict[self.active_tail[key][i]]

            rotate_number-=1

        self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['transform'] = 0
        print('after rotating....', self.active_tail)
        print('after rotating.... original ', self.tails_data.tails[int(self.active_tail['number'])])

    def set_original_tail_sides(self):
        """
        Reset tail sides to original values.
        """
        print('active tail before set original ', self.active_tail, 'transformation number for current grid cell ', self.game_grid[self.active_desk_id[0]][self.active_desk_id[1]]['transform'])
        original_image_name = self.active_tail['name']
        print('file ', original_image_name)
        self.active_tail['top'] = original_image_name[3]
        self.active_tail['right'] = original_image_name[5]
        self.active_tail['bot'] = original_image_name[7]
        self.active_tail['left'] = original_image_name[9]
        print('active tail after set original ', self.active_tail)

    def display_message(self, text):
        mes = QMessageBox()
        mes.setFont(QFont("Century", 10))
        mes.setWindowTitle('Message')
        mes.setMinimumSize(QtCore.QSize(200, 100))
        pixmap = QPixmap(f'{self.path_to_icon}/warning.png')
        pixmap = pixmap.scaledToHeight(70)
        mes.setIconPixmap(pixmap)
        mes.setText(text)
        mes.exec()

    def print_active_player_chars(self):
        print('printing chars...')
        for char in self.players_char_lists[self.active_player]:
            if char['active'] and char['tail'] is None:
                char_widget = self.players_char_lists[self.active_player][char_id]['widget']
                char_pixmap = QPixmap(f'{self.path_to_icon}/{self.players[self.active_player]["color"]}_men.png')
                char_pixmap = char_pixmap.scaledToHeight(conf.char_picture_size)
                char_widget.setPixmap(char_pixmap)
                char_widget.setAlignment(QtCore.Qt.AlignCenter)
                self.players_char_lists[self.active_player][char_id]['active'] = False
                self.players_char_lists[self.active_player][char_id]['tail'] = None
                self.players_char_lists[self.active_player][char_id]['grid_id'] = []

                print('reset char for player ', self.active_player, ' and id ', char_id)
            print(char)
        
        print('END')