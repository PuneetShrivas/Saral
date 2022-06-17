import spacy
from string import punctuation
from elasticsearch import Elasticsearch
import json
from matplotlib import pyplot as plt
import numpy as np

es = Elasticsearch(
    cloud_id="saraldemo:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDNkZjA4Mzg3YjcxNzQ3NGE4OTFhZDU2NGEyYzQ0N2NjJDIzNzU2NjdjOTQ4YTQ3NDU5YTM5MDFjZTgxZTgzZDdi",
    http_auth=("elastic", "Nt2eZIl6yTQOwQzXrdBXowUP")
    # api_key=("oJjqLYEB-l7PgjpzMhgr", "ut6DqTHPRfupBJQ2Su5yrw"),
    )
nlp = spacy.load('en_core_web_sm')

for id in range(1,2):
    sent_response = es.search(index="similarity_sample", body={
        "track_total_hits": True,
        "_source": "*",
        "query": {"match": {"_id": id}}})

    print("processing case " + str(id))

    sents_response_array = []
    for i in sent_response['hits']['hits'][0]['_source']['jt']:
        sents_response_array.append(
            {"text": i['text'], "cited_ids": i['cited_ids'], "weight": i['weight'], "date_range": i['date_range']})

# 1. array of all scores vs ids
# 2. avg scores
# 3. max scores

    for sent in sents_response_array:
        avg_score = 0
        max_score = 0
        sent_cases_ids = []
        inter_cases_response = es.search(index="similarity_sample", body={
            "track_total_hits": True,
            "_source": "_id",
            "query": {
                "more_like_this": {
                    "fields": [
                        "jt.text"
                    ],
                    "like": sent['text'],
                    "min_term_freq": 1,
                    "max_query_terms": 500,
                    "min_doc_freq": 1,
                    "minimum_should_match": 1
                }
            }
        }
        )
        count = 0
        for i in inter_cases_response['hits']['hits']:
            sent_cases_ids.append({"id": i['_id'],"score":float(i['_score'])})
            avg_score = (avg_score*count + i['_score'])/(1+count)
            count = count + 1
            if(max_score<i['_score']):
                max_score = i['_score']
        sent['cited_ids'] = sent_cases_ids
        sent['avg_score'] = float(avg_score)
        sent['max_score'] = float(max_score)
        print('avg_score:' + str(avg_score))
        print('max_score:' + str(max_score))
        print("*")

    print("storing "+ str(id) +" in similarity_search")
    response = es.index(
        index="similarity_sample",
        id=id,
        # only change this id on next document
        body={"jt": sents_response_array}
    )
    print(response)


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

    # sents_response_array = [{"text": "abc", "cited_ids": [1,2,3],"score":12},{"text": "xyz", "cited_ids": [1,2,3],"score":10},{"text": "ac", "cited_ids": [1,2,3],"score":15}]
    # Sorting JSON
    # sorted_sents_response = sorted(sents_response_array, key = lambda k: k['score'], reverse = True)
    sorted_sents_response = sents_response_array.sort(
        key=extract_score, reverse=True)


    count=1
    a = []
    x = np.linspace(0,100,100)
    for i in sents_response_array[0:100]:
        print("Case number: " + str(count))
        print("score: " + str(i['weight']))
        a.append(i['weight'])
        print("text: " + i['text'])
        # print("cited_ids: ")
        # for j in i['cited_ids']:
        #     print(j)
        print("****")
        count += 1

plt.scatter(x, a)
plt.title("Score")
plt.show()