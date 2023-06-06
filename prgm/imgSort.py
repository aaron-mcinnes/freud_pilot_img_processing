# -*- coding: utf-8 -*-
"""
Created on Mon May 29 16:55:21 2023

@author: pc

Brings up a GUI for user to categorise images into window/no window
Will save mean/sd luminance along with file name and categorisation into the target path
"""
import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from PIL import Image, ImageTk
import shutil

## options
method = 'cielab__histMatch2_sfMatch1'
#sourceDirs = ['msp', 'stp']
extension = '.jpg'

#Set up paths
baseDir = os.path.join(os.path.dirname(os.getcwd()), '3_calibImg') 
sourceDirs = os.listdir(baseDir) 
sourceDirs = list(filter(lambda item: item != 'all', sourceDirs))
sourcePaths = [os.path.join(baseDir, dir, method) for dir in sourceDirs]
targetPaths = [os.path.join(os.path.dirname(os.getcwd()), '4_sortedImg', dir) for dir in sourceDirs]
statsPath = os.path.join(baseDir, 'all', method, 'DIAGNOSTICS', 'meanVec.csv')

class ImageCategorizer:
    def __init__(self, root, source_dir):
        self.root = root
        self.image_paths = []
        self.current_index = 0
        self.source_dir = source_dir

        # Create GUI elements
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.label = tk.Label(root, text="Does the landmark have windows?")
        self.label.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.yes_button = tk.Button(self.button_frame, text="Yes", width=10, command=self.save_categorization_yes)
        self.yes_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.no_button = tk.Button(self.button_frame, text="No", width=10, command=self.save_categorization_no)
        self.no_button.pack(side=tk.LEFT, padx=5, pady=5)

        # self.skip_button = tk.Button(self.button_frame, text="Skip", width=10, command=self.skip_image)
        # self.skip_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.reject_button = tk.Button(self.button_frame, text="Reject", width=10, command=self.reject_image)
        self.reject_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.flag_button = tk.Button(self.button_frame, text="Flag", width=10, command=self.flag_image)
        self.flag_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.note_label = tk.Label(root, text="Notes:")
        self.note_label.pack()

        self.note_entry = tk.Entry(root, width=30)
        self.note_entry.pack()

        self.save_button = tk.Button(root, text="Save and Quit", width=15, command=self.save_and_quit)
        self.save_button.pack(pady=10)

        # Load image paths
        self.load_image_paths()

        # Display first image
        self.display_image()

    def load_image_paths(self):
        file_paths = os.listdir(self.source_dir)
        self.image_paths = [os.path.join(self.source_dir, file) for file in file_paths if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if not self.image_paths:
            messagebox.showinfo("Image Categorization", "No images found in the specified directory!")
            self.root.destroy()

    def display_image(self):
        if self.current_index < len(self.image_paths):
            image_path = self.image_paths[self.current_index]
            image = Image.open(image_path)
            image = image.resize((400, 400), Image.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        else:
            messagebox.showinfo("Image Categorization", "All " + imgCity + " images categorized!")

    def save_categorization_yes(self):
        self.save_categorization(True, False, False)

    def save_categorization_no(self):
        self.save_categorization(True, False, False)
        
    def reject_image(self):
        self.save_categorization(False, True, False)
    
    def flag_image(self):
        self.save_categorization(True, False, True)

    def save_categorization(self, has_windows, rejectImg, flagImg):
        image_path = self.image_paths[self.current_index]
        image_name = os.path.basename(image_path)  # Extract only the file name
        notes = self.note_entry.get()

        csv_file = os.path.join(os.path.dirname(targetPath), 'img_info.csv') 

        #get the image luminance and contrast
        colorspace = method.split('_')[0]
        shortName = image_name.replace('SHINE_color_' + colorspace + '_', '')
        statsPath = os.path.join(baseDir, 'all', method, 'DIAGNOSTICS', 'meanVec.csv')
        meanVec = pd.read_csv(statsPath)
        meanLum = meanVec.loc[meanVec['img'] == shortName, 'meanLum'].values[0]
        sdLum = meanVec.loc[meanVec['img'] == shortName, 'sdLum'].values[0]
                
        # Save data to spreadsheet
        data = {'Image': [image_name], 'City': [imgCity], 'HasWindows': [has_windows], 
                'Reject': [rejectImg], 'Flag': [flagImg],
                'meanLum':[meanLum],'sdLum':[sdLum], 'colorspace': [colorspace], 'Notes': [notes]}
        df = pd.DataFrame(data)

        # Check if the file already exists
        if os.path.isfile(csv_file):
            df.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_file, index=False)

        #make img rejection folder
        rejectPath = targetPath.replace('4_sortedImg', '4_badImg')
        
        #categorise into folder
        if rejectImg or flagImg:
            if rejectImg:
                winCategory = 'reject'
            elif flagImg:
                winCategory = 'flag'
            categoryFolder = os.path.join(rejectPath, winCategory)
        else :
            if has_windows:
                winCategory = 'win'
            else:
                winCategory = 'nowin'
            categoryFolder = os.path.join(targetPath, winCategory)
        if not os.path.isdir(categoryFolder):
            os.makedirs(categoryFolder, exist_ok=True)
        shutil.copy(image_path, categoryFolder)
        
        self.current_index += 1
        self.note_entry.delete(0, tk.END)
        self.display_image()
        

    def skip_image(self):
        self.current_index += 1
        self.note_entry.delete(0, tk.END)
        self.display_image()

    def save_and_quit(self):
        self.root.destroy()

i = 0
for path in sourcePaths:
    print('categorising ' + path)
    source_directory = path
    targetPath = targetPaths[i]
    if not os.path.isdir(targetPath):
        os.makedirs(targetPath, exist_ok=True)

    #get whether msp/stp
    for city in sourceDirs:
        if city in path:
            imgCity = city
    
    # Create the root window
    root = tk.Tk()
    root.title("Image Categorizer")
    
    # Create the ImageCategorizer object with the source directory
    app = ImageCategorizer(root, source_directory)
    
    # Start the Tkinter event loop
    root.mainloop()
    i = i+1



