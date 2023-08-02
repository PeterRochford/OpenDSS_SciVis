'''
This function gets the list of files in the directory

Input:

directory: The directory that user wants to get

Output:

csv_files: A list of CSV files in the the directory

Created on Jun 28, 2023

Author: Kevin Wu
        Parsons Corporation
        www.parsons.com
'''
import os

def get_files_in_directory(directory):
    csv_files = []
    for file in os.listdir(directory):
        extension = os.path.splitext(file)[1]
        extension = extension.lower()
        if extension == '.csv':
            csv_files.append(file)
    return csv_files