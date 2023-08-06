'''
How to plot a time series of all power system quantities in a CSV File.

A first example of how to plot all quantities in an OpenDSS CSV file. The 
Python code is kept to a minimum.

It supports the following arguments as options. 

-noshow : No figure is shown if this flag is present
-nosave : No figure is saved if this flag is present

They can be invoked from a command line as, for example, to not show the
plot to allow batch execution: 

$ python example01.py -noshow

All functions in the OpenDSS SciVis library are designed to only work with 
one-dimensional arrays, e.g. time series of power system variables for a 
given component in a power grid. The one-dimensional data are read in as 
dictionaries via Comma, Separated, Value (CSV) files:

filename = 'SimpleDemo_Mon_g1out_1'
data = osv.read_element_data(filename)

The plot is written to a file in Portable Network Graphics (PNG) format, see
plt.savefig() below. Other formats are available by specifying the appropriate
file suffix for graphics supported by matplotlib. 

The data used in this example is for a simulated event consisting of a 
3-phase fault to ground with zero impedance on the high voltage side of 
the station transformer (bus HT). The fault is cleared after 70 ms and 
the simulation continues until 5s. This is named the simple Dynamic 
Kundur case because it replicates a single machine infinite bus example 
in the textbook Kundur (1994), p. 732, Example 12.2. 

The functions used here from the OpenDSS_SciVis library read the files
output by OpenDSS in Comma Separated Value (CSV) format. The first row of
the latter is a header describing the the quantities stored in each column, 
their units, etc., as shown below.

hour t(sec) Frequency Theta (Deg) Vd       PShaft    dSpeed (Deg/sec)  dTheta (Deg)
0    0.001    60      41.7727     1.16259  2.00E+09  -9.26E-05         -9.00E-10
0    0.002    60      41.7727     1.16259  2.00E+09  -9.26E-05         -2.43E-09
...

The first two columns contain the time evolution in hours & seconds while the third and 
subsequent columns indicate monitored quantities.

Frequency (Hz): network frequency (fundamental frequency, typical nominal values are
                50 or 60Hz)
Theta (Deg)     : rotor angle of the synchronous machine (generator)
Vd              : direct axis voltage of the generator terminal bus
PShaft          : shaft power or mechanical from prime mover (typically a hydro, 
                  gas or steam turbine that spins the generator to generate electricity)
dSpeed (Deg/sec): speed deviation of synchronous machine. This should be zero in steady 
                  state and vary after/during disturbances
dTheta (Deg)    : angular deviation of synchronous machine rotor. Should be zero in
                  steady state and vary after a disturbance.

Reference: 

Kundur, Prabha (1994) Power System Stability and Control, McGraw Hill, New York, New 
  York, pp. 1176.

Author: Peter A. Rochford
        Xator Corporation
        www.xatorcorp.com

Created on Aug 8, 2023

@author: peter.rochford@xatorcorp.com
'''

import argparse
import matplotlib.pyplot as plt
from matplotlib import rcParams
import opendss_scivis as osv
import skill_metrics as sm
        
if __name__ == '__main__':
    
    # Define optional arguments for script
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-noshow', dest='no_show', action='store_true',
                            help="No figure is shown if this flag is present.")
    arg_parser.add_argument('-nosave', dest='no_save', action='store_true',
                            help="No figure is saved if this flag is present.")
    args = arg_parser.parse_args()
    del arg_parser

    # Set the figure properties (optional)
    rcParams["figure.figsize"] = [8.0, 6.4] #works
    rcParams.update({'font.size': 12}) # font size of axes text

    # Close any previously open graphics windows
    plt.close('all')
        
    # Read data from OpenDSS CSV file
    filename = 'SimpleDemo_Mon_g1out_1'
    data = osv.read_element_data(filename)

    # Extract all data
    tsdata = osv.get_time_series([],data)
    max_number_plots = len(tsdata.keys()) - 1

    '''
    Produce line plot of all time series

    For an exhaustive list of options to customize your diagram, 
    please call the function at a Python command line:
    >> time_series_plot
    '''
    osv.time_series_plot(tsdata)

    # Write plot to file if arguments say so
    None if args.no_save else plt.savefig('example01.png')

    # Show plot if arguments say so
    None if args.no_show else plt.show()
