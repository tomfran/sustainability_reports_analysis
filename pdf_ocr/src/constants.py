"""
Contants variables used in the project
"""
# pdf files location
PDF_DIRECTORY   = "data/pdf/"
# images and paragraphs save location
IMAGES_PATH     = "data/images/"
# text save location
TEXTS_PATH      = "data/converted/"
# dilate iterations     (ADAPT FOR EVERY RESOLUTION ???)
IMAGE_PROC_ITERATIONS   = 7
# saved images DPI setting
IMAGE_DPI               = 175
# paragraphs separator in the output file
PARAGRAPH_SEPARATOR     = "\n\n"
# create directory error
DIRECTORY_ERROR         = "\rCan not create directory to store data.\033[K"
#rectangle size used in getstructuringelements (higher first value to merge words but not lines)
MORPH_RECT_SIZE         = (7,5)
# max thread spawned in image processing
MAX_THREAD_NUMBER_IMAGE = 20
# max thread spawned in text processing
MAX_THREAD_NUMBER_TEXT  = 5
# max threads in pdf conversion
MAX_THREAD_NUMBER_PDF = 15
