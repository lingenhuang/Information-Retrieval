from ctypes import sizeof
import json
import jieba
import codecs
with open('wiki_2021_10_05_50000.json', encoding="utf-8") as json_file:
    data = json.loads(json_file.read())


# print(s)
# print(data[999]['id'])
# print(data[999]['title'])
# print(data[999]['articles'])
# jieba cut

jieba.case_sensitive = True
jieba.set_dictionary('./dict.txt.big.txt')
jieba.load_userdict('./title.txt')

dict = {}
for i in range(50000):
    print(i)
    seg_list = jieba.lcut(data[i]['articles'])
    for item in seg_list:                           # start to build inverted index
        if item not in dict:
            dict[item] = []
            dict[item].append(data[i]['id'])
        elif item in dict:
            flag = 0
            for j in dict[item]:
                if j == data[i]['id']:
                    flag = 1
            if flag == 0:
                dict[item].append(data[i]['id'])

    seg_list.clear()


for item in dict.keys():
    dict[item].sort()
    # print(item)


# print(dict['使用'])
with codecs.open("InvertedIndex.json", 'w', encoding="utf-8") as tmpFp:
    json.dump(dict, tmpFp, sort_keys=True, ensure_ascii=False)
