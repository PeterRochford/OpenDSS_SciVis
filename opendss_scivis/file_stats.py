'''
This function compares the csv files in a pair of directories. It first gets the model directory and 
checks to see if the files in the model directory exist in the reference directory. It the checks if 
any column statistic has a fail and if it does it will mark all_success as 'Fail'

Input:
mod_dir: the model directory the user wants to test
ref_dir: reference directory against which the user wants to compare

Keywords:
exclude: a list of file names to be excluded from comparison as specified by substrings,
         e.g., exclude=['Summary','YPRIM'] to ignore any files containing these substrings in the
         filenames

Output:
file_dict: a dictionary with the key being the file name and the value being the statistic
all_success: the value that checks to see whether the test has passed or failed

Created on Jun 28, 2023

Author: Kevin Wu
        Parsons Corporation
        www.parsons.com
'''
import os
from opendss_scivis.get_files_in_directory import get_files_in_directory
from opendss_scivis.colname_stats import colname_stats

def file_stats(mod_dir, ref_dir, exclude=None):
    
    try:
        mod_file = get_files_in_directory(mod_dir)
    except ValueError as err:
        print(err.args)
        print(os.getcwd())
        mod_file = []

    file_dict = {}
    if mod_file:
        # Non-empty list of files
        all_success = 'Pass' # Assume test for all files pass by default
    else:
        # Empty file list 
        all_success = 'Fail' # Test fails because there are no files
        return file_dict,all_success

    if not (exclude is None):
        if type(exclude) == str: exclude = [exclude]

    for file_name in mod_file:
        if not (exclude is None):
            skip = False
            for substr in exclude:
                if substr in file_name:
                    skip = True
                    break

        if skip: continue
        ref_file_path = os.path.join(ref_dir, file_name)
        if not os.path.isfile(ref_file_path):
            raise Exception(f"File '{file_name}' does not exist in the reference directory: " + ref_dir)

        mod_file_path = os.path.join(mod_dir, file_name)
        col_dict = colname_stats(mod_file_path,ref_file_path)
        file_dict[file_name] = col_dict
        if col_dict['success'] != 'Pass': all_success='Fail'

    return file_dict,all_success
