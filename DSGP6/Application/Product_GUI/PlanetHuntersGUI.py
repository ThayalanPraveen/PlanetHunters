import time
import PySide6
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import json
from matplotlib import use
import pandas as pd
import os
import joblib
import lightkurve as lk
import matplotlib.pyplot
import numpy as np
import matplotlib.pyplot as plt
import requests
import firebase_admin
from firebase_admin import db
import sys
import firebase_admin
from firebase_admin import credentials
from cryptography.fernet import Fernet
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

# Credentitials for firebase authentication
# --------------------------------------------------------------------------
cred = credentials.Certificate(os.path.join(sys.path[0],'planet-hunters-1b294-firebase-adminsdk-ksboi-00cff64782.json'))
# --------------------------------------------------------------------------

# Initialize firebase database with cred file
# --------------------------------------------------------------------------
firebase_admin.initialize_app(cred , {
    'databaseURL': 'https://planet-hunters-1b294-default-rtdb.firebaseio.com'
})
# --------------------------------------------------------------------------

# API key to use google services to login and signup
# --------------------------------------------------------------------------
apikey='AIzaSyAqvXwzaDvA3F3xkhHzbAGWmswYu5NDAds'# the web api key
# --------------------------------------------------------------------------

# Used to send and recievce target search results info from multi threading process
# --------------------------------------------------------------------------
target_search_result_scrollable_label = None
target_search_result = None
target_search_id = None
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
advanced_search_results = None
# --------------------------------------------------------------------------

# Used to send and recieve sign in info from multi threading process
# --------------------------------------------------------------------------
sign_up = False
signup_email_id = None
signup_error_msg = ""
signup_success = False
# --------------------------------------------------------------------------

# Used to store the load and store account profile picture 
# --------------------------------------------------------------------------
avatar = None
pfp_load = False
network_status = False
# --------------------------------------------------------------------------

# Used to change window dimensions
# --------------------------------------------------------------------------
width = 0
height = 0
# --------------------------------------------------------------------------

# Used to add data to the database 
# --------------------------------------------------------------------------
username = ""
db_username = ""
# --------------------------------------------------------------------------

# Used to check if login or signup request has failed
# --------------------------------------------------------------------------
login_network_fail = False
signup_network_fail = False
# --------------------------------------------------------------------------

# Used to check if there were any problems while downloading lightcurves
# --------------------------------------------------------------------------
search_result_isDownloaded_error = True
search_result_select_isDownloaded_error = True
# --------------------------------------------------------------------------

# Store the downloaded lightcurve from the multi-thread process
# --------------------------------------------------------------------------
lightcurve = None
# --------------------------------------------------------------------------

# Worker class for multi threading
# --------------------------------------------------------------------------
class Worker(QObject):
    finished = Signal()
    progress = Signal(int)
    # Light curve download multi-threading process
    # --------------------------------------------------------------------------
    def download_lightcurve(self):
        global lightcurve
        global select_input
        global target_search_result
        global search_result_select_isDownloaded_error
        try:
            lightcurve = target_search_result[int(select_input)].download()
            search_result_select_isDownloaded_error = False
            self.finished.emit()
        except:
            search_result_select_isDownloaded_error = True
            self.finished.emit()
    # --------------------------------------------------------------------------

    # Light curve search download multi-threading process
    # --------------------------------------------------------------------------
    def dowload_search_results(self):
        global target_search_result
        global search_result_isDownloaded_error
        try:
            target_search_result = lk.search_lightcurve(target_search_id)
            search_result_isDownloaded_error = False
            self.finished.emit()
        except:
            search_result_isDownloaded_error = True
            self.finished.emit()
    # --------------------------------------------------------------------------

    # Login multi-threading process
    # --------------------------------------------------------------------------
    def login(self):
        global payload
        global r
        global login_success
        global login_network_fail

        login_network_fail = False
        try:
            r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword',
                                params={"key": apikey},
                                data=payload)
            login_network_fail = True
            self.finished.emit()
        except:
            self.finished.emit()
    # --------------------------------------------------------------------------
    
    # Signup multi-threading process
    # --------------------------------------------------------------------------
    def signup(self):
        global signup_error_msg
        global signup_email_id
        global sign_up
        global r
        global details
        global signup_success
        global signup_network_fail

        signup_success = False
        signup_network_fail = False
        try: 
            # send post request
            r=requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={}'.format(apikey),data=details)

            #check for errors in result
            if 'error' in r.json().keys():
                authenticate =  {'status':'error','message':r.json()['error']['message']}
                signup_error_msg = authenticate["message"][:43] + "\n" +  authenticate["message"][44:]
            #if the registration succeeded
            if 'idToken' in r.json().keys() :
                signup_success = True
                authenticate =  {'status':'success','idToken':r.json()['idToken']}

            # Add new user to the database in signup screen
            # --------------------------------------------------------------------------
            if authenticate['status'] == 'success' :
                sign_up = True
                mail_id = signup_email_id
                mail_id = mail_id.replace("@","")
                mail_id = mail_id.replace(".","")
                ref = db.reference('/users')
                ref.update({
                    mail_id : {
                        'History': { "array" : [0] }
                    }
                })
            # --------------------------------------------------------------------------
            self.finished.emit()
        except:
            signup_network_fail = True
            self.finished.emit()
    # --------------------------------------------------------------------------

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

