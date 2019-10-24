from utils.extract_keras_bert_feature import KerasBertVector

from math import pi
import numpy as np

import math


class SimTwoQuestion:
    def __init__(self, questions=None):
        self.bert_vector = KerasBertVector()
        self.vectors = self.bert_vector.bert_encode(questions)
        print("完成原始问题集词向量化！")

    @staticmethod
    def cosine_distance(v1, v2):  # 余弦距离
        if all(v1) and all(v2):
            return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        else:
            return 0

    @staticmethod
    def scale_zoom(rate):  # sig 缩放
        zoom = (1 + np.exp(-float(rate))) / 2
        return zoom

    @staticmethod
    def scale_triangle(rate):  # sin 缩放
        triangle = math.sin(rate / 1 * pi / 2 - pi / 2)
        return triangle

    def sim_questions(self, question):
        question_vector = self.bert_vector.bert_encode([question])
        sim = [self.cosine_distance(self.vectors[i], question_vector[0]) for i in range(len(self.vectors))]
        return sim
