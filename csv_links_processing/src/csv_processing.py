"""
Contains csv processing functions.
Used to detect pdf files links.
"""
import csv
from .link_analysis import *
from .utilities import clean_pdf_list
import pandas as pd

def process(csv_file, verbose):
    """
    Find useful links in a pdf pool.
    A link is useful if evaluate return True.
    It also collect stats regarding the pdfs found and the websites who published them.

    Return:
    ret: dict containing 
    {"websitename" : [pdfs links]}
    
    stats: tuple containing 
    (total websites, websites who published, total links, useful links, average pdfs depth in website)
    """

    # dict to return
    ret = {}
    csv.field_size_limit(100000000)
    # set to count websites
    with open(csv_file) as csv_file:    
        csv_reader = csv.reader(csv_file, delimiter=',')
        # used to get stats
        total = useful = depth_sum = homelinks = 0
        counter = -1
        #pdf list in csv
        pdf_dump = []
        for row in csv_reader:
            counter += 1            
            if verbose:
                print("\r[ ]\tProcessing line %d" %(total), end = '', flush=True)
            #skip first line
            if counter == 0 : continue
            pdf_dump = eval(row[1])
            total += len(pdf_dump)
            #get only useful ones

            # [({link}, True, score, "2018" occurrences)]
            pdf_dump = [k for k in [(l,evaluate(l)) for l in pdf_dump] if k[1][0]]
            # pdf_dump = [l for l in [evaluate(p) for p in pdf_dump] if l[0] == True]
            
            # keep only url and source page url, remove duplicates
            pdf_dump = clean_pdf_list(pdf_dump)
            
            #add depth to total
            for l in pdf_dump:
                d = get_depth(l)
                if d == 1:
                    homelinks += 1
                depth_sum += d
            
            useful += len(pdf_dump)
            # {"sitename" = pdf list, ...}
            if pdf_dump:
                ret[row[0]] = [{"url":l['pdfUrl'], "score":l['score']} for l in pdf_dump] 
    
    if verbose:
        print("\r[\033[1m\033[92m✓\033[0m]\tAll lines processed\033[K")
    # total websites, useful websites, total links, useful links, avg depth, homelinks num
    if not useful:
        stats = (counter, len(ret), total, useful, 0, homelinks)
    else:
        stats = (counter, len(ret), total, useful, depth_sum/useful, homelinks)
    return ret, stats

def process_classifier(csv_file, classifier, verbose):
    ret = {}
    csv.field_size_limit(100000000)
    # set to count websites
    with open(csv_file) as csv_file:    
        csv_reader = csv.reader(csv_file, delimiter=',')
        # used to get stats
        total = useful = depth_sum = homelinks = 0
        counter = -1
        #pdf list in csv
        pdf_dump = []
        for row in csv_reader:
            counter += 1            
            if verbose:
                print("\r[ ]\tProcessing line %d" %(total), end = '', flush=True)
            #skip first line
            if counter == 0 : continue
            pdf_dump = eval(row[1])
            total += len(pdf_dump)
            #get only useful ones

            # [({link}, True, score, "2018" occurrences)]
            pdf_dump = [k for k in [(l,evaluate_classifier(l, classifier)) for l in pdf_dump] if k[1][0]]
            # pdf_dump = [l for l in [evaluate(p) for p in pdf_dump] if l[0] == True]
            
            # keep only url and source page url, remove duplicates
            pdf_dump = clean_pdf_list(pdf_dump)
            
            #add depth to total
            for l in pdf_dump:
                d = get_depth(l)
                if d == 1:
                    homelinks += 1
                depth_sum += d
            
            useful += len(pdf_dump)
            # {"sitename" = pdf list, ...}
            if pdf_dump:
                ret[row[0]] = [{"url":l['pdfUrl'], "score":l['score']} for l in pdf_dump] 
    
    if verbose:
        print("\r[\033[1m\033[92m✓\033[0m]\tAll lines processed\033[K")
    # total websites, useful websites, total links, useful links, avg depth, homelinks num
    
    if not useful:
        stats = (counter, len(ret), total, useful, 0, homelinks)
    else:
        stats = (counter, len(ret), total, useful, depth_sum/useful, homelinks)
    return ret, stats