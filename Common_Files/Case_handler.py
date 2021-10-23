import re
import spacy
import datetime
from string import punctuation
nlp = spacy.load('en_core_web_sm')
sal_re_indicators = ['Shri', 'Sh\.', 'Sh', 'Mr\.', 'Mr', 'Miss', 'Ms\.', 'Ms', 'Mrs\.', 'Ms', 'Dr\.', 'Dr']
section_re_indicators = ['s\.', 'section', 'rule', 'article', 'chapter', 'clause', 'paragraph', 'explanation']
law_re_indicators = ['Act', 'Statute', 'Rules', 'Regulations', 'Reference', 'Constitution', 'Circular', 'Notice', 'Notification', 'Code','Adhiniyam']
case_re_indicators = ['v', 'v\.', 'vs', 'vs\.', 'Vs', 'Vs\.', 'versus', 'Versus']
counsel_petitioner_re_indicators = ['for(\s+)(the)?(\s+)((appellant(s?))|(petitioner(s?)))(\.?)']
counsel_respondent_re_indicators = ['for(\s+)(the)?(\s+)respondent(s?)(\.?)']
list_stop = ['of', 'for', 'the', 'and', 'under', '\.', ',', '\(', '\)', '\-']
list_stop_regex = '('+'|'.join(list_stop)+')'
first_cap_regex = '([A-Z]\S*\s*('+list_stop_regex+'*\s*'+'([A-Z]|\d)\S*\s*)+)'
law_regex_no_words = first_cap_regex+'(((,|of)\s+)?(\d)*\s*)*'
act_name_patterns = 'act|law|constitution|rule|notification|circular|paragraph|article|statute|reference|section|interpretation|regulation|regulations'
case_id_re_indicators = ['(.*)(\s?)(.*?)(\s?)(.*)(\s?)(of)(\s?)(\d{4})']
"""
Constitutional Bench is not a law - DONE
'Section' is never mentioned under the Constitution - DONE
'The Act' is not a law - TODO
Some laws contain the word 'Code' - DONE
Similarly occurring extraction - The Constitution + Constitution of India - TODO
Abbreviated Laws - IPC (Indian Penal Code, 1860), CrPC (Criminal Procedural Code, 1973), CPC (Code of Civil Procedure, 1908), IBC (Insolvency & Bankruptcy Code, 2018) - DONE
TODO: 
"""

"""
case_id TODO: 
1. Extract phrase of case id for given case
2. Extract phrase of cited case ids 
3. For adding citations use ES for title and _doc mapping. For no matches, store found case_id string in cited_cases
4. Add regexes for situations like 122/133/2021 
"""

"""
date TODO:
1. Extract all dates
2. Find context defining phrases for cases's date
    ideas:  Date of judgement
            Latest date in list of dates in headnote
"""

