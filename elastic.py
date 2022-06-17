# Store line paraphrasing count
# Store line's range of date of paraphrasing
# Doc's id array for paraphrasing
#thresholds: 18-19

from http.client import REQUEST_TIMEOUT
import spacy
from string import punctuation
from elasticsearch import Elasticsearch
import json
es = Elasticsearch(
    cloud_id="saraldemo:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDNkZjA4Mzg3YjcxNzQ3NGE4OTFhZDU2NGEyYzQ0N2NjJDIzNzU2NjdjOTQ4YTQ3NDU5YTM5MDFjZTgxZTgzZDdi",
    http_auth=("elastic", "Nt2eZIl6yTQOwQzXrdBXowUP"),
    request_timeout=120
    # api_key=("oJjqLYEB-l7PgjpzMhgr", "ut6DqTHPRfupBJQ2Su5yrw"),
    )
nlp = spacy.load('en_core_web_sm')


judgement_text_unprocessed = """1. This appeal under Section 18(1) of the Telecom Regulatory Authority of India Act, 1997 is directed against an order dated 9th April, 2003 passed by the Telecom Dispute Settlement and Appellate Tribunal whereby Petition No.24/2001 filed under Section 14(a)(i) read with Section 14A(1) of the Telecom Regulatory Authority of India Act, 1997 has been dismissed. The factual matrix giving rise to the appeal may be summarised at the outset.

2. The appellant-Shyam Telelink Ltd. was granted a licence under the Indian Telecom Act, 1885 on 4th March, 1998 for providing basic telecom services in Rajasthan Circle. A licence agreement was executed between the parties that, inter alia, required the appellant to start commercial operations within twelve months from the date on which the agreement was executed. The appellant's case before the Tribunal so also before us is that, it was ready to commence commercial operations in the last week of February 1999 and had sought permission of the respondents to do so. Permission was, however, denied on the ground that certain technical deficiencies remained to be removed and certain conditions for the grant of permission remained to be fulfilled. In the meantime the Union of India appears to have offered a Migration Package to all the Telecom Operators in July 1999. Under this package which was offered to the appellant-Shyam Telelink Ltd. on 22nd July, 1999 the fixed licence fee was to stand replaced by a revenue-sharing arrangement w.e.f. 1st August, 1999  subject to the stipulation that atleast 35% of all outstanding dues including interest payable as on 31st July, 1999 and liquidated damages in full is paid by the appellant on or before 15th August, 1999. Migration Package further provided that the company shall have to accept all the conditions stipulated in the package and that all proceedings instituted by the licensee or their associations against the Union of India shall have to be withdrawn.

3. It is not in dispute that the appellant gave an unconditional acceptance to the Migration Package on 22nd July, 1999 nor is it disputed that on 10th August, 1999 the respondent advised the appellant that a sum of Rs.6,74,90,481/- was payable towards outstanding licence fee and interest due thereon apart from a sum of Rs.7.30 crores payable towards liquidated damages that were provisionally determined. The appellant-company was informed that in terms of the Migration Package at least 35% of the total licence fee along with interest amounting to Rs.6,74,90,481/- had to be paid by it before 16th August,  1999 and the balance dues covered by a Financial Bank Guarantee by the 30th November, 1999. The liquidated damages payable by the appellant-company were demanded in full and had to be paid on or before 16th August, 1999.

4. On receipt of the intimation demanding payment of the amounts mentioned above the appellant-company appears to have prayed for waiver of the liquidated damages on the ground that it could not commence commercial operations by the stipulated date on account of certain procedural delay. That prayer was upon consideration turned down with the result that the appellant paid 35% of the outstanding licence fee and interest amounting to Rs.2.36 crores on 16th August, 1999. It also paid the full amount of Rs.7.30 crores towards liquidated damages as demanded by the Government.

5. Commercial operations in Rajasthan were finally started by the appellant-company on 5th June 2000. In March 2001 a demand was raised by the respondent for payment of a  further amount of Rs.70 lakhs as liquidated damages for the delay in the commissioning of the service. Aggrieved by the demand of Rs.8 crores towards liquidated damages out of which the appellant had already paid Rs.7.30 crores on 16th August, 1999 the appellant approached the Tribunal for redress. As mentioned earlier the appellant's case before the Tribunal was that it was ready to commence commercial operations in the last week of February 1999 and had sought permission to do so from the respondent which permission was in an arbitrary, illegal and discriminatory manner refused by the respondent. Recovery of the liquidated damages was, therefore bad, argued the appellant who demanded refund of the entire amount of Rs.8 crores recovered towards liquidated damages from it.

6. The respondent contested the petition before the Tribunal, inter alia, on the ground that the petitioner- appellant was not entitled to question any demand arising out of the agreement executed between the parties after it had unconditionally accepted the Migration Package under  which it agreed to deposit without demur the outstanding licence fee as also the liquidated damages payable under the licence agreement. The respondent also asserted that the appellant was not ready with the commissioning of the service as was evident from the admissions made in several communications sent by it to the respondent. It was further pointed out by the respondent that the computation of actual liquidated damages could be undertaken only after the appellant had commenced commercial operations. The actual charges after such computation were according to the respondent determined at Rs.29.86 crores but the demand was restricted to Rs.8 crores in terms of the explicit limitation prescribed under the licence. An amount of Rs.7.3 crores having already been paid under the Migration Package, a demand for payment of Rs.70 lakhs only was raised by the respondent. It was also asserted by the respondent that the appellant had not disputed calculation of the amount of Rs.7.3 crores as liquidated damages for non- commissioning of the service at the time of Migration  Package and paid the same with other dues. Having done so, the Migration Package which contained a specific stipulation that the acceptance of the package "will be deemed as a full and final settlement of all existing disputes whatsoever irrespective of whether they are related to the present package or not" could not be questioned by the petitioner-appellant. The respondent also raised the question of limitation and assailed the maintainability of the petition on that ground. By its order dated 9th April, 2003 impugned in this appeal the Tribunal dismissed the petition filed by the appellant aggrieved whereof the appellant has filed C.A. No.7236 of 2003 before this Court.

7. We have heard learned counsel for the parties and perused the record. A two-fold contention was urged in support of the appeal by counsel appearing for the appellant. Firstly, it was contended that the appellant was ready to commence commercial operations in February 1999 i.e. within one year of the date on which the agreement was signed between the parties. The fact that the petitioner had  applied for the grant of permission to commence commercial operations in Jaipur from 3rd February, 1999 was according to the appellant sufficient to show its readiness to commence such operations. There is, in our opinion, no force in that contention. It is not disputed that the actual operations started only on 5th June, 2000. The material placed before the Tribunal clearly established that during the intervening period the appellant had been informed by the respondent that clearance for commencing commercial operations could be considered only after the following requirements of the licence agreement were complied with:

(a) Payment of next instalment of licence fee due on 3.3.1999;
(b) Provision of Performance Bank Guarantee (PBG) and enhanced Financial Bank Guarantee (FBG) for requisite amount and validity before commencement of succeeding year on 3.3.1999;
(c) Rectification of deficiencies pointed out by TEC before the commencement of commercial operations;
(d) Submission of plan in respect of providing Direct Exchange Lines (DEL-s) and Village Public Telephones (VPT-s) as per committed targets failing which Liquidated Damages (LD-s) are payable; and
(e) Establishment of a separate bank account (an escrow account as stipulated under condition 18.6 of the Licence Agreement).
8. Material further established that the deficiencies pointed out by the TEC could not be rectified by M/s Qualcomm manufacturer of the equipment purchased by the appellant forcing the latter to go for a new set of equipment from a new vendor in December 1999 which equipment was finally delivered and installed in April 2000. It was only after the installation of the said equipment that fresh test  certificates were issued by TEC on 1st June, 2000 leading to the start of the commercial operations on 5th June, 2000. The fact that the appellant was not ready to commence commercial operations in February 1999 is evident from its own letter dated 19th July, 1999 in which the appellant had clearly admitted that the system was not yet ready for such operations and that the appellant was engaged only in monitoring and testing the credential of the new technology and the related software/hardware. It is also evident from the letter of the appellant dated 25th August, 1999 that the appellant was not in a position to indicate any firm date for a formal launch of the service as the system was not yet in a position to do so. The relevant part of the letter reads as under:

"............ at this stage we are unable to indicate any date for formal commissioning of the commercial launch of the service since still there are bugs in the system provided by our supplier. In any case the testing has to continue for monitoring the behaviour of the equipment even after 75% loading of the system which is also being followed by DoT/MTNL, while acceptance testing of the  systems. However, we hope to commercialize the services by middle of December 1999, as supplier is continuously working to resolve the bugs in the software."
9. In the light of the above admission which is the best evidence against the appellant, it is not open to the appellant to argue that it was ready to start commercial operations in February 1999. The Tribunal was, therefore, perfectly justified in holding that the commercial operations were started only on 5th June, 2000 and that for the intervening period such operations could not be commenced on account of deficiencies that were attributed entirely to the defects in the system which the appellant had installed. The Tribunal was also justified in our opinion in holding that the denial of permission to the appellant was neither arbitrary nor mala fide especially when the conditions in the licence agreement requiring the appellant to arrange and install suitable equipment to meet the prevailing technical specifications by Telecommunication Engineering Centre were not complied with nor were all performance tests  required for successful commissioning of the services carried out by the Licensor before the services are commissioned for public use.

10. The argument that the respondent has acted arbitrarily and in a discriminatory manner by overlooking similar deficiencies in the case of other service providers has also been correctly repelled by the Tribunal on the ground that the nature of the deficiencies found in the case of the appellant have not been found similar to those found in other cases where permission was granted. As a matter of fact, the appellant was given an opportunity to implead the other service providers so that the allegation could be examined in detail but the appellant failed to do so nor was any material placed on record to show that any discriminatory treatment was meted out to it. At any rate so long as the conditions of the agreement entitled the respondents to decline permission to commence commercial operations on account of failure on the part of the appellant to comply with the conditions stipulated in the said  agreement, which condition included a defect-free efficient system, the fact that some other service providers were given permission in the peculiar facts of their cases and deficiencies allegedly noticed in their system could not make out a case for the appellant to question the demand raised on the basis of a package which the appellant had accepted unconditionally and pursuant to which acceptance a substantial part of the liquidated damages amounting to Rs.7.3 crores had been deposited by it without any demur.

11. The Tribunal has also held and in our view correctly so that the computation of the liquidated damages for non- commencing of the services as well as limiting the same to a total amount of Rs.8 crores was in conformity with the licence conditions executed between the parties. There is nothing before us to suggest that any error has crept in the computation of liquidated damages nor was any such error pointed out before the Tribunal. As a matter of fact, according to the respondents the amount of damages works  out to Rs.29.86 crores was limited to Rs.8 crores in explicit terms of the limitation laid down in the licence agreement.

12. The factual aspects apart we need to remember that the payment of liquidated damages was an essential condition of the Migration Package which was offered to the service providers. Unconditional acceptance of the package including the payment of outstanding licence fee with interest due thereon and liquidated damages was a specific requirement of the Migration Package which was unequivocally accepted by the appellant in terms of the declaration made in the following words:

".. With reference to the letter No.842- 153/99-VAS (Vol.V) (Pt.) dated 22nd July, 1999 on the subject noted above, I hereby covey unconditional acceptance on behalf of the Licensee with regard to the package proposed for migration of the existing licenses to NTP 1999 Regime on the terms and conditions in the letter under reference.... "
13. The unconditional acceptance of the terms of the package and the benefit which the appellant derived under  the same will estop the appellant from challenging the recovery of the dues under the package or the process of its determination. No dispute has been raised by the appellant and rightly so in regard to the payment of outstanding licence fee or the interest due thereon. The controversy is limited to the computation of liquidated damages of Rs.8 crores out of which Rs.7.3 crores was paid by the appellant in the beginning without any objection followed by a payment of Rs.70 lakhs made on 29th May, 2001. Although the appellant had sought waiver of the liquidated damages yet upon rejection of that request it had made the payment of the amount demanded which signified a clear acceptance on its part of the obligation to pay. If the appellant proposed to continue with its challenge to demand, nothing prevented it from taking recourse to appropriate proceedings and taking the adjudication process to its logical conclusion before exercising its option. Far from doing so, the appellant gave up the plea of waiver and deposited the amount which clearly indicates acceptance on its part of its liability to pay  especially when it was only upon such payment that it could be permitted to avail of the Migration Package. Allowing the appellant at this stage to question the demand raised under the Migration Package would amount to permitting the appellant to accept what was favourable to it and reject what was not. The appellant cannot approbate and reprobate. The maxim qui approbat non reprobat (one who approbates cannot reprobate) is firmly embodied in English Common Law and often applied by Courts in this country. It is akin to the doctrine of benefits and burdens which at its most basic level provides that a person taking advantage under an instrument which both grants a benefit and imposes a burden cannot take the former without complying with the latter. A person cannot approbate and reprobate or accept and reject the same instrument. In Ambu Nair v. Kelu Nair AIR 1933 PC 167 the doctrine was explained thus:

"Having thus, almost in terms, offered to be redeemed under the usufructuary mortgage in order to get payment of the other  mortgage debt, the appellant, Their Lordships think, cannot now turn round and say that redemption under the usufructuary mortgage had been barred nearly seventeen years before he so obtained payment. It is a well- accepted principle that a party cannot both approbate and reprobate. He cannot, to use the words of Honyman, J. in Smith v. Baker (1878) LR 8 CP 350 at p. 357 `at the same time blow hot and cold. He cannot say at one time that the transaction is valid and thereby obtain some advantage to which he could only be entitled on the footing that it is valid, and at another time say it is void for the purpose of securing some further advantage'."
14. View taken in the above decision has been reiterated by this Court in City Montessori School v. State of Uttar Pradesh and Ors. (2009) 14 SCC 253. To the same effect is the decision of this Court in New Bihar Biri Leaves Co. v. State of Bihar 1981 (1) SCC 537 where this Court said :

"It is a fundamental principle of general application that if a person of his own accord, accepts a contract on certain terms and works out the contract, he cannot be allowed to adhere to and abide by some of the terms of the contract which proved advantageous to him and repudiate the other terms of the same contract which might be  disadvantageous to him. The maxim is qui approbat non reprobat (one who approbates cannot reprobate). This principle, though originally borrowed from Scots Law, is now firmly embodied in English Common Law. According to it, a party to an instrument or transaction cannot take advantage of one part of a document or transaction and reject the rest. That is to say, no party can accept and reject the same instrument or transaction (Per Scrutton, L.J., Verschures Creameries Ltd. v. Hull & Netherlands Steamship Co.)"
15. The decision of this Court in R.N. Goswain v. Yashpal Dhir AIR 1993 SC 352, brings in the doctrine of election in support of the very same conclusion in the following words :

"10. Law does not permit a person to both approbate and reprobate. This principle is based on the doctrine of election which postulates that no party can accept and reject the same instrument and that "a person cannot say at one time that a transaction is valid and thereby obtain some advantage, to which he could only be entitled on the footing that it is valid, and then turn round and say it is void for the purpose of securing some other advantage". [See: Verschures Creameries Ltd. v. Hull and Netherlands Steamship Co. Ltd. (1921) 2 KB 608, at p.612, Scrutton, L.J.] According to Halsbury's Laws of England, 4th Edn., Vol. 16, "after taking an advantage under an order (for example for the payment of costs) a party may be precluded from saying that it  is invalid and asking to set it aside". (para 1508)"
16. In America Estoppel by acceptance of benefits is one of the recognized situations that would prevent a party from taking up inconsistent positions qua a contract or transaction under which it has benefited.

17. American Jurisprudence, 2nd Edition, Volume 28, pages 677-680 discusses `Estoppel by acceptance of benefits' in the following passage:

"Estoppel by the acceptance of benefits: Estoppel is frequently based upon the acceptance and retention, by one having knowledge or notice of the facts, of benefits from a transaction, contract, instrument, regulation which he might have rejected or contested. This doctrine is obviously a branch of the rule against assuming inconsistent positions.
As a general principle, one who knowingly accepts the benefits of a contract or conveyance is estopped to deny the validity or binding effect on him of such contract or conveyance.
This rule has to be applied to do equity and must not be applied in such a manner as to  violate the principles of right and good conscience."
18. For the reasons set out by us hereinabove, we have no hesitation in holding that the appellant was not entitled to question the terms of the Migration Package after unconditionally accepting and acting upon the same.

19. In the result this appeal fails and is hereby dismissed but in the circumstances without any order as to costs."""

doc_nlp = nlp(judgement_text_unprocessed)
sents_array = []
sents_response_array = []
case_ids = []


for sent in doc_nlp.sents:
    case_ids = []
    score = 0
    sents_array.append({"text": sent.text, "weight": score,"cited_ids": [],
                       "date_range": {"start": "2021-06-01T07:21:51", "end": "2021-06-01T07:21:51"}})

# for id in range(46, 47):
#     sent_response = es.search(index="similarity_sample", body={
#         "track_total_hits": True,
#         "_source": "*",
#         "query": {"match": {"_id": id}}})

#     print("processing case " + str(id))

#     sents_response_array = []
#     for i in sent_response['hits']['hits'][0]['_source']['jt']:
#         sents_response_array.append(
#             {"text": i['text'], "cited_ids": i['cited_ids'], "weight": i['weight'], "date_range": i['date_range']})

#1. array of all scores vs ids
#2. avg scores
#3. max scores

    # for sent in sents_response_array:
    #     avg_score = 0
    #     max_score = 0
    #     sent_cases_ids = []
    #     inter_cases_response = es.search(index="similarity_sample", body={
    #         "track_total_hits": True,
    #         "_source": "_id",
    #         "query": {
    #             "more_like_this": {
    #                 "fields": [
    #                     "jt.text"
    #                 ],
    #                 "like": sent['text'],
    #                 "min_term_freq": 1,
    #                 "max_query_terms": 500,
    #                 "min_doc_freq": 1,
    #                 "minimum_should_match": 1
    #             }
    #         }
    #     }
    #     )
    #     count = 0
    #     for i in inter_cases_response['hits']['hits']:
    #         sent_cases_ids.append({"id": i['_id'],"score":float(i['_score'])})
    #         avg_score = (avg_score*count + i['_score'])/(1+count)
    #         count = count + 1
    #         if(max_score<i['_score']):
    #             max_score = i['_score']
    #     sent['cited_ids'] = sent_cases_ids
    #     sent['avg_score'] = float(avg_score)
    #     sent['max_score'] = float(max_score)
    #     print('avg_score:' + str(avg_score))
    #     print('max_score:' + str(max_score))
    #     print("*")

    # print("storing "+ str(id) +" in similarity_search")
    # response = es.index(
    #     index="similarity_sample",
    #     id=id,
    #     # only change this id on next document
    #     body={"jt": sents_response_array}
    # )
    # print(response)

