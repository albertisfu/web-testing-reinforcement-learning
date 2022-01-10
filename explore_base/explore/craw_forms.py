
from mechanize import Browser

class CrawForms:
    def __init__(self, url):
        self.browser = Browser()
        self.browser.open(url)
        self.quantity = 0
        self.results = []

        self.get_field_forms()

    
    def get_field_forms(self):
        forms = self.browser.forms()
        nr_form = 0
        for form in forms:
            #print(form)
            print("Form name:", form.name)
            field_dict = {}
            self.browser.select_form(nr=nr_form)
            for control in form.controls:
                print(control)
                print ("type=%s, name=%s value=%s" % (control.type, control.name, [control.name]))
                print('--------------------')

                if control.type == 'select' or control.type == 'text' or control.type == 'number' or control.type == 'checkbox':
                    if control.type == 'select':
                        options = self.browser.form.possible_items(control.name)
                        field_dict[control.name] = [control.type, options]
                    else:
                        field_dict[control.name] = [control.type, '']
            
            self.results.append(field_dict)
        
            nr_form = nr_form + 1
        
        self.quantity = nr_form



    
