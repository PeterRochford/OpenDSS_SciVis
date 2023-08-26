'''
Gets list of Comma, Separated, Value (CSV) files in a directory

Input:

directory: directory path containing desired list of files

Output:

csv_files: a list of CSV files in the the directory

Created on Jun 28, 2023

Author: Kevin Wu
        Parsons Corporation
        www.parsons.com
'''
import os

def get_files_in_directory(directory):
    if not os.path.exists(directory):
        raise ValueError("Directory does not exist: " + directory)
    csv_files = []
    for file in os.listdir(directory):
        if file.endswith(".csv") or file.endswith(".CSV"):
            csv_files.append(file)
    return csv_files