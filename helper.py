import json


def dumpToJson(name, dic):
    f = open(name + ".json", "w")
    json.dump(dic, f)
    f.close()
