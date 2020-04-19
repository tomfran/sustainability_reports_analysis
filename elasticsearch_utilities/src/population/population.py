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
                print("Getting company")
                
            
            
            

            d = get_company(company, atoka_token)
            if d:
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
                        
                        key = "%s_%s" %(company, converted_pdf.replace(".txt", ".pdf"))
                        pdf_info = score_dict.get(key)
                        
                        if pdf_info:
                            d.update(pdf_info)
                        
                        res = es.index(INDEX_NAME, d, doc_type='pdf', id = counter)
                        if verbose:
                            print("Success")
                        counter += 1
                        # updating stats count
                        stats = update_stats(stats, d) 
                    else:
                        if verbose:
                            print("Error")
            else:
                if verbose:
                    print("Error")
                    
    stats['total'] = counter-1
    return stats
        

