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
                 "slowed",
                 "reverb",
                 "+",
                 "%",
                 ")",  ")", "()", "-", "(", ")", "//", "ft.", "(Explicit)"]
    query = title.lower()
    result = re.sub("\[(.*?)\]|\((.*?)\)|ft(.*)", repl="",
                    string=query)
    for word in STOPWORDS:
        result = result.replace(word, "")
    result = re.sub(" +", " ", result)
    result = result.split(" ")
    if(result[-1].isnumeric()):
        result.pop()
    result = " ".join(map(str, result))
    return result


