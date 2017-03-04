#-*- coding: utf-8 -*-

import sys
import random
import math
from operator import itemgetter

random.seed(0)

''' 基于近邻用户的TopN推荐算法 - ItemBasedCF '''
class ItemBasedCF():


    # 初始化类
    def __init__(self, user_num, item_num, workSignal):
        
        self.trainset = {}      # 训练集
        self.testset = {}       # 测试集

        self.sim_item_num = user_num       # 相似用户数
        self.rec_item_num = item_num       # 推荐物品数

        self.workSignal = workSignal  # 输出信号

        self.item_sim_mat = {}      # 物品相似度矩阵
        self.item_popular = {}      # 物品流行度
        self.item_count = 0         # 总物品数

        self.workSignal.emit('相似用户数 = %d' % self.sim_item_num)
        self.workSignal.emit('推荐物品数 = %d' % self.rec_item_num)

    # 加载数据集文件，返回一个生成器
    def loadfile(self, filename):
        fp = open(filename, 'r')
        self.workSignal.emit('加载数据集: %s 中...' % (filename))
        for i, line in enumerate(fp):
            yield line.strip('\r\n')
        fp.close()
        self.workSignal.emit('加载数据集: %s 已完成' % (filename))
        self.workSignal.emit('数据集数据量为：%s ' % (i - 1))

    # 加载数据集，并将其划分为训练集和测试集
    def generate_data_set(self, filename, pivot=0.8):

        train_set_len = 0       # 训练集数据量
        test_set_len = 0        # 测试集数据量

        # 将数据集随机分为训练集和测试集
        for line in self.loadfile(filename):
            user, item, rating, _ = line.split('::')
            if (random.random() < pivot):
                self.trainset.setdefault(user, {})
                self.trainset[user][item] = int(rating)
                train_set_len += 1
            else:
                self.testset.setdefault(user, {})
                self.testset[user][item] = int(rating)
                test_set_len += 1

        self.workSignal.emit('生成训练集和测试集中...')
        self.workSignal.emit('生成训练集与测试集已完成')
        self.workSignal.emit('训练集数据量 = %s' % (train_set_len - 1))
        self.workSignal.emit('测试集数据量 = %s' % (test_set_len - 1))

    # 计算出物品相似度矩阵
    def calc_item_sim(self):

        com_users_num = self.item_sim_mat       # 物品共同用户数

        #计算物品总流行度
        self.workSignal.emit('计算总物品数和物品流行度中...')
        for user, ites in self.trainset.items():
            for item in ites:
                if item not in self.item_popular:
                    self.item_popular[item] = 0
                self.item_popular[item] += 1
        self.item_count = len(self.item_popular)
        self.workSignal.emit('计算总物品数和物品流行度已完成')
        self.workSignal.emit('物品总数量 = %d' % self.item_count)

        # 计算两个物品之间共同用户数
        self.workSignal.emit('建立物品之间相同用户数矩阵中...')
        for user, ites in self.trainset.items():
            for i in ites:
                for j in ites:
                    if i == j: continue
                    com_users_num.setdefault(i,{})
                    com_users_num[i].setdefault(j,0)
                    com_users_num[i][j] += 1
        self.workSignal.emit('建立物品之间相同用户数矩阵已完成')

        # 计算出物品之间相似度矩阵 
        self.workSignal.emit('建立物品之间的被喜好相似度矩阵中...')
        for i, related_ites in com_users_num.items():
            for j, count in related_ites.items():
                self.item_sim_mat[i][j] = count / math.sqrt(self.item_popular[i] * self.item_popular[j])
        self.workSignal.emit('建立物品之间的被喜好相似度矩阵已完成')

    # 找到K个最相似物品并且推荐N个物品，rating=用户对改物品的评分
    def recommend(self, user):

        rank = {}                   # 兴趣物品预测得分排名
        K = self.sim_item_num       # 相似物品数
        N = self.rec_item_num       # 推荐物品数
        interacted_ites = self.trainset[user]      # 用户已用物品集，需过滤不再推荐

        for item, rating in interacted_ites.items():
            for related_item, w in sorted(self.item_sim_mat[item].items(),key=itemgetter(1), reverse=True)[0:K]:
                if related_item in interacted_ites:
                    continue
                rank.setdefault(related_item, 0)
                rank[related_item] += w * rating
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    # 运行推荐函数，并评测算法，计算准确率，召回率，覆盖率和流行度
    def evaluate(self):

        hit = 0                 # 推荐物品命中次数
        rec_count = 0           # 推荐物品总次数
        test_count = 0          # 被推荐用户在测试集喜欢物品总次数
        popular_sum = 0         # 物品流行度总和
        all_rec_ites = set()   # 所有被推荐物品集合
        N = self.rec_item_num   # 对一个用户推荐物品数

        self.workSignal.emit('根据%d个最相似物品推荐%d个物品中...' % (self.sim_item_num, self.rec_item_num))
        for i, user in enumerate(self.trainset):
            test_ites = self.testset.get(user, {})
            rec_ites = self.recommend(user)
            for item, w in rec_ites:
                if item in test_ites:
                    hit += 1
                all_rec_ites.add(item)
                popular_sum += math.log(1 + self.item_popular[item])
            rec_count += N
            test_count += len(test_ites)
        self.workSignal.emit('根据%d个最相似用户推荐%d个物品已完成' % (self.sim_item_num, self.rec_item_num))

        self.workSignal.emit('评测该推荐系统各项指标中...')
        precision = hit / (1.0 * rec_count)                         # 准确率
        recall = hit / (1.0 * test_count)                           # 召回率
        coverage = len(all_rec_ites) / (1.0 * self.item_count)     # 覆盖率
        popularity = popular_sum / (1.0 * rec_count)                # 流行度
        self.workSignal.emit('评测该推荐系统各项指标已完成')
        self.workSignal.emit('准确率=%.2f %% \t召回率=%.2f %% \n覆盖率=%.2f %% \t流行度=%.4f' % \
                             (precision * 100, recall * 100, coverage * 100, popularity))

'''运行程序'''
if __name__ == '__main__':
    filename = 'ml-1m/ratings.dat'
    ItemCF = ItemBasedCF()
    ItemCF.generate_data_set(filename)
    ItemCF.calc_item_sim()
    ItemCF.evaluate()
