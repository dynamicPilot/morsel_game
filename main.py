"""
Main script

"""
import sys

from start_menu import StartMenu

from PyQt5.QtWidgets import (QAction, qApp, QMainWindow, QMessageBox, QApplication)
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):

        # set players data glodal dict
        self.players = {'player1': {'color': 'blue', 'name': 'Player 1'}, 
        'player2': {'color': 'red', 'name': 'Player 2'}}
        
        # set central widget
        self.c_widget = StartMenu(self.players)
        self.setCentralWidget(self.c_widget)
        self.setStyleSheet("background-color:white;")

        # set window params
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Carcassonne')
        self.show()

    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    #def show_history(self):
        #self.display_history_window = DisplayHistory(self.data_class)
        #self.display_history_window.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