# Used to create a plot area to display the plot
# --------------------------------------------------------------------------
class PlotArea(QScrollArea):
 
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
 
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        self.toolbar = NavigationToolbar(self.sc, self)

        lay.addWidget(self.toolbar)
        
        lay.addWidget(self.sc)

        self.x_axis  = []
        self.y_axis = []

    def class_to_array(self):

        self.x_axis = []
        self.y_axis = []
        
        for x in lightcurve.flux:
            self.y_axis.append(x.value)
            
        for x in lightcurve.time:
            self.x_axis.append(x.value)
            
    
    def update_plot(self):
        global lightcurve
        self.class_to_array()
        if len(lightcurve) > 0:
            # Drop off the first y element, append a new one.
            self.sc.axes.cla()  # Clear the canvas.
            self.sc.axes.plot(self.x_axis , self.y_axis)
            
            # Trigger the canvas to update and redraw.
            self.sc.draw()
        

# --------------------------------------------------------------------------

# Used to create a scrollable text field to show search results
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
# --------------------------------------------------------------------------

# Exo-Planet detection window
# --------------------------------------------------------------------------
class ExoDetection(QWidget):

    # Initialize Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def __init__(self, parent=None):
        super().__init__()
        global width,height

        self.window = None
        width = 450
        height = 180
        self.setWindowTitle("Exo Planet Detection - Planet Hunters")
        self.setFixedHeight(height)
        self.setFixedWidth(width)
        self.create_widgets()
        self.setStyleSheet("background-color: rgb(20, 21, 32)")

    # Generate url for profile picture for Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def create_url(self):
        url = 'https://avatars.dicebear.com/api/bottts/' + username + '.svg?background=%23141520'
        return url

    # Exo-Planet Detection screen widgets
    # --------------------------------------------------------------------------
    def create_widgets(self):
        global username
        global avatar
        global pfp_load
        global network_status

        # Plot Area to display the plots after selecting a sector
        # --------------------------------------------------------------------------
        self.target_plot = PlotArea(self)
        self.target_plot.setGeometry(460, -3, 830, 420)
        self.target_plot.setHidden(True)
        # --------------------------------------------------------------------------
        
        # Validation label for the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.validation_label = QLabel(self)
        self.validation_label.setGeometry(10,140,300,30)
        self.validation_label.setStyleSheet("color:#c23b02;")
        # --------------------------------------------------------------------------

        # progress_bar_exo_detection in Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.progress_bar_exo_detection = QProgressBar(self)
        self.progress_bar_exo_detection.setGeometry(10,130,150,10)
        self.progress_bar_exo_detection.setMaximum(0)
        self.progress_bar_exo_detection.setMinimum(0)
        self.progress_bar_exo_detection.setHidden(True)
        # --------------------------------------------------------------------------


        # Generating and displaying profile picture for the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.pfp  = QLabel(self)
        self.pfp_pixmap = QPixmap()
        pfp_url = self.create_url()

        try:
            if pfp_load == False:
                request = requests.get(pfp_url)
                avatar = request.content
                network_status = True
                pfp_load = True
        except:
            pass

        if network_status == True:
            self.pfp_pixmap.loadFromData(avatar)
            self.pfp.setPixmap(self.pfp_pixmap.scaled(30,30,Qt.KeepAspectRatio))
            self.pfp.setGeometry(50,10,30,30)
            welcome_txt = "Welcome,\n" + username
        else:
            self.pfp.setText(":(")
            self.pfp.setFont(QFont("Helvetica",25))
            self.pfp.setGeometry(60,8,30,30)
            welcome_txt = "OOPS!\n" + "Check your connection!"
            self.validation_label.setText("A working network connection is required")
            self.validation_label.setStyleSheet("color: #c23b02;")
        # --------------------------------------------------------------------------
        
        # Welcome label to welcome the user in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.welcome_label = QLabel(welcome_txt,self)
        self.welcome_label.setFont(QFont("Helvetica",12))
        self.welcome_label.setGeometry(90,0,300,50)
        # --------------------------------------------------------------------------

        # Target search / Advanced search label in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.search_label = QLabel("Target search",self)
        self.search_label.setFont(QFont("Helvetica"))
        self.search_label.setStyleSheet("color: #ffffff")
        self.search_label.setGeometry(10,45,200,15)
        # --------------------------------------------------------------------------

        # Target search support label in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_label = QLabel("Enter Target ID :", self)
        self.target_label.setFont(QFont("Helvetica",12))
        self.target_label.setGeometry(10,60,200,30)
        # --------------------------------------------------------------------------
        
        # Advanced search dropdown box in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.adv_select = QComboBox(self)
        self.adv_select.setGeometry(10,65,150,18)
        self.adv_select.addItems(['dataproduct_type', 'calib_level', 'obs_collection', 'obs_id', 'target_name', 's_ra',
                                's_dec', 't_min', 't_max', 't_exptime', 'wavelength_region', 'filters', 'em_min',
                                'em_max', 'target_classification', 'obs_title', 't_obs_release', 'instrument_name',
                                'proposal_pi', 'proposal_id', 'proposal_type', 'project', 'sequence_number',
                                'provenance_name', 's_region', 'jpegURL', 'dataURL', 'dataRights', 'mtFlag', 'srcDen',
                                'intentType', 'obsid', 'objID', 'exptime', 'distance', 'obsID',
                                'obs_collection_products', 'dataproduct_type_products', 'description', 'type',
                                'dataURI', 'productType', 'productGroupDescription', 'productSubGroupDescription',
                                'productDocumentationURL', 'project_products', 'prvversion', 'proposal_id_products',
                                'productFilename', 'size', 'parent_obsid', 'dataRights_products',
                                'calib_level_products', 'author', 'mission', '#', 'year', 'sort_order'])
        self.adv_select.setStyleSheet("""
                                QComboBox {
                                    border: 1px solid gray;
                                    border-radius: 3px;
                                    padding: 1px 18px 1px 3px;
                                    min-width: 6em;
                                }
                                """)
        self.adv_select.setHidden(True)
        # --------------------------------------------------------------------------

        # Advanced search hyperlink for parameters description in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.adv_search_learn_more = QLabel(self)
        self.adv_search_learn_more.setText('''<a href='https://mast.stsci.edu/api/v0/_c_a_o_mfields.html'>Learn more about these parameters here</a>''')
        self.adv_search_learn_more.openExternalLinks()
        self.adv_search_learn_more.setOpenExternalLinks(True)
        self.adv_search_learn_more.setGeometry(170,65,300,18)
        self.adv_search_learn_more.setHidden(True)
        # --------------------------------------------------------------------------

        # Advanced search parameter input value in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.adv_search_input = QLineEdit(self)
        self.adv_search_input.setFont(QFont("Helvetica",15))
        self.adv_search_input.setPlaceholderText("Enter value")
        self.adv_search_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.adv_search_input.setGeometry(10,90,350,30)
        self.adv_search_input.setAlignment(Qt.AlignCenter)
        self.adv_search_input.setHidden(True)
        # --------------------------------------------------------------------------

        # Target ID input textbox in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_search_input = QLineEdit(self)
        self.target_search_input.setFont(QFont("Helvetica",15))
        self.target_search_input.setPlaceholderText("eg: TIC 42173628")
        self.target_search_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.target_search_input.setGeometry(10,90,150,30)
        self.target_search_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Search output for targed id in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_search_result_scrollable_label = ScrollLabel(self)
        self.target_search_result_scrollable_label.setGeometry(10, 170, 400, 180)
        self.target_search_result_scrollable_label.setHidden(True)
        # --------------------------------------------------------------------------

        # Search button for target search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_search_btn = QPushButton(self)
        self.target_search_btn.setFont(QFont("Helvetica",15))
        self.target_search_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/search.png')))
        self.target_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.target_search_btn.setGeometry(170,90,50,30)
        self.target_search_btn.clicked.connect(self.search_clicked)
        # --------------------------------------------------------------------------

        # Add button for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.add_advanced_search_btn = QPushButton(self)
        self.add_advanced_search_btn.setFont(QFont("Helvetica",15))
        self.add_advanced_search_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/add.png')))
        self.add_advanced_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.add_advanced_search_btn.setGeometry(370,90,30,30)
        self.add_advanced_search_btn.setHidden(True)
        # --------------------------------------------------------------------------

        # Search button for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.search_advanced_search_btn = QPushButton(self)
        self.search_advanced_search_btn.setFont(QFont("Helvetica",15))
        self.search_advanced_search_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/search.png')))
        self.search_advanced_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.search_advanced_search_btn.setGeometry(10,130,30,30)
        self.search_advanced_search_btn.setHidden(True)
        # --------------------------------------------------------------------------

        # Undo button for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.undo_advanced_search_btn = QPushButton(self)
        self.undo_advanced_search_btn.setFont(QFont("Helvetica",15))
        self.undo_advanced_search_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/undo.png')))
        self.undo_advanced_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.undo_advanced_search_btn.setGeometry(50,130,30,30)
        self.undo_advanced_search_btn.setHidden(True)
        # --------------------------------------------------------------------------

        # Clear button for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.clear_advanced_search_btn = QPushButton(self)
        self.clear_advanced_search_btn.setFont(QFont("Helvetica",15))
        self.clear_advanced_search_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/clear.png')))
        self.clear_advanced_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.clear_advanced_search_btn.setGeometry(90,130,30,30)
        self.clear_advanced_search_btn.setHidden(True)
        # --------------------------------------------------------------------------

        # Parameters input validation for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.parameter_validation_label = QLabel("Add parameters and search, undo or clear.\nselected parameters are displayed below",self)
        self.parameter_validation_label.setGeometry(10,170,500,30)
        self.parameter_validation_label.setStyleSheet("color: #edb009")
        self.parameter_validation_label.setHidden(True)
        # --------------------------------------------------------------------------
        
        # Selected parameters label for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.selected_parameters_label = QLabel("Selected Parameters: ",self)
        self.selected_parameters_label.setGeometry(10,210,200,10)
        self.selected_parameters_label.setHidden(True)
        # --------------------------------------------------------------------------

        # Scrollable text field for selected parameters for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.adv_selected_paramters = ScrollLabel(self)
        self.adv_selected_paramters.setGeometry(10,230,400,100)
        self.adv_selected_paramters.setHidden(True)
        # --------------------------------------------------------------------------

        # Search results label for advaned search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.search_results_selected_parameters_label = QLabel("Search results: ",self)
        self.search_results_selected_parameters_label.setGeometry(10,340,200,10)
        self.search_results_selected_parameters_label.setHidden(True)
        # --------------------------------------------------------------------------
       
        # Advanced search button for target search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.advanced_search_btn = QPushButton("Advanced Search",self)
        self.advanced_search_btn.setFont(QFont("Helvetica",15))
        self.advanced_search_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.advanced_search_btn.setGeometry(230,90,150,30)
        self.advanced_search_btn.clicked.connect(self.adv_clicked)
        # --------------------------------------------------------------------------

        # Target search button for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_screen_btn = QPushButton("Back To Target Search",self)
        self.target_screen_btn.setFont(QFont("Helvetica",15))
        self.target_screen_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.target_screen_btn.setGeometry(240,130,200,30)
        self.target_screen_btn.clicked.connect(self.target_screen_clicked)
        self.target_screen_btn.setHidden(True)
        # --------------------------------------------------------------------------

        # Select from table label for target/advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.select_label = QLabel("Select from table",self)
        self.select_label.setFont(QFont("Helvetica",12))
        self.select_label.setStyleSheet("color: #ffffff")
        self.select_label.setGeometry(10,360,100,10)
        # --------------------------------------------------------------------------

        # Select value input textbox for target/advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.select_input = QLineEdit(self)
        self.select_input.setFont(QFont("Helvetica",15))
        self.select_input.setPlaceholderText(" eg: 0 or 1 ")
        self.select_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.select_input.setGeometry(10,380,80,30)
        self.select_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Select button for target/advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.select_btn = QPushButton(self)
        self.select_btn.setFont(QFont("Helvetica",15))
        self.select_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/select.png')))
        self.select_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.select_btn.setGeometry(100,380,50,30)
        self.select_btn.clicked.connect(self.select_clicked)
        # --------------------------------------------------------------------------

        # Back button to go to Select screen from the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.back_btn = QPushButton(self)
        self.back_btn.setFont(QFont("Helvetica",15))
        self.back_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/back.png')))
        self.back_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #0a71d1;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.back_btn.setGeometry(10,10,30,30)
        self.back_btn.clicked.connect(self.back_click)
        # --------------------------------------------------------------------------

        # Logout button to go to login screen from Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.lgout_btn = QPushButton(self)
        self.lgout_btn.setFont(QFont("Helvetica",15))
        self.lgout_btn.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/logout.png')))
        self.lgout_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #c23b02;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.lgout_btn.setGeometry(410,10,30,30)
        self.lgout_btn.clicked.connect(self.login_click)
        # --------------------------------------------------------------------------
        try:
            self.target_search_input.setText(target_search_id)
            if len(target_search_result) > 0 :
                self.setFixedHeight(420)
                self.target_search_result_scrollable_label.setText(str(target_search_result))
                self.target_search_result_scrollable_label.setHidden(False)
        except:
            pass
    
    # Target search button click function in the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def target_screen_clicked(self):
        global window
        if self.window is None:
            window.close()
            window = ExoDetection()
        window.show()

    # --------------------------------------------------------------------------
   
   # Advanced search button click function in the Exo-Planet Detection screen
   # --------------------------------------------------------------------------
    def adv_clicked(self):
        self.setFixedHeight(430)
        self.select_label.setHidden(True)
        self.select_input.setHidden(True)
        self.select_btn.setHidden(True)
        self.parameter_validation_label.setHidden(False)
        self.selected_parameters_label.setHidden(False)
        self.target_search_result_scrollable_label.setHidden(True)
        self.adv_selected_paramters.setHidden(False)
        self.validation_label.setText("")
        self.target_search_input.setHidden(True)
        self.search_label.setText("Advanced Search")
        self.target_search_btn.setHidden(True)
        self.target_label.setHidden(True)
        self.adv_select.setHidden(False)
        self.adv_search_input.setHidden(False)
        self.advanced_search_btn.setHidden(True)
        self.adv_search_learn_more.setHidden(False)
        self.add_advanced_search_btn.setHidden(False)
        self.search_advanced_search_btn.setHidden(False)
        self.undo_advanced_search_btn.setHidden(False)
        self.clear_advanced_search_btn.setHidden(False)
        self.target_screen_btn.setHidden(False)
    # --------------------------------------------------------------------------


    # Search button click function for target search in the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def search_clicked(self):
        global target_search_result_scrollable_label
        global target_search_id
        global target_search_result
        global search_result_isDownloaded_error

        self.validation_label.setText("Searching..")
        self.validation_label.setStyleSheet("color: #edb009;")

        self.progress_bar_exo_detection.setHidden(False)

        if self.target_search_input.text().strip() == "" :
            #self.setFixedHeight(180)
            self.validation_label.setText("!! Enter Target ID to search.\nTo search with other parameters use advanced search !!")
            self.progress_bar_exo_detection.setHidden(True)
        else:
            target_search_id = self.target_search_input.text()   
            self.target_search_btn.setEnabled(False)
            self.advanced_search_btn.setEnabled(False)
            
            
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.dowload_search_results)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # Step 6: Start the thread
            self.thread.start()
            self.thread.finished.connect(self.update_search_results)


    def update_search_results(self):
        global search_result_isDownloaded_error
        self.validation_label.setGeometry(10,140,300,30)
        self.validation_label.setStyleSheet("color:#c23b02;")

        self.progress_bar_exo_detection.setHidden(True)
        if search_result_isDownloaded_error == False:
            self.validation_label.setText("Here's what we found")
            self.validation_label.setStyleSheet("color: #edb009;")
            self.setFixedHeight(420)
            self.target_search_result_scrollable_label.setText(str(target_search_result))
            self.target_search_result_scrollable_label.setHidden(False) 
        else:
            self.target_search_result_scrollable_label.setHidden(True)
            self.setFixedHeight(170)
            self.validation_label.setText("!! A working network connection is required !!")
            self.validation_label.setStyleSheet("color: #c23b02;")  

        self.target_search_btn.setEnabled(True)
        self.advanced_search_btn.setEnabled(True) 
        
        # Add search to the database under the user
        '''
        ## Adding search to database
        hist_array = []
        ref = db.reference('/users')
        users_ref = ref.child(db_username)
        user_data = users_ref.get()
        hist_array = user_data['History']['array']

        if hist_array[0] == 0 :
            hist_array[0] = self.target_search_input.text()
        else:
            hist_array.append(self.target_search_input.text())
        
        users_ref.update({

            'History': {"array" : hist_array }
        })
        '''
    # --------------------------------------------------------------------------
    
    def select_clicked(self):
        global lightcurve
        global select_input
        select_valid = True
        self.validation_label.setGeometry(10,140,300,30)
        self.validation_label.setStyleSheet("color: #edb009;")
        try :
            if len(target_search_result) < 1 :
                self.validation_label.setText("!! No items to select from, search again !!")
                select_valid = False

        except :
            select_valid = False
            self.validation_label.setText("!! No items to select from, search again !!")
        
        if select_valid == True:
            if self.select_input.text().strip() == "" :
                select_valid = False
                self.validation_label.setText("!! Please input a valid # number !!")

        if select_valid == True:
            try:
                select_input_int = int(self.select_input.text().strip())
            except:
                select_valid = False
                self.validation_label.setText("!! Please input an integer !!")
        
        if select_valid == True:
            try:
                self.target_search_btn.setEnabled(False)
                self.advanced_search_btn.setEnabled(False)
                self.select_btn.setEnabled(False) 

                select_input = self.select_input.text().strip()

                # Step 2: Create a QThread object
                self.thread = QThread()
                # Step 3: Create a worker object
                self.worker = Worker()
                # Step 4: Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Step 5: Connect signals and slots
                self.thread.started.connect(self.worker.download_lightcurve)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                # Step 6: Start the thread
                self.thread.start()
                self.thread.finished.connect(self.update_plot)

                self.progress_bar_exo_detection.setGeometry(160,370,144,30)
                self.progress_bar_exo_detection.setHidden(False)
                self.validation_label.setGeometry(160,387,300,30)
                self.validation_label.setText("Downloading Lightcurve")

            except:
                self.validation_label.setText("!! Please select from available # numbers !!")
        
    def update_plot(self):
        global search_result_select_isDownloaded_error

        self.target_plot.update_plot()
        self.progress_bar_exo_detection.setHidden(True)
        if search_result_select_isDownloaded_error == False:
            self.validation_label.setText("Download Complete")
            self.validation_label.setStyleSheet("color: #edb009;")
            self.setFixedWidth(1300)
            self.target_plot.setHidden(False)
           
        else:
            self.validation_label.setGeometry(10,140,300,30)
            self.validation_label.setText("!! A working network connection is required !!")
            self.validation_label.setStyleSheet("color: #c23b02;")  

        self.target_search_btn.setEnabled(True)
        self.advanced_search_btn.setEnabled(True)
        self.select_btn.setEnabled(True) 

    # logout button click function to take to the login screen from the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def login_click(self):
        global window
        if self.window is None:
            window.close()
            window = Login()
        window.show()
    # --------------------------------------------------------------------------

    # Back button click function to take to select screen from the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def back_click(self):
        global window
        if self.window is None:
            window.close()
            window = Select()
        window.show()
    # --------------------------------------------------------------------------
