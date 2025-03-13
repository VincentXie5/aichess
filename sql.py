import pickle
import random
import sqlite3
import time

from config import CONFIG


class DataBase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None):
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.conn.commit()
        return cursor

    def insert_play_data(self, play_data):
        # 插入收集到训练数据
        binary_play_data = [(pickle.dumps(data),) for data in play_data]
        self.conn.cursor().executemany('INSERT INTO t_play_data (data) VALUES (?)', binary_play_data)
        self.conn.commit()

    def get_play_data_randomly(self, batch_size):
        while True:
            try:
                # 随机获取batch_size个局面，用于训练模型
                rows = self.get_total_rows()
                random_index = random.sample(range(1, rows + 1), batch_size)
                placeholders = ','.join('?' for _ in random_index)
                query = f'SELECT data FROM t_play_data WHERE id IN ({placeholders})'
                cursor = self.execute(query, random_index)
                return [pickle.loads(data[0]) for data in cursor.fetchall()]
            except Exception as e:
                print('获取对弈数据报错, 休眠{}秒'.format(CONFIG['train_update_interval']))
                print('报错信息：', e)
                time.sleep(CONFIG['train_update_interval'])


    def get_total_rows(self):
        cursor = self.execute('Select max(id) from t_play_data')
        return cursor.fetchone()[0]

    # 获取这是下的第几盘，获取一次，递增一次，需要确保多进程安全，采用事务
    def get_iter_and_increment(self):
        cursor = self.conn.cursor()
        cursor.execute('BEGIN EXCLUSIVE TRANSACTION')
        try:
            cursor.execute('SELECT iter FROM t_iter')
            current_iter = cursor.fetchone()[0]
            new_iter = current_iter + 1
            cursor.execute('UPDATE t_iter SET iter = ?', (new_iter,))
            self.conn.commit()
            return new_iter
        except Exception as e:
            print('获取盘次失败，请检查')
            self.conn.rollback()
            raise e

    # 获取当前已经下了多少盘
    def get_iter(self):
        cursor = self.execute('SELECT iter FROM t_iter')
        return cursor.fetchone()[0]

    def close(self):
        # 手动关闭连接
        if self.conn:
            self.conn.close()
            self.conn = None

    def __del__(self):
        # 析构函数，确保连接关闭
        self.close()

if __name__ == '__main__':
    with DataBase(CONFIG['db_file']) as db:
        # db.execute('CREATE TABLE IF NOT EXISTS t_play_data (id INTEGER PRIMARY KEY AUTOINCREMENT, data BLOB)')
        # db.execute('CREATE TABLE IF NOT EXISTS t_iter (iter INTEGER)')
        # db.execute('INSERT INTO t_iter (iter) VALUES (0)')
        # randomly = db.get_play_data_randomly(512)
        print('rows:', db.get_total_rows())
        print('执行完毕')
