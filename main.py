# -*- coding: utf-8 -*-
# !python3
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       sheng
   date：          2019/9/4
-------------------------------------------------
   Change Activity:
                   2019/9/4:
-------------------------------------------------
"""
import json

import redis

from utils.tet_bert_keras_sim import SimTwoQuestion
from utils.redis_db import get_data_from_db_by_name, generate_html_by_data

from utils.redis_db import update_QA_db
from utils.BaiduTransAPI import trans_question
from utils.cut_td_idf import main
from utils.redis_db import update_history_question, update_common_question
from utils.redis_db import remove_temp_pic


class Query:

    def __init__(self):
        remove_temp_pic()
        update_QA_db()
        remove_temp_pic()
        main()
        r = redis.Redis(host="127.0.0.1", port=6379, db=0)
        questions = [q.decode('utf-8') for q in r.keys('*')]
        self.update_trans_questions(questions)
        self.questions_dict = json.load(open('Data/txt_file/questions_dict.json', 'r', encoding="utf-8"))
        self.questions = list(self.questions_dict.keys())
        self.sim_two_question = SimTwoQuestion(self.questions)
        r.close()
        print("完成初始化Query！")

    @staticmethod
    def update_trans_questions(questions):
        trans_question(questions)

    def query(self, question):
        scores = self.sim_two_question.sim_questions(question)
        print(max(scores))
        max_index = scores.index(max(scores))
        print(self.questions[max_index])
        answer_raw = get_data_from_db_by_name(name=self.questions_dict[self.questions[max_index]])
        update_common_question(self.questions_dict[self.questions[max_index]])
        update_history_question(self.questions_dict[self.questions[max_index]])
        answer = generate_html_by_data(answer_raw)
        print(answer)

        return answer

    def simple_query(self, question):
        scores = self.sim_two_question.sim_questions(question)
        max_index = scores.index(max(scores))
        return self.questions[max_index]


if __name__ == '__main__':
    query = Query()

    while True:
        question = input("请输入问题：")
        print(query.simple_query(question))
