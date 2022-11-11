# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 2022
@author: zczuba
"""
import os
import numpy as np
import cv2

IMG_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/Complete_Tiff"
MASK_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/Complete_Masks_v2"
COMBO_DIR = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/combo"

for filename in os.listdir(IMG_DIR_PATH):
    path_to_img = os.path.join(IMG_DIR_PATH, filename)
    path_to_mask = os.path.join(MASK_DIR_PATH, filename)
    
    if os.path.exists(path_to_img) and os.path.exists(path_to_mask):

        combo_name = filename.split(".")[0] + ".png"

        path_to_combo = os.path.join(COMBO_DIR, combo_name)

        img = cv2.imread(path_to_img)
        mask = cv2.imread(path_to_mask)
        combo = cv2.add(img, mask)
        
        cv2.imwrite(path_to_combo, combo)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------