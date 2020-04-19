def update_stats (s, d):
    for k in d.keys():
        if k in s:
            s[k] += 1
        else:
            s[k] = 1
    return s