"""自我对弈收集数据"""
import copy
import os
import time

import zip_array
from config import CONFIG
from game import Board, Game, move_action2move_id, move_id2move_action, flip_map
from mcts import MCTSPlayer
from sql import DataBase

if CONFIG['use_frame'] == 'paddle':
    from paddle_net import PolicyValueNet
elif CONFIG['use_frame'] == 'pytorch':
    from pytorch_net import PolicyValueNet
else:
    print('暂不支持您选择的框架')


# 定义整个对弈收集数据流程
class CollectPipeline:

    def __init__(self, init_model=None):
        # 象棋逻辑和棋盘
        self.board = Board()
        self.game = Game(self.board)
        # 对弈参数
        self.temp = 1  # 温度
        self.n_playout = CONFIG['play_out']  # 每次移动的模拟次数
        self.c_puct = CONFIG['c_puct']  # u的权重
        self.iters = 0
        self.episode_len = 0

    # 从主体加载模型
    def load_model(self):
        if CONFIG['use_frame'] == 'paddle':
            model_path = CONFIG['paddle_model_path']
        elif CONFIG['use_frame'] == 'pytorch':
            model_path = CONFIG['pytorch_model_path']
        else:
            print('暂不支持所选框架')
        try:
            self.policy_value_net = PolicyValueNet(model_file=model_path)
            print('已加载最新模型')
        except:
            self.policy_value_net = PolicyValueNet()
            print('已加载初始模型')
        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
                                      c_puct=self.c_puct,
                                      n_playout=self.n_playout,
                                      is_selfplay=1)

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

    def collect_selfplay_data(self, n_games=1):
        # 收集自我对弈的数据
        for i in range(n_games):
            self.load_model()  # 从本体处加载最新模型
            winner, play_data = self.game.start_self_play(self.mcts_player, temp=self.temp, is_shown=True)
            play_data = list(play_data)[:]
            self.episode_len = len(play_data)
            # 增加数据
            play_data = self.get_equi_data(play_data)
            if os.path.exists(CONFIG['db_file']):
                with DataBase(CONFIG['db_file']) as db:
                    db.insert_play_data(play_data)
                    self.iters = db.get_iter_and_increment()
            else:
                print('数据库文件未初始化，请执行sql.py的代码')

    def run(self):
        """开始收集数据"""
        try:
            while True:
                start_time = time.time()
                self.collect_selfplay_data()
                print('对局序号: {}, 对局步数: {}, 对局时间：{}'.format(
                    self.iters, self.episode_len, time.time() - start_time))
        except KeyboardInterrupt:
            print('\n\rquit')

if __name__ == '__main__':
    if CONFIG['use_frame'] == 'paddle':
        collecting_pipeline = CollectPipeline(init_model='current_policy.model')
        collecting_pipeline.run()
    elif CONFIG['use_frame'] == 'pytorch':
        collecting_pipeline = CollectPipeline(init_model='current_policy.pkl')
        collecting_pipeline.run()
    else:
        print('暂不支持您选择的框架')
        print('训练结束')
