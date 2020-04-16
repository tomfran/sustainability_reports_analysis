"""
Contains pdf utilities functions.
"""

import os
from .constants import *
from pdf2image import convert_from_path 

# Images are stored in data/images/[pdf_name]
def get_images(pdf_file, pdf_dir, verbose = False):
    """
    Convert a pdf file to images.texts

    Args :
        pdf_file : path to the pdf file needed to be converted.
        verbose  : boolean value to display or not status messages.
    
    Returns :
        None. The images are stored in the path below:
        " IMAGES/PATH/[pdf_name] "
        
        The images path is defined in the constants file.
    """
    # status print
    if verbose:
        print("[ ]\tConverting pdf file into images", end = '', flush=True)
    
    # create directory: name of file without .pdf
    name_no_ext = pdf_file.rstrip('.pdf')
    try:
        os.makedirs(IMAGES_PATH + name_no_ext)
    except OSError:
        print(DIRECTORY_ERROR)
        return

    pdf_path = PDF_DIRECTORY + pdf_dir + "/" + pdf_file
    # actual conversion
    try:
        pages = convert_from_path(pdf_path, dpi = IMAGE_DPI, fmt = 'jpeg', thread_count=MAX_THREAD_NUMBER_PDF)
    except Exception:
        # status print
        if verbose:
            print("\r[\033[1m\033[91m✗\033[0m]\tCould not convert pdf file to images\033[K\n")
        raise Exception

    # save them on disk (colors)
    counter = 1
    for page in pages:
        num = ("0" * (len(str(len(pages))) - len(str(counter)))) + str(counter)
        page_folder = "/page_" + num
        try:
            os.makedirs(IMAGES_PATH + name_no_ext + page_folder)
        except OSError:
            print(DIRECTORY_ERROR)
            return

        savepath = IMAGES_PATH + name_no_ext + page_folder + "/page.jpeg"
        page.save(savepath, 'JPEG')
        counter += 1

    # status print
    if verbose:
        print("\r[\033[1m\033[92m✓\033[0m]\tPdf converted\033[K")
