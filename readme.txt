--------------- DESCRIPTION ---------------

Downloading and sorting images from your phone can be quite a task. Images from different sources, such as from your phone camera, or downloaded from facebook, whatsapp, or any other social media, all tend to have different naming conventions, making it difficult to sort your image files.

This Python program is used to standardise image and video file names by automatically renaming the files according to the date that the image/video was taken. The name format is in YYYY.MM.DD (#N), where #N is the file ID according to the relevant date, starting from 1. 

For example, take two images taken on 27 July 2022, one by your phone camera and the other downloaded from whatsapp. The first image will be named something like '20220727_090835' while the second will have the whatsapp naming convention, like 'IMG-20220727-WA0005'. The program will detect the image date and rename the two files 2022.07.27 (1) and 2022.07.22 (2) respecively, regardless of the different naming conventions.

The program uses three methods to detect the image data. If one fails, it automatically moves on to the next method in the following order:
    1. FUNCTION extract_date_from_name - Extracts image date from image name (assumes that first string of eight successive digits is the image date).
    2. FUNCTION get_image_exif_data - Extracts image date from the file EXIF data.
    3. FUNCTION get_date_modified - If above methods fail, image date is set as the file's 'date modified'.

--------------- HOW TO USE ---------------

1. Place images to be renamed into a single folder.
2. Run file in Python.
3. When prompted, insert the path of the folder where the images are stored into the command prompt. 
4. Check that the renaming process has worked. If not, you may want to check that you have inserted the correct file path in step 3. 

NOTE: This program currently only works on .jpg and .jpeg image files, and on .mp4 video files.