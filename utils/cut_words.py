#! python
# -*- encoding: utf-8 -*-
'''
@File    :   cut_words.py
@Time    :   2019/09/23 15:45:07
@Author  :   Shen Guoxin 
@Version :   1.0
@Contact :   shenguoxin@bupt.edu.cn
@License :   (C)Copyright 2019-2020, Shenguoxin
@Desc    :   None
'''

# here put the import lib
from jieba import lcut
from main import Query
from py2neo import Graph
from conf.path_config import stop_words_path

graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="sgxsgwbd"
)


def contents2txt():
    query = Query()
    contents = query.questions
    print(contents)
    # contents = [','.join(content) for content in contents]
    txt = ','.join(contents)
    txt += ','.join(query.questions)
    with open('temp.txt', 'w', encoding='utf-8') as f:
        f.write(txt)


def stopwordslist():
    stopwords = [line.strip() for line in open(
        stop_words_path, encoding='UTF-8').readlines()]
    return stopwords


def process_txt():
    text = open('temp.txt', 'r', encoding='utf-8').read()
    text = text.replace('\xa0', '')
    stopwords = stopwordslist()
    cut_words = lcut(text)
    cut_words = filter(lambda s: s not in stopwords, cut_words)
    cut_words = list(cut_words)
    print(cut_words)
    mytext = ' '.join(cut_words)
    from wordcloud import WordCloud
    wordcloud = WordCloud(
        font_path="D:/Import_Download/simsun.ttf").generate(mytext)
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()
    plt.axis("off")


def create_words_links(data, label):
    """
    data是一个列表，里面包含词语
    """
    for index in range(len(data) - 1):
        head = data[index]
        end = data[index + 1]
        graph.run(
            'merge (P:%s词语{Word:"%s"}) return id(P)'
            % (label, head))
        graph.run(
            'merge (P:%s词语{Word:"%s"}) return id(P)'
            % (label, end))
        graph.run(
            'match (s:%s词语),(e:%s词语) where s.Word="%s" and e.Word="%s" merge(s)-[r1:上下词]->(e)' %
            (label, label, head, end))
        break


def create_question_words():
    query = Query()
    questions = query.questions
    stopwords = stopwordslist()
    for question in questions:
        cut_words = lcut(question)
        cut_words = filter(lambda s: s not in stopwords, cut_words)
        cut_words = list(cut_words)
        create_words_links(cut_words, label="问句")


def create_answer_words():
    query = Query()
    contents = query.contents
    stopwords = stopwordslist()
    for _ in contents:
        for content in _:
            cut_words = lcut(content)
            cut_words = filter(lambda s: s not in stopwords, cut_words)
            cut_words = list(cut_words)
            create_words_links(cut_words, label="答案")


if __name__ == "__main__":
    # contents2txt()
    # process_txt()
    # create_question_words()
    create_answer_words()
