# -*- coding: utf-8 -*-

import codecs
import sys, locale, os
import re
from pymongo import MongoClient
#from prettytable import PrettyTable
from pycorenlp import *
#import textract
import textract
#from pymongo import MongoClient
import json

nlp = StanfordCoreNLP("http://localhost:9000/")
#sentence = 'Beam used his former employer as a reference when he applied for his new job.'
#sentence = 'Kaiser has travel on Hogsmeade Village, He visited the Honeydukes, He go to Hogsmeade Village after the sunset, He had been sitting in a chair,Kaiser has travel on the Honeydukes,We visited Hogsmeade Village.'
#sentence = 'John has snoring loudly,he had been sitting in a chair,Sombut has travel on tokyo,he visited the Kiyomizu-dera temple,they go to home after the sunset.'
#sentence = 'Edwin told Kenny that Dr. Wilson suspected that he cheated on the chemistry exam.'
#sentence = "harry was snoring loudly. He had been sitting in a chair beside his bedroom window," +  \
#			"and Ron had finally fallen asleep with one side of his face pressed against the clod windowpane."
#sentence = 'John had just set down the overstuffed sandwich when he spotted a cockroach on the table, sam is running into the room he can not sleep.'
#sentence = 'John has travel on tokyo, he visited the Kiyomizu-dera temple,he go to home after the sunset, he had a lot monry, She made poor use of it.John had just set down the overstuffed sandwich when he spotted a cockroach on the table, He smashed it with his open palm before he could eat.John had just set down the overstuffed sandwich when he spotted a cockroach on the table, He smashed it with his open palm before he could eat.'
#sentence =' I love my mom. She took care of me when I was very young. She took care of me when I was sick. She taught me how to read. She taught me how to get dressed. She taught me how to button my shirt. She taught me how to tie my shoes. She taught me how to brush my teeth. She taught me to be kind to others. She taught me to tell the truth. She taught me to be polite. She took me to school on my first day of school. She held my hand. She helped me with my homework. She was nice to all my friends. She always cheered me up. Next year I will graduate from high school. I will go to college. I will do well in college. I will do well after college. My mom has taught me well.'
#print (type(sentence))

#sentence = 'we have about three hundred registrations for student Sacraments and therefore your co operation in meeting these deadlines is imperative.'
#sentence = sentence1.replace(u'\xa0', u' ')
#sentence = sentence1.encode('ascii', 'ignore')

#sentence = 'Beam love my mom. She took care of me when I was very young. '


text_file = open("file_extract.txt", "w")
text_file.write(textract.process("simple1.pdf"))
text_file.close()   #close file
print text_file

with open('file_extract.txt', 'r') as myfile:
    sentence=myfile.read().replace('\n', '').replace('\n', '/').replace('\n', '—').replace('\n', '’')
#print type(sentence)
sentence = sentence.replace(',', '')
#print sentence

output = nlp.annotate(sentence,
			properties={"annotators": "coref",
					"outputFormat": "json", "openie.triple.strict": "true"})
#print(output)
corefs = output['corefs']
tokens = output['sentences'][0]['tokens']
#print(corefs)
#print(tokens)
sent = [t['word'] for t in tokens]

print type(sent)
for  i in corefs:
	#print(corefs)
	mention = ''
	for  j in corefs[i]:
         print j['isRepresentativeMention']
         print mention
        if j['isRepresentativeMention'] == True:
            mention = j['text']
            print  j['text']
        else:
            sent[j['startIndex']-1] = mention
            print j['text']
print(sent)
'''
for i in corefs:
    mention = ''
    for j in corefs[i]:
        if j['isRepresentativeMention'] == True:
            mention = j['text']
        else:
            (sent[j['startIndex']-1]).append(mention)
print sent
'''
#sentence.close()

sent = ' '.join(t for t in sent).encode("utf-8")
output = nlp.annotate(sent,
			properties={"annotators": "openie",
					"outputFormat": "json", "openie.triple.strict": "true"})
