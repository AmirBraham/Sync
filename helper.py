import json
import re


def dumpToJson(name, dic):
    f = open(name + ".json", "w")
    json.dump(dic, f)
    f.close()


def titleCleanup(title):
    STOPWORDS = ['(audio)', "(official", "video)",
                 "(Lyric", " Video)",
                 'audio)', '(video)', '-', 'Lyric', "(", ")", "//", "ft.", "(Explicit)"]
    query = title
    querywords = query.split()
    resultwords = [word for word in querywords if word.lower()
                   not in STOPWORDS]
    result = re.sub(' +', ' ', ' '.join(resultwords))
    return result
