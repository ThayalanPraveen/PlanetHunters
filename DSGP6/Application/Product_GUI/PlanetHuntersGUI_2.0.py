import pickle
import time
import PySide6
from astropy import units as u
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

# Store if user is a pro user or not
# --------------------------------------------------------------------------
pro = None
# --------------------------------------------------------------------------

# Used to store the load and store account profile picture 
# --------------------------------------------------------------------------
avatar = None # component_3
pfp_load = False # component_3
network_status = False # component_3
# --------------------------------------------------------------------------

# Used to change window dimensions
# --------------------------------------------------------------------------
width = 0
height = 0
# --------------------------------------------------------------------------

# Used to add data to the database 
# --------------------------------------------------------------------------
username = "" # component_3 
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
mission = 0
lightcurve_collection = None
# --------------------------------------------------------------------------

# Used to store data for bls analysis
# --------------------------------------------------------------------------
fold_period = 0
fold_freq = 0
bls_period = 0
bls_transit = 0
bls_duration = 0
bls_fold_clicked = False
# --------------------------------------------------------------------------

# Used for flatten plot
# --------------------------------------------------------------------------
window_length = 101
polyorder = 2
niters = 3
sigma = 3
#--------------------------------------------------------------------------

# Used for binned plot
# --------------------------------------------------------------------------
n_bins = None
bins = None

# Used for Habitability
# --------------------------------------------------------------------------
axhline = None
axline_val = 0
ylim_min = -2
ylim_max = 2
xlim_min = -2
xlim_max = 2
albedo = 0
# --------------------------------------------------------------------------

# Store current plot type
# -------------------------------------------
current_selected_plot = 0
current_selected_plot_type = 0
error = ""

# Application font
# --------------------------------------------------------------------------
app_font = "Arial"
# --------------------------------------------------------------------------

# Store selected parameters 
# --------------------------------------------------------------------------
parameters_text = [] # Store list of selected parameters and used for undo
filter_array = [] # keep track of the search filters applied for undo
target_search_result_copy = None # copy of search result to filter search result
filtered = False # boolean to check if user is in the filter screen
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
        global error

        try:
            if filtered == False:
                lightcurve = target_search_result[int(select_input)].download()
            else:
                lightcurve = target_search_result_copy[int(select_input)].download()

            search_result_select_isDownloaded_error = False
            self.finished.emit()
        except BaseException as e:
            search_result_select_isDownloaded_error = True
            error = str(e)
            self.finished.emit()
    # --------------------------------------------------------------------------

    # Light curve search download multi-threading process
    # --------------------------------------------------------------------------
    def dowload_search_results(self):
        global target_search_result
        global target_search_result_copy
        global search_result_isDownloaded_error
        global error 

        try:
            if mission > 0:
                if mission == 1 :
                    target_search_result = lk.search_lightcurve(target_search_id, mission = 'Kepler', cadence='long')
                    self.finished.emit()
                elif mission == 2 :
                    target_search_result = lk.search_lightcurve(target_search_id, mission = 'K2', cadence='long')
                    self.finished.emit()
                else:
                    target_search_result = lk.search_lightcurve(target_search_id, mission = 'TESS', cadence='long')
                    self.finished.emit()
            else:
                target_search_result = lk.search_lightcurve(target_search_id, cadence='long')
                target_search_result_copy = target_search_result
                search_result_isDownloaded_error = False
                self.finished.emit()
        
        except BaseException as e:
            search_result_isDownloaded_error = True
            error = str(e)
            self.finished.emit()
    # --------------------------------------------------------------------------

    # Login multi-threading process
    # --------------------------------------------------------------------------
    def login(self):
        global payload
        global r
        global pro
        global login_network_fail

        login_network_fail = False
        try:
            r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword',
                                params={"key": apikey},
                                data=payload)
            try:
                ref = db.reference('/users')
                users_ref = ref.child(db_username)
                user_data = users_ref.get()
                pro = user_data['Pro']
            except:
                pass
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

