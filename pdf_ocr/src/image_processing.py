"""
Contains image processing utilities functions.
"""

from .constants import *
import cv2
from PIL import Image
import os
from pyocr import PyocrException
import threading

# Identify and save paragraphs in the image. 
# Paragraphs are saved after a threshold operation to reduce noise
# Includes orientation detection and auto rotation
# Saved in data/images/[pdf_name]/[page_num]/paragraph_num.jpeg
def get_paragraphs(pdf_file, tools, verbose = False):
    """
    Find all the paragraphs in a pdf file.

    Every page is managed by a different thread.
    The maximum number of threads spawned can be found in constants.

    Args :
        pdf_file : name of the pdf file needed to be processed.
        tools    : pyocr available tools
        verbose  : boolean value to display or not status messages.
    
    Returns :
        None. The paragraphs are stored in the path below:
        " IMAGES/PATH/[pdf_name]/[page_num]/ "
        
        The images path is defined in the constants file.
    """
    name_no_ext = pdf_file.rstrip('.pdf')
    page_list = sorted(os.listdir(IMAGES_PATH + name_no_ext))
    threads = []
    for page in page_list:
        # status print
        if verbose:
            print("\r[ ]\tDetecting paragraphs from page %s" %(page[page.find('_') + 1 : len(page)]), end = '', flush=True)
        thread = threading.Thread(target = get_paragraph, args=(page, name_no_ext, tools))
        thread.start()
        threads.append(thread)

        if len(threads) == MAX_THREAD_NUMBER_IMAGE:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    # status print
    if verbose: 
        print("\r[\033[1m\033[92m✓\033[0m]\tParagraphs detected from all pages\033[K")

def get_paragraph(page, pdf_name, tools):
    """
    Sub function that finds paragraphs in a page, used by each thread spawned by "get_paragraphs".

    Args :
        page     : page to be converted
        pdf_name : name of the pdf file to be converted
        tools    : pyocr available tools
    
    Returns :
        None. The paragraphs images are stored in:
        " IMAGES/PATH/[pdf_name]/[page] "
        
        The images path is defined in the constants file.
    """
    page_path = IMAGES_PATH + pdf_name + '/' + page + "/page.jpeg"
    # find contours and process the adaptive threshold image, 
    # later used for saving
    sorted_cnts, thresh_adaptive = find_boxes(page_path)
    image = cv2.imread(page_path)
    counter = 1
    cv2.imwrite("/home/fran/Documents/Documents/normal.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    for c in sorted_cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (31, 91, 20), 3)
        num = ("0" * (len(str(len(sorted_cnts))) - len(str(counter)))) + str(counter)
        savepath = IMAGES_PATH + pdf_name + '/' + page + '/paragraph_' + num + '.jpeg'
        crop_img = thresh_adaptive[y:y+h, x:x+w]
        crop_img = rotate_image(crop_img, tools)
        
        cv2.imwrite(savepath, crop_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        counter += 1
    cv2.imwrite("/home/fran/Documents/Documents/rect.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    os.remove(IMAGES_PATH + pdf_name + '/' + page + "/page.jpeg")

    # savepath = IMAGES_PATH + pdf_name + '/' + page + '/cont_' + num + '.jpeg'
    # cv2.imwrite(savepath, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    

def find_boxes(path):
    """
    Find contours boxes around each paragraph.

    Args :
        path     : path to image
    
    Returns :
        a list of sorted countours in the format (x1, y1, x2, y2) and
        a thresholded image that will be saved as a paragraph 
    """
    # grayscale and blur operations
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image to return, this will be cropped
    thresh_return = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+ cv2.THRESH_OTSU)[1]
    # threshold operation 
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # dilate operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, MORPH_RECT_SIZE)
    dilate = cv2.dilate(thresh, kernel, iterations=IMAGE_PROC_ITERATIONS)
    # finding paragraphs 
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # saving paragraphs for later text extraction
    # sorting contours based on up-right bounding rectangle
    cv2.imwrite("/home/fran/Documents/Documents/thresh.jpg", thresh, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    cv2.imwrite("/home/fran/Documents/Documents/dilate.jpg", dilate, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    sorted_cnts = sorted(cnts, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * image.shape[1])
    for c in sorted_cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(dilate, (x, y), (x + w, y + h), (255,0,0), 1)
    cv2.imwrite("/home/fran/Documents/Documents/dilate2.jpg", dilate, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


    return sorted_cnts, thresh_return

# rotate images if an orientation is detected
def rotate_image(image, tools):
    """
    Rotate an image if an orientation is detected.

    Args :
        image     : path to image
        tools     : pyocr available tools
    
    Returns :
        rotated image, if an orientation is found, the original image otherwise.
    """
    # convert image array to pil image, used to detect orientation
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    try:
        orientation = tools.detect_orientation(pil_image)
        if orientation['angle'] != 0:
            # rotating angle
            angle = 360 - orientation['angle']
            (h, w) = image.shape[:2]
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            # new height and width
            newX = h if orientation['angle'] != 180 else w
            newY = w if orientation['angle'] != 180 else h
            # translate image to new height and width center
            (tx,ty) = ((newX-w)/2,(newY-h)/2)
            M[0,2] += tx
            M[1,2] += ty
            return cv2.warpAffine(image, M, (newX, newY))
        # if there's not reason to rotate, return original
        return image
    except PyocrException as exc:
        # if no text detected or no orientation detected, return the original
        return image
