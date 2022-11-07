##########
# Component ID : 13
# Function : Habitability Controls

# Offset Control
#-----------------
cmp_No_x_offset = 0
cmp_No_y_offset = 0
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

# --------------------------------------------------------------------------
axhline = None
axline_val = 0
ylim_min = -2
ylim_max = 2
xlim_min = -2
xlim_max = 2
albedo = 0
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

        self.cmp_13_create()

    def cmp_13_create(self):
        # Input Parameters label in the Habitability Detection screen
        # --------------------------------------------------------------------------

        self.input_param_label = QLabel("Input Parameters",self)
        self.input_param_label.setFont(QFont(app_font))
        self.input_param_label.setStyleSheet("color: #ffffff")
        self.input_param_label.setGeometry(460,10,100,15)
        # --------------------------------------------------------------------------
        # Period label in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.period_label = QLabel("Enter Period :", self)
        self.period_label.setFont(QFont(app_font,12))
        self.period_label.setGeometry(460,30,100,30)
        # --------------------------------------------------------------------------
        # period input textbox in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.period_input = QLineEdit(self)
        self.period_input.setFont(QFont(app_font,15))
        self.period_input.setPlaceholderText("eg: 2.3467877")
        self.period_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.period_input.setGeometry(460,60,150,30)
        self.period_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------
        # Period label in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.epoch_label = QLabel("Enter Transit Epoch (t0) :", self)
        self.epoch_label.setFont(QFont(app_font,12))
        self.epoch_label.setGeometry(460,100,150,30)
        # --------------------------------------------------------------------------
        # period input textbox in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.epoch_input = QLineEdit(self)
        self.epoch_input.setFont(QFont(app_font,15))
        self.epoch_input.setPlaceholderText("eg: 170.456")
        self.epoch_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.epoch_input.setGeometry(460,130,150,30)
        self.epoch_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------
        # phase fold search button for target search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.phase_fold_btn = QPushButton("Phase Fold",self)
        self.phase_fold_btn.setFont(QFont(app_font,15))
        self.phase_fold_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.phase_fold_btn.setGeometry(484,170,100,30)
        #self.phase_fold_btn.clicked.connect(self.phase_fold)

        # ------------------------------------------------------------------------

        self.slider_label = QLabel("Adjust axhline :", self)
        self.slider_label.setFont(QFont(app_font,12))
        self.slider_label.setStyleSheet("color: #"+button_hover_hex)
        self.slider_label.setGeometry(460,210,150,30)

        self.slider = QSlider(Qt.Horizontal,self)
        self.slider.setMinimum(ylim_min*1000000)
        self.slider.setMaximum(ylim_max*1000000)
        self.slider.setSingleStep(1)
        self.slider.setGeometry(460,230,150,30)
        #self.slider.sliderMoved.connect(self.slider_position)

        self.y_label = QLabel("Adjust Y limits :", self)
        self.y_label.setFont(QFont(app_font,12))
        self.y_label.setStyleSheet("color: #"+button_hover_hex)
        self.y_label.setGeometry(460,260,150,20)

        self.y_min = QLabel("Y min :", self)
        self.y_min.setFont(QFont(app_font,12))
        self.y_min.setGeometry(460,290,150,20)

        self.y_min_input = QLineEdit(self)
        self.y_min_input.setFont(QFont(app_font,13))
        self.y_min_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.y_min_input.setGeometry(505,290,70,20)
        self.y_min_input.setAlignment(Qt.AlignCenter)

        self.y_max = QLabel("Y max :", self)
        self.y_max.setFont(QFont(app_font,12))
        self.y_max.setGeometry(460,320,150,30)

        self.y_max_input = QLineEdit(self)
        self.y_max_input.setFont(QFont(app_font,13))
        self.y_max_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.y_max_input.setGeometry(505,325,70,20)
        self.y_max_input.setAlignment(Qt.AlignCenter)

        self.y_btn = QPushButton(self)
        self.y_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/refresh.png')))
        self.y_btn.setFont(QFont(app_font,15))
        self.y_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.y_btn.setGeometry(583,297,40,40)
        #self.y_btn.clicked.connect(self.y_axis_change)


        self.x_label = QLabel("Adjust X limits :", self)
        self.x_label.setFont(QFont(app_font,12))
        self.x_label.setStyleSheet("color: #"+button_hover_hex)
        self.x_label.setGeometry(460,360,150,20)

        self.x_min = QLabel("X min :", self)
        self.x_min.setFont(QFont(app_font,12))
        self.x_min.setGeometry(460,390,150,20)

        self.x_min_input = QLineEdit(self)
        self.x_min_input.setFont(QFont(app_font,13))
        self.x_min_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.x_min_input.setGeometry(505,390,70,20)
        self.x_min_input.setAlignment(Qt.AlignCenter)

        self.x_max = QLabel("X max :", self)
        self.x_max.setFont(QFont(app_font,12))
        self.x_max.setGeometry(460,420,150,30)

        self.x_max_input = QLineEdit(self)
        self.x_max_input.setFont(QFont(app_font,13))
        self.x_max_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.x_max_input.setGeometry(505,425,70,20)
        self.x_max_input.setAlignment(Qt.AlignCenter)

        self.x_btn = QPushButton(self)
        self.x_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/refresh.png')))
        self.x_btn.setFont(QFont(app_font,15))
        self.x_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.x_btn.setGeometry(583,397,40,40)
        #self.x_btn.clicked.connect(self.x_axis_change)

        self.star_radius_label = QLabel("Input Star Radius :", self)
        self.star_radius_label.setFont(QFont(app_font,12))
        self.star_radius_label.setStyleSheet("color: #"+button_hover_hex)
        self.star_radius_label.setGeometry(460,460,150,20)

        self.star_radius_input = QLineEdit(self)
        self.star_radius_input.setFont(QFont(app_font,13))
        self.star_radius_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.star_radius_input.setGeometry(460,490,150,20)
        self.star_radius_input.setAlignment(Qt.AlignCenter)

        self.albedo_label = QLabel("Planet Albedo : 0", self)
        self.albedo_label.setFont(QFont(app_font,12))
        self.albedo_label.setStyleSheet("color: #"+button_hover_hex)
        self.albedo_label.setGeometry(630,520,200,20)

        self.albedo_slider = QSlider(Qt.Horizontal,self)
        self.albedo_slider.setMinimum(0)
        self.albedo_slider.setMaximum(100)
        self.albedo_slider.setSingleStep(1)
        self.albedo_slider.setGeometry(630,550,150,30)
        #self.albedo_slider.sliderMoved.connect(self.albedo_position)

        self.star_eff_label = QLabel("Input Star Effective Temp", self)
        self.star_eff_label.setFont(QFont(app_font,12))
        self.star_eff_label.setStyleSheet("color: #"+button_hover_hex)
        self.star_eff_label.setGeometry(460,520,150,20)

        self.star_eff_input = QLineEdit(self)
        self.star_eff_input.setFont(QFont(app_font,13))
        self.star_eff_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.star_eff_input.setGeometry(460,550,150,20)
        self.star_eff_input.setAlignment(Qt.AlignCenter)

        self.calc_radius_btn = QPushButton('Generate Results',self)
        self.calc_radius_btn.setFont(QFont(app_font,15))
        self.calc_radius_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.calc_radius_btn.setGeometry(460,590,320,30)
        #self.calc_radius_btn.clicked.connect(self.calc_radius)

        self.summary_label = QLabel("-- Summary --", self)
        self.summary_label.setFont(QFont(app_font,13))
        self.summary_label.setStyleSheet("color: #"+button_hover_hex)
        self.summary_label.setGeometry(810,460,150,20)

        self.summary_period_label = QLabel("Period : Not Set", self)
        self.summary_period_label.setFont(QFont(app_font,12))
        self.summary_period_label.setGeometry(810,525-40,150,20)

        self.summary_epoch_label = QLabel("Transit Epoch (t0) : Not Set", self)
        self.summary_epoch_label.setFont(QFont(app_font,12))
        self.summary_epoch_label.setGeometry(810,545-40,150,20)

        self.summary_axhline_label = QLabel("Transit Depth (1 - Axhline) : 1", self)
        self.summary_axhline_label.setFont(QFont(app_font,12))
        self.summary_axhline_label.setGeometry(810,565-40,240,20)

        self.summary_star_radius_label = QLabel("Star Radius : Not Set", self)
        self.summary_star_radius_label.setFont(QFont(app_font,12))
        self.summary_star_radius_label.setGeometry(810,585-40,150,20)

        self.summary_star_temp_label = QLabel("Star Eff Temp : Not Set", self)
        self.summary_star_temp_label.setFont(QFont(app_font,12))
        self.summary_star_temp_label.setGeometry(810,605-40,150,20)

        self.summary_planet_albedo_label = QLabel("Planet Albedo : Not Set", self)
        self.summary_planet_albedo_label.setFont(QFont(app_font,12))
        self.summary_planet_albedo_label.setGeometry(810,625-40,150,20)

        self.results_label = QLabel("-- Results --", self)
        self.results_label.setFont(QFont(app_font,13))
        self.results_label.setStyleSheet("color: #"+button_hover_hex)
        self.results_label.setGeometry(1020,520-60,150,20)

        self.results_solar_label = QLabel("Radius as Solar Radius : Not Calculated ", self)
        self.results_solar_label.setFont(QFont(app_font,12))
        self.results_solar_label.setGeometry(1020,545-60,350,20)

        self.results_earth_label = QLabel("Radius as Earth Radius : Not Calculated", self)
        self.results_earth_label.setFont(QFont(app_font,12))
        self.results_earth_label.setGeometry(1020,565-60,350,20)

        self.results_axis_label = QLabel("Orbit Semi Major Axis as Solar Radius: Not Calculated", self)
        self.results_axis_label.setFont(QFont(app_font,12))
        self.results_axis_label.setGeometry(1020,585-60,350,20)

        self.results_axis_earth_label = QLabel("Orbit Semi Major Axis as Earth Radius: Not Calculated", self)
        self.results_axis_earth_label.setFont(QFont(app_font,12))
        self.results_axis_earth_label.setGeometry(1020,605-60,350,20)

        self.results_temp_label = QLabel("Equilibrium Temperature : Not Calculated", self)
        self.results_temp_label.setFont(QFont(app_font,12))
        self.results_temp_label.setGeometry(1020,625-60,350,20)
        
       

  

    
        

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 