import pymongo

client = pymongo.MongoClient("mongodb+srv://PuneetShrivas:admin@betatesting.nsnxl.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client["indian_court_data"]
col = db["cases"]

updated_array=[]

for case in col.find({'title':'Rajeev Suri vs Union Of India on 5 January, 2021'}):
    Cases_ref=case['cases_referred']
    print(Cases_ref)

    for case_ref in Cases_ref:
        if type(case_ref)==str:
            if col.find_one({'title':case_ref})!=None:
                search_case=col.find_one({'title':case_ref})
                searched_case_id=search_case['_id']
                searched_case_id_title=search_case['_title']
                updated_array.append({'case_title' : searched_case_id,'case_id' : searched_case_id})
            else:
                updated_array.append({'case_title' : case_ref})
    
        #col.update_one({'title' : searched_case_id_title},{"$set" : {'cases_referred' : updated_array}}, False, True)
                    
                
        
