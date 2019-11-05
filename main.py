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

from utils.redis_db import update_db
from utils.BaiduTransAPI import trans_question
from utils.cut_td_idf import cut_td_idf_main
from utils.redis_db import update_history_question, update_common_question
from utils.redis_db import remove_temp_pic


class Query:

    def __init__(self):
        remove_temp_pic()
        if input("是否添加新的问题？(Y/N)") == "Y":
            update_db()
            remove_temp_pic()
        cut_td_idf_main()
        r = redis.Redis(host="127.0.0.1", port=6379, db=0)
        questions = [q.decode('utf-8') for q in r.keys('*')]
        trans_question(questions)
        self.questions_dict = json.load(open('Data/txt_file/questions_dict.json', 'r', encoding="utf-8"))
        self.questions = list(self.questions_dict.keys())
        self.sim_two_question = SimTwoQuestion(self.questions)
        r.close()
        print("完成初始化Query！")

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
        print(query.simple_query(input("请输入问题：")))
