from csv_links_processing import find_reports
from downloader import download
from pdf_ocr import convert
from elasticsearch_population import elastic_population
from constants import *

def main():
    # search for sustainability links in csv_links_processing
    find_reports(CSV_SOURCE_PATH, CSV_DEST_PATH, CSV_STATS_PATH)
    # download the useful pdf files found
    download(CSV_DEST_PATH, OCR_PDF_PATH, limit=3)
    # ocr the documents to get the texts
    convert(True)



if __name__ == "__main__":
    main()