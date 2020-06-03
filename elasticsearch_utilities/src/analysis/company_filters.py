from elasticsearch import Elasticsearch
import requests
import json
from ..constants import *
from .queries import *
import re

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
    return {i+1 : h['_source']['all_entities'] for i,h in enumerate(res['hits']['hits'])}

def get_index_top_entities(es, query, size = -1):
    res = es.search(index=INDEX_NAME, body=query, size=200)
    return {i+1 : h['_source']['top_entities'] for i,h in enumerate(res['hits']['hits'])}

def get_pdf_texts(es, query, size = -1):
    res = es.search(index=INDEX_NAME, body=query, size=200)
    return {i+1 : h['_source']['pdf_text'] for i,h in enumerate(res['hits']['hits'])}

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

def get_consulting_companies(es, query):
    res = es.search(index=INDEX_NAME, body=query, size=200)
    ret = {}
    consulting_regex = "(KPMG|deloitte|pwc|kpmg|EY|Deloitte|PwC)"
    rev = "assurance|indipendent|revision|third.+party|support|process|consult"
    for h in res['hits']['hits']:
        cc = []
        text = h['_source']['pdf_text']
        ll = [(m.start(0), m.end(0)) for m in re.finditer(rev, text)]
        if ll:
            for l in ll:
                text_s = text[l[0]-100:l[1]+100]
                kk = [(m.start(0), m.end(0)) for m in re.finditer(consulting_regex, text_s)]
                if kk:
                    for k in kk:
                        cc.append(text_s[k[0]:k[1]])
        if cc:
            ret[h['_id']] = list(set(cc))
            ret[h['_id']].append(h['_source']['url'])
    return ret

def get_punctual_data(es, query):
    res = es.search(index=INDEX_NAME, body=query, size=200)
    ret = {}
    nums = "[0-9]+"
    rev = "(water|acqua).*[0-9]+"
    for h in res['hits']['hits']:
        if "cabot" in h['_source']['url']:
            cc = []        
            text = h['_source']['pdf_text'].casefold()
            ll = [(m.start(0), m.end(0)) for m in re.finditer(rev, text)]
            if ll:
                for l in ll:
                    text_s = text[l[0]:l[1]+20]
                    print(text_s)
                    # kk = [(m.start(0), m.end(0)) for m in re.finditer(nums, text_s)]
                    # if kk:
                    #     for k in kk:
                    #         cc.append(text_s[k[0]:k[1]])
            if cc:
                ret[h['_id']] = cc

    return ret

def get_median_pdf_length(es):
    dd = get_pdf_texts(es, match_all_query)
    ll = [len([w for w in v.split(" ") if w]) for k, v in dd.items()]
    ll.sort()
    return ll
    return ll[len(ll)//2]