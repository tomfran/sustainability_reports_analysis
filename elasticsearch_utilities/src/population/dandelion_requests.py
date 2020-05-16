"""
Dandelion API request to get entities in text
"""

import requests
import json
import sys
from ..constants import *

def get_entities(text, token, verbose = False):
    """
    Get entities and top entities in a text using 
    Dandelion API
    
    Arguments:
        text : text to analyse
        token : Dandelion token
    
    Returns:
        Dictionary containing the list of all entities and 
        the top entities if no API errors occurs, an empty one
        otherwise
    """

    req_body = {
        "token" : token,
        "text" : text,
        "top_entities" : TOP_ENTITIES_NUMBER,
        "include" : ['types']
    }

    try:
        r = requests.post(url = DANDELION_URL, data = req_body)
        jd = json.loads(r.text)
    except Exception:
        return {}
    
    ret = {}
    
    # print(json.dumps(jd, indent=2))

    if "error" not in jd:

        occ = {}
        for a in jd["topEntities"]:
            i = a["id"]
            if i in occ:
                occ[i] += 1
            else:
                occ[i] = 1

        te_list = []
        e_list = []

        for a in jd["annotations"]:
            skip = False
            for t in a['types']:
                tc = t.casefold()
                #remove places and locations from entities and top entities
                if 'place' in tc and \
                'location' in tc:
                    skip = True
                    break

            if not skip:
                e_list.append(a["title"])
                i = a["id"]
                if occ.get(i):
                    te_list.append(a["title"])
                    occ[i] -= 1
                    if occ[i] == 0:
                        occ.pop(i)        

        ret["top_entities"] = te_list
        ret["all_entities"] = e_list
    else:
        if verbose:
            print("Can't find entities", file=sys.stderr)
    
    return ret