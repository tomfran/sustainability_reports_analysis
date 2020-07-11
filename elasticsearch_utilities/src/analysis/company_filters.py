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
            rr[h['_id']] = h['_source']['revenue']
    return rr

def get_all_employees(es,query):
    res = es.search(index=INDEX_NAME, body=query, size=200)

    rr = {}
    for h in res['hits']['hits']:
        if h['_source'].get('employees'):
            rr[h['_id']] = h['_source']['employees']
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


def get_locations_distribution(atoka_token, es, query):
    res = es.search(index=INDEX_NAME, body=query, size=200)
    rr = {}
    dist = {k : 0 for k,v in REGION_DICT.items()}
    for h in res['hits']['hits']:
        if h['_source'].get('full_address'):
            fa = h['_source']['full_address'] 
            loc = fa[fa.find("(")::].replace("(", "").replace(")", "")
            if loc in PROVINCE_DICT:
                reg = PROVINCE_DICT[loc]
                if reg in dist:
                    dist[reg] += 1
                else:
                    dist[reg] = 1
    return dist


def get_locations_distribution_normalized(atoka_token, es, query):
    dist = get_locations_distribution(atoka_token, es, query)

    for k, v in REGION_DICT.items():
        req_body = {
            "token" : atoka_token,
            "regions" : v,    
            "packages" : "base"
        }
        r = requests.post(url = ATOKA_URL, data = req_body)
        jd = json.loads(r.text)
        tot = jd["meta"]["count"]
        if tot>0:
            dist[k] /= jd["meta"]["count"]

    return dist

def get_company_age(atoka_token, es, query):
    res = es.search(index=INDEX_NAME, body=query, size=200)
    tt = [ h['_source']["atoka_id"] for h in res['hits']['hits'] if h['_source'].get('atoka_id') ]
    ll = ['1940-07-19', '1989-09-22', '1992-04-15', None, '2013-11-13', '1997-03-28', '1951-07-30', '1995-06-09', None, '2000-01-29', '2000-01-29', '1995-05-12', None, None, None, '1988-06-03', None, '2000-06-08', '2000-06-08', None, None, '1973-07-18', '1994-04-19', '1994-04-19', '1946-08-23', '2013-10-18', '2000-09-12', '1961-01-10', '1961-01-10', '1979-12-12', '2003-06-27', '1980-10-07', '1984-10-18', None, None, '1997-11-06', '2011-12-05', '2005-06-16', '1981-09-29', '1991-03-11', '1960-08-05', '2012-08-24', None, None, None, None, '1998-02-03', '1961-08-26', '1961-08-26', '1961-08-26', '1993-09-28', '1994-02-26', None, None, '1938-02-01', None, None, '1995-08-17', '1988-07-04', '1977-01-27', '1977-07-28', '1995-07-19', '2002-02-05', '1955-03-28', '2003-05-31', None, '2015-10-20', '2015-10-20', '2004-07-26', '2004-07-26', '2004-07-26', None, None, '1946-03-27', None, '1992-04-15', '1995-07-19', '2012-06-08', '1990-04-11', None, None, None, None, '1989-05-05', '1982-10-29', '1982-10-29', '1999-12-14', '1999-12-14', '1999-12-14', None, '2013-11-13', '2013-11-13', '1990-11-19', '1995-03-17', '1994-03-25', '2014-11-27', '1997-09-22', '2020-02-25', '1972-02-03', '1961-09-15', '2006-10-05', '1988-10-20', None, '1998-03-30', '1998-03-30', '1962-06-27', '1962-06-27', '1962-06-27', '1962-06-27', '2017-05-22', '1998-02-24', '2002-05-03', '1998-08-10', '1998-08-10', '2008-12-15', '2015-08-05', '1985-09-23', None, '2016-11-29', '1999-12-17', '1999-12-17', '1984-10-18', '1984-10-18', '2000-12-29', '1960-08-05', None, '2009-08-04', '1988-12-31', '1961-01-25', None, '2007-11-23', '1982-05-26', '2006-06-06', '2006-06-06', '2004-07-01', '1990-06-20']
    i = 1
    ss = []
    ll = []
    for t in tt:
        print(i)
        req_body = {
            "token" : atoka_token,
        }
        r = requests.get(url = "%s/%s" %(ATOKA_URL, t), params = req_body)
        jd = json.loads(r.text)
        # print(jd)
        if jd.get('item'):
            f = jd['item'].get('base').get('founded')
            st = jd['item'].get('base').get('startup')
            print(f, st)
            ll.append(f)
            ss.append(st)
        i+=1
    print(ll)
    print(sorted([int(l.split("-")[0]) for l in ll if l]))
    print(ss)
