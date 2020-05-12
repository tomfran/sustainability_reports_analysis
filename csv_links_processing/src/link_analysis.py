
import sys
from .constants import *
import re
from sklearn import tree

def evaluate(link):
    """
    Check if a link is a probable sustainability pdf or not. 
    
    Arguments:
        link dict with pdfUrl, sourcePageUrl, anchor and cssSelector fields
    
    Returns:
        True if the link can be a sustainability pdfs, False otherwise
    """
    score = 0
    # remove http://, and then domain
    filename = link['pdfUrl'].split("/")[-1].casefold()

    url = link['pdfUrl'][link['pdfUrl'].find("://")+3:]
    url = url[url.find("/")+1:-len(filename)]
    anchor = link['anchor'].casefold()

    if "sostenibilit" in filename or \
       "sostenibilit" in anchor or \
       "sustainability" in filename or \
       "sustainability" in anchor: 
        score += 40

    if "ambient" in filename or \
       "ambient" in anchor or \
       "environment" in filename or \
       "environment" in anchor:
        score += 20
    
    if "bilancio" in filename or \
       "bilancio" in anchor or \
       "balance" in filename or \
       "balance" in anchor:
        score += 20

    if "rapporto" in filename or \
       "rapporto" in anchor or \
       "report" in filename or \
       "report" in anchor:
        score += 20

    if "sostenibilit" in url or \
       "sustainability" in url: 
        score += 10

    if "ambient" in url or \
       "environment" in url: 
        score += 10

    year = int("2018" in filename) + int("2018" in url) + int("2018" in anchor)
    
    # delete not 18 cases checking filename
    if re.match(r'(.*)20[0-2]([0-7]|[9])(.*)', filename) and not re.match(r'(.*)18(.*)', filename):
        score = 0

    return score >= EVALUATION_THRESHOLD and year > 0, score, year
    # return score >= EVALUATION_THRESHOLD and "2018" in filename, score, year
    # return score >= EVALUATION_THRESHOLD and ("2018" in anchor), score, year
    # return score >= EVALUATION_THRESHOLD and ("2018" in filename or "2018" in anchor), score, year
    # return score >= EVALUATION_THRESHOLD , score, 0

def evaluate_classifier(link, model):
    filename = link['pdfUrl'].split("/")[-1].casefold()
    url = link['pdfUrl'][link['pdfUrl'].find("://")+3:]
    url = url[url.find("/")+1:-len(filename)]
    anchor = link['anchor'].casefold()

    features = get_features(filename, anchor, url)
    # probability of each class
    pred = model.predict_proba([features])[0]
    # 0 = negative
    cond = pred[1] > pred[0]
    score = max(pred)
    return cond, score

def get_depth(l):
    """
    Get the depth of a page from a url

    Arguments:
        l {link dict}

    Returns:
        Number of levels
    """
    s = l["sourcePageUrl"]
    #"remove https://"
    ss = s[s.find("://")+3:]
    #remove last / if present
    if ss[-1] == "/":
        ss = ss[:-1]
    # count levels
    d = ss.count("/") +1
    k = d
    # remove unnecessary levels (eg: /home /en /it)
    for i in range(d):
        if ss[:ss.find("/")] in NOT_COUNT_SET:
            k -= 1
        ss = ss[ss.find("/")+1:]
    return k

def get_features(filename, anchor, url):
    """
    Generate features vector to later tree classification

    Arguments:
        filename string -- filename of the pdf to analyze
        anchor string -- anchor fo the pdf file
        url string -- url of the pdf file

    Returns:
        List of features found on the link
    """
    kk = [
        ("sostenibilit","sustainability"), 
        ("ambient","environment"),
        ("bilancio","balance"),
        ("rapporto","report"),
        # ("qualit", "qualit"),
        # ("impact", "impatto"),
        # ("global", "global"),
        ("2018", "18")
    ]

    ff = [filename, anchor, url]
    
    ret = []
    for k in kk:
        for f in ff:
            ret.append(int(k[0] in f or k[1] in f))

    return ret