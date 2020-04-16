import wget
import os
import csv
import requests 

def download(links_path, path, limit = -2):
    """
    Download pdf files from a list of links.
    The list is obtained from the csv_links_processing 
    package

    Files are stored in a path like:
        path/company/pdfs
    
    Arguments:
        links_path {string} -- Path to link list
        path {string} -- Path to download directory
        limit {integer} -- limit to the number of companies to consider

    """

    print("\n\033[1mDownloader\033[0m", end = "\n\n") 
    with open(links_path, 'r') as file:
        reader = csv.reader(file)
        i = -1
        tot = 0
        err = 0
        for row in reader:
            if i == limit:
                break
            i+= 1
            if i == 0 or i <= 19: 
                continue
            print("\n\nWebsite number: %d" %i)
            try:
                os.makedirs("%s/%s" %(path, row[0]))
            except Exception:
                pass
            ll = eval(row[1])
            for l in ll:
                filename = l['url'].split('/')[-1]
                save_path = "%s/%s/%s" %(path, row[0], filename)
                try:
                    s = wget.download(l['url'], save_path)
                    print(s)
                    tot += 1
                except Exception:
                    err += 1

    clean_folder(path)
    print("\n%6d pdf downloaded\n%6d total pdfs\n" %(tot, tot+err))

def clean_folder(path):
    """
    Remove all empty directories in download folder.
    They could have been created by an error while downloading
    
    Arguments:
        path {string} -- path to the folder to clean
    """
    dir_list = ["%s/%s" %(path, d) for d in os.listdir(path)]
    for d in dir_list:
        # rmdir remove only empty directories 
        try:
            os.rmdir(d)
        except Exception:
            pass

if __name__ == "__main__":
    download()