#****************************CASE CLASS DEFINITION****************************
class CaseDoc:
    def __init__(self):
        self.title = ""                     #self defined
        self.case_id = ""                   #self defined
        self.url = ""                       #self defined
        self.source = ""                    #self defined
        self.date = datetime.datetime.now() #self defined
        self.doc_author = ""                #self defined
        self.petitioner = ""                #self defined
        self.respondent = ""                #self defined
        self.bench = []                     #self defined
        self.petitioner_counsel = []        #function done
        self.respondent_counsel = []        #function done
        self.cases_cited = []               #function done
        self.cases_citing = []              #self defined
        self.judgement = ""                 #function done
        self.judgement_text = ""            #self defined
        self.provisions_referred = []       #function done 
        self.query_terms = []               #self defined
        self.year = ""            #self defined
        self.month = ""
        self.day = ""
    def process_text(self): #processes text and retrieves a set of case variables
        print("********processing text********") 
        text = self.judgement_text.replace('>>>>','')
        doc_nlp = nlp(text)
        self.case_id = case_get_case_id(text, doc_nlp)
        self.cases_cited = case_get_cases_list(text, doc_nlp)
        self.provisions_referred = case_get_acts_list(text, doc_nlp)
        self.petitioner_counsel = case_get_petitioner_counsel(text, doc_nlp)
        self.respondent_counsel = case_get_respondent_counsel(text, doc_nlp)
        self.judgement = case_get_judgement(self.judgement_text.split(' >>>> ')[-5:]) # increase -3 if judgement is not extracted
        print("********processed text********") 

    def print_case_attributes(self):
        print("date : "  + str(self.date))
        print("year : " + str(self.year))
        print("month : " + str(self.month))
        print("day : " + str(self.day))
        print("url : "  + str(self.url))
        print("author : "  + str(self.doc_author))
        print("bench : "  + str(self.bench))
        print("title : "  + str(self.title))
        print("petitioner : "  + str(self.petitioner))
        print("respondent : "  + str(self.respondent))
        print("source : "  + str(self.source))
        print("query_terms : "  + str(self.query_terms))
        print("judgement : "  + str(self.judgement))
        print("petitioner counsel : "  + str(self.petitioner_counsel))
        print("respondent counsel : "  + str(self.respondent_counsel))
        print("cases cited : " + str(self.cases_cited))
        print("provisions referred : " + str(self.provisions_referred))
        print("judgement_text length : " + str(len(self.judgement_text)))



#****************************CASE SPECIFIC FUNCTIONS****************************
#TODO Remove starting lines with random characters, like %, *                       @PDFS
#TODO case ID function for indkanoon cases                                          Later
#TODO corrections required in case_get_acts_list and case_get_judgement             
#TODO Bench function (Looks to be source specific)
#TODO Doc_author function (Check for source specific nature)

def case_get_case_id(case_text, doc_nlp):
    case_id_regexp = '('+'|'.join(case_id_re_indicators)+')'
    print(case_id_regexp)
    case_id = set()

    # try:
    for sent in doc_nlp.sents:
        # txt_lower = sent.text.lower()
        start = 0
        for m in re.finditer(case_id_regexp, sent.text, re.IGNORECASE):
            print(("match : " + sent.text).strip())
            print(m.group(),m.start(),m.end())
            # if m:
            #     print("in for if ")
            #     print(sent.text)
                # case_id |= find_case_id(sent.text, start, m.start())
                # start = m.end()    
    # except:
    #     print("case_id not found")
    print(case_id)
    return list(case_id)


def find_case_id(sent_text, start, end):
    caseIDs = set()
    sent_text_split = re.split(',\s?', sent_text[start:end])
    # print(sent_text_split)
    return caseIDs




def case_get_petitioner_counsel(case_text, doc_nlp):
    sal_regexp = get_salutation_regexp(sal_re_indicators)
    counsel_petitioner_regexp = get_counsel_regexp(counsel_petitioner_re_indicators)
    petitioner_counsel = set()
    try:
        # doc_nlp = nlp(case_text)
        for sent in doc_nlp.sents:
            txt_lower = sent.text.lower()
            start = 0
            for m in re.finditer(counsel_petitioner_regexp, sent.text, re.IGNORECASE):
                if m:
                    petitioner_counsel |= find_counsel(sent.text, start, m.start())
                    start = m.end()
    except:
        print ("oops parsing petitioner counsel")
    petitioner_counsel = normalize_person_set(petitioner_counsel, sal_regexp)
    return list(petitioner_counsel)

def case_get_respondent_counsel(case_text, doc_nlp):
    sal_regexp = get_salutation_regexp(sal_re_indicators)
    counsel_respondent_regexp = get_counsel_regexp(counsel_respondent_re_indicators)
    respondent_counsel = set()
    try:
        for sent in doc_nlp.sents:
            txt_lower = sent.text.lower()
            start = 0
            for m in re.finditer(counsel_respondent_regexp, sent.text, re.IGNORECASE):
                if m:
                    respondent_counsel |= find_counsel(sent.text, start, m.start())
                    start = m.end()
    except:
        print ("oops parsing respondent counsel")
    respondent_counsel = normalize_person_set(respondent_counsel, sal_regexp)
    return list(respondent_counsel)

