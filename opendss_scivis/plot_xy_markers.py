import matplotlib.pyplot as plt
import matplotlib.colors as clr
import matplotlib
import warnings
from opendss_scivis import add_marker_legend

def plot_xy_markers(X,Y,option):
    '''
    Plots a one-dimensional variable in an x-y plot using markers.
    
    Plots a function Y(X) such as frequency with time.
    
    INPUTS:
    x       : independent coordinates
    y       : function values at x-coordinates
    option  : dictionary containing option values. (Refer to 
              get_time_series_plot_options function for more information.)
    option['axismax'] : maximum for the X & Y values. Used to limit maximum 
                        range to display markers
    option['axismin'] : minimum for the X & Y values. Used to limit minimum 
                        range to display markers
    option['index_x'] : index for x values in option
    option['index_y'] : index for y values in option

    OUTPUTS:
    None
    
    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com

    Created on May 1, 2022
    '''
    
    index_x = option['index_x']
    index_y = option['index_y']

    # Set face color transparency
    alpha = option['alpha']
    
    # Set font and marker size
    fontSize = matplotlib.rcParams.get('font.size') - 2
    markerSize = option['markersize']
    
    if option['markerlegend'] == 'on':
        # Check that marker labels have been provided
        if option['markerlabel'] == '':
            raise ValueError('No marker labels provided.')

        # Plot markers of different color and shapes with labels 
        # displayed in a legend
        
        # Define markers
        kind = ['+','o','x','s','d','^','v','p','h','*']
        colorm = ['b','r','g','c','m','y','k']
        if len(X) > 70:
            _disp('You must introduce new markers to plot more than 70 cases.')
            _disp('The ''marker'' character array need to be extended inside the code.')
        
        if len(X) <= len(kind):
            # Define markers with specified color
            marker = []
            markercolor = []
            for color in colorm:
                for symbol in kind:
                    marker.append(symbol + option['markercolor'])
                    rgba = clr.to_rgb(option['markercolor']) + (alpha,)
                    markercolor.append(rgba)
        else:
            # Define markers and colors using predefined list
            marker = []
            markercolor = [] #Bug Fix: missing array initialization
            for color in colorm:
                for symbol in kind:
                    marker.append(symbol + color)
                    rgba = clr.to_rgb(color) + (alpha,)
                    markercolor.append(rgba)
        
        # Plot markers at data points
        limit = option['axismax']
        hp = ()
        markerlabel = []
        for i, xval in enumerate(X):
            if abs(X[i]) <= limit and abs(Y[i]) <= limit:
                h = plt.plot(X[i],Y[i],marker[i], markersize = markerSize, 
                     markerfacecolor = markercolor[i],
                     markeredgecolor = marker[i][1],
                     markeredgewidth = 2)
                hp += tuple(h)
                markerlabel.append(option['markerlabel'][i])

        # Add legend
        if len(markerlabel) == 0:
            warnings.warn('No markers within axis limit ranges.')
        else:
            add_marker_legend(markerlabel, option, rgba, markerSize, fontSize, hp)
    else:
        # Plot markers as dots of a single color with accompanying labels
        # and no legend
        
        # Plot markers at data points
        axismin = option['axismin']
        axismax = option['axismax']
        rgba = clr.to_rgb(option['markercolor']) + (alpha,) 
        for i,xval in enumerate(X):
            if X[i] >= axismin[index_x] and X[i] <= axismax[index_x] and \
                        Y[i] >= axismin[index_y] and Y[i] <= axismax[index_y]:
                # Plot marker
                marker = option['markersymbol']
                plt.plot(X[i],Y[i],marker, markersize = markerSize, 
                     markerfacecolor = rgba,
                     markeredgecolor = option['markercolor'])
                
                # Check if marker labels provided
                if type(option['markerlabel']) is list:
                    # Label marker
                    xtextpos = X[i]
                    ytextpos = Y[i]
                    plt.text(xtextpos,ytextpos,option['markerlabel'][i], 
                             color = option['markerlabelcolor'],
                             verticalalignment = 'bottom',
                             horizontalalignment = 'right',
                             fontsize = fontSize)

        # Add legend if labels provided as dictionary
        markerlabel = option['markerlabel']
        if type(markerlabel) is dict:
            add_marker_legend(markerlabel, option, rgba, markerSize, fontSize)

def _disp(text):
    print(text)
