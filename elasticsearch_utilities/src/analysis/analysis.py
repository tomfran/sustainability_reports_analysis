from elasticsearch import Elasticsearch
import requests
import json
from ..constants import *
from .utilities import *
from .queries import *
from .company_filters import *
from statistics import mean 
import pandas as pd

def get_ateco(es):
    ateco_frequency = get_all_ateco(es, match_all_query)
    # output_csv(POPULATION_CSV_PATH_NEW + "ateco/ateco_frequency.csv", ateco_frequency, ATECO_HD)
    print(json.dumps(ateco_frequency, indent = 2))
    data = pd.read_csv("stats/elastic/ateco_codes.csv")
    ateco_dict = {row['c']: row['d'] for index, row in data.iterrows()}
    filt = {}
    for k, v in ateco_frequency.items():
        key = k.split(".")[0]
        if key in filt:
            filt[key] += v
        else:
            filt[key] = v
    filt = {k : v for k,v in sorted(filt.items(), key= lambda x : x[0])}
    print(json.dumps(filt, indent = 2))
    for k, v in filt.items():
        print(f"{k}, {v}")
    filt = {ateco_dict[k] : v for k, v in sorted(filt.items(), key= lambda x : x[1], reverse = True)}
    print(json.dumps(filt, indent = 2))

def get_revenues(es):
    rr = get_all_revenues(es, match_all_query)
    rl = [v for k, v in sorted(rr.items(), key=lambda x: x[1])]
    print(rl)
    st = 1000000
    c = [(i, i+st) for i in range(0, 3000000000, st)]
    fd = [0] * len(c)
    for r in rl:
        j=0
        for k in c:
            if r <= k[1] and r >= k[0]:
                fd[j] += 1
                break
            j+=1
    
    revlist = []
    for i in range(len(fd)):
        for j in range(fd[i]):
            revlist.append(c[i][0])
    print(revlist)

def get_employees(es):
    rr = get_all_employees(es, match_all_query)
    rl = [v for k, v in sorted(rr.items(), key=lambda x: x[1])]
    
    st = 50
    c = [(i, i+st) for i in range(0, 8200, st)]
    fd = [0] * len(c)
    for r in rl:
        j=0
        for k in c:
            if r <= k[1] and r >= k[0]:
                fd[j] += 1
                break
            j+=1
    
    revlist = []
    for i in range(len(fd)):
        for j in range(fd[i]):
            revlist.append(c[i][0])
    print(revlist)
        # print(f"{c[i][0]},{fd[i]}")

def get_locations(atoka_token, es):
    dd = get_locations_distribution(atoka_token, es, match_all_query)
    output_csv("stats/locations/regions_frequency.csv", dd, ['Regione','Frequenza'])
    dd = get_locations_distribution_normalized(atoka_token, es, match_all_query)
    output_csv("stats/locations/regions_frequency_norm.csv", dd, ['Regione','Frequenza'])

def get_entities_LDA(es):
    ie = get_index_entities(es, match_all_query)
    top_e = get_index_top_entities(es, match_all_query)
    te = translate_entities(ie)
    top_e = translate_entities(top_e)
    path = "%s%s%s.csv" %(POPULATION_CSV_PATH_NEW, "", "input_all_entities_en")
    output_LDA_input(path, te)
    path = "%s%s%s.csv" %(POPULATION_CSV_PATH_NEW, "", "input_top_entities_en")
    output_LDA_input(path, top_e)

def get_consulting(es):
    
    dd = get_consulting_companies(es, match_all_query)
    ff = {}
    for k, v in dd.items():
        for l in v:
            if l in ff:
                ff[l] += 1
            else:
                ff[l] = 1
    output_csv("stats/elastic/revision_companies.csv", dd, ['Società','Frequenza'])
    # print("\n\n")
    # (json.dumps(get_punctual_data(es, match_all_query), indent=2))
    
def get_ages(atoka_token, es):
    get_company_age(atoka_token, es, match_all_query)

def analyze(atoka_token):
    es=Elasticsearch([{'host':HOSTNAME,'port':PORT_NUMBER}])
    # get_ateco(es)
    # get_revenues(es)
    # get_employees(es)
    # get_entities_LDA(es)
    # print("Median pdf length: {}".format(get_median_pdf_length(es)))
    # get_consulting(es)
    # get_locations(atoka_token, es)
    get_ages(atoka_token, es)

if __name__ == "__main__":
    analyze()