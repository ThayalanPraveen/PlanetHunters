##########
# Component ID : 11
# Function : Display logout button

# Offset Control
#-----------------
cmp_11_x_offset = 0
cmp_11_y_offset = 0
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

        self.cmp_11_create(cmp_11_x_offset,cmp_11_y_offset)

    def cmp_11_create(self,cmp_11_x_offset,cmp_11_y_offset):
        # Logout button to go to login screen from Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.lgout_btn = QPushButton(self)
        self.lgout_btn.setFont(QFont(app_font,15))
        self.lgout_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/logout.png')))
        self.lgout_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + logout_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.lgout_btn.setGeometry(10 + cmp_11_x_offset ,10 + cmp_11_y_offset,30,30) #410
        self.lgout_btn.clicked.connect(self.login_click)
        # --------------------------------------------------------------------------
        
    def login_click(self):
        pass

    def cmp_11_visibility(self,bool):
        self.lgout_btn.setHidden(bool)

  

    
        

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 