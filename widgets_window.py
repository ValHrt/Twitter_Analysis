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
        self.filename = "NoImg"
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
        self.imgLabel = QLabel()
        self.selectImg = QPushButton("Select Image")
        self.selectImg.setHidden(True)
        self.selectImg.clicked.connect(self.uploadImage)
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
        self.bottomLayout.addRow(self.imgLabel, self.selectImg)
        self.bottomLayout.addRow(QLabel(), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def postTweet(self):
        text = self.tweetContent.toPlainText()
        if len(text) > 280:
            QMessageBox.information(self, "Info",
                                    "Your tweet contains too many characters!")
        elif len(text) == 0 and self.filename == "NoImg":
            QMessageBox.information(self, "Info",
                                    "Your tweet is empty")
        else:
            mbox = QMessageBox.Yes
            if self.imageCombo.currentText() == "Add Image" and self.filename == "NoImg":
                mbox = QMessageBox.question(self, "Warning", f"You haven't"
                                            f" upload an image! Post without"
                                            f" image?",
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
            if mbox == QMessageBox.Yes:
                self.twitter_api.simple_tweet(text, self.filename)
                QMessageBox.information(self, "Info",
                                        "Your tweet has been posted on Twitter 👍")
                self.close()

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
            self.selectImg.setHidden(True)
            self.imgLabel.clear()
            self.filename = "NoImg"
        else:
            self.selectImg.setHidden(False)

    def uploadImage(self):
        filename = QFileDialog.getOpenFileName(self, "Upload Image", "",
                                               "Image Files(*.jpg *.png *.jpeg)")
        if filename[0] != "":
            self.filename = filename[0]
            self.imgSelected = QPixmap(resource_path(self.filename))
            self.imgSelected = self.imgSelected.scaled(50, 50)
            self.imgLabel.setPixmap(self.imgSelected)
        else:
            self.filename = "NoImg"


class TweetBotWindow(QWidget):
    def __init__(self, api_connection):
        super().__init__()
        self.twitter_api = api_connection
        self.filename = "NoImg"
        self.setWindowTitle("Tweet Bot")
        self.setGeometry(525, 150, 400, 650)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        #################Top Layout Widgets#################
        self.titleText = QLabel("Tweet Bot")
        self.titleText.setAlignment(Qt.AlignCenter)
        self.tweetBotImg = QLabel()
        self.img = QPixmap(resource_path('icons/robot.png'))
        self.img = self.img.scaled(250, 250)
        self.tweetBotImg.setPixmap(self.img)
        self.tweetBotImg.setAlignment(Qt.AlignCenter)

        #################Bottom Layout Widgets#################
        self.comboChoice = QComboBox()
        choice_list = ["Tweet containing: ", "Tweet finishing by: "]
        self.comboChoice.addItems(choice_list)
        self.wordSearched = QLineEdit()
        self.wordSearched.setPlaceholderText("Enter your word here")
        self.numberOfTweets = QSpinBox()
        self.numberOfTweets.setRange(1, 20)
        self.answerBot = QLineEdit()
        self.answerBot.setPlaceholderText("Reply to tweets")
        self.imageCombo = QComboBox()
        self.imageCombo.addItems(["No Image", "Add Image"])
        self.imageCombo.currentIndexChanged.connect(self.generateImgBtn)
        self.imgLabel = QLabel()
        self.selectImg = QPushButton("Select Image")
        self.selectImg.setHidden(True)
        self.selectImg.clicked.connect(self.uploadImage)
        self.submitBtn = QPushButton("Launch Bot 🤖")
        self.submitBtn.clicked.connect(self.botTweet)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        #################Top Layout Widgets#################
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.tweetBotImg)
        self.topFrame.setLayout(self.topLayout)

        #################Bottom Layout Widgets#################
        self.bottomLayout.addRow(QLabel("Options: "), self.comboChoice)
        self.bottomLayout.addRow(QLabel("Searched word: "), self.wordSearched)
        self.bottomLayout.addRow(QLabel("Number of tweets: "),
                                 self.numberOfTweets)
        self.bottomLayout.addRow(QLabel("Your reply: "), self.answerBot)
        self.bottomLayout.addRow(QLabel(), self.imageCombo)
        self.bottomLayout.addRow(QLabel(), self.selectImg)
        self.bottomLayout.addRow(QLabel(), self.imgLabel)
        self.bottomLayout.addRow(self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def generateImgBtn(self):
        option_selected = self.imageCombo.currentText()
        if option_selected == "No Image":
            self.selectImg.setHidden(True)
            self.imgLabel.clear()
            self.filename = "NoImg"
        else:
            self.selectImg.setHidden(False)

    def uploadImage(self):
        filename = QFileDialog.getOpenFileName(self, "Upload Image", "",
                                               "Image Files(*.jpg *.png *.jpeg)")
        if filename[0] != "":
            self.filename = filename[0]
            self.imgSelected = QPixmap(resource_path(self.filename))
            self.imgSelected = self.imgSelected.scaled(50, 50)
            self.imgLabel.setAlignment(Qt.AlignCenter)
            self.imgLabel.setPixmap(self.imgSelected)
        else:
            self.filename = "NoImg"

    def botTweet(self):
        word_searched = self.wordSearched.text()
        reply_text = self.answerBot.text()
        if word_searched and reply_text != "":
            self.twitter_api.bot_tweet("Test", word_searched, 1, reply_text, "Test")
        else:
            QMessageBox.information(self, "Info", "Fields should not be empty")
