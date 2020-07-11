from urllib.parse import urlparse

def listprint(ll):
    """
    Create a string representing a list in a eval friendly format
    
    Arguments:
        ll input list
    
    Returns:
        String like "[""item"", ...]"
    """
    ret = '"['
    for l in ll:
        ret += '{'
        for k, v in l.items():
            ret += '""%s"":""%s"",'%(k,v)
        ret = ret[:-1]
        ret += '},'
    ret = ret[:-1]
    ret += ']"'
    return ret


def get_stats(s):
    """
    Create a string for the stats given by the csv process function
    
    Arguments:
        s tuple containing (Total websites, websites who published, total links, useful links, average depth)
    
    Returns:
        String in a csv format with the stats and additional percentages
    """
    return "metric,value\nTotal websites,%d\nWebsites who published,%d\n\
Published percentage,%f\nTotal links,%d\n\
Probable sustainability pdfs links,%d\n\
Useful pdfs percentage,%f\nAverage depth,%f\n\
Pdfs in homepage,%d" %(s[0], s[1], (s[1]/s[0])*100, s[2], s[3], (s[3]/s[2])*100, s[4], s[5])

def save_stats(path, s):
    with open(path, 'w') as f:
        f.write(get_stats(s))

def clean_pdf_list(ll):
    #keep only the link and the source (needed to get depth later)
    ret = []
    for l in ll:
        k = {}
        u = urlparse(l[0]['pdfUrl'])
        k['pdfUrl'] = "%s://%s%s" %(u[0], u[1], u[2])
        k['sourcePageUrl'] = l[0]['sourcePageUrl']
        k['score'] = l[1][1]
        ret.append(k)


    # remove #page= and GET arguments
    for r in ret:
        if "#page=" in r['pdfUrl']:
            s = r['pdfUrl']
            r['pdfUrl'] = s[:s.find("#page=")]
            s = r['pdfUrl']
            i = s.find("?") 
            j = s.find(".pdf")
            if i > 0 and j < i:
                r['pdfUrl'] = s[:s.find(".pdf")+4]
    
    #remove duplicates
    s = set()
    for d in ret:
        s.add(d['pdfUrl'])
    no_dup = []
    for r in ret:
        if r['pdfUrl'] in s:
            no_dup.append(r)
            s.remove(r['pdfUrl'])

    return no_dup
