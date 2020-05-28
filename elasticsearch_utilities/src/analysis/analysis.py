from elasticsearch import Elasticsearch
import requests
import json
from ..constants import *
from .utilities import *
from .queries import *
from .company_filters import *
from statistics import mean 

def get_ateco_entities_revenue(es):
    ma_entities = get_recurrent_entities(es, match_all_query)
    output_csv(POPULATION_CSV_PATH_NEW + "all/all_entities_frequency.csv", ma_entities, ENTITIES_HD)
    
    ma_top_entities = get_recurrent_top_entities(es, match_all_query)
    output_csv(POPULATION_CSV_PATH_NEW + "all/top_entities_frequency.csv", ma_top_entities, ENTITIES_HD)

    ateco_frequency = get_all_ateco(es, match_all_query)
    output_csv(POPULATION_CSV_PATH_NEW + "ateco/ateco_frequency.csv", ateco_frequency, ATECO_HD)

    for a, v in ateco_frequency.items():
        q = set_key(match_ateco_query, "ateco", a)
        ef = get_recurrent_top_entities(es, q)
        path = "%s%s%s.csv" %(POPULATION_CSV_PATH_NEW, "ateco/recurrent_entities/", a)
        output_csv(path, ef, ENTITIES_HD)

    revenue_frequency = get_all_revenues(es, match_all_query)
    path = POPULATION_CSV_PATH_NEW + "revenue/revenues_frequency.csv"
    output_csv(path, revenue_frequency, REVENUE_HD)

    SPL_SIZE = 10
    spl = [k for k,v in revenue_frequency.items()]
    spl = [(spl[x],spl[min(x+SPL_SIZE, len(spl)-1)]) for x in range(0, len(spl), SPL_SIZE)]

    for s in spl:
        q = set_key(revenue_range_query, "lte", s[0])
        q = set_key(revenue_range_query, "gte", s[1])
        ef = get_recurrent_top_entities(es, q)
        path = "%s%s%s.csv" %(POPULATION_CSV_PATH_NEW, "revenue/recurrent_entities/", s)
        output_csv(path, ef, ENTITIES_HD)

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
    # get_ateco_entities_revenue(es)
    get_entities_LDA(es)
    # test(es)
if __name__ == "__main__":
    analyze()