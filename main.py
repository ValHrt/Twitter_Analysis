import sys, os, csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import Image
import requests

from twitter_func import TwitterApiFunc
from widgets_window import SimpleTweetWindow, TweetBotWindow, AuthWindow
import modules_text
import style


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
        self.check_credentials()

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
        self.getTweets.triggered.connect(self.getTweetsWindow)
        self.tb.addSeparator()

        #################Tweet Bot#################
        self.botTweet = QAction(QIcon(resource_path('icons/robot.png')), "Tweet Bot",
                                    self)
        self.tb.addAction(self.botTweet)
        self.botTweet.triggered.connect(self.tweet_bot_func)
        self.tb.addSeparator()

        #################Simple Tweet#################
        self.simpleTweet = QAction(QIcon(resource_path('icons/plume.png')), "Simple Tweet",
                                    self)
        self.tb.addAction(self.simpleTweet)
        self.simpleTweet.triggered.connect(self.simple_tweet_func)
        self.tb.addSeparator()

        #################Top Tweet#################
        self.topTweet = QAction(QIcon(resource_path('icons/badge.png')), "Top Tweets",
                                self)
        self.tb.addAction(self.topTweet)
        self.topTweet.triggered.connect(self.topTweetWindow)
        self.tb.addSeparator()

        #################Authentification#################
        self.authentification = QAction(QIcon(resource_path('icons/authentification.png')),
                                        "Authentification", self)
        self.tb.addAction(self.authentification)
        self.authentification.triggered.connect(self.authWindow)
        self.tb.addSeparator()

    def tabWidget(self):
        # TODO : Créer une tab d'accueil expliquant le fonctionnement des
        # modules ainsi que la manip pour connecter son compte dev Twitter
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)

    def widgets(self):
        #################Welcome Screen Tab#################
        self.tabWelcome = QWidget()
        tab_welc_index = self.tabs.addTab(self.tabWelcome, "Welcome")
        self.tabs.setTabIcon(tab_welc_index,
                             QIcon(resource_path('icons/twitter.icns')))
        # Remove close button from welcome tab
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, None)

        #################Welcome Screen Widgets#################
        self.titleWelcLabel = QLabel("Welcome to the Twitter Toolbox Dev App")
        self.titleWelcLabel.setAlignment(Qt.AlignCenter)
        self.titleWelcLabel.setStyleSheet("font-size: 45pt;font-family: Cochin")
        self.welcText = QLabel("Select in the list widget below"
                               " to get information about the selected module.")
        self.welcText.setStyleSheet("font-family: Cochin; font-size: 20pt")
        self.welcText.setAlignment(Qt.AlignCenter)
        self.welcimg = QPixmap(resource_path('icons/down-arrow.png'))
        self.welcImage = QLabel()
        self.welcImage.setPixmap(self.welcimg)
        self.welcImage.setAlignment(Qt.AlignCenter)
        self.welcComboWidget = QComboBox()
        # setEditable set to True to center items in the dropdown menu
        self.welcComboWidget.setEditable(True)
        widgets_list = ["Compare", "Get Tweets", "Tweet Bot", "Simple Tweet",
                        "Top Tweets", "Authentification"]
        self.welcComboWidget.addItems(widgets_list)
        self.welcComboWidget.currentIndexChanged.connect(self.moduleInfo)
        # line_edit variable used to center each item in the list
        line_edit = self.welcComboWidget.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        # setReadOnly to turn off the setEditable set to True before
        line_edit.setReadOnly(True)

    def layouts(self):
        #################Welcome Screen Layouts#################
        self.welcMainLayout = QVBoxLayout()
        self.welcMainLayout.setAlignment(Qt.AlignHCenter)
        self.welcMainLayout.setContentsMargins(200, 0, 200, 0)
        self.horizontalContainer = QHBoxLayout()
        self.welcLeftSubLayout = QVBoxLayout()
        self.welcRightSubLayout = QVBoxLayout()

        self.moduleImage = QLabel()
        self.moduleimg = QPixmap(resource_path('icons/twin.png'))
        self.moduleimg = self.moduleimg.scaled(300, 300)
        self.moduleImage.setPixmap(self.moduleimg)
        self.moduleImage.setAlignment(Qt.AlignCenter)
        self.moduleLabel = QLabel(modules_text.compare_module)
        self.moduleLabel.setWordWrap(True)
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.setStyleSheet(style.WelcomeLabelDescription())

        #################Main Layout Widgets#################
        self.welcMainLayout.addWidget(self.titleWelcLabel)
        self.welcMainLayout.addWidget(self.welcText)
        self.welcMainLayout.addWidget(self.welcImage)
        self.welcMainLayout.addWidget(self.welcComboWidget)

        #################Subs Layout Widgets#################
        self.welcLeftSubLayout.addWidget(self.moduleImage)
        self.welcRightSubLayout.addWidget(self.moduleLabel)
        self.horizontalContainer.addLayout(self.welcLeftSubLayout, 50)
        self.horizontalContainer.addLayout(self.welcRightSubLayout, 50)
        self.welcMainLayout.addLayout(self.horizontalContainer)

        self.tabWelcome.setLayout(self.welcMainLayout)

    def compareStatsWindow(self):
        self.tabCompare = QWidget()
        tab_compare_index = self.tabs.addTab(self.tabCompare, "Compare")
        self.tabs.setTabIcon(tab_compare_index,
                             QIcon(resource_path('icons/twin.png')))
        index = self.tabs.indexOf(self.tabCompare)
        self.tabs.setCurrentIndex(index)

        #################Main Left Layout Widget#################
        self.firstPersonTitle = QLabel("First person")
        self.firstPersonTitle.setAlignment(Qt.AlignCenter)

        # TODO: Temporaire, à mettre dans la feuille de style ensuite
        self.firstPersonTitle.setStyleSheet("font-size: 22pt;font-family: Cochin")

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

        # TODO: Temporaire, à mettre dans la feuille de style ensuite
        self.secondPersonTitle.setStyleSheet("font-size: 22pt;font-family: Cochin")
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
        self.includeReplies.setStyleSheet(style.RadioButtonCompare())
        self.excludeReplies = QRadioButton("Exclude replies")
        self.excludeReplies.setStyleSheet(style.RadioButtonCompare())
        self.excludeReplies.setChecked(True)
        self.tweetsNumber = QLabel("Number of tweets: ")
        self.tweetsSpinBox = QSpinBox()
        self.tweetsSpinBox.setRange(10, 150)
        self.tweetsSpinBox.setSingleStep(10)
        self.submitBtn = QPushButton("🚀 Launch comparison 🚀")
        self.submitBtn.setStyleSheet(style.SubmitButton())
        self.submitBtn.clicked.connect(self.compare_func)

        #################Tab Layouts#################
        self.mainLayout=QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightMiddleLayout = QFormLayout()
        self.topGroupBox = QGroupBox("Twitter names")
        self.topGroupBox.setStyleSheet(style.BoxStyleTop())
        self.middleGroupBox = QGroupBox("Additional options")
        self.middleGroupBox.setStyleSheet(style.BoxStyleMiddle())
        self.bottomGroupBox = QGroupBox()

        #################Add Widgets#################

        #################Left Main Layout Setting#################
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

        #################Right Main Layout Setting#################
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

        #################Right Top Layout Setting#################
        self.rightTopLayout.addWidget(self.firstText)
        self.rightTopLayout.addWidget(self.firstEntry)
        self.rightTopLayout.addWidget(self.secondText)
        self.rightTopLayout.addWidget(self.secondEntry)
        self.topGroupBox.setLayout(self.rightTopLayout)

        #################Right Middle Layout Setting#################
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
        self.tabCompare.setLayout(self.mainLayout)

    def getTweetsWindow(self, top_tweet_keyword=None):
        """Get Tweet Window. Parameter top_tweet_keyword is used to retrieve the
        keyword passed from topTweetWindow when a user double click on a trend
        to get the top 10 tweets related to this keyword."""
        self.tabGetTweets = QWidget()
        if not top_tweet_keyword:
            tab_get_tweets_index = self.tabs.addTab(self.tabGetTweets, "Get Tweets")
            self.tabs.setTabIcon(tab_get_tweets_index,
                                 QIcon(resource_path('icons/note.png')))
        else:
            tab_get_tweets_index = self.tabs.addTab(self.tabGetTweets, "Top 10 Tweets")
            self.tabs.setTabIcon(tab_get_tweets_index,
                                 QIcon(resource_path('icons/trophy.png')))
        index = self.tabs.indexOf(self.tabGetTweets)
        self.tabs.setCurrentIndex(index)

        #################Left Layout Widgets#################
        self.tableTweets = QTableWidget()
        self.tableTweets.setWordWrap(True)
        self.tableTweets.setColumnCount(6)
        self.tableTweets.setColumnHidden(0, True)
        col_names = ["Tweet ID", "Name", "Tweet", "Date", "Like", "Retweet"]
        for i, v in enumerate(col_names):
            self.tableTweets.setHorizontalHeaderItem(i, QTableWidgetItem(v))
        self.tableTweets.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableTweets.doubleClicked.connect(self.reply_tweet_func)

        # Align left for Table Widget and auto stretching
        self.tableTweets.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableTweets.horizontalHeader().setSectionResizeMode(2,
                                                                 QHeaderView.Stretch)
        self.tableTweets.verticalHeader().setDefaultSectionSize(150)

        self.tableTweets.setAlternatingRowColors(True)
        self.tableTweets.horizontalHeader().setFixedHeight(25)

        #################Right Layout Widgets#################
        #################Top Widgets#################
        self.keywordLineEdit = QLineEdit()
        self.keywordLineEdit.setPlaceholderText("Keyword")
        if top_tweet_keyword:
            self.keywordLineEdit.setText(top_tweet_keyword)
        self.nbSearchLabel = QLabel("Nb of tweets: ")
        self.getTweetsSpin = QSpinBox()
        self.getTweetsSpin.setRange(5, 100)
        self.getTweetsSpin.setSingleStep(5)
        self.getTweetsSpin.setValue(10)
        self.getTweetsBtn = QPushButton("Search")
        self.getTweetsBtn.setStyleSheet(style.SearchButton())
        self.getTweetsBtn.clicked.connect(self.get_tweets_func)

        #################Middle Widgets#################
        self.userLineEdit = QLineEdit()
        self.userLineEdit.setPlaceholderText("elonmusk")
        self.userSelected = QRadioButton("Select User")
        self.noUserSelected = QRadioButton("Global Search")
        self.noUserSelected.setChecked(True)

        #################Middle 2 Widgets#################
        self.searchOptionLabel = QLabel("Search Option")
        self.searchOptionMenu = QComboBox()
        options = ["Recent", "Popular"]
        self.searchOptionMenu.addItems(options)
        if top_tweet_keyword:
            self.searchOptionMenu.setCurrentIndex(1)

        #################Bottom Widgets#################
        self.infoGetTweets = QLabel(modules_text.get_tweets_info)
        self.infoGetTweets.setWordWrap(True)
        self.infoGetTweets.setStyleSheet(style.InfosLabelGetTweet())

        #################Tab Layouts#################
        self.getTweetsMainLayout = QHBoxLayout()
        self.getTweetsLeftLayout = QVBoxLayout()
        self.getTweetsRightLayout = QVBoxLayout()
        self.getTweetsTopRightLayout = QHBoxLayout()
        self.getTweetsMiddleRightLayout = QHBoxLayout()
        self.getTweetsMiddleRightLayout_2 = QHBoxLayout()
        self.getTweetsBottomRightLayout = QHBoxLayout()
        self.getTweetsTopBox = QGroupBox("Keyword Search")
        self.getTweetsTopBox.setStyleSheet(style.BoxStyleTop())
        self.getTweetsMiddleBox = QGroupBox("User")
        self.getTweetsMiddleBox.setStyleSheet(style.BoxStyleMiddle())
        self.getTweetsMiddleBox_2 = QGroupBox("Options")
        self.getTweetsMiddleBox_2.setStyleSheet(style.BoxStyleMiddle_2())
        self.getTweetsBottomBox = QGroupBox("Useful Information")
        self.getTweetsBottomBox.setStyleSheet(style.BoxStyleBottom())

        #################Left Layout Setting#################
        self.getTweetsLeftLayout.addWidget(self.tableTweets)

        #################Right Layout Setting#################
        if not top_tweet_keyword:

            #################Top Box Settings#################
            self.getTweetsTopRightLayout.addWidget(self.keywordLineEdit)
            self.getTweetsTopRightLayout.addWidget(self.nbSearchLabel)
            self.getTweetsTopRightLayout.addWidget(self.getTweetsSpin)
            self.getTweetsTopRightLayout.addWidget(self.getTweetsBtn)
            self.getTweetsTopBox.setLayout(self.getTweetsTopRightLayout)
            self.getTweetsRightLayout.addWidget(self.getTweetsTopBox, 20)

            #################Middle Box Settings#################
            self.getTweetsMiddleRightLayout.addWidget(self.userLineEdit)
            self.getTweetsMiddleRightLayout.addWidget(self.userSelected)
            self.getTweetsMiddleRightLayout.addWidget(self.noUserSelected)
            self.getTweetsMiddleBox.setLayout(self.getTweetsMiddleRightLayout)
            self.getTweetsRightLayout.addWidget(self.getTweetsMiddleBox, 20)

            self.getTweetsMiddleRightLayout_2.addWidget(self.searchOptionLabel)
            self.getTweetsMiddleRightLayout_2.addWidget(self.searchOptionMenu)
            self.getTweetsMiddleBox_2.setLayout(self.getTweetsMiddleRightLayout_2)
            self.getTweetsRightLayout.addWidget(self.getTweetsMiddleBox_2, 20)

            #################Bottom Box Settings#################
            self.getTweetsBottomRightLayout.addWidget(self.infoGetTweets)
            self.getTweetsBottomBox.setLayout(self.getTweetsBottomRightLayout)
            self.getTweetsRightLayout.addWidget(self.getTweetsBottomBox, 40)

        #################Set Layouts#################
        self.getTweetsMainLayout.addLayout(self.getTweetsLeftLayout, 70)
        if not top_tweet_keyword:
            self.getTweetsMainLayout.addLayout(self.getTweetsRightLayout, 30)
        self.tabGetTweets.setLayout(self.getTweetsMainLayout)

    def topTweetWindow(self):
        self.tabTopTweet = QWidget()
        tab_top_tweet_index = self.tabs.addTab(self.tabTopTweet, "Top Tweets")
        self.tabs.setTabIcon(tab_top_tweet_index,
                             QIcon(resource_path('icons/badge.png')))
        index = self.tabs.indexOf(self.tabTopTweet)
        self.tabs.setCurrentIndex(index)

        twitter_api = self.check_credentials()
        if twitter_api != "Error":
            woeid_list = twitter_api.get_trends_loc()
            woeid_list_tmp = {}
            for v in woeid_list:
                #print(v["country"], v["name"], v["woeid"])
                woeid_list_tmp.setdefault(v["country"], []).append([v["name"], v["woeid"]])
                #print(woeid_list_tmp)
            self.woeid_list_cleaned = dict(sorted(woeid_list_tmp.items()))
            self.woeid_list_cleaned.pop('')

        #################Left Layout Widgets#################
        self.table_label = QLabel("Country: City")
        self.table_label.setAlignment(Qt.AlignCenter)
        self.tableTopTweet = QTableWidget()
        self.tableTopTweet.setWordWrap(True)
        self.tableTopTweet.setColumnCount(2)
        col_names = ["Trend", "Tweet Volume"]
        for i, v in enumerate(col_names):
            self.tableTopTweet.setHorizontalHeaderItem(i, QTableWidgetItem(v))
        self.tableTopTweet.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableTopTweet.doubleClicked.connect(self.get_top_10_tweets)

        # Align left for Table Widget and auto stretching
        self.tableTopTweet.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableTopTweet.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableTopTweet.horizontalHeader().setFixedHeight(25)

        #################Right Layout Widgets#################
        #################Right Top Layout Widgets#################
        self.country_label = QLabel("Country: ")
        self.country_menu = QComboBox()
        self.city_label = QLabel("City: ")
        self.city_menu = QComboBox()
        if twitter_api != "Error":
            country_list = list(self.woeid_list_cleaned.keys())
            #print(country_list)
            self.country_menu.addItems(country_list)
            self.country_menu.setCurrentIndex(country_list.index("United States"))
            for v in self.woeid_list_cleaned["United States"]:
                #print(v)
                self.city_menu.addItem(v[0])
            self.country_menu.currentIndexChanged.connect(self.updateCityList)
        else:
            self.country_menu.addItem("Login Error!")
            self.city_menu.addItem("Login Error!")

        #################Right Middle Layout Widgets#################
        self.trending_tweets = QRadioButton("Trending Tweets")
        self.trending_tweets.setChecked(True)
        self.trending_hashtags = QRadioButton("Trending Hashtags")
        self.submitBtnTopTweet = QPushButton("Submit")
        self.submitBtnTopTweet.setStyleSheet(style.SubmitButton())
        self.submitBtnTopTweet.clicked.connect(self.top_tweet_func)

        #################Tab Layouts#################
        self.topTweetMainLayout = QHBoxLayout()
        self.topTweetLeftLayout = QVBoxLayout()
        self.topTweetRightLayout = QVBoxLayout()
        self.topTweetTopRightLayout = QHBoxLayout()
        self.topTweetMiddleRightLayout = QHBoxLayout()
        self.topTweetBottomRightLayout = QHBoxLayout()
        self.topTweetTopBox = QGroupBox("Localisation")
        self.topTweetTopBox.setStyleSheet(style.BoxStyleTop())
        self.topTweetMiddleBox = QGroupBox("Trending selection")
        self.topTweetMiddleBox.setStyleSheet(style.BoxStyleMiddle())
        self.topTweetBottomBox = QGroupBox()

        #################Left Layout Setting#################
        self.topTweetLeftLayout.addWidget(self.table_label)
        self.topTweetLeftLayout.addWidget(self.tableTopTweet)

        #################Right Layout Setting#################
        self.topTweetTopRightLayout.addWidget(self.country_label)
        self.topTweetTopRightLayout.addWidget(self.country_menu)
        self.topTweetTopRightLayout.addWidget(self.city_label)
        self.topTweetTopRightLayout.addWidget(self.city_menu)
        self.topTweetTopBox.setLayout(self.topTweetTopRightLayout)
        self.topTweetRightLayout.addWidget(self.topTweetTopBox, 30)

        self.topTweetMiddleRightLayout.addWidget(self.trending_tweets)
        self.topTweetMiddleRightLayout.addWidget(self.trending_hashtags)
        self.topTweetMiddleRightLayout.addWidget(self.submitBtnTopTweet)
        self.topTweetMiddleBox.setLayout(self.topTweetMiddleRightLayout)
        self.topTweetRightLayout.addWidget(self.topTweetMiddleBox, 30)

        self.topTweetRightLayout.addWidget(self.topTweetBottomBox, 40)

        #################Set Layouts#################
        self.topTweetMainLayout.addLayout(self.topTweetLeftLayout, 70)
        self.topTweetMainLayout.addLayout(self.topTweetRightLayout, 30)
        self.tabTopTweet.setLayout(self.topTweetMainLayout)

    def moduleInfo(self):
        module_selected = self.welcComboWidget.currentText()
        module_dict = {
            "Compare": ["twin.png", "compare_module"],
            "Get Tweets": ["note.png", "search_tweets_module"],
            "Tweet Bot": ["robot.png", "tweet_bot_module"],
            "Simple Tweet": ["plume.png", "simple_tweet_module"],
            "Top Tweets": ["badge.png", "top_tweets_module"],
            "Authentification": ["authentification.png",
                                 "authentification_module"]
        }
        self.moduleimg = QPixmap(resource_path(f'icons/{module_dict[module_selected][0]}'))
        self.moduleimg = self.moduleimg.scaled(300, 300)
        self.moduleImage.setPixmap(self.moduleimg)
        module_txt = eval(f"modules_text.{module_dict[module_selected][1]}")
        self.moduleLabel.setText(module_txt)

    def compare_func(self):
        twitter_api = self.check_credentials()
        if twitter_api != "Error":
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
                self.firstPersonTitle.setText(f"@{first_results[9]}")
                #################First person image#################
                try:
                    if first_results[10] != "?":
                        # Load img from url without size 48x48 by removing _normal from API
                        first_img_url = f"{first_results[10][:-11]}.jpg"
                        first_img = Image.open(requests.get(first_img_url, stream=True).raw)
                        first_img = first_img.resize(img_size)
                        first_img.save(resource_path(f"img/first_img.jpg"))
                        self.firstimg = QPixmap(resource_path("img/first_img.jpg"))
                        self.firstPersonImg.setPixmap(self.firstimg)
                    else:
                        QMessageBox.information(self, "Info", f"@{first_twitter_name} "
                                                f"doesn't exists on Twitter (or has not "
                                                f"tweeted more than {spin_value} times or "
                                                f"is in private profile)")
                except Exception as e:
                    print(e)
                    QMessageBox.information(self, "Info", f"Impossible to retrieve"
                                            f" the photo of @{first_twitter_name}"
                                            f" because the photo is too old and is not"
                                            f" retrieved by the Twitter API")

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
                self.secondPersonTitle.setText(f"@{second_results[9]}")
                #################Second person image#################
                try:
                    if second_results[10] != "?":
                        # Load img from url without size 48x48 by removing _normal from API
                        second_img_url = f"{second_results[10][:-11]}.jpg"
                        second_img = Image.open(requests.get(second_img_url, stream=True).raw)
                        second_img = second_img.resize(img_size)
                        second_img.save(resource_path(f"img/second_img.jpg"))
                        self.secondimg = QPixmap(resource_path("img/second_img.jpg"))
                        self.secondPersonImg.setPixmap(self.secondimg)
                    else:
                        QMessageBox.information(self, "Info", f"@{second_twitter_name} "
                                                f"doesn't exists on Twitter (or has not "
                                                f"tweeted more than {spin_value} times or "
                                                f"is in private profile)")

                except Exception as e:
                    print(e)
                    QMessageBox.information(self, "Info", f"Impossible to retrieve"
                                            f" the photo of @{second_twitter_name}"
                                            f" because the photo is too old and is not"
                                            f" retrieved by the Twitter API")

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

    def get_tweets_func(self):
        twitter_api = self.check_credentials()
        if twitter_api != "Error":
            keyword = self.keywordLineEdit.text()
            spin_value = self.getTweetsSpin.value()
            search_option = self.searchOptionMenu.currentText()
            if self.noUserSelected.isChecked():
                values = twitter_api.get_tweets(keyword, spin_value,
                                                search_option)
            else:
                user_name = self.userLineEdit.text()
                values = twitter_api.get_tweets(keyword, spin_value, search_option,
                                                user_selected=user_name)

            if len(values) == 6:
                if len(values[0]) >= 1:
                    self.tableTweets.setRowCount(len(values[0]))
                    for i, v in enumerate(values):
                        for idx in range(len(v)):
                            self.tableTweets.setItem(idx, i, QTableWidgetItem(str(v[idx])))
                    self.tableTweets.resizeColumnToContents(3)
                    self.tableTweets.resizeColumnToContents(4)
                    self.tableTweets.resizeColumnToContents(5)
                else:
                    QMessageBox.information(self, "Info", "This request doesn't"
                                            " return any tweet: check the keyword"
                                            " or the username (if you checked that"
                                            " option)")
            else:
                QMessageBox.information(self, "Info", values)

    def reply_tweet_func(self):
        tweet_id = self.tableTweets.item(self.tableTweets.currentRow(), 0).text()
        tweet_name = self.tableTweets.item(self.tableTweets.currentRow(), 1).text()
        tweet_text = self.tableTweets.item(self.tableTweets.currentRow(),
                                           2).text()
        self.reply_tweet_window = SimpleTweetWindow(twitter_api, True, tweet_id,
                                                   tweet_name, tweet_text)

    def simple_tweet_func(self):
        twitter_api = self.check_credentials()
        if twitter_api != "Error":
            self.simple_tweet_window = SimpleTweetWindow(twitter_api, False)

    def tweet_bot_func(self):
        twitter_api = self.check_credentials()
        if twitter_api != "Error":
            self.tweet_bot_window = TweetBotWindow(twitter_api)

    def top_tweet_func(self):
        twitter_api = self.check_credentials()
        if twitter_api != "Error":
            city_index = self.city_menu.currentIndex()
            country_selected = self.country_menu.currentText()
            city_selected = self.city_menu.currentText()
            woeid = self.woeid_list_cleaned[country_selected][city_index][1]
            #print(woeid)
            if country_selected != city_selected:
                self.table_label.setText(f"{country_selected}: {city_selected}")
            else:
                self.table_label.setText(country_selected)

            if self.trending_hashtags.isChecked():
                values = twitter_api.get_top_tweets(woeid, True)
            else:
                values = twitter_api.get_top_tweets(woeid, False)

            self.tableTopTweet.setRowCount(len(values))
            for row, (key, value) in enumerate(values.items()):
                for column in range(2):
                    if column == 0:
                        self.tableTopTweet.setItem(row, column,
                                                   QTableWidgetItem(key))
                    else:
                        self.tableTopTweet.setItem(row, column,
                                               QTableWidgetItem(str(value)))

    def get_top_10_tweets(self):
        trend_keyword = self.tableTopTweet.item(self.tableTopTweet.currentRow(), 0).text()
        self.getTweetsWindow(trend_keyword)
        self.get_tweets_func()

    def authWindow(self):
        if os.path.exists(os.path.join(os.getenv('HOME'), '.twi_auth',
                                       'credentials.csv')):
            with open(f"{os.getenv('HOME')}/.twi_auth/credentials.csv") as f:
                csv_reader = csv.reader(f)
                credentials_csv = next(csv_reader)
                f.close()
            self.auth_window = AuthWindow(True, twitter_api, credentials_csv)
        else:
            self.auth_window = AuthWindow(False, twitter_api)

    def updateCityList(self):
        country_selected = self.country_menu.currentText()
        self.city_menu.clear()
        for city in self.woeid_list_cleaned[country_selected]:
            self.city_menu.addItem(city[0])

    @staticmethod
    def compare_winner(first, second):
        if first > second:
            return "🏆"
        elif first == second:
            return "🟰"
        else:
            return "🥈"

    def check_credentials(self):
        twitter_api = TwitterApiFunc()
        if twitter_api.error_msg == "Credentials Missing":
            QMessageBox.information(self, "Info", "You need to save your"
            " twitter dev account credentials to use this application!\n\n"
            "You will be redirected to the Authentification window.")
            self.authWindow()
            return "Error"
        elif twitter_api.error_msg == "Wrong Credentials":
            QMessageBox.information(self, "Info", "The credentials provided"
            " are wrong, please check again!\n\nYou will be redirected to"
            " the Authentification window.")
            self.authWindow()
            return "Error"
        else:
            return twitter_api



def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon(resource_path("icons/twitter.icns")))
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
