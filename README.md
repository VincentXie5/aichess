# aichess
# 使用alphazero算法打造属于你自己的象棋AI

## 一、每个文件的意义
collect.py      自我对弈用于数据收集

train.py    用于训练模型

game.py    实现象棋的逻辑

mcts.py    实现蒙特卡洛树搜索

paddle_net.py，pytorch_net.py   神经网络对走子进行评估

play_with_ai.py  人机对弈print版

UIplay.py   GUI界面人机对弈

UIplay_for_collect.py   GUI界面人机对弈，并且会将对弈的数据收集起来


## 二、提供了两个框架的版本进行训练：
使用pytorch版本请设置config.py 中CONFIG['use_frame'] = 'pytorch'，

使用pytorch版本请设置config.py 中CONFIG['use_frame'] = 'paddle'。

不管是使用哪个框架，都一定要安装gpu版本，而且要用英伟达显卡，因为我们蒙特卡洛一次走此要进行上千次的神经网络推理，所以必须要快！

## 三、本项目是多进程同步训练。
训练时，在终端运行python collect.py用于自我对弈产生数据，这个可以多开。

运行python UIplay_for_collect.py 进行界面人机对弈数据收集

然后，在终端运行python train.py用于模型训练，这个终端只用开一个。

## 四、声明
本项目fork自https://github.com/tensorfly-gpu/aichess，并为了运行做了一些代码修改

源代码可以去原始仓库查看，支持原作者
