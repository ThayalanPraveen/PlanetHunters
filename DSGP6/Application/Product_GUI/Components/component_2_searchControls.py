##########
# Component ID : 2
# Function : Contains controls for searching targets

# Offset Control
#-----------------
cmp_2_x_offset = 0
cmp_2_y_offset = 0
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
        global width,height
        width = 400
        height = 450
        self.setStyleSheet("background-color: #" + background_color_hex +";")

        self.cmp_2_create()
    
    def cmp_2_create(self):
        # Components set 2

        # Target search / Advanced search label in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.search_label = QLabel("Target search",self)
        self.search_label.setFont(QFont(app_font))
        self.search_label.setStyleSheet("color: #ffffff")
        self.search_label.setGeometry(10+cmp_2_x_offset,10+cmp_2_y_offset,200,15)
        # --------------------------------------------------------------------------

        # Target search support label in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_label = QLabel("Enter Target ID :", self)
        self.target_label.setFont(QFont(app_font,12))
        self.target_label.setGeometry(10+cmp_2_x_offset,25+cmp_2_y_offset,200,30)
        # --------------------------------------------------------------------------

        # Target ID input textbox in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_search_input = QLineEdit(self)
        self.target_search_input.setFont(QFont(app_font,15))
        self.target_search_input.setPlaceholderText("eg: TIC 42173628")
        self.target_search_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.target_search_input.setGeometry(10+cmp_2_x_offset,55+cmp_2_y_offset,150,30)
        self.target_search_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # mission select dropdown box in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        # self.mission_comboBox = QComboBox(self)
        # self.mission_comboBox.setGeometry(220+cmp_2_x_offset,55+cmp_2_y_offset,50,30)
        # self.mission_comboBox.addItems(['All','Kepler','K2','TESS'
        #                             ])
        # self.mission_comboBox.setStyleSheet("""
        #                         QComboBox {
        #                             border: 3px solid gray;
        #                             border-radius: 5px;
        #                             padding: 1px 18px 1px 3px;
        #                             min-width: 4em;
        #                         }
        #                         """)
        # --------------------------------------------------------------------------

        # Search button for target search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_search_btn = QPushButton(self)
        self.target_search_btn.setFont(QFont(app_font,15))
        self.target_search_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/refresh.png')))
        self.target_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.target_search_btn.setGeometry(165+cmp_2_x_offset,55+cmp_2_y_offset,50,30)
        self.target_search_btn.clicked.connect(self.search_clicked)
        # --------------------------------------------------------------------------

        # Search button for target search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_search_btn = QPushButton(self)
        self.target_search_btn.setFont(QFont(app_font,15))
        self.target_search_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/search.png')))
        self.target_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.target_search_btn.setGeometry(220+cmp_2_x_offset,55+cmp_2_y_offset,50,30)
        self.target_search_btn.clicked.connect(self.search_clicked)
        # --------------------------------------------------------------------------

        # Advanced search button for target search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.advanced_search_btn = QPushButton("Filter Search",self)
        self.advanced_search_btn.setFont(QFont(app_font,15))
        self.advanced_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.advanced_search_btn.setGeometry(275+cmp_2_x_offset,55+cmp_2_y_offset,120,30)
        self.advanced_search_btn.clicked.connect(self.adv_clicked)


        # progress_bar_exo_detection in Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.search_progressBar = QProgressBar(self)
        self.search_progressBar.setGeometry(10+cmp_2_x_offset,105+cmp_2_y_offset,150,10)
        self.search_progressBar.setMaximum(0)
        self.search_progressBar.setMinimum(0)
        self.search_progressBar.setHidden(False)
        # --------------------------------------------------------------------------

        # Validation label for the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.validation_label = QLabel("Enter target id and start hunting!",self)
        self.validation_label.setGeometry(10+cmp_2_x_offset,105+cmp_2_y_offset,300,30)
        self.validation_label.setStyleSheet("color:#" + button_hover_hex + ";")
    

    # Component set 2
    # Search button click function for target search in the Exo-Planet Detection screen
    #---------------------------------------------------------------------------    
    def search_clicked(self):
        pass
    #---------------------------------------------------------------------------

    def adv_clicked(self):
        pass
    
    # Component set 2 visibility function
    #---------------------------------------------------------------------------
    def cmp_2_visibility(self,bool):
        self.search_label.setHidden(bool)
        self.target_label.setHidden(bool)
        self.validation_label.setHidden(bool)
        self.target_search_btn.setHidden(bool)
        self.search_progressBar.setHidden(bool)
        self.mission_comboBox.setHidden(bool)
        self.target_search_input.setHidden(bool)
        self.advanced_search_btn.setHidden(bool)
    #---------------------------------------------------------------------------
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 