def get_tokens(path):
    f = open(path, "r")
    s = f.read()
    atoka, dandelion = eval(s)
    return {"atoka":atoka, "dandelion":dandelion}