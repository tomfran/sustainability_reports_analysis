from .src import process, get_stats, listprint

def main():
    print("\n\033[1mCSV processing\033[0m", end = "\n\n") 

    rows, stats = process("data/pdf_links.csv", True)
    with open("data/filtered_pdf_links.csv", "w") as f:
        f.write('"domain","pdf_dump"\n')
        
        for k, v in rows.items():
            f.write('"%s",%s\n'%(k, listprint(v)))
    
    with open("data/stats.csv", "w") as f:
        s = get_stats(stats)
        f.write(s)
    
    print("\n%s\n" %(s.replace(",", ": ")))

if __name__ == "__main__":
    main()

