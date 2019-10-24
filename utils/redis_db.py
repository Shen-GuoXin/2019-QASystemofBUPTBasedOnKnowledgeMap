#! python
# -*- encoding: utf-8 -*-
'''
@File    :   redis_db
@Time    :   2019/09/22 21:46:54
@Author  :   Shen Guoxin 
@Version :   1.0
@Contact :   shenguoxin@bupt.edu.cn
@License :   (C)Copyright 2019-2020, Shenguoxin
@Desc    :   None
'''

# here put the import lib
from __future__ import absolute_import
import redis
import base64
from utils.read_words import ReadWords
import datetime
import os
from conf.path_config import projectdir

extime = datetime.datetime(2020, 9, 8, 15, 19, 10)
r0 = redis.Redis(host='127.0.0.1', port=6379, db=0)
r1 = redis.Redis(host='127.0.0.1', port=6379, db=1)
'''
存储提取到redis数据库中
'''
imagesNumber = 0


def update_history_question(question):
    """
    保存最近十条问题；
    """
    if r1.exists("history_question"):
        if r1.scard("history_question") < 10:
            r1.sadd("history_question", question)
        else:
            r1.spop('history_question')
            r1.sadd("history_question", question)
    else:
        r1.sadd("history_question", question)
    r1.expireat('history_question', extime)


def get_history_question():
    return [_.decode('utf-8') for _ in r1.smembers('history_question')]


def update_common_question(question):
    """
    保存常见问题；
    """
    r1.zincrby('common_question', value=question, amount=1)
    r1.expireat('common_question', extime)


def get_common__question():
    return [_[0].decode('utf-8') for _ in
            r1.zrange("common_question", start=0, end=3, desc=True, withscores=True, score_cast_func=int)]


def pic2data(file):
    with open(file, "rb") as f:
        base64_data = base64.b64encode(f.read())
        return base64_data


def data2pic(data, filename="temp.jpeg"):
    data = base64.b64decode(data)
    with open(filename, "wb") as f:
        f.write(data)


def update_QA_db():
    read_word = ReadWords()
    questions = read_word.questions
    contents = read_word.contents
    for index in range(len(questions)):
        question = questions[index]
        if r0.exists(question):
            continue
        print("增加新问题：{}".format(question))
        content = contents[index]
        pics = read_word.get_pic_from_word(os.path.join(projectdir,
                                                        'Data/questions/{}.docx'.format(question)))
        final_result = []
        _ = 0
        flag = True
        for t in content:
            if t != '':
                final_result.append("0")  # 0代表文字
                final_result.append(t)
            else:
                try:
                    pic_data = pic2data(
                        os.path.join(
                            projectdir, "static/tempImages/{}".format(pics[_])))
                    final_result.append(pics[_])  # 1代表图片信息
                    final_result.append(pic_data)
                    _ += 1
                except Exception as e:
                    print(e)
                    print(question, content, pics)
                    flag = False
                    break
        if not flag:
            print("问题：“{}”出错！".format(question))
            continue
        for d in final_result:
            r0.lpush(question, d)
        r0.expireat(question, extime)
        print("增加新问题：{}成功！".format(question))
    print("完成更新问题库！")


def remove_temp_pic():
    for i in os.listdir(os.path.join(projectdir, "static/tempImages")):
        os.remove(os.path.join(os.path.join(
            projectdir, "static/tempImages", i)))


def get_data_from_db_by_name(name):
    global imagesNumber
    txtOrPic = True
    imageName = ""
    all_data = []
    for index in range(r0.llen(name)):
        data = r0.lindex(name, r0.llen(name) - index - 1).decode("utf-8")
        if data == "0":
            txtOrPic = True
        elif 'image' in data:
            txtOrPic = False
            imageName = data
        else:
            if not txtOrPic:
                data2pic(
                    data, filename=os.path.join(
                        projectdir, "static/tempImages/image{}{}".format(imagesNumber, imageName)))
                data = "../static/tempImages/image{}{}".format(imagesNumber, imageName)
                imagesNumber += 1
        all_data.append(data)
    return all_data


def generate_html_by_data(data):
    html = '<div>'
    txtOrPic = True
    for d in data:
        if d == '0':
            txtOrPic = True
        elif 'image' in d and 'static' not in d:
            txtOrPic = False
        else:
            if txtOrPic:
                html += '<p>' + d + '</p>'
            else:
                html += '<img src="{}"  width:auto height:100%;>'.format(
                    d.replace('\\', '/'))
    html += '</div>'
    return html


if __name__ == "__main__":
    # data = get_data_from_db_by_name("Mac笔记本如何连接BUPT-Portal？")
    # print(data)
    remove_temp_pic()
    print(get_common__question())

    print("********************************")
    print(get_history_question())
