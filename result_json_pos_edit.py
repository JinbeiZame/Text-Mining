from pymongo import MongoClient
from prettytable import PrettyTable
from pycorenlp import *
nlp = StanfordCoreNLP("http://localhost:9000/")
#sentence = 'Sombut has travel on tokyo,We visited the Kiyomizu-dera temple,they go to home after the sunset'
#sentence = 'Although Mrs. Smit had a lot monry, She made poor use of it.'
#sentence = 'Edwin told Kenny that Dr. Wilson suspected that he cheated on the chemistry exam.'
#sentence = 'John had just set down the overstuffed sandwich when he spotted a cockroach on the table, He smashed it with his open palm before he could eat.'
sentence = 'Sombut has travel on tokyo,We visited the Kiyomizu-dera temple,they go to home after the sunset.Although Mrs. Smit had a lot monry, She made poor use of it.John had just set down the overstuffed sandwich when he spotted a cockroach on the table, He smashed it with his open palm before he could eat.'
#sentence =
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
