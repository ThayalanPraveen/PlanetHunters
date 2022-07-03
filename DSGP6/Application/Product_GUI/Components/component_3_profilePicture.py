##########################################################################
# Component ID : 3
# Function : Display profile picture and welcome message

# Offset Control
#-----------------
cmp_3_x_offset = 0
cmp_3_y_offset = 0
#-----------------

# Component Variables
# -----------------
avatar = None # component_3
pfp_load = False # component_3
network_status = False # component_3
username = "" # component_3
# -----------------

###########################################################################


# Imports, variables and themes of components
###########################################################################
import time
import PySide6
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import json
from matplotlib import use
import pandas as pd
import os
import joblib
import lightkurve as lk
import matplotlib.pyplot
import numpy as np
import matplotlib.pyplot as plt
import requests
import firebase_admin
from firebase_admin import db
import sys
import firebase_admin
from firebase_admin import credentials
from cryptography.fernet import Fernet
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


# Application font
# --------------------------------------------------------------------------
app_font = "Arial"
# --------------------------------------------------------------------------

# Application colors
# --------------------------------------------------------------------------
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb
# rgb_to_hex((255, 255, 195)) use if needed

background_color = (20, 21, 32)
background_color_hex = "141520"
logout_color_hex = "c23b02"
error_color_hex = "c23b02"
button_color_hex = "4b993f"
button_alt_color_hex = "0a71d1"
button_hover_hex = "edb009"

# --------------------------------------------------------------------------

# Color schemes
# --------------------------------------------------------------------------
scheme1 = ["141520","4b993f","0a71d1","edb009"]

# Set Color scheme
# --------------------------------------------------------------------------

def set_scheme(scheme):
    global background_color_hex
    global button_color_hex
    global button_hover_hex
    global button_alt_color_hex

    background_color_hex = scheme[0]
    button_color_hex = scheme[1]
    button_alt_color_hex = scheme[2]
    button_hover_hex = scheme[3]
    
set_scheme(scheme1)
# --------------------------------------------------------------------------
###########################################################################


class Component(QWidget):

    # Initialize login screen
    # --------------------------------------------------------------------------
    def __init__(self, parent=None):
        super().__init__()
        self.window = None
        self.window2 = None
        global width,height
        width = 400
        height = 450
        self.setStyleSheet("background-color: #" + background_color_hex +";")

        self.create_widgets()

    def create_widgets(self):

        # Component set 3
        ###########################################################################
        # Generating and displaying profile picture for the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.pfp_label  = QLabel(self)
        self.pfp_pixmap = QPixmap()
        pfp_url = self.create_url()

        try:
            request = requests.get(pfp_url)
            avatar = request.content
            network_status = True
            self.pfp_pixmap.loadFromData(avatar)
            self.pfp_label.setPixmap(self.pfp_pixmap.scaled(30,30,Qt.KeepAspectRatio))
            self.pfp_label.setGeometry(10+ cmp_3_x_offset,10+ cmp_3_y_offset,30,30)
            welcome_txt = "Welcome,\n" + username
        except:
            self.pfp_label.setText(":(")
            self.pfp_label.setFont(QFont(app_font,25))
            self.pfp_label.setGeometry(20+ cmp_3_x_offset,8+ cmp_3_y_offset,30,30)
            welcome_txt = "OOPS!\n" + "Check your connection!"
        # --------------------------------------------------------------------------

        # Welcome label to welcome the user in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.welcome_label = QLabel(welcome_txt,self)
        self.welcome_label.setFont(QFont(app_font,12))
        self.welcome_label.setGeometry(50+ cmp_3_x_offset,0+ cmp_3_y_offset,300,50)
        # --------------------------------------------------------------------------
        ###########################################################################

    
    # Generate url for profile picture for Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def create_url(self):
        url = 'https://avatars.dicebear.com/api/bottts/' + username + '.svg?background=%23' + background_color_hex
        return url
    
    def cmp_3_visibility(self,bool):
        self.pfp_label.setHidden(bool)
        self.welcome_label.setHidden(bool)
    

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 