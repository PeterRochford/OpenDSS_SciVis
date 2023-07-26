def get_time_series_plot_options(data,**kwargs):
    '''
    Get optional arguments for time_series_plot function.
    
    Retrieves the optional arguments supplied to the time_series_plot 
    function as a variable-length keyword argument list (*KWARGS), and
    returns the values in an OPTION dictionary. Default values are 
    assigned to selected optional arguments. The function will terminate
    with an error if an unrecognized optional argument is supplied.
            
    ToDo: update as package evolves
    
    INPUTS:
    data    : time series of quantities in a dictionary
    *kwargs : variable-length keyword argument list. The keywords by 
              definition are dictionaries with keys that must correspond to 
              one choices given in OUTPUTS below.
    
    OUTPUTS:
    option : dictionary containing option values. (Refer to 
             display_target_diagram_options function for more information.)
    option['alpha']           : blending of symbol face color (0.0 
                                transparent through 1.0 opaque). (Default : 1.0)
    option['axislim']         : axes limits [xmin, xmax, ymin, ymax] (Default: data values)
    option['linespec']  : line specification (default solid black, 'k-')
    option['linewidth'] : line width specification (default rcParams 'lines.linewidth')
    option['circles']         : radii of circles to draw to indicate 
                                isopleths of standard deviation (empty by default)
    option['cmapzdata']       : data values to use for color mapping of
                                markers, e.g. RMSD or BIAS. (Default empty)
    option['colormap']        : 'on'/'off' switch to map color shading of
                                 markers to CMapZData values ('on') or min to
                                 max range of CMapZData values ('off').
                                 (Default : 'on')
    option['locationcolorbar'] : location for the colorbar, 'NorthOutside' or
                                 'EastOutside'
    option['markerdisplayed'] : markers to use for individual experiments
                                = 'line' to get a continuous line
                                = 'marker' to display only markers at provided points
    option['markerlabel']     : name of the experiment to use for marker
    option['markerlabelcolor'] : marker label color (Default 'k')
    option['markerlegend']    : 'on'/'off' switch to display marker legend
                                (Default 'off')
    option['markersize']      : marker size (Default 10)
    option['markersymbol']    : marker symbol (Default 'o')

    option['overlay']         : 'on'/'off' switch to overlay current
                                statistics on Taylor diagram (Default 'off')
                                Only markers will be displayed.
    option['plottype']        : type of x-y plot
                                'linear', standard linear plot (Default)
                                'loglog', log scaling on both the x and y axis
                                'semilogx', log scaling on the x axis
                                'semilogy', log scaling on the y axis
    option['ticks']           : define tick positions (default is that used 
                                by the axis function)
    option['titlecolorbar']   : title for the colorbar
    option['xticklabelpos']   : position of the tick labels along the x-axis 
                                (empty by default)
    option['yticklabelpos']   : position of the tick labels along the y-axis 
                                (empty by default)
  
    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com

    Created on Apr 27, 2022
    Revised on Apr  4, 2023
    '''
    from matplotlib import rcParams

    nargin = len(kwargs)
    number_variables = len(data.keys())

    # Set default parameters for all options
    option = {}
    option['alpha'] = 1.0
    option['axeslabel'] = []
    option['axislim'] = [None] * number_variables
    option['axismax']=[]
    option['axismin']=[]
    option['linespec'] = 'k-'
    option['linewidth'] = rcParams.get('lines.linewidth')

    option['index_x'] = None
    option['index_y'] = None

    option['markercolor'] = 'r'
    option['markerdisplayed'] = 'line'
    option['markerlabel'] = ''
    option['markerlabelcolor'] = 'k'
    option['markerlegend'] = 'off'
    option['markersize'] = 10
    option['markersymbol'] = 'o'

    option['overlay'] = 'off'
    option['plottype'] = 'linear'
    option['ticks'] = []
    option['titlecolorbar'] = ''
    option['xticklabelpos'] = []
    option['yticklabelpos'] = []
    if nargin == 0:
        # No options requested, so return with only defaults
        return option
    
    # Check for valid keys and values in dictionary
    for optname, optvalue in kwargs.items():
        optname = optname.lower()
        if not optname in option:
            raise ValueError('Unrecognized option: ' + optname)
        else:
            # Replace option value with that from arguments
            option[optname] = optvalue

            # Check values for specific options
            if optname == 'cmapzdata':
                if isinstance(option[optname], str):
                    raise ValueError('cmapzdata cannot be a string!')
                elif isinstance(option[optname], bool):
                    raise ValueError('cmapzdata cannot be a boolean!')
                option['cmapzdata'] = optvalue
            elif optname == 'markerlabel':
                if type(optvalue) is list:
                    option['markerlabel'] = optvalue
                elif type(optvalue) is dict:
                    option['markerlabel'] = optvalue
                else:
                    raise ValueError('markerlabel value is not a list or dictionary: ' +
                                     str(optvalue))
    
    return option
