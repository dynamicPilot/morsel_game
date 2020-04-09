"""
Main script

"""
import sys

from start_menu import StartMenu
import config as conf

from PyQt5.QtWidgets import (QAction, qApp, QMainWindow, QMessageBox, QApplication)
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):

        # set players data global dict
        self.players = {'player1': {'color': 'blue', 'name': 'Player 1', 'score': 0}, 
        'player2': {'color': 'red', 'name': 'Player 2', 'score': 0}}
        
        # set central widget
        self.c_widget = StartMenu(self.players)
        self.setCentralWidget(self.c_widget)
        self.setStyleSheet("QMainWindow {background-image: url(icons/wooden_back0.png);}, QMainWindow QMessageBox {background-color: 'white';}")

        # set window params
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Morsel')
        self.setWindowIcon(QIcon(f'{conf.icons_folder_path}/blue_logo.png'))
        self.show()

    
    def closeEvent(self, event):
        mes = QMessageBox()
        reply = mes.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


