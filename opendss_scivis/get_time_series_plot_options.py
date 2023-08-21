def _default_options() -> dict:
    '''
    Set default optional arguments for time_series_plot function.
    
    Sets the default optional arguments for the TIME_SERIES_PLOT 
    function in an OPTION dictionary. Default values are 
    assigned to selected optional arguments. 
    
    INPUTS:
    None
        
    OUTPUTS:
    option : dictionary containing option values. (Refer to 
             display_display_time_series_options function for more information.)
    option['alpha']           : blending of symbol face color (0.0 
                                transparent through 1.0 opaque). (Default : 1.0)
    option['axislim']         : axes limits for each subplot provided as a dictionary,
                                [xmin, xmax, ymin, ymax] 
                                (Default: data values), e.g. for a subplot of the
                                variable Frequency: option['axislim]['Frequency'].
                                Note that values of None can be used in the list to specify
                                the min/max ranges are determined from the data. 
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
    option['layout']           : matrix layout for subplots specified as a list 
                                 [m,n] where m is number of rows and n number of columns.
                                 A value of m = 0 lets package specify number of rows
                                 per figure. (Default: [0,2])
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
    '''
    from matplotlib import rcParams

    # Set default parameters for all options
    option = {}
    option['alpha'] = 1.0
    option['axeslabel'] = []
    option['axislim'] = None
    option['layout'] = [0, 2]
    option['linespec'] = 'k-'
    option['linewidth'] = rcParams.get('lines.linewidth')

    option['index_x'] = None #used internally
    option['index_y'] = None #used internally
    option['subplot'] = None #used internally

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
         
    return option

def _get_options(option, **kwargs) -> dict:
    '''
    Get values for optional arguments for time_series_plot function.
    
    Gets the default optional arguments for the TIME_SERIES_PLOT 
    function in an OPTION dictionary. 
    
    INPUTS:
    option  : dictionary containing default option values
    *kwargs : variable-length keyword argument list. The keywords by 
              definition are dictionaries with keys that must correspond to 
              one of the choices given in the _default_options function.
        
    OUTPUTS:
    option : dictionary containing option values
  
    Author:
    
    Peter A. Rochford
        rochford.peter1@gmail.com

    Created on Aug 8, 2023
    Revised on Aug 8, 2023
    '''    
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
 
        del optname, optvalue   
    
    # Set layout if an overlay
    if option['overlay'] == 'on':
        option['layout'][0] = number_rows
        option['layout'][1] = number_cols
    else: 
        number_rows = option['layout'][0]
        number_cols = option['layout'][1] 

    return option   

def get_time_series_plot_options(**kwargs):
    '''
    Get optional arguments for time_series_plot function.
    
    Retrieves the optional arguments supplied to the time_series_plot 
    function as a variable-length keyword argument list (*KWARGS), and
    returns the values in an OPTION dictionary. Default values are 
    assigned to selected optional arguments. The function will terminate
    with an error if an unrecognized optional argument is supplied.
            
    ToDo: update as package evolves
    
    INPUTS:
    *kwargs : variable-length keyword argument list. The keywords by 
              definition are dictionaries with keys that must correspond to 
              one choices given in OUTPUTS below.
    
    OUTPUTS:
    option : dictionary containing option values. (Refer to 
             display_display_time_series_options function for more information.)
  
    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com

    Created on Aug 8, 2023
    Revised on Aug 8, 2023
    '''
    global number_cols, number_rows, subplot_axis

    nargin = len(kwargs)

    # Set default parameters for all options
    option = _default_options()

    # No options requested, so return with only defaults
    if nargin == 0: return option

    # Check for valid keys and values in dictionary
    # Allows user to override options specified in CSV file
    option = _get_options(option, **kwargs)
    
    return option
