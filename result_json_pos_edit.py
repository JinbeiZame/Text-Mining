import codecs
from pymongo import MongoClient
from prettytable import PrettyTable
from pycorenlp import *

#from pymongo import MongoClient
import json

nlp = StanfordCoreNLP("http://localhost:9000/")
#sentence = 'Sombut has travel on tokyo,We visited the Kiyomizu-dera temple,they go to home after the sunset'
#sentence = 'Although Mrs. Smit had a lot monry, She made poor use of it.'
#sentence = 'Edwin told Kenny that Dr. Wilson suspected that he cheated on the chemistry exam.'
#sentence = 'John had just set down the overstuffed sandwich when he spotted a cockroach on the table, He smashed it with his open palm before he could eat.'
sentence = 'Sombut has travel on tokyo,We visited the Kiyomizu-dera temple,they go to home after the sunset.Although Mrs. Smit had a lot monry, She made poor use of it.John had just set down the overstuffed sandwich when he spotted a cockroach on the table, He smashed it with his open palm before he could eat.'
#sentence =

	#f = open('data_mining.txt', 'r')
	#sentence = f.read()
#sentencee = open('data_mining.txt', 'r', encoding='utf8')
#sentence =sentencee.read()
#f = codecs.open('data_mining.txt', 'r', 'UTF-8')
#sentence = f.read()
output = nlp.annotate(sentence,
			properties={"annotators": "coref",
					"outputFormat": "json", "openie.triple.strict": "true"})

corefs = output['corefs']
tokens = output['sentences'][0]['tokens']
#print(corefs)
sent = [t['word'] for t in tokens]
for i in corefs:
	mention = ''
	for j in corefs[i]:
		if j['isRepresentativeMention'] == True:
			mention = j['text']
		else:
			sent[j['startIndex']-1] = mention
#print(sent)
sent = ' '.join(t for t in sent).encode("utf-8")
output = nlp.annotate(sent,
			properties={"annotators": "openie",
					"outputFormat": "json", "openie.triple.strict": "true"})
relation = output['sentences'][0]['openie']
#print(relation)

client = MongoClient()
db = client.Textmining

for rel in relation:
	result = db.relation.insert_one(
	    {
	    	"subject" : rel['subject'],
	    	"relation" : rel['relation'],
	    	"object" : rel['object']
	    }
	)

#t = PrettyTable(['Word', 'part-of-speech'])

#for w in output['sentences'][0]['tokens']:
#	print([w['word'], w['pos']])


client = MongoClient()
db = client.Textmining

data = {
   "_comment":"Created with OWL2VOWL (version 0.3.1), http://vowl.visualdataweb.org",
   "header":{
      "languages":[
         "undefined"
      ],
      "baseIris":[
         "http://schema.org",
         "http://www.w3.org/2000/01/rdf-schema",
         "http://www.w3.org/2003/01/geo/wgs84_pos",
         "http://purl.org/dc/terms",
         "http://www.w3.org/2001/XMLSchema",
         "http://xmlns.com/foaf/0.1",
         "http://www.w3.org/2000/10/swap/pim/contact",
         "http://www.w3.org/2004/02/skos/core"
      ],
      "title":{
         "undefined":"Friend of a Friend (FOAF) vocabulary"
      },
      "iri":"http://xmlns.com/foaf/0.1/",
      "description":{
         "undefined":"The Friend of a Friend (FOAF) RDF vocabulary, described using W3C RDF Schema and the Web Ontology Language."
      },
      "other":{
         "title":[
            {
               "identifier":"title",
               "language":"undefined",
               "value":"Friend of a Friend (FOAF) vocabulary",
               "type":"label"
            }
         ]
      }
   },
   "namespace":[ ],
   "metrics":{},
   "class":[ ],
   "classAttribute":[ ],
   "property":[ ],
   "propertyAttribute":[ ],
   "datatype":[],
   "datatypeAttribute":[]
}


class_r = {}
count = 1
for row in db.relation.find({}):
	if row['subject'] not in class_r:
		data['class'].append({ "id": row['subject'], "type": 'owl:Class'})
		data['classAttribute'].append({
					"id": row['subject'],
					"label": {
			            "IRI-based": row['subject'],
			            "undefined": row['subject']
			        },
			        "comment":{
						"undefined":""
			        },
			        "iri" : ""
			})
		class_r[row['subject']] = True
	if row['object'] not in class_r:
		data['class'].append({ "id": row['object'], "type": 'owl:Class'})
		data['classAttribute'].append({
					"id": row['object'],
					"label": {
			            "IRI-based": row['object'],
			            "undefined": row['object']
			        },
			        "comment":{
						"undefined":""
					},
			        "iri" : ""
			})
		class_r[row['object']] = True
	id_property = 'property'+str(count)
	data['property'].append({"id":id_property , "type":"owl:objectProperty"})
	data['propertyAttribute'].append({	"id": id_property, 
									  	"domain": row['subject'],
									  	"range": row['object'],
									  	"label":{
								            "IRI-based":id_property,
								            "undefined":row['relation']
							        	},
										"comment":{
								            "undefined":""
								        },
								        "iri": ""
							        })
	count += 1
with open('result.json', 'w') as fp:
    json.dump(data, fp)


