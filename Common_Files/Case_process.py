import pymongo
path="mongodb://db_user:firstCaseDevTeam@107.20.44.181:27017,3.229.151.98:27017,54.175.129.116:27017/?authSource=admin&replicaSet=aName&readPreference=primaryPreferred&ssl=false"
import re
client = pymongo.MongoClient(path)
db = client["indian_court_data"]
col = db["cases"]


  
for case in col.find({}):
    count=0
    if count<=1:
        text = (col["judgement_text"])
        print(text)
        
        count=count+1
          
    else:
        break    