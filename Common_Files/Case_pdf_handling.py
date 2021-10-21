########################  Downloading Pdf Files ########################
import requests
import re


def case_get_text_paragraphs(case_text):
    paragraphs = re.split('(\n\n()?\d\d\. )|(\n\n()?\d\. )',case_text)
    #TODO add subparagraphs line
    paragraphs.insert(1,' ')
    try:
        paragraphs = [i.strip(' ') for i in paragraphs]
    except Exception as inst:
        print(str(inst) + " : oops paragraph stripping")
    while('' in paragraphs):
        paragraphs.remove('')
    while(None in paragraphs):
        paragraphs.remove(None)
    count = 0
    joined_paragraphs = []
    while(count<=len(paragraphs)):
        if count==len(paragraphs)-1:
            joined_paragraphs.append(paragraphs[count])
            # pass
        else: 
            try:
                joined_paragraphs.append(paragraphs[count] + " " + paragraphs[count+1])
            except Exception:
                pass
        count = count + 2
    return joined_paragraphs

def download_Pdf(a):
    url = a
    r = requests.get(url,verify=False)
    # download_location = r"C:\\Users\\Pushpak\\Documents\\First_case\\pdf\\" 
    filename =  r.url[url.rfind('/')+1:]
    # textFilename = Final_Dir + pdf + ".txt"  ###  For remmembering the method
    open(filename, 'wb').write(r.content)
    print("File Downloaded Successfully")

# test download
# a = "http://164.100.69.66/jupload/dhc/SID/judgement/11-02-2021/SID10022021CRLW2802021_232130.pdf"
# download_Pdf(a)
#######################################################################

#######################################################
##### Using Pdfminer Pdf to text converter ##########################
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt



def extract_txt(url, fname, pages=None):

    r = requests.get(url,verify=False)
    #filename = r.url[url.rfind('/')+1:]
    #print(filename)
    open(fname, 'wb').write(r.content)

    #processing-text
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close

    cleaned_paragraphs = []
    paragraphs = case_get_text_paragraphs(text)
    cleaned_paragraphs.append(paragraphs[0])
    # cleaned_paragraphs.append(" ")
    paragraphs.pop(0)
    for paragraph in paragraphs:
        cleaned_paragraphs.append(paragraph.replace('\n','').replace('\r','').replace('',''))
    return ' >>>> '.join(cleaned_paragraphs)
    # return text 




# def Pdf2Conv(initial_Dir, Final_Dir):
#     if initial_Dir == "": initial_Dir = os.getcwd() + "\\" 
#     for pdf in os.listdir(initial_Dir): 
#         fileExtension = pdf.split(".")[-1]
#         if fileExtension == "pdf":
#             pdfFilename = initial_Dir + pdf 
#             text = extract_txt(pdfFilename) 
#             textFilename = Final_Dir + pdf + ".txt"
#             textFile = open(textFilename, "w") #make text file
#             textFile.write(text) #write text to text file

# test convert file #############################			
# initial_Dir = (r"C:\\Users\\Pushpak\\Documents\\First_case\\pdf\\")
# Final_Dir = (r"C:\\Users\\Pushpak\\Documents\\First_case\\text\\")
# Pdf2Conv(initial_Dir, Final_Dir)
# print("Pdf saved")

#####################################################################################


