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



q_matrix = {'0000':[0,0,0,0,0,0,0,0],'0010':[0,0,0,0,0,0,0,0],'0020':[0,0,0,0,0,0,0,0],'0100':[0,0,0,0,0,0,0,0],
'0110':[0,0,0,0,0,0,0,0],'0120':[0,0,0,0,0,0,0,0],'1000':[0,0,0,0,0,0,0,0],'1010':[0,0,0,0,0,0,0,0],'1020':[0,0,0,0,0,0,0,0],
'1100':[0,0,0,0,0,0,0,0],'1110':[0,0,0,0,0,0,0,0],'1120':[0,0,0,0,0,0,0,0],'0001':[0,0,0,0,0,0,0,0],'0011':[0,0,0,0,0,0,0,0],
'0021':[0,0,0,0,0,0,0,0],'0101':[0,0,0,0,0,0,0,0],'0111':[0,0,0,0,0,0,0,0],'0121':[0,0,0,0,0,0,0,0],'1001':[0,0,0,0,0,0,0,0],
'1011':[0,0,0,0,0,0,0,0],'1021':[0,0,0,0,0,0,0,0],'1101':[0,0,0,0,0,0,0,0],'1111':[0,0,0,0,0,0,0,0],'1121':[0,0,0,0,0,0,0,0]}



q_matrix_trained = {'0000': [112.91211887817714, 123.42509973074664, 114.45320164075915, 112.64657647930915, 105.01542303394667, 106.53756442618592, 113.82446988023189, 105.30422462269061], '0010': [87.84528184317026, 125.84476854764671, 96.5320821417835, 107.67286760280379, 92.88182401961112, 93.12496269409914, 103.23370390503752, 97.62024880369559], '0020': [101.47927588963859, 127.9512682065136, 103.64700740432593, 113.2361379493344, 98.44529691470302, 95.4946334698056, 103.18595961416776, 100.55695569445706], '0100': [93.96475099916917, 124.56161093782839, 95.44867129984608, 93.37693207216097, 99.60930794450302, 97.82067183142516, 106.79122500997285, 91.03945665335742], '0110': [101.98074631037369, 144.5500507247492, 89.20440766095807, 107.9172593064893, 86.42252937335974, 107.96491891150413, 103.25352913144606, 96.37138692592376], '0120': [100.86752840525699, 147.18503933996172, 96.91440089429541, 106.35509242476454, 82.76769776012154, 104.30608200325976, 107.57074716126239, 97.53786479636943], '1000': [88.01917680039824, 96.6496886305511, 98.6687159512642, 124.87489139524915, 97.52539607064722, 123.4458515061685, 125.4139151634108, 96.17701106445399], '1010': [86.50104405778778, 126.90297443529255, 123.0255393688361, 156.3289165953722, 100.00724556363018, 119.89755972904166, 124.1429784616353, 90.66636908265181], '1020': [106.29578279560485, 123.22677222438745, 125.08543844440678, 149.01418627284778, 98.42041129628709, 123.31666942347053, 122.94676048569653, 98.4161832662619], '1100': [87.03760303835271, 122.81764471469535, 95.87588469725803, 118.93364091379814, 127.28175432056892, 154.27236485047766, 141.75238197110122, 67.47711335954641], '1110': [108.62716838211915, 152.00140973158415, 125.0084692822856, 145.72593761509611, 114.60057728309665, 146.56536894991868, 153.5584096907264, 186.00507982921673], '1120': [110.61094886293017, 138.40456362976104, 121.22943002902863, 147.74749475200065, 112.91663677352385, 150.86607212980934, 150.17212540941466, 186.52946004484528], '0001': [0, 0, 0, 10.291272498251532, 0, 9.228824290848157, 9.728335890249129, 0], '0011': [0, 0, 4.640271023194053, 0.12444040235426017, 0, 0, 0, 0], '0021': [0, 0, 2.0282019997429592, 0, 2.627598872103462, 0, 1.0602088228521995, 0], '0101': [0, 0, 6.556308094614342, 6.15882531764446, 0, 0.5068373040693684, 0, 0.5274454688615021], '0111': [0, 12.593904990937606, 0, 0.055938364290000014, 0, 0, 8.080322108274158, 5.410619370682575], '0121': [10.066863510692626, 4.009564219265456, 0, 0, 0.139239, 6.926926658776961, 0, 0], '1001': [0.22520238264900008, 0, 0, 0, 0, 0, 0, 3.0835581124115556], '1011': [0, 6.319920089307299, 0, 0, 3.1449611502199097, 0, 0.2956347703060567, 0], '1021': [0.14661, 0, 0.6023246893863793, 0, 0, 0, 1.324564562111751, 12.207864955240865], '1101': [9.167313224715711, 0, 1.7640976744505268, 0, 0, 0, 8.455402692163043, 0], '1111': [0.9507595235790149, 7.648007270970777, 0, 1.0653897586711192, 0.2696855778773602, 0, 0, 0], '1121': [7.505362679437382, 13.480462240048684, 10.327993586590727, 6.314168315559062, 0, 13.838517635338505, 0, 2.3701648419294203]}

def training(entorno):
	discount = 0.9
	learning_rate = 0.1
	for _ in range(1): #cambiar numero de epocas de entrenamiento
		#inicializar entorno en cada epoca
		entorno.initialize()

		#obtener un estado de forma aleatoria.
		cur_pos, action = random.choice(list(environment_matrix.items()))
		counter = 0
		#mientras no se envie el formulario
		while(entorno.http_response == ''):
			counter = counter +1
			# obtener todas las acciones posibles a aplicar
			possible_actions = entorno.get_all_possible_actions()
			# seleccionar una acción de forma aleatoria
			#TODO check, it seems that every step a random action is selected, we are lacking explotation with gama 
			action = random.choice(possible_actions)
			# obtener el siguiente estado en base a la acción seleccionada
			next_state = entorno.get_next_state(action)
			# actualizar la matriz Q
			q_matrix[cur_pos][action] = q_matrix[cur_pos][action] + learning_rate * (environment_matrix[cur_pos][action] + 
				discount * max(q_matrix[next_state]) - q_matrix[cur_pos][action])
			# actualizar estado actual
			cur_pos = next_state
			print('Estado Actual:',cur_pos)
		print('Estatus HTTP: ', entorno.http_response)
		print('Iteraciones: ', counter)
		print("Episodio ", _ , " done")
	print(q_matrix)
	print("Entrenamiento Terminado..")


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

#training(entorno)








