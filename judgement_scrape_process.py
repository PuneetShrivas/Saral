from selenium import webdriver
import datefinder
import re
import string
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from Common_Files.Case_handler import CaseDoc
from Common_Files.Case_storage import store_case_document
from Common_Files.Elasticsearch_functions import es_case_exists_by_url
from datetime import date,datetime,timedelta
import time
case = CaseDoc()

missed_cases_count = 0
scraped_cases_count = 0
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
PATH = r"C:\\Program Files (x86)\\chromedriver.exe"
#PATH = "/root/chromedriver" ## only uncomment when on server
# driver = webdriver.Chrome(PATH,chrome_options=options) #Uncomment only this line for Headless
driver = webdriver.Chrome(PATH) #Uncomment only this line for Windowed
original_years_handle = ''
original_months_handle = ''
original_table_handle = ''
original_case_handle = ''
missed_cases_list = []
#TODO Only discard first pre tag
def process_IndKanoon_case_url(url):
    case = CaseDoc()
    script = "window.open('{0}', 'case_window')".format(url)
    driver.execute_script(script)
    original_case_handle = driver.window_handles[-2]
    driver.switch_to_window(driver.window_handles[-1])
    driver.set_page_load_timeout(60)
    try:
        try:
            source = driver.find_element_by_css_selector(".docsource_main").text
        except TimeoutException:
            print(url + " was partially loaded")
        except NoSuchElementException:
            time.sleep(5)
            try:
                source = driver.find_element_by_css_selector(".docsource_main").text
            except:
                print("Page Retried")        
        try:
            judgement_div = driver.find_element_by_css_selector(".judgments")
        except NoSuchElementException: 
            print("no judgement")
        try:
            author = driver.find_element_by_css_selector(".doc_author").text.split(':')[-1].translate(str.maketrans('', '', string.punctuation)).strip()
        except NoSuchElementException:
            print("no author found")
        try:
            bench = driver.find_element_by_css_selector(".doc_bench").text.split(':')[-1].split(',')
            if '[' in bench[0]:
                bench = re.findall("\[(.*?)\]", bench[0])
        except NoSuchElementException:
            print("no bench found")
        try:
            title = driver.find_element_by_css_selector(".doc_title").text
        except NoSuchElementException:
            print("no title found")
        try:
            source = driver.find_element_by_css_selector(".docsource_main").text
        except NoSuchElementException:
            print("no source found")
        try:
            query_terms_elements = driver.find_elements_by_css_selector(".item_toselect")
            for query_terms_element in query_terms_elements:
                case.query_terms.append(query_terms_element.text)  
        except NoSuchElementException:
            print("no query terms found")
        try:
            p_tags = judgement_div.find_elements_by_css_selector("blockquote, p")
            pre_tags = judgement_div.find_elements_by_tag_name("pre")
        except NoSuchElementException:
            pass
        pre_text = ""
        for pre_tag in pre_tags:
            pre_text = pre_text + "\n\n" + pre_tag.text
        pre_text_splitted = pre_text.replace('ACT:','>>>').replace('HEADNOTE:','>>>').replace('CITATION:','>>>').replace('JUDGEMENT:','>>>').split('>>>')
        paragraphs = p_tags[1:]
        judgement_text_paragraphs = []
        judgement_text_paragraphs.append(pre_text_splitted[0])
        for paragraph in paragraphs:
            judgement_text_paragraphs.append(paragraph.text.replace('\n','').replace('\r','').replace('',''))
        case.judgement_text = ' >>>> '.join(judgement_text_paragraphs)
        date_string=title.split(" on ")[-1]
        dates = datefinder.find_dates(date_string)
        for i in dates:
            date = i
        case.title = title
        print(case.title)
        try:
            case.petitioner = title.split(' vs ')[0].translate(str.maketrans('', '', string.punctuation)).strip()
        except:
            print("NO Petitioner")
        try:
            case.respondent = title.split(' vs ')[1].split(' on ')[0]
        except:
            print("No Respondent")
        try:
            case.date = date
            case.year = date.strftime("%Y")
            case.month = date.strftime("%B")
            case.day = date.strftime("%d")
        except:
            print("Date error")
        try:
            case.url = url
        except:
            print("NO url")
        try:
            case.doc_author = author
        except:
            print("NO Author")
        try:
            case.bench = bench
        except:
            print("No Bench")
        try:
            case.source = source
        except:
            print("No Source")
        case.process_text() 
        #store_case_document(case) #VERY DANGEROUS!!! DON'T UNCOMMENT UNLESS STORING TO DATABASE
        case.print_case_attributes()
    except Exception as inst:
        print(inst)
        open("indian_kanoon_missed_urls.txt", 'a+').write("%s\n" %(url) )
        print("Missed : %s\n" %(url) + (datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) )
   
    driver.close()
    driver.switch_to_window(original_case_handle) 
    return case

