from csv_links_processing import find_reports, find_reports_tree, save_stats, get_stats
from downloader import download
from pdf_ocr import convert
from elasticsearch_utilities import elastic_population, analyze
from utilities import get_score_dictionary
from utilities.constants import *
from links_decision_tree import generate_tree
import json
import sys

def links():
	#find reports using notebook function
	if 0:
		website_links, stats = find_reports(CSV_SOURCE_PATH, verbose=True)
		save_stats(CSV_EVALUATION_PATH, stats)

	#find reports using tree and see what happens
	dt = generate_tree()['tree']
	w_links_2, stats_2 = find_reports_tree(CSV_SOURCE_PATH, dt, verbose=True)
	save_stats(CSV_EVALUATION_PATH_TREE, stats_2)

	with open("new_urls.txt", "w") as f:
		for k, v in w_links_2.items():
			for l in v:
				f.write("{}\n{}\n\n".format(l['url'], l['score']))
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
	w_l, s = links()
	# dwl(w_l)
	# ocr()
	# elastic(s)
	# an()

if __name__ == "__main__":
	main()