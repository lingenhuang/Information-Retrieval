import jieba
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
# from ckiptagger import data_utils, construct_dictionary, WS
import pandas as pd
import os
import csv

jieba.load_userdict('dict_taiwan.txt')
# jieba.enable_parallel(4)
# data_utils.download_data("./")

# ws = WS("./data")
stop_words_list = list()
with open('stop_list.txt', encoding  = 'utf-8', newline='\n') as txtfile:
        stop_words_list = txtfile.read().split("\n")
stop_words_list = stop_words_list[1:-1]

withoutyou = 0
for i in range(3,4):
    print("i: {}".format(i))
    idx = []
    doc = []
    filename = ""
    for ind, file in enumerate(os.listdir(r'txt')):
        # print(ind)
        # if ind == 1:
        #     break
        if ind%100 ==  0:
            print(ind)
        domain = os.path.abspath(r'txt')
        strr = file[:-4]
        idx.append(strr)
        file = os.path.join(domain, file)
        file = open(file, 'r', encoding='utf-8')
        txt = file.read()
        
        strrr = ''.join(strr.split()) #將歌名字串中的空格拿掉
        txt += strr + " " + strrr  #放歌名進去切
        temp_list = list()
        temp_list.append(txt)
        if i == 0:
            # sent_words = ws(temp_list)
            filename = "output_file_taiwan_no_stopwords_notation/ckiptagger_output.csv"
        elif i == 1:
            sent_words = [list(jieba.cut(txt))]
            filename = "output_file_taiwan_no_stopwords_notation/jieba_normal_output.csv"
        elif i == 2:
            sent_words = [list(jieba.cut(txt, cut_all=True))]
            filename = "output_file_taiwan_no_stopwords_notation/jieba_cut_all_output.csv"
        else:
            sent_words = [list(jieba.cut_for_search(txt))]
            filename = "output_file_taiwan_no_stopwords_notation/jieba_search_output.csv"

        for splitt in stop_words_list:
            strr = ''.join(strr.split(splitt))
        sent_words[0].append(strrr) #加入整個歌名

        # if strr == "24HoursfeatJuliaWu":
        #     withoutyou = ind
        #     print("txt\n{}\n\nstrr\n{}\n\nsent_words\n{}".format(txt,strr,sent_words[0]))

        document = [" ".join(sent0) for sent0 in sent_words]
        doc += document
        file.close()

    # 轉換TFIDF
    # vectorizer = TfidfVectorizer(sublinear_tf=False, stop_words = stop_words_list, token_pattern="(?u)\\b\w+\\b", smooth_idf=True, norm='l2')
    vectorizer = TfidfVectorizer(sublinear_tf=False, stop_words = None, token_pattern="(?u)\\b\w+\\b", smooth_idf=True, norm='l2')
    tfidf = vectorizer.fit_transform(doc)
    df_tfidf = pd.DataFrame(tfidf.toarray(
    ), columns=vectorizer.get_feature_names(), index=idx)

    print("________finish cut_________")
    
    word_list = list(vectorizer.get_feature_names())
    tfidf_list = list()
    song_list = list()

    # for index, i in enumerate(word_list):
    #     if tfidf[withoutyou, index] != 0:
    #         print(i)



    for index, i in enumerate(word_list):
        tfidf_list.append(list())
        song_list.append(list())

        if index%100 == 0:
            print(index)   
        for j in range(len(idx)):
            if tfidf[j, index] != 0:
                tfidf_list[index].append(tfidf[j, index])
                song_list[index].append(idx[j])
            
        tfidf_list[index], song_list[index] = zip(*sorted(zip(tfidf_list[index], song_list[index])))
        tfidf_list[index] = list(tfidf_list[index])
        song_list[index] = list(song_list[index])
        tfidf_list[index].reverse()
        song_list[index].reverse()

    table_list = list()#len(vectorizer.get_feature_names())
    for index, i in enumerate(word_list):
        table_list.append(list())
        table_list[index].append(i)
        for j in range(len(song_list[index])):
            table_list[index].append(song_list[index][j])
            table_list[index].append(tfidf_list[index][j])
        

    # 開啟輸出的 CSV 檔案
    with open(filename, 'w', encoding = "utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table_list)


 
