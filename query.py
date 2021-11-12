import json
import codecs
with open('InvertedIndex3.json', encoding="utf-8") as json_file:
    data = json.loads(json_file.read())

dict = {}
while 1:

    query = input()
    if query == "exit":
        break
    dict[query] = data[query]
    print(dict)

with codecs.open("query.json", 'w', encoding="utf-8") as tmpFp:
    json.dump(dict, tmpFp, sort_keys=True, ensure_ascii=False)
