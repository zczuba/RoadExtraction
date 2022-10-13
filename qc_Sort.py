import cv2
import os

UNSORTED_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/combo"
GOOD_IMG_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/combo/00_GoodToGo"
BAD_IMG_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/combo/02_Bad"

# img = cv2.imread('/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/json_files/190_1.tif') # load a dummy image
# while(1):
#     cv2.imshow('img',img)
#     k = cv2.waitKey(0)
#     if k==27:    # Esc key to stop
#         break
#     elif k==-1:  # normally -1 returned,so don't print it
#         continue
#     else:
#         print(k) # else print its value

for filename in os.listdir(UNSORTED_DIR_PATH):
    if filename.endswith('.png'):
        path_to_img = os.path.join(UNSORTED_DIR_PATH, filename)
        img = cv2.imread(path_to_img)

        while(1):
            print(filename)
            cv2.imshow(filename, img)
            k = cv2.waitKey(0)
            if k == 27:    # Esc key to stop
                exit()
            elif k == 13:  # Enter
                goodDest = os.path.join(GOOD_IMG_PATH, filename)
                os.rename(path_to_img, goodDest)
                break
            elif k == 127:  # Delete
                badDest = os.path.join(BAD_IMG_PATH, filename)
                os.rename(path_to_img, badDest)
                break