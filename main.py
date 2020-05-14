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
	website_links, stats = find_reports(CSV_SOURCE_PATH, verbose=True)
	save_stats(CSV_EVALUATION_PATH, stats)

	#find reports using tree and see what happens

	# dt = generate_tree(load_name='e_2_10')

	url_set = set()
	for k, v in website_links.items():
		for l in v:
			url_set.add(l['url'])

	print(len(url_set))
	i = 0
	a = 0
	name = "8_0"
	score_occ = []
	print("\n" + name)
	dt = generate_svm(load_name=name)
	w_links_2, stats_2 = find_reports_classifier(CSV_SOURCE_PATH, dt, verbose=True)
	print(get_stats(stats_2))
	save_stats(CSV_EVALUATION_PATH_SVM + "{}.csv".format(name), stats_2)
	with open("svm_links/{}_filtered_0.75_new.txt".format(name), "w") as f:
		for k, v in w_links_2.items():
			for l in v:
				if l['score'] >= 0.75:
					if l['url'] in url_set:
						url_set.remove(l['url'])
						f.write("{}\n{}\n\n".format(l['url'], l['score']))
						a += 1
					i += 1
	print("Total links found above 0.75: {}\nLinks found both by function and svm: {} of {}\nActual new links: {}".format(i, a, len(url_set), i-a))
	# get a dictionary with: website_filename : {score : _ , url: _ }
	# it makes population way easier
	score_dict = get_score_dictionary(website_links)
	
	with open("svm_links/{}_filtered_0.75_NOTFOUND.txt".format(name), "w") as f:
		for a in url_set:
			f.write("{}\n".format(a))
			
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