# -*- coding: utf-8 -*-
"""
Code to rename image files in standardised format based on date: YYYY.MM.DD (#N), where #N is photo ID for relevant date (starting from 1).
"""

#-------------------------SETTING UP-------------------------
from PIL import Image
import PIL.ExifTags
from PIL import UnidentifiedImageError
import os
import re
import datetime
from datetime import datetime as dt

#-------------------------DEFINING FUNCTIONS-------------------------
def get_exif_tag_keys(required_tags):
    '''
    The PIL module provides a dictionary containing all possible ExifTags (value) and their keys (digits)
    This function takes a list of required exif tags and extracts their key from the provided dictionary
    Returns list of tuples (tag, key)
    '''
    
    #get dictionary from PIL module     
    exif_tags = PIL.ExifTags.TAGS

    #get keys of required tags
    required_tag_keys = []
    for t in required_tags:
        #get dictionary key given value
        tag_key = (list(exif_tags.keys())[list(exif_tags.values()).index(t)])
        required_tag_keys.append(tag_key)
    
    required_key2tag = list(zip(required_tags, required_tag_keys))
    
    return required_key2tag

def get_image_exif_data(image_path, required_key2tag):
    '''
    Use Pillow to extract image date from its EXIF info
    
    Arguments:
    1.image_path (str) is image file path
    2. required_key2tag is list of (tag, key) pairs for required exif data
    
    Returns:
    Dictionary of image data
    '''
    
    #open image and get its exif data
    image = Image.open(image_path)
    image_exif = image.getexif() 
    
    #extract required image info 
    image_data = {} #to store data
    for t, k in required_key2tag:
        #if image exif contains required key
        if k in image_exif:
            image_data[t] = image_exif[k]
        else:
            image_data[t] = None

    image.close()

    return image_data

def extract_date_from_name(image_path):
    '''
    Function to extract image date from image name
    Assumes that first string of eight successive digits is image date
    
    Returns image date as string
    '''
    
    #use os module to get file name from path
    image_name = os.path.basename(image_path)
    
    #extract digits from name - returns a list of all digit sequences
    numbers = re.findall('[0-9]+', image_name)
    
    if len(numbers) > 0:
        for n in numbers:
            image_date_str = None #this accounts for case when no sequence is 8 digits long
            if len(n) == 8:
                #convert to datetime and then to required string format
                image_date = dt.strptime(n, '%Y%m%d')
                image_date_str = image_date.strftime("%Y.%m.%d")
                break
    else: 
        image_date_str = None
    
    return image_date_str

def get_date_modified(image_path):
    '''
    Function to get date modified of image
    
    Arguments:
    1.image_path (str) is image file path
    
    Returns:
    Image date
    '''
    #use os module to extract date modified
    modified_timestamp = os.path.getmtime(image_path)
    
    if modified_timestamp is not None:
        #convert timestamp to datetime and then to string
        date_modified = datetime.datetime.fromtimestamp(modified_timestamp)
        date_modified_str = date_modified.strftime("%Y.%m.%d")
    else: 
        date_modified_str = None
        
    return date_modified_str

def image_date(image_path, required_key2tag):
    '''
    Extract image date using three procedures defined above (in the following order):
    1. Get image date from image name
    2. Get image date from exif data
    3. Get image date from date modified
    If one fails, move on to next one.
    
    Arguments:
    1.image_path (str) is image file path
    2. required_key2tag is list of (tag, key) pairs for required exif data
    
    Returns:
    Image date as string, used to rename image file
    '''
    #only jpeg files for now
    if image_path.lower().endswith(('.jpg', '.jpeg')):
    
        image_date_str = extract_date_from_name(image_path)
        
        if image_date_str == None:
            
            try:
                image_data = get_image_exif_data(image_path, required_key2tag)
                image_date = image_data['DateTimeOriginal']
                if image_date is not None:
                    #parse datetime and then convert to string using only date info
                    image_date = dt.strptime(image_date,'%Y:%m:%d %H:%M:%S')
                    image_date_str = image_date.strftime("%Y.%m.%d")

                #if no exif date data, extract date from date modified
                else:               
                    image_date_str = get_date_modified(image_path)

            except UnidentifiedImageError: #error in opening image
                print(f'Could not open {image_path}')
    
    #video files - extract from name or date modified (no exif data)
    elif image_path.lower().endswith(('.mp4')):
        
        image_date_str = extract_date_from_name(image_path)

        if image_date_str == None:
            image_date_str = get_date_modified(image_path)

    #if any other file type
    else:
        print(f'{image_path} is not an image/video')
        image_date_str = 'N/A'
        
    return image_date_str


#-------------------------RUNNING-------------------------
if __name__ == "__main__":
    
    path = input('Insert Image Folder Path: ')
    
    #get list of files in folder
    image_list = []
    for root, dirs, files in os.walk(path):
           for f in files: #files is list of file names
               image_list.append(os.path.join(root, f))

    #get required (tag, key) pairs from get_exif_tag_keys() function
    required_tags =['DateTimeOriginal','GPSInfo']
    required_key2tag = get_exif_tag_keys(required_tags)

    #get image date and rename
    new_image_paths = []
    for image_path in image_list:
    
        image_date_str = image_date(image_path, required_key2tag)
        
        old_name = os.path.basename(image_path)
        ext = old_name.split('.', 10)[-1] #split up to 10 times in case period in name
        
        for i in list(range(1,100)):
            new_name = image_date_str + ' (' + str(i) + ').' 
            new_path = image_path.replace(old_name, new_name)
            if new_path in new_image_paths:
                continue
            else:
                new_image_paths.append(new_path)
                new_path_ext = new_path + ext
                os.rename(image_path, new_path_ext)
                break  
           