"""
Dandelion API request to get entities in text
"""

import requests
import json
import sys
from ..constants import *

def get_entities(text, token):
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
        "top_entities" : 10
    }

    try:
        r = requests.post(url = DANDELION_URL, data = req_body)
        jd = json.loads(r.text)
    except Exception:
        return {}
    
    ret = {}
    
    if "error" not in jd:
        te = set()
        e = set()
        for a in jd["topEntities"]:
            te.add(a["id"])    

        te_list = []
        for a in jd["annotations"]:
            e.add(a["title"])
            if a["id"] in te:
                te.remove(a["id"])
                te_list.append(a["title"])

        ret["top_entities"] = te_list
        ret["all_entities"] = list(e)
    
    else:
        print("Can't find entities", file=sys.stderr)
    
    return ret