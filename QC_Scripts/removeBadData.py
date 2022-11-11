import os

BAD_COMBO_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/geojson_files"
IMG_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/RGB-PanSharpen"
MASK_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/geojson_masks"

BAD_IMG_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/geojson_masks"
BAD_MASK_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/geojson_masks"

for filename in os.listdir(BAD_COMBO_DIR_PATH):
    tiffName = filename.split('.')[0] + ".tif"

    path_to_img = os.path.join(IMG_DIR_PATH, tiffName)
    path_to_mask = os.path.join(MASK_DIR_PATH, tiffName)

    if os.path.exists(path_to_img) and os.path.exists(path_to_mask):
        badImgDest = os.path.join(BAD_IMG_PATH, tiffName)
        badMaskDest = os.path.join(BAD_MASK_PATH, tiffName)

        os.rename(path_to_img, badImgDest)
        os.rename(path_to_mask, badMaskDest)