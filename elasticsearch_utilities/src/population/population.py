"""
Elastic search population
"""
import os
import requests
import json
import sys
from elasticsearch import Elasticsearch
from ..constants import *
from .atoka_requests import get_company
from .dandelion_requests import get_entities
from .utilities import update_stats

def populate(atoka_token, dandelion_token, score_dict, verbose = False):
    """
    Connect to the elasticsearch instance running at HOSTNAME and PORT_NUMBER 
    defined in constants, and populate an index called INDEX_NAME with the
    content of pdf files in /data/.

    Entities are found using get_entities()

    """
    es=Elasticsearch([{'host':HOSTNAME,'port':PORT_NUMBER}])    
    
    counter = 1

    stats = {}
    # for each directory (named with url)
    for company in sorted(os.listdir(PDFS_PATH)):
        # for each converted pdf in directory
        for converted_pdf in sorted(os.listdir("%s/%s" %(PDFS_PATH, company))):
            if verbose:
                print("\n\033[1m%d. %s\033[0m" % (counter, converted_pdf), end = "\n\n")

            key = "%s_%s" %(company, converted_pdf.replace(".txt", ".pdf"))
            pdf_info = score_dict.get(key)
                    
            if pdf_info:
                d = pdf_info
                if verbose:
                    print("Getting company")
                ci = get_company(company, atoka_token)
                if ci:
                    d.update(ci)
                elif verbose:
                    print("Error getting commpany")
                # if a company is matched
                file_path = "%s/%s/%s" %(PDFS_PATH, company, converted_pdf)
                with open(file_path) as f:        
                    if verbose:
                        print("Getting entities")

                    d['pdf_text'] = f.read()
                    ent = get_entities(d["pdf_text"], dandelion_token, verbose)
                    if ent:
                        #if entities found
                        d.update(ent)

                        print("Sending")
                        res = es.index(INDEX_NAME, d, doc_type='sustainability_report', id = counter)
                        print("DONE")
                        
                        if verbose:
                            print("Success")
                        counter += 1
                        # updating stats count
                        stats = update_stats(stats, d) 
                    else:
                        if verbose:
                            print("Error getting entities")
            else:
                if verbose:
                    print("Could not get url and score")
    stats['total'] = counter-1
    return stats
        

