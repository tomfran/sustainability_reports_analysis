def print_vocab(dd):
    print("Total words in vocabulary : %d \n\nWords:\n" %len(dd))
    for i, k in enumerate(dd):
        if i < 10:
            print("'%s' : %s" %(k,dd[k]))
        else: 
            print("...") 
            break

def filter_frequency(s, fd, n):

    ret = ""
    for w in s.split(" "):
        if fd[w] >= n:
            ret += "%s " %w
            
    return ret[:-1]