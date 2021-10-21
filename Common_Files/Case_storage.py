import pymongo
path = "mongodb://db_user:firstCaseDevTeam@107.20.44.181:27017,3.229.151.98:27017,54.175.129.116:27017/?authSource=admin&replicaSet=aName&readPreference=primaryPreferred&ssl=false"

def store_case_document(case):
    client = pymongo.MongoClient(path)
    db = client["indian_court_data"]
    col = db["cases"]
    data_object = {
        "title": case.title,
        "case_id": case.case_id,
        "url": case.url,
        "source": case.source,
        "date": case.date,
        "year": case.year,
        "month": case.month,
        "day" : case.day,
        "doc_author": case.doc_author,
        "petitioner": case.petitioner,
        "respondent": case.respondent,
        "bench": case.bench,
        "petitioner_counsel": case.petitioner_counsel,
        "respondent_counsel": case.respondent_counsel,
        "cases_referred": case.cases_cited,
        "citing_cases": case.cases_citing,
        "judgement": case.judgement,
        "judgement_text": case.judgement_text,
        # "judgement_text_paragraphs": case.judgement_text_paragraphs,
        "provisions_referred": case.provisions_referred,
        "query_terms": case.query_terms
    }
    print(str(col.insert_one(data_object)))

def case_exists_by_url(url):
    client = pymongo.MongoClient(path)
    db = client["indian_court_data"]
    col = db["cases"]
    if(col.find({"url": url}).count()>0):
        return 1
    else:
        return 0

def case_exists_by_title(title):
    client = pymongo.MongoClient(path)
    db = client["indian_court_data"]
    col = db["cases"]
    if(col.find({"title": title}).count()>0):
        return 1
    else:
        return 0

def case_exists_by_case_id(case_id):
    client = pymongo.MongoClient(path)
    db = client["indian_court_data"]
    col = db["cases"]
    if(col.find({"case_id": case_id}).count()>0):
        return 1
    else:
        return 0