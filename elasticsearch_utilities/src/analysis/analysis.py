from elasticsearch import Elasticsearch
import requests
import json
from ..constants import *
from .utilities import *
from .queries import *
from .company_filters import *
from statistics import mean 
from googletrans import Translator

def analyze():
    es=Elasticsearch([{'host':HOSTNAME,'port':PORT_NUMBER}])

    ma_entities = get_recurrent_entities(es, match_all_query)
    path = POPULATION_CSV_PATH + "all/all_entities_frequency.csv"
    output_csv(path, ma_entities, ENTITIES_HD)
    
    ma_top_entities = get_recurrent_top_entities(es, match_all_query)
    path = POPULATION_CSV_PATH + "all/top_entities_frequency.csv"
    output_csv(path, ma_top_entities, ENTITIES_HD)
    

    ateco_frequency = get_all_ateco(es, match_all_query)
    path = POPULATION_CSV_PATH + "ateco/ateco_frequency.csv"
    output_csv(path, ateco_frequency, ATECO_HD)

    for a, v in ateco_frequency.items():
        q = set_key(match_ateco_query, "ateco", a)
        ef = get_recurrent_top_entities(es, q)
        path = "%s%s%s.csv" %(POPULATION_CSV_PATH, "ateco/recurrent_entities/", a)
        output_csv(path, ef, ENTITIES_HD)

    revenue_frequency = get_all_revenues(es, match_all_query)
    path = POPULATION_CSV_PATH + "revenue/revenues_frequency.csv"
    output_csv(path, revenue_frequency, REVENUE_HD)

    SPL_SIZE = 10
    spl = [k for k,v in revenue_frequency.items()]
    spl = [(spl[x],spl[min(x+SPL_SIZE, len(spl)-1)]) for x in range(0, len(spl), SPL_SIZE)]

    for s in spl:
        q = set_key(revenue_range_query, "lte", s[0])
        q = set_key(revenue_range_query, "gte", s[1])
        ef = get_recurrent_top_entities(es, q)
        path = "%s%s%s.csv" %(POPULATION_CSV_PATH, "revenue/recurrent_entities/", s)
        output_csv(path, ef, ENTITIES_HD)
        


    # ie = get_index_entities(es, match_all_query)

    # translate_urls = ["translate.google.com", "translate.google.co.kr",
    #                     "translate.google.at", "translate.google.de",
    #                     "translate.google.ru", "translate.google.ch",
    #                     "translate.google.fr", "translate.google.es"]
    # t = Translator(service_urls=translate_urls)
    
    # for k, v in ie.items():
    #     ie[k] = '"%s"' %" ".join([translate_to_en(t, w.replace(',', '_')) for w in v])
    # path = "%s%s%s.csv" %(POPULATION_CSV_PATH, "", "input")
    # output_csv(path, ie, ["elastic_index","entities"])

if __name__ == "__main__":
    analyze()