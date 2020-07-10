import easyocr

reader = easyocr.Reader(['ch_sim', 'en'])

# text = reader.readtext('chinese.jpg')
text = reader.readtext('img/2018-1.jpg')
print(text)
