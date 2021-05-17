import re
from mechanize import Browser

import mechanize
import urllib3


browser = Browser()
browser.open("http://localhost:8080/test_suite")

browser.select_form(nr=1)

print(browser)
tipos = browser.form.possible_items("type")
print(tipos)

browser['title'] = ''
browser.set(True, tipos[0] , "type")
browser.find_control("checkbox").items[0].selected = False

print('current estatus')
print(browser['title'])
print(browser['type'])
print(browser['checkbox'])


if browser['title'] == '':
	print('val tit: ', 0)

else:
	print('val tit: ', 1)

if len(browser['checkbox'])==0:
	print('val check: ', 0)
else:
	print('val check: ', 1)

if browser['type'][0] == '0':
	print('val type: ', 0)

elif browser['type'][0] == '1':
	print('val type: ', 1)

elif browser['type'][0] == '2':
	print('val type: ', 2)



try:
	response = browser.submit()
	print('after submit')
	#content = response.read()

	code = response.code

	print(code)
except mechanize.HTTPError as e:
	print('Error:', e)


