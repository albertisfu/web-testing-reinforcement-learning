import re
from mechanize import Browser

import mechanize
import urllib3

import random

#import sys
#sys.setrecursionlimit(100000)

url = "http://localhost:8080/page_1"




class Webpage:
	def __init__(self, url):
		self.browser = Browser()
		self.browser.open(url)

entorno = Webpage(url)

#entorno.browser.select_form(nr=2)

print(entorno.browser.forms())

forms = entorno.browser.forms()

for form in forms:
	#print(form)
	print("Form name:", form.name)
	for control in form.controls:
		print(control)
		print ("type=%s, name=%s value=%s" % (control.type, control.name, [control.name]))
		print('--------------------')


	


