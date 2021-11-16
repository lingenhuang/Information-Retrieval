import json
import codecs
import jieba
from iteration_utilities import duplicates
import collections
from os import error
with open('InvertedIndex.json', encoding="utf-8") as json_file:
    data = json.loads(json_file.read())

jieba.case_sensitive = True
jieba.set_dictionary('./dict.txt.big.txt')
jieba.load_userdict('./title.txt')
ans = []
input = ["Volkswagen", "凡爾賽宮", "洛杉磯市", "東京迪士尼樂園", "史丹福橋球場"]
# print(type(data))
for q in input:
    merge = []
    if q not in data:  # for the query that can not be found
        seg_list = jieba.lcut(q)
        for item in seg_list:
            print(seg_list)
            merge += data[item]
        dual = [item for item, count in collections.Counter(
            merge).items() if count == len(seg_list)]  # 找重複的
        dual.sort()  # 排序
        A = [str(x) for x in dual]
        ans.append(A)
    else:
        A = [str(x) for x in data[q]]
        ans.append(A)

print(ans)

# while 1:

#     query = input()
#     if query == "exit":
#         break
#     dict[query] = data[query]
#     print(dict)

with codecs.open("query.json", 'w', encoding="utf-8") as tmpFp:
    json.dump(ans, tmpFp, sort_keys=True, ensure_ascii=False)
