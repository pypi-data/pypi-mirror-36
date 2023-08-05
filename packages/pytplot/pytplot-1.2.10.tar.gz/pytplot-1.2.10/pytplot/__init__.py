# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import numpy as np
from _collections import OrderedDict

#This variable will be constantly changed depending on what x value the user is hovering over
class HoverTime(object):
    
    hover_time = 0
    functions_to_call = []
    
    def register_listener(self, fn):
        self.functions_to_call.append(fn)
        return
    
    def change_hover_time(self, new_time):
        self.hover_time = new_time
        for f in self.functions_to_call:
            f(self.hover_time)
        return

using_graphics = True

try:
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtWidgets 
    
    pg.setConfigOptions(imageAxisOrder='row-major')
    pg.setConfigOptions(background='w')
    
    class PlotWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            self.initUI()
             
        def initUI(self):
            self.setWindowTitle('PyTplot')
            menubar = self.menuBar()
            exportMenu = menubar.addMenu('Export')
            exportDatapngAction = QtWidgets.QAction("PNG", self)
            exportDatapngAction.triggered.connect(self.exportpng)
            exportMenu.addAction(exportDatapngAction)
             
        def exportpng(self):
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Open file', 'pytplot.png', filter ="png (*.png *.)")
            sshot = self.centralWidget().grab()
            sshot.save(fname[0])
        
        def newlayout(self, layout):
            self.setCentralWidget(layout)
            
except:
    
    using_graphics = False



class TVar(object):
    """ 
    The basic data object in pytplot.  Each dataset is its own separate TVar object.  
    This exists to encapsulate the data and details about how to plot the data.  
    """
    
    def __init__(self, name, number, data, spec_bins, yaxis_opt, zaxis_opt, line_opt,
                 trange, dtype, create_time, time_bar, extras, links):
        
        #Name of the TVar
        self.name = name
        #TVar number
        self.number = number
        #The data of the TVar
        self.data = data
        #The spec_bins, if applicable
        self.spec_bins = spec_bins
        #Dictionary of the y axis options
        self.yaxis_opt = yaxis_opt
        #Dictionary of the z axis options
        self.zaxis_opt = zaxis_opt
        #Dictionary of line options
        self.line_opt = line_opt
        #The time range
        self.trange = trange
        #The data type of the data (ex - int/double)
        self.dtype = dtype
        #String of creation time of this object
        self.create_time = create_time
        #Array of time bar objects
        self.time_bar = time_bar
        #Dictionary of extra objects
        self.extras = extras
        #Dictionary of linked tvars (things like latitude/longitude/altitude)
        self.links = links
        #Whether or not the spec_bins vary in time
        self.spec_bins_time_varying = False
        #Whether the spec_bins are ascending or decending order
        self.spec_bins_ascending = self._check_spec_bins_ordering()
        
    def _check_spec_bins_ordering(self):
        '''
        This is a private function of the TVar object, this is run during 
        object creation to check if spec_bins are ascending or descending
        '''
        if self.spec_bins is None:
            return
        if len(self.spec_bins) == len(self.data.index):
            self.spec_bins_time_varying = True
            break_top_loop = False
            for index,row in self.spec_bins.iterrows():
                if row.isnull().values.all():
                    continue
                else:
                    for i in row.index:
                        if np.isfinite(row[i]) and np.isfinite(row[i+1]):
                            ascending = row[i] < row[i+1]
                            break_top_loop = True
                            break
                        else:
                            continue
                    if break_top_loop:
                        break
        else:
            ascending = self.spec_bins[0].iloc[0] < self.spec_bins[1].iloc[0]
        return ascending
        
    def link_to_tvar(self, name, link, method='linear'):
        from scipy import interpolate
        from scipy.interpolate import interp1d
        from .store_data import store_data
        #pull saved variables from data_quants
        link_timeorig = np.asarray(data_quants[link].data.index.tolist())
        link_dataorig = np.asarray(data_quants[link].data[0].tolist())
        tvar_timeorig = np.asarray(self.data.index.tolist())
         
        #shorten tvar array to be within link array
        while tvar_timeorig[-1] > link_timeorig[-1]:
            tvar_timeorig = np.delete(tvar_timeorig,-1)
        while tvar_timeorig[0] < link_timeorig[0]:
            tvar_timeorig = np.delete(tvar_timeorig,0)
     
        x = link_timeorig
        y = link_dataorig
        xnew = tvar_timeorig
     
        #choose method, interpolate, plot, and store
        if method == 'linear':
            f = interp1d(x,y)
            newvarname = link + "_" + self.name + "_link"
            store_data(newvarname, data={'x':xnew,'y':f(xnew)})
        elif method == 'cubic':
            f2 = interp1d(x, y, kind='cubic')
            newvarname = link + "_" + self.name + "_link"
            store_data(newvarname, data={'x':xnew,'y':f2(xnew)})
        elif method == 'quad_spline':
            tck = interpolate.splrep(x,y,s=0,k=2)
            ynew = interpolate.splev(xnew, tck, der=0)
            newvarname = link + "_" + self.name + "_link"
            store_data(newvarname, data={'x':xnew,'y':ynew})
             
        else:
            print('Error: choose interpolation method.')
            print('linear, cubic, quad_spline')
            return

        self.links[name] = newvarname
        

#Global Variables
hover_time = HoverTime()
data_quants = OrderedDict()
tplot_opt_glob = dict(tools = "xpan,crosshair,reset", 
                 min_border_top = 15, min_border_bottom = 0, 
                 title_align = 'center', window_size = [800, 800],
                 title_size='12pt', title_text='')
lim_info = {}
extra_layouts = {}

if using_graphics:
    pytplotWindows = [] #This is a list that will hold future qt windows
    from . import QtPlotter
    qt_plotters = {'qtTVarFigure1D':QtPlotter.TVarFigure1D,
                   'qtTVarFigureSpec':QtPlotter.TVarFigureSpec,
                   'qtTVarFigureAlt':QtPlotter.TVarFigureAlt,
                   'qtTVarFigureMap':QtPlotter.TVarFigureMap}

from . import HTMLPlotter
bokeh_plotters = {'bkTVarFigure1D':HTMLPlotter.TVarFigure1D,
                  'bkTVarFigureMap':HTMLPlotter.TVarFigureMap,
                  'bkTVarFigureAlt':HTMLPlotter.TVarFigureAlt,
                  'bkTVarFigureSpec':HTMLPlotter.TVarFigureSpec}

from .store_data import store_data
from .tplot import tplot
from .get_data import get_data
from .xlim import xlim
from .ylim import ylim
from .zlim import zlim
from .tlimit import tlimit
from .tplot_save import tplot_save
from .tplot_names import tplot_names
from .tplot_restore import tplot_restore
from .get_timespan import get_timespan
from .tplot_options import tplot_options
from .tplot_rename import tplot_rename
from .get_ylimits import get_ylimits
from .timebar import timebar
from .del_data import del_data
from .timespan import timespan
from .options import options
from .timestamp import timestamp
from .cdf_to_tplot import cdf_to_tplot
from .netcdf_to_tplot import netcdf_to_tplot
from .tplot_utilities import compare_versions
from .link import link
#from .tplot_math import *
#from .tplot_resample import tplot_resample
#from .degap import degap
#from .clip import clip
#from .deflag import deflag

#If we are in an ipython environment, set the gui to be qt5
#This allows the user to interact with the window in real time
try:
    magic = get_ipython().magic
    magic(u'%gui qt5')
    print("i set the gui")
except:
    pass

if using_graphics:
    pg.mkQApp()

compare_versions()



