import os

IMG_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/doOver/Zac_Half/Modded_Images"
MASK_DIR_PATH = "/Users/zczuba/Documents/Sanborn_Projects/roadExtraction/doOver/Zac_Half/Clipped_Masks"

count = 1

for filename in os.listdir(IMG_DIR_PATH):
    path_to_img = os.path.join(IMG_DIR_PATH, filename)
    path_to_mask = os.path.join(MASK_DIR_PATH, filename)

    if os.path.exists(path_to_img) and os.path.exists(path_to_mask):
        newFilename = f"{count}.tif"
        new_img_path = os.path.join(IMG_DIR_PATH, newFilename)
        new_mask_path = os.path.join(MASK_DIR_PATH, newFilename)

        if os.path.exists(new_img_path) and os.path.exists(new_mask_path):
            print(f"Error with {filename} and {newFilename}")

        else:
            os.rename(path_to_img, new_img_path)
            os.rename(path_to_mask, new_mask_path)
            count += 1

    else:
        print(f"Error with {filename}")

print("Done!")