# --------------------------------------------------------------------------

class Signup(QWidget):
    
    # Initialize signup screen
    # --------------------------------------------------------------------------
    def __init__(self, parent=None):
        super().__init__()
        self.window = None
        global width,height
        width = 400
        height = 450
        self.setWindowTitle("Sign Up - Planet Hunters")
        self.setFixedHeight(height)
        self.setFixedWidth(width)
        self.create_widgets()
        self.setStyleSheet("background-color: rgb(20, 21, 32)")
    # --------------------------------------------------------------------------

    # create signup screen widgets
    # -------------------------------------------------------------------------- 
    def create_widgets(self):
        
        # Signup logo in signup screen
        # --------------------------------------------------------------------------
        logo = QLabel("",self)
        logo_pixmap = QPixmap(os.path.join(sys.path[0],"Images/logo_small.png"))
        logo.setPixmap(logo_pixmap)
        logo.setGeometry((width/2)-30,40,50,50)
        # --------------------------------------------------------------------------

        # Signup title in signup screen
        # --------------------------------------------------------------------------
        self.welcome_msg = QLabel("          Sign Up to Planet Hunters",self)
        self.welcome_msg.setFont(QFont("Helvetica",20))
        self.welcome_msg.setGeometry((width/2)-170,100,300,30)
        # --------------------------------------------------------------------------
        
        # Input email in signup screen
        # --------------------------------------------------------------------------
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText(" Email")
        self.email_input.setGeometry((width/2)-150,140,300,30)
        # --------------------------------------------------------------------------

        # Input password in signup screen
        # --------------------------------------------------------------------------
        self.pass_input = QLineEdit(self)
        self.pass_input.setPlaceholderText(" Password")
        self.pass_input.setEchoMode(PySide6.QtWidgets.QLineEdit.Password)
        self.pass_input.setGeometry((width/2)-150,190,300,30)
        # --------------------------------------------------------------------------

        # Re-Input password in signup screen
        # --------------------------------------------------------------------------
        self.repass_input = QLineEdit(self)
        self.repass_input.setPlaceholderText(" Re-enter Password")
        self.repass_input.setEchoMode(PySide6.QtWidgets.QLineEdit.Password)
        self.repass_input.setGeometry((width/2)-150,240,300,30)
        # --------------------------------------------------------------------------

        # Signup validation label in signup screen
        # --------------------------------------------------------------------------
        self.validation_msg = QLabel("",self)
        self.validation_msg.setFont(QFont("Helvetica",12))
        self.validation_msg.setStyleSheet("color: #e84f61")
        self.validation_msg.setGeometry((width/2)-150,274,300,25)
        # --------------------------------------------------------------------------

        # Signup button in signup screen
        # --------------------------------------------------------------------------
        self.signup_btn = QPushButton("Sign Up",self)
        self.signup_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.signup_btn.setGeometry((width/2)-150,310,300,30)
        self.signup_btn.clicked.connect(self.signup_click)
        # --------------------------------------------------------------------------

        # Back to login button in signup screen
        # --------------------------------------------------------------------------
        self.login_btn= QPushButton("Back to Login",self)
        self.login_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #0a71d1;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)

        self.login_btn.setGeometry((width/2)-150,350,300,30)
        self.login_btn.clicked.connect(self.login_click)
        # --------------------------------------------------------------------------

        # Progress bar in signup screen
        # --------------------------------------------------------------------------
        self.progress_bar_login = QProgressBar(self)
        self.progress_bar_login.setMaximum(0)
        self.progress_bar_login.setMinimum(0)
        self.progress_bar_login.setGeometry((width/2)-150,390,300,10)
        self.progress_bar_login.setHidden(True)
        # --------------------------------------------------------------------------

        # Progress bar label in login screen
        # --------------------------------------------------------------------------
        self.login_label = QLabel("Signing you up",self)
        self.login_label.setGeometry((width/2)-50,410,300,30)
        self.login_label.setHidden(True)
        # --------------------------------------------------------------------------

    # Signup button click function in signup screen
    # --------------------------------------------------------------------------
    def signup_click(self):
        global window
        global sign_up
        global signup_email_id
        global details
        global r

        self.progress_bar_login.setHidden(False)
        self.login_label.setHidden(False)
        if self.email_input.text().strip == "":
            self.validation_msg.setText("No email input, please try again")
            self.progress_bar_login.setHidden(True)
            self.login_label.setHidden(True)
        elif self.pass_input.text() != self.repass_input.text() :
            self.validation_msg.setText("Passwords do not match, please try again")
            self.progress_bar_login.setHidden(True)
            self.login_label.setHidden(True)
        else:
            details={
                'email':self.email_input.text(),
                'password':self.pass_input.text(),
                'returnSecureToken': True
            }
            signup_email_id = self.email_input.text()

            # Multi threading the login request in login screen
            # --------------------------------------------------------------------------
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.signup)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # Step 6: Start the thread
            self.thread.start()

            # Block buttons till login request complete
            self.login_btn.setEnabled(False)
            self.signup_btn.setEnabled(False)

            self.thread.finished.connect(self.signup_continue)
            # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    
    # Sign up continue after multi threading process complete
    # --------------------------------------------------------------------------
    def signup_continue(self):
        global window
        global signup_error_msg
        global signup_network_fail

        if signup_network_fail == True:
            self.validation_msg.setText("Please connect to a working internet connection")
            self.progress_bar_login.setHidden(True)
            self.login_label.setHidden(True)
            self.login_btn.setEnabled(True)
            self.signup_btn.setEnabled(True)

        elif signup_success == True:
            if self.window is None:
                window.close()
                window = Login()
            window.show()
        else:
            self.validation_msg.setText(signup_error_msg)
            self.progress_bar_login.setHidden(True)
            self.login_label.setHidden(True)
            self.login_btn.setEnabled(True)
            self.signup_btn.setEnabled(True) 
        

    # Login button click function in signup screen
    # --------------------------------------------------------------------------
    def login_click(self):
        global window
        if self.window is None:
            window.close()
            window = Login()
        window.show()
    # --------------------------------------------------------------------------
