##########################################################################
# Component ID : 5
# Function : Display advanced search controls

# Offset Control
#-----------------
cmp_5_x_offset = 0
cmp_5_y_offset = 0
#-----------------

###########################################################################


# Imports, variables and themes of components
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
class ScrollLabel(QScrollArea):
 
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
 
        # making widget resizable
        self.setWidgetResizable(True)
 
        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)
 
        # vertical box layout
        lay = QVBoxLayout(content)
 
        # creating label
        self.label = QLabel(content)

        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
 
        # making label multi-line
        self.label.setWordWrap(True)
 
        # adding label to the layout
        lay.addWidget(self.label)
 
    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)

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

        self.cmp_5_create()
        self.cmp_5_visibility(False)
    
    def cmp_5_create(self):
        # Advanced search dropdown box in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.adv_select_comboBox = QComboBox(self)
        self.adv_select_comboBox.setGeometry(10+cmp_5_x_offset,10+cmp_5_y_offset,150,18)
        self.adv_select_comboBox.addItems(['calib_level',"objID","obsid","sequence_number","distance","em_max","em_min",
                                    "s_ra","srcDen","t_exptime","t_max","t_min","mtFlag","dataRights",
                                    "dataURL","dataproduct_type","filters","instrument_name","intentType",
                                    "jpegURL","obs_collection","obs_id","obs_title","project",
                                    "proposal_id","proposal_pi","proposal_type","provenance_name",
                                    "s_region","target_classification","target_name","wavelength_region"
                                    ])
        self.adv_select_comboBox.setStyleSheet("""
                                QComboBox {
                                    border: 1px solid gray;
                                    border-radius: 3px;
                                    padding: 1px 18px 1px 3px;
                                    min-width: 6em;
                                }
                                """)
        self.adv_select_comboBox.activated.connect(self.adv_search_parameter_select_clicked)
        # --------------------------------------------------------------------------

        # Advanced search hyperlink for parameters description in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.adv_search_learn_more_label = QLabel(self)
        self.adv_search_learn_more_label.setText('''<a href='https://mast.stsci.edu/api/v0/_c_a_o_mfields.html'>Learn more about these parameters here</a>''')
        self.adv_search_learn_more_label.openExternalLinks()
        self.adv_search_learn_more_label.setOpenExternalLinks(True)
        self.adv_search_learn_more_label.setGeometry(170+cmp_5_x_offset,10+cmp_5_y_offset,300,18)
        # --------------------------------------------------------------------------

        # Advanced search parameter input value in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.adv_search_input = QLineEdit(self)
        self.adv_search_input.setFont(QFont(app_font,15))
        self.adv_search_input.setPlaceholderText("Enter value")
        self.adv_search_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.adv_search_input.setGeometry(10+cmp_5_x_offset,35+cmp_5_y_offset,350,30)
        self.adv_search_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Add button for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.add_advanced_search_btn = QPushButton(self)
        self.add_advanced_search_btn.setFont(QFont(app_font,15))
        self.add_advanced_search_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/add.png')))
        self.add_advanced_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.add_advanced_search_btn.setGeometry(370+cmp_5_x_offset,35+cmp_5_y_offset,30,30)
        self.add_advanced_search_btn.clicked.connect(self.adv_search_add_clicked)
        # --------------------------------------------------------------------------

        # Undo button for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.undo_advanced_search_btn = QPushButton(self)
        self.undo_advanced_search_btn.setFont(QFont(app_font,15))
        self.undo_advanced_search_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/undo.png')))
        self.undo_advanced_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.undo_advanced_search_btn.setGeometry(10+cmp_5_x_offset,75+cmp_5_y_offset,30,30)
        self.undo_advanced_search_btn.clicked.connect(self.adv_search_undo_clicked)
        # --------------------------------------------------------------------------

        # Clear button for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.clear_advanced_search_btn = QPushButton(self)
        self.clear_advanced_search_btn.setFont(QFont(app_font,15))
        self.clear_advanced_search_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/clear.png')))
        self.clear_advanced_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.clear_advanced_search_btn.setGeometry(50+cmp_5_x_offset,75+cmp_5_y_offset,30,30)
        # --------------------------------------------------------------------------

        # Parameters input validation for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.parameter_validation_label = QLabel("Add parameters and search, undo or clear.\nselected parameters are displayed below",self)
        self.parameter_validation_label.setGeometry(10+cmp_5_x_offset,135+cmp_5_y_offset,400,30)
        self.parameter_validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
        # --------------------------------------------------------------------------
        
        # Selected parameters label for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.selected_parameters_label = QLabel("Selected Parameters: ",self)
        self.selected_parameters_label.setGeometry(10+cmp_5_x_offset,175+cmp_5_y_offset,200,10)
        # --------------------------------------------------------------------------

        # Scrollable text field for selected parameters for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.adv_selected_paramters_scrollLabel = ScrollLabel(self)
        self.adv_selected_paramters_scrollLabel.setGeometry(10+cmp_5_x_offset,175+cmp_5_y_offset,400,100)
        # --------------------------------------------------------------------------

        # Search results label for advaned search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.search_results_selected_parameters_label = QLabel("Search results: ",self)
        self.search_results_selected_parameters_label.setGeometry(10+cmp_5_x_offset,305+cmp_5_y_offset,200,10)
        # --------------------------------------------------------------------------

         
        # Target search button for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_screen_btn = QPushButton("Back To Target Search",self)
        self.target_screen_btn.setFont(QFont(app_font,15))
        self.target_screen_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.target_screen_btn.setGeometry(240+cmp_5_x_offset,75+cmp_5_y_offset,200,30)
        self.target_screen_btn.clicked.connect(self.target_screen_clicked)
    
    def adv_search_parameter_select_clicked(self):
        pass

    def adv_search_add_clicked(self):
        pass

    def adv_search_undo_clicked(self):
        pass

    def target_screen_clicked(self):
        pass

    def cmp_5_visibility(self,bool):
        self.selected_parameters_label.setHidden(bool)
        self.parameter_validation_label.setHidden(bool)
        self.search_results_selected_parameters_label.setHidden(bool)
        self.adv_search_learn_more_label.setHidden(bool)
        self.adv_search_input.setHidden(bool)
        self.target_screen_btn.setHidden(bool)
        self.add_advanced_search_btn.setHidden(bool)
        self.undo_advanced_search_btn.setHidden(bool)
        self.clear_advanced_search_btn.setHidden(bool)
        self.adv_select_comboBox.setHidden(bool)
        self.adv_selected_paramters_scrollLabel.setHidden(bool)

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 