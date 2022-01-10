import re
from mechanize import Browser

import mechanize
import urllib3

import random

#import sys
#sys.setrecursionlimit(100000)

import json

class State:
	def __init__(self, id, text, number, check, type, url, error_code):
		#form state variables 
		self.text = text
		self.number = number
		self.check = check
		self.type = type
		#reference to prev node
		self.prev_node = None
		self.id = id
		self.url =  url
		self.error_code = error_code
		#TODO add branches references to build tree




class Path:
	def __init__(self):
		#reference to path root node 
		self.root = None
		self.nodes_counter = 0

	#append new elements to path method
	def append(self, id, prev_state, text, number, check, type, url, error_code):
		#create new state

		
		new_state = State(self.nodes_counter, text, number, check, type, url, error_code)
		self.nodes_counter = self.nodes_counter +1
		
		#check if path root is None (it means theresn't a root path already set)
		#here prev_state would be None, because is the first node without a previous node
		#print('prev node id: ', new_state.id)
		if self.root == None:
			#if there is not a root path already set, asign state as root node
			self.root = new_state
			return new_state
		else:
			#if root node already exist then next nodes have to reference to prev node because is a reverse reference
			#the new state we are creating is referenced to the previous one 
			new_state.prev_node = prev_state
			return new_state

class Node:
    def __init__(self, data):
        self.data = data
        self.next_node = None

class Stack:
	def __init__(self):
		self.head = None
	
	def push(self, state):
		new_node = Node(state)
		if self.head == None:
			self.head = new_node
		else:
			prev_head = self.head
			self.head =  new_node
			new_node.next_node = prev_head
	
	def pop(self):
		if self.head != None:
			last_node = self.head
			#print(last_node.data)
			self.head = last_node.next_node
			return last_node.data
		else:
			#print('None')
			return None
	
	#function to check if stack is empty
	def empty(self):
		#print('entro check if empty')
		if self.head == None:
			
			return True
		else:
			return False
	
	#print elements of linked list
	def print_list(self):
		if self.head != None:
			current_node = self.head
			while current_node != None:
				#print(current_node.data.url)
				print(current_node.data)
				current_node = current_node.next_node
	

	#print elements of linked list
	def print_errors(self):
		if self.head != None:
			current_node = self.head
			while current_node != None:
				print('--- error branch ---- ')
				#print(current_node.data.url)
				#print(current_node.data)
				local_stack =  current_node.data

				if local_stack.head != None:
					local_current_node = local_stack.head
					while local_current_node != None:
						print('********')
						print('ID', local_current_node.data.id)
						print('Error', local_current_node.data.error_code)
						print(local_current_node.data.url)
						print('Text', local_current_node.data.text)
						print('Number', local_current_node.data.number)
						print('Check', local_current_node.data.check)
						print('Type', local_current_node.data.type)
						print('********')

						#print(current_node.data)
						local_current_node = local_current_node.next_node

				current_node = current_node.next_node

	def build_json(self):
		data = []

		if self.head != None:
			current_node = self.head
			while current_node != None:
				branch = []
				print('--- error branch ---- ')
				#print(current_node.data.url)
				#print(current_node.data)
				local_stack =  current_node.data

				if local_stack.head != None:
					local_current_node = local_stack.head
					while local_current_node != None:

						nodo = dict()

						nodo['id'] = local_current_node.data.id
						nodo['error'] = local_current_node.data.error_code
						nodo['url'] = local_current_node.data.url
						nodo['text'] = local_current_node.data.text
						nodo['number'] = local_current_node.data.number
						nodo['check'] = local_current_node.data.check
						nodo['type'] = local_current_node.data.type

						branch.append(nodo)


						#print(current_node.data)
						local_current_node = local_current_node.next_node

				data.append(branch)
				current_node = current_node.next_node



		return data






#function to recreate state on every step in order continue testing fordward last state
#state: desire state to recreate, entorno: entorno to testing, operate web page to reach desire state
def recreate_state(state, entorno):
	#create an stack where is stored from the current state to previous node before root
	stack = Stack()
	#asign state to current state (desire state to recreate)
	current_state = state
	#iterate until get a node before root
	while current_state.prev_node!=None:
		stack.push(current_state)
		current_state = current_state.prev_node

	print('- - - - - - Entro Stack recreate State')
	#print('Estado Head:', stack.head)
	#stack.print_list()
	print('---fin lista urls')
	#initialize entorno, get root url
	entorno.initialize()
	#build each state, pop last stack element and recreate state
	if stack.head != None:
		#review if this is empty 
		print('....... is stack empty? recreate: ', stack.empty())
		while stack.empty()!=True:
			print('Ingreso if stack empty: ')
			#get_next_form(entorno.url, stack)
			#reload page, get form of new page
			entorno.browser.open(entorno.browser.geturl())
			entorno.reload()
			#get first state before root
			state_last = stack.pop()
			#get tipos of current form page
			#entorno.tipos = entorno.browser.form.possible_items("type")
			entorno.browser['title'] = state_last.text
			entorno.browser['cantidad'] = state_last.number
			if state_last.check == 'on':
				entorno.browser.find_control("boleano").items[0].selected = True
			else:
				entorno.browser.find_control("boleano").items[0].selected = False
			entorno.browser.set(True, state_last.type , "tipo")

			entorno.status_submit = '1'
			#submit form
			try:
				response = entorno.browser.submit()
				#print('after submit')
				#content = response.read()
				code = response.code
				#print(code)
				entorno.http_response = code
				if entorno.http_response == 200:
					#TODO verify if is necesary go to URL
					#url = response.geturl()
					#return
					entorno.reload()
					print('¿¿***¿¿¿----- URL actual')
					print(entorno.browser.geturl())
					print('===== se avanzo para pasar de pagina')
					#pass

			except mechanize.HTTPError as e:
				print('Error recreate state:', e)
				#entorno.http_response = 500
				#capture error?
				#return
		print('===== Finalizo While entrar pagina')



