from elasticsearch import Elasticsearch
import requests
import json
from ..constants import *
from statistics import mean 

def analyze():
    es=Elasticsearch([{'host':HOSTNAME,'port':PORT_NUMBER}])

    match_all_query = {
        "query" : {
            "match_all" : {}
        }
    }

    print(get_recurrent_entities(es, match_all_query, 20))
   
    print(get_recurrent_top_entities(es, match_all_query, 20))

    print(get_all_ateco(es, match_all_query))

if __name__ == "__main__":
    analyze()

def get_recurrent_entities(es, query, size = -1):

    res = es.search(index=INDEX_NAME, body=query, size=200)

    all_entities_list = [h['_source']['all_entities'] for h in res['hits']['hits']]

    occ = {}
    for ll in all_entities_list:
        for l in ll:
            if l in occ:
                occ[l] += 1
            else:
                occ[l] = 1
    
    occ = {k: v for k, v in sorted(occ.items(), key=lambda item: item[1], reverse = True)[:size]}
    return occ

def get_recurrent_top_entities(es, query, size = -1):
    res = es.search(index=INDEX_NAME, body=query, size=200)

    all_entities_list = [h['_source']['top_entities'] for h in res['hits']['hits']]
    # print("Average number of entities found: %d" %mean([len(l) for l in all_entities_list]))
    
    occ = {}
    for ll in all_entities_list:
        for l in ll:
            if l in occ:
                occ[l] += 1
            else:
                occ[l] = 1
    
    occ = {k: v for k, v in sorted(occ.items(), key=lambda item: item[1], reverse = True)[:size]}
    return occ

def get_all_ateco(es, query):

    res = es.search(index=INDEX_NAME, body=query, size=200)

    ll = []
    for h in res['hits']['hits']:
        if h['_source'].get('ateco'):
            ll.append(h['_source']['ateco'])

    return list(set(ll))