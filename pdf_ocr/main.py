from .src import *
import os
from pyocr import pyocr
from pyocr import builders
# import pyocr
# import pyocr.builders

def convert(verbose = False):
    tools = pyocr.get_available_tools()[0]
    counter = 1
    # f = open("data/logs.txt", "w")
    # convert into image and then text every pdf file in "data/pdf"
    for pdf_dir in sorted(os.listdir(PDF_DIRECTORY)):
        for pdf_file in sorted(os.listdir(PDF_DIRECTORY + "/" + pdf_dir)):
            # status print
            if verbose:
                print("\n\033[1m%d. %s\033[0m" % (counter, pdf_file), end = "\n\n") 
            try:
                get_images(pdf_file, pdf_dir, verbose)
                get_paragraphs(pdf_file, tools, verbose)
                get_texts(pdf_file, pdf_dir, tools, verbose)
            except Exception:
                # f.write("ERROR: %s\n" %(pdf_file))
                pass
            counter +=1
            return
    # f.close()

if __name__ == "__main__":
    convert(True)

