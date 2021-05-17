import re
from mechanize import Browser

import mechanize
import urllib3

import random

fields = {'title': ['', 'test'], 'type':[0,1,2], 'checkbox':[0,1], 'submit':[0,1]}






class Enviroment:
	def __init__(self):
		#self.fields = fields
		self.states = {}
		self.status_submit = '0'
		self.http_response = ''

		self.browser = Browser()
		self.browser.open("http://localhost:8080/test_suite")
		self.browser.select_form(nr=1)
		self.tipos = self.browser.form.possible_items("type")

	def initialize(self):
		self.browser = Browser()
		self.browser.open("http://localhost:8080/test_suite")
		self.browser.select_form(nr=1)
		self.tipos = self.browser.form.possible_items("type")
		self.status_submit = '0'
		self.http_response = ''


	def apply_action(self,action):

		if action == 0:
			self.browser['title'] = ''
			self.status_submit = '0'

		elif action == 1:
			self.browser['title'] = 'Prueba'
			self.status_submit = '0'
		elif action == 2:
			self.browser.find_control("checkbox").items[0].selected = False
			self.status_submit = '0'

		elif action == 3:
			self.browser.find_control("checkbox").items[0].selected = True
			self.status_submit = '0'

		elif action == 4:
			self.browser.set(True, self.tipos[0] , "type")
			self.status_submit = '0'

		elif action == 5:
			self.browser.set(True, self.tipos[1] , "type")
			self.status_submit = '0'

		elif action == 6:
			self.browser.set(True, self.tipos[2] , "type")
			self.status_submit = '0'

		elif action == 7:
			self.status_submit = '1'

			#just submit if all fields are filled
			if self.browser['title'] != '' and self.browser['type'][0] != '0' and len(self.browser['checkbox'])!=0:
				try:
					response = self.browser.submit()
					#print('after submit')
					#content = response.read()
					code = response.code
					#print(code)
					self.http_response = code
				except mechanize.HTTPError as e:
					#print('Error:', e)
					self.http_response = 500



	def get_current_state(self):

		if self.browser['title'] == '':
			val_tit = '0'

		else:
			val_tit = '1'

		if len(self.browser['checkbox'])==0:
			val_che = '0'
		else:
			val_che = '1'

		if self.browser['type'][0] == '0':
			val_typ = '0'

		elif self.browser['type'][0] == '1':
			val_typ = '1'

		elif self.browser['type'][0] == '2':
			val_typ = '2'


		state = val_tit+val_che+val_typ+self.status_submit
		#0110
		return state


	def get_all_possible_actions(self):
		actions = [0,1,2,3,4,5,6,7]
		return actions

	def get_next_state(self,action):
		#(0110, 2)
		self.apply_action(action)
		if action ==7:
			return '0000'
		else:
			return self.get_current_state()





environment_matrix = {'0000':[0,0,0,0,0,0,0,0],'0010':[0,0,0,0,0,0,0,0],'0020':[0,0,0,0,0,0,0,0],'0100':[0,0,0,0,0,0,0,0],
'0110':[0,0,0,0,0,0,0,0],'0120':[0,0,0,0,0,0,0,0],'1000':[0,0,0,0,0,0,0,0],'1010':[0,0,0,0,0,0,0,0],'1020':[0,0,0,0,0,0,0,0],
'1100':[0,0,0,0,0,0,0,0],'1110':[0,0,0,0,0,0,0,100],'1120':[0,0,0,0,0,0,0,100],'0001':[0,0,0,0,0,0,0,0],'0011':[0,0,0,0,0,0,0,0],
'0021':[0,0,0,0,0,0,0,0],'0101':[0,0,0,0,0,0,0,0],'0111':[0,0,0,0,0,0,0,0],'0121':[0,0,0,0,0,0,0,0],'1001':[0,0,0,0,0,0,0,0],
'1011':[0,0,0,0,0,0,0,0],'1021':[0,0,0,0,0,0,0,0],'1101':[0,0,0,0,0,0,0,0],'1111':[0,0,0,0,0,0,0,0],'1121':[0,0,0,0,0,0,0,0]}




q_matrix_trained = {'0000':[0,10,0,10,0,10,10,0],'0010':[0,10,0,10,0,0,10,0],'0020':[0,10,0,10,0,10,0,0],'0100':[0,10,0,0,0,10,10,0],
'0110':[0,10,0,0,0,0,10,0],'0120':[0,10,0,0,0,10,0,0],'1000':[0,0,0,10,0,10,10,0],'1010':[0,0,0,10,0,0,10,0],'1020':[0,0,0,10,0,10,0,0],
'1100':[0,0,0,0,0,10,10,0],'1110':[0,0,0,0,0,0,10,100],'1120':[0,0,0,0,0,10,0,100],'0001':[0,10,0,10,0,10,10,0],'0011':[0,10,0,10,0,0,10,0],
'0021':[0,10,0,10,0,10,0,0],'0101':[0,10,0,0,0,10,10,0],'0111':[0,10,0,0,0,0,10,0],'0121':[0,10,0,0,0,10,0,0],'1001':[0,0,0,10,0,10,10,0],
'1011':[0,0,0,10,0,0,10,0],'1021':[0,0,0,10,0,10,0,0],'1101':[0,0,0,0,0,10,10,0],'1111':[0,0,0,0,0,0,0,0],'1121':[0,0,0,0,0,0,0,0]}


def testing(entorno):
	discount = 0.9
	learning_rate = 0.1
	entorno.initialize()
	# get starting place
	cur_pos, action = random.choice(list(environment_matrix.items()))
	# while goal state is not reached
	counter = 0
	while(entorno.http_response == ''):
		counter = counter +1
		# get all possible next states from cur_step
		possible_actions = entorno.get_all_possible_actions()
		# select any one action randomly
		max_value = max(q_matrix_trained[cur_pos])
		action = max_index = q_matrix_trained[cur_pos].index(max_value)
		# find the next state corresponding to the action selected
		next_state = entorno.get_next_state(action)
		# update the q_matrix
		# go to next state
		cur_pos = next_state
		print('Estado Actual:',cur_pos)

	print('Estatus HTTP: ', entorno.http_response)	
	print('Iteraciones: ', counter)

entorno = Enviroment()

testing(entorno)




