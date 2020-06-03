from PyPDF2 import PdfFileReader
import os
from .constants import *

def get_median_pages_count():
    ll = []
    for pdf_dir in ["{}{}".format(PDF_DIRECTORY, k) for k in sorted(os.listdir(PDF_DIRECTORY))]:
        for pdf_file in ["{}/{}".format(pdf_dir, k) for k in sorted(os.listdir(pdf_dir))]:
            try:
                reader = PdfFileReader(open(pdf_file, 'rb'))
                ll.append(reader.getNumPages()) 
            except Exception as e:
                pass
    print(sorted(ll))
    return 0