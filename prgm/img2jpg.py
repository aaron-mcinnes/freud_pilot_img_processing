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

from tqdm import tqdm


def checkjpg(sourceFile):
    _, extension = os.path.splitext(sourceFile)
    return extension.lower() != '.jpg' and extension.lower() != '.jpeg'

def convert2jpg(sourceFile, targetPath):
    img = Image(filename = sourceFile)
    img.format='jpg'
    img.save(filename=targetPath)
    img.close()
    
     
# Provides the directory of the two image folders relative to this script
rawDir = os.path.join(os.path.dirname(os.getcwd()), 'RawImg') 
sourceFolders = os.listdir(rawDir)
sourcePaths = list(map(lambda element: rawDir + "\\" +  element, sourceFolders))


#iterate over the source directories
for path in sourcePaths:
    sourceDir = path
    #set the target path
    targetDir = sourceDir.replace('RawImg', '1_convertedImg') 
    targetDir = targetDir.replace('_Raw', '_Converted')
    targetDir = targetDir.replace('Minneapolis', 'msp') #keep consistent with intheon naming convention
    targetDir = targetDir.replace('StPaul', 'stp') #keep consistent with intheon naming convention
    # Create the target directories if they don't exist
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    print('\n>>Converting images in {} to {}'.format(sourceDir, targetDir))
    #iterate over the files in the source path
    with tqdm(total = len(os.listdir(sourceDir))) as pbar:
        for file in os.listdir(sourceDir):
            pbar.update(1)
            sourceFile = os.path.join(sourceDir, file)
            sourceName = os.path.splitext(file)[0]
            targetPath = os.path.join(targetDir, sourceName + ".jpg")
            if checkjpg(sourceFile): #if not jpg
                convert2jpg(sourceFile, targetPath) #convert to jpg in target folder
            else:
                shutil.copy2(sourceFile, targetPath)
    #check that all images made it safely
    if len(os.listdir(sourceDir)) == len(os.listdir(targetDir)) :
        print('\n>>All images in {} were converted to {}'.format(sourceDir, targetDir))
    else:
        print('\n>>Files were lost in conversion. Check for errors')
        break


print('Done!')




            

