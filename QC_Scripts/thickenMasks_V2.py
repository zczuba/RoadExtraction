import cv2
import numpy as np
import os

##### PATHS #####
ORIGINAL_IMG_PATH = "/mnt/vol1/312018241_HD_Map_Fern_Phoenix/Outputs/Model_Training_Data/Dataset_3_V2/Images"
ORIGINAL_MASK_PATH = "/mnt/vol1/312018241_HD_Map_Fern_Phoenix/Outputs/Model_Training_Data/Dataset_3_V2/Masks"
MODDED_IMG_PATH = "/mnt/vol1/312018241_HD_Map_Fern_Phoenix/Outputs/Modified_Data/Output_3/Images"
MODDED_MASK_PATH = "/mnt/vol1/312018241_HD_Map_Fern_Phoenix/Outputs/Modified_Data/Output_3/Masks"
BAD_IMG_PATH = "/mnt/vol1/312018241_HD_Map_Fern_Phoenix/Outputs/Modified_Data/Output_3/Bad_Images"


##### Functions #####
'''Makes a list with all of the masks for the image entered'''
# Input: Image
# Output: List of mask images
def generate_mask_list(imageName):
    maskList = []
    maskFolder = os.path.join(ORIGINAL_MASK_PATH, imageName.split(".")[0])
    for mask in os.listdir(maskFolder):
        if mask.endswith(".tif"):
            path_to_mask = os.path.join(maskFolder, mask)
            maskList.append(cv2.imread(path_to_mask))
    return maskList

'''Makes a single mask image of all the masks from the entered list of masks'''
# Input: List of mask images
# Output: Single mask image
def stitch_mega_mask(maskList):
    megaMask = maskList[0]
    if len(maskList) <= 1:
        return megaMask
    else:
        for i in range(1, len(maskList)):
            megaMask = cv2.add(megaMask, maskList[i])
        return megaMask


##### Global Variables #####
defaultKernel = np.ones((5, 5), np.uint8)
southKernel = np.array([[1,1,1,1,1], [0,0,0,0,0], [0,0,0,0,0] ,[0,0,0,0,0] , [0,0,0,0,0]], np.uint8)
westKernel = np.array([[0,0,0,0,1], [0,0,0,0,1], [0,0,0,0,1] ,[0,0,0,0,1] , [0,0,0,0,1]], np.uint8)
northKernel = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0] ,[0,0,0,0,0] , [1,1,1,1,1]], np.uint8)
eastKernel = np.array([[1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0] ,[1,0,0,0,0] , [1,0,0,0,0]], np.uint8)


'''Main'''
for filename in os.listdir(ORIGINAL_IMG_PATH):
    if filename.endswith('.tif'):
        path_to_img = os.path.join(ORIGINAL_IMG_PATH, filename)
        originalMaskList = generate_mask_list(filename)

        img = cv2.imread(path_to_img)
        megaMask = stitch_mega_mask(originalMaskList)
        combo = cv2.add(img, megaMask)
        # cv2.namedWindow(filename)
        # cv2.moveWindow(filename, 0, 0)
        
        moddedMaskList = originalMaskList.copy()
        index = 0
        preview = True
        megaMaskShowing = False
        displayString = f"{filename} - MaskCount = {len(originalMaskList)}"

        while(1):
            # if preview == True:
            #     displayString = f"{filename}: Preview"
            # elif megaMaskShowing == True:
            #     displayString = f"{filename}: Final"
            # else:
            #     displayString = f"{filename}: LineString {index+1}/{len(originalMaskList)}"

            cv2.imshow(displayString, combo)
            k = cv2.waitKey(0)

            # Esc key - Quit the script
            if k == 27:
                numRemaining = len([entry for entry in os.listdir(ORIGINAL_IMG_PATH) if os.path.isfile(os.path.join(ORIGINAL_IMG_PATH, entry))])
                print(f"\n{numRemaining} images left\n")
                exit()

            # Up arrow - Dilate
            elif k == 0:
                if megaMaskShowing == False and preview == False:        
                    moddedMaskList[index] = cv2.dilate(moddedMaskList[index], defaultKernel, iterations=1)
                    combo = cv2.add(img, moddedMaskList[index])

            # Down arrow - Erode
            elif k == 1:  
                if megaMaskShowing == False and preview == False:
                    moddedMaskList[index] = cv2.erode(moddedMaskList[index], defaultKernel, iterations=1)
                    combo = cv2.add(img, moddedMaskList[index])

            # Left arrow - Cycle back line string
            elif k == 2:
                if megaMaskShowing == True:
                    combo = cv2.add(img, moddedMaskList[index])
                    megaMaskShowing = False

                elif index > 0 and preview == False:
                    index -= 1
                    combo = cv2.add(img, moddedMaskList[index])

            # Right arrow - Cycle forward line string
            elif k == 3:
                if preview == True:
                    combo = cv2.add(img, moddedMaskList[index])
                    preview = False

                elif index < len(moddedMaskList) - 1:
                    index += 1
                    combo = cv2.add(img, moddedMaskList[index])

                else:
                    megaMask = stitch_mega_mask(moddedMaskList)
                    combo = cv2.add(img, megaMask)
                    megaMaskShowing = True

            # W - Nudge North
            elif k == 119:
                if megaMaskShowing == False and preview == False:
                    moddedMaskList[index] = cv2.dilate(moddedMaskList[index], northKernel, iterations=1)
                    combo = cv2.add(img, moddedMaskList[index])

            # D - Nudge East
            elif k == 100:
                if megaMaskShowing == False and preview == False:
                    moddedMaskList[index] = cv2.dilate(moddedMaskList[index], eastKernel, iterations=1)
                    combo = cv2.add(img, moddedMaskList[index])

            # S - Nudge South
            elif k == 115:
                if megaMaskShowing == False and preview == False:
                    moddedMaskList[index] = cv2.dilate(moddedMaskList[index], southKernel, iterations=1)
                    combo = cv2.add(img, moddedMaskList[index])

            # A - Nudge West
            elif k == 97:
                if megaMaskShowing == False and preview == False:
                    moddedMaskList[index] = cv2.dilate(moddedMaskList[index], westKernel, iterations=1)
                    combo = cv2.add(img, moddedMaskList[index])

            # Space - Reset current line to Original
            elif k == 32:
                if megaMaskShowing == False and preview == False:
                    moddedMaskList[index] = originalMaskList[index]
                    combo = cv2.add(img, moddedMaskList[index])

            # Tab - Reset all to original
            elif k == 9:
                moddedMaskList = originalMaskList.copy()
                index = 0
                combo = cv2.add(img, moddedMaskList[index])
                megaMaskShowing == False
                
            # Enter - Save New Mask
            elif k == 13:
                if megaMaskShowing == True:
                    moddedImgDest = os.path.join(MODDED_IMG_PATH, filename)
                    moddedMaskDest = os.path.join(MODDED_MASK_PATH, filename)
                    megaMask = stitch_mega_mask(moddedMaskList)
                    cv2.destroyAllWindows()
                    cv2.imwrite(moddedMaskDest, megaMask)
                    os.rename(path_to_img, moddedImgDest)
                    print(f'{filename} moved to MODDED')
                    break
            
            # Delete - Mark Image as BAD
            elif k == 127:
                badImgDest = os.path.join(BAD_IMG_PATH, filename)
                cv2.destroyAllWindows()
                os.rename(path_to_img, badImgDest)
                print(f'{filename} moved to BAD')
                break