def process_IndKanoon_paginated_table_url(url):
    # time.sleep(2)
    script = "window.open('{0}', 'table_window')".format(url)
    driver.execute_script(script)
    original_table_handle = driver.window_handles[-2]
    driver.switch_to_window(driver.window_handles[-1])
    try:
        total_case_mentioned = int(driver.find_element_by_css_selector("b:nth-child(1)").text.split('of')[-1])
        print("Total Cases: " + str(total_case_mentioned))
        if total_case_mentioned <= 400:
            print("total")
            case_count_in_table = 0
            found_next_page = True
            current_count = 1
            while(found_next_page):
                case_tags = driver.find_elements_by_css_selector(".result_title a")
                case_count_in_table = case_count_in_table + len(case_tags)
                
                for case_tag in case_tags:
                    case_url = case_tag.get_attribute("href")
                    print("...#" + str(current_count) + " of total " + str(total_case_mentioned) + "cases...")
                    if es_case_exists_by_url(case_url)==0:
                        process_IndKanoon_case_url(case_url)
                        current_count = current_count + 1
                    else:
                        print("Case Exist in our Database.")
                try:
                    next_page_tag_url = driver.find_element_by_css_selector(".pagenum+ a").get_attribute("href")
                    driver.get(next_page_tag_url)
                except NoSuchElementException:
                    print("...cases missed in scraping :" + str(total_case_mentioned - case_count_in_table))
                    found_next_page = False
        else:
            
            url = driver.current_url
            source = url.split("doctypes:")[1].split("%20fromdate:")[0]
            f_date = url.split("fromdate:")[1].split("%20todate")[0]
            t_date = url[::-1].split("02%")[0][::-1]
            
            driver.get(url)
            for i in range(30):

                date = datetime.strptime(f_date,'%d-%m-%Y')
                startdate = date
                nextdate = startdate + timedelta(days=1)
                t_date = nextdate.strftime("%d-%m-%Y")
                
                

                searchbox = driver.find_element_by_xpath('//*[@id="search-box"]')
                searchbox.clear()
                searchbox.send_keys(f"doctypes: {source} fromdate: {f_date} todate: {t_date} sortby: leastrecent")
                submit = driver.find_element_by_xpath('//*[@id="submit-button"]')
                submit.click()
                try:
                    total_case_mentioned = int(driver.find_element_by_css_selector("b:nth-child(1)").text.split('of')[-1])
                    # print("Total Cases: " + str(total_case_mentioned))
                    case_count_in_table = 0
                    found_next_page = True
                    current_count = 1
                    while(found_next_page):
                        case_tags = driver.find_elements_by_css_selector(".result_title a")
                        case_count_in_table = case_count_in_table + len(case_tags)
                        
                        for case_tag in case_tags:
                            case_url = case_tag.get_attribute("href")
                            print("...#" + str(current_count) + " of total " + str(total_case_mentioned) + f"cases...mentioned on {f_date} - {t_date}")
                            if es_case_exists_by_url(case_url) == 0:
                                process_IndKanoon_case_url(case_url)
                                current_count = current_count + 1
                            else:
                                print("Case Exist in Database.")    
                        try:
                            next_page_tag_url = driver.find_element_by_css_selector(".pagenum+ a").get_attribute("href")
                            driver.get(next_page_tag_url)
                        except NoSuchElementException:
                            print("...cases missed in scraping :" + str(total_case_mentioned - case_count_in_table))
                            if (total_case_mentioned - case_count_in_table)>0:
                                missed_cases_list.append(f"{total_case_mentioned-case_count_in_table} cases missed in between {f_date} - {t_date}")
                            found_next_page = False

                except ValueError:
                    print("No Case This Month.")
                nextdate = startdate + timedelta(days=2)
                t_date = nextdate.strftime("%d-%m-%Y")
                f_date = t_date        
    except:
        print("nothing")
    driver.close()
    driver.switch_to_window(original_table_handle)

def process_IndKanoon_months_url(url):
    # time.sleep(2)
    script = "window.open('{0}', 'month_window')".format(url)
    driver.execute_script(script)
    original_months_handle = driver.window_handles[-2]
    driver.switch_to_window(driver.window_handles[-1])
    month_tags = driver.find_elements_by_css_selector(".browselist a")
    for month_tag in month_tags:
        print(month_tag.text)
        paginated_table_url = month_tag.get_attribute("href")
        process_IndKanoon_paginated_table_url(paginated_table_url)
    driver.close()
    driver.switch_to_window(original_months_handle)

def process_IndKanoon_court_years_url(url):
    # time.sleep(2)
    script = "window.open('{0}', 'year_window')".format(url)
    driver.execute_script(script)
    original_years_handle = driver.window_handles[-2]
    driver.switch_to_window(driver.window_handles[-1])
    year_tags = driver.find_elements_by_css_selector(".browselist a")
    for year_tag in year_tags:
        print(year_tag.text)
        month_url = year_tag.get_attribute("href")
        process_IndKanoon_months_url(month_url)
    driver.close()
    driver.switch_to_window(original_years_handle)

# driver.get("https://indiankanoon.org/browse/")
# court_tags = driver.find_elements_by_css_selector(".browselist") 
# for court_tag in court_tags:
#     print(court_tag.text)
#     court_url = court_tag.find_element_by_tag_name("a").get_attribute("href")
#     process_IndKanoon_court_years_url(court_url)
court_url = "https://indiankanoon.org/browse/himachal_pradesh/"
process_IndKanoon_court_years_url(court_url)

# driver.get("https://www.google.com/") #any dummy url
# case = process_IndKanoon_case_url("https://indiankanoon.org/doc/105912122/")
# case.print_case_attributes()
# case = process_IndKanoon_case_url("https://indiankanoon.org/doc/871220/")
# case.print_case_attributes()
# case = process_IndKanoon_case_url("https://indiankanoon.org/doc/1902038/")
# case.print_case_attributes()

driver.quit()
print("Completed")
# store_case_document(case) #VERY DANGEROUS!!! DON'T UNCOMMENT UNLESS STORING TO DATABASE

# TODO: ADD TRY EXCEPT BLOCKS FOR TAGS EXTRACTION