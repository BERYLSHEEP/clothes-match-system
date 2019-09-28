class params:
	def __init__(self):

		self.max_num = 200

		self.save_fre = 500
		self.save_tf_idf_fre = 500

class  total_params(params):
	def  __init__(self):
		super().__init__()
		self.dim_items='dim_item(new).txt'
		#self.dim_items='dim_item_mini.txt'
		self.dim_fashion_matchsets='dim_fashion_matchsets(new).txt'
		self.new_fashion_matchsets='new_match_list.txt'

		self.fashion_catogory='fashion_catogory_list.txt'
		self.new_fashion_catogory = "new_fashion_catogory_list.txt"

		self.user_bought_history='user_bought_history.txt'
		self.fashion_catogory_list='fashion_catogory_list.txt'
		self.test_file='test_item(new).txt'

		self.tf_save = 'tf_save.txt'
		self.idf_save = 'idf_save.txt'
		self.tf_idf_save = 'tf_idf_save.txt'
		self.result_file='result.txt'

		self.model1_result_file = 'model1_result.txt'
		self.model2_result_file = 'model2_result.txt'
		self.model3_result_file = 'model3_result.txt'
		self.model_result_file='model_result.txt'
		self.match_result_list='match_result.txt'

		self.model1_save_fre = 100

		self.test = [29,119,414,43,413,424,3542,8144]
		#self.test = [29]


class mini_params(params):
	def __init__(self):
		super().__init__()
		file = 'mini_data/'
		self.dim_items=file+'dim_items_my.txt'
		self.dim_fashion_matchsets=file+'dim_fashion_match_sets_my.txt'
		self.fashion_catogory='fashion_catogory_list.txt'
		self.user_bought_history=file+'user_bought_history_my.txt'
		self.fashion_catogory_list=file+'fashion_catogory_list_my.txt'
		self.test_file=file+'test_item_my.txt'

		self.tf_save = file+'tf_save.txt'
		self.idf_save = file+'idf_save.txt'
		self.tf_idf_save = file+'tf_idf_save.txt'
		self.result_file= file+'result.txt'

if __name__ == '__main__':
	temp = mini_params()
	print(temp.save_fre)