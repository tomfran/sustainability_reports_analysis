from .src import process, get_stats, listprint

def find_reports(source_path, dest_path, stats_path):
    print("\n\033[1mCSV processing\033[0m", end = "\n\n") 

    rows, stats = process(source_path, True)
    with open(dest_path, "w") as f:
        f.write('"domain","pdf_dump"\n')
        for k, v in rows.items():
            f.write('"%s",%s\n'%(k, listprint(v)))

    with open(stats_path, "w") as f:
        s = get_stats(stats)
        f.write(s)
    
    print("\n%s\n" %(s.replace(",", ": ")))

if __name__ == "__main__":
    find_reports()

