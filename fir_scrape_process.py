#Scraper For website:  
#Converts pdf document to string.
#Covered Cases: 
#   FIR in image format: png,jpeg
#   FIR in pdf/doc format
#Detect language and translate. 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from datetime import date,datetime,timedelta
from deep_translator import MyMemoryTranslator
from io import StringIO
from PIL import Image
from pdf2image import convert_from_path
import time
import os
import shutil
import pytesseract
import codecs

class ReportDoc:
    def __init__(self):
        self.fir_number = ""
        self.fir_date = ""
        self.district = ""
        self.police_station = ""
        self.year = ""
        self.fir_name = ""
        self.date_filing = ""
        self.time_filing = ""
        self.acts = []
        self.date_information_recieved = ""
        self.time_information_recieved = ""
        self.general_diary_entry_number = ""
        self.time_information_recieved = ""
        self.date_general_diary = ""
        self.time_general_diary = ""
        self.type_of_information = ""
        self.name_complainant = ""
        self.name_complainant_father = ""
        self.dob_complainant = ""
        self.nationality_complainant = ""
        self.UID_complainant = ""
        self.Passport_complainant = ""
        self.ID_details = []
        self.occupation_complainant = ""
        self.address_complainant = ""
        self.phone_number_complainant = ""
        self.mobile_number_complainant = ""
        self.details_suspect = ""
        self.details_property = ""
        self.total_value_property = ""
        self.inquest_report = []
        self.fir_content = ""
        self.district = ""

reports_list = []

options = Options()
prefs = {'download.default_directory' : "C:\\Users\\punee\\Legal_DDP\\Downloads"}
options.add_experimental_option('prefs', prefs)
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
PATH = "C:/Users/punee/Legal_DDP/chromedriver"
driver = webdriver.Chrome(PATH,chrome_options=options)

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def pdf_to_text(pages=None):
    text_full = ""
    pages = convert_from_path('C:/Users/punee/Legal_DDP/Downloads/record.pdf', 500, poppler_path='C:/Program Files (x86)/poppler-0.68.0/bin')
    print(pages)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    print("Running OCR")
    for page in pages:
        text_small = ""
        print("***new img***")
        page.save('out.jpg', 'JPEG')
        im = Image.open("C:/Users/punee/Documents/GitHub/Saral/out.jpg")
        text_small = pytesseract.image_to_string(im, lang = 'hin+eng')
        text_full = text_full + text_small
    return (text_full)

def translate_text(text_full):   
    print("Translating")
    print(text_full)
    translated_full = ""
    chunks = chunkstring(text_full,499)
    for chunk in chunks:
        translated_chunk = ""
        print("***new chunk***")
        print(len(chunk))
        translated_chunk = MyMemoryTranslator(source='auto', target='en').translate(chunk)
        translated_full = translated_full + translated_chunk
        print(len(translated_full))
        time.sleep(120)
    text_full = translated_full
    print(translated_full)
    f = codecs.open('bla.txt', encoding='utf-8', mode='w')
    f.write(text_full)
    f.close()
    file1 = open("bla.txt", encoding='utf-8',mode="r+")
    file1.seek(0)
    return text_full

driver.get("https://haryanapolice.gov.in/ViewFIR/FIRStatusSearch?From=LFhlihlx/W49VSlBvdGc4w==")
year_parse = "2019"
district = "BHIWANI"
police_station = "LOHARU"
print("Scraping")
select = Select(driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_ddFIRYear']"))
select.select_by_value(year_parse)
select = Select(driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_ddlDistrict']"))
select.select_by_visible_text(district)
select = Select(driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_ddlPoliceStation']"))
select.select_by_visible_text(police_station)
driver.find_element_by_css_selector('#ContentPlaceHolder1_btnStatusSearch').click()
records_processed = 0
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".lightrow td"))).click()
records = driver.find_elements_by_css_selector('#tblDisplayRecords a')
for record in records:
    record.click()
    original_table_handle = driver.window_handles[-2]
    driver.switch_to_window(driver.window_handles[-1])
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#RptView_ctl06_ctl04_ctl00"))).click()
    download = driver.find_element_by_css_selector("#RptView_ctl06_ctl04_ctl00")
    download.click()
    time.sleep(2)
    print("Downloading")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='RptView_ctl06_ctl04_ctl00_Menu']/div[1]/a"))).click()
    download_2 = driver.find_element_by_xpath("//*[@id='RptView_ctl06_ctl04_ctl00_Menu']/div[1]/a")
    try:
        download_2.click()
    except:
        pass
    driver.switch_to_window(original_table_handle)
    records_processed = records_processed + 1
    time.sleep(2)
    Initial_path = r"C:\\Users\\punee\\Legal_DDP\\Downloads"
    filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)],key=os.path.getctime)
    shutil.move(filename,os.path.join(Initial_path,r"record.pdf"))
    print("Downloaded")
    text = pdf_to_text()
    translated_text = translate_text(text)
    print("record#" + str(records_processed))
driver.quit()

