
#from match import *
from model1 import *
from params import *

import pickle
	#模型融合
def gather(modelA,modelB,modelC,w1,w2,match_num):
	w3=1-w1-w2
	model=dict()
	size=len(modelA)
	for a in modelA:
		model[a]=w1*modelA[a]
		if a in modelB:
			model[a]+=w2*modelB[a]
			del modelB[a]
			if a in modelC:
				model[a]+=w3*modelC[a]
				del modelC[a]
	for b in modelB:
		model[b]=w2*modelB[b]
		if b in modelC:
			model[b]+=w3*modelC[b]
			del modelC[b]
	for c in modelC:
		model[c]=w3*modelC[c]
	# 按匹配度排序
	temp = sorted(model.items(), key=lambda x: x[1], reverse=True)
	n=0
	best_match = dict()
	for i in temp:
		best_match[i[0]] = i[1]
		n += 1
		if n > match_num:
			break
	return best_match

#读入类间搭配表
def read_cat(file):
	f=open(file,'r')
	item_cat=dict()
	lines=f.readlines()
	for line in lines:
		id=line[0]
		line=line[1:]
		item_cat[id]=line


	return item_cat
#过滤模型子集
def filter(model2,id):
	user=user_bought_history()
	par = total_params()
	item_cat=read_cat(par.new_fashion_catogory) #类间搭配表
	cot=user.id_get_col(str(id))
	if cot in item_cat:
		i_list=item_cat[cot]
		for i in model2:
			if i not in i_list:
				model2[i]*=0.1
	return model2

#读每个模型的结果
def read_match(file):
	f=open(file,"rb")
	model=pickle.load(f)
	return model

#id：待测商品id,w1,w2权重，num:想要选择的搭配商品数目
def final(par,id,w1,w2,num):
	#文件中只有一个待测id的搭配数据
	model1 = read_match(par.model1_result_file)
	model2 = read_match(par.model2_result_file)
	model3 = read_match(par.model3_result_file)
	model_1 = model1
	model_2 = filter(model2, id)
	model_3 = filter(model3, id)
	#model是一个字典 {id1:m1,id2:m2...}
	model = gather(model_1, model_2, model_3, w1, w2, num)
	return model

if __name__ == "__main__":
	#测试运行时间
	start = time.time()

	par = total_params()
	id=input("输入待测商品id:")
	model=final(par,id,0.4,0.3,100)
	f=open(par.model_result_file,'wb')
	pickle.dump(model,f)
	f2=open(par.match_result_list,'w')
	f2.write("%s\t" % id)
	for j in model:
		f2.write("%s " % j)
	end = time.time()
	p1 = time.process_time()
	c1 = time.perf_counter()
	runtime = end - start

	print("程序运行时间为： ", runtime)

