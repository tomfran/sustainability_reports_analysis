def get_score_dictionary(dd):
    score_dict = {}
    for k in dd:
        website, links = k, dd[k]
        for l in links:
            filename = l['url'].split('/')[-1]
            score_dict["%s_%s" %(website,filename)] = l
    
    return score_dict