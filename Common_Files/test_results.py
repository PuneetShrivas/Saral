from elasticsearch import Elasticsearch
import json

from numpy.lib.function_base import average
es = Elasticsearch(
    ["https://search-firstcasecourtdata-fhx2m5ssjtso7lmalxrhhzrkmy.us-east-2.es.amazonaws.com"])

sents_response_array = []
for case_id in range(1,11):
    print('getting case : ' + str(case_id))
    if (case_id==12):
        continue
    sent_response = es.search(index="similarity_sample", body={
            "track_total_hits": True,
            "_source": "*",
            "query": {"match":{"_id":case_id}}})

    for i in sent_response['hits']['hits'][0]['_source']['jt']:
        sents_response_array.append({"text": i['text'], "cited_ids": i['cited_ids'], "weight":i['weight'], "date_range": i['date_range'],"max_score":i['max_score'],"avg_score":i['avg_score']})

def extract_score(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return float(json['weight'])
    except KeyError:
        return 0

def extract_avg_score(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return float(json['avg_score'])
    except KeyError:
        return 0

def extract_max_score(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return float(json['max_score'])
    except KeyError:
        return 0

def extract_avg_minus_self_score(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        if(json['avg_score']<9):
            return 0
        if(json['weight']<9):
            return 0
        else:
            return float(json['avg_score']/json['weight'])
    except KeyError:
        return 0

def extract_max_divide_len_score(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        if(json['avg_score']<9):
            return 0
        if(json['weight']<9):
            return 0
        else:
            return float(json['max_score']/len(json['text']))
    except KeyError:
        return 0

def extract_avg_divide_len_score(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        if(json['avg_score']<9):
            return 0
        if(json['weight']<9):
            return 0
        else:
            return float(json['max_score']/len(json['text']))
    except KeyError:
        return 0

# sents_response_array = [{"text": "abc", "cited_ids": [1,2,3],"score":12},{"text": "xyz", "cited_ids": [1,2,3],"score":10},{"text": "ac", "cited_ids": [1,2,3],"score":15}]
###Sorting JSON
# sorted_sents_response = sorted(sents_response_array, key = lambda k: k['score'], reverse = True)

# sorted_sents_response = sents_response_array.sort(key = extract_score, reverse = True) #self-score
# sorted_sents_response = sents_response_array.sort(key = extract_max_score, reverse = True) #max-score
# sorted_sents_response = sents_response_array.sort(key = extract_avg_score, reverse = True) #avg_score
sorted_sents_response = sents_response_array.sort(key = extract_max_divide_len_score, reverse = True) #diff_score

# body = {"jt": sents_array}
# print(len(sents_array))
# response = es.index(
#     index="similarity_sample",
#     id=1,
#     body=body
# )

# # print(response)

for i in sents_response_array[0:30]: 
    print("score: " + str(i['weight']) )
    print("avg_score: " + str(i['avg_score']))
    print("max_score: " + str(i['max_score']))
    print("division_score: " + str(i['avg_score']/i['weight']))

    print("text: " + i['text'])
    # print("cited_ids: ")
    # for j in i['cited_ids']:
    #     print(j)
    print("****************************")    