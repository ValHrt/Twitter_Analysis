import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


# For compiling with PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class SimpleTweetWindow(QWidget):
    def __init__(self, api_connection):
        super().__init__()
        self.twitter_api = api_connection
        self.setWindowTitle("Simple Tweet")
        self.setGeometry(525, 150, 400, 650)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        #################Top Layout Widgets#################
        self.titleText = QLabel("Simple Tweet")
        self.titleText.setAlignment(Qt.AlignCenter)
        self.simpleTweetImg = QLabel()
        self.img = QPixmap(resource_path('icons/plume.png'))
        self.img = self.img.scaled(250, 250)
        self.simpleTweetImg.setPixmap(self.img)
        self.simpleTweetImg.setAlignment(Qt.AlignCenter)

        #################Bottom Layout Widgets#################
        self.tweetContent = QTextEdit()
        self.tweetContent.textChanged.connect(self.txtInputChanged)
        self.tweetLenghtLabel = QLabel("0/280 characters")
        self.imageCombo = QComboBox()
        self.imageCombo.addItems(["No Image", "Add Image"])
        self.imageCombo.currentIndexChanged.connect(self.generateImgBtn)
        self.selectImg = QPushButton("Select Image")
        self.submitBtn = QPushButton("Post Tweet")
        self.submitBtn.clicked.connect(self.postTweet)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        #################Top Layout Widgets#################
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.simpleTweetImg)
        self.topFrame.setLayout(self.topLayout)

        #################Bottom Layout Widgets#################
        self.bottomLayout.addRow(QLabel("Tweet: "), self.tweetContent)
        self.bottomLayout.addRow(QLabel(), self.tweetLenghtLabel)
        self.bottomLayout.addRow(QLabel(), self.imageCombo)
        self.bottomLayout.addRow(QLabel(), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def postTweet(self):
        text = self.tweetContent.toPlainText()
        print(text)
        self.tweetContent.clear()

    def txtInputChanged(self):
        len_tweet = len(self.tweetContent.toPlainText())
        self.tweetLenghtLabel.setText(f"{len_tweet}/280 characters")
        if len_tweet > 280:
            self.tweetLenghtLabel.setStyleSheet("color: red")
        else:
            self.tweetLenghtLabel.setStyleSheet("color: green")

    def generateImgBtn(self):
        option_selected = self.imageCombo.currentText()
        if option_selected == "No Image":
            self.bottomLayout.addRow(QLabel(), self.submitBtn)
        else:
            self.bottomLayout.addRow(QLabel(), self.selectImg)
            self.bottomLayout.addRow(QLabel(), self.submitBtn)

        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)
