# -*- coding: utf-8 -*-
"""
Created on Wed May 24 20:15:26 2023

@author: pc

Searches image directories and converts them to .jpg if they are in a different format
Assumes that this script is saved in a folder which is a sister directory of "RawImg"
"""

from wand.image import Image #install imagemagick on your system as well https://docs.wand-py.org/en/0.6.11/guide/install.html#install-imagemagick-on-windows
import shutil
import os
import pandas as pd
import re
import os.path

from tqdm import tqdm


def checkjpg(sourceFile):
    _, extension = os.path.splitext(sourceFile)
    return extension.lower() != '.jpg' and extension.lower() != '.jpeg'

def convert2jpg(sourceFile, targetPath):
    img = Image(filename = sourceFile)
    img.format='jpg'
    img.save(filename=targetPath)
    img.close()

def filter_folders(file_directories):
    filtered_directories = []
    for directory in file_directories:
        if os.path.isdir(directory):
            filtered_directories.append(directory)
    return filtered_directories

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

# Provides the directory of the two image folders relative to this script
rawDir = os.path.join(os.path.dirname(os.getcwd()), 'RawImg') 
sourceFolders = os.listdir(rawDir)
sourcePaths = list(map(lambda element: rawDir + "\\" +  element, sourceFolders))
sourcePaths = filter_folders(sourcePaths)

#check for rejected photos according to Michael's accept/reject .xlsx
listPath = os.path.join(os.getcwd(), 'FREUD Photograph Accept or Reject List.xlsx') 
acceptList = pd.read_excel(listPath)
filteredList = acceptList[acceptList['AcceptFlag'] == 0] #find the rejected images
photos2reject = filteredList['Photo Name'].tolist() #store the rejected image names


#iterate over the source directories
for path in sourcePaths:
    sourceDir = path
    #set the target path
    targetDir = sourceDir.replace('RawImg', '1_convertedImg') 
    targetDir = targetDir.replace('_Raw', '_Converted')
    targetDir = targetDir.replace('Minneapolis', 'msp') #keep consistent with intheon naming convention
    targetDir = targetDir.replace('StPaul', 'stp') #keep consistent with intheon naming convention
    targetDir = targetDir.replace('Control', 'ctl') #keep consistent with intheon naming convention
    # Create the target directories if they don't exist
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    print('\n>>Converting images in {} to {}'.format(sourceDir, targetDir))
    #iterate over the files in the source path
    with tqdm(total = len(os.listdir(sourceDir))) as pbar:
        for file in os.listdir(sourceDir):
            pbar.update(1)
            if os.path.splitext(file)[0] in photos2reject: #skip if it is a rejected image
                print('rejected image ' + file)
                continue
            sourceFile = os.path.join(sourceDir, file)
            sourceName = os.path.splitext(file)[0]
            # if len(sourceName) > 50: #trim file name if it is too long (causes error in matlab processing)
            #     sourceName = sourceName[0:50]
            sourceName = imgRename(targetStrings, sourceName)
            targetPath = os.path.join(targetDir, sourceName + ".jpg")
            if os.path.isfile(targetPath):
                targetPath = os.path.join(targetDir, sourceName + "_2" + ".jpg")
            if checkjpg(sourceFile): #if not jpg
                convert2jpg(sourceFile, targetPath) #convert to jpg in target folder
            else:
                shutil.copy2(sourceFile, targetPath)
    #check that all images made it safely -- Don't check anymore bc images are checked for rejection
    if len(os.listdir(sourceDir)) == len(os.listdir(targetDir)) :
        print('\n>>All images in {} were converted to {}'.format(sourceDir, targetDir))
    else:
        print('\n>>Files were lost in conversion. Check for errors')
        break


print('Done!')


            


        