# --------------------------------------------------------------------------       
class Select(QWidget):
   
   # Initialize select screen
   # --------------------------------------------------------------------------
    def __init__(self, parent=None):
        super().__init__()
        self.window = None
        global width,height
        width = 400
        height = 450
        self.setWindowTitle("Select Program - Planet Hunters")
        self.setFixedHeight(height)
        self.setFixedWidth(width)
        self.create_widgets()
        self.setStyleSheet("background-color: rgb(20, 21, 32)")

    # url creator for profile picture in select screen
    # --------------------------------------------------------------------------
    def create_url(self):
        url = 'https://avatars.dicebear.com/api/bottts/' + username + '.svg?background=%23141520'
        return url
    # --------------------------------------------------------------------------
    
    # Creating widgets for select screen 
    # --------------------------------------------------------------------------
    def create_widgets(self):
        global avatar
        global pfp_load
        global network_status

        # Welcome label to greet user in select screen
        # --------------------------------------------------------------------------
        self.hello_label = QLabel(self)
        self.hello_label.setFont(QFont("Helvetica",12))
        self.hello_label.setGeometry((width/2)-100,0,300,50)
        # --------------------------------------------------------------------------

        # Generate profile picture and display in select screen
        # --------------------------------------------------------------------------
        self.pfp  = QLabel(self)
        self.pfp_pixmap = QPixmap()
        pfp_url = self.create_url()

        try:
            if pfp_load == False:
                request = requests.get(pfp_url)
                avatar = request.content
                network_status = True
                pfp_load = True
        except:
            pass

        if network_status == True:
            self.pfp_pixmap.loadFromData(avatar)
            self.pfp.setPixmap(self.pfp_pixmap.scaled(30,30,Qt.KeepAspectRatio))
            self.pfp.setGeometry((width/2)-150,10,30,30)
            hello_txt = "Welcome,\n" + username
            self.hello_label.setText(hello_txt)
        else:
            self.pfp.setText(":(")
            self.pfp.setFont(QFont("Helvetica",25))
            self.pfp.setGeometry((width/2)-150,8,30,30)
            hello_txt = "OOPS!\n" + "Check your connection!"
            self.hello_label.setText(hello_txt)
            self.hello_label.setGeometry((width/2)-120,0,300,50)
        # --------------------------------------------------------------------------

        # Habitability title in select screen
        # --------------------------------------------------------------------------
        self.hab_title = QLabel("Habitability Detection",self)
        self.hab_title.setFont(QFont("Helvetica",20))
        self.hab_title.setGeometry((width/2)-150,60,300,30)
        # --------------------------------------------------------------------------
        
        # Habitability description in select screen
        # --------------------------------------------------------------------------
        self.hab_desc = QLabel("Lorem ipsum dolor sit amet, consectetur adipiscing elit.\nAenean dolor enim, aliquam sit amet odio et, tempor tincidunt nibh.\nQuisque dictum rhoncus ipsum ut pulvinar.\nNam gravida quam lacus, vitae luctus enim aliquet vitae.\nMorbi non libero ullamcorper tortor mollis consequat.\nSed feugiat neque ac augue commodo pharetra.",self)
        self.hab_desc.setFont(QFont("Helvetica",12))
        self.hab_desc.setGeometry((width/2)-150,90,300,110)
        # --------------------------------------------------------------------------
        
        # Habitability button in select screen
        # --------------------------------------------------------------------------
        habitability_btn = QPushButton("Start Habitability Detection",self)
        habitability_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        habitability_btn.setGeometry((width/2)-150,200,300,30)
        habitability_btn.clicked.connect(self.hab_click)
        # --------------------------------------------------------------------------

        # Exo-Planet detection title in select screen
        # --------------------------------------------------------------------------
        self.exo_title = QLabel("Exoplanet Detection",self)
        self.exo_title.setFont(QFont("Helvetica",20))
        self.exo_title.setGeometry((width/2)-150,240,300,30)
        # --------------------------------------------------------------------------
        
        # Exo-Planet detecttion description in select screen
        # --------------------------------------------------------------------------
        self.exo_desc = QLabel("Lorem ipsum dolor sit amet, consectetur adipiscing elit.\nAenean dolor enim, aliquam sit amet odio et, tempor tincidunt nibh.\nQuisque dictum rhoncus ipsum ut pulvinar.\nNam gravida quam lacus, vitae luctus enim aliquet vitae.\nMorbi non libero ullamcorper tortor mollis consequat.\nSed feugiat neque ac augue commodo pharetra.",self)
        self.exo_desc.setFont(QFont("Helvetica",12))
        self.exo_desc.setGeometry((width/2)-150,270,300,110)
        # --------------------------------------------------------------------------

        # Exo-Planet detection button in select screen
        # --------------------------------------------------------------------------
        Detection_btn= QPushButton("Start Exoplanet Detection",self)
        Detection_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #0a71d1;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        Detection_btn.setGeometry((width/2)-150,390,300,30)
        Detection_btn.clicked.connect(self.det_click)
        # --------------------------------------------------------------------------

        # Logout button in select screen
        # --------------------------------------------------------------------------
        self.logout = QPushButton(self)
        self.logout.setIcon(PySide6.QtGui.QIcon(os.path.join(sys.path[0],'Images/logout.png')))
        self.logout.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #c23b02;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.logout.setGeometry(320,10,30,30)
        self.logout.clicked.connect(self.login_click)
        # --------------------------------------------------------------------------

    # Login button function in select screen
    # --------------------------------------------------------------------------
    def login_click(self):
        global window
        if self.window is None:
            window.close()
            window = Login()
        window.show()
    # --------------------------------------------------------------------------

    # Habitability button function in select screen
    # --------------------------------------------------------------------------
    def hab_click(self):
        pass
    # --------------------------------------------------------------------------

    # Exo-Planet detection button function in select screen
    # --------------------------------------------------------------------------
    def det_click(self):
        global window
        if self.window is None:
            window.close()
            window = ExoDetection()
        window.show()
    # --------------------------------------------------------------------------