def case_get_judgement(paragraphs):
    for segment in paragraphs:
            try:
                segment = segment.strip().lower()
            except:
                segment = ''
            # print(segment)
            if 'allow' in segment:
                judgement = 'allowed'
                if 'partly' in segment:
                    judgement = 'partly allowed'
                break
            elif 'allowed' in segment:
                judgement = 'allowed'
                if 'partly' in segment:
                    judgement = 'partly allowed'
                break
            elif 'dismiss' in segment:
                judgement = 'dismissed'
                if 'partly' in segment:
                    judgement = 'partly dismissed'
                break    
            elif 'dismissed' in segment:
                judgement = 'dismissed'
                if 'partly' in segment:
                    judgement = 'partly dismissed'
                break 
            elif 'disposed' in segment:
                judgement = 'dismissed'
                if 'partly' in segment:
                    judgement = 'partly dismissed'
                break    
            else:
                judgement = 'tied / unclear'
    return judgement

def case_get_acts_list(case_text, doc_nlp):
    section_regexp = get_section_regexp(section_re_indicators)
    law_regexp = get_law_regexp(law_re_indicators)
    law_dict = {}
    try:
        # doc_nlp = nlp(case_text)
        law_prev = ''
        for sent in doc_nlp.sents:
            txt_lower = sent.text.lower()
            sent_laws = find_laws(law_dict, sent.text, law_regexp)
            if re.search(section_regexp, sent.text, re.IGNORECASE):
                law_prev = find_section_and_law(law_dict, sent.text, section_regexp, law_regexp, law_prev, sent_laws)
            else:
                if len(sent_laws) > 0:
                    law_prev = sent_laws[-1][0]
    except: 
        print("oops parsing laws")
    law_dict.pop("Constitutional Bench", None)
    combine_laws(law_dict)
    provisions_array = break_provisions(repr_laws(law_dict))
    return provisions_array

def case_get_cases_list(case_text, doc_nlp):
    case_regexp = get_case_regexp(case_re_indicators)
    case_list = []
    try:
        # doc_nlp = nlp(case_text)
        for sent in doc_nlp.sents:
            txt_lower = sent.text.lower()
            if re.search(case_regexp, sent.text):
                case_list.extend(find_case(sent.text, case_regexp))
    except: 
        print("oops parsing cases")
    removal_indices = []    
    if len(case_list)>0:
        for i in range(len(case_list)):
            if case_list[i].find('\n') != -1:
                print("Omitting from cited case list: " + str(case_list[i]))
                removal_indices.append(i)
    for index in reversed(removal_indices):
        case_list.pop(index)
    return case_list

def case_get_length(case_text):
    return(len(case_text)) 


#****************************HELPER FUNCTIONS****************************
def find_assoc_law(text):
    return re.match(law_regex_no_words, text)

def find_first_set_cap_words(str_in):
    m = re.findall(first_cap_regex, str_in)
    if m:
        if len(m) > 0:
            return m[0][0]
    return None

def find_last_set_cap_words(str_in):
    m = re.findall(first_cap_regex, str_in)
    if m:
        if len(m) > 0:
            return m[-1][0]
    return None

def extend_dict(dict_a, dict_b):
    for k in dict_b:
        if k in dict_a:
            dict_a[k].extend(dict_b[k])
        else:
            dict_a[k] = dict_b[k][:]

def get_salutation_regexp(sal_re_indicators):
    re_sal_str = '('+'|'.join(sal_re_indicators)+')'
    salutation_regexp = re_sal_str+'(\s+)'
    # print (salutation_regexp)
    return salutation_regexp

