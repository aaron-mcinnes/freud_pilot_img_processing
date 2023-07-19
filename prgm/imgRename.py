# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 11:04:43 2023

@author: freud
"""

#rename images for word presentation
import os
import re



def imgRename(prefixes, sourceLoc):
    images = os.listdir(dir)
    for name in images:
        for prefix in prefixes:
            newName = name.replace(prefix, '') # replace string matches
            newName = re.sub(r'(?<!\s)([a-z])([A-Z])', r'\1 \2', name) #regex to search for "snake case". ALLCAPS need to be manually changed
        os.chdir(dir)
        os.rename(name, newName)
            

        
        