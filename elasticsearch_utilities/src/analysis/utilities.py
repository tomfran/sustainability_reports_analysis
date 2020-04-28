from googletrans import Translator
from .translation_dict import *
import sys
import time
from langdetect import detect

def output_csv(path, dd, headings):
    with open(path, "w") as f:
        s = ""
        for h in headings: 
             s += "%s," %(h)
        s = s[:-1] + '\n'
        f.write(s)
        for k, v in dd.items():
            f.write("%s,%s\n" %(k, v))

def set_key(dd, k, v):
    if isinstance(dd,dict):
        if k in dd :
            dd[k] = v
        else:
            for d, dv in dd.items():
                dv = set_key(dv, k, v)
    return dd

translate_urls = ["translate.google.com", "translate.google.co.kr",
                    "translate.google.at", "translate.google.de",
                    "translate.google.ru", "translate.google.ch",
                    "translate.google.fr", "translate.google.es"]
t = Translator(service_urls=translate_urls)

def translate_to_en(s):
    if s in T_DICT:
        return T_DICT[s]

    ret = s.replace(" ", "_")
    try:
        d = detect(s)
    except Exception as e:
        d = '...'
    
    if d != 'en':
        ret = t.translate(s, dest='en').text.replace(" ", "_")

        T_DICT[s] = ret
        print('"%s" : "%s" ,' %(s,ret))
        print('"%s" : "%s" ,' %(s,ret), file = sys.stderr)
    
    return ret

def translate_entities(ie):
    ret = {}
    for k, v in ie.items():
        ret[k] = [translate_to_en(w.replace(',', '_').replace('"', "'")) for w in v]
    return ret
    
def output_LDA_input(path, te):

    dd = {}
    for k, v in te.items():
        dd[k] = '"%s"' %" ".join(v)

    output_csv(path, dd, ["elastic_index","entities"])


def output_LDA_input_filtered(path, ee, n, m):
    # for k, v in tt:
    #     freq = {}
    #     # TODO frequency table (need to keep duplicates from dandelion)

    freq = {}
    for k, v in ee.items():
        for w in v:
            if w in freq:
                freq[w] += 1
            else:
                freq[w] = 1

    dd = {}
    for k, v in ee.items():
        dd[k] = '"%s"' %" ".join([w for w in v if freq[w] >= m])

    output_csv(path, dd, ["elastic_index","entities"])