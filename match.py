from math import  *
from numpy import *
from model2 import *
import pickle
from params import *
import time

num_pickle=500    #数据的批次
result_list=list()
par=total_params()
class Match():
	def __init__(self,id):

		self.item_dict=dict()     #商品搭配字典
		self.id=id                 #想要寻找商品a的搭配商品
		self.match_num=100        #选择搭配的商品数目
		#一些参数
		self.p = 4
		self.aa = 0.15
		self.bb = 1
		self.sim_dict=dict()    #相似度字典



	# 读入搭配数据,形成搭配表
	def build_match_dict(self,file):
		#items_dict=dict()     #存放搭配数据的字典 {id1：[match_id1,match_id2...],id2:[match_id1,match_id2...],...}

		with open(file,'r') as f:
			lines = f.readlines()
			x = 0
			for line in lines:
				line=line.split()  #按空格分开，将物品id和coll_id分开
				line=line[1]

				line=line.split(";") #按；分开，分开后的互相搭配

				for group in line:
					temp=list(line)
					temp.remove(group)
					group=group.split(",")
					i_list=[]
					for tem in temp:
						tem=tem.split(",")
						for i in tem:
							i_list.append(i)
					for i in group:
						if i in self.item_dict:
							t_list=self.item_dict[i]
							for j in i_list:
								if j not in t_list:
									self.item_dict[i].append(j)
						else:
							self.item_dict[i]=i_list
		#将更新搭配列表重新写入txt
		new_match_file = open(par.new_fashion_matchsets, 'w')
		for i in self.item_dict:
			new_match_file.write("%s\t" %i)
			for j in self.item_dict[i]:
				new_match_file.write("%s,"%j)
			new_match_file.write("\n")

	#计算待测商品与搭配表中所有商品的相似度，方便后面计算搭配度
	def get_sim_dict(self):
		for i in self.item_dict:
			sim_a_i=get_sim(str(self.id), str(i))
			#print(sim_a_i)
			self.sim_dict[i]=sim_a_i
		filename="sim_"+str(self.id)+".txt"
		f=open(filename,'w')
		for j in self.sim_dict:
			f.write("%s\t%s\n"%(j,self.sim_dict[j]))

	#fai函数
	#将搭配商品数用该函数进行转换
	def ff(self,x):
		# if x==0:
		# 	x=1
		return self.aa * math.log(x) + self.bb


#计算待测商品a和b的搭配度
	# 计算a,b的搭配度
	# sim 相似度
	# item_dict 搭配列表，记录每件商品与什么搭配
	def cal_match(self,b):
		#b的搭配商品集
		b_list=self.item_dict[b]
		#计算a和b的搭配集商品的相似度，以获取与b的搭配度
		sum=0
		n= len(self.item_dict[b])
		for i in b_list:
			n_i = len(self.item_dict[i])
			#sim_a_i=get_sim(str(self.id),str(i))
			# 计算a和i的相似度
			sim_a_i = self.sim_dict[i]
			sum += pow(sim_a_i / self.ff(n_i), self.p)

		f_b = self.ff(n)
		m_ab = f_b * (pow(sum, 1 / self.p))
		return m_ab

	#计算a与所有搭配集中商品的匹配度
	#返回最大的匹配度的物品
	def max_match(self):
		self.get_sim_dict()
		match_dict = dict()  #存放搭配度字典
		for b in self.item_dict:
			if b != self.id:
				#计算a和b的搭配度
				match_ab = self.cal_match(b)
				match_dict[b]=match_ab
		#排序
		temp = sorted(match_dict.items(), key=lambda x: x[1], reverse=True)
		n=0
		best_match=dict()

		for i in temp:
			best_match[i[0]]=i[1]
			n+=1
			if n>self.match_num:
				break
		return  best_match





#分批储存tf-idf
def divide_data(file):
	flag=0
	item_tf_idf = []
	with open(file,'rb') as f:
		#n=0
		child_file=0
		content=[]

		#一个批次一个批次的读
		for i in range(num_pickle):
			temp=pickle.load(f)

			for j in range(len(temp)):
				content.append(temp[j])
				if flag==0:
					item_tf_idf=temp[j]
					flag=1

			filename = "child_" + str(child_file) + ".txt"
			f2 = open(filename, 'wb')
			pickle.dump(content, f2)
			child_file += 1
			content = []
			f2.close()
		f.close()

		return child_file,item_tf_idf

	# 聚类的数据
def read_tf_idf(n):
	file = "child_" + str(n) + ".txt"
	f = open(file, 'rb')
	temp = pickle.load(f)
	tf_idf = dict()
	for i in temp:
		l = len(i)
		tf_idf[i[l - 1]] = i[:l - 1]
	return tf_idf





start=time.time()
id=input("请输入你想要寻找为此搭配的商品的id：")
a_match = Match(id)
a_match.build_match_dict(par.dim_fashion_matchsets)
model3=a_match.max_match()

f2=open(par.model3_result_file,'wb')
pickle.dump(model3,f2)

end=time.time()
runtime=end-start

print("程序运行时间1为： ",runtime)
#print(model3)
print("结束")



#逻辑：待预测商品a
#计算与搭配集所有商品的搭配度，根据该商品的搭配集商品与a的相似度用相关公式进行计算
#选出搭配度最大的前100件商品为搭配子集
