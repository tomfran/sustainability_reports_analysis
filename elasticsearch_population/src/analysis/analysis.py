from elasticsearch import Elasticsearch
import requests
import json
from src.constants import *

def test():
    es=Elasticsearch([{'host':HOSTNAME,'port':PORT_NUMBER}])
    
    query = {
        'query':{
            'bool':{
                'must':[{
                    'match':{
                        "top_entities": "Sustainability"
                    }
                }],
                'filter':[{
                    'match':{
                        "top_entities": "Customer"
                    }
                }]
            }
        }
    }

    res = es.search(index=INDEX_NAME, body=query)
    # print("RESPONSE: %s\n" %json.dumps(res, indent=2))
    

    print("TOTAL:\n%s\n" %json.dumps(res['hits']['total'], indent=2))
    print("MAX SCORE: %s\n" %json.dumps(res['hits']['max_score'], indent=2))
    for hit in res['hits']['hits']:
        print("%f : %s " %(hit['_score'],hit['_source']["name"]))

if __name__ == "__main__":
    test()