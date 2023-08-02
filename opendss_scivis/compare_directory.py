'''
This function compares the csv files in a pair of directories. It first gets the model directory and 
checks to see if the files in the model directory exist in the reference directory. It the checks if 
any column statistic has a fail and if it does it will mark all_success as 'Fail'

Input:
mod_dir: the model directory the user want to test
ref_dir: reference directory the user want to compare the model directory to

Output:
file_dict: a dictionary with the key being the file name and the value being the statistic
all_success: the value that checks to see whether the test has passed or failed
Created on Jun 28, 2023

Author: Kevin Wu
        Parsons Corporation
        www.parsons.com
'''

import os
from opendss_scivis.get_file_directory import get_files_in_directory
from opendss_scivis.colname_stats import colname_stats

def file_stats(mod_dir, ref_dir):
    mod_file=get_files_in_directory(mod_dir)
    all_success = 'Pass' # Assume test for all files passes by default
    file_dict = {}
    for file_name in mod_file:
        ref_file_path = os.path.join(ref_dir, file_name)
        if not os.path.isfile(ref_file_path):
            raise Exception(f"File '{file_name}' does not exist in the reference directory.")
        mod_file_path = os.path.join(mod_dir, file_name)
        col_dict=colname_stats(mod_file_path,ref_file_path)
        file_dict[file_name]=col_dict
        if col_dict['success'] != 'Pass':
            all_success='Fail'
    return file_dict,all_success


    