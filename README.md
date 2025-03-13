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
本项目fork自https://github.com/tensorfly-gpu/aichess

并为了运行做了一些代码修改

源代码可以去原始仓库查看，支持原作者

## 五、训练日记
我用4060 TI 跑了两种参数，每种参数跑了两天
一种是playout=200,思考的很快，但自我对弈了七千多盘的之后，
效果依然很差，会无意义的起边相和不断的拱兵，还没有体现出它对子力的理解
说明在这个参数下自我对弈的质量非常差

一种是playout=1200，思考的很慢，两天只下了491盘，
但是开始选择中炮这类有点意义的起步，但中盘依然有无意义的拱兵之类的

两者在两天训练出来的效果差不多，也已经学会了基本的防守，在被将军时会尽量保证将军存活，
但第二种效果收集到491盘就棋力和第一种差不多，说明还是第二种好一点，虽然不省时间，但能省点存储空间

