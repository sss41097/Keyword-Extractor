import re
import pandas as pd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import operator
debug = False
test = True


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

text=convert_pdf_to_txt('JavaBasics-notes.pdf')
file = open('pdf_to_text.txt','w')
file.write(text)
file.close()

string_of_words=''
text=open('pdf_to_text.txt')
for line in text:
 line=re.sub('[^ A-Za-z]+', '', line)
 line=re.sub(r'\W+', ' ', line)
 string_of_words+=line
 string_of_words+=' '
dictionary={}
list_words=string_of_words.split()
for word in list_words:
	if len(word)<=1:
		continue
	if word not in dictionary:
		dictionary[word]=1
	else:
		dictionary[word]+=1
print(dictionary)				 

df = pd.DataFrame(dictionary,index=[0]).T
df.to_csv('keywords_with_weights.csv')
