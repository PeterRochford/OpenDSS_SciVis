import os
import pandas as pd

def read_element_data(name):
    '''
    Read data of an element in power grid that contains a time series of monitored power 
    system quantities from a Comma Separated Value (CSV) file output by OpenDSS.

    Input:
    name : name of CSV file with or without suffix, e.g. SimpleDemo.csv or SimpleDemo. 

    Output:
    objectData : data contained in CSV file as a two-dimensional data structure with labeled axes
    
    The data format of objectData is a DataFrame as provided by the pandas.read_csv function. An 
    example of the format for the contents of an OpenDSS CVS file is 
    
          hour   t(sec)   Frequency  ...        PShaft  dSpeed (Deg/sec)  dTheta (Deg)
0        0    0.001     60.0000  ...  2.000000e+09         -0.000093 -9.000000e-10
1        0    0.002     60.0000  ...  2.000000e+09         -0.000093 -2.430000e-09
2        0    0.003     60.0000  ...  2.000000e+09         -0.000093 -4.040000e-09
3        0    0.004     60.0000  ...  2.000000e+09         -0.000093 -5.660000e-09
4        0    0.005     60.0000  ...  2.000000e+09         -0.000093 -7.280000e-09
...    ...      ...         ...  ...           ...               ...           ...
4979     0    4.980     60.4106  ...  2.000000e+09       -575.187000  2.579670e+00
4980     0    4.981     60.4090  ...  2.000000e+09       -576.661000  2.569620e+00
4981     0    4.982     60.4074  ...  2.000000e+09       -578.108000  2.559550e+00
4982     0    4.983     60.4058  ...  2.000000e+09       -579.527000  2.549440e+00
4983     0    4.984     60.4041  ...  2.000000e+09       -580.918000  2.539320e+00

[4984 rows x 8 columns]

    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com
    
    Created on Apr 22, 2022
    '''

    # Check if CSV file suffix
    file_name, file_extension = os.path.splitext(name)
    if file_extension == "":
        filename = name + '.csv'
    elif file_extension.lower()=='.csv':
        filename = name
    else:
        raise Exception("Invalid file type: " + name)
    
    # Check if file exists and is readable
    if not os.path.isfile(filename):
        raise Exception("File does not exist: " + filename)
    elif not os.access(filename, os.R_OK):
        raise Exception("File is not readable: " + filename)
        
    # Load object from CSV file
    try:
        # Default of comma delimiter
        objectData = pd.read_csv(filename)
    except:
        # Second case of tab delimiter
        objectData = pd.read_csv(filename, delimiter='\t')
    
    return objectData
