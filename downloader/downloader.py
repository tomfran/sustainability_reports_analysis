import wget
import os
import csv

def download():
    print("Downloading pdf files\n")
    with open('filtered_pdf_links.csv', 'r') as file:
        reader = csv.reader(file)
        i = -1
        tot = 0
        err = 0
        for row in reader:
            if tot == 20:
                break
            i+= 1
            if i == 0: 
                continue
            print("\n\nWebsite number: %d" %i)
            try:
                os.makedirs("pdfs/" + row[0])
            except Exception:
                pass
            ll = eval(row[1])
            for l in ll:
                path = "pdfs/" + row[0] + "/" + l.split('/')[-1]
                try:
                    wget.download(l, path)
                    tot += 1
                except Exception:
                    err += 1

    print("\n\n%6d pdf downloaded\n%6d total pdfs\n\n" %(tot, tot+err))

if __name__ == "__main__":
    download()