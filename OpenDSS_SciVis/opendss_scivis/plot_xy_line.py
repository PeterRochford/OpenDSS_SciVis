import matplotlib.pyplot as plt
import matplotlib

from opendss_scivis import add_line_legend

def plot_xy_line(X,Y,option):
    '''
    Plots a one-dimensional variable in an x-y plot using lines.
    
    Plots a function Y(X) such as frequency with time.
    
    INPUTS:
    x       : independent coordinates
    y       : function values at x-coordinates
    option  : dictionary containing option values. (Refer to 
              get_time_series_plot_options function for more information.)
    option['linespec']  : line specification (default solid black, 'k-')
    option['linewidth'] : line width specification (default rcParams 'lines.linewidth')
    option['plottype']  : type of x-y plot
                          'linear', standard linear plot (Default)
                          'loglog', log scaling on both the x and y axis
                          'semilogx', log scaling on the x axis
                          'semilogy', log scaling on the y axis

    OUTPUTS:
    None
    
    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com

    Created on May 1, 2022
    '''

    # Plot line according to plot type
    plottype = option['plottype']
    if plottype == "linear":
        plt.plot(X,Y, option['linespec'], linewidth=option['linewidth'])
    elif plottype == "loglog":
        plt.loglog(X,Y, option['linespec'], linewidth=option['linewidth'])
    elif plottype == "semilogx":
        plt.semilogx(X,Y, option['linespec'], linewidth=option['linewidth'])
    elif plottype == "semilogy":
        plt.semilogy(X,Y, option['linespec'], linewidth=option['linewidth'])
    else:
        raise ValueError('Unknown option: ' + plottype)
                
