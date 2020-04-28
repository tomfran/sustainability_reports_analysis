from csv_links_processing import find_reports, save_stats, get_stats
from downloader import download
from pdf_ocr import convert
from elasticsearch_utilities import elastic_population, analyze
import json
from utilities import get_score_dictionary
from utilities.constants import *

def links():
	website_links, stats = find_reports(CSV_SOURCE_PATH, verbose=True)

	save_stats(CSV_EVALUATION_PATH, stats)

	# get a dictionary with: website_filename : {score : _ , url: _ }
	# it makes population way easier
	score_dict = get_score_dictionary(website_links)

	return website_links, score_dict

def dwl(website_links):
	# download the useful pdf files found
	download(website_links, OCR_PDF_PATH)

def ocr():
	# ocr the documents to get the texts
	convert(True)

def elastic(score_dict):
	# populate elasticsearch index with converted pdfs 
	stats = elastic_population(TOKENS_PATH, score_dict, verbose=True)
	with open("elasticsearch_utilities/stats/population.csv", 'w') as s:
		s.write(json.dumps(stats, indent = 2))

def an():
	# analyze results elastic
	analyze()

def main():
	# w_l, s = links()
	# dwl(w_l)
	# ocr()
	# elastic(s)
	an()

if __name__ == "__main__":
	main()