# Instructions for Thicken Masks:

## Overview: A script to run you through a batch of images and masks and modify each mask in the corresponding image's mask folder, then output a single mask with all the modified individual masks stitched together.

## Instructions:
### BEFORE RUNNING
Set file paths in the script for
  1. Original Images
  2. Original Masks //directory of directories for each Image
  3. Destination for the Images once they have had their new mask modified
  4. Destination for the new Mask that is generated from this script
  5. A destination for images that have been designated as Bad (bad mask coverage, etc.)
 
### RUNNING THE SCRIPT
#### START
Opens an image with all of its individual masks overlayed on top. 
  - This lets you do a quick QC check to see if there is a mask in place for the expected roads in the image

Available Actions:
Right Arrow Key = Start adjusting mask line segments for the image (Jump to next section)
Backspace = Move image to Bad Folder and start process with next image

#### INDIVIDUAL LINE STRING ADJUSTMENT
Opens the current image with only one Mask Line Segment open

Available Actions:
 - Up Arrow Key = Dilate line string (make thicker)
 - Down Arrow Key = Erode line string (make thinner)
 - Right Arrow Key = Advance to next line string
    - Note: if on the final line string, pressing right will show a final view of all the line strings at once
 - Left Arrow Key = Step back to previous line string to edit

 - W Key = Nudge linestring North
    - Note: Result of nudging varies on the angle of the linestring.
      - For North/South East/West types of roads it shifts the mask in the desired direction.
      - For diagonal/angled lines it typically thickens the mask in the direction pressed.  
 - D Key = Nudge linestring East
 - S Key = Nudge linestring South
 - A Key = Nudge linestring West

 - Spacebar = Revert current linestring back to original state
 - Tab = Revert EVERY linestring back to original state and start back on the first of the line strings to edit
 - Backspace = Move image to Bad Folder and start process with next image
 - Enter key = Stitch line strings together into one mask and save result to the New Mask folder (and moves image to Modified folder)
    - Note: Only works on final view screen
 - Esc Key = Quit out of the script
