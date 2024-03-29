import sys, os, csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import style


# For compiling with PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class SimpleTweetWindow(QWidget):
    def __init__(self, api_connection, is_reply, tweet_id=None,
                 tweet_name=None, tweet_text=None):
        super().__init__()
        self.twitter_api = api_connection
        self.reply = is_reply
        self.tweet_id = tweet_id
        self.tweet_text = tweet_text
        self.tweet_name = tweet_name
        self.filename = "NoImg"
        if not self.reply:
            self.setWindowTitle("Simple Tweet")
        else:
            self.setWindowTitle(f"Reply to @{tweet_name}")
        self.setGeometry(525, 150, 400, 650)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        #################Top Layout Widgets#################
        if not self.reply:
            self.titleText = QLabel("Simple Tweet")
            self.titleText.setStyleSheet(style.TitleLabelWindow())
            self.simpleTweetImg = QLabel()
            self.img = QPixmap(resource_path('icons/plume.png'))
            self.img = self.img.scaled(250, 250)
            self.simpleTweetImg.setPixmap(self.img)
        else:
            self.titleText = QLabel("Tweet: ")
            self.simpleTweetImg = QLabel(self.tweet_text)
            self.simpleTweetImg.setWordWrap(True)

        self.titleText.setAlignment(Qt.AlignCenter)
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
        self.submitBtn.setStyleSheet(style.SubmitButton())
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
                if not self.reply:
                    self.twitter_api.simple_tweet(text, self.filename)
                    QMessageBox.information(self, "Info",
                                            "Your tweet has been posted on Twitter 👍")
                else:
                    self.twitter_api.reply_tweet(self.tweet_id, text,
                                                 self.filename)
                    QMessageBox.information(self, "Info",
                                            f"You have replied to @{self.tweet_name}")
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
        self.titleText.setStyleSheet(style.TitleLabelWindow())
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
        self.submitBtn.setStyleSheet(style.SubmitButton())
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
        option = self.comboChoice.currentText()
        word_searched = self.wordSearched.text()
        reply_text = self.answerBot.text()
        nb_tweets = self.numberOfTweets.value()
        if word_searched != "":
            if reply_text != "" or self.filename != "NoImg":
                mbox = QMessageBox.Yes
                if self.imageCombo.currentText() == "Add Image" and self.filename == "NoImg":
                    mbox = QMessageBox.question(self, "Warning", f"You haven't"
                                                f" upload an image! Post without"
                                                f" image?",
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
                if mbox == QMessageBox.Yes:
                    answers_count = self.twitter_api.bot_tweet(option, word_searched,
                                                               nb_tweets, reply_text,
                                                               self.filename)
                    if answers_count > 1:
                        QMessageBox.information(self, "Info", f"Bot answered to"
                        f" {answers_count} tweets")
                        self.close()
                    elif answers_count == 1:
                        QMessageBox.information(self, "Info", f"Bot answered to"
                        f" {answers_count} tweet")
                        self.close()
                    else:
                        QMessageBox.information(self, "Info", f"No matching tweet"
                        f", please try again!")
            else:
                QMessageBox.information(self, "Info", f"You must insert text or"
                                        f" select an image")
        else:
            QMessageBox.information(self, "Info", "Fields should not be empty")


class AuthWindow(QWidget):
    def __init__(self, existing_directory: bool, api_connection,
                 credentials=None):
        super().__init__()
        self.existing_dir = existing_directory
        self.twitter_api = api_connection
        if self.existing_dir:
            self.credentials = credentials
        self.setWindowTitle("Authentification")
        self.setGeometry(325, 250, 800, 400)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.consumerKeyEntry = QLineEdit()
        self.consumerSecretEntry = QLineEdit()
        self.tokenKeyEntry = QLineEdit()
        self.tokenSecretEntry = QLineEdit()
        if self.existing_dir:
            self.consumerKeyEntry.setText(self.credentials[0])
            self.consumerSecretEntry.setText(self.credentials[1])
            self.tokenKeyEntry.setText(self.credentials[2])
            self.tokenSecretEntry.setText(self.credentials[3])
        self.testBtn = QPushButton("Connection Test")
        self.testBtn.clicked.connect(self.testCredentials)
        self.saveBtn = QPushButton("Save")
        self.saveBtn.clicked.connect(self.saveCredentials)
        self.infoTxt = QLabel("You must have a dev account with read and write"
                              " permissions if you want to have access to all"
                              " functionnalities from this app (Tweet Bot,"
                              " Simple Tweet,...)")
        self.infoTxt.setAlignment(Qt.AlignCenter)
        self.infoTxt.setWordWrap(True)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.authFormLayout = QFormLayout()
        self.authFrame = QFrame()

        self.authFormLayout.addRow(QLabel("Consumer Key: "),
                                   self.consumerKeyEntry)
        self.authFormLayout.addRow(QLabel(), QLabel())
        self.authFormLayout.addRow(QLabel("Consumer Secret: "),
                                   self.consumerSecretEntry)
        self.authFormLayout.addRow(QLabel(), QLabel())
        self.authFormLayout.addRow(QLabel("Token Key: "),
                                   self.tokenKeyEntry)
        self.authFormLayout.addRow(QLabel(), QLabel())
        self.authFormLayout.addRow(QLabel("Token Secret: "),
                                   self.tokenSecretEntry)
        self.authFormLayout.addRow(QLabel(), QLabel())
        self.authFormLayout.addRow(QLabel(), self.testBtn)
        self.authFormLayout.addRow(QLabel(), QLabel())
        self.authFormLayout.addRow(QLabel(), self.saveBtn)
        self.authFormLayout.addRow(QLabel(), QLabel())
        self.authFormLayout.addRow(QLabel("Information: "), self.infoTxt)

        self.authFrame.setLayout(self.authFormLayout)
        self.mainLayout.addWidget(self.authFrame)

        self.setLayout(self.mainLayout)

    def saveCredentials(self):
        consumer_key = self.consumerKeyEntry.text()
        consumer_secret = self.consumerSecretEntry.text()
        token_key = self.tokenKeyEntry.text()
        token_secret = self.tokenSecretEntry.text()
        records_list = [consumer_key, consumer_secret, token_key, token_secret,
                        "Not tested"]
        if consumer_key and consumer_secret and token_key and token_secret != "":
            directory = ".twi_auth"
            home_dir = os.getenv('HOME')
            path = os.path.join(home_dir, directory)

            if self.existing_dir:
                file = open(f"{path}/credentials.csv", "w")
                file.truncate()
                file.close()
            else:
                os.makedirs(path)

            with open(f"{path}/credentials.csv", "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(records_list)
                f.close()
            QMessageBox.information(self, "Info", "Credentials saved!")
            self.close()
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty!")

    def testCredentials(self):
        consumer_key = self.consumerKeyEntry.text()
        consumer_secret = self.consumerSecretEntry.text()
        token_key = self.tokenKeyEntry.text()
        token_secret = self.tokenSecretEntry.text()
        if consumer_key and consumer_secret and token_key and token_secret != "":
            if self.twitter_api.valid_connection(consumer_key, consumer_secret,
                                                 token_key, token_secret):
                QMessageBox.information(self, "Info", "You are successfully"
                " connected ✅")
            else:
                QMessageBox.information(self, "Info", "There is an error in your"
                                        " login information ❌")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty!")
