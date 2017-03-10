# -*- coding: utf-8 -*-

import sys
import random
import math
from operator import itemgetter
import os
random.seed(0)

''' 基于近邻用户的TopN推荐算法 - UserBasedCF '''
class UserBasedCF():

    # self.workSignal.emit('--------------------------------------------------------------')
    # self.workSignal.emit('欢迎使用基于近邻的 UserBased 推荐系统')
    # self.workSignal.emit('--------------------------------------------------------------')

    # 初始化类
    def __init__(self, user_num, item_num, workSignal):

        self.train_set = {}      # 训练集
        self.test_set = {}       # 测试集

        self.sim_user_num = user_num    # 相似用户数
        self.rec_item_num = item_num    # 推荐物品数

        self.workSignal = workSignal  # 输出信号

        self.user_sim_mat = {}      # 用户兴趣相似度矩阵
        self.item_popular = {}      # 物品流行度
        self.item_count = 0         # 总物品数

        self.workSignal.emit('相似用户数 = %d' % self.sim_user_num)
        self.workSignal.emit('推荐物品数 = %d' % self.rec_item_num)


        # self.workSignal.emit('相似用户数 = %d' % self.sim_user_num)
        # self.workSignal.emit('推荐物品数 = %d' % self.rec_item_num)
        # self.workSignal.emit('--------------------------------------------------------------')

    # 加载数据集文件，返回一个生成器
    def loadfile(self, filename):
        fp = open(filename, 'r')

        self.workSignal.emit('加载数据集: %s 中...' % (os.path.basename(filename)))
        # self.workSignal.emit()
        
        for i, line in enumerate(fp):# 计算出用户相似度矩阵
            yield line.strip('\r\n')
        fp.close()
        self.workSignal.emit('加载数据集: %s 已完成' % (os.path.basename(filename)))
        self.workSignal.emit('数据集数据量为：%s ' %(i - 1))

    # 加载数据集，并将其划分为训练集和测试集
    def generate_data_set(self, filename, pivot=0.8):

        train_set_len = 0       # 训练集数据量
        test_set_len = 0        # 测试集数据量

        # 将数据集随机分为训练集和测试集
        for line in self.loadfile(filename):
            user, item, rating, timestamp = line.split('::')    # 用户，项目，评分，时间戳
            if (random.random() < pivot):
                self.train_set.setdefault(user, {})
                self.train_set[user][item] = int(rating)
                train_set_len += 1
            else:
                self.test_set.setdefault(user, {})
                self.test_set[user][item] = int(rating)
                test_set_len += 1
        self.workSignal.emit('生成训练集和测试集中...')
        self.workSignal.emit('生成训练集与测试集已完成')
        self.workSignal.emit('训练集数据量 = %s' % (train_set_len - 1))
        self.workSignal.emit('测试集数据量 = %s' % (test_set_len - 1))

    # 计算出用户相似度矩阵
    def calc_user_sim(self):

        item_to_users = dict()                 # 物品到用户倒排表
        com_items_num = self.user_sim_mat      # 用户共同物品数

        #建立"物品->用户"倒排表，计算物品的流行度
        self.workSignal.emit('建立"物品->用户"倒排表中...')
        for user, items in self.train_set.items():
            for item in items:
                if item not in item_to_users:
                    item_to_users[item] = set()
                item_to_users[item].add(user)
                if item not in self.item_popular:
                    self.item_popular[item] = 0
                self.item_popular[item] += 1
        self.item_count = len(item_to_users)
        self.workSignal.emit('建立"物品->用户"到排表已完成')
        self.workSignal.emit('物品总数量 = %d' % self.item_count)

        # 计算两个用户之间的共同物品数
        self.workSignal.emit('建立用户之间相同物品数矩阵中...')
        for item, users in item_to_users.items():
            for u in users:
                for v in users:
                    if u == v: continue
                    com_items_num.setdefault(u, {})
                    com_items_num[u].setdefault(v, 0)
                    com_items_num[u][v] += 1
        self.workSignal.emit('建立用户之间相同物品数矩阵已完成')

        # 通过余弦相似度计算出用户之间兴趣相似度矩阵
        self.workSignal.emit('建立用户之间的兴趣相似度矩阵中...')
        for u, related_users in com_items_num.items():
            for v, count in related_users.items():
                self.user_sim_mat[u][v] = count / math.sqrt(len(self.train_set[u]) * len(self.train_set[v]))
        self.workSignal.emit('建立用户之间的兴趣相似度矩阵已完成')

    # 找到K个最相似用户并且推荐N个物品，wuv=用户u和用户v的兴趣相似度
    def recommend(self, user):

        rank = dict()             # 兴趣物品预测得分排名
        K = self.sim_user_num     # 相似用户数
        N = self.rec_item_num     # 推荐物品数
        interacted_items = self.train_set[user]     # 用户已用物品集，需过滤不再推荐

        for v, wuv in sorted(self.user_sim_mat[user].items(),key=itemgetter(1), reverse=True)[0:K]:
            for item in self.train_set[v]:
                if item in interacted_items:
                    continue
                rank.setdefault(item, 0)
                rank[item] += wuv*1
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    # 运行推荐函数，并评测算法，计算准确率，召回率，覆盖率和流行度
    def evaluate(self):

        hit = 0                 # 推荐物品命中次数
        rec_count = 0           # 推荐物品总次数
        test_count = 0          # 被推荐用户在测试集喜欢物品总次数
        popular_sum = 0         # 物品流行度总和
        all_rec_items = set()   # 所有被推荐物品集合
        N = self.rec_item_num   # 对一个用户推荐物品数

        self.workSignal.emit('根据%d位最相似用户推荐%d个物品中...' %(self.sim_user_num,self.rec_item_num))
        for i, user in enumerate(self.train_set):
            test_items = self.test_set.get(user, {})
            rec_items = self.recommend(user)
            for item, w in rec_items:
                if item in test_items:
                    hit += 1
                all_rec_items.add(item)
                popular_sum += math.log(1 + self.item_popular[item])
            rec_count += N
            test_count += len(test_items)
        self.workSignal.emit('根据%d位最相似用户推荐%d个物品已完成' % (self.sim_user_num, self.rec_item_num))

        self.workSignal.emit('评测该推荐系统各项指标中...')
        precision = hit / (1.0 * rec_count)                         #准确率
        recall = hit / (1.0 * test_count)                           #召回率
        coverage = len(all_rec_items) / (1.0 * self.item_count)     #覆盖率
        popularity = popular_sum / (1.0 * rec_count)                #流行度
        self.workSignal.emit('评测该推荐系统各项指标已完成')
        self.workSignal.emit('准确率=%.2f %% \t召回率=%.2f %% \n覆盖率=%.2f %% \t流行度=%.4f' % \
                             (precision * 100, recall * 100, coverage * 100, popularity))

'''运行程序'''
if __name__ == '__main__':
    filename = 'ml-1m/ratings.dat'
    UserCF = UserBasedCF(20,10)
    UserCF.generate_data_set(filename)
    UserCF.calc_user_sim()
    UserCF.evaluate()
