import re
from mechanize import Browser

import mechanize
import urllib3

import random

text = 'aaaa'
number = 9

fields_1 = {'check':[0,1], 'type':[0,1,2,3,4]}
fields_1_1 = {'check':[0,1], 'type':[0,1,2,3,4,5]}
fields_1_1_1 = {'check':[0,1], 'type':[0,1,2,3,4,5,6]}
fields_1_1_2 = {'check':[0,1], 'type':[0,1,2,3,]}
fields_1_1_1_1 = {'check':[0,1], 'type':[0,1,2,3,4,5,6,7]}

fields_1_2 = {'check':[0,1], 'type':[0,1,2,3,4,5,6]}
fields_1_2_1 = {'check':[0,1], 'type':[0,1,2,3,4]}



#get URL to visit, initial page


#text= fix
#number =  fix
#check = [1,2] fix
#get options for type


#estado/nodo
    #dato
    #prev_node

    #field1=none
    #field2=none
    #field3=none
    #field4=none
    

#path
    #self.root = None

    #def append
    #   append node 


#recreate_state(estado):
    #append nodos en un stack, de atras al principio, el principio quedara hasta arriba
    #ir a page 1
    #recrear estado, llenando form de arriba del stack hacia abajo
    



#function set_submit_form(url, last_state):
    #recreate_state(estado)
    #get Form of page  
    #get options for type
    
    

    #for ty in type:
        #for ch in checkbox:
            #set text = 'aaa'
            #set number = 10
            #set checkbox = ch
            #set type = ty

            #current_state= create estado antes de submit
            #current_state.prev_node = last_state

            #submit
            #newurl = submit.url
            #if url  = 400 or 500: 
                #return
            #else
                #set_submit_form(newurl, current_state)



#create path

#function set_submit_form(url, root_state)

        








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




entorno = Enviroment()

#testing(entorno)

#training(entorno)








