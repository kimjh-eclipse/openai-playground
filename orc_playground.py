import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import easyocr
reader = easyocr.Reader(['ko']) # this needs to run only once to load the model into memory
result = reader.readtext('gilon_sample.jpg')
print(result)
