import re
from mechanize import Browser

import mechanize
import urllib3

import random

#import sys
#sys.setrecursionlimit(100000)


text = 'aaaa'
number = '9'

url = "http://localhost:8080/page_1"


class State:
	def __init__(self, id, text, number, check, type, url):
		#form state variables 
		self.text = text
		self.number = number
		self.check = check
		self.type = type
		#reference to prev node
		self.prev_node = None
		self.id = id
		self.url =  None
		#TODO add branches references to build tree


class Path:
	def __init__(self):
		#reference to path root node 
		self.root = None
		self.nodes_counter = 0

	#append new elements to path method
	def append(self, id, prev_state, text, number, check, type, url):
		#create new state
		self.nodes_counter = self.nodes_counter + id
		new_state = State(self.nodes_counter, text, number, check, type, url)
		
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
		if self.head.next_node == None:
			
			return True
		else:
			return False
	
	#print elements of linked list
	def print_list(self):
		if self.head != None:
			current_node = self.head
			while current_node != None:
				print(current_node.data.text)
				current_node = current_node.next_node


#function to recreate state on every step in order continue testing fordward last state
#state: desire state to recreate, entorno: entorno to testing, operate web page to reach desire state
def recreate_state(state, entorno):
	#create an stack where is stored from the current state to previous node before root
	stack = Stack()
	#asign state to current state
	current_state = state
	#iterate until get a node before root
	while current_state.prev_node!=None:
		stack.push(current_state)
		current_state = current_state.prev_node

	print('- - - - - - Entro Stack recreate State')
	print('Estado Head:', stack.head)
	stack.print_list()

	#build each state, pop last stack element and recreate state
	if stack.head != None:
		#review if this is empty 
		print('....... is stack empty? recreate: ', stack.empty())
		while stack.empty()!=True:
			print('Ingreso if stack empty: ')
			#get_next_form(entorno.url, stack)
			#initialize enviorement, get form of new page
			entorno.initialize()
			state_last = stack.pop()
			#get tipos of current form page
			entorno.tipos = entorno.browser.form.possible_items("type")
			entorno.browser['title'] = state_last.text
			entorno.browser['cantidad'] = state_last.number
			if state_last.check == 'on':
				entorno.browser.find_control("checkbox").items[0].selected = True
			else:
				entorno.browser.find_control("checkbox").items[0].selected = False
			entorno.browser.set(True, entorno.tipos[int(state_last.type)] , "type")

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
					#TODO verify if necesary go to URL
					#url = response.geturl()
					#return
					print('===== se avanzo para pasar de pagina')
					pass

			except mechanize.HTTPError as e:
				print('Error recreate state:', e)
				#entorno.http_response = 500
				#capture error?
				#return
		print('===== Finalizo While entrar pagina')



def build_error_chain(state):
	#create an stack where is stored from the current state to previous node before root
	local_error_stack = Stack()
	#asign state to current state
	current_state = state
	#iterate until get a node before root
	while current_state.prev_node!=None:
		local_error_stack.push(current_state)
		current_state = current_state.prev_node
	
	global_error_stack.push(local_error_stack)



def set_submit_form(entorno, last_state):

	print(';;;;;;;;; Entro Set Submit Form')

	recreate_state(last_state, entorno)
	#if stack vacio no se recrea nada
	#fill current state
	entorno.initialize()
	print('----- URL actual')
	print(entorno.browser.geturl())
	entorno.tipos = entorno.browser.form.possible_items("type")

	print('Tipos Entorno: ', entorno.tipos)
	for ty in entorno.tipos:
		for ch in ['on', 'off']:
			#reload page to celan fields and test other combinations
			#initialize browser to load form again also get tipos again

			print('--- Entro Submit iterate type, ty:', ty)
			print(entorno.tipos)

			entorno.browser.open(entorno.browser.geturl())
			entorno.initialize()

			entorno.browser['title'] = text
			entorno.browser['cantidad'] = number
			if ch == 'on':
				entorno.browser.find_control("checkbox").items[0].selected = True
			else:
				entorno.browser.find_control("checkbox").items[0].selected = False

		

			entorno.browser.set(True, entorno.tipos[int(ty)] , "type")
			entorno.status_submit = '1'

			#create new state on every different submition data, save URL with each state
			current_state = new_path.append(last_state.id, last_state, text, number, ch, ty, entorno.browser.geturl())

			#submit form
			try:
				print('-----try to submit')
				
				response = entorno.browser.submit()
				
				#print('after submit')
				#content = response.read()
				code = response.code
				#print(code)
				entorno.http_response = code
				if entorno.http_response == 200:
					print('**** call recursive')
					set_submit_form(entorno, current_state)
					

			except mechanize.HTTPError as e:
				print('------- Error:', e)
				error_400 = "HTTP Error 400: Bad Request"
				error_500 = "HTTP Error 500: Internal Server Error"
				if e ==error_400:
					print('got error 400')
					build_error_chain(current_state)
				elif e ==error_500:
					print('got error 500')
					build_error_chain(current_state)

				#entorno.http_response = 500
				#TODO capture error?
				#return



class Enviroment:
	def __init__(self, url):
		self.status_submit = '0'
		self.http_response = ''
		self.browser = Browser()
		self.browser.open(url)
		self.browser.select_form(nr=1)
		self.url = url
		self.tipos = []
	def initialize(self):
		self.status_submit = '0'
		self.http_response = ''
		#self.browser = Browser()
		#self.browser.open(url)
		self.browser.select_form(nr=1)
		#self.url = url
		#self.tipos = []

		

entorno = Enviroment(url)

new_path = Path()

root_state = new_path.append(0, None, None, None, None, None, None)

global_error_stack = Stack()

set_submit_form(entorno, root_state)