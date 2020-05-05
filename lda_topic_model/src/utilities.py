def print_vocab(dd):
    print("Total words in vocabulary : %d \n\nWords:\n" %len(dd))
    for i, k in enumerate(dd):
        if i < 10:
            print("'%s' : %s" %(k,dd[k]))
        else: 
            print("...") 
            break

def filter_frequency(s, fd, n, m):

    fr = {}
    for w in s.split(" "):
        if w in fr:
            fr[w] += 1
        else:
            fr[w] = 1

    ret = ""
    for w in s.split(" "):
        f1 = fd.get(w)
        f2 = fr.get(w)

        if f1 and f2:
            if f1 >= n and f2 >= m:
                ret += "%s " %w

    return ret[:-1]
