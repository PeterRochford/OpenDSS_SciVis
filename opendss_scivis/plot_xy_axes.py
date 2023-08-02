from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib

def plot_xy_axes(axes,option,subplot_axis):
    '''
    Plot axes for X-Y plot.
    
    Plots the x & y axes for a X-Y plot using the information provided in 
    the AXES dictionary returned by the get_time_series_axes function.
    
    INPUTS:
    axes   : dictionary containing axes information for X-Y plot
    option  : dictionary containing option values. (Refer to 
              get_time_series_plot_options function for more information.)
    option['xlabel'] : label to use for x-axis
    option['ylabel'] : label to use for y-axis
    subplot_axis : axis handle for subplot
    
    OUTPUTS:
    None
    
    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com

    Created on May 1, 2022
    '''
    
    # ax = plt.gca()
    index_x = option['index_x']
    index_y = option['index_y']
    nlabel = len(option['axeslabel'])

    # Set new ticks
    plt.xticks(axes['xtick'])
    plt.yticks(axes['ytick'])

    # Set axes limits
    axislim = [axes['xtick'][0], axes['xtick'][-1], axes['ytick'][0], axes['ytick'][-1]]
    plt.axis(axislim)
    
    plottype = option['plottype']
    if plottype == 'linear':

        # Check whether to scale an axis to scientific notation
        if option['axismax'][index_y-1] > 100.0:
            # Set formatter of the major ticker
            ax = plt.gca()
            yScalarFormatter = ScalarFormatterClass(useMathText=True)
            yScalarFormatter.set_powerlimits((0,0))
            ax.yaxis.set_major_formatter(yScalarFormatter)
        
    # Label x-axis
    fontSize = matplotlib.rcParams.get('font.size')
    xpos = axes['xtick'][-1] + 2*axes['xtick'][-1]/30
    ypos = axes['xtick'][-1]/30
    if nlabel > 0:
        if index_x >=0 and index_x < nlabel:
            xlabelh = subplot_axis.set_xlabel(option['axeslabel'][index_x], fontsize = fontSize, \
                                 horizontalalignment = 'center')
        else:
            raise ValueError("option['axeslabel'][" + str(index_x) + "] does not exist")

    # Label y-axis
    xpos = 0
    ypos = axes['ytick'][-1] + 2*axes['ytick'][-1]/30
    if nlabel > 0:
        if index_x >=0 and index_x < nlabel:
            ylabelh = subplot_axis.set_ylabel(option['axeslabel'][index_y], fontsize = fontSize, \
                                 horizontalalignment = 'center')
        else:
            raise ValueError("option['axeslabel'][" + str(index_x) + "] does not exist")

    subplot_axis.tick_params(axis='both', direction='in', which='both') # have ticks inside plot
    
    # Set axes line width
    lineWidth = rcParams.get('lines.linewidth')
    subplot_axis.spines['left'].set_linewidth(lineWidth)
    subplot_axis.spines['right'].set_linewidth(lineWidth)
    subplot_axis.spines['top'].set_linewidth(lineWidth)
    subplot_axis.spines['bottom'].set_linewidth(lineWidth)

class ScalarFormatterClass(ScalarFormatter):
   def _set_format(self):
       # Specify only 1 significant digit after decimal place
       self.format = "%1.1f"
