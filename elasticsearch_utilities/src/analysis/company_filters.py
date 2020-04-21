from elasticsearch import Elasticsearch
import requests
import json
from ..constants import *
from .queries import *

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


def get_index_entities(es, query, size = -1):
    res = es.search(index=INDEX_NAME, body=query, size=200)
    return {i+1 : h['_source']['top_entities'] for i,h in enumerate(res['hits']['hits'])}

def get_all_ateco(es, query):

    res = es.search(index=INDEX_NAME, body=query, size=200)
    aa = {}
    for h in res['hits']['hits']:
        if h['_source'].get('ateco'):
            at = h['_source']['ateco']
            if at in aa:
                aa[at] += 1
            else:
                aa[at] = 1
    
    aa = {k: v for k, v in sorted(aa.items(), key=lambda item: item[1], reverse = True)}
    return aa



def get_all_revenues(es, query):

    res = es.search(index=INDEX_NAME, body=query, size=200)

    rr = {}
    for h in res['hits']['hits']:
        if h['_source'].get('revenue'):
            re = h['_source']['revenue']
            if re in rr:
                rr[re] += 1
            else:
                rr[re] = 1
    
    rr = {k: v for k, v in sorted(rr.items(), key=lambda item: item[0], reverse = True)}
    return rr