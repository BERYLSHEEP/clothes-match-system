# coding: utf-8
from params import *
import math
import time
import pickle

params=total_params()

class user_bought_history(object):
	"""docstring for user_bought_history"""
	def __init__(self):
		self.user_bought_history=[]
		#	user_id			item_id			creat_at
		self.item_catogory={}
		#key:item_id		value:catogory value
		self.result={}
		#key: item_id 	value: frequency
		self.fashion_catogory_list=[]
		#catogory 
		self.have_init = False


	def is_a_Day(self,time1,time2):
		if time1 is time2:
			return True
		else:
			return False

	def init_cal_file(self):
		#read file
		with open(params.user_bought_history,'r')as f:
			items = f.readlines()

			for line in items:
				item = line.split()
				self.user_bought_history.append(item)


		with open(params.dim_items,'r')as f:
			items = f.readlines()

			for line in items:
				item = line.split()
				self.item_catogory[item[0]]=item[1]



		with open(params.fashion_catogory_list,'r')as f:
			items = f.readlines()

			for line in items:
				item = line.split()
				self.fashion_catogory_list.append(item)

	def id_get_col(self,item_id):
		if not self.have_init:
			print("initialzing……")
			self.init_cal_file()
			self.have_init = True
		cat = self.item_catogory[item_id]	
		return cat

	def cal(self,item_id):
		self.result = {}
		users_times = []

		for history in self.user_bought_history:
			if item_id == history[1]:
				users_times.append(history)

		cat_A = self.item_catogory[item_id]
		for user_time in users_times:
			for history in self.user_bought_history:
				if user_time[0] == history[0] and user_time[2] == history[2] and user_time[1] != history[1]:
					cat_B = self.item_catogory[history[1]]
					if cat_A != cat_B :
						if history[1] in self.result:
						#cal the f_pm: the frequency that a,b hanppend toghter
							self.result[history[1]] += 1
						else:
							self.result[history[1]] = 1

		for key in self.result:
			cat_B = self.item_catogory[key]
			# cal the similarity between the catogory
			f_cm = 0
			for item in self.fashion_catogory_list:
				if cat_A in item and cat_B in item:
					f_cm += 1

			#cal total similarity
			f_pm = self.result[key]
			self.result[key] = f_pm * math.log(1+f_cm)
			#print("key:{0}, f_cm:{1}, f_pm:{2},result:{3}".format(key,f_cm,f_pm,self.result[key]))

		self.result = sorted(self.result.items(),key = lambda item:item[1],reverse = True)
		#print(self.result)
		return self.result

	def single_sim(self,term_id):
		if not self.have_init:
			print("initialzing……")
			self.init_cal_file()
			self.have_init = True
			print("finishing initialzing……")
		sim = s.cal(term_id)
		sim = dict(sim)
		if sim:
			sim = self.dict_normalize(sim)
		print(sim)
		return sim

	def dict_normalize(self,sim_dict):
		max_value = max(sim_dict.values())
		min_value = min(sim_dict.values())
		if max_value != min_value:
			for key in sim_dict:
				sim_dict[key] = (sim_dict[key] - min_value)/(max_value - min_value)
		return sim_dict



if __name__=='__main__':

	s = user_bought_history()
	result = []
	model_save_times = 0

	time1 = time.time()
	with open(params.model1_result_file, 'wb') as f:
		id = input("请输入你想要寻找为此搭配的商品的id：")
		sim = s.single_sim(str(id))
		pickle.dump(sim, f)
	# with open(params.model1_result_file,'wb') as f:
	# 	for index,item_id in enumerate(params.test):
	# 		print(item_id)
	# 		sim = s.single_sim(str(item_id))
	# 		result.append(sim)
	# 		if index and (index+1)%params.model1_save_fre == 0 or index == (len(params.test)-1) :
	# 			model_save_times += 1
	# 			#if model_save_times%1 == 0:
	# 			print("已经保存{0}次".format(model_save_times))
	# 			pickle.dump(result,f)
	# 			result = []
	'''
	s.init_cal_file()
	num = 0
	with open(params.result_file,'w') as result_file:
		with open(params.test_file,'r') as test_file:
			test_lines = test_file.readlines()

			for line in test_lines:
				item_id = line.split()[0]
				result = s.cal(item_id)
				result_file.write(item_id+' ')
				row = len(result)
				if row > params.max_num:
					row = params.max_num
				for index in range(0,row):
					result_file.write(result[index][0])
					if index == row-1:
						result_file.write('\n')
					else:
						result_file.write(',')

				break;
	'''
	time2 = time.time()
	time_elapsed = time2-time1
	print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
'''
				num += 1
				#if num % 10 == 0:
				print("finishing {0} lines".format(num))
'''

