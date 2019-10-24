import pathlib
import sys
import os


# base dir
projectdir = str(pathlib.Path(os.path.abspath(__file__)).parent.parent)
sys.path.append(projectdir)


# path of BERT model
model_dir = projectdir + '/Data/chinese_L-12_H-768_A-12'
config_name = model_dir + '/bert_config.json'
ckpt_name = model_dir + '/bert_model.ckpt'
vocab_file = model_dir + '/vocab.txt'
# gpu使用率
gpu_memory_fraction = 0.32
# 默认取倒数第二层的输出值作为句向量
layer_indexes = [-2] # 可填 1, 2, 3, 4, 5, 6, 7..., 13,其中1为embedding层
# 序列的最大程度
max_seq_len = 32
