##########
# Component ID : 8
# Function : Select input and button after search

# Offset Control
#-----------------
cmp_8_x_offset = 0
cmp_8_y_offset = 0
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

        self.cmp_8_create(cmp_8_x_offset,cmp_8_y_offset)
        self.cmp_8_visibility(False)

    def cmp_8_create(self,cmp_8_x_offset,cmp_8_y_offset):

        # Select from table label for target/advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.select_label = QLabel("Select from table",self)
        self.select_label.setFont(QFont(app_font,12))
        self.select_label.setStyleSheet("color: #ffffff")
        self.select_label.setGeometry(10+ cmp_8_x_offset,10+cmp_8_y_offset,100,10)
        # --------------------------------------------------------------------------

        # Select value input textbox for target/advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.select_input = QLineEdit(self)
        self.select_input.setFont(QFont(app_font,15))
        self.select_input.setPlaceholderText(" eg: 0 or 1 ")
        self.select_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.select_input.setGeometry(10+ cmp_8_x_offset,30+ cmp_8_y_offset,80,30)
        self.select_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Select button for target/advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.select_btn = QPushButton(self)
        self.select_btn.setFont(QFont(app_font,15))
        self.select_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/select.png')))
        self.select_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.select_btn.setGeometry(100+ cmp_8_x_offset,30+ cmp_8_y_offset,50,30)
        self.select_btn.clicked.connect(self.select_clicked)
        
       
    def select_clicked(self):
        pass
  
    def cmp_8_visibility(self,bool):
        self.select_label.setHidden(bool)
        self.select_btn.setHidden(bool)
        self.select_input.setHidden(bool)
    
        

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 