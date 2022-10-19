import cv2
import numpy as np
import os

ORIGINAL_IMG_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/Czuba_Data/Original_Data/Images"
ORIGINAL_MASK_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/Czuba_Data/Original_Data/Masks"

MODDED_IMG_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/Czuba_Data/Modded_Data/Images"
MODDED_MASK_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/Czuba_Data/Modded_Data/Masks"

# up == 0, down == 1

for filename in os.listdir(ORIGINAL_IMG_PATH):
    if filename.endswith('.tif'):
        path_to_img = os.path.join(ORIGINAL_IMG_PATH, filename)
        path_to_mask = os.path.join(ORIGINAL_MASK_PATH, filename)

        img = cv2.imread(path_to_img)
        mask = cv2.imread(path_to_mask)
        combo = cv2.add(img, mask)
        # cv2.namedWindow(filename)
        # cv2.moveWindow(filename, 0, 0)

        kernel = np.ones((5, 5), np.uint8)
        moddedMask = mask

        while(1):
            cv2.imshow(filename, combo)
            k = cv2.waitKey(0)

            if k == 27:    # Esc key to stop
                exit()

            elif k == 0:    # Up arrow - Dilate 
                moddedMask = cv2.dilate(moddedMask, kernel, iterations=1)
                combo = cv2.add(img, moddedMask)

            elif k == 1:    # Down arrow - Erode
                moddedMask = cv2.erode(moddedMask, kernel, iterations=1)
                combo = cv2.add(img, moddedMask)

            elif k == 127:  # Delete - Reset to Original
                moddedMask = mask
                combo = cv2.add(img, moddedMask)

            elif k == 13:  # Enter - Save New Mask
                moddedImgDest = os.path.join(MODDED_IMG_PATH, filename)
                moddedMaskDest = os.path.join(MODDED_MASK_PATH, filename)
                cv2.destroyAllWindows()
                cv2.imwrite(moddedMaskDest, moddedMask)
                os.rename(path_to_img, moddedImgDest)
                print(f'{filename} moved to GOOD')
                break

            

            
