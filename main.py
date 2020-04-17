from csv_links_processing import find_reports
from downloader import download
from pdf_ocr import convert
from elasticsearch_population import elastic_population
import json
from utilities import get_score_dictionary
from constants import *

def main():
	# search for sustainability links in csv_links_processing
	website_links, stats = find_reports(CSV_SOURCE_PATH, verbose=True)
	
	# get a dictionary with: website_filename : {score : _ , url: _ }
	# it makes population way easier
	score_dict = get_score_dictionary(website_links)
	
	# download the useful pdf files found
	# download(website_links, "../.misc")

	# ocr the documents to get the texts
	# convert(True)

	# populate elasticsearch index with converted pdfs 
	stats = elastic_population(TOKENS_PATH, score_dict, verbose=True)
	
	with open("elasticsearch_population/stats.txt", 'w') as s:
		s.write(json.dumps(stats, indent = 2))

if __name__ == "__main__":
    main()
