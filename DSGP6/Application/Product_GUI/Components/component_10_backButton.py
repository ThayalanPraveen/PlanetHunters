##########
# Component ID : 10
# Function : display back button

# Offset Control
#-----------------
cmp_10_x_offset = 0
cmp_10_y_offset = 0
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
        self.cmp_10_create()

    def cmp_10_create(self,cmp_10_x_offset,cmp_10_y_offset):
        # Back button to go to Select screen from the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.back_btn = QPushButton(self)
        self.back_btn.setFont(QFont(app_font,15))
        self.back_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/back.png')))
        self.back_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_alt_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.back_btn.setGeometry(10 + cmp_10_x_offset,10 + cmp_10_y_offset,30,30)
        self.back_btn.clicked.connect(self.back_click)
        # --------------------------------------------------------------------------
        
    def back_click(self):
        pass

    def cmp_10_visibility(self,bool):
        self.back_btn.setHidden(bool)
  

    
        

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 