# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 2022
@author: zczuba

Script to generate masks for each image. End result is a folder for each image that has masks for each LineString in the geoJSON within

"""
import os
import fiona
import rasterio
import rasterio.mask
import numpy as np
import cv2

GEOJSON_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/doOver/GeoJSONs"
IMG_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/doOver/Images"
MASK_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/doOver/Masks"

# convert the geojson to mask
count = 0
for filename in os.listdir(GEOJSON_DIR_PATH):
    if filename.endswith('.geojson'):
        path_to_file = os.path.join(GEOJSON_DIR_PATH, filename)
        path_to_img = os.path.join(IMG_DIR_PATH, filename.split('.')[0] + ".tif")
        
        if os.path.exists(path_to_file) and os.path.exists(path_to_img):
            # print(filename)
            mask_dir_name = os.path.join(MASK_DIR_PATH, filename.split(".")[0])
            if not os.path.exists(mask_dir_name):
                os.makedirs(mask_dir_name)

            with fiona.open(path_to_file, "r") as geojson:
                geoms = [feature["geometry"] for feature in geojson]

            for i, geo in enumerate(geoms):
                geoList = []
                geoList.append(geo)
                with rasterio.open(path_to_img) as src:
                    # print(geo)
                    out_image, out_transform = rasterio.mask.mask(src, geoList, crop=False, nodata=0, invert=False)
                    out_meta = src.meta.copy()

                out_meta.update({"driver": "GTiff",
                                "height": out_image.shape[1],
                                "width": out_image.shape[2],
                                "transform": out_transform})

                path_to_mask = os.path.join(mask_dir_name, f"{i}.tif")

                with rasterio.open(path_to_mask, "w", **out_meta) as dest:
                    binarized = np.where(out_image > 0, 255, 0)
                    dest.write(binarized)

                img = cv2.imread(path_to_mask)
                kernel = np.ones((5, 5), np.uint8)
                img_dilation = cv2.dilate(img, kernel, iterations=9)
                
                cv2.imwrite(path_to_mask, img_dilation)
            
        else:
            print(f"Error with {filename}")

print("Done!")
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