def build_error_chain(state, global_error_stack):

	#global_error_stack.push(state)
	#create an stack where is stored from the current state to previous node before root
	local_error_stack = Stack()
	#asign state to current state
	current_state = state
	#iterate until get a node before root
	while current_state.prev_node!=None:
		local_error_stack.push(current_state)
		current_state = current_state.prev_node
	
	global_error_stack.push(local_error_stack)



def set_submit_form(entorno, last_state, numr, new_path, global_error_stack):
	print(';;;;;;;;; Entro Set Submit Form')
	recreate_state(last_state, entorno)
	#if stack vacio no se recrea nada
	#fill current state
	#entorno.initialize()
	print('¿¿***¿¿¿----- URL actual para Submit')
	print(entorno.browser.geturl())
	entorno.tipos = entorno.browser.form.possible_items("tipo")

	print('Tipos Entorno: ', entorno.tipos)
	cp_tipos = entorno.tipos

	#TODO replace these for by states tables and translate to from actions
	for ty in cp_tipos:
		for ch in ['on', 'off']:
			#recreate state
			print('recreate state inside for')
			recreate_state(last_state, entorno)
			print('--- Error debug before error: ', entorno.browser.geturl())
			entorno.browser.open(entorno.browser.geturl())
			#print(entorno.browser.title())
			entorno.reload()
			#entorno.tipos = entorno.browser.form.possible_items("type")
			#reload page to clean fields and test other combinations
			#initialize browser to load form again also get tipos again
			print('--- Entro Submit')
			print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ',cp_tipos)
			print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Type :', ty)
			print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Check :', ch)
			
			#entorno.reload()
			text = entorno.text
			number = entorno.number
			entorno.browser['title'] = entorno.text
			entorno.browser['cantidad'] = entorno.number
			if ch == 'on':
				entorno.browser.find_control("boleano").items[0].selected = True
			else:
				entorno.browser.find_control("boleano").items[0].selected = False

		

			entorno.browser.set(True, ty, "tipo")
			entorno.status_submit = '1'

			#create new state on every different submition data, save URL with each state

			current_state = new_path.append(last_state.id, last_state, text, number, ch, ty, entorno.browser.geturl(), '200')
			#submit form
			try:
				print('-----try to submit')
				print('Recursion number:', numr, current_state.url)
				
				response = entorno.browser.submit()
				
				#print('after submit')
				#content = response.read()
				code = response.code
				#print(code)
				entorno.http_response = code
				if entorno.http_response == 200:
					print('--- URL New before recursive: ', entorno.browser.geturl())
					print('**** call recursive')
					numr = numr +1
					#print('---- debug error: ', current_state.id, current_state.url)
					#current_state.error_code = "200"
					#build_error_chain(current_state)
					set_submit_form(entorno, current_state, numr, new_path, global_error_stack)
					

			except mechanize.HTTPError as e:
				error = str(e)
				print('-------------- *Error:',error)
				print('aqui va el error')
				if error == 'HTTP Error 400: Bad Request':
					print('got error 400')
					current_state.error_code = "400"
					build_error_chain(current_state, global_error_stack)
					#build_error_chain('error 400')
				elif error == 'HTTP Error 500: Internal Server Error':
					print('got error 500')
					current_state.error_code = "500"
					build_error_chain(current_state, global_error_stack)

				#entorno.http_response = 500
				#TODO capture error?
				#return

#TODO UPDATE URL en entorno para saber en donde esta.

class Enviroment:
	def __init__(self, url, text, number):
		self.status_submit = '0'
		self.http_response = ''
		self.browser = Browser()
		self.browser.open(url)
		self.browser.select_form(nr=1)
		self.url = url
		self.text = text
		self.number = number
		self.tipos = []

		self.new_path = Path()
		self.root_state = self.new_path.append(0, None, None, None, None, None, None, None)
		self.global_error_stack = Stack()
		#counter_errors = 0
		set_submit_form(self, self.root_state, 0, self.new_path, self.global_error_stack)


	def initialize(self):
		self.status_submit = '0'
		self.http_response = ''
		#self.browser = Browser()
		self.browser.open(self.url)
		self.browser.select_form(nr=1)
		#self.url = url
		#self.tipos = []
	def reload(self):
		self.status_submit = '0'
		self.http_response = ''
		#self.browser.open(url)
		self.browser.select_form(nr=1)
		#self.url = url
		#self.tipos = []
	
	def print_stack_errors(self):
		print('inicio final')
		self.global_error_stack.print_errors()
		print('final')

	
	def return_json_errors(self):
		return self.global_error_stack.build_json()



def ajax_process():

	data = dict()

	text = 'aaaa'
	number = '9'
	url = "http://localhost:8080/page_1"

	entorno = Enviroment(url, text, number)
	results = entorno.return_json_errors()

	print('resultados')
	print(results)



ajax_process()