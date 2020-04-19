from elasticsearch import Elasticsearch
import requests
import json
from ..constants import *
from statistics import mean 

def analyze():
    es=Elasticsearch([{'host':HOSTNAME,'port':PORT_NUMBER}])
    
    # query = {
    #     'query':{
    #         'bool':{
    #             'must':[{
    #                 'match':{
    #                     "top_entities": "Sustainability"
    #                 }
    #             }],
    #             'filter':[{
    #                 'match':{
    #                     "top_entities": "Customer"
    #                 }
    #             }]
    #         }
    #     }
    # }
    query = {
        "query" : {
            "match_all" : {}
        }
    }

    res = es.search(index=INDEX_NAME, body=query, size=200)
    # print("RESPONSE: %s\n" %json.dumps(res, indent=2))


    all_entities_list = [h['_source']['all_entities'] for h in res['hits']['hits']]
    print("Average number of entities found: %d" %mean([len(l) for l in all_entities_list]))
    
    occ = {}
    for ll in all_entities_list:
        for l in ll:
            if l in occ:
                occ[l] += 1
            else:
                occ[l] = 1
    
    occ = {k: v for k, v in sorted(occ.items(), key=lambda item: item[1], reverse = True)}

    i = 0
    for k, v in occ.items():
        i +=1
        print ("%s : %d" %(k,v))
        if i == 10:
            break


if __name__ == "__main__":
    analyze()