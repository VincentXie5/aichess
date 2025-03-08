CONFIG = {
    'kill_action': 30,      #和棋回合数
    'dirichlet': 0.2,       # 国际象棋，0.3；日本将棋，0.15；围棋，0.03，视每一步的可选择走子而定，每一步的选择越多，这个值越小，作者综合考虑后，选择了0.2
    'play_out': 120,        # 每次移动的模拟次数
    'c_puct': 5,             # u的权重
    'buffer_size': 100000,   # 经验池大小
    'paddle_model_path': 'current_policy.model',      # paddle模型路径
    'pytorch_model_path': 'current_policy.pkl',   # pytorch模型路径
    'db_file': 'play_data.db', # 数据库文件名
    'batch_size': 512,  # 每次更新的train_step数量
    'kl_targ': 0.02,  # kl散度控制
    'epochs' : 5,  # 每次更新的train_step数量
    'game_batch_num': 3000,  # 训练更新的次数
    'use_frame': 'pytorch',  # paddle or pytorch根据自己的环境进行切换
    'train_update_interval': 90,  #模型更新间隔时间
}