def get_section_regexp(section_indicators):
    re_section_str = '('+'|'.join(section_indicators)+')'
    section_regexp = '(((\s|,|\.)+)'+re_section_str+'(\s+)(\S+)(\s?))((of|in)\s+(the\s+)?)?'
    # print (section_regexp)
    return section_regexp

def get_law_regexp(law_re_indicators):
    return '('+'|'.join(law_re_indicators)+')'

def get_case_regexp(case_indicators):
    re_case_str = '('+'|'.join(case_indicators)+')'
    case_regexp = '(\s+)'+re_case_str+'(\s+)'
    # print (case_regexp)
    return case_regexp

def get_counsel_regexp(counsel_indicators):
    re_counsel_str = '('+'|'.join(counsel_indicators)+')'
    counsel_regexp = '(\s+)'+re_counsel_str
    # print (counsel_regexp)
    return counsel_regexp

def find_laws(law_dict, sent_text, law_regexp):
    sent_laws = []
    for m in re.finditer(law_regex_no_words, sent_text):
        law = m.group(0).strip()
        if re.search(law_regexp, law):
            if law not in law_dict:
                law_dict[law] = []
            sent_laws.append((law, m.start(), m.end()))
    return sent_laws
        
def find_section_and_law(law_dict, sent_text, section_regexp, law_regexp, law_prev, sent_laws):
    curr_idx = -1
    if len(sent_laws) > 0:
        curr_idx = 0
    for m in re.finditer(section_regexp, sent_text, re.IGNORECASE):
        if curr_idx >= 0:
            while curr_idx < len(sent_laws) and m.start() > sent_laws[curr_idx][2]:
                law_prev = sent_laws[curr_idx][0]
                curr_idx += 1
        section_str = m.group(1).strip()
        if m.group(6):
            assoc_law = find_assoc_law(sent_text[m.end():])
            if assoc_law: 
                curr_law = assoc_law.group(0).strip()
                if re.search(law_regexp, curr_law):
                    law_prev = curr_law
                else:
                    section_str += ', '+curr_law
        if len(law_prev) > 0 and law_prev not in law_dict:
            law_dict[law_prev] = []
        if len(law_prev) > 0:
            law_dict[law_prev].append(section_str)
    if len(sent_laws) > 0:
        law_prev = sent_laws[-1][0]
    return law_prev

def normalize_person_set(set_persons, sal_regexp):
    new_set_persons = set()
    for person in set_persons:
        person = re.sub(sal_regexp, '', person)
        new_set_persons.add(person)
    return new_set_persons
            
def find_case(sent_text, case_regexp):
    list_cases = []
    last_case = ''
    for m in re.finditer(case_regexp, sent_text):
        first_case = find_last_set_cap_words(sent_text[:m.start()])
        if first_case and ' and ' in first_case and first_case.strip() == last_case.strip():
            curr = first_case.split(' and ')
            try:
                past_case_split = list_cases[-1].split(mid)
                list_cases[-1] = past_case_split[0]+mid+curr[0]
            except:
                #print "oops case"
                pass
            first_case = curr[1]
        mid = m.group(0)
        last_case = find_first_set_cap_words(sent_text[m.end():])
        if first_case and mid and last_case:
            list_cases.append(first_case.strip()+mid+last_case.strip())
        else:
            # print (first_case, mid, last_case)
            pass
    return list_cases
        
def find_counsel(sent_text, start, end):
    counsels = set()
    sent_text_split = re.split(',\s?', sent_text[start:end])
    if 'and' in sent_text_split[-1]:
        sent_text_split[-1] = re.split('\s?and\s', sent_text_split[-1])
    if '&' in sent_text_split[-1]:
        sent_text_split[-1] = re.split('\s?&\s', sent_text_split[-1])
    final_phrase_list = []
    for sublist in sent_text_split:
        if len(sublist) > 0:
            if type(sublist) is list:
                for item in sublist:
                    if len(item) > 0:
                        final_phrase_list.append(item)
            else:
                final_phrase_list.append(sublist)
    for phrase in final_phrase_list:
        phrase_doc = nlp(phrase)
        if len(phrase_doc.ents) > 0:
            last_ent = phrase_doc.ents[-1]
            if last_ent.label_ == 'PERSON' and phrase.endswith(last_ent.text) and len(last_ent.text.split()) > 1:
                counsels.add(last_ent.text)
            else:
                m = find_last_set_cap_words(phrase)
                if m and len(m.split()) > 1:
                    counsels.add(m)
        else:
            m = find_last_set_cap_words(phrase)
            if m and len(m.split()) > 1:
                counsels.add(m)
    return counsels

