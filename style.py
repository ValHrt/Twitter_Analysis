#################Box styles#################

def BoxStyleTop():
    return """
        QGroupBox{
        background-color:#3AB0FF;
        font:20pt Cochin;
        color:white;
        border:2px solid gray;
        border-radius:15px;
        }
    """

def BoxStyleMiddle():
    return """
        QGroupBox{
        background-color:#53BF9D;
        font:20pt Cochin;
        color:white;
        border:2px solid gray;
        border-radius:15px;
        }
    """

def BoxStyleMiddle_2():
    return """
        QGroupBox{
        background-color:#7858A6;
        font:20pt Cochin;
        color:white;
        border:2px solid gray;
        border-radius:15px;
        }
    """

def BoxStyleBottom():
    return """
        QGroupBox{
        font:20pt Cochin;
        color:white;
        border:2px solid gray;
        border-radius:15px;
        }
    """


#################Button styles#################

def SearchButton():
    return """
        QPushButton{
        margin: 10px;
        font-size: 15px;
        padding: 5px;
        background: #2155CD;
        color: #fff;
        outline: none;
        border-radius: 4px;
        border: 1px solid transparent;
        }
        QPushButton:hover{
        background: #001D6E;
        color: #fff;
        }
        QPushButton:pressed{
        background: #112B3C;
        color: #fff;
        }
    """

def SubmitButton():
    return """
        QPushButton{
        margin: 10px;
        font-size: 15px;
        padding: 5px;
        background: #005555;
        color: #fff;
        outline: none;
        border-radius: 4px;
        border: 1px solid transparent;
        }
        QPushButton:hover{
        background: #1A3C40;
        color: #fff;
        }
        QPushButton:pressed{
        background: #1D5C63;
        color: #fff;
        }
    """


#################Label styles#################

def InfosLabelGetTweet():
    return """
        QLabel{
        padding-top:1em;
        font-family: Cochin;
        font-size: 14pt;
        }
    """

def WelcomeLabelDescription():
    return """
        QLabel{
        font-family: Cochin;
        font-size: 15pt;
        }
    """

def TitleLabelWindow():
    return """
        QLabel{
        font-family: Cochin;
        font-size: 20pt;
        }
    """


#################Radio button style#################

def RadioButtonCompare():
    return """
        QRadioButton{
        padding-top:2em;
        }
    """
