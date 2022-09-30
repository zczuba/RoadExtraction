# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 2022
@author: zczuba
"""
import os
import fiona
import rasterio
import rasterio.mask
from osgeo import osr, ogr, gdal
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)


geojsonDir_path = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/geojson_files"
imgDir_path = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/RGB-PanSharpen"

#-----------------------------------------------------------------------------
# To test individual image uncomment this part
#-----------------------------------------------------------------------------
# filename = "190.tif"
# path_to_img = os.path.join(imgDir_path, filename) 
# path_to_file = os.path.join(geojsonDir_path, filename.split('.')[0] + ".json")
# create_mask = CreateMask(path_to_img, path_to_file)
# xy, pixels, imgtif, features = create_mask.extract_lane_points()
# # create_mask.display()
# create_mask.save_mask(geojsonDir_path, imgDir_path)
# for feature in features:
#     if len(feature["geometry"]["coordinates"])>1:
#         for i in range(0, len(feature["geometry"]["coordinates"])):
#             print(feature["geometry"]["coordinates"][i])

#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# To run on a dirctory uncomment this part
#-----------------------------------------------------------------------------
# convert the geojson to mask
count = 0
for filename in os.listdir(geojsonDir_path):
    if filename.endswith('.geojson'):
        # filename = "192.json"
        # imgDir_path = "20190116/TIF_TFW"
        path_to_file = os.path.join(geojsonDir_path, filename)
        path_to_img = os.path.join(imgDir_path, filename.split('_')[0] + "_IMG.tif")       
        
        if os.path.exists(path_to_file) and os.path.exists(path_to_img):
            print(filename)
            mask_name = filename.split(".")[0] + ".tif"

            with fiona.open(path_to_file, "r") as geojson:
                geoms = [feature["geometry"] for feature in geojson]

            with rasterio.open(path_to_img) as src:
                out_image, out_transform = rasterio.mask.mask(src, geoms, crop=False, invert=False)
                out_meta = src.meta.copy()

            out_meta.update({"driver": "GTiff",
                            "height": out_image.shape[1],
                            "width": out_image.shape[2],
                            "transform": out_transform})

            with rasterio.open(mask_name, "w", **out_meta) as dest:
                # print(out_meta)
                
                dest.write(out_image)
            
        else:
            print(f"Error with {filename}")
        count += 1

        # if count==2:
        #     break

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------


