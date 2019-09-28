from tf_idf import *
import numpy as np

s = tfIdf()

# 载入模型
with open('train.pkl', 'rb') as f:
    km = pickle.load(f)


# 根据商品id得到tf_idf
def get_tf_idf(item_id):
    tf_idf = s.single_tf_idf(item_id)

    return tf_idf


# 得到tf_idf所在的类别
def get_cluster(tf_idf):
    X = np.array(tf_idf)
    y_pred = km.predict([X])
    # 返回类别
    return y_pred[0]


# 计算两个商品相似度
def get_sim(id1, id2):
    tf_idf1 = get_tf_idf(id1)
    tf_idf2 = get_tf_idf(id2)
    sim = s.similarity(tf_idf1, tf_idf2)
    return sim


def model2(id):
    #
    print(id)
    search_tf_idf = get_tf_idf(id)
    id_cluster = get_cluster(search_tf_idf)

    # 对应类文件
    file_name = 'cluster_file/tf_idf_save' + str(id_cluster + 1) + '.txt'
    print(file_name)

    # 加载该类别文件的批次数量
    with open('cluster_file_pickle.txt', 'rb') as f:
        cluster_file_pickle = pickle.load(f)

    # 计算相似度
    simi = {}

    print(cluster_file_pickle[id_cluster])

    with open(file_name, 'rb') as f:
        for i in range(cluster_file_pickle[id_cluster]):
            tf_idf = pickle.load(f)
            for item in range(len(tf_idf)):
                t = tf_idf[item]
                key = t[-1]
                del t[-1]
                simi[key] = s.similarity(search_tf_idf, t)
            simi = s.sort(simi)
            # print(simi)
            simi = dict(simi)
        # print(simi)

    # simi排序
    print(s.sort(simi))


if __name__=='__main__':
    id=input("请输入你想要寻找为此搭配的商品的id：")
    model2(str(id))

