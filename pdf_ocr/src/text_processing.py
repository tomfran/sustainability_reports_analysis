"""
Contains ocr utilities functions.
Used for text detection.
"""


from PIL import Image
import pyocr
from .constants import *
import os
import shutil
import threading
import re

def get_texts(pdf_file, pdf_dir, tools, verbose = False):
    """
    Convert a pdf file to text.
    The pdf file is organized in a directory with pages, which contains
    cropped images of paragraphs.
    The main directory is in:
    " IMAGES/PATH/[pdf_name] "

    Every page is managed by a different thread.
    The maximum number of threads spawned can be found in constants.

    Args :
        pdf_file : name of the pdf file to be converted
        tools    : pyocr available tools
        verbose  : boolean value to display or not status messages
    
    Returns :
        None. The pages texts are stored in the path below:
        " TEXTS/PATH/[pdf_name] "
        
        The texts path is defined in the constants file.
    """
    # create directory to store the converted text
    name_no_ext = pdf_file.rstrip('.pdf')
    try:
        os.makedirs(TEXTS_PATH + pdf_dir + "/" + name_no_ext)
    except OSError:
        print(DIRECTORY_ERROR)
        return 

    threads = []
    # data/images/[pdf_name]
    for page_dir in sorted(os.listdir(IMAGES_PATH + name_no_ext)):
        # status print
        if verbose:
            print("\r[ ]\tDetecting text from page %s" %(page_dir[page_dir.find('_') + 1 : len(page_dir)]), end = '', flush=True)
        thread = threading.Thread(target = get_text, args=(page_dir, pdf_dir, name_no_ext, tools))
        thread.start()
        threads.append(thread)

        if len(threads) == MAX_THREAD_NUMBER_TEXT:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    merge_pages(TEXTS_PATH + pdf_dir + "/" + name_no_ext)
    shutil.rmtree(IMAGES_PATH + name_no_ext)
    shutil.rmtree(TEXTS_PATH + pdf_dir + "/" + name_no_ext)


    # status print
    if verbose:
        print("\r[\033[1m\033[92m✓\033[0m]\tText detected from all pages\033[K")

def get_text(page_dir, pdf_dir, pdf_name, tools):
    """
    Sub function that convert a page, used by each thread spawned by "get_texts".

    Args :
        page_dir : page to be converted ( identified by a directory of paragraphs )
        pdf_name : name of the pdf file to be converted
        tools    : pyocr available tools
    
    Returns :
        None. The page text is stored in the path below:
        " TEXTS/PATH/[pdf_name]/[page_dir].txt "
        
        The texts path is defined in the constants file.
    """
    
    # foreach paragraph detect and write text on the output file

    output = TEXTS_PATH + pdf_dir + "/" + pdf_name + '/' + page_dir +'.txt'
    f = open(output, "a")
    
    # dir : data/images/[pdf_name]/page_num
    for image_file in sorted(os.listdir(IMAGES_PATH + pdf_name + '/' + page_dir)):
        # paragraph : data/.images/[pdf_name]/page_num/paragraph_num.jpeg
        paragraph_path = IMAGES_PATH + pdf_name + '/' + page_dir + "/" + image_file
        # pyocr
        text = tools.image_to_string(Image.open(paragraph_path), builder=pyocr.builders.TextBuilder())
        text = re.sub(r'(\n *)+', '\n', text)
        if text:
            f.write(text + PARAGRAPH_SEPARATOR)
    f.close()

def merge_pages(pdfdir):
    page_list = sorted(os.listdir(pdfdir))

    out = open(pdfdir + ".txt", 'a')
    for page in page_list:
        f = open(pdfdir + "/" + page)
        for line in f:
            out.write(line)
        f.close()
        os.remove(pdfdir + "/" + page)
    out.close()
