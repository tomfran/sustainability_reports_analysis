from .src import populate

def elastic_population():

    f = open("tokens.txt", "r")
    s = f.read()
    atoka, dandelion = eval(s)
    stats = populate(atoka, dandelion)
    print (stats)
    # test()

if __name__ == "__main__":
    elastic_population()
