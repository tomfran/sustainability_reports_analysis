"""
Atoka API request to get companies info
"""
import json
import requests
import sys
from ..constants import *

def match_company(url, token):
    """
    Match a company given the url of one of its websites, 
    using Atoka API
    
    Arguments:
        url : website url
        token : Atoka token
    
    Returns:
        Dictionary containing the atoka id and name if a company
        is matched, an empty one otherwise.
    """
    
    req_body = {
        "token" : token,
        "websitesDomains" : url
    }
    r = requests.post(url = ATOKA_MATCH_URL, data = req_body)
    jd = json.loads(r.text)
    ret = {}
    
    if jd["meta"]["count"] == 0:
        print("No match for url : %s" %url, file=sys.stderr)
        return ret

    items = jd["items"][0]
    a_id = items.get("id")
    name = items.get("name")
    if a_id and name:
        ret["atoka_id"] = a_id
        ret["name"] = name

    return ret

def get_base_economics(id, token):
    """
    Get base and economics info for a company given the id, 
    using Atoka API

    Arguments:
        id : string representing the Atoka id
        token : string representing Atoka token
    
    Returns:
        Dictionary containing retrieved information
    """

    req_body = {
        "token" : token,
        "ids" : id,
        "packages" : "base,economics"
    }
    r = requests.post(url = ATOKA_URL, data = req_body)
    jd = json.loads(r.text)
    ret = {}

    #if no response
    if jd["meta"]["count"] == 0:
        print("No base and economics for atoka id: %s" %id, file=sys.stderr)
        return ret
    
    items = jd["items"][0]
    base = items.get("base")
    if base:
        # get the address
        addr = base.get("registeredAddress")
        if addr:
            fa = addr.get("fullAddress")
            if fa:
                ret["full_address"] = fa

        # get ateco
        atc = base.get("ateco")
        if atc:
            code = atc[0].get("code")
            if code:
                ret["full_address"] = code
    
    # get revenue
    ecs = items.get("economics")
    if ecs:
        bsheet = ecs.get("balanceSheets")
        if bsheet:
            rev = bsheet[0].get("revenue")
            if rev : 
                ret["revenue"] = rev
        
        # get employees
        empl = ecs.get("employees")
        if empl:
            val = empl[0].get("value")
            if val:
                ret["employees"] = val
    
    return ret
    
def get_company(url, token):
    d = match_company(url, token)
    if d:
        d.update(get_base_economics(d["atoka_id"], token))
    return d