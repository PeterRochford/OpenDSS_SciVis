from math import ceil, floor, log
import matplotlib.ticker as ticker
import numpy as np

def get_time_series_axes(x,y,option):
    '''
    Get axes value for time_series_plot function.
    
    Determines the axes information for a time series plot given the axis 
    values (X,Y) and the options in the data structure OPTION returned by 
    the get_time_series_plot_options function.
    
    INPUTS:
    x       : values for x-axis
    y       : values for y-axis
    option  : dictionary containing option values. (Refer to 
              get_time_series_plot_options function for more information.)
    option['index_x'] : index for x values in option
    option['index_y'] : index for y values in option
    
    OUTPUTS:
    axes           : dictionary containing axes information for time series plot
    axes['xtick']  : x-values at which to place tick marks
    axes['ytick']  : y-values at which to place tick marks
    axes['xlabel'] : labels for xtick values
    axes['ylabel'] : labels for ytick values
    option : dictionary containing updated option values
    
    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com
    
    Created on Apr 25, 2022
    '''

    # Specify max & min for axes
    maxx, maxy = _getmax(option,x,y)
    minx, miny = _getmin(option,x,y)
    
    option['axismax'].append(maxy)

    # Check if min & max the same within a tolerance
    equal = np.allclose(miny,maxy)
    if equal:
        # set min & max to suitable range
        offset = 0.1*maxy
        miny = miny - offset
        maxy = maxy + offset

    # Determine tick values marks according to plot type
    plottype = option['plottype']
    xtickvals = None
    ytickvals = None
    if plottype == "linear":
        xtickvals = ticker.AutoLocator().tick_values(minx, maxx)
        ytickvals = ticker.AutoLocator().tick_values(miny, maxy)
    elif plottype == "loglog":
        xtickvals = [ 10**int(x) for x in np.arange(np.log10(minx), np.log10(maxx)+1)]
        # ytickvals = ticker.LogLocator(base=10).tick_values(miny, maxy)
        ytickvals = [ 10**int(y) for y in np.arange(np.log10(miny), np.log10(maxy)+1)]
        # Adjust tick values if outside specified range
        xvals = [x for x in xtickvals if x >= minx and x <= maxx]
        yvals = [y for y in ytickvals if y >= miny and y <= maxy]
        xtickvals = np.array(xvals)
        ytickvals = np.array(yvals)
    elif plottype == "semilogx":
        xtickvals = ticker.LogLocator(base=10.0).tick_values(minx, maxx)
        ytickvals = ticker.AutoLocator().tick_values(miny, maxy)
    elif plottype == "semilogy":
        xtickvals = ticker.AutoLocator().tick_values(minx, maxx)
        ytickvals = ticker.LogLocator(base=10.0).tick_values(miny, maxy)
    else:
        raise ValueError('Unknown option: ' + plottype)

    ntest = np.sum(xtickvals > 0)
    if ntest > 0:
        nxticks = len(xtickvals) - 1
        nyticks = len(ytickvals) - 1
        
        # Save nxticks and nyticks as function attributes for later 
        # retrieval in function calls
        get_time_series_axes.nxticks = nxticks
        get_time_series_axes.nyticks = nyticks
    else:
        # Use function attributes for nxticks and nyticks
        if hasattr(get_time_series_axes, 'nxticks') and \
            hasattr(get_time_series_axes, 'nxticks'):
            nxticks = get_time_series_axes.nxticks
            nyticks = get_time_series_axes.nyticks
        else:
            raise ValueError('No saved values for nxticks & nyticks.')
    
    # Convert to integer if whole number
    if type(minx) is float and minx.is_integer(): minx = int(round(minx))
    if type(miny) is float and miny.is_integer(): miny = int(round(miny))
    if type(maxx) is float and maxx.is_integer(): maxx = int(round(maxx))
    if type(maxy) is float and maxy.is_integer(): maxy = int(round(maxy))
    
    # Determine tick values
    if len(option['ticks']) > 0:
        xtick = option['ticks']
        ytick = option['ticks']
    else:
        xtick = xtickvals
        ytick = ytickvals

    # Assign tick label positions
    if len(option['xticklabelpos']) == 0:
        option['xticklabelpos'] = xtick
    if len(option['yticklabelpos']) == 0:
        option['yticklabelpos'] = ytick

    # # Set tick labels using provided tick label positions
    # xlabel =[]; ylabel = [];
    #
    # # Set x tick labels
    # for i in range(len(xtick)):
    #     index = np.where(option['xticklabelpos'] == xtick[i])
    #     if len(index) > 0:
    #         label = get_axis_tick_label(xtick[i])
    #         xlabel.append(label)
    #     else:
    #         xlabel.append('')
    #
    # # Set y tick labels
    # for i in range(len(ytick)):
    #     index = np.where(option['yticklabelpos'] == ytick[i])
    #     if len(index) > 0:
    #         label = get_axis_tick_label(ytick[i])
    #         ylabel.append(label)
    #     else:
    #         ylabel.append('')
    
    # Store output variables in data structure
    axes = {}
    axes['xtick'] = xtick
    axes['ytick'] = ytick
    # axes['xlabel'] = xlabel
    # axes['ylabel'] = ylabel
    
    return axes

