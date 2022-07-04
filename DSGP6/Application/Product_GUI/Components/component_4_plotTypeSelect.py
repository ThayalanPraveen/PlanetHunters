##########################################################################
# Component ID : 4
# Function : Display different plot types to select from

# Offset Control
#-----------------
cmp_4_x_offset = 0
cmp_4_y_offset = 0
#-----------------

###########################################################################


# Imports, variables and themes of components
###########################################################################

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys



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

        self.cmp_4_create()
        self.cmp_4_visibility(True)

    def cmp_4_create(self):

        # Component set 4
        # Label to show "Select line type" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.line_type_label = QLabel("Select line type" , self)
        self.line_type_label.setGeometry(10 + cmp_4_x_offset, 10 + cmp_4_y_offset, 150, 20)
        self.line_type_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Radio button to select line type as Line in Exo-Detection Screen 
        # --------------------------------------------------------------------------
        self.line_radioBtn = QRadioButton("Line", self)
        self.line_radioBtn.setGeometry(10+ cmp_4_x_offset,45+ cmp_4_y_offset, 100, 20)
        self.line_radioBtn.setChecked(True)
        self.line_radioBtn.toggled.connect(self.switch_plot_radio_clicked)
        # --------------------------------------------------------------------------
        
        # Radio button to select line type as Scatter in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.scatter_radioBtn = QRadioButton("Scatter", self)
        self.scatter_radioBtn.setGeometry(10+ cmp_4_x_offset, 75+ cmp_4_y_offset, 100, 20)
        self.scatter_radioBtn.toggled.connect(self.switch_plot_radio_clicked)
        # --------------------------------------------------------------------------

        # Radio button to select line type as Errorbar in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.error_radioBtn = QRadioButton("Error Bar", self)
        self.error_radioBtn.setGeometry(10+ cmp_4_x_offset, 105+ cmp_4_y_offset, 100, 20)
        #self.river_btn.setEnabled(False)
        self.error_radioBtn.toggled.connect(self.switch_plot_radio_clicked)
        
    # Component set 4
    # Switch plot according to selected radio button  
    def switch_plot_radio_clicked(self):   
        pass
    
    def cmp_4_visibility(self,bool):
        self.line_type_label.setHidden(bool)
        self.line_radioBtn.setHidden(bool)
        self.error_radioBtn.setHidden(bool)
        self.scatter_radioBtn.setHidden(bool)
     
    

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 