from opendss_scivis import get_time_series_axes
from opendss_scivis import get_time_series_plot_options
from opendss_scivis import plot_xy
from opendss_scivis import plot_xy_axes

import math
import matplotlib.pyplot as plt

def time_series_plot(*args, **kwargs):
    '''
    Plot a time series of one or more quantities calculated in OpenDSS.
    
    time_series_plot(data,keyword=value)
    
    The first arguments must be the input as described below followed by
    keywords in the format OPTION = value. An example call to the function 
    would be:
    
    ToDo: update as package evolves
    time_series_plot(variables,data,markerdisplayed='marker')
    
    INPUTS:
    data : dictionary returned from get_time_series function

    OUTPUTS:
    None.
    
    LIST OF OPTIONS:
    For an exhaustive list of options to customize your plot, call the 
    function without arguments at a Python command line:
    % python
    >>> import opendss_scivis as osv
    >>> osv.time_series_plot()

    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com
    
    Created on Apr 22, 2022
    '''
    global number_cols, number_rows, subplot_axis

    nargin = len(args)
    data = _get_time_series_plot_arguments(*args,**kwargs)
    if nargin == 0: return
    
    # Get options
    option = get_time_series_plot_options(**kwargs)
    
    #  Get time axis values for plot
    key_list = list(data)
    key = key_list[0]
    time = data[key].get('values')
    
    # Get number of time series to plot
    max_number_plots = len(data.keys()) - 1
    nlabel = len(option['axeslabel'])
    if nlabel == 0:
        units = data[key].get('units')
        if len(units) > 0:
            axis_label = key + ' (' + units + ')'
        else:
            axis_label = key
        option['axeslabel'].append(axis_label)
    
    # Do maximum of 6 subplots per page
    for iplot in range(0, max_number_plots, 6):
        page = int(iplot/6)
        number_plots = min(max_number_plots - 6*page,6)
        option['nplots'] = number_plots
        option['index_x'] = 0

        # Set matrix of subplots for figure
        fig = _set_subplots(option)
     
        # Produce subplots
        for x in range(1,number_plots+1):
            # Get quantity
            key = key_list[iplot+x]
            quantity = data[key].get('values')
    
            option['variable'] = key
            option['subplot'] = iplot
            option['index_y'] = iplot+x
            if nlabel == 0: 
                units = data[key].get('units')
                if len(units) > 0:
                    axis_label = key + ' (' + units + ')'
                else:
                    axis_label = key
                    
                option['axeslabel'].append(axis_label)
            
            # Get axes values for plot
            axes = get_time_series_axes(time,quantity,option)
    
            # Produce x-y plot
            plot_xy(time,quantity,option,subplot_axis[x-1])
    
            # Modify axes for this plot
            if option['overlay'] == 'off':
            
                # Plot axes
                plot_xy_axes(axes,option,subplot_axis[x-1])
            else:
                markerLabel = option['markerlabel']
                subplot_axis[x-1].legend(markerLabel)
        
        # Hide last subplot if odd number of subplots in 2 columns
        number_rows = math.ceil(number_plots / number_cols)
        # Updated code to handle the box in the last plot
        if number_cols == 2:
            if number_plots % 2 == 1:
                subplot_axis[-1].axis('off')
                if number_rows > 1:
                    subplot_index = (number_rows - 1) * number_cols
                    subplot_axis[subplot_index].spines['top'].set_visible(True)
                    subplot_axis[subplot_index].spines['right'].set_visible(True)
                    subplot_axis[subplot_index].spines['bottom'].set_visible(True)
                    subplot_axis[subplot_index].spines['left'].set_visible(True)
       
def _get_time_series_plot_arguments(*args,**kwargs):
    '''
    Get arguments for time_series_plot function.
    
    Retrieves the arguments supplied to the time_series_plot function as
    arguments and displays the optional arguments if none are supplied.
    Otherwise, tests the first argument is a non-empty dictionary and returns it.
        
    INPUTS:
    args : variable-length input argument list
    
    OUTPUTS:
    time_series_data: time series of quantities in a dictionary
    '''
    
    time_series_data = {}
    nargin = len(args)
    if nargin == 0:
        # Display options list
        _display_time_series_plot_options()
        return time_series_data
    elif nargin != 1:
        raise ValueError('Must supply 1 argument')

    time_series_data = args[0]

    # Test the data type of first argument
    if not isinstance(time_series_data, dict):
        raise ValueError('First argument is not a dictionary')
    elif not time_series_data:
        raise ValueError('First argument is an empty dictionary')

    return time_series_data