relation = output['sentences'][0]['openie']
#print(relation)

client = MongoClient()
db = client.Textmining
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

#for inning in relation:
	#print(inning['subject'], inning['relation'], inning['object'])
store0 = [t['relationSpan'] for t in relation]
store = [t['relationSpan'][0] for t in relation]
store1 = [t['relationSpan'][1] for t in relation]

#print(len(store0))
#print(store0)
#print(store0)
len_store = len(store0)
#print(len_store)

#for i in store0:
#print(store0)

mylist = store0
# -*- coding: utf-8 -*-
from collections import Iterable

#x = [[14, 15], [14, 15], [14, 15], [26, 27], [26, 27], [15, 17],[26, 28], [14, 15], [14, 15], [26, 27], [26, 27], [15, 17]]
x = store0
countt =1
#print x

'''
for d, fel  in enumerate(sort_list):
    xx = [ [ j for j in store0[i] if i != fel ] for i in range(len(store0)) ]    #delete duplicate index
print xx '''
text_file = open("Output.txt", "w")
for el in list(x):
        #print ( " ".join([str(index) for index, value in enumerate(x) if value == el]))
        text_file.write( " ".join([str(index) for index, value in enumerate(x) if value == el]))
        text_file.write('\n')
text_file.close()
#print text_file
text_file1 = open("Output1.txt", "w")
for el in list(x):

    text_file1.write(" ".join([str(index) for index, value in enumerate(x) if value == el]))
    text_file1.write('\n')
text_file1.close()

with open('Output.txt', 'r') as file1:
    with open('Output1.txt', 'r') as file2:
        same = set(file1).intersection(file2)
        print same
same.discard('\n')

with open('some_output_file.txt', 'w') as file_out:
    for line in same:
        file_out.write(line)


f = open("some_output_file.txt", "r")
g = open("intersection.txt", "w")
#print  g
for line in f:

    if line.strip():
        g.write("\n".join(line.split()[1:]) + "\n")

f.close()
g.close()


f = open("intersection.txt", "r")
contents = f.readlines()
#print contents
f.close()

contents.insert(0, "\n")                                 #Insert \n in first line text file

f = open("intersection1.txt", "w")
contents = "".join(contents)
#print contents
f.write(contents)
f.close()


with open('intersection.txt') as f:
    h = [int(x) for x in next(f).split()]
    array = [[int(x) for x in line.split()] for line in f]
    #print array

list2 = [x for x in array if x]
#print(list2)



def flatten(list2):
    for item in list2:
        if isinstance(item, Iterable) and not isinstance(item, basestring):
            for x in flatten(item):
                yield x                                                             #Convert nest list to list of integer
        else:
            yield item

#print(list(flatten(list2)))
import numbers
CNLTLOI = list(flatten(list2))
#print CNLTLOI
results_integer = list(map(int, [x for x in CNLTLOI if isinstance(x, numbers.Number)]))
#print results_integer

sort_list = sorted(results_integer, reverse=False)
#print(sort_list)    #array had a duplicated

'''#mylist = [[14, 15], [14, 15], [14, 15], [26, 27], [26, 27], [15, 17],[26, 28], [14, 15], [14, 15], [26, 27], [26, 27], [15, 17]]
m=0
index=[]
inde =0
for i, j in enumerate(mylist[:-1]):
    if j  == mylist[i+1]:
        #mylist[i] = m
        mylist[i+1] =m+1
    m+=1
#print mylist
'''
import numbers
#print(type([x for x in mylist if isinstance(x, numbers.Number)]))   #integer only
#results = list(map(int, [x for x in mylist if isinstance(x, numbers.Number)]))
#print type(results)
#print results
count = 0

#for idx, val in enumerate(sort_list):
#    print(idx, val)
indd =0
a = []
for indd, val in enumerate(sort_list):
    a.append(val)
    #print val
	#indd+=1
