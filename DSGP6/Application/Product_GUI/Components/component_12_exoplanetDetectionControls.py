##########
# Component ID : 12
# Function : Display Exoplanet Detection Controls

# Offset Control
#-----------------
cmp_12_x_offset = 0
cmp_12_y_offset = 0
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

        self.cmp_12_create(0,0)

    def cmp_12_create(self,cmp_12_x_offset,cmp_12_y_offset):
        
        # Label to show "BLS Analysis" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bls_label = QLabel("BLS Analysis" , self)
        self.bls_label.setGeometry(920+ cmp_12_x_offset, 500+ cmp_12_y_offset, 150, 20)
        self.bls_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Label to show "Period" for BLS Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bls_period_label = QLabel("Period :" , self)
        self.bls_period_label.setGeometry(920+ cmp_12_x_offset, 535+ cmp_12_y_offset, 150, 20)
        self.bls_period_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Inout for "Period" for BLS Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bls_period_input = QLineEdit(self)
        self.bls_period_input.setGeometry(970+ cmp_12_x_offset, 535+ cmp_12_y_offset, 50, 20)
        self.bls_period_input.setText("20")
        # --------------------------------------------------------------------------

        # Label to show "Frequency Factor :" for BLS Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bls_freq_label = QLabel("Frequency Factor :" , self)
        self.bls_freq_label.setGeometry(920+ cmp_12_x_offset, 565+ cmp_12_y_offset, 150, 20)
        self.bls_freq_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Inout for "Frequency Factor" for BLS Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bls_freq_input = QLineEdit(self)
        self.bls_freq_input.setGeometry(1035+ cmp_12_x_offset, 565+ cmp_12_y_offset, 30, 20)
        self.bls_freq_input.setText("500")
        # --------------------------------------------------------------------------

        # Button for BLS Plot in BLS Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bls_plot_btn = QPushButton("BLS Plot",self)
        self.bls_plot_btn.setGeometry(920+ cmp_12_x_offset, 595+ cmp_12_y_offset, 150, 20)
        self.bls_plot_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        #self.bls_plot_btn.clicked.connect(self.bls_btn_clicked)
        # --------------------------------------------------------------------------
        
        # Label for "BLS Planet Results" for BLS Results in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bls_label = QLabel("BLS Planet Results" , self)
        self.bls_label.setGeometry(1080+ cmp_12_x_offset, 500+ cmp_12_y_offset, 150, 20)
        self.bls_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Label for "Period : Requires BLS" for BLS Results in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bls_results_period_label = QLabel("Period : Requires BLS" , self)
        self.bls_results_period_label.setGeometry(1080+ cmp_12_x_offset, 535+ cmp_12_y_offset, 200, 20)
        self.bls_results_period_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Label for Tranist Time : Requires BLS" for BLS Results in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bls_results_transit_label = QLabel("Tranist Time : Requires BLS" , self)
        self.bls_results_transit_label.setGeometry(1080+ cmp_12_x_offset, 565+ cmp_12_y_offset, 200, 20)
        self.bls_results_transit_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------
        
        # Label for "Duration : Requires BLS" for BLS Results in Exo-Detection Screen 
        # --------------------------------------------------------------------------
        self.bls_results_duration_label = QLabel("Duration : Requires BLS" , self)
        self.bls_results_duration_label.setGeometry(1080+ cmp_12_x_offset, 595+ cmp_12_y_offset, 200, 20)
        self.bls_results_duration_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Button for phase folded graph from BLS Results in Exo-Detection Screen 
        # --------------------------------------------------------------------------
        self.bls_fold_plot_btn = QPushButton("BLS Phase Fold",self)
        self.bls_fold_plot_btn.setGeometry(920+ cmp_12_x_offset, 635+ cmp_12_y_offset, 150, 20)
        self.bls_fold_plot_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        #self.bls_fold_plot_btn.clicked.connect(self.bls_fold_plot_btn_clicked)
        self.bls_fold_plot_btn.setEnabled(False)

        # Button for ML Prediction in Exo-Detection Screen 
        # --------------------------------------------------------------------------
        self.ml_btn = QPushButton("Predict with ML",self)
        self.ml_btn.setGeometry(1230, 500, 150, 20)
        self.ml_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.ml_btn.setEnabled(False)
        #self.ml_btn.clicked.connect(self.ml_predict)

        self.ml_label = QLabel(self)
        self.ml_label.setGeometry(1080, 530, 300, 50)
        self.ml_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------
        
    def cmp_12_visibility(self,bool):
        self.bls_label.setHidden(bool)
        self.bls_period_label.setHidden(bool)
        self.bls_fold_plot_btn.setHidden(bool)
        self.bls_freq_input.setHidden(bool)
        self.bls_freq_label.setHidden(bool)
        self.bls_period_input.setHidden(bool)
        self.bls_plot_btn.setHidden(bool)
        self.bls_results_duration_label.setHidden(bool)
        self.bls_results_period_label.setHidden(bool)
        self.bls_results_transit_label.setHidden(bool)
        self.ml_btn.setHidden(bool)

  

    
        

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 