def _display_time_series_plot_options():
    '''
    Displays available options for TIME_SERIES_PLOT function.
    '''
    
    _disp('General options:')
    _dispopt("'colormap'","'on'/ 'off' (default): "  + 
        "Switch to map color shading of markers to colormap ('on')\n\t\t"  +
        "or min to max range of RMSDz values ('off').")
    _dispopt("'overlay'","'on' / 'off' (default): " +
        'Switch to overlay current statistics on Taylor diagram. ' +
        '\n\t\tOnly markers will be displayed.')
    _disp('')
    
    _disp('Marker options:')
    _dispopt("'MarkerDisplayed'",
        "'line' : use a continuous line (default)\n\t\t"  + 
        "'marker' : disp0lay markers at provide points")
    _disp("OPTIONS when 'MarkerDisplayed' == 'line'")
    _dispopt("'lineSpec'","Line specification (default solid black, 'k-')")
    _dispopt("'lineWidth'","Line width specification (default default rcParams " + 
             "'lines.linewidth'")

    _disp("OPTIONS when 'MarkerDisplayed' == 'marker'")
    _dispopt("'alpha'","Blending of symbol face color (0.0 transparent through 1.0 opaque)" +
             "\n\t\t" + "(Default: 1.0)")
    _dispopt("'markerColor'",'Single color to use for all markers'  +
        ' (Default: red)')
    _dispopt("'markerLabel'",'Labels for markers. (Default: None)')
    _dispopt("'markerLabelColor'",'Marker label color (Default: black)')
    _dispopt("'markerLegend'","'on' / 'off' (default): "  +
        'Use legend for markers')
    _dispopt("'markers'",'Dictionary providing individual control of the marker label, ' + 
             'label color, \n\t\t' + 
             'symbol, size, face color, and edge color. (Default: none)')
    _dispopt("'markerSize'",'Marker size (Default: 10)')
    _dispopt("'markerSymbol'","Marker symbol (Default: '.')")
    _disp('')
    
    _disp('Axes options:')
    _dispopt("'axislim'",'Axes limits [xmin, xmax, ymin, ymax] (Default: data values)')
    _dispopt("'ticks'",'Define tick positions (default is that used by axis function)')
    _dispopt("'xtickLabelPos'",'Position of the tick labels along the x-axis ' + 
             '(empty by default)')
    _dispopt("'ytickLabelPos'",'Position of the tick labels along the y-axis ' + 
             '(empty by default)')
    _disp('')
    
    _disp('Plot options:')
    _dispopt("'plotType'",
        "'linear': Standard linear plot\n\t\t"  + 
        "'loglog': Log scaling on both the x and y axis\n\t\t"  + 
        "'semilogx': Log scaling on the x axis\n\t\t"  + 
        "'semilogy' : Log scaling on the y axis")

def _disp(text):
    print(text)

def _dispopt(optname,optval):
    '''
    Displays option name and values

    This is a support function for the display_time_series_plot_options function.
    It displays the option name OPTNAME on a line by itself followed by its 
    value OPTVAL on the following line.
    '''

    _disp('\t%s' % optname)
    _disp('\t\t%s' % optval)

def _set_subplots(option):
    global number_cols, number_rows, subplot_axis

    number_plots = option['nplots']
    number_cols = option['layout'][1]

    # Constrain number of columns to within number of plots
    if number_cols > number_plots: number_cols = number_plots

    if option['overlay'] == 'off':
        number_rows = math.ceil(number_plots / number_cols)
        
        if number_plots < 4:
            fig, ax = plt.subplots(number_rows, number_cols)
        elif number_plots < 7:
            fig, ax = plt.subplots(number_rows, number_cols, figsize=(8.5, 11))
        else:
            raise ValueError('Not programmed to handle more than 6 subplots.')

        if number_plots == 1:
            subplot_axis = []
            subplot_axis.append(ax)
        else:
            subplot_axis = ax.flatten()

        return fig
