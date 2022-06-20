import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class SimpleTweetWindow(QWidget):
    def __init__(self, api_connection):
        super().__init__()
        self.twitter_api = api_connection
        self.setWindowTitle("Simple Tweet")
        self.setGeometry(525, 150, 400, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        pass

    def layouts(self):
        pass
