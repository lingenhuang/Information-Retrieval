from flask import Flask, render_template, request
# from ckiptagger import data_utils, construct_dictionary, WS
import jieba
import csv

jieba.load_userdict('dict_taiwan.txt')
stop_words_list = list()
with open('stop_list.txt', encoding  = 'utf-8', newline='\n') as txtfile:
        stop_words_list = txtfile.read().split("\n")
stop_words_list = stop_words_list[1:-1]
# ws = WS("./data")
data = list()
app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if request.values['send'] == 'send':
            output_list = startSearch(request.values['keyword'])
            return render_template('IR.html', keyword=output_list[:15], user_input=request.values['keyword'])
    return render_template('IR.html', keyword="")
    # return render_template("IR.html")


def startSearch(input_keyword):
    # cut_keyword = ws([input_keyword])[0]
    # cut_keyword = jieba.lcut(input_keyword, cut_all=False, HMM=True)
    # cut_keyword = jieba.lcut(input_keyword, cut_all=True, HMM=True)
    word =input_keyword + " " + ''.join(input_keyword.split())#將keyword字串中的空格拿掉
    cut_keyword = jieba.lcut_for_search(word.lower())# 切keyword
    # input_keyword = ''.join(input_keyword.split())
    for splitt in stop_words_list:
            input_keyword = ''.join(input_keyword.split(splitt))
    cut_keyword.append(input_keyword.lower()) #直接放 keyword  ##空格拿掉
    print("cut: {}".format(cut_keyword))
    song_list, score_list, flag = countScore(cut_keyword)
    if flag == False:
        song_list.append("找不到歌!!!!!!")
    return song_list


def countScore(cut_keyword):
    global data
    score_dict = dict()
    song_list = list()
    score_list = list()
    feature_counter_dict = dict()
    kw_counter = 0
    for kw in cut_keyword:
        if data.get(kw) is not None:
            kw_counter += 1
            data_list = data.get(kw)
            print(kw)
            print(data_list)
            print()
            for idx in range(0, len(data_list), 2):
                score_dict[data_list[idx]] = score_dict.get(data_list[idx], 0) + float(data_list[idx+1])
                feature_counter_dict[data_list[idx]] = feature_counter_dict.get(data_list[idx], 0) + 1

    for i in feature_counter_dict.keys():
        if feature_counter_dict[i] == kw_counter:
            score_dict[i] = score_dict.get(i) * 10
        elif feature_counter_dict[i] == kw_counter - 1:
            score_dict[i] = score_dict.get(i) * 4

    flag = True
    if len(score_dict.keys()) == 0:
        flag = False
    else:
        song_list = list(score_dict.keys())
        score_list = list(score_dict.values())
        score_list, song_list = zip(*sorted(zip(score_list, song_list)))
        song_list = list(song_list)
        score_list = list(score_list)
        song_list.reverse()
        score_list.reverse()
        for i in range(len(song_list)):
            print("{} : {}".format(song_list[i], score_list[i]))

        # print("song list: {}".format(song_list))
        # print("score list: {}".format(score_list))

    return song_list, score_list, flag


def readData():
    global data
    with open('output_file_taiwan_no_stopwords_notation/jieba_search_output.csv', encoding = 'utf-8', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        data = list(csv.reader(csvfile))


def listToDict():
    global data
    temp_data = dict()
    for i in data:
        temp_list = list()
        for idx, j in enumerate(i):
            if idx != 0:
                temp_list.append(j)
        temp_data[i[0]] = temp_list
    data = temp_data


    # run app
if __name__ == "__main__":
    readData()
    listToDict()
    app.run(host='127.0.0.1', port=5000)
