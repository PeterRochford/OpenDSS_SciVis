import numpy as np
from opendss_scivis.read_element_data import read_element_data
from skill_metrics import bias
from skill_metrics import bias_percent
from skill_metrics import centered_rms_dev
from skill_metrics import rmsd

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
def colname_stats(file_ref, file_mod):
    '''
    Calculate statistical metrics of the differences between Comma Separated Value (CSV) files
    for each column in the file.
    
    The function first checks to see if the dimensions of the two CSV files are the same. 
    It then loops through each column and checks if the columns in the two files are the same. 
    If it is not the same, then it will calculate several statistical metrics and return them in 
    a dictionary which will be the value of the outer dictionary with the key of the outer 
    dictionary the column name. 
    
    Example output: {col1:{'bias':bias,'crmsd':crmsd,...}, ...
                     col2:{'bias':bias,'crmsd':crmsd,...},...}
    
    Input:
    file_ref: the reference CSV file
    file_mod: the model CSV file that is used to compare with the reference
    
    Output: 
    col_dict: a dictionary that contains dictionaries of statistical metrics
    '''
    
    # Get data from CSV files
    csv1 = read_element_data(file_ref)
    csv2 = read_element_data(file_mod)
    # if csv1.shape == csv2.shape:
    #     print("The files have the same size")
    # else:
    #     raise Exception("The file sizes do not match")

    '''
    Create a dictionary where the key is the column name and its values is another
    dictionary containing the statistical metrics calculated, e.g., 
    metrics = {"bias": bias, "rmse": rmse, ...}. 

    This provides the flexibility to add other metrics returned by the function in future
    without breaking earlier written code. 
    '''
    
    file_success = 'Pass' # Assume test for all column passes by default
    
    col_dict={}
    for col in csv1.columns:
        if col == 'Unnamed: 8':
            break
        metrics={}
        if not csv1[col].equals(csv2[col]):
            value_ref=np.array(csv1[col].tolist())
            value_model=np.array(csv2[col].tolist())
            metrics['bias']= bias(value_model,value_ref)
            metrics['crmsd']=centered_rms_dev(value_model,value_ref)
            metrics['rmsd']=rmsd(value_model,value_ref)
    
            sdevm = np.std(value_model)
            sdevr = np.std(value_ref)
            metrics['sdev'] = [sdevr, sdevm]
            
            if sdevm == 0 or sdevr == 0:
                ccoef = -1
            else:
                ccoef=np.corrcoef(value_model,value_ref)
                metrics['ccoef'] = ccoef[0]

            Bp = bias_percent(value_model,value_ref)
            metrics['bias_percent'] = Bp
            
            metrics['success'] = pass_fail(metrics)
            if metrics['success']=='Fail':
                file_success='Fail'
        else:
            metrics['success'] = 'Pass'

        col_dict[col] = metrics
    
    col_dict['success'] = file_success

    return col_dict

'''
ToDo: We'll need to investigate using other statistical metrics for the pass/fail. 
The t-test is based on the assumption one is comparing two statistical samples for
a significant difference. For our current application, we are doing a test to see
if a software application exactly reproduces a previous result, i.e. a verification 
test. We expect the element by element difference to be zero or relatively small and
wish to know whenever such is the case. 
'''
def pass_fail(metrics,tolerance=0.1):
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
    #ToDo: check for presence of key 'bias_percent'
    if metrics['bias_percent'] < tolerance:
        return 'Pass'
    else:
        return 'Fail'
