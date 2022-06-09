import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
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
        self.compareStats = QAction(QIcon(resource_path('')), "Compare",
                                    self)
        self.tb.addAction(self.compareStats)
        self.compareStats.triggered.connect(self.compareStatsWindow)
        self.tb.addSeparator()

        #################Get Last Tweets#################
        self.getTweets = QAction(QIcon(resource_path('')), "Get Tweets",
                                    self)
        self.tb.addAction(self.getTweets)
        self.tb.addSeparator()

    def tabWidget(self):
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
        self.tabs.addTab(self.tab1, "Stats")
        #################Tab 1 Widgets#################

        #################Main Left Layout Widget#################

        #################Right Top Layout Widget#################

        #################Right Middle Layout Widget#################

        #################Tab 1 Layouts#################
        self.mainLayout=QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightMiddleLayout = QHBoxLayout()
        self.topGroupBox = QGroupBox("Search Box")
        self.middleGroupBox = QGroupBox("List Box")
        self.bottomGroupBox = QGroupBox()

        #################Add Widgets#################

        #################Left Main Layout Widgets#################

        #################Right Top Layout Widget#################

        #################Right Middle Layout Widget#################
        self.mainLayout.addLayout(self.mainLeftLayout, 70)
        self.mainRightLayout.addWidget(self.topGroupBox, 20)
        self.mainRightLayout.addWidget(self.middleGroupBox, 20)
        self.mainRightLayout.addWidget(self.bottomGroupBox, 60)
        self.mainLayout.addLayout(self.mainRightLayout, 30)
        self.tab1.setLayout(self.mainLayout)


    def get_followers_func(self):
        twitter_name = self.lineTest.text()
        followers_count = twitter_api.get_followers(twitter_name)
        self.LabelTest.setText(f"Number of followers: {followers_count}")



def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    # Ajouter l'icone pour l'application
    #app.setWindowIcon(QIcon(resource_path("icons/icon.icns")))
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
