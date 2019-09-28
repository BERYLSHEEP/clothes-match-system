from params import *
import math
import time
import pickle
import os

#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt

params = total_params()


class tfIdf(object):
    def __init__(self):
        # dictory : documents' number that have this term
        # {term1:2,term:10}=>term1词出现在两个文档中
        self.term_dict = {}
        self.dict_index = {}
        # 对应商品id号的标题分词
        self.cloth_items = []
        # 商品的id号
        self.items_id = []
        # 保存的tf次数
        self.tf_times = 0
        # 保存的idf次数
        self.idf_times = 0
        self.idf = []
        self.have_idf = 0
        self.have_dict = 0

    # 建立词表
    def build_dict(self):
        with open(params.dim_items, 'r') as f:
            lines = f.readlines()
            for line in lines:
                temp = line.split()
                if len(temp) == 2:
                    print(line)
                fenci = temp[2]
                self.items_id.append(temp[0])
                items = fenci.split(',')
                self.cloth_items.append(items)
                flag = []
                for item in items:
                    if item not in self.term_dict:
                        self.term_dict[item] = 1
                    elif item not in flag:
                        self.term_dict[item] += 1
                    flag.append(item)

        new_dict = {}
        index = 0
        for term in self.term_dict:
            # 注意要修改去掉少用的词  total_params = 4
            if self.term_dict[term] > 4:
                new_dict[term] = self.term_dict[term]
                self.dict_index[term] = index
                index += 1

        self.term_dict = new_dict

        # print(len(self.term_dict))

        # 画图，查看词表的词频规律
        '''
        max_num = 20
        total = len(self.term_dict)
        X=[i for i in range(1,max_num)]
        Y=[]
        for i in X:
            num = self.cal_dict_times(i)
            Y.append(num)
            total -= num
            print("词表出现{0}次的单词有{1}个".format(i,num))

        #print("词表出现11词及以上的单词有{0}个".format(total))

        #画一个柱状图来显示词表的单词出现次数

        X.append(max_num)
        Y.append(total)
        fig = plt.figure()
        plt.bar(x = X, height = Y, color="green")
        plt.xlabel("term accur times")
        plt.ylabel("term number")
        plt.title("term distribution")


        plt.show()  
        '''

    # 统计词典只出现一次的词的个数
    def cal_dict_times(self, times):
        num = 0
        for item in self.term_dict:
            if self.term_dict[item] == times:
                num += 1

        return num

    def cal_tf(self):
        terms_vector = []
        with open(params.tf_save, 'wb') as f:
            for cloth in range(len(self.cloth_items)):
                term_vector = self.single_tf(cloth)
                #				if term_vector != 0:
                terms_vector.append(term_vector)
                if cloth and (cloth + 1) % params.save_fre == 0 or cloth == (len(self.cloth_items) - 1):
                    # print(terms_vector)
                    self.tf_times += 1
                    if self.tf_times % 10 == 0:
                        print("已经保存{0}次".format(self.tf_times))
                    pickle.dump(terms_vector, f)
                    terms_vector = []

    def cal_idf(self):
        N = len(self.cloth_items)
        # print(N)
        terms_vector = []
        with open(params.idf_save, 'wb') as f:
            for term in self.term_dict:
                # print(self.term_dict[term])
                idf = math.log((N / (self.term_dict[term] + 1)) + 1)
                terms_vector.append(idf)
            pickle.dump(terms_vector, f)
        # print(terms_vector)

    def cal_tf_idf(self):
        tf_idf = {}
        items_index = 0
        if os.path.getsize(params.tf_save) > 0:
            # print(params.tf_save + " is not empty")

            with open(params.idf_save, 'rb') as idf_File:
                with open(params.tf_save, 'rb') as tf_File:
                    with open(params.tf_idf_save, 'wb') as tf_idf_File:
                        idf = pickle.load(idf_File)
                        for i in range(self.tf_times):
                            tf = pickle.load(tf_File)
                            # print("tf's lenghth = {0}".format(len(tf)))
                            for tf_item in range(len(tf)):
                                temp = [a * b for a, b in zip(idf, tf[tf_item])]
                                tf_idf[self.items_id[items_index]] = temp
                                items_index += 1
                                if tf_item and (tf_item + 1) % params.save_tf_idf_fre == 0 or tf_item == (len(tf) - 1):
                                    pickle.dump(tf_idf, tf_idf_File)
                                    tf_idf = {}

    def single_id_tf(self, cloth_id):
        index = self.items_id.index(cloth_id)
        term_vector = self.single_tf(index)
        return term_vector

    def load_idf(self):
        with open(params.idf_save, 'rb') as idf_File:
            self.idf = pickle.load(idf_File)  

    def judge_init(self):
        if self.have_dict == 0:
            self.build_dict()
            print("building dictory")
            self.have_dict = 1
        if self.have_idf == 1:
            self.load_idf()
            print("loading idf")
            self.have_idf = 1         

    def single_tf_idf(self, cloth_id):
        self.judge_init()
        term_tf = self.single_id_tf(cloth_id)
        term_tf_idf = [a * b for a, b in zip(self.idf, term_tf)]
        return term_tf_idf

    def single_tf(self, index):
        term_vector = [0 for i in range(len(self.term_dict))]
        for item in self.cloth_items[index]:
            if item in self.term_dict:
                index = self.dict_index[item]
                term_vector[index] += 1
        N = sum(term_vector)
        if N == 0:
            print("序号为{0}的商品标题与其他商品都没有大的相似性".format(index))
        # 处理，不要没有太大相关性的商品？
        #			self.items_id[index] = -1
        #			term_vector = 0
        else:
            term_vector = [term / N for term in term_vector]
        return term_vector

    def dot_product(self, v1, v2):
        return sum(a * b for a, b in zip(v1, v2))

    def magnitude(self, v1):
        return math.sqrt(self.dot_product(v1, v1))

    def similarity(self, v1, v2):
        return self.dot_product(v1, v2) / (self.magnitude(v1) * self.magnitude(v2) + 0.000000000001)

    def sort(self, simi):
        simi = sorted(simi.items(), key=lambda item: item[1], reverse=True)
        return simi[:100]

    def sim(self, term_id):
        # match the term_id
        index = self.items_id.index(term_id)
        # single calculate tf_idf
        search_tf = self.single_tf(index)

        self.judge_init()

        search_tf_idf = [a * b for a, b in zip(search_tf, self.idf)]

        simi = {}
        with open(params.tf_idf_save, 'rb') as tf_idf_File:
            for time in range(self.tf_times):
                tf_idf = pickle.load(tf_idf_File)
                print(len(tf_idf))
                for items in range(len(tf_idf)):
                    ii = time * params.save_tf_idf_fre + items
                    if time != 0:
                        ii += 1
                    if ii != index:
                        # print(tf_idf[self.items_id[ii]])
                        if self.items_id[ii] not in tf_idf:
                            print(self.items_id[ii])
                            print(ii)
                        simi[self.items_id[ii]] = self.similarity(search_tf_idf, tf_idf[self.items_id[ii]])
                simi = self.sort(simi)
                simi = dict(simi)
        return simi

