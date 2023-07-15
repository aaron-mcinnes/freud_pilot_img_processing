# -*- coding: utf-8 -*-
"""
Created on Thu May 25 08:52:47 2023

@author: pc

Crops images into a square and sets a fixed resolution for all images
There is a function that finds the minimum resolution across the source folders for downsampling
Alternatively, a fixed resolution can be set for all images, 
e.g. targetResolution = (600 x 600)
"""

from PIL import Image, ExifTags
import os
from tqdm import tqdm

############################### options #######################################
downsample = 1 #whether or not you want to downsample to the minimum resolution of all images in collection
targetMinResolution = 700 #images will be rejected if x or y resolution is below this 
###############################################################################


#when cropping, images are rotated if their height is greater than width. This gets the orientation so they can be rotated before cropping if needed
def get_exif_orientation(image):
    try:
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == 'Orientation':
                    return value
    except AttributeError:
        # Image has no attribute '_getexif'
        pass
    return 1 

#this rotates the image if needed
def rotate_image(image):
    orientation = get_exif_orientation(image)
    if orientation == 3:
        return image.rotate(180, expand=True)
    elif orientation == 6:
        return image.rotate(-90, expand=True)
    elif orientation == 8:
        return image.rotate(90, expand=True)
    return image

#crops images to square
def crop2square(file, targetDir):
    # Open the image
    sourcePath = os.path.join(sourceDir, file)
    image = Image.open(sourcePath)
    image = rotate_image(image)
        
    # Get the dimensions of the image
    width, height = image.size

    # Calculate the size of the square to crop
    size = min(width, height)

    # Calculate the coordinates for cropping
    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))
    if downsample:
        cropped_image.thumbnail(targetResolution)

    # Save the cropped image with the same filename
    targetFile = os.path.splitext(file)[0] + "_cropped.jpg"
    targetPath = os.path.join(targetDir, targetFile)
    cropped_image.save(targetPath)
    
# Function to get the resolution of an image
def get_image_resolution(image_path):
    with Image.open(image_path) as img:
        return img.size

# Function to find the minimum resolution among multiple images
#also reject images if they are below target res 
def find_minimum_resolution(image_paths):
    min_resolution = float('inf')
    badPaths = []
    for path in image_paths:
        resolution = get_image_resolution(path)
        min_resolution = min(min_resolution, min(resolution))
        if min_resolution < targetMinResolution:
            badPaths.append(path)
            min_resolution = targetMinResolution
    return [min_resolution, badPaths]


# Specify the path to your folder of images
rawDir = os.path.join(os.path.dirname(os.getcwd()), '1_convertedImg') 
sourceFolders = os.listdir(rawDir)
sourcePaths = list(map(lambda element: rawDir + "\\" +  element, sourceFolders))

#get paths to search across
if downsample:
    all_image_paths = []
    for folder in sourcePaths:
        image_paths = [os.path.join(folder, filename) for filename in os.listdir(folder)]
        all_image_paths.extend(image_paths)
    
minRes = find_minimum_resolution(all_image_paths)
targetResolution = (minRes[0], minRes[0])

for path in sourcePaths:
    sourceDir = path
    #set the target path
    targetDir = sourceDir.replace('1_convertedImg', '2_croppedImg') 
    targetDir = targetDir.replace('_Converted', "")
    #set path for rejected photos (resolution too low)
    junkDir = sourceDir.replace('1_convertedImg', '4_badImg') 
    junkDir = junkDir.replace('_Converted', "_ResolutionTooLow")
    # Create the target directories if they don't exist
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    if not os.path.exists(junkDir):
        os.makedirs(junkDir)
    print('\n>>Cropping images in \n{} to \n{}\n'.format(sourceDir, targetDir))
    with tqdm(total = len(os.listdir(sourceDir))) as pbar:
        for file in os.listdir(sourceDir):
            pbar.update(1)
            if os.path.join(sourceDir, file) in minRes[1]:
                crop2square(file, junkDir)
                continue
            else:
                crop2square(file, targetDir)
    #check that all images made it safely
    if len(os.listdir(sourceDir)) == len(os.listdir(targetDir)) :
        print('\n>>All images in {} were cropped to {}'.format(sourceDir, targetDir))
    else:
        nCropped = len(os.listdir(targetDir))
        nRemoved = len(os.listdir(sourceDir)) - len(os.listdir(targetDir))
        print('\n>>{} valid images cropped to {}. {} images were removed due to low resolution.'.format(nCropped, targetDir, nRemoved))
        


