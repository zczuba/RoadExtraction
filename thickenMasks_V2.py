import cv2
import numpy as np
import os

# Be sure to set the correct file paths for everything
ORIGINAL_IMG_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/doOver/Images"
ORIGINAL_MASK_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/doOver/Masks"

MODDED_IMG_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/doOver/Modded_Images"
MODDED_MASK_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/doOver/Modded_Masks"

BAD_IMG_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/doOver/BAD_IMAGES"

def generate_mask_list(imageName):
    maskList = []
    maskFolder = os.path.join(ORIGINAL_MASK_PATH, imageName.split(".")[0])
    for mask in os.listdir(maskFolder):
        if mask.endswith(".tif"):
            path_to_mask = os.path.join(maskFolder, mask)
            maskList.append(cv2.imread(path_to_mask))
    return maskList

def stitch_mega_mask(maskList):
    megaMask = maskList[0]
    if len(maskList) <= 1:
        return megaMask
    else:
        for i in range(1, len(maskList)):
            megaMask = cv2.add(megaMask, maskList[i])
        return megaMask

for filename in os.listdir(ORIGINAL_IMG_PATH):
    if filename.endswith('.tif'):
        path_to_img = os.path.join(ORIGINAL_IMG_PATH, filename)
        originalMaskList = generate_mask_list(filename)

        img = cv2.imread(path_to_img)
        combo = cv2.add(img, originalMaskList[0])
        # cv2.namedWindow(filename)
        # cv2.moveWindow(filename, 0, 0)

        kernel = np.ones((5, 5), np.uint8)
        moddedMaskList = originalMaskList.copy()
        index = 0
        megaMaskShowing = False

        while(1):
            cv2.imshow(filename, combo)
            k = cv2.waitKey(0)

            if k == 27:    # Esc key to quit the script
                exit()

            elif k == 0:    # Up arrow - Dilate
                if megaMaskShowing == False:        
                    moddedMaskList[index] = cv2.dilate(moddedMaskList[index], kernel, iterations=1)
                    combo = cv2.add(img, moddedMaskList[index])

            elif k == 1:    # Down arrow - Erode
                if megaMaskShowing == False:
                    moddedMaskList[index] = cv2.erode(moddedMaskList[index], kernel, iterations=1)
                    combo = cv2.add(img, moddedMaskList[index])

            elif k == 2: # Left arrow - Cycle back line string
                if megaMaskShowing == True:
                    combo = cv2.add(img, moddedMaskList[index])
                    megaMaskShowing = False

                elif index > 0:
                    index -= 1
                    combo = cv2.add(img, moddedMaskList[index])

            elif k == 3: # Right arrow - Cycle forward line string
                if index < len(moddedMaskList) - 1:
                    index += 1
                    combo = cv2.add(img, moddedMaskList[index])
                else:
                    megaMask = stitch_mega_mask(moddedMaskList)
                    combo = cv2.add(img, megaMask)
                    megaMaskShowing = True

            elif k == 32:  # Space - Reset current line to Original
                if megaMaskShowing == False:
                    moddedMaskList[index] = originalMaskList[index]
                    combo = cv2.add(img, moddedMaskList[index])

            elif k == 9: # Tab - Reset all to original
                moddedMaskList = originalMaskList.copy()
                index = 0
                combo = cv2.add(img, moddedMaskList[index])
                
            elif k == 13:   # Enter - Save New Mask
                moddedImgDest = os.path.join(MODDED_IMG_PATH, filename)
                moddedMaskDest = os.path.join(MODDED_MASK_PATH, filename)
                megaMask = stitch_mega_mask(moddedMaskList)
                cv2.destroyAllWindows()
                cv2.imwrite(moddedMaskDest, moddedMegaMask)
                os.rename(path_to_img, moddedImgDest)
                print(f'{filename} moved to MODDED')
                break

            elif k == 127:    # Delete - Mark Image as BAD
                badImgDest = os.path.join(BAD_IMG_PATH, filename)
                cv2.destroyAllWindows()
                os.rename(path_to_img, badImgDest)
                print(f'{filename} moved to BAD')
                break