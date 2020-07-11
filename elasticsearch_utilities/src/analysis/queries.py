match_all_query = {
    "query" : {
        "match_all" : {}
    }
}

match_ateco_query = {
    "query" : {
        "bool": {
            "must" : {
                "match" : {
                    "ateco" : ""
                }
            }
        }\
    }
}

match_consulting_query = {
    "query": {
        "bool" : {
            "must" : {
                "match" : {
                    "pdf_text" : {
                        "value" : "", 
                        "fuzziness" : 2
                    }
                }
            }
        }
    }
}


revenue_range_query = {
    "query" : {
        "bool": {
            "must" : {
                "range" : {
                    "revenue" : {
                        "lte" : 0,
                        "gte" : 0,
                    }
                }
            }
        }
    }
}