def remove_stop(text):
    text = text.lower()
    text = re.sub(list_stop_regex, ' ', text)
    text = re.sub(' +', ' ', text)
    return text.strip()

def combine_laws(law_dict):
    init_keys = list(law_dict.keys())
    mapping = {}
    for law in init_keys:
        law_abbr = None
        if "constitution" in law.lower():
            for elem in law_dict[law]:
                if "s. " in elem or "section" in elem:
                    law_dict[law].remove(elem)
        if law == "IPC":
            law_abbr = "Indian Penal Code, 1860"
        if law == "CrPC":
            law_abbr = "Criminal Procedural Code, 1973"
        if law == "CPC":
            law_abbr = "Code of Civil Procedure, 1908"
        if law == "IBC":
            law_abbr = "Insolvency & Bankruptcy Code, 2018"
        law_norm = remove_stop(law)
        if law_norm in law_dict:
            if mapping[law_norm][1] < len(law_dict[law]):
                if law_abbr:
                    mapping[law_norm] = (law_abbr, len(law_dict[law]))
                else:
                    mapping[law_norm] = (law, len(law_dict[law]))
            law_dict[law_norm].extend(law_dict[law])
        else:
            if law_abbr:
                mapping[law_norm] = (law_abbr, len(law_dict[law]))
            else:
                mapping[law_norm] = (law, len(law_dict[law]))
            law_dict[law_norm] = law_dict[law][:]
        del law_dict[law]
    new_keys = list(law_dict.keys())
    for law in new_keys:
        law_dict[mapping[law][0]] = law_dict.pop(law)
        
def repr_laws(law_dict):
    str_laws_with_sections = ""
    for law in law_dict:
        str_laws_with_sections += law+':'
        str_laws_with_sections += '|'.join(law_dict[law]) + ';'
    return str_laws_with_sections[:-1]

def handler(signum, frame):
    print ("Forever is over!")
    raise Exception()

def find_petitioner(petitioner, txt):
    if len(petitioner) == 0:
        try:
            
            petitioner = re.search('((([A-Z](\S*)(\s?))|(and(\s?))|(&(\s?)))+)((\.)+)(\s?)(Appellant|APPELLANT)', txt).group(1)
        except Exception as exc:
            
            print ("oops petitioner")
            petitioner = ''
    return petitioner

def break_provisions(provisions_string):
    if type(provisions_string) == str:
        provisions_array = []
        for act in provisions_string.split(';'):
            act_splits = re.split('[|:]',act)
            act_splits = [i for i in act_splits if i]
            if len(act_splits):
                act_name = act_splits[0].strip(punctuation)
                if  re.search(act_name_patterns,act_name,re.IGNORECASE) == None : 
                    # print('Act_name ommited: ' + act_name + '..........')
                    # print(act_splits)
                    continue
                act_sections = act_splits[1:]
                ommit_sections = []
                for section in act_sections:
                    if re.search(r"S\.|s\.|S\. |s\. |rule",section,re.IGNORECASE) != None : 
                        if re.search(r"\d+", section) == None :
                            # print(act_name + "'s section ommited: " + section)
                            ommit_sections.append(section)
                for section in ommit_sections:
                    while section in act_sections:
                            act_sections.remove(section)
                act_sections = list(set(act_sections)) 
                provisions_array.append({"act_name": act_name, "act_sections": act_sections})
    return provisions_array
