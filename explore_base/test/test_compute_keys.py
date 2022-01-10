import pytest

#from explore_module.compute_keys import get_all_paths

import sys

#paths testing
print('print syspath')
print(sys.path)


from explore.compute_keys import Generator
from explore.craw_forms import CrawForms

@pytest.mark.parametrize('field_options,states_number', [
    ([[0,1,2],[0,1], [0,1], [0,1], [0,1], [0,1], [0,1]], 192,)
])

def test_states_generator(field_options, states_number):
    combinations = Generator(field_options)
    #print('All combinations')
    #print(combinations.paths)

    assert isinstance(combinations.states, dict)
    print('number states ', states_number)

    #TODO test two different assertions in one function
    assert combinations.counter == states_number



@pytest.mark.parametrize('url,num_forms,fields_forms', 
    [('http://localhost:8080/page_1', 2, [{'title':['text', ''], 'cantidad':['number', ''], 'tipo':['select', ['0', '1']], 'boleano':['checkbox', '']}]
     )])
def test_get_forms_fields(url, num_forms, fields_forms):
    forms = CrawForms(url)

    print('results Craw ', forms.results)

    assert forms.quantity == num_forms
    #assert forms.results == fields_forms