print("storing in self_sample")
body = {"jt": sents_array}
print(len(sents_array))
response = es.index(
    index="self_sample",
    id=2,
    body=body
)
print("stored in self_sample")

for sent in doc_nlp.sents:
    case_ids = []
    score = 0
    weight = 0
    sents_array.append({"text": sent.text, "weight": weight,"cited_ids": [],
                       "date_range": {"start": "2021-06-01T07:21:51", "end": "2021-06-01T07:21:51"}})
    print("req generated")
    sent_response = es.search(index="self_sample", body={
        "track_total_hits": True,
        "_source": "",
        "query": {
            "more_like_this": {
                "fields": [
                    "jt.text"
                ],
                "like": sent.text,
                "min_term_freq": 1,
                "max_query_terms": 500,
                "min_doc_freq": 1,
                "minimum_should_match": 1
            }
        }
    }
    )
    count = 0
    for i in sent_response['hits']['hits']:
        count = count+1
        # case_ids.append(i["_id"])
        # if(score<i['_score']):
        #     score = i['_score']
        score = (score*count + i['_score'])/(count + 1)
        if score!=0:
            print(score)
    sents_response_array.append({"text": sent.text, "cited_ids": case_ids, "weight":float(score), "date_range": {"start": "2021-06-01T07:21:51", "end": "2021-06-01T07:21:51"}})

print("deleting from self_sample")
response = es.index(
    index="self_sample",
    id=1,
    body={"jt": []}
)



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
sorted_sents_response = sorted(sents_response_array, key = lambda k: k['weight'], reverse = True)
# sorted_sents_response = sents_response_array.sort(
#     key=extract_score, reverse=True)

body = {"jt": sents_response_array}
print(len(sents_array))


response = es.index(
    index="similarity_sample",
    id=10,
    body=body
)
print(response)



# for i in sents_response_array[0:30]:
#     print("score: " + str(i['weight']))
#     print("text: " + i['text'])
#     print("cited_ids: ")
#     for j in i['cited_ids']:
#         print(j)
#     print("****")