#function to activate and send form, based 
def get_next_form(url, stack):
	#initialize enviorement
	entorno.initialize(url)

	#get tipos of current form page
	state_last = stack.pop()
	entorno.tipos = entorno.browser.form.possible_items("type")

	entorno.browser['title'] = state_last.text

	entorno.browser['cantidad'] = state_last.number

	if state_last.check == 'on':
		entorno.browser.find_control("checkbox").items[0].selected = True
	else:
		entorno.browser.find_control("checkbox").items[0].selected = False

	entorno.browser.set(True, entorno.tipos[state_last.type] , "type")

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
			url = response.geturl()
			get_next_form(url, stack)
		else:
			#check if there is a 400 error
			return
	except mechanize.HTTPError as e:
		print('Error:', e)
		entorno.http_response = 600
		return




try:
	response = entorno.browser.submit()
	entorno.http_response = code
	if entorno.http_response == 200:
		print('200')
except mechanize.HTTPError as e:
	print('Error:', e)