def _getmax(option,x,y):
    '''
    Get maximum axes values according to plot type.
    
    INPUTS:
    x       : values for x-axis
    y       : values for y-axis
    option  : dictionary containing option values. (Refer to 
              get_time_series_plot_options function for more information.)
    option['index_x'] : index for x values in option
    option['index_y'] : index for y values in option
    option['plottype']        : type of x-y plot
                                'linear', standard linear plot (Default)
                                'loglog', log scaling on both the x and y axis
                                'semilogx', log scaling on the x axis
                                'semilogy', log scaling on the y axis
    
    OUTPUTS:
    maxx : maximum for x axis
    maxy : maximum for y axis
    '''
    index_x = option['index_x']
    index_y = option['index_y']

    plottype = option['plottype']
    if plottype == "linear":
        # Axis limit not specified
        maxx = np.amax(x)
        maxy = np.amax(y)
    elif plottype == "loglog":
        maxx = 10**floor(log(np.max(x),10))
        maxy = 10**floor(log(np.max(y),10))
    elif plottype == "semilogx":
        maxx = 10**floor(log(np.max(x),10))
        maxy = np.amax(y)
    elif plottype == "semilogy":
        maxx = np.amax(x)
        maxy = 10**floor(log(np.max(y),10))
    else:
        raise ValueError('Unknown option: ' + plottype)
        
    if option['axislim'][index_x] is not None:
        # Axis limit is specified
        maxx = option['axislim'][index_x+1]

    if option['axislim'][index_y] is not None:
        # Axis limit is specified
        maxy = option['axislim'][index_y+2]
        
    return maxx, maxy

def _getmin(option,x,y):
    '''
    Get minimum axes values according to plot type.
    
    INPUTS:
    x       : values for x-axis
    y       : values for y-axis
    option  : dictionary containing option values. (Refer to 
              get_time_series_plot_options function for more information.)
    option['index_x'] : index for x values in option
    option['index_y'] : index for y values in option
    option['plottype']        : type of x-y plot
                                'linear', standard linear plot (Default)
                                'loglog', log scaling on both the x and y axis
                                'semilogx', log scaling on the x axis
                                'semilogy', log scaling on the y axis
    
    OUTPUTS:
    minx : minimum for x axis
    miny : minimum for y axis
    '''
    index_x = option['index_x']
    index_y = option['index_y']

    plottype = option['plottype']
    if plottype == "linear":
        # Axis limit not specified
        minx = np.amin(x)
        miny = np.amin(y)
    elif plottype == "loglog":
        minx = 10**ceil(log(np.min(x),10))
        miny = 10**ceil(log(np.min(y),10))
    elif plottype == "semilogx":
        minx = 10**ceil(log(np.min(x),10))
        miny = np.amin(y)
    elif plottype == "semilogy":
        minx = np.amin(x)
        miny = 10**ceil(log(np.min(y),10))
    else:
        raise ValueError('Unknown option: ' + plottype)
        
    if option['axislim'][index_x] is not None:
        # Axis limit is specified
        minx = option['axislim'][index_x]

    if option['axislim'][index_y] is not None:
        # Axis limit is specified
        miny = option['axislim'][index_y+1]
        
    return minx, miny