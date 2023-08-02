import matplotlib.pyplot as plt
import opendss_scivis as osv

def plot_xy(X,Y,option,subplot_axis):
    '''
    Plots a one-dimensional variable in an x-y plot.
    
    Plots a function Y(X) such as frequency with time.
    
    INPUTS:
    x       : independent coordinates
    y       : function values at x-coordinates
    option  : dictionary containing option values. (Refer to 
              get_time_series_plot_options function for more information.)
    option['markerdisplayed'] : markers to use for plots
    subplot_axis : axis handle for subplot

    OUTPUTS:
    None
    
    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com

    Created on May 1, 2022
    '''
    
    plt.axes(subplot_axis) # set axis for subplot

    lowcase = option['markerdisplayed'].lower()
    if lowcase == 'line':
        osv.plot_xy_line(X,Y,option)
    elif lowcase == 'marker':
        osv.plot_xy_markers(X,Y,option)
    else:
        raise ValueError('Unrecognized option: ' + 
                         option['markerdisplayed'])

