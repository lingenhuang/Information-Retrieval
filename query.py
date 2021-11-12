import json
import codecs
import jieba
from os import error
with open('InvertedIndex5.json', encoding="utf-8") as json_file:
    data = json.loads(json_file.read())

jieba.case_sensitive = True
jieba.set_dictionary('./dict.txt.big.txt')
jieba.load_userdict('./title.txt')
ans = []
input = ["Volkswagen", "凡爾賽宮", "洛杉磯市", "東京迪士尼樂園好玩", "史丹福橋球場"]
# print(type(data))
for q in input:
    merge = []
    if q not in data:  # for the query that can not be found
        seg_list = jieba.lcut(q)
        for item in seg_list:
            merge += data[item]
        merge = list(dict.fromkeys(merge))  # remove duplicate
        merge.sort()
        ans.append(merge)
    else:
        ans.append(data[q])


print(ans)
# while 1:

#     query = input()
#     if query == "exit":
#         break
#     dict[query] = data[query]
#     print(dict)

# with codecs.open("query.json", 'w', encoding="utf-8") as tmpFp:
#     json.dump(dict, tmpFp, sort_keys=True, ensure_ascii=False)
