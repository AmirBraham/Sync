import json
import re


def dumpToJson(name, dic):
    f = open(name + ".json", "w")
    json.dump(dic, f)
    f.close()


def titleCleanup(title):
    STOPWORDS = ["audio", "official", "video",
                 "lyrics",
                 "lyric",
                 "()",
                 "[",
                 "]",
                 "Visualizer",

                 ")",  ")", "()", "-", "(", ")", "//", "ft.", "(Explicit)"]
    query = title.lower()
    for word in STOPWORDS:
        query = query.replace(word, "")
    result = re.sub(" +", " ", query)
    return result