# Canvas to create the plots
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

        self.toolbar = NavigationToolbar(self.sc, self)

        lay.addWidget(self.toolbar)
        
        lay.addWidget(self.sc)

        self.x_axis  = []
        self.y_axis = []

    # --------------------------------------------------------------------------
    def update_plot(self,selector,plot_type):
        global lightcurve
        global bls_period
        global bls_transit
        global bls_duration
        global data
        global data2
        global axhline

        # Nested if to switch plot type and line type
        # --------------------------------------------------------------------------

        # Plot Light Curve
        # --------------------------------------------------------------------------
        if plot_type == 0 :
            self.sc.axes.cla()
            lightcurve_plot_data = lightcurve
            if selector == 0:
                lightcurve_plot_data.plot(ax=self.sc.axes)
            elif selector == 1:
                lightcurve_plot_data.scatter(ax=self.sc.axes)
            else:
                lightcurve_plot_data.errorbar(ax=self.sc.axes)
        # --------------------------------------------------------------------------

        # Plot Normalized Light Curve
        # --------------------------------------------------------------------------
        elif plot_type == 1:
            self.sc.axes.cla()
            lightcurve_plot_data = lightcurve.normalize()
            if selector == 0:
                lightcurve_plot_data.plot(ax=self.sc.axes)
            elif selector == 1:
                lightcurve_plot_data.scatter(ax=self.sc.axes)
            else:
                lightcurve_plot_data.errorbar(ax=self.sc.axes)
        # --------------------------------------------------------------------------
    
        # Plot Folded Light Curve
        # --------------------------------------------------------------------------
        elif plot_type == 2:
            self.sc.axes.cla()
            lightcurve_plot_data = lightcurve.fold(period = fold_period)
            if selector == 0:
                lightcurve_plot_data.plot(ax=self.sc.axes)
            elif selector == 1:
                lightcurve_plot_data.scatter(ax=self.sc.axes)
            else:
                lightcurve_plot_data.errorbar(ax=self.sc.axes)
        # --------------------------------------------------------------------------
        
        # Plot Flattened Light Curve
        # --------------------------------------------------------------------------
        elif plot_type == 3:
            self.sc.axes.cla()
            lightcurve_plot_data = lightcurve.flatten(window_length = window_length,polyorder=polyorder,niters=niters,sigma=sigma)
            if selector == 0:
                lightcurve_plot_data.plot(ax=self.sc.axes)
            elif selector == 1:
                lightcurve_plot_data.scatter(ax=self.sc.axes)
            else:
                lightcurve_plot_data.errorbar(ax=self.sc.axes)
        # --------------------------------------------------------------------------
        
        # Plot Binned Light Curve
        # --------------------------------------------------------------------------
        elif plot_type == 4:
            self.sc.axes.cla()
            lightcurve_plot_data = lightcurve.bin(bins = bins)
            if selector == 0:
                lightcurve_plot_data.plot(ax=self.sc.axes)
            elif selector == 1:
                lightcurve_plot_data.scatter(ax=self.sc.axes)
            else:
                lightcurve_plot_data.errorbar(ax=self.sc.axes)
        # --------------------------------------------------------------------------
        
        # Plot BLS
        # --------------------------------------------------------------------------
        elif plot_type == 5:
            self.sc.axes.cla()
            lightcurve_plot_data = lightcurve
            period = np.linspace(1, fold_period, 10000)
            bls = lightcurve_plot_data.to_periodogram(method='bls', period=period, frequency_factor=fold_freq)
            bls_period = bls.period_at_max_power
            bls_transit = bls.transit_time_at_max_power
            bls_duration = bls.duration_at_max_power

            if selector == 0:
                bls.plot(ax=self.sc.axes)
            elif selector == 1:
                bls.scatter(ax=self.sc.axes)
            else:
                bls.errorbar(ax=self.sc.axes)
        # --------------------------------------------------------------------------
        
        # Plot Folded Light Curve
        # --------------------------------------------------------------------------
        elif plot_type ==6:
            self.sc.axes.cla()
            lightcurve_plot_data = lightcurve
            lightcurve_plot_data = lightcurve_plot_data.fold(period=bls_period, epoch_time=bls_transit)
            if selector == 0:
                lightcurve_plot_data.plot(ax=self.sc.axes)
            elif selector == 1:
                lightcurve_plot_data.scatter(ax=self.sc.axes)
            else:
                lightcurve_plot_data.errorbar(ax=self.sc.axes)
            self.sc.axes.set_xlim(-1,1)
        # --------------------------------------------------------------------------

        # Plot Folded Light Curve in Habitability
        # --------------------------------------------------------------------------
        elif plot_type ==7:
            self.sc.axes.cla()
            data = lc_phased.plot(ax = self.sc.axes, marker = '.', linewidth = 0, color = 'red', alpha = 0.2, markersize = 3, label = 'unbinned')
            data2 = lc_phased_binned.plot(ax = self.sc.axes, marker = 'o', linewidth = 0, color = 'k', alpha = 0.8, markersize = 6, label = 'binned')

            axhline = self.sc.axes.axhline((ylim_min + ylim_max)/2)
            self.sc.axes.set_xlim(xlim_min,xlim_max) 
            self.sc.axes.set_ylim(ylim_min, ylim_max) 
        # --------------------------------------------------------------------------

        elif plot_type ==8:
            axhline.set_ydata(selector)

        # Draw the plot on screen
        # --------------------------------------------------------------------------
        if len(lightcurve) > 0:
            self.sc.draw()
    
    def plotTargetPixelFile(self):
        try:
            search_result = lk.search_targetpixelfile(target_search_id,author = lightcurve.author)
            tpf = search_result[int(select_input)].download()

            # plot the data ('pipeline' command tells it to plot the red aperture)
            self.sc.axes.cla()
            tpf.plot(aperture_mask='pipeline',ax=self.sc.axes)
            self.sc.draw()
        except:
            print("Target pixel file is not available for this particular lightcurve")
    
    def plotLightCurve(self):
        try:
            sector_data = lk.search_lightcurve(target_search_id,author = lightcurve.author)
            lc = sector_data[int(select_input)].download()
            self.sc.axes.cla()
            lc.plot(linewidth = 0, marker = '.', color = 'black', alpha = 0.3,ax=self.sc.axes)
            self.sc.draw()
        except:
            pass
    
    def backgroundFlux(self):
        try:
            sector_data = lk.search_lightcurve(target_search_id,author = lightcurve.author)
            lc = sector_data[int(select_input)].download()
            self.sc.axes.cla()
            self.sc.axes.plot(lc.time.value, lc.sap_bkg.value, color = 'blue', lw = 0, marker = '.', ms = 1)
            self.sc.axes.set_ylabel("Background flux") # label the axes
            self.sc.axes.set_xlabel("Time (TJD)")
            self.sc.draw()
        except:
            pass
    
    def backgroundFluxAtTransitEvent(self):
        try:
            sector_data = lk.search_lightcurve(target_search_id,author = lightcurve.author)
            lc = sector_data[int(select_input)].download()
            transit_time = bls_transit # variable. time of transit event 

            # generate a mask so that we only see the times around the transit event
            # in this example we are looking at 2 days on either side of the event but you can CHANGE THIS depending on the signal.
            transit_mask = (lc.time.value > transit_time - 2) & (lc.time.value < transit_time + 2)

            self.sc.axes.cla()

            # mask the date (both the time and the flux using the mask we just generated)
            self.sc.axes.plot(lc.time.value[transit_mask], lc.sap_bkg.value[transit_mask], color = 'blue', lw = 0, marker = '.', ms = 1)

            self.sc.axes.axvline(transit_time) # axv line is similar to our axh line...now its vertical only

            self.sc.axes.set_ylabel("Background flux") 
            self.sc.axes.set_xlabel("Time (TJD)")
            self.sc.draw()
        except:
            pass

            
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
        self.setStyleSheet("background-color: #" + background_color_hex +";")

    # Exo-Planet Detection screen widgets
    # --------------------------------------------------------------------------
    def create_widgets(self):

        global filtered
        global username
        global avatar
        global pfp_load 
        global network_status 

        # Component set 3
        self.cmp_3_create(40,0)
        
        # Components set 2
        self.cmp_2_create(0,35)
        self.search_progressBar.setHidden(True)

        # Enable and disable filter button depending on length of search result
        # -------------------------------------------------------------------------
        try:
            if len(target_search_result) > 0 :
                self.advanced_search_btn.setEnabled(True)
            else:
                self.advanced_search_btn.setEnabled(False)
        except:
            self.advanced_search_btn.setEnabled(False)

        # Component set 6
        self.cmp_6_create(0,160)

        # Component set 7
        self.cmp_7_create(460,490)
        
        # Component set 4
        self.cmp_4_create(640,490)

        # Components set 1
        self.cmp_1_create(750,490)

        # Components set 5
        self.cmp_5_create(0,55)
        self.cmp_5_visibility(True)

        # Components set 8
        self.cmp_8_create(0,350)

        # Component set 9
        self.cmp_9_create(450,-13)

        # Component set 10
        self.cmp_10_create(0,0)

        # Component set 11
        self.cmp_11_create(400,0)

        # Components set 12
        self.cmp_12_create(-160,0)
        self.cmp_12_visibility(True)

        # Component set 15
        self.cmp_15_create(620,490)
        self.cmp_15_visibility(True)

        try:
            self.target_search_input.setText(target_search_id)
            if len(target_search_result) > 0 :
                self.setFixedHeight(420)
                self.target_search_result_scrollable_label.setText(str(target_search_result))
                self.target_search_result_scrollable_label.setHidden(False)
        except:
            pass

        filtered = False
    
    # Component set 1
    # -------------------------------------------------------------------------------
    # Create component
    def cmp_1_create(self,cmp_1_x_offset,cmp_1_y_offset):

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
        self.lightcurve_plot_btn.clicked.connect(self.lc_btn_clicked)
        # --------------------------------------------------------------------------
        
        # Label to show "Fold Light Curve" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------        
        self.fold_label = QLabel("Fold Light Curve : BLS" , self)
        self.fold_label.setGeometry(10 + cmp_1_x_offset, 100+ cmp_1_y_offset, 150, 20)
        self.fold_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Period label
        # --------------------------------------------------------------------------
        self.period_label = QLabel("Period (days) : " , self)
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
        self.period_input.setGeometry(100+ cmp_1_x_offset,130+ cmp_1_y_offset,50,20)
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
        self.folded_plot_btn.clicked.connect(self.fold_btn_clicked)
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
        self.flattened_plot_btn.clicked.connect(self.flat_btn_clicked)
        # --------------------------------------------------------------------------

        # Label to show "Plot Folded Curve" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------        
        self.folded_label = QLabel("Plot Binned Curve" , self)
        self.folded_label.setGeometry(350+ cmp_1_x_offset, 10+ cmp_1_y_offset, 150, 20)
        self.folded_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Bins label
        # --------------------------------------------------------------------------
        self.bins_label = QLabel("Bins : " , self)
        self.bins_label.setGeometry(350+ cmp_1_x_offset, 40+ cmp_1_y_offset, 200, 20)
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
        self.bins_input.setGeometry(455+ cmp_1_x_offset,40+ cmp_1_y_offset,50,20)
        self.bins_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------
        # --------------------------------------------------------------------------
        self.binned_plot_btn = QPushButton("Binned Plot",self)
        self.binned_plot_btn.setGeometry(350+ cmp_1_x_offset, 70 + cmp_1_y_offset, 130, 20)
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
        self.binned_plot_btn.clicked.connect(self.bin_btn_clicked)

    def lc_btn_clicked(self):
        global current_selected_plot
        if self.normalize_check.isChecked() == True:
            current_selected_plot = 1
            self.target_plot.update_plot(current_selected_plot_type,1)
        else:
            current_selected_plot = 0
            self.target_plot.update_plot(current_selected_plot_type,0)

    def fold_btn_clicked(self):
        global current_selected_plot
        global fold_period
        current_selected_plot = 2
        fold_period = float(self.period_input.text())
        self.target_plot.update_plot(current_selected_plot_type,2)


    def flat_btn_clicked(self):
        global window_length
        global polyorder
        global niters
        global sigma
        global current_selected_plot
        current_selected_plot = 3
        window_length = int(float(self.window_length_input.text()))
        polyorder = int(float(self.poly_order_input.text()))
        niters = int(float(self.niters_input.text()))
        sigma = int(float(self.sigma_input.text()))
        self.target_plot.update_plot(current_selected_plot_type,3)

    def bin_btn_clicked(self):
        global bins
        global n_bins
        global current_selected_plot
        current_selected_plot = 4
        bins = int(float(self.bins_input.text()))
        self.target_plot.update_plot(current_selected_plot_type,4)
    
    # Component set 1 visibility function
    def cmp_1_visibility(self,bool):
        self.bins_label.setHidden(bool)
        self.sigma_label.setHidden(bool)
        self.folded_label.setHidden(bool)
        self.niters_label.setHidden(bool)
        self.flattened_label.setHidden(bool)
        self.poly_order_label.setHidden(bool)
        self.lightcurve_label.setHidden(bool)
        self.window_length_label.setHidden(bool)
        self.period_label.setHidden(bool)
        self.fold_label.setHidden(bool)
        self.binned_plot_btn.setHidden(bool)
        self.flattened_plot_btn.setHidden(bool)
        self.lightcurve_plot_btn.setHidden(bool)
        self.folded_plot_btn.setHidden(bool)
        self.period_input.setHidden(bool)
        self.bins_input.setHidden(bool)
        self.normalize_check.setHidden(bool)
        self.bins_input.setHidden(bool)
        self.sigma_input.setHidden(bool)
        self.niters_input.setHidden(bool)
        self.poly_order_input.setHidden(bool)
        self.window_length_input.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component set 2
    #-------------------------------------------------------------------------------
    # Create components set 2
    def cmp_2_create(self,cmp_2_x_offset,cmp_2_y_offset):
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
        self.mission_comboBox = QComboBox(self)
        self.mission_comboBox.setGeometry(165+cmp_2_x_offset,55+cmp_2_y_offset,50,30)
        self.mission_comboBox.addItems(['All','Kepler','K2','TESS'
                                    ])
        self.mission_comboBox.setStyleSheet("""
                                QComboBox {
                                    border: 3px solid gray;
                                    border-radius: 5px;
                                    padding: 1px 18px 1px 3px;
                                    min-width: 4em;
                                }
                                """)
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
        self.target_search_btn.setGeometry(260+cmp_2_x_offset,55+cmp_2_y_offset,50,30)
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
        self.advanced_search_btn.setGeometry(315+cmp_2_x_offset,55+cmp_2_y_offset,120,30)
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
    
    # Search button click function for target search in the Exo-Planet Detection screen
    def search_clicked(self):
        global target_search_result_scrollable_label
        global target_search_id
        global target_search_result
        global search_result_isDownloaded_error
        global mission

        self.validation_label.setText("Searching..")
        self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")

        self.search_progressBar.setHidden(False)

        if self.target_search_input.text().strip() == "" :
            #self.setFixedHeight(180)
            self.validation_label.setText("!! Enter Target ID to search.\nTo search with other parameters use advanced search !!")
            self.search_progressBar.setHidden(True)
        else:
            target_search_id = self.target_search_input.text()
            mission = self.mission_comboBox.currentIndex()

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

    # Advanced search button click function in the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def adv_clicked(self):
        global filtered

        filtered = True
        self.setFixedHeight(680)
        self.parameter_validation_label.setHidden(False)
        self.selected_parameters_label.setHidden(False)
        self.search_results_selected_parameters_label.setHidden(False)
        self.adv_selected_parameters_scrollLabel.setHidden(False)
        self.validation_label.setText("")
        self.target_search_input.setHidden(True)
        self.mission_comboBox.setHidden(True)
        self.search_label.setText("Advanced Search")
        self.target_search_btn.setHidden(True)
        self.target_label.setHidden(True)
        self.adv_select_comboBox.setHidden(False)
        self.adv_search_input.setHidden(False)
        self.advanced_search_btn.setHidden(True)
        self.adv_search_learn_more_label.setHidden(False)
        self.add_advanced_search_btn.setHidden(False)
        self.undo_advanced_search_btn.setHidden(False)
        self.clear_advanced_search_btn.setHidden(False)
        self.target_screen_btn.setHidden(False)
   
        self.validation_label.setGeometry(10,155,300,30)
        self.target_search_result_scrollable_label.setGeometry(10,380,400,180)
        self.target_search_result_scrollable_label.setText(str(target_search_result))
        self.select_label.setGeometry(10,620,100,10)
        self.select_input.setGeometry(10,640,80,30)
        self.select_btn.setGeometry(100,640,50,30)

    # Component set 2 visibility function
    def cmp_2_visibility(self,bool):
        self.search_label.setHidden(bool)
        self.target_label.setHidden(bool)
        self.validation_label.setHidden(bool)
        self.target_search_btn.setHidden(bool)
        self.search_progressBar.setHidden(bool)
        self.mission_comboBox.setHidden(bool)
        self.target_search_input.setHidden(bool)
        self.advanced_search_btn.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component set 3
    #-------------------------------------------------------------------------------
    # Create Components
    def cmp_3_create(self,cmp_3_x_offset,cmp_3_y_offset):

        # Component set 3
        # Generating and displaying profile picture for the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.pfp_label  = QLabel(self)
        self.pfp_pixmap = QPixmap()
        pfp_url = self.create_url()

        try:
            request = requests.get(pfp_url)
            avatar = request.content
            network_status = True
            self.pfp_pixmap.loadFromData(avatar)
            self.pfp_label.setPixmap(self.pfp_pixmap.scaled(30,30,Qt.KeepAspectRatio))
            self.pfp_label.setGeometry(10+ cmp_3_x_offset,10+ cmp_3_y_offset,30,30)
            welcome_txt = "Welcome,\n" + username
        except:
            self.pfp_label.setText(":(")
            self.pfp_label.setFont(QFont(app_font,25))
            self.pfp_label.setGeometry(20+ cmp_3_x_offset,8+ cmp_3_y_offset,30,30)
            welcome_txt = "OOPS!\n" + "Check your connection!"
        # --------------------------------------------------------------------------

        # Welcome label to welcome the user in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.welcome_label = QLabel(welcome_txt,self)
        self.welcome_label.setFont(QFont(app_font,12))
        self.welcome_label.setGeometry(50+ cmp_3_x_offset,0+ cmp_3_y_offset,300,50)
       
    # Generate url for profile picture for Exo-Planet Detection screen
    def create_url(self):
        url = 'https://avatars.dicebear.com/api/bottts/' + username + '.svg?background=%23' + background_color_hex
        return url

    # Component set 3 visibility function
    def cmp_3_visibility(self,bool):
        self.pfp_label.setHidden(bool)
        self.welcome_label.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component set 4
    #-------------------------------------------------------------------------------
    # Create component 4
    def cmp_4_create(self,cmp_4_x_offset,cmp_4_y_offset):

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
      
    # Switch plot according to selected radio button  
    def switch_plot_radio_clicked(self):
        global current_selected_plot_type
        if self.line_radioBtn.isChecked() == True:
            self.target_plot.update_plot(0,current_selected_plot)
            current_selected_plot_type = 0
        elif self.scatter_radioBtn.isChecked() == True:
            self.target_plot.update_plot(1,current_selected_plot)
            current_selected_plot_type = 1
        else:
            self.target_plot.update_plot(2,current_selected_plot)
            current_selected_plot_type = 2

    # Component 4 visibility
    def cmp_4_visibility(self,bool):
        self.line_type_label.setHidden(bool)
        self.line_radioBtn.setHidden(bool)
        self.error_radioBtn.setHidden(bool)
        self.scatter_radioBtn.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component 5 
    #-------------------------------------------------------------------------------
    # Create component 5
    def cmp_5_create(self,cmp_5_x_offset,cmp_5_y_offset):
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
        self.adv_selected_parameters_scrollLabel = ScrollLabel(self)
        self.adv_selected_parameters_scrollLabel.setGeometry(10+cmp_5_x_offset,175+cmp_5_y_offset,400,100)
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
    
    # Parameter select data type validaion message in advanced search in  the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def adv_search_parameter_select_clicked(self):
    
        if self.adv_select_comboBox.currentIndex() < 4 :
            self.adv_search_input.setPlaceholderText("Input integers to search " + self.adv_select_comboBox.currentText())
        elif self.adv_select_comboBox.currentIndex() < 12 :
            self.adv_search_input.setPlaceholderText("Input float to search " + self.adv_select_comboBox.currentText())
        elif self.adv_select_comboBox.currentIndex() < 13 :
            self.adv_search_input.setPlaceholderText("Input boolean(True/False) to search " + self.adv_select_comboBox.currentText())
        else: 
            self.adv_search_input.setPlaceholderText("Input string to search " + self.adv_select_comboBox.currentText()) 

    # Add parameter button click function in advanced search in  the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def adv_search_add_clicked(self):
        global target_search_result_copy
        global parameters_text
        global filter_array

        self.validation_label.setGeometry(10,155,300,30)

        if len(self.adv_search_input.text()) == 0:
                self.validation_label.setText("Field empty! Enter parameter value")
        else:
            try:
                config_exists = False
                for x in parameters_text:
                    if x  == (self.adv_select_comboBox.currentText() + " value :" + self.adv_search_input.text() + "\n") :
                        self.validation_label.setText("Configuration already exists")
                        config_exists = True
                if config_exists == False:
                    if self.adv_select_comboBox.currentIndex() < 4 :
                        filter = np.where(target_search_result_copy.table[self.adv_select_comboBox.currentText()] == int(self.adv_search_input.text()))[0]
                    elif self.adv_select_comboBox.currentIndex() < 12 :
                        filter = np.where(target_search_result_copy.table[self.adv_select_comboBox.currentText()] == float(self.adv_search_input.text()))[0]
                    elif self.adv_select_comboBox.currentIndex() < 13 :
                        filter = np.where(target_search_result_copy.table[self.adv_select_comboBox.currentText()] == bool(self.adv_search_input.text()))[0]
                    else: 
                        filter = np.where(target_search_result_copy.table[self.adv_select_comboBox.currentText()] == self.adv_search_input.text())[0]
                    
                    filter_array.append(filter)
                    target_search_result_copy = target_search_result

                    for x in filter_array:
                        target_search_result_copy = target_search_result_copy[x]

                    self.validation_label.setText("Updated search results")
                    self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
                    parameters_text.append(self.adv_select_comboBox.currentText() + " value :" + self.adv_search_input.text() + "\n")
                    self.update_parameters_display()
                    self.target_search_result_scrollable_label.setText(str(target_search_result_copy))
                    self.adv_search_parameter_select_clicked()
            except:
                self.validation_label.setText("Invalid datatype entered")

    # Undo function in advanced search in Exo-Detection Screen
    # -------------------------------------------------------------------------- 
    def adv_search_undo_clicked(self):
        global parameters_text
        global filter_array
        global target_search_result_copy

        try:
            parameters_text.pop()
            filter_array.pop()
            self.validation_label.setText("Undo applied")
        except:
            self.validation_label.setText("Nothing to undo")

        target_search_result_copy = target_search_result

        for x in filter_array:
            target_search_result_copy = target_search_result_copy[x]

        
        self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
        self.update_parameters_display()
        self.target_search_result_scrollable_label.setText(str(target_search_result_copy))
              
    # Target search button click function in the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def target_screen_clicked(self):
        global window
        if self.window is None:
            window.close()
            window = ExoDetection()
        window.show()
   
    # component 5 visibility
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
        self.adv_selected_parameters_scrollLabel.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component 6
    #-------------------------------------------------------------------------------
    def cmp_6_create(self,cmp_6_x_offset,cmp_6_y_offset):
        # Search output for targed id in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_search_result_scrollable_label = ScrollLabel(self)
        self.target_search_result_scrollable_label.setGeometry(10 + cmp_6_x_offset, 10 + cmp_6_y_offset , 400, 180)
        
    def cmp_6_visibility(self,bool):
        self.target_search_result_scrollable_label.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component 7
    #-------------------------------------------------------------------------------
    def cmp_7_create(self,cmp_7_x_offset,cmp_7_y_offset):

        # Button to select Sector Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.sector_btn = QPushButton("Sector Analysis",self)
        self.sector_btn.setGeometry(10+cmp_7_x_offset,10+ cmp_7_y_offset, 150, 20)
        self.sector_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.sector_btn.clicked.connect(self.sector_clicked)
        # --------------------------------------------------------------------------

        # Button to select Exoplanet Detection in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.detection_btn = QPushButton("Exoplanet Detection",self)
        self.detection_btn.setGeometry(10+cmp_7_x_offset, 40+ cmp_7_y_offset, 150, 20)
        self.detection_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.detection_btn.clicked.connect(self.detection_clicked)
    
    # Button to select False Positive Analaysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.falsePositive_btn = QPushButton("False Positive Analysis",self)
        self.falsePositive_btn.setGeometry(10+cmp_7_x_offset, 70+ cmp_7_y_offset, 150, 20)
        self.falsePositive_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.falsePositive_btn.clicked.connect(self.falsePositiveClicked)

    # Sector button click function in the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def sector_clicked(self):
        self.falsePositive_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.detection_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.sector_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_alt_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.cmp_1_visibility(False)
        self.cmp_4_visibility(False)
        self.cmp_12_visibility(True)
        self.cmp_15_visibility(True)

    # Detection button click function in the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def detection_clicked(self):
        self.falsePositive_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.detection_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_alt_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.sector_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.cmp_1_visibility(True)
        self.cmp_4_visibility(False)
        self.cmp_12_visibility(False)
        self.cmp_15_visibility(True)
    
    # False Positive button click function in the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def falsePositiveClicked(self):
        self.falsePositive_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_alt_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.detection_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.sector_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.cmp_12_visibility(True)
        self.cmp_4_visibility(True)
        self.cmp_1_visibility(True)
        self.cmp_15_visibility(False)

    def cmp_7_visibility(self,bool):
        self.sector_btn.setHidden(bool)
        self.detection_btn.setHidden(bool)  
        self.falsePositive_btn.setHidden(bool)  
    #-------------------------------------------------------------------------------

    # Component 8
    #-------------------------------------------------------------------------------
    # Create component
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
        
    # select sector from search results
    def select_clicked(self):
        global lightcurve
        global select_input
        select_valid = True
        self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
     
        if filtered == True :
            self.validation_label.setGeometry(10,155,300,30)
        else:
            self.validation_label.setGeometry(10,140,300,30)

        try :
            if filtered == False:
                if len(target_search_result) < 1 :
                    self.validation_label.setText("!! No items to select from, search again !!")
                    select_valid = False
            else:
                if len(target_search_result_copy) < 1 :
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
                if filtered == True:
                    if (int(self.select_input.text().strip()) > len(target_search_result_copy)-1) or (int(self.select_input.text().strip()) < 0) :
                        select_valid = False
                        self.validation_label.setText("!! Please input within range !!")
                else:
                    if (int(self.select_input.text().strip()) > len(target_search_result)-1) or (int(self.select_input.text().strip()) < 0) :
                        select_valid = False
                        self.validation_label.setText("!! Please input within range !!")
            except:
                pass
        
        if select_valid == True:

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

            self.search_progressBar.setGeometry(160,370,144,30)
            self.search_progressBar.setHidden(False)
            self.validation_label.setGeometry(160,387,300,30)
            self.validation_label.setText("Downloading Lightcurve")

    # Component visibility
    def cmp_8_visibility(self,bool):
        self.select_label.setHidden(bool)
        self.select_btn.setHidden(bool)
        self.select_input.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component 9
    #-------------------------------------------------------------------------------
    def cmp_9_create(self,cmp_9_x_offset,cmp_9_y_offset):
        # Plot Area to display the plots after selecting a sector
        # --------------------------------------------------------------------------
        self.target_plot = PlotArea(self)
        self.target_plot.setGeometry(10 + cmp_9_x_offset,10 + cmp_9_y_offset, 830, 500)
    
    def cmp_9_visibility(self,bool):
        self.target_plot.setHidden(bool)
    #-------------------------------------------------------------------------------
   
    # Component 10
    #-------------------------------------------------------------------------------
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
    
    # Back button click function to take to select screen from the Habitability screen
    # --------------------------------------------------------------------------
    def back_click(self):
        global window
        if self.window is None:
            window.close()
            window = Select()
        window.show()
    
    def cmp_10_visibility(self,bool):
        self.back_btn.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component 11
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
        self.lgout_btn.setGeometry(10+cmp_11_x_offset,10+cmp_11_y_offset,30,30) #410
        self.lgout_btn.clicked.connect(self.login_click)
    
    # logout button click function to take to the login screen from the Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def login_click(self):
        global window
        if self.window is None:
            window.close()
            window = Login()
        window.show()
        
    def cmp_11_visibility(self,bool):
        self.lgout_btn.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component 12
    def cmp_12_create(self,cmp_12_x_offset,cmp_12_y_offset):
        
        # Label to show "BLS Analysis" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bls_analysis_label = QLabel("BLS Analysis" , self)
        self.bls_analysis_label.setGeometry(920+ cmp_12_x_offset, 500+ cmp_12_y_offset, 150, 20)
        self.bls_analysis_label.setStyleSheet("color:#" + button_hover_hex + ";")
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
        self.bls_plot_btn.clicked.connect(self.bls_btn_clicked)
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
        self.bls_fold_plot_btn.clicked.connect(self.bls_fold_plot_btn_clicked)
        self.bls_fold_plot_btn.setEnabled(False)
        # --------------------------------------------------------------------------

        # Button for ML Prediction in Exo-Detection Screen 
        # --------------------------------------------------------------------------
        self.ml_btn = QPushButton("Predict with ML",self)
        self.ml_btn.setGeometry(1250+cmp_12_x_offset, 500+cmp_12_y_offset, 150, 20)
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
        self.ml_btn.clicked.connect(self.ml_predict)

        self.ml_label = QLabel(self)
        self.ml_label.setGeometry(1230+cmp_12_x_offset, 530+cmp_12_y_offset, 300, 50)
        self.ml_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------
    
    def cmp_12_visibility(self,bool):
        self.bls_analysis_label.setHidden(bool)
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
        self.ml_label.setHidden(bool)

     # Produce BLS analysis results on button click
    # --------------------------------------------------------------------------
    def bls_btn_clicked(self):
        global bls_fold_clicked
        global fold_period
        global fold_freq
        global current_selected_plot

        try:
            fold_period = float(self.bls_period_input.text())
            fold_freq = float(self.bls_freq_input.text())

            if self.line_radioBtn.isChecked() == True:
                self.target_plot.update_plot(0,5)
            elif self.scatter_radioBtn.isChecked() == True:
                self.target_plot.update_plot(1,5)
            else:
                self.target_plot.update_plot(2,5)

            self.bls_results_period_label.setText("Period : " + str(round(bls_period.value,4)))
            self.bls_results_transit_label.setText("Transit Time : " + str(round(bls_transit.value,4)))
            self.bls_results_duration_label.setText("duration : " + str(round(bls_duration.value,4)))

            current_selected_plot = 5

            if bls_period > 0 :
                self.bls_fold_plot_btn.setEnabled(True)
                self.ml_btn.setEnabled(True)
                bls_fold_clicked = False


        except:
            print("wrong data types or invalid inputs")
        
    # --------------------------------------------------------------------------

    # Show BLS Phase fold plot on button click
    # --------------------------------------------------------------------------
    def bls_fold_plot_btn_clicked(self):
        global bls_fold_clicked
        global current_selected_plot

        self.bls_fold_plot_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_alt_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)

        if self.line_radioBtn.isChecked() == True:
            self.target_plot.update_plot(0,6)
        elif self.scatter_radioBtn.isChecked() == True:
            self.target_plot.update_plot(1,6)
        else:
            self.target_plot.update_plot(2,6)
        
        current_selected_plot = 6
        
        bls_fold_clicked = True
    # --------------------------------------------------------------------------
    
    # Update parameters display when new parameters are added to the filter in the advanced search in Exo-Detection Screen
    # --------------------------------------------------------------------------    
    def update_parameters_display(self):
        parameters_display_text = ""
        for x in parameters_text:
            parameters_display_text = parameters_display_text + x
        self.adv_selected_parameters_scrollLabel.setText(parameters_display_text)
     
    # Display search results after search complete in Exo-Planet detection screen
    # --------------------------------------------------------------------------
    def update_search_results(self):
        global search_result_isDownloaded_error
        self.validation_label.setGeometry(10,140,300,30)
        self.validation_label.setStyleSheet("color:#" + logout_color_hex + ";")

        self.search_progressBar.setHidden(True)
        if search_result_isDownloaded_error == False:
            self.validation_label.setText("Here's what we found")
            self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
            self.setFixedHeight(420)
            self.target_search_result_scrollable_label.setText(str(target_search_result))
            self.target_search_result_scrollable_label.setHidden(False) 
        else:
            self.target_search_result_scrollable_label.setHidden(True)
            self.setFixedHeight(170)
            self.validation_label.setText("!! A working network connection is required !!")
            self.validation_label.setStyleSheet("color:#" + logout_color_hex + ";")

        self.target_search_btn.setEnabled(True)

        try:
            if len(target_search_result) > 0 :
                self.advanced_search_btn.setHidden(False)
                self.advanced_search_btn.setEnabled(True) 
        except:
            pass
        
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
    
    # function to update plot 
    # --------------------------------------------------------------------------
    def update_plot(self):
        global search_result_select_isDownloaded_error
        
        self.target_plot.update_plot(0,0)
        self.search_progressBar.setHidden(True)
        if search_result_select_isDownloaded_error == False:
            self.validation_label.setText("Download Complete")
            self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
            self.setFixedWidth(1300)
            self.target_plot.setHidden(False)
           
        else:
            self.validation_label.setGeometry(10,140,300,30)
            self.validation_label.setText("!! A working network connection is required !!")
            self.validation_label.setStyleSheet("color:#" + logout_color_hex + ";")

        self.target_search_btn.setEnabled(True)
        self.advanced_search_btn.setEnabled(True)
        self.select_btn.setEnabled(True) 
        self.adv_clicked()

    # function to predict using ML models
    # --------------------------------------------------------------------------
    def ml_predict(self):
        if pro == True:
            data_period = bls_period.value
            data_epoch = bls_transit.value
            data_duration = bls_duration.value

            lcs = lk.search_lightcurve(lightcurve.label,author=lightcurve.author,cadence='long').download_all()
            lc = lcs.stitch()
            lc_clean = lc.remove_outliers(sigma=20, sigma_upper=4)
            temp_fold = lc_clean.fold(data_period, epoch_time=data_epoch)
            fractional_duration = (data_duration / 24.0) / data_period
            phase_mask = np.abs(temp_fold.phase.value) < (fractional_duration * 1.5)
            transit_mask = np.in1d(lc_clean.time.value, temp_fold.time_original.value[phase_mask])
            lc_flat, trend_lc = lc_clean.flatten(return_trend=True, mask=transit_mask)
            lc_fold = lc_flat.fold(data_period, epoch_time=data_epoch)
            lc_global = lc_fold.bin(time_bin_size=0.005).normalize() - 1
            lc_global = (lc_global / np.abs(lc_global.flux.min()) ) * 2.0 + 1
            lc_global.scatter()

            phase_mask = (lc_fold.phase > -4*fractional_duration) & (lc_fold.phase < 4.0*fractional_duration)
            lc_zoom = lc_fold[phase_mask]
            lc_local = lc_zoom.bin(time_bin_size=0.0005).normalize() - 1
            lc_local = (lc_local / np.abs(np.nanmin(lc_local.flux)) ) * 2.0 + 1

            array_all = []

            global_lc = []
            local_lc = []

            for x in range(0,len(lc_global.flux),10):
                try:
                    global_lc.append(lc_global.flux[x])
                except:
                    break

            for x in range(0,len(lc_local.flux)):
                try:
                    local_lc.append(lc_local.flux[x])
                except:
                    break
            
            with open(os.path.join(sys.path[0],'Models/RFM_G_model_pkl') , 'rb') as f:
                global_model = pickle.load(f)

            with open(os.path.join(sys.path[0],'Models/RFM_L_model_pkl') , 'rb') as f:
                local_model = pickle.load(f)

            #-----------------------------------------

            for i in range(len(global_lc),17134):
                global_lc.append(-999)

            df_global = pd.DataFrame(global_lc)
            df_global = df_global.fillna(-999)

            global_lc = []
            for x in df_global[0] :
                global_lc.append(x)

            for i in range(len(local_lc),2773):
                local_lc.append(-999)

            df_local = pd.DataFrame(local_lc)
            df_local = df_local.fillna(-999)

            local_lc = []
            for x in df_local[0] :
                local_lc.append(x)

        
            g = global_model.predict([global_lc])
            l = local_model.predict([local_lc])

            if g[0] ==1 and l[0] ==1 :
                self.ml_label.setText("Very likely to be an exoplanet!")
            elif g[0]==1 or l[0]==1 :
                self.ml_label.setText("Likely to be an exoplanet transit,\nRequires further analysis to confirm")
            else :
                self.ml_label.setText("Not likely to be an exoplanet")
        else:
            self.ml_label.setText("Must be a Pro User for \nML Prediction")
    
    def cmp_15_create(self,cmp_7_x_offset,cmp_7_y_offset):

        # Label to show "Plot Target Pixel File" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.tp_label = QLabel("Plot Target Pixel File" , self)
        self.tp_label.setGeometry(20 + cmp_7_x_offset, 10 + cmp_7_y_offset, 150, 20)
        self.tp_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Button to select Sector Analysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.tpImage_btn = QPushButton("Plot TP Image",self)
        self.tpImage_btn.setGeometry(10+cmp_7_x_offset,40+ cmp_7_y_offset, 150, 20)
        self.tpImage_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.tpImage_btn.clicked.connect(self.plotTP)
        # --------------------------------------------------------------------------

        # Label to show "Plot Light Curve" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.lc_label = QLabel("Plot Light Curve" , self)
        self.lc_label.setGeometry(180 + cmp_7_x_offset, 10 + cmp_7_y_offset, 150, 20)
        self.lc_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Button to select Exoplanet Detection in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.lc_btn = QPushButton("Plot Light Curve",self)
        self.lc_btn.setGeometry(170+cmp_7_x_offset, 40+ cmp_7_y_offset, 150, 20)
        self.lc_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.lc_btn.clicked.connect(self.plotLC)

        # Label to show "Plot Background Flux" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bf_label = QLabel("Plot Background Flux" , self)
        self.bf_label.setGeometry(340 + cmp_7_x_offset, 10 + cmp_7_y_offset, 150, 20)
        self.bf_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Button to select False Positive Analaysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bf_btn = QPushButton("Background Flux",self)
        self.bf_btn.setGeometry(330+cmp_7_x_offset, 40+ cmp_7_y_offset, 150, 20)
        self.bf_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.bf_btn.clicked.connect(self.plotBF)

        # Label to show "Plot Background Flux" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bft_label = QLabel("Plot Background Flux At \nTransit" , self)
        self.bft_label.setGeometry(500 + cmp_7_x_offset, -5 + cmp_7_y_offset, 150, 50)
        self.bft_label.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        # Label to show "Transit Time" for plots in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.transitTimeLabel = QLabel("Transit Time" , self)
        self.transitTimeLabel.setGeometry(500 + cmp_7_x_offset, 35 + cmp_7_y_offset, 150, 50)
        self.transitTimeLabel.setStyleSheet("color:#" + button_hover_hex + ";")
        # --------------------------------------------------------------------------

        #  Input Transit Time
        # --------------------------------------------------------------------------
        self.transitTime_input = QLineEdit(self)
        self.transitTime_input.setFont(QFont(app_font,15))
        self.transitTime_input.setPlaceholderText(" eg: 1518.2 ")
        self.transitTime_input.setStyleSheet("""
                                QLineEdit {
                                    border-radius:10px;
                                    background-color: #ffffff;
                                    color: #000000;
                                    }
                                """)
        self.transitTime_input.setGeometry(580+ cmp_7_x_offset,50+ cmp_7_y_offset,80,20)
        self.transitTime_input.setAlignment(Qt.AlignCenter)
        # --------------------------------------------------------------------------

        # Button to select False Positive Analaysis in Exo-Detection Screen
        # --------------------------------------------------------------------------
        self.bft_btn = QPushButton("Background Flux At Transit",self)
        self.bft_btn.setGeometry(490+cmp_7_x_offset, 80+ cmp_7_y_offset, 170, 20)
        self.bft_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        self.bft_btn.clicked.connect(self.plotBFT)
    
    def plotTP(self):
        self.target_plot.plotTargetPixelFile()

    def plotLC(self):
        self.target_plot.plotLightCurve()
    
    def plotBF(self):
        self.target_plot.backgroundFlux()
    
    def plotBFT(self):
        self.target_plot.backgroundFluxAtTransitEvent()

    def cmp_15_visibility(self,bool):
        self.transitTime_input.setHidden(bool)
        self.transitTimeLabel.setHidden(bool)
        self.lc_label.setHidden(bool)
        self.tp_label.setHidden(bool)
        self.bf_label.setHidden(bool)
        self.bft_label.setHidden(bool)
        self.bf_btn.setHidden(bool)
        self.bft_btn.setHidden(bool)
        self.tpImage_btn.setHidden(bool)
        self.lc_btn.setHidden(bool)

# Class for sign up screen
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
        self.setStyleSheet("background-color: #" + background_color_hex + ";")
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
        self.welcome_msg.setFont(QFont(app_font,20))
        self.welcome_msg.setGeometry((width/2)-170,100,300,30)
        # --------------------------------------------------------------------------
        
        # Input email in signup screen
        # --------------------------------------------------------------------------
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText(" Email")
        self.email_input.setGeometry((width/2)-150,140,300,30)
        self.email_input.setStyleSheet(("""
                                    QLineEdit {
                                        border: 0.1px solid #dadada;
                                        border-radius: 7px;
                                    }
                                    QLineEdit:focus{
                                        border: 1px solid #dadada;
                                        border-radius: 7px;
                                    }
                                    """))
        # --------------------------------------------------------------------------

        # Input password in signup screen
        # --------------------------------------------------------------------------
        self.pass_input = QLineEdit(self)
        self.pass_input.setPlaceholderText(" Password")
        self.pass_input.setEchoMode(PySide6.QtWidgets.QLineEdit.Password)
        self.pass_input.setGeometry((width/2)-150,190,300,30)
        self.pass_input.setStyleSheet(("""
                                    QLineEdit {
                                        border: 0.1px solid #dadada;
                                        border-radius: 7px;
                                    }
                                    QLineEdit:focus{
                                        border: 1px solid #dadada;
                                        border-radius: 7px;
                                    }
                                    """))
        # --------------------------------------------------------------------------

        # Re-Input password in signup screen
        # --------------------------------------------------------------------------
        self.repass_input = QLineEdit(self)
        self.repass_input.setPlaceholderText(" Re-enter Password")
        self.repass_input.setEchoMode(PySide6.QtWidgets.QLineEdit.Password)
        self.repass_input.setStyleSheet(("""
                                    QLineEdit {
                                        border: 0.1px solid #dadada;
                                        border-radius: 7px;
                                    }
                                    QLineEdit:focus{
                                        border: 1px solid #dadada;
                                        border-radius: 7px;
                                    }
                                    """))
        self.repass_input.setGeometry((width/2)-150,240,300,30)
        # --------------------------------------------------------------------------

        # Signup validation label in signup screen
        # --------------------------------------------------------------------------
        self.validation_msg = QLabel("",self)
        self.validation_msg.setFont(QFont(app_font,12))
        self.validation_msg.setStyleSheet("color: #e84f61")
        self.validation_msg.setGeometry((width/2)-150,274,300,25)
        # --------------------------------------------------------------------------

        # Signup button in signup screen
        # --------------------------------------------------------------------------
        self.signup_btn = QPushButton("Sign Up",self)
        self.signup_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
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
                                    background-color: #""" + button_alt_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
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

# Class for select screen
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
        self.setStyleSheet("background-color: #" + background_color_hex + ";")

    # url creator for profile picture in select screen
    # --------------------------------------------------------------------------
    def create_url(self):
        url = 'https://avatars.dicebear.com/api/bottts/' + username + '.svg?background=%23' + background_color_hex
        return url
    # --------------------------------------------------------------------------
    
    # Creating widgets for select screen 
    # --------------------------------------------------------------------------
    def create_widgets(self):

        # Component Offsets
        # --------------------------------------------------------------------------
        cmp_3_x_offset = 40
        cmp_3_y_offset = 0
        # --------------------------------------------------------------------------

        global avatar
        global pfp_load
        global network_status

        # Welcome label to greet user in select screen
        # --------------------------------------------------------------------------
        self.hello_label = QLabel(self)
        self.hello_label.setFont(QFont(app_font,12))
        self.hello_label.setGeometry((width/2)-100,0,300,50)
        # --------------------------------------------------------------------------

        # Component set 3
        ###########################################################################
        # Generating and displaying profile picture for the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.pfp_label  = QLabel(self)
        self.pfp_pixmap = QPixmap()
        pfp_url = self.create_url()

        try:
            request = requests.get(pfp_url)
            avatar = request.content
            network_status = True
            self.pfp_pixmap.loadFromData(avatar)
            self.pfp_label.setPixmap(self.pfp_pixmap.scaled(30,30,Qt.KeepAspectRatio))
            self.pfp_label.setGeometry(10+ cmp_3_x_offset,10+ cmp_3_y_offset,30,30)
            welcome_txt = "Welcome,\n" + username
        except:
            self.pfp_label.setText(":(")
            self.pfp_label.setFont(QFont(app_font,25))
            self.pfp_label.setGeometry(20+ cmp_3_x_offset,8+ cmp_3_y_offset,30,30)
            welcome_txt = "OOPS!\n" + "Check your connection!"
        # --------------------------------------------------------------------------

        # Welcome label to welcome the user in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.welcome_label = QLabel(welcome_txt,self)
        self.welcome_label.setFont(QFont(app_font,12))
        self.welcome_label.setGeometry(50+ cmp_3_x_offset,0+ cmp_3_y_offset,300,50)
        # --------------------------------------------------------------------------
        ###########################################################################

        # Habitability title in select screen
        # --------------------------------------------------------------------------
        self.hab_title = QLabel("Habitability Detection",self)
        self.hab_title.setFont(QFont(app_font,20))
        self.hab_title.setGeometry((width/2)-150,60,300,30)
        # --------------------------------------------------------------------------
        
        # Habitability description in select screen
        # --------------------------------------------------------------------------
        self.hab_desc = QLabel("Detect habitability using bls results calculated during\ndetection.Radius,Semi-Major-Axis and Equilibrium \ntemperatures can be calculated for different\nalbedo values",self)
        self.hab_desc.setFont(QFont(app_font,12))
        self.hab_desc.setGeometry((width/2)-150,90,300,110)
        # --------------------------------------------------------------------------
        
        # Habitability button in select screen
        # --------------------------------------------------------------------------
        habitability_btn = QPushButton("Start Habitability Detection",self)
        habitability_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
                                    color: #000000
                                    }
                                """)
        habitability_btn.setGeometry((width/2)-150,200,300,30)
        habitability_btn.clicked.connect(self.hab_click)
        # --------------------------------------------------------------------------

        # Exo-Planet detection title in select screen
        # --------------------------------------------------------------------------
        self.exo_title = QLabel("Exoplanet Detection",self)
        self.exo_title.setFont(QFont(app_font,20))
        self.exo_title.setGeometry((width/2)-150,240,300,30)
        # --------------------------------------------------------------------------
        
        # Exo-Planet detecttion description in select screen
        # --------------------------------------------------------------------------
        self.exo_desc = QLabel("Light-curves,binned and \nfolded graphs can be generated and the BLS\nanalysis can be conducted, and results from BLS can\nbe passed to an ML Prediction Model to \ndetect if it is an exoplanet or a false positive.",self)
        self.exo_desc.setFont(QFont(app_font,12))
        self.exo_desc.setGeometry((width/2)-150,270,300,110)
        # --------------------------------------------------------------------------

        # Exo-Planet detection button in select screen
        # --------------------------------------------------------------------------
        Detection_btn= QPushButton("Start Exoplanet Detection",self)
        Detection_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_alt_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
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
                                    background-color: #""" + logout_color_hex + """;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
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
        global window
        if self.window is None:
            window.close()
            window = Habitability()
        window.show()
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

# Class for habitability screen
# --------------------------------------------------------------------------
class Habitability(QWidget):

    # Initialize Exo-Planet Detection screen
    # --------------------------------------------------------------------------
    def __init__(self, parent=None):
        super().__init__()
        global width,height

        self.window = None
        width = 450
        height = 180
        self.setWindowTitle("Habitability - Planet Hunters")
        self.setFixedHeight(height)
        self.setFixedWidth(width)
        self.create_widgets()
        self.setStyleSheet("background-color: #" + background_color_hex +";")

    def create_widgets(self):

        global filtered
        global username
        global avatar
        global pfp_load 
        global network_status 

        # Components set 2
        self.cmp_2_create(0,35)
        self.search_progressBar.setHidden(True)

        # Component set 3
        self.cmp_3_create(40,0)

        # Enable and disable filter button depending on length of search result
        # -------------------------------------------------------------------------
        try:
            if len(target_search_result) > 0 :
                self.advanced_search_btn.setEnabled(True)
            else:
                self.advanced_search_btn.setEnabled(False)
        except:
            self.advanced_search_btn.setEnabled(False)

        # Components set 5
        self.cmp_5_create(0,55)
        self.cmp_5_visibility(True)

        # Component set 6
        self.cmp_6_create(0,160)

        # Components set 8
        self.cmp_8_create(0,350)

        # Component set 9
        self.cmp_9_create(450,-13)

        # Component set 10
        self.cmp_10_create(0,0)

        # Component set 13
        self.cmp_13_create(0,0)

        try:
            self.target_search_input.setText(target_search_id)
            if len(target_search_result) > 0 :
                self.setFixedHeight(420)
                self.target_search_result_scrollable_label.setText(str(target_search_result))
                self.target_search_result_scrollable_label.setHidden(False)
        except:
            pass

        filtered = False
        
    # Component set 2
    #-------------------------------------------------------------------------------
    # Create components set 2
    def cmp_2_create(self,cmp_2_x_offset,cmp_2_y_offset):
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
        self.mission_comboBox = QComboBox(self)
        self.mission_comboBox.setGeometry(165+cmp_2_x_offset,55+cmp_2_y_offset,50,30)
        self.mission_comboBox.addItems(['All','Kepler','K2','TESS'
                                    ])
        self.mission_comboBox.setStyleSheet("""
                                QComboBox {
                                    border: 3px solid gray;
                                    border-radius: 5px;
                                    padding: 1px 18px 1px 3px;
                                    min-width: 4em;
                                }
                                """)
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
        self.target_search_btn.setGeometry(260+cmp_2_x_offset,55+cmp_2_y_offset,50,30)
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
        self.advanced_search_btn.setGeometry(315+cmp_2_x_offset,55+cmp_2_y_offset,120,30)
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
    
    # Search button click function for target search in the Habitability screen
    def search_clicked(self):
        global target_search_result_scrollable_label
        global target_search_id
        global target_search_result
        global search_result_isDownloaded_error
        global mission

        self.validation_label.setText("Searching..")
        self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")

        self.search_progressBar.setHidden(False)

        if self.target_search_input.text().strip() == "" :
            #self.setFixedHeight(180)
            self.validation_label.setText("!! Enter Target ID to search.\nTo search with other parameters use advanced search !!")
            self.search_progressBar.setHidden(True)
        else:
            target_search_id = self.target_search_input.text()
            mission = self.mission_comboBox.currentIndex()

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

    # Advanced search button click function in the Habitability screen
    # --------------------------------------------------------------------------
    def adv_clicked(self):
        global filtered

        filtered = True
        self.setFixedHeight(630)
        self.parameter_validation_label.setHidden(False)
        self.selected_parameters_label.setHidden(False)
        self.search_results_selected_parameters_label.setHidden(False)
        self.adv_selected_parameters_scrollLabel.setHidden(False)
        self.validation_label.setText("")
        self.target_search_input.setHidden(True)
        self.search_label.setText("Advanced Search")
        self.target_search_btn.setHidden(True)
        self.target_label.setHidden(True)
        self.adv_select_comboBox.setHidden(False)
        self.adv_search_input.setHidden(False)
        self.advanced_search_btn.setHidden(True)
        self.adv_search_learn_more_label.setHidden(False)
        self.add_advanced_search_btn.setHidden(False)
        self.undo_advanced_search_btn.setHidden(False)
        self.clear_advanced_search_btn.setHidden(False)
        self.target_screen_btn.setHidden(False)
   


        self.validation_label.setGeometry(10,155,300,30)
        self.target_search_result_scrollable_label.setGeometry(10,380,400,180)
        self.target_search_result_scrollable_label.setText(str(target_search_result))
        self.select_label.setGeometry(10,570,100,10)
        self.select_input.setGeometry(10,590,80,30)
        self.select_btn.setGeometry(100,590,50,30)

    # Component set 2 visibility function
    def cmp_2_visibility(self,bool):
        self.search_label.setHidden(bool)
        self.target_label.setHidden(bool)
        self.validation_label.setHidden(bool)
        self.target_search_btn.setHidden(bool)
        self.search_progressBar.setHidden(bool)
        self.mission_comboBox.setHidden(bool)
        self.target_search_input.setHidden(bool)
        self.advanced_search_btn.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component set 3
    #-------------------------------------------------------------------------------
    # Create Components
    def cmp_3_create(self,cmp_3_x_offset,cmp_3_y_offset):

        # Component set 3
        # Generating and displaying profile picture for the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.pfp_label  = QLabel(self)
        self.pfp_pixmap = QPixmap()
        pfp_url = self.create_url()

        try:
            request = requests.get(pfp_url)
            avatar = request.content
            network_status = True
            self.pfp_pixmap.loadFromData(avatar)
            self.pfp_label.setPixmap(self.pfp_pixmap.scaled(30,30,Qt.KeepAspectRatio))
            self.pfp_label.setGeometry(10+ cmp_3_x_offset,10+ cmp_3_y_offset,30,30)
            welcome_txt = "Welcome,\n" + username
        except:
            self.pfp_label.setText(":(")
            self.pfp_label.setFont(QFont(app_font,25))
            self.pfp_label.setGeometry(20+ cmp_3_x_offset,8+ cmp_3_y_offset,30,30)
            welcome_txt = "OOPS!\n" + "Check your connection!"
        # --------------------------------------------------------------------------

        # Welcome label to welcome the user in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.welcome_label = QLabel(welcome_txt,self)
        self.welcome_label.setFont(QFont(app_font,12))
        self.welcome_label.setGeometry(50+ cmp_3_x_offset,0+ cmp_3_y_offset,300,50)
       
    # Generate url for profile picture for Habitability screen
    def create_url(self):
        url = 'https://avatars.dicebear.com/api/bottts/' + username + '.svg?background=%23' + background_color_hex
        return url

    # Component set 3 visibility function
    def cmp_3_visibility(self,bool):
        self.pfp_label.setHidden(bool)
        self.welcome_label.setHidden(bool)
    #-------------------------------------------------------------------------------

     # Component 5 
    #-------------------------------------------------------------------------------
    # Create component 5
    def cmp_5_create(self,cmp_5_x_offset,cmp_5_y_offset):
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
        self.adv_selected_parameters_scrollLabel = ScrollLabel(self)
        self.adv_selected_parameters_scrollLabel.setGeometry(10+cmp_5_x_offset,175+cmp_5_y_offset,400,100)
        # --------------------------------------------------------------------------

        # Search results label for advaned search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.search_results_selected_parameters_label = QLabel("Search results: ",self)
        self.search_results_selected_parameters_label.setGeometry(10+cmp_5_x_offset,305+cmp_5_y_offset,200,10)
        # --------------------------------------------------------------------------

         
        # Target search button for advanced search in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_screen_btn = QPushButton("Back To Habitability Search",self)
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
    
    # Parameter select data type validaion message in advanced search in the Habitability screen
    # --------------------------------------------------------------------------
    def adv_search_parameter_select_clicked(self):
    
        if self.adv_select_comboBox.currentIndex() < 4 :
            self.adv_search_input.setPlaceholderText("Input integers to search " + self.adv_select_comboBox.currentText())
        elif self.adv_select_comboBox.currentIndex() < 12 :
            self.adv_search_input.setPlaceholderText("Input float to search " + self.adv_select_comboBox.currentText())
        elif self.adv_select_comboBox.currentIndex() < 13 :
            self.adv_search_input.setPlaceholderText("Input boolean(True/False) to search " + self.adv_select_comboBox.currentText())
        else: 
            self.adv_search_input.setPlaceholderText("Input string to search " + self.adv_select_comboBox.currentText()) 

    # Add parameter button click function in advanced search in the Habitability screen
    # --------------------------------------------------------------------------
    def adv_search_add_clicked(self):
        global target_search_result_copy
        global parameters_text
        global filter_array

        self.validation_label.setGeometry(10,155,300,30)

        if len(self.adv_search_input.text()) == 0:
                self.validation_label.setText("Field empty! Enter parameter value")
        else:
            try:
                config_exists = False
                for x in parameters_text:
                    if x  == (self.adv_select_comboBox.currentText() + " value :" + self.adv_search_input.text() + "\n") :
                        self.validation_label.setText("Configuration already exists")
                        config_exists = True
                if config_exists == False:
                    if self.adv_select_comboBox.currentIndex() < 4 :
                        filter = np.where(target_search_result_copy.table[self.adv_select_comboBox.currentText()] == int(self.adv_search_input.text()))[0]
                    elif self.adv_select_comboBox.currentIndex() < 12 :
                        filter = np.where(target_search_result_copy.table[self.adv_select_comboBox.currentText()] == float(self.adv_search_input.text()))[0]
                    elif self.adv_select_comboBox.currentIndex() < 13 :
                        filter = np.where(target_search_result_copy.table[self.adv_select_comboBox.currentText()] == bool(self.adv_search_input.text()))[0]
                    else: 
                        filter = np.where(target_search_result_copy.table[self.adv_select_comboBox.currentText()] == self.adv_search_input.text())[0]
                    
                    filter_array.append(filter)
                    target_search_result_copy = target_search_result

                    for x in filter_array:
                        target_search_result_copy = target_search_result_copy[x]

                    self.validation_label.setText("Updated search results")
                    self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
                    parameters_text.append(self.adv_select_comboBox.currentText() + " value :" + self.adv_search_input.text() + "\n")
                    self.update_parameters_display()
                    self.target_search_result_scrollable_label.setText(str(target_search_result_copy))
                    self.adv_search_parameter_select_clicked()
            except:
                self.validation_label.setText("Invalid datatype entered")

    # Undo function in advanced search in Habitability Screen
    # -------------------------------------------------------------------------- 
    def adv_search_undo_clicked(self):
        global parameters_text
        global filter_array
        global target_search_result_copy

        try:
            parameters_text.pop()
            filter_array.pop()
            self.validation_label.setText("Undo applied")
        except:
            self.validation_label.setText("Nothing to undo")

        target_search_result_copy = target_search_result

        for x in filter_array:
            target_search_result_copy = target_search_result_copy[x]

        
        self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
        self.update_parameters_display()
        self.target_search_result_scrollable_label.setText(str(target_search_result_copy))
              
    # Target search button click function in the Habitability screen
    # --------------------------------------------------------------------------
    def target_screen_clicked(self):
        global window
        if self.window is None:
            window.close()
            window = Habitability()
        window.show()
   
    # component 5 visibility
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
        self.adv_selected_parameters_scrollLabel.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component 6
    #-------------------------------------------------------------------------------
    def cmp_6_create(self,cmp_6_x_offset,cmp_6_y_offset):
        # Search output for targed id in the Exo-Planet Detection screen
        # --------------------------------------------------------------------------
        self.target_search_result_scrollable_label = ScrollLabel(self)
        self.target_search_result_scrollable_label.setGeometry(10 + cmp_6_x_offset, 10 + cmp_6_y_offset , 400, 180)
        
    def cmp_6_visibility(self,bool):
        self.target_search_result_scrollable_label.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component 8
    #-------------------------------------------------------------------------------
    # Create component
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
        
    # select sector from search results
    def select_clicked(self):
        global lightcurve
        global select_input
        select_valid = True
        self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
     
        if filtered == True :
            self.validation_label.setGeometry(10,155,300,30)
        else:
            self.validation_label.setGeometry(10,140,300,30)

        try :
            if filtered == False:
                if len(target_search_result) < 1 :
                    self.validation_label.setText("!! No items to select from, search again !!")
                    select_valid = False
            else:
                if len(target_search_result_copy) < 1 :
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
                if filtered == True:
                    if (int(self.select_input.text().strip()) > len(target_search_result_copy)-1) or (int(self.select_input.text().strip()) < 0) :
                        select_valid = False
                        self.validation_label.setText("!! Please input within range !!")
                else:
                    if (int(self.select_input.text().strip()) > len(target_search_result)-1) or (int(self.select_input.text().strip()) < 0) :
                        select_valid = False
                        self.validation_label.setText("!! Please input within range !!")
            except:
                pass
        
        if select_valid == True:

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

            self.search_progressBar.setGeometry(160,370,144,30)
            self.search_progressBar.setHidden(False)
            self.validation_label.setGeometry(160,387,300,30)
            self.validation_label.setText("Downloading Lightcurve")

    # Component visibility
    def cmp_8_visibility(self,bool):
        self.select_label.setHidden(bool)
        self.select_btn.setHidden(bool)
        self.select_input.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component 9
    #-------------------------------------------------------------------------------
    def cmp_9_create(self,cmp_9_x_offset,cmp_9_y_offset):
        # Plot Area to display the plots after selecting a sector
        # --------------------------------------------------------------------------
        self.target_plot = PlotArea(self)
        self.target_plot.setGeometry(620, -3, 790, 460)
    
    def cmp_9_visibility(self,bool):
        self.target_plot.setHidden(bool)
    #-------------------------------------------------------------------------------

    # Component 10
    #-------------------------------------------------------------------------------
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
    
    def cmp_13_create(self,cmp_13_x_offset,cmp_13_y_offset):
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
        self.phase_fold_btn.clicked.connect(self.phase_fold)

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
        self.slider.setSliderPosition((ylim_min*1000000+ylim_max*1000000)/2)
        self.slider.sliderMoved.connect(self.slider_position)

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
        self.y_btn.clicked.connect(self.y_axis_change)


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
        self.x_btn.clicked.connect(self.x_axis_change)

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
        self.albedo_slider.sliderMoved.connect(self.albedo_position)

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
        self.calc_radius_btn.clicked.connect(self.calc_radius)

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

    # Display search results after search complete in Habitability screen
    # --------------------------------------------------------------------------
    def update_search_results(self):
        global search_result_isDownloaded_error
        self.validation_label.setGeometry(10,140,300,30)
        self.validation_label.setStyleSheet("color:#" + logout_color_hex + ";")

        self.search_progressBar.setHidden(True)
        if search_result_isDownloaded_error == False:
            self.validation_label.setText("Here's what we found")
            self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
            self.setFixedHeight(420)
            self.target_search_result_scrollable_label.setText(str(target_search_result))
            self.target_search_result_scrollable_label.setHidden(False) 
        else:
            self.target_search_result_scrollable_label.setHidden(True)
            self.setFixedHeight(170)
            self.validation_label.setText("!! A working network connection is required !!")
            self.validation_label.setStyleSheet("color:#" + logout_color_hex + ";")

        self.target_search_btn.setEnabled(True)

        try:
            if len(target_search_result) > 0 :
                self.advanced_search_btn.setHidden(False)
                self.advanced_search_btn.setEnabled(True) 
        except:
            pass
        
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
    
    # function to update plot 
    # --------------------------------------------------------------------------
    def update_plot(self):
        global search_result_select_isDownloaded_error
        
        self.target_plot.update_plot(0,0)
        self.search_progressBar.setHidden(True)
        if search_result_select_isDownloaded_error == False:
            self.validation_label.setText("Download Complete")
            self.validation_label.setStyleSheet("color: #" + button_hover_hex + ";")
            self.setFixedWidth(1420)
            self.setFixedHeight(750)
            self.target_plot.setHidden(False)
           
        else:
            self.validation_label.setGeometry(10,140,300,30)
            self.validation_label.setText("!! A working network connection is required !!")
            self.validation_label.setStyleSheet("color:#" + logout_color_hex + ";")

        self.target_search_btn.setEnabled(True)
        self.advanced_search_btn.setEnabled(True)
        self.select_btn.setEnabled(True) 
        self.adv_clicked()

    # Update parameters display when new parameters are added to the filter in the advanced search in Habitability Screen
    # --------------------------------------------------------------------------    
    def update_parameters_display(self):
        parameters_display_text = ""
        for x in parameters_text:
            parameters_display_text = parameters_display_text + x
        self.adv_selected_parameters_scrollLabel.setText(parameters_display_text)

    # Back button click function to take to select screen from the Habitability screen
    # --------------------------------------------------------------------------
    def back_click(self):
        global window
        if self.window is None:
            window.close()
            window = Select()
        window.show()
     
    def phase_fold(self):
        global lightcurve
        global lc_phased_binned
        global lc_phased

        lc_phased = lightcurve.fold(period = float(self.period_input.text()), epoch_time = float(self.epoch_input.text()))
        # bin the lightcurve to 15 minutes (divide by 24 and 60 to get into the units of days)
        lc_phased_binned = lc_phased.bin(15/24/60) #--------
        self.target_plot.update_plot(0,7)

    def x_axis_change(self):
        global xlim_min
        global xlim_max

        min = xlim_min
        max = xlim_max
        try:
            min = float(self.x_min_input.text())
            max = float(self.x_max_input.text())
        except:
            pass

        xlim_min = min
        xlim_max = max
        
        self.target_plot.update_plot(0,7)

    def y_axis_change(self):
        global ylim_min
        global ylim_max
        min = ylim_min
        max = ylim_max
        try:
            min = float(self.y_min_input.text())
            max = float(self.y_max_input.text())
        except:
            pass

        ylim_min = min
        ylim_max = max

        self.slider.setMinimum(ylim_min*1000000)
        self.slider.setMaximum(ylim_max*1000000)
        self.target_plot.update_plot((ylim_min*1000000 + ylim_max*1000000)/2,7)
        self.slider.setSliderPosition((ylim_min*1000000 + ylim_max*1000000)/2)

    def slider_position(self,p):
            global axhline_val
            axhline_val = p/1000000
            self.slider_label.setText('Adjust axhline : '+ str(p/1000000))
            self.target_plot.update_plot(p/1000000,8)
    
    def albedo_position(self,p):
        global albedo
        albedo = p/100
        self.albedo_label.setText("Planet Albedo : "+ str(albedo))
    
    def calc_radius(self):
        global albedo

        self.summary_period_label.setText("Period : " + self.period_input.text())
        self.summary_epoch_label.setText("Transit Epoch (t0) : " + self.epoch_input.text())
        self.summary_axhline_label.setText("Transit Depth (1 - Axhline) : " + format(1-axhline_val,'.4f'))
        self.summary_star_radius_label.setText("Star Radius : " + self.star_radius_input.text())
        self.summary_star_temp_label.setText("Star Temp :" +  self.star_eff_input.text())
        self.summary_planet_albedo_label.setText("Planet Alebedo :" + str(albedo) )

        transit_depth = 1 - axhline_val
        R_star = float(self.star_radius_input.text()) * u.Rsun

        r_pl_solar_radius = np.sqrt(transit_depth) * R_star
        r_pl_earth_radius = r_pl_solar_radius.to(u.Rearth)

        self.results_earth_label.setText("Radius as Earth Radius : " + str(r_pl_earth_radius))
        self.results_solar_label.setText("Radius as Solar Radius : " + str(r_pl_solar_radius))

        a = np.sqrt ((R_star + r_pl_solar_radius)**2) / np.sin (np.pi * 0.191  / float(self.period_input.text()))
        a_earth_radius = a.to(u.Rearth)

        self.results_axis_label.setText("Orbit Semi Major Axis as Solar Radius : "+ str(a))
        self.results_axis_earth_label.setText("Orbit Semi Major Axis as Earth Radius : "+ str(a_earth_radius))

        T_eff = float(self.star_eff_input.text())
        planet_albedo = albedo
        T_eq = T_eff * np.sqrt(R_star / (2 * a)) * (1 - planet_albedo)**0.25
        T_eq
        self.results_temp_label.setText("Equilibrium Temperature : "+ str(T_eq))
    # --------------------------------------------------------------------------
   
# Class for login screen
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

        #self.setWindowIcon(QIcon("Images/logo_small.png"))
        self.setWindowIcon(QIcon(r'Application\Product_GUI\Images\icon.png'))
        self.setWindowTitle("Log In - Planet Hunters")
        self.setFixedHeight(height)
        self.setFixedWidth(width)
        self.create_widgets()
        self.setStyleSheet("background-color: #" + background_color_hex + ";")

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
        joblib.dump([],os.path.join(sys.path[0],'loader_request.joblib'))
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
            self.welcome_msg = QLabel("Log In to Planet Hunters",self)
            self.welcome_msg.setAlignment(Qt.AlignCenter)
            self.welcome_msg.setGeometry((width/2)-150,110,300,30)
            self.welcome_msg.setStyleSheet("color: white;")
            self.welcome_msg.setFont(QFont(app_font,20))
            
        else:
            logo.setGeometry((width/2)-30,20,50,50)
            self.welcome_msg = QLabel("Thank you for signing up!\nyou can now log In to Planet Hunters",self)
            self.welcome_msg.setGeometry((width/2)-150,80,350,60)
            self.welcome_msg.setStyleSheet("color: white;")
            self.welcome_msg.setFont(QFont(app_font,15))
            sign_up = False
        # --------------------------------------------------------------------------

        # Email input textbox in login screen
        # --------------------------------------------------------------------------
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText(" Email")
        self.email_input.setStyleSheet("""
                                    QLineEdit {
                                        border: 0.1px solid #dadada;
                                        border-radius: 7px;
                                        color: white;
                                    }
                                    QLineEdit:focus{
                                        border: 1px solid #dadada;
                                        border-radius: 7px;
                                    }
                                    """)
        self.email_input.setGeometry((width/2)-150,150,300,30)
        # --------------------------------------------------------------------------

        # Password input textbox in login screen
        # --------------------------------------------------------------------------
        self.pass_input = QLineEdit(self)
        self.pass_input.setPlaceholderText(" Password")
        self.pass_input.setEchoMode(PySide6.QtWidgets.QLineEdit.Password)
        self.pass_input.setStyleSheet(("""
                                    QLineEdit {
                                        border: 0.1px solid #dadada;
                                        border-radius: 7px;
                                        color: white;
                                    }
                                    QLineEdit:focus{
                                        border: 1px solid #dadada;
                                        border-radius: 7px;
                                    }
                                    """))
        self.pass_input.setGeometry((width/2)-150,190,300,30)
        # --------------------------------------------------------------------------

        

        # Login validation label in login screen
        # --------------------------------------------------------------------------
        self.validation_msg = QLabel("",self)
        self.validation_msg.setFont(QFont(app_font,12))
        self.validation_msg.setStyleSheet("color: #e84f61")
        self.validation_msg.setGeometry((width/2)-150,225,300,30)
        # --------------------------------------------------------------------------

        # Remember me checkbox to remember the login details when app opened next time in login screen
        # --------------------------------------------------------------------------
        self.checkbox = QCheckBox("Remember Me", self)
        self.checkbox.setGeometry((width/2)-150,250,300,30)
        self.checkbox.setStyleSheet("color: white;")
        self.checkbox.setChecked(True)
        # --------------------------------------------------------------------------

        # Login button in login screen
        # --------------------------------------------------------------------------
        self.login_btn = QPushButton("Login",self)
        self.login_btn.setStyleSheet("""
                                QPushButton {
                                    border-radius:10px;
                                    background-color: #""" + button_color_hex + """;
                                    color: white;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
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
                                    background-color: #""" + button_alt_color_hex + """;
                                    color: white;
                                    }
                                QPushButton:hover {
                                    background-color: #""" + button_hover_hex + """;
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
        global db_username

        self.progress_bar_login.setHidden(False)
        self.login_label.setHidden(False)
            
        # Login validation with google api in login screen
        # --------------------------------------------------------------------------
        payload = json.dumps({
        "email": self.email_input.text(),
        "password": self.pass_input.text(),
        "returnSecureToken": True
        })

        # Login validation with google api in login screen
        # --------------------------------------------------------------------------
        db_username = self.email_input.text().lower()
        db_username = db_username.replace("@","")
        db_username = db_username.replace(".","")

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
                        fernet = joblib.load(os.path.join(sys.path[0],'loader.joblib'))
                        encMessage = fernet.encrypt(message.encode())
                        lines_w.append(encMessage)
                    
                    joblib.dump(lines_w,os.path.join(sys.path[0],"loader_request.joblib"))
                
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

# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
pixmap = QPixmap(os.path.join(sys.path[0],"Images/logo.png"))
splash = QSplashScreen(pixmap)
splash.show()
window = Login()
window.show()
splash.finish(window)
sys.exit(app.exec())
# -------------------------------------------------------------------------- 