#print type(a)
#print a
#print indd
'''
aa = []
for i in enumerate(sort_list):
     aa.append(a.pop(-1))
#print  type(aa)

for ii,i in enumerate(aa):
   print aa[ii]

del aa[1]

print aa
'''
'''
for d, fel  in enumerate(sort_list):
            xx = [ [ j for j in store0[i] if j != aa ] for i in range(len(store0)) ]    #delete duplicate index
            print (" ")

print xx'''
aa = []
save = []
for i in enumerate(sort_list):
     aa.append(a.pop())
#print  type(aa)
store01 =store0
#print store01
for ii,i in enumerate(sort_list):
    for y , x in enumerate(store01):
        if y == aa[ii]:
            del store01[aa[ii]]
#print store01


aa1 = []
save1 = []
for i in enumerate(sort_list):
     aa1.append(aa.pop())
#print  type(aa1)
store001 =store01
#print store001
for ii,i in enumerate(sort_list):
    for y , x in enumerate(store001):   # round 2
        if y == aa1[ii]:
            del store001[aa1[ii]]
#print store001


'''
for d, fel  in enumerate(sort_list):


    print ([ [ for j in store0[i] if i != fel ] for i in range(len(store0)) ] )   #delete duplicate index
    print fel

'''
count = 0
for b, sec in enumerate(store001):
          count+=1
hr = count
#for ii, i in enumerate(store001):
for rel in enumerate(relation):
    #print rel


    for j, rel in enumerate(relation):

        for b, sec in enumerate(store001):
            if count > 0:
                        if rel['relationSpan'] != ( ii for i in range(len(store001))):
                            if store001[b] == rel['relationSpan']:
                                #print store001[b]
                                #print rel['relationSpan']
                                #print ('\n')
                                result = db.relation.insert_one(
                                    {
                                        "subject": rel['subject'].lower(),
                                        # "subject": stemmer.stem(rel['subject']),
                                        "relation": rel['relation'].lower(),
                                        # "relation": stemmer.stem(rel['relation']),
                                        "object": rel['object'].lower()
                                        # "object": stemmer.stem(rel['object'])

                                    }
                                )
                                count -= 1
                        else:
                            print ("Equal")





'''


for rel in relation:

        result = db.relation.insert_one(
	    {
	    	"subject" : rel['subject'].lower(),
			#"subject": stemmer.stem(rel['subject']),
	    	"relation" : rel['relation'].lower(),
			#"relation": stemmer.stem(rel['relation']),
	    	"object" : rel['object'].lower()
			#"object": stemmer.stem(rel['object'])

	    }
	)
'''
#sum += 1

#How to receieve value from php or python input browser ??
client = MongoClient()
db = client.Textmining

#re1 = db.relation.remove( { "subject" : { "$ne": "Mrs. Smit" },{}} )           #use remove not good for this can u try

#result = db.relation.find({"$or": [{"subject": "Mrs. Smit"}, {"object": "Mrs. Smit"}]}) #use find and "@and" it so well on time in this version
#print(result)
#db.relation.find({"$and": [{"subject": "Josh"}, {"object": "Josh"}]}) #use find and "@and" it so well on time in this version
#with open('result1.json', 'w') as fp:
#    json.dump(re1, fp)

#results = db.getCollection('relation').find({"subject" : "Sombut"})
#print(results)
#posts.insert(new_posts)
#t = PrettyTable(['Word', 'part-of-speech'])

#for w in output['sentences'][0]['tokens']:
#	print([w['word'], w['pos']])
import cgi
form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')



client = MongoClient()
db = client.Textmining
#db = client.results

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

#{"$or": [{"subject": "kaiser"}]}
class_r = {}
count = 1
for row in db.relation.find({"$or": [{"subject": "he"}]}):    #precision to find the subject that interesting ex.. subject as beam and object as beam together
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