# --------------------------------------------------------------------------
class Login(QWidget):

    # Initialize login screen
    # --------------------------------------------------------------------------
    def __init__(self, parent=None):
        super().__init__()
        self.window = None
        self.window2 = None
        global width,height
        width = 400
        height = 450
        
        self.setWindowTitle("Log In - Planet Hunters")
        self.setFixedHeight(height)
        self.setFixedWidth(width)
        self.create_widgets()
        self.setStyleSheet("background-color: rgb(20, 21, 32)")

        # Decrypting saved user info and display in the login screen if user has selected remember me previously
        # --------------------------------------------------------------------------

        try:
            path_loader_request = str(os.path.join(sys.path[0],'loader_request.joblib'))
            path_loader = str(os.path.join(sys.path[0],'loader.joblib'))
            info = joblib.load(path_loader_request)

            if len(info) > 1 :
                self.checkbox.setChecked(False)
                self.checkbox.setText("Forget me")
                self.checkbox.clicked.connect(self.forget_me)
                fernet = joblib.load(path_loader)
                self.email_input.setText(fernet.decrypt(info[0]).decode())
                self.pass_input.setText(fernet.decrypt(info[1]).decode())
        except:
            pass

         # --------------------------------------------------------------------------
    # Function to forget user login details after clicking on forget me in login screen
    # --------------------------------------------------------------------------
    def forget_me(self):
        self.email_input.setText("")
        self.pass_input.setText("")
        self.checkbox.setText("Remember me")
        joblib.dump([],"loader_request.joblib")
     # --------------------------------------------------------------------------

    # Creating the widgets for the login screen
    # --------------------------------------------------------------------------
    def create_widgets(self):
        global sign_up

        # Login logo in login screen
        # --------------------------------------------------------------------------
        logo = QLabel("",self)
        logo_pixmap = QPixmap(os.path.join(sys.path[0],"Images/logo_small.png"))
        logo.setPixmap(logo_pixmap)
        logo.setGeometry((width/2)-30,50,50,50)
        # --------------------------------------------------------------------------

        # Login Title in login screen
        # --------------------------------------------------------------------------

        if (sign_up == False):
            self.welcome_msg = QLabel("           Log In to Planet Hunters",self)
            self.welcome_msg.setGeometry((width/2)-170,110,300,30)
            self.welcome_msg.setFont(QFont("Helvetica",20))
        else:
            logo.setGeometry((width/2)-30,20,50,50)
            self.welcome_msg = QLabel("           Thank you for signing up!\n  you can now log In to Planet Hunters",self)
            self.welcome_msg.setGeometry((width/2)-160,80,350,60)
            self.welcome_msg.setFont(QFont("Helvetica",18))
            sign_up = False
        # --------------------------------------------------------------------------

        # Email input textbox in login screen
        # --------------------------------------------------------------------------
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText(" Email")
        self.email_input.setGeometry((width/2)-150,150,300,30)
        # --------------------------------------------------------------------------

        # Password input textbox in login screen
        # --------------------------------------------------------------------------
        self.pass_input = QLineEdit(self)
        self.pass_input.setPlaceholderText(" Password")
        self.pass_input.setEchoMode(PySide6.QtWidgets.QLineEdit.Password)
        self.pass_input.setGeometry((width/2)-150,200,300,30)
        # --------------------------------------------------------------------------

        # Password re-input textbox in login screen
        # --------------------------------------------------------------------------
        self.repass_input = QLineEdit(self)
        self.repass_input.setPlaceholderText(" Re-enter Password")
        self.repass_input.setEchoMode(PySide6.QtWidgets.QLineEdit.Password)
        self.repass_input.setGeometry((width/2)-150,250,300,30)
        self.repass_input.setHidden(True)
        # --------------------------------------------------------------------------

        # Login validation label in login screen
        # --------------------------------------------------------------------------
        self.validation_msg = QLabel("",self)
        self.validation_msg.setFont(QFont("Helvetica",12))
        self.validation_msg.setStyleSheet("color: #e84f61")
        self.validation_msg.setGeometry((width/2)-150,225,300,30)
        # --------------------------------------------------------------------------

        # Remember me checkbox to remember the login details when app opened next time in login screen
        # --------------------------------------------------------------------------
        self.checkbox = QCheckBox("Remember Me", self)
        self.checkbox.setGeometry((width/2)-150,250,300,30)
        self.checkbox.setChecked(True)
        # --------------------------------------------------------------------------

        # Login button in login screen
        # --------------------------------------------------------------------------
        self.login_btn = QPushButton("Login",self)
        self.login_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #4b993f;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)
        self.login_btn.setGeometry((width/2)-150,310,300,30)
        self.login_btn.clicked.connect(self.login_click)
        # --------------------------------------------------------------------------
        
        # Sign up button in login screen
        # --------------------------------------------------------------------------
        self.signup_btn= QPushButton("Not a planet hunter yet? Sign Up here",self)
        self.signup_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #0a71d1;
                                    }
                                QPushButton:hover {
                                    background-color: #edb009;
                                    color: #000000
                                    }
                                """)

        self.signup_btn.setGeometry((width/2)-150,350,300,30)
        self.signup_btn.clicked.connect(self.signup_click)
        # --------------------------------------------------------------------------

        # Progress bar in login screen
        # --------------------------------------------------------------------------
        self.progress_bar_login = QProgressBar(self)
        self.progress_bar_login.setMaximum(0)
        self.progress_bar_login.setMinimum(0)
        self.progress_bar_login.setGeometry((width/2)-150,390,300,10)
        self.progress_bar_login.setHidden(True)
        # --------------------------------------------------------------------------

        # Progress bar label in login screen
        # --------------------------------------------------------------------------
        self.login_label = QLabel("Logging you in",self)
        self.login_label.setGeometry((width/2)-50,400,300,30)
        self.login_label.setHidden(True)
        # --------------------------------------------------------------------------


    # Login button click function in login screen
    # --------------------------------------------------------------------------
    def login_click(self):
        global payload

        self.progress_bar_login.setHidden(False)
        self.login_label.setHidden(False)
            
        # Login validation with google api in login screen
        # --------------------------------------------------------------------------
        payload = json.dumps({
        "email": self.email_input.text(),
        "password": self.pass_input.text(),
        "returnSecureToken": True
        })

        # Multi threading the login request in login screen
        # --------------------------------------------------------------------------
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.login)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()

        # Block buttons till login request complete
        self.login_btn.setEnabled(False)
        self.signup_btn.setEnabled(False)

        self.thread.finished.connect(self.login_continue)
        # --------------------------------------------------------------------------

            
    # Complete login after multithreading complete in login screen
    # --------------------------------------------------------------------------
    def login_continue(self):
        global window 
        global username 
        global db_username
        global payload
        global r
        global window
        global login_network_fail

        lines_w = []
        self.login_btn.setEnabled(True)
        self.signup_btn.setEnabled(True)
        if login_network_fail == False :
            self.validation_msg.setText("Please connect to a working internet connection") 
            self.progress_bar_login.setHidden(True)
            self.login_label.setHidden(True)
        else:
            if 'error' in r.json().keys():
                self.validation_msg.setText(" Invalid email/password")
                self.progress_bar_login.setHidden(True)
                self.login_label.setHidden(True)
            #if the login succeeded
            if 'idToken' in r.json().keys() :
                username = self.email_input.text()
                db_username = username
                db_username = db_username.replace("@","")
                db_username = db_username.replace(".","")
                        
                if self.checkbox.isChecked() == True :
                    lines = [self.email_input.text(),self.pass_input.text()]
                    for x in range(0,2):
                        message = lines[x]
                        fernet = joblib.load("loader.joblib")
                        encMessage = fernet.encrypt(message.encode())
                        lines_w.append(encMessage)
                    
                    joblib.dump(lines_w,"loader_request.joblib")
                
                if self.window is None:
                    window.close()
                    window = Select()
                window.show()
    # --------------------------------------------------------------------------


    # Signup button click function in login screen
    # --------------------------------------------------------------------------
    def signup_click(self):
        global window
        if self.window is None:
            window.close()
            window = Signup()
        window.show()
    # --------------------------------------------------------------------------
# --------------------------------------------------------------------------      

# Application start
# --------------------------------------------------------------------------  

app = QApplication([])
pixmap = QPixmap(os.path.join(sys.path[0],"Images/logo.png"))
splash = QSplashScreen(pixmap)
splash.show()
window = Login()
window.show()
splash.finish(window)
sys.exit(app.exec())

