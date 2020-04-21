def output_csv(path, dd, headings):
    with open(path, "w") as f:
        s = ""
        for h in headings: 
             s += "%s," %(h)
        s = s[:-1] + '\n'
        f.write(s)
        for k, v in dd.items():
            f.write("%s, %d\n" %(k, v))

def set_key(dd, k, v):
    if isinstance(dd,dict):
        if k in dd :
            dd[k] = v
        else:
            for d, dv in dd.items():
                dv = set_key(dv, k, v)
    return dd