from elasticsearch import Elasticsearch
import requests
import json
from ..constants import *
from .utilities import *
from .queries import *
from .company_filters import *
from statistics import mean 
import pandas as pd

def get_ateco_revenue(es):
    ateco_frequency = get_all_ateco(es, match_all_query)
    output_csv(POPULATION_CSV_PATH_NEW + "ateco/ateco_frequency.csv", ateco_frequency, ATECO_HD)
    
    data = pd.read_csv("elasticsearch_utilities/stats/ateco_codes.csv")
    ateco_dict = {row['c']: row['d'] for index, row in data.iterrows()}

    filt = {}
    for k, v in ateco_frequency.items():
        key = k.split(".")[0]
        if key in filt:
            filt[key] += v
        else:
            filt[key] = v
    filt = {ateco_dict[k] : v for k, v in sorted(filt.items(), key= lambda x : x[0])}
    print(json.dumps(filt, indent = 2))
    # revenue_frequency = get_all_revenues(es, match_all_query)
    # path = POPULATION_CSV_PATH_NEW + "revenue/revenues_frequency.csv"
    # output_csv(path, revenue_frequency, REVENUE_HD)

def get_entities_LDA(es):
    ie = get_index_entities(es, match_all_query)
    top_e = get_index_top_entities(es, match_all_query)
    te = translate_entities(ie)
    top_e = translate_entities(top_e)
    path = "%s%s%s.csv" %(POPULATION_CSV_PATH_NEW, "", "input_all_entities_en")
    output_LDA_input(path, te)
    path = "%s%s%s.csv" %(POPULATION_CSV_PATH_NEW, "", "input_top_entities_en")
    output_LDA_input(path, top_e)

def test(es):
    print(json.dumps(get_consulting_companies(es, match_all_query), indent=2))
    # print("\n\n")
    # (json.dumps(get_punctual_data(es, match_all_query), indent=2))
    
def analyze():
    es=Elasticsearch([{'host':HOSTNAME,'port':PORT_NUMBER}])
    get_ateco_revenue(es)
    # get_entities_LDA(es)
    # print("Median pdf length: {}".format(get_median_pdf_length(es)))
    test(es)
if __name__ == "__main__":
    analyze()