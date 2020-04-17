from .src import populate

def elastic_population(tokens_path, score_dict, verbose = False):
    f = open(tokens_path, "r")
    s = f.read()
    atoka, dandelion = eval(s)
    return populate(atoka, dandelion, score_dict, verbose)

if __name__ == "__main__":
    elastic_population()
