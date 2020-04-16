from .src import populate

def elastic_population(tokens_path, score_dict):
    f = open(tokens_path, "r")
    s = f.read()
    atoka, dandelion = eval(s)
    stats = populate(atoka, dandelion, score_dict)
    print (stats)
    # test()

if __name__ == "__main__":
    elastic_population()
