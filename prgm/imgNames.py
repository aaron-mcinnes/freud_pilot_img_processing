# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 12:34:04 2023

@author: freud
"""
import os
import pandas as pd
import re

# get file names of source images and processed images
targetStrings = ['Sullivan_', 'Ichel_', 'Buchanan', 'MPLS_', 'STP_', 'CTL_']
def imgRename(targetStrings, name):
    #replace target stringd
    for targetStr in targetStrings:
        name = name.replace(targetStr, '')
    name = name.replace('_', ' ')
    name = name.replace('-', ' ')
    name = re.sub(r'(?<!\s)([a-z])([A-Z])', r'\1 \2', name)    
    newName = name.title()
    newName = newName.split()
    #hard code some specific cases
    for i, word in enumerate(newName):
        if word.upper() in ["US", "SE", "NE", "UMN", "MN", "ATT", "CHS", "DNS", "SPS"]:
            newName[i] = word.upper()
        if "’S" in word:
            newName[i] = word.replace("’S", "’s")
    newName = " ".join(newName)
    if newName == 'M M S Store':
        newName = 'M&Ms Store'
    if newName == 'O’shaughnessy Stadium':
        newName = 'O’Shaughnessy Stadium'
    match = re.search(r'(\s)(\d+)$', newName)
    if match:
        space_number = match.group(0)  # The matched "<space><number>" string
        number = match.group(2)        # The matched "<number>" string
        newName = newName.replace(space_number, '_' + number)  # Replace space with underscore
    return newName

def filter_folders(file_directories):
    filtered_directories = []
    for directory in file_directories:
        if os.path.isdir(directory):
            filtered_directories.append(directory)
    return filtered_directories

# Provides the directory of the two image folders relative to this script
rawDir = os.path.join(os.path.dirname(os.getcwd()), 'RawImg') 
sourceFolders = os.listdir(rawDir)
sourcePaths = list(map(lambda element: rawDir + "\\" +  element, sourceFolders))
sourcePaths = filter_folders(sourcePaths)



#iterate over the source directories
for path in sourcePaths:
    sourceDir = path
    #save path
    csv_file = os.path.join(sourceDir, 'img_names.csv') 
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, file)
        sourceName = os.path.splitext(file)[0]
        processedName = imgRename(targetStrings, sourceName)
        # Save data to spreadsheet
        data = {'SourceName': [sourceName], 'ProcessedName': [processedName]}
        df = pd.DataFrame(data)

        # Check if the file already exists
        if os.path.isfile(csv_file):
            df.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_file, index=False)


