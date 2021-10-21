#Case exists by url, title and ID
#Insertion 
#Search 
from elasticsearch import Elasticsearch
import json
es = Elasticsearch(["https://search-firstcasecourtdata-fhx2m5ssjtso7lmalxrhhzrkmy.us-east-2.es.amazonaws.com"])

def es_case_exists_by_url(url):
    query_body = {
  "track_total_hits": True,
  "size": 0, 
  "query": {
    "terms": {
      "url.keyword": [url]
    }
  }
}
    result = es.search(index="indian_court_data.cases",body=query_body)
    return (result['hits']['total']['value'])

def es_case_exists_by_title(title):
    query_body = {
    "track_total_hits": True,
    "size": 0, 
    "query": {
        "terms": {
        "title.keyword": [title]
        }
    }
    }
    result = es.search(index="indian_court_data.cases",body=query_body)
    return (result['hits']['total']['value'])    

def es_case_exists_by_case_id(id):
    query_body = {
    "track_total_hits": True,
    "size": 0, 
    "query": {
        "terms": {
        "case_id.keyword": [id]
        }
    }
    }
    result = es.search(index="indian_court_data.cases",body=query_body)
    return (result['hits']['total']['value'])    

def es_count_by_source(source):
    query_body = {
    "track_total_hits": True,
    "size": 0, 
    "query": {
        "terms": {
        "source.keyword": [source]
        }
    }
    }
    result = es.search(index="indian_court_data.cases",body=query_body)
    return (result['hits']['total']['value'])
# print(es_case_exists_by_url("https://indiankanoon.org/docfragment/1920027/?formInput=doctypes%3A%20supremecourt%20fromdate%3A%201-3-2010%20todate%3A%2031-3-2010"))
# print(es_case_exists_by_title("Gulab Singh Bhati vs State Of U.P. And Others"))
# print(es_count_by_source("Supreme Court of India"))