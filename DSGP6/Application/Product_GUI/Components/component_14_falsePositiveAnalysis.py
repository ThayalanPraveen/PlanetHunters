##########
# Component ID : 9
# Function : Area to show the plot

# Offset Control
#-----------------
cmp_9_x_offset = 0
cmp_9_y_offset = 0
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
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import lightkurve as lk
import matplotlib.pyplot as plt

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
class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

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
    
    def plotTargetPixelFile(self):
        TIC = 'TIC 55525572' 
        search_result = lk.search_targetpixelfile(TIC,author="SPOC",sector=5)
        tpf = search_result.download()

        # plot the data ('pipeline' command tells it to plot the red aperture)
        tpf.plot(aperture_mask='pipeline',ax=self.sc.axes)
    
    def plotLightCurve(self):
        TIC = 'TIC 55525572'
        sector_data = lk.search_lightcurve(TIC, author = 'SPOC', sector = 5)
        lc = sector_data.download()
        lc.plot(linewidth = 0, marker = '.', color = 'black', alpha = 0.3,ax=self.sc.axes)
    
    def backgroundFlux(self):
        TIC = 'TIC 55525572'
        sector_data = lk.search_lightcurve(TIC, author = 'SPOC', sector = 5)
        lc = sector_data.download()
        self.sc.axes.plot(lc.time.value, lc.sap_bkg.value, color = 'blue', lw = 0, marker = '.', ms = 1)
        self.sc.axes.set_ylabel("Background flux") # label the axes
        self.sc.axes.set_xlabel("Time (TJD)")
    
    def backgroundFluxAtTransitEvent(self):
        TIC = 'TIC 55525572'
        sector_data = lk.search_lightcurve(TIC, author = 'SPOC', sector = 5)
        lc = sector_data.download()
        transit_time = 1454.7 # variable. time of transit event 

        # generate a mask so that we only see the times around the transit event
        # in this example we are looking at 2 days on either side of the event but you can CHANGE THIS depending on the signal.
        transit_mask = (lc.time.value > transit_time - 2) & (lc.time.value < transit_time + 2)

        # mask the date (both the time and the flux using the mask we just generated)
        self.sc.axes.plot(lc.time.value[transit_mask], lc.sap_bkg.value[transit_mask], color = 'blue', lw = 0, marker = '.', ms = 1)

        self.sc.axes.axvline(transit_time) # axv line is similar to our axh line...now its vertical only

        self.sc.axes.set_ylabel("Background flux") 
        self.sc.axes.set_xlabel("Time (TJD)")
    
        
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

        self.cmp_9_create(cmp_9_x_offset,cmp_9_y_offset)

    def cmp_9_create(self,cmp_9_x_offset,cmp_9_y_offset):
        # Plot Area to display the plots after selecting a sector
        # --------------------------------------------------------------------------
        self.target_plot = PlotArea(self)
        self.target_plot.setGeometry(10 + cmp_9_x_offset,10 + cmp_9_y_offset, 830, 500)
        self.target_plot.plotLightCurve()
    
    def cmp_9_visibility(self,bool):
        self.target_plot.setHidden(bool)
       






# Application start
# -------------------------------------------------------------------------- 
app = QApplication([])
app.setStyleSheet("QLabel {color: white;} QLineEdit {color: white;}") # Setting all labels in the app to white color
window = Component()
window.show()
sys.exit(app.exec())
# -------------------------------------------------------------------------- 