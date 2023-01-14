##########
# Component ID : 7
# Function : Select between multiple modes in the application

# Offset Control
#-----------------
cmp_7_x_offset = 0
cmp_7_y_offset = 0
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

        self.cmp_7_create(0,0)

    def cmp_7_create(self,cmp_7_x_offset,cmp_7_y_offset):

        # Button to select Sector Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.sector_btn = QPushButton("Sector Analysis",self)
        self.sector_btn.setGeometry(10+cmp_7_x_offset,10+ cmp_7_y_offset, 150, 20)
        self.sector_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.sector_btn.clicked.connect(self.sector_clicked)
        # --------------------------------------------------------------------------

        # Button to select Exoplanet Detection in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.detection_btn = QPushButton("Exoplanet Detection",self)
        self.detection_btn.setGeometry(10+cmp_7_x_offset, 40+ cmp_7_y_offset, 150, 20)
        self.detection_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.detection_btn.clicked.connect(self.detection_clicked)

        # Button to select False Positive Analaysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.detection_btn = QPushButton("False Positive Analysis",self)
        self.detection_btn.setGeometry(10+cmp_7_x_offset, 70+ cmp_7_y_offset, 150, 20)
        self.detection_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.detection_btn.clicked.connect(self.detection_clicked)
        
        
       
    def detection_clicked(self):
        pass

    def sector_clicked(self):
        pass

    def cmp_7_visibility(self,bool):
        self.sector_btn.setHidden(bool)
        self.detection_btn.setHidden(bool)
  

    
        

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 