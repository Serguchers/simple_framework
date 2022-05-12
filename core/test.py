import chardet
print(chardet.detect(b'%26%231092%3B%26%231099%3B%26%231074%3B'))
print(b'%26%231092%3B%26%231099%3B%26%231074%3B'.decode('ascii'))