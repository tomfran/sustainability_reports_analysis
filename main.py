from csv_links_processing import find_reports, find_reports_classifier, save_stats, get_stats
from downloader import download
from pdf_ocr import convert
from elasticsearch_utilities import elastic_population, analyze
from utilities import get_score_dictionary
from utilities.constants import *
from links_classifiers import generate_tree, generate_forest, generate_svm
import json
import sys

def links():
	#find reports using notebook function
	# website_links, stats = find_reports(CSV_SOURCE_PATH, verbose=True)
	# save_stats(CSV_EVALUATION_PATH, stats)
	
	name = "c_8_0_rbf"

	s = generate_svm(load_name=name)
	website_links, stats = find_reports_classifier(CSV_SOURCE_PATH, s, verbose=True)
	print(get_stats(stats))
	# save_stats(CSV_EVALUATION_PATH_SVM + "{}.csv".format(name), stats_2)

	score_dict = get_score_dictionary(website_links)	
	return website_links, score_dict

def dwl(website_links):
	# download the useful pdf files found
	# download(website_links, OCR_PDF_PATH)
	download(website_links, NEW_DOWNLOAD_PATH)

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