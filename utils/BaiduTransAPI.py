# 百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8

import http.client
import hashlib
import urllib
import random
import json
from conf.path_config import projectdir
import os


def baiduTranslate(text, toLang="en"):
    if text is None:
        return None
    appid = '20191017000342155'  # 填写你的appid

    secretKey = 'yRFtHiTxqbPoXQjvd47d'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'
    fromLang = 'auto'  # 原文语种
    # toLang = 'en'  # 译文语种
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        # print(result)
        return result['trans_result'][0]['dst']

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


def trans_question(texts):
    print("开始回译问题")
    try:
        questions_dict = json.load(
            open(os.path.join(projectdir, "Data/txt_file/questions_dict.json"), 'r', encoding='utf-8'))
    except:
        questions_dict = {}
    exits_question = list(set(questions_dict.values()))
    languages = ['en', 'jp', 'kor', 'fra', 'spa', 'ru', 'de']
    for text in texts:
        text = text.strip()
        if text in exits_question:
            continue
        questions_dict[text] = text
        for language in languages:
            temp_text = baiduTranslate(text, language)
            temp_text = baiduTranslate(temp_text, 'zh')
            if temp_text != "null":
                questions_dict[temp_text] = text
        with open(os.path.join(projectdir, "Data/txt_file/questions_dict.json"), 'w', encoding='utf-8') as f:
            json.dump(questions_dict, f, ensure_ascii=False, indent=4)
    print("回译问题完成")


if __name__ == "__main__":
    pass
