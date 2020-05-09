def print_vocab(dd):
    """Print the head of a dictionary

    Arguments:
        dd dict
    """
    print("Total words in vocabulary : %d \n\nWords:\n" %len(dd))
    for i, k in enumerate(dd):
        if i < 10:
            print("'%s' : %s" %(k,dd[k]))
        else: 
            print("...") 
            break

def filter_frequency(s, fd, n, m):
    """Filter words based on their interdocument and intradocument frequency

    Arguments:
        s string -- input words as "word1 word2.."
        fd dict -- interdocument frequency {word: freq}
        n int -- interdocument frequency restriction 
        m int -- intradocument frequency restriction

    Returns:
        String representing filtered words, same format as input 
    """
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

def filter_frequency_relevant(s, fd, n, m):
    """Filter words based on their interdocument frequency and 
       their relevance in a document

    Arguments:
        s string -- input words as "word1 word2.."
        fd dict -- interdocument frequency {word: freq}
        n int -- interdocument frequency restriction 
        m int -- quantity of words to pick from the list (the list is sorted by importance)

    Returns:
        String representing filtered words, same format as input 
    """
    ret = ""
    for w in s.split(" ")[:m]:
        f1 = fd.get(w)
        if f1 >= n:
            ret += "%s " %w
            
    return ret[:-1]
