##########
# Component ID : 1
# Function : Contains controls selectable for Sector Analysis in Exo-Planet Detection

# Offset Control
#-----------------
cmp_1_x_offset = 0
cmp_1_y_offset = 0
#-----------------
##########


# Imports and themes of components
###########################################################################

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

        self.cmp_1_create()

    def cmp_1_create(self):

        # Components set 1
        # Label to show "Plot Light Curve" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------        
        self.lightcurve_label = QLabel("Plot Light Curve" , self)
        self.lightcurve_label.setGeometry(10 + cmp_1_x_offset, 10+ cmp_1_y_offset, 150, 20)
        self.lightcurve_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Normalize checkbox 
        # --------------------------------------------------------------------------
        self.normalize_check = QCheckBox("Normalize", self)
        self.normalize_check.setGeometry(10+ cmp_1_x_offset, 40+ cmp_1_y_offset, 130, 20)
        # --------------------------------------------------------------------------

        # Button for Light Curve Plot in BLS Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.lightcurve_plot_btn = QPushButton("Light Curve Plot",self)
        self.lightcurve_plot_btn.setGeometry(10+ cmp_1_x_offset, 70+ cmp_1_y_offset, 130, 20)
        self.lightcurve_plot_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        #self.lightcurve_plot_btn.clicked.connect(self.bls_btn_clicked)
        # --------------------------------------------------------------------------
        
        # Label to show "Fold Light Curve" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------        
        self.fold_label = QLabel("Fold Light Curve : BLS" , self)
        self.fold_label.setGeometry(10 + cmp_1_x_offset, 100+ cmp_1_y_offset, 150, 20)
        self.fold_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Period label
        # --------------------------------------------------------------------------
        self.period_label = QLabel("Period : 1 to " , self)
        self.period_label.setGeometry(10+ cmp_1_x_offset, 130+ cmp_1_y_offset, 200, 20)
        self.period_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Input value for period in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.period_input = QLineEdit(self)
        self.period_input.setFont(QFont(app_font,15))
        self.period_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.period_input.setGeometry(90+ cmp_1_x_offset,130+ cmp_1_y_offset,50,20)
        self.period_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Button for Folded Plot in Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.folded_plot_btn = QPushButton("Folded Plot",self)
        self.folded_plot_btn.setGeometry(10+ cmp_1_x_offset, 160+ cmp_1_y_offset, 130, 20)
        self.folded_plot_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        #self.lightcurve_plot_btn.clicked.connect(self.bls_btn_clicked)
        # --------------------------------------------------------------------------

        # Label to show "Plot Flattened Curve" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------        
        self.flattened_label = QLabel("Plot Flattened Curve" , self)
        self.flattened_label.setGeometry(170+ cmp_1_x_offset, 10+ cmp_1_y_offset, 150, 20)
        self.flattened_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Window Length label
        # --------------------------------------------------------------------------
        self.window_length_label = QLabel("Window Length : " , self)
        self.window_length_label.setGeometry(170+ cmp_1_x_offset, 40+ cmp_1_y_offset, 200, 20)
        self.window_length_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Input value for window length in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.window_length_input = QLineEdit(self)
        self.window_length_input.setFont(QFont(app_font,15))
        self.window_length_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.window_length_input.setGeometry(275+ cmp_1_x_offset,40+ cmp_1_y_offset,50,20)
        self.window_length_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Poly order label
        # --------------------------------------------------------------------------
        self.poly_order_label = QLabel("Poly Order : " , self)
        self.poly_order_label.setGeometry(170+ cmp_1_x_offset, 70+ cmp_1_y_offset, 200, 20)
        self.poly_order_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Input value for poly order in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.poly_order_input = QLineEdit(self)
        self.poly_order_input.setFont(QFont(app_font,15))
        self.poly_order_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.poly_order_input.setGeometry(275+ cmp_1_x_offset,70+ cmp_1_y_offset,50,20)
        self.poly_order_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Niters label
        # --------------------------------------------------------------------------
        self.niters_label = QLabel("Niters : " , self)
        self.niters_label.setGeometry(170+ cmp_1_x_offset, 100+ cmp_1_y_offset, 200, 20)
        self.niters_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Input value for niters in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.niters_input = QLineEdit(self)
        self.niters_input.setFont(QFont(app_font,15))
        self.niters_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.niters_input.setGeometry(275+ cmp_1_x_offset,100+ cmp_1_y_offset,50,20)
        self.niters_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Sigma label
        # --------------------------------------------------------------------------
        self.sigma_label = QLabel("Sigma : " , self)
        self.sigma_label.setGeometry(170+ cmp_1_x_offset, 130+ cmp_1_y_offset, 200, 20)
        self.sigma_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Input value for sigma in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.sigma_input = QLineEdit(self)
        self.sigma_input.setFont(QFont(app_font,15))
        self.sigma_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.sigma_input.setGeometry(275+ cmp_1_x_offset,130+ cmp_1_y_offset,50,20)
        self.sigma_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Button for Flattened Curve Plot in BLS Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.flattened_plot_btn = QPushButton("Flattened Plot",self)
        self.flattened_plot_btn.setGeometry(170+ cmp_1_x_offset, 160+ cmp_1_y_offset, 130, 20)
        self.flattened_plot_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        #self.flattened_plot_btn.clicked.connect(self.bls_btn_clicked)
        # --------------------------------------------------------------------------

        # Label to show "Plot Folded Curve" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------        
        self.folded_label = QLabel("Plot Binned Curve" , self)
        self.folded_label.setGeometry(350+ cmp_1_x_offset, 10+ cmp_1_y_offset, 150, 20)
        self.folded_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # N Bins label
        # --------------------------------------------------------------------------        
        self.n_bins_label = QLabel("N Bins : " , self)
        self.n_bins_label.setGeometry(350+ cmp_1_x_offset, 40+ cmp_1_y_offset, 200, 20)
        self.n_bins_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Input value for n bins in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.n_bins_input = QLineEdit(self)
        self.n_bins_input.setFont(QFont(app_font,15))
        self.n_bins_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.n_bins_input.setGeometry(455+ cmp_1_x_offset,40+ cmp_1_y_offset,50,20)
        self.n_bins_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Bins label
        # --------------------------------------------------------------------------

        self.bins_label = QLabel("Bins : " , self)
        self.bins_label.setGeometry(350+ cmp_1_x_offset, 70+ cmp_1_y_offset, 200, 20)
        self.bins_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------



        # Input value for bins in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.bins_input = QLineEdit(self)
        self.bins_input.setFont(QFont(app_font,15))
        self.bins_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.bins_input.setGeometry(455+ cmp_1_x_offset,70+ cmp_1_y_offset,50,20)
        self.bins_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------
        # --------------------------------------------------------------------------
        self.binned_plot_btn = QPushButton("Binned Plot",self)
        self.binned_plot_btn.setGeometry(350+ cmp_1_x_offset, 100 + cmp_1_y_offset, 130, 20)
        self.binned_plot_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
       

    # Component set 1
    def cmp_1_visibility(self,bool):
        self.bins_label.setHidden(bool)
        self.sigma_label.setHidden(bool)
        self.folded_label.setHidden(bool)
        self.n_bins_label.setHidden(bool)
        self.niters_label.setHidden(bool)
        self.flattened_label.setHidden(bool)
        self.poly_order_label.setHidden(bool)
        self.lightcurve_label.setHidden(bool)
        self.window_length_label.setHidden(bool)
        self.binned_plot_btn.setHidden(bool)
        self.flattened_plot_btn.setHidden(bool)
        self.lightcurve_plot_btn.setHidden(bool)
        self.bins_input.setHidden(bool)
        self.n_bins_input.setHidden(bool)
        self.normalize_check.setHidden(bool)
        self.bins_input.setHidden(bool)
        self.sigma_input.setHidden(bool)
        self.n_bins_input.setHidden(bool)
        self.niters_input.setHidden(bool)
        self.poly_order_input.setHidden(bool)
        self.window_length_input.setHidden(bool)

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 