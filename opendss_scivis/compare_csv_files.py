import numpy as np
import pandas as pd
import os
import sys
sys.path.append('C:\Users\FF16GK3\OpenDSS_SciVis')
import scipy.stats as stats
from skill_metrics import centered_rms_dev
from OpenDSS_SciVis.opendss_scivis.read_element_data import read_element_data


'''
This file allows users to compare files to see if there is any difference between them. 

It first sets a tolerance, for limiting the amount of difference, then counts to see how 
many differences are in the file. The function also searches/creates a folder for the 
comparison file. Then it takes in the Comma Separated Value (CSV) files the user wants 
to compare and checks to see if the files are the same size. Finally we compare
the CSV files to see if the two files have any significant differences based on the 
tolerance set.

Input:
file_old: name of the reference for the CSV file is trying to compare
file_new: name of the CSV file user wants to compare

output:
resolve: a dictionary containing ... (need to provide details once function finished)

Author: Kevin Wu
        Parsons Corporation
        www.parsons.com

Created on Jun 7, 2023

@author: kevin.wu@xatorcorp.com
'''
def colname_stat_dict(file_ref, file_mod,stat_list=[]):
    '''
    This is used to create a dictionary that contains another dictionary. 
    
    It first checks if stat_list has any value. Then it checks to see if the dimensions of the two csv files
    are the same. It loops through each column and checks if each column are the same. If it is not the same
    it will solve all the statistical metrics and put it into a dictionary which will be the value of the 
    outer dictionary and the key of the outer dictionary is the column name
    
    Example output: {col1:{'bias':bias,'crmsd':crmsd,...},col2:{{'bias':bias,'crmsd':crmsd,...},...}
    
    Input:
    file_ref: the reference csv file
    file_mod: the model csv file that is used to compare with the reference
    stat_list: a list for the statistical metrics that need to be solved
    
    Output: 
    col_dict: a dictionary that contains dictionaries of statistical metrics
    '''
    if len(stat_list)==0:
        stat_list=['bias_percent','bias','crmsd','rmsd','ccoef','sdev']
    
    csv1 = read_element_data(file_ref)
    csv2 = read_element_data(file_mod)
    if csv1.shape == csv2.shape:
        print("The files have the same size")
    else:
        raise Exception("The files size do not match")

    #ToDo: Have this function return a dictionary where the key is the 
    # column name, e.g. "P1" in the case of "SimpleDemo_Mon_g1_1.csv". 
    # different_columns['P1'] = 
    # Each element associated with the key will be another dictionary
    # containing the statistical metrics calculated, e.g., 
    # metrics = {"bias": bias, "rmse": rmse}
    # different_columns['P1'] = metrics
    #
    # We will essentially be returning a dictionary of dictionaries. This provides
    # the flexibility to add other metrics returned by the function in future
    # without breaking earlier written code. 
    #
    # Also put this function into a separate file as part of the opendss_scivis module. 
    
    col_dict={}
    for col in csv1.columns:
        if not csv1[col].equals(csv2[col]):
            stat_dict={}
            value_ref=np.array(csv1[col].tolist())
            value_model=np.array(csv2[col].tolist())
            for stat in stat_list:
                if stat == 'bias':
                    stat_dict['bias']= np.mean(value_model) - np.mean(value_ref)
                elif stat == 'crmsd':
                    #converts list to array because the function requires ndarray
                    stat_dict['crmsd']=centered_rms_dev(value_model,value_ref)
                elif stat == 'rmsd':
                    stat_dict['rmsd']=np.sqrt(np.sum(np.square(np.subtract(value_model,value_ref)))/float(value_model.size))
                elif stat == 'ccoef':
                    ccoef=np.corrcoef(value_model,value_ref)
                    stat_dict['ccoef'] = ccoef[0]
                elif stat == 'sdev':
                    sdevm = np.std(value_model)
                    sdevr = np.std(value_ref)
                    stat_dict['sdev'] = [sdevr, sdevm]
                elif stat == 'bias_percent':
                    #(model-reference)/reference
                    stat_dict['bias_percent']=pass_fail(value_ref, value_model)
            col_dict[col]=stat_dict
    print(col_dict)
    return col_dict

#ToDo: For now, leave this as a helper function for colname_difference. 
def calc_stat_by_col(file_ref, file_mod):
    '''
    This function takes the list from the colname_difference function and 
    converts the values in each column of the list. Using the list to find the average 
    and bias of each column.
    
    Input:
    file_old: the reference csv file
    file_new: the model csv file that is used to compare with the reference
    
    Output:
    stats: a dictionary containing statistics of the differences
    stats['bias'] = bias
    ...
    '''
    column_list = colname_stat_dict(file_ref, file_mod)
    csv1 = read_element_data(file_ref)
    csv2 = read_element_data(file_mod)
    stats={}
    for name in column_list:
        value1=csv1[name].tolist()
        value2=csv2[name].tolist()

        #ToDo: use statistics functions from the Skill Metrics package where 
        # possible, e.g. for the bias. This will ensure consistency with any 
        # target and Taylor diagrams we create with the same data. 
        avg1=np.mean(value1)
        avg2=np.mean(value2)
        bias= avg1-avg2
        stats[name]={"bias": bias}
    print(stats)
    return stats

'''
ToDo: We'll need to investigate using other statistical metrics for the pass/fail. 
The t-test is based on the assumption one is comparing two statistical samples for
a significant difference. For our current application, we are doing a test to see
if a software application exactly reproduces a previous result, i.e. a verification 
test. We expect the element by element difference to be zero or relatively small and
wish to know whenever such is the case. 
'''
def pass_fail(m,r,tolerance=0.01):
    '''
    This function checks the quotient of the bias and the reference average and compares it 
    with a tolerance which determines if there is significant difference.
    
    Input:
    m:     model data
    r:     reference data
    tolerance: the value that determines whether to pass or fail
    
    Output:
    Pass: if percentage is less than tolerance
    Fail: if percentage is greater than tolerance
    '''
    model=np.mean(m)
    ref=np.mean(r)
    bias_percent=abs((model-ref)/ref)
    if bias_percent<tolerance:
        return 'Pass'
    else:
        return 'Fail'

#ToDo: This needs to be one of the quantities returned in the metrics dictionary 
# of as discussed above in my feedback on the colname_difference function.
# We may also want to give some thought on renaming the functions but this should
# be relatively easy to do. (I implemented this in the colname_stat_dict function)
def csv_file_col_variation(file_ref, file_mod,tolerance=0.01):
    '''
    This function takes the list from the colname_difference function and 
    converts the values in each column of the list. Using the list to find the 
    average and bias of each column.
    
    Input:
    file_old: the reference csv file
    file_new: the model csv file that is used to compare with the reference
    
    Output:
    bias_dict: a dictionary that hold all the bias value from the columns 
    '''
    column_list = colname_stat_dict(file_ref, file_mod)
    csv1 = read_element_data(file_ref)
    csv2 = read_element_data(file_mod)
    test_result={}
    for name in column_list:
        value1=csv1[name].tolist()
        value2=csv2[name].tolist()
        pass_fail_result=pass_fail(value2, value1)
        test_result[name]=pass_fail_result
    print(test_result)
    return test_result