import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import Image
import requests

from twitter_func import TwitterApiFunc


twitter_api = TwitterApiFunc()


# For compiling with PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twitter Analysis")
        self.setGeometry(50, 150, 1350, 750)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        #################Toolbar Buttons#################

        #################Compare Stats#################
        self.compareStats = QAction(QIcon(resource_path('icons/twin.png')), "Compare",
                                    self)
        self.tb.addAction(self.compareStats)
        self.compareStats.triggered.connect(self.compareStatsWindow)
        self.tb.addSeparator()

        #################Get Last Tweets#################
        self.getTweets = QAction(QIcon(resource_path('icons/note.png')), "Get Tweets",
                                    self)
        self.tb.addAction(self.getTweets)
        self.tb.addSeparator()

        #################Tweet Bot#################
        self.botTweet = QAction(QIcon(resource_path('icons/robot.png')), "Tweet Bot",
                                    self)
        self.tb.addAction(self.botTweet)
        self.tb.addSeparator()

        #################Simple Tweet#################
        self.simpleTweet = QAction(QIcon(resource_path('icons/plume.png')), "Simple Tweet",
                                    self)
        self.tb.addAction(self.simpleTweet)
        self.tb.addSeparator()

    def tabWidget(self):
        # TODO : Créer une tab d'accueil expliquant le fonctionnement des
        # modules ainsi que la manip pour connecter son compte dev Twitter
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)

    def widgets(self):
        pass

    def layouts(self):
        pass

    def compareStatsWindow(self):
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Compare")

        #################Main Left Layout Widget#################
        self.firstPersonTitle = QLabel("First person")
        self.firstPersonTitle.setAlignment(Qt.AlignCenter)
        self.firstPersonImg = QLabel()
        self.firstimg = QPixmap(resource_path('icons/man.png'))
        self.firstPersonImg.setPixmap(self.firstimg)
        self.firstPersonImg.setAlignment(Qt.AlignCenter)
        self.firstPersonFollowers = QLabel("Number of followers: ?")
        self.firstPersonFollowers.setAlignment(Qt.AlignCenter)
        self.firstPersonLikes = QLabel("Max of likes: ?")
        self.firstPersonLikes.setAlignment(Qt.AlignCenter)
        self.firstPersonRetweets = QLabel("Max retweets: ?")
        self.firstPersonRetweets.setAlignment(Qt.AlignCenter)
        self.firstPersonLikesMean = QLabel("Likes mean: ?")
        self.firstPersonLikesMean.setAlignment(Qt.AlignCenter)
        self.firstPersonRetweetsMean = QLabel("Retweets mean: ?")
        self.firstPersonRetweetsMean.setAlignment(Qt.AlignCenter)
        self.firstPersonEngageLikes = QLabel("Max engagement rate for likes:"
                                             " ?")
        self.firstPersonEngageLikes.setAlignment(Qt.AlignCenter)
        self.firstPersonEngageRetweets = QLabel("Max engagement rate for"
                                            " retweets: ?")
        self.firstPersonEngageRetweets.setAlignment(Qt.AlignCenter)
        self.firstPersonBestFavTweet = QLabel("Most fav tweet: ?")
        self.firstPersonBestFavTweet.setAlignment(Qt.AlignCenter)
        self.firstPersonBestRtTweet = QLabel("Most retweeded tweet: ?")
        self.firstPersonBestRtTweet.setAlignment(Qt.AlignCenter)

        #################Main Right Layout Widget#################
        self.secondPersonTitle = QLabel("Second person")
        self.secondPersonTitle.setAlignment(Qt.AlignCenter)
        self.secondPersonImg = QLabel()
        self.secondimg = QPixmap(resource_path('icons/woman.png'))
        self.secondPersonImg.setPixmap(self.secondimg)
        self.secondPersonImg.setAlignment(Qt.AlignCenter)
        self.secondPersonFollowers = QLabel("Number of followers: ?")
        self.secondPersonFollowers.setAlignment(Qt.AlignCenter)
        self.secondPersonLikes = QLabel("Max of likes: ?")
        self.secondPersonLikes.setAlignment(Qt.AlignCenter)
        self.secondPersonRetweets = QLabel("Max retweets: ?")
        self.secondPersonRetweets.setAlignment(Qt.AlignCenter)
        self.secondPersonLikesMean = QLabel("Likes mean: ?")
        self.secondPersonLikesMean.setAlignment(Qt.AlignCenter)
        self.secondPersonRetweetsMean = QLabel("Retweets mean: ?")
        self.secondPersonRetweetsMean.setAlignment(Qt.AlignCenter)
        self.secondPersonEngageLikes = QLabel("Max engagement rate for likes:"
                                             " ?")
        self.secondPersonEngageLikes.setAlignment(Qt.AlignCenter)
        self.secondPersonEngageRetweets = QLabel("Max engagement rate for"
                                            " retweets: ?")
        self.secondPersonEngageRetweets.setAlignment(Qt.AlignCenter)
        self.secondPersonBestFavTweet = QLabel("Most fav tweet: ?")
        self.secondPersonBestFavTweet.setAlignment(Qt.AlignCenter)
        self.secondPersonBestRtTweet = QLabel("Most retweeded tweet: ?")
        self.secondPersonBestRtTweet.setAlignment(Qt.AlignCenter)

        #################Right Top Layout Widget#################
        self.firstText = QLabel("1st: ")
        self.firstEntry = QLineEdit()
        self.firstEntry.setPlaceholderText("elonmusk")
        self.secondText = QLabel("2nd: ")
        self.secondEntry = QLineEdit()
        self.secondEntry.setPlaceholderText("potus")

        #################Right Middle Layout Widget#################
        self.includeReplies = QRadioButton("Include replies")
        self.excludeReplies = QRadioButton("Exclude replies")
        self.tweetsNumber = QLabel("Number of tweets: ")
        self.tweetsSpinBox = QSpinBox()
        self.tweetsSpinBox.setRange(10, 150)
        self.tweetsSpinBox.setSingleStep(10)
        self.submitBtn = QPushButton("🚀 Launch comparison 🚀")
        self.submitBtn.clicked.connect(self.compare_func)

        #################Tab Layouts#################
        self.mainLayout=QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightMiddleLayout = QFormLayout()
        self.topGroupBox = QGroupBox("Twitter names")
        self.middleGroupBox = QGroupBox("Additional options")
        self.bottomGroupBox = QGroupBox()

        #################Add Widgets#################

        #################Left Main Layout Widgets#################
        self.mainLeftLayout.addWidget(self.firstPersonTitle)
        self.mainLeftLayout.addWidget(self.firstPersonImg)
        self.mainLeftLayout.addWidget(self.firstPersonFollowers)
        self.mainLeftLayout.addWidget(self.firstPersonLikes)
        self.mainLeftLayout.addWidget(self.firstPersonRetweets)
        self.mainLeftLayout.addWidget(self.firstPersonLikesMean)
        self.mainLeftLayout.addWidget(self.firstPersonRetweetsMean)
        self.mainLeftLayout.addWidget(self.firstPersonEngageLikes)
        self.mainLeftLayout.addWidget(self.firstPersonEngageRetweets)
        self.mainLeftLayout.addWidget(self.firstPersonBestFavTweet)
        self.mainLeftLayout.addWidget(self.firstPersonBestRtTweet)

        #################Right Main Layout Widgets#################
        self.mainRightLayout.addWidget(self.secondPersonTitle)
        self.mainRightLayout.addWidget(self.secondPersonImg)
        self.mainRightLayout.addWidget(self.secondPersonFollowers)
        self.mainRightLayout.addWidget(self.secondPersonLikes)
        self.mainRightLayout.addWidget(self.secondPersonRetweets)
        self.mainRightLayout.addWidget(self.secondPersonLikesMean)
        self.mainRightLayout.addWidget(self.secondPersonRetweetsMean)
        self.mainRightLayout.addWidget(self.secondPersonEngageLikes)
        self.mainRightLayout.addWidget(self.secondPersonEngageRetweets)
        self.mainRightLayout.addWidget(self.secondPersonBestFavTweet)
        self.mainRightLayout.addWidget(self.secondPersonBestRtTweet)

        #################Right Top Layout Widget#################
        self.rightTopLayout.addWidget(self.firstText)
        self.rightTopLayout.addWidget(self.firstEntry)
        self.rightTopLayout.addWidget(self.secondText)
        self.rightTopLayout.addWidget(self.secondEntry)
        self.topGroupBox.setLayout(self.rightTopLayout)

        #################Right Middle Layout Widget#################
        self.rightMiddleLayout.addRow(self.includeReplies, self.excludeReplies)
        self.rightMiddleLayout.addRow(QLabel(""), QLabel(""))
        self.rightMiddleLayout.addRow(self.tweetsNumber, self.tweetsSpinBox)
        self.rightMiddleLayout.addRow(QLabel(""), QLabel(""))
        self.rightMiddleLayout.addRow(QLabel(""), self.submitBtn)
        self.middleGroupBox.setLayout(self.rightMiddleLayout)

        #################Set Layouts#################
        self.mainLayout.addLayout(self.mainLeftLayout, 35)
        self.mainLayout.addLayout(self.mainRightLayout, 35)
        self.rightLayout.addWidget(self.topGroupBox, 20)
        self.rightLayout.addWidget(self.middleGroupBox, 30)
        self.rightLayout.addWidget(self.bottomGroupBox, 50)
        self.mainLayout.addLayout(self.rightLayout, 30)
        self.tab1.setLayout(self.mainLayout)


    def compare_func(self):
        img_size = (200, 200)
        first_twitter_name = self.firstEntry.text()
        second_twitter_name = self.secondEntry.text()
        spin_value = self.tweetsSpinBox.value()
        if self.includeReplies.isChecked():
            radio_value = False
        else:
            radio_value = True

        if first_twitter_name and second_twitter_name != "":
            first_results = twitter_api.comparison_infos(first_twitter_name,
                                                      radio_value, spin_value)
            second_results = twitter_api.comparison_infos(second_twitter_name,
                                                          radio_value, spin_value)

            #################First person widgets#################
            self.firstPersonTitle.setText(first_results[9])
            #################First person image#################
            if first_results[10] != "?":
                # Load img from url without size 48x48 by removing _normal from API
                first_img_url = f"{first_results[10][:-11]}.jpg"
                first_img = Image.open(requests.get(first_img_url, stream=True).raw)
                first_img = first_img.resize(img_size)
                first_img.save(resource_path(f"img/first_img.jpg"))
                self.firstimg = QPixmap(resource_path("img/first_img.jpg"))
                self.firstPersonImg.setPixmap(self.firstimg)
            else:
                QMessageBox.information(self, "Info", f"{first_twitter_name} doesn't"
                " exists on Twitter")

            #################First person labels#################
            self.firstPersonFollowers.setText(f"Number of followers: "
            f"{first_results[0]} {self.compare_winner(first_results[0], second_results[0])}")
            self.firstPersonLikes.setText(f"Max of likes: {first_results[1]} "
                                          f"{self.compare_winner(first_results[1], second_results[1])}")
            self.firstPersonRetweets.setText(f"Max retweets: {first_results[2]} "
                                             f"{self.compare_winner(first_results[2], second_results[2])}")
            self.firstPersonLikesMean.setText(f"Likes mean: {first_results[3]} "
                                              f"{self.compare_winner(first_results[3], second_results[3])}")
            self.firstPersonRetweetsMean.setText(f"Retweets mean: "
                                                 f"{first_results[4]} "
                                                 f"{self.compare_winner(first_results[4], second_results[4])}")
            self.firstPersonEngageLikes.setText(f"Max engagement rate for likes:"
                                                 f" {first_results[5]}% "
                                                f"{self.compare_winner(first_results[5], second_results[5])}")
            self.firstPersonEngageRetweets.setText(f"Max engagement rate for"
                                                f" retweets: {first_results[6]}% "
                                                   f"{self.compare_winner(first_results[6], second_results[6])}")
            self.firstPersonBestFavTweet.setText(f"Most fav tweet:\n"
                                                 f"{first_results[7]}")
            self.firstPersonBestFavTweet.setWordWrap(True)
            self.firstPersonBestRtTweet.setText(f"Most retweeded tweet:\n"
                                                f"{first_results[8]}")
            self.firstPersonBestRtTweet.setWordWrap(True)

            #################Second person widgets#################
            self.secondPersonTitle.setText(second_results[9])
            #################Second person image#################
            if second_results[10] != "?":
                # Load img from url without size 48x48 by removing _normal from API
                second_img_url = f"{second_results[10][:-11]}.jpg"
                second_img = Image.open(requests.get(second_img_url, stream=True).raw)
                second_img = second_img.resize(img_size)
                second_img.save(resource_path(f"img/second_img.jpg"))
                self.secondimg = QPixmap(resource_path("img/second_img.jpg"))
                self.secondPersonImg.setPixmap(self.secondimg)
            else:
                QMessageBox.information(self, "Info", f"{second_twitter_name} doesn't"
                " exists on Twitter")

            #################Second person labels#################
            self.secondPersonFollowers.setText(f"Number of followers: "
            f"{second_results[0]} {self.compare_winner(second_results[0], first_results[0])}")
            self.secondPersonLikes.setText(f"Max of likes: {second_results[1]} "
                                           f"{self.compare_winner(second_results[1], first_results[1])}")
            self.secondPersonRetweets.setText(f"Max retweets: {second_results[2]} "
                                              f"{self.compare_winner(second_results[2], first_results[2])}")
            self.secondPersonLikesMean.setText(f"Likes mean: {second_results[3]} "
                                               f"{self.compare_winner(second_results[3], first_results[3])}")
            self.secondPersonRetweetsMean.setText(f"Retweets mean: "
                                                 f"{second_results[4]} "
                                                  f"{self.compare_winner(second_results[4], first_results[4])}")
            self.secondPersonEngageLikes.setText(f"Max engagement rate for likes:"
                                                 f" {second_results[5]}% "
                                                 f"{self.compare_winner(second_results[5], first_results[5])}")
            self.secondPersonEngageRetweets.setText(f"Max engagement rate for"
                                                f" retweets: {second_results[6]}% "
                                                    f"{self.compare_winner(second_results[6], first_results[6])}")
            self.secondPersonBestFavTweet.setText(f"Most fav tweet:\n"
                                                 f"{second_results[7]}")
            self.secondPersonBestFavTweet.setWordWrap(True)
            self.secondPersonBestRtTweet.setText(f"Most retweeded tweet:\n"
                                                f"{second_results[8]}")
            self.secondPersonBestRtTweet.setWordWrap(True)

        else:
            QMessageBox.information(self, "Info", "Names fields should not be"
            " empty")

    @staticmethod
    def compare_winner(first, second):
        if first > second:
            return "🏆"
        elif first == second:
            return "🟰"
        else:
            return "🥈"



def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon(resource_path("icons/twitter.icns")))
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
