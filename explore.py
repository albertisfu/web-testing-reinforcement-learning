import requests
import lxml.html as lh


def gender_genie(text, genre):
    url = 'http://localhost:8080/test_suite'
    caption = 'The Gender Genie thinks the author of this passage is:'

    form_data = {
        'title': text,
        'integer': genre,
        'type': 3,
        'submit': 'submit',
    }

    response = requests.post(url, data=form_data)

    tree = lh.document_fromstring(response.content)

    return tree


if __name__ == '__main__':
    print(gender_genie('I have a beard!', 2))