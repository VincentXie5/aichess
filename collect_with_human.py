"""和人类对弈收集数据"""
from collections import deque
import copy
import os
import pickle
import time
from game import move_action2move_id, move_id2move_action, flip_map
from config import CONFIG

import zip_array



# 定义整个对弈收集数据流程
class CollectWithHumanPipeline:
    def __init__(self, init_model=None):
        # 对弈参数
        self.temp = 1  # 温度
        self.n_playout = CONFIG['play_out']  # 每次移动的模拟次数
        self.c_puct = CONFIG['c_puct']  # u的权重
        self.buffer_size = CONFIG['buffer_size']  # 经验池大小
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.iters = 0

    def get_equi_data(self, play_data):
        """左右对称变换，扩充数据集一倍，加速一倍训练速度"""
        extend_data = []
        # 棋盘状态shape is [9, 10, 9], 走子概率，赢家
        for state, mcts_prob, winner in play_data:
            # 原始数据
            extend_data.append(zip_array.zip_state_mcts_prob((state, mcts_prob, winner)))
            # 水平翻转后的数据
            state_flip = state.transpose([1, 2, 0])
            state = state.transpose([1, 2, 0])
            for i in range(10):
                for j in range(9):
                    state_flip[i][j] = state[i][8 - j]
            state_flip = state_flip.transpose([2, 0, 1])
            mcts_prob_flip = copy.deepcopy(mcts_prob)
            for i in range(len(mcts_prob_flip)):
                mcts_prob_flip[i] = mcts_prob[move_action2move_id[flip_map(move_id2move_action[i])]]
            extend_data.append(zip_array.zip_state_mcts_prob((state_flip, mcts_prob_flip, winner)))
        return extend_data

    def collect(self, play_data):
        play_data = list(play_data)[:]
        self.episode_len = len(play_data)
        # 增加数据
        play_data = self.get_equi_data(play_data)
        if os.path.exists(CONFIG['train_data_with_human_buffer_path']):
            while True:
                try:
                    with open(CONFIG['train_data_with_human_buffer_path'], 'rb') as data_dict:
                        data_file = pickle.load(data_dict)
                        self.data_buffer = deque(maxlen=self.buffer_size)
                        self.data_buffer.extend(data_file['data_buffer'])
                        self.iters = data_file['iters']
                        del data_file
                        self.iters += 1
                        self.data_buffer.extend(play_data)
                    print('成功载入数据')
                    break
                except:
                    time.sleep(30)
        else:
            self.data_buffer.extend(play_data)
            self.iters += 1
        data_dict = {'data_buffer': self.data_buffer, 'iters': self.iters}
        with open(CONFIG['train_data_with_human_buffer_path'], 'wb') as data_file:
            pickle.dump(data_dict, data_file)
            print('成功保存数据')
        return self.iters
