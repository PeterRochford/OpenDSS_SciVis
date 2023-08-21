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
    option['axislim'] : axes limits for each subplot provided as a dictionary,
                       [xmin, xmax, ymin, ymax], e.g. for a subplot of the 
                       variable Frequency: option['axislim]['Frequency'].

    OUTPUTS:
    None
    
    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com

    Created on May 1, 2022
    Revised on Aug 19, 2023
    '''
    key = option['variable']
    minx = option['axislim'][key][0]
    maxx = option['axislim'][key][1]
    miny = option['axislim'][key][2]
    maxy = option['axislim'][key][3]

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
        hp = ()
        markerlabel = []
        for i, xval in enumerate(X):
            if  X[i] >= minx and X[i] <= maxx and \
                Y[i] >= miny and Y[i] <= maxy:
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
        rgba = clr.to_rgb(option['markercolor']) + (alpha,) 
        for i,xval in enumerate(X):
            if  X[i] >= minx and X[i] <= maxx and \
                Y[i] >= miny and Y[i] <= maxy:
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
