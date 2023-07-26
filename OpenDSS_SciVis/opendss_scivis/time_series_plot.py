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
    
    # Check for number of arguments
    nargin = len(args)
    data = _get_time_series_plot_arguments(*args,**kwargs)
    if nargin == 0: return
    
    # Get options
    option = get_time_series_plot_options(data,**kwargs)
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
        if number_plots % 2 == 1 and number_cols > 1:
            subplot_axis[-1].axes.get_xaxis().set_visible(False)
            subplot_axis[-1].axes.get_yaxis().set_visible(False)
            plt.box(False) #remove box
        
        # Adjust spacing between subplots to minimize the overlaps.
        plt.tight_layout()
       
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
    Displays available options for TAYLOR_DIAGRAM function.
    '''
    
    _disp('ToDo: display_time_series_plot_options remains to be implemented!')
    
    # _disp('General options:')
    # _dispopt("'numberPanels'",'1 or 2: Panels to display (1 for ' +
    #          'positive correlations, 2 for positive and negative' +
    #          ' correlations). \n\t\tDefault value depends on ' +
    #          'correlations (CORs)')
    # _dispopt("'overlay'","'on' / 'off' (default): " +
    #     'Switch to overlay current statistics on Taylor diagram. ' +
    #     '\n\t\tOnly markers will be displayed.')
    # _dispopt("'alpha'","Blending of symbol face color (0.0 transparent through 1.0 opaque)" +
    #          "\n\t\t" + "(Default: 1.0)")
    # _dispopt("'axismax'",'Maximum for the radial contours')
    # _dispopt("'colormap'","'on'/ 'off' (default): "  + 
    #     "Switch to map color shading of markers to colormap ('on')\n\t\t"  +
    #     "or min to max range of RMSDz values ('off').")
    # _disp('')
    #
    # _disp('Marker options:')
    # _dispopt("'MarkerDisplayed'",
    #     "'marker' (default): Experiments are represented by individual " + 
    #     "symbols\n\t\t"  + 
    #     "'colorBar': Experiments are represented by a color described " + \
    #     "in a colorbar")
    # _disp("OPTIONS when 'MarkerDisplayed' == 'marker'")
    # _dispopt("'markerLabel'",'Labels for markers')
    # _dispopt("'markerLabelColor'",'Marker label color (Default: black)')
    # _dispopt("'markerColor'",'Single color to use for all markers'  +
    #     ' (Default: red)')
    # _dispopt("'markerLegend'","'on' / 'off' (default): "  +
    #     'Use legend for markers')
    # _dispopt("'markerSize'",'Marker size (Default: 10)')
    # _dispopt("'markerSymbol'","Marker symbol (Default: '.')")
    #
    # _disp("OPTIONS when MarkerDisplayed' == 'colorbar'")
    # _dispopt("'cmapzdata'","Data values to use for " +
    #         'color mapping of markers, e.g. RMSD or BIAS.\n\t\t' +
    #         '(Used to make range of RMSDs values appear above color bar.)')
    # _dispopt("'titleColorBar'",'Title of the colorbar.')
    # _dispopt("'titleColorBar'",'Title of the colorbar.')
    # _disp('')
    #
    # _disp('RMS axis options:')
    # _dispopt("'tickRMS'",'RMS values to plot grid circles from ' +
    #          'observation point')
    # _dispopt("'rincRMS'",'axis tick increment for RMS values')
    # _dispopt("'colRMS'",'RMS grid and tick labels color. (Default: green)')
    # _dispopt("'showlabelsRMS'","'on' (default) / 'off': "  +
    #     'Show the RMS tick labels')
    # _dispopt("'tickRMSangle'",'Angle for RMS tick labels with the ' +
    #          'observation point. Default: 135 deg.')
    # _dispopt("'rmsLabelFormat'","String format for RMS contour labels, e.g. '0:.2f'.\n\t\t" +
    #          "(Default '0', format as specified by str function.)")
    # _dispopt("'styleRMS'",'Line style of the RMS grid')
    # _dispopt("'widthRMS'",'Line width of the RMS grid')
    # _dispopt("'labelRMS'","RMS axis label (Default 'RMSD')")
    # _dispopt("'titleRMS'","'on' (default) / 'off': "  +
    #     'Show RMSD axis title')
    # _dispopt("'titleRMSDangle'","angle at which to display the 'RMSD' label for the\n\t\t" +
    #          "RMSD contours (Default: 160 degrees)")
    _disp('')

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
    '''
    Sets matrix of subplots for figure

    This is a support function for the time_series_plot function.
    It sets the number of rows and columns for subplots on a figure and
    sets the axes for the subplots.

    '''
    global number_cols, number_rows, subplot_axis

    number_plots = option['nplots']
    if option['overlay'] == 'off':
        # Specify number of subplots per page
        if number_plots < 4:
            number_rows = number_plots
            number_cols = 1
            fig, ax = plt.subplots(number_rows,number_cols)
            if number_plots == 1:
                subplot_axis = []
                subplot_axis.append(ax)
            else:
                subplot_axis = ax.flatten()
        elif number_plots < 7:
            number_rows = math.ceil(number_plots/2) 
            number_cols = 2
            fig, ax = plt.subplots(number_rows,number_cols,figsize =(8.5,11))
            subplot_axis = ax.flatten()
        else:
            # To Do: Allow for subplots across multiple pages, 6 per each
            raise ValueError('Not programmed to handle more than 6 subplots.')
        
        return fig 
