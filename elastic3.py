from elasticsearch import Elasticsearch
from matplotlib import pyplot as plt
import json
import numpy as np

from numpy.lib.function_base import average
es = Elasticsearch(
    cloud_id="saraldemo:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDNkZjA4Mzg3YjcxNzQ3NGE4OTFhZDU2NGEyYzQ0N2NjJDIzNzU2NjdjOTQ4YTQ3NDU5YTM5MDFjZTgxZTgzZDdi",
    http_auth=("elastic", "Nt2eZIl6yTQOwQzXrdBXowUP")
    # api_key=("oJjqLYEB-l7PgjpzMhgr", "ut6DqTHPRfupBJQ2Su5yrw"),
    )

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
        if(json['avg_score']<5):
            return 1000
        if(json['weight']<5):
            return 1000
        else:
            return abs(float((json['avg_score']-json['weight'])/len(json['text'])))
    except KeyError:
        return 0

def extract_max_divide_len_score(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        if(json['avg_score']<5):
            return 0
        if(json['weight']<5):
            return 0
        else:
            return float(json['max_score']/len(json['text']))
    except KeyError:
        return 0

def extract_avg_divide_len_score(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        if(json['avg_score']<5):
            return 0
        if(json['weight']<5):
            return 0
        else:
            return float(json['avg_score']/len(json['text']))
    except KeyError:
        return 0

# sents_response_array = [{"text": "abc", "cited_ids": [1,2,3],"score":12},{"text": "xyz", "cited_ids": [1,2,3],"score":10},{"text": "ac", "cited_ids": [1,2,3],"score":15}]
###Sorting JSON
# sorted_sents_response = sorted(sents_response_array, key = lambda k: k['score'], reverse = True)

# sents_response_array.sort(key = extract_score, reverse = True) #self-score
# sents_response_array.sort(key = extract_max_score, reverse = True) #max-score
# sents_response_array.sort(key = extract_avg_score, reverse = True) #avg_score
# sents_response_array.sort(key = extract_max_divide_len_score, reverse = True) #diff_score
# sents_response_array.sort(key = extract_avg_divide_len_score, reverse = True)
sents_response_array.sort(key = extract_avg_minus_self_score)

# body = {"jt": sents_array}
# print(len(sents_array))
# response = es.index(
#     index="similarity_sample",
#     id=1,
#     body=body
# )

# # print(response)
a = []
b = []
c = []
d = []
e = []
f = []
g = []
num = 100
x = np.linspace(0,num,num)
count = 1
for i in sents_response_array[0:num]: 
    print("Case number: " + str(count))
    print("score: " + str(i['weight']) )
    a.append(i['weight'])
    print("avg_score: " + str(i['avg_score']))
    b.append(i['avg_score'])
    print("max_score: " + str(i['max_score']))
    c.append(i['max_score'])
    # print("division_score: " + str(i['avg_score']/i['weight']))
    # d.append(i['avg_score']/i['weight'])
    print("normalized_max: " + str(extract_max_divide_len_score(i)))
    e.append(extract_max_divide_len_score(i))
    print("normalized_avg: " + str(extract_avg_divide_len_score(i)))
    f.append(extract_avg_divide_len_score(i))
    print("score_error: " + str(extract_avg_minus_self_score(i)))
    g.append(extract_avg_minus_self_score(i))

    print("text: " + i['text'])
    # print("cited_ids: ")
    # for j in i['cited_ids']:
    #     print(j)
    print("**********")
    count += 1

fig, axs = plt.subplots(2, 3, figsize =(10, 7), tight_layout = True)
 
axs[0,0].scatter(x, a)
axs[0,0].set_title("Score")
axs[0,1].scatter(x, b)
axs[0,1].set_title("Average Score")
axs[0,2].scatter(x, c)
axs[0,2].set_title("Maximum Score")
axs[1,0].scatter(x, g)
axs[1,0].set_title("Score Error")
axs[1,1].scatter(x, e)
axs[1,1].set_title("Normalized Max")
axs[1,2].scatter(x, f)
axs[1,2].set_title("Normalized Average")

plt.show()