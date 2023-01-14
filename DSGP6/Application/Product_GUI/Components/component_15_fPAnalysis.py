##########
# Component ID : 7
# Function : Select between multiple modes in the application

# Offset Control
#-----------------
cmp_15_x_offset = 0
cmp_15_y_offset = 0
#-----------------
##########


# Imports and themes of components
###########################################################################

import PySide6
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
import os

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

        self.cmp_15_create(0,0)

    def cmp_15_create(self,cmp_7_x_offset,cmp_7_y_offset):

        # Button to select Sector Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.tpImage_btn = QPushButton("Plot TP Image",self)
        self.tpImage_btn.setGeometry(10+cmp_7_x_offset,10+ cmp_7_y_offset, 150, 20)
        self.tpImage_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.tpImage_btn.clicked.connect(self.sector_clicked)
        # --------------------------------------------------------------------------

        # Button to select Exoplanet Detection in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.lc_btn = QPushButton("Plot Light Curve",self)
        self.lc_btn.setGeometry(170+cmp_7_x_offset, 10+ cmp_7_y_offset, 150, 20)
        self.lc_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.lc_btn.clicked.connect(self.detection_clicked)

        # Button to select False Positive Analaysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bf_btn = QPushButton("Background Flux",self)
        self.bf_btn.setGeometry(330+cmp_7_x_offset, 10+ cmp_7_y_offset, 150, 20)
        self.bf_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.bf_btn.clicked.connect(self.detection_clicked)

        # Button to select False Positive Analaysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bft_btn = QPushButton("Background Flux At Transit",self)
        self.bft_btn.setGeometry(490+cmp_7_x_offset, 10+ cmp_7_y_offset, 170, 20)
        self.bft_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.bft_btn.clicked.connect(self.detection_clicked)
        
    def detection_clicked(self):
        pass

    def cmp_15_visibility(self,bool):
        self.bf_btn.setHidden(bool)
        self.bft_btn.setHidden(bool)
        self.tpImage_btn.setHidden(bool)
        self.lc_btn.setHidden(bool)
  

    
        

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 