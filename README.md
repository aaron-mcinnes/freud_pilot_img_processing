# freud_pilot_img_processing
calibrating images for TOI1 pilot task

Scripts to run image calibration are in the prgm folder. 
This assumes that source images are sorted into RawImg>Minneapolis_Raw or RawImg>StPaul_Raw

Images are processed in the following steps:

1. Images in .heic (or other) format are converted to .jpg. 
*Input is RawImg folder and output is 1_convertedImg, using prgm>img2jpg.py

2. Images are cropped 
*Input is 1_convertedImg and output is 2_croppedImg, using prgm>imgCrop.py
*Images are cropped from the center and downsampled to the minimum resolution of the source images (i.e. output images are all exactly the same size)

3. Images are calibrated for luminance and contrast
*Input is 2_croppedImg and output is 3_calibImg, using imgCalibration.m
*Additional post-processing statistics are calculated using compLum.m
*See calibResults.ipynb for a detailed description of the method used and example output of the image calibration

4. Images are sorted into msp/stp win/nowin 
*Input is 3_calibImg and output is 4_sortedImg, using prgm>imgSort.py
*imgSort.py produces a GUI that displays each image and lets the user categorise the image as window or non window. The user can also attach notes to the images.
In the output directory, folders are structured according to Intheon's naming convention for the GNAT file structure.
i.e. msp>nowin, msp>win, stp>nowin, stp>win
Inside the output directory, a .csv is stored with the following:
-Image name 
-City 
-Has Windows (boolean)
-Mean Luminance 
-SD Luminance 
-Colorspace 
-User notes 





