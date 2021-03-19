import rdflib
from rdflib import Namespace , Literal , URIRef
from rdflib.namespace import RDF , RDFS


# create an empty Graph
g = rdflib.ConjunctiveGraph()

result = g.parse(r"C:\Users\Giulia\Desktop\tutorial\artchives3_birthplaces.nq", format='nquads')  #uso il file ricavato

wd = Namespace("http://www.wikidata.org/entity/") # remember that a prefix matches a URI until the last slash (or hashtag #)
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")

birthplaces_list = set() #crei il set così non ci sono le ripetizioni

for s,p,o in g.triples((None, wdt.P19, None)):
    if "www.wikidata.org/entity/" in str(o):
        birthplaces_list.add("<" +str(o) + ">")
#prendo  birhtplaces da sto artchives3 --> serializzato dalla query "birthplaces", visto che in artchives.nq non ci sta la proprietà P19

birthplaces = ' '.join(birthplaces_list) #così unisci tutti i risultati

#print(birthplaces)

arthistorians_list = set() #crei il set così non ci sono le ripetizioni

for s,p,o in g.triples((None, wdt.P170, None)):
    if "www.wikidata.org/entity/" in str(o):
        arthistorians_list.add("<" +str(o) + ">")
        
#print(arthistorians_list) questo ce lo dà come set, con risultati separate da virgole#include the variable in the query string

arthistorians = ' '.join(arthistorians_list) #così unisci tutti i risultati

query_birthplaces = g.query("""
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT DISTINCT  ?historian ?historian_label ?birthplace ?birthplace_label 
WHERE {
   VALUES ?birthplaces {"""+birthplaces+"""} ?historian {"""+arthistorians+"""} .  
   ?birthplace rdfs:label ?birthplace_label .
   ?historian rdfs:label ?historian_label .
   
   
   FILTER (langMatches(lang(?birthplace_label), "EN"))
   FILTER (langMatches(lang(?historian_label), "EN"))
   }
""")
#LA QUERY E' GIUSTA! #hai importato i set dei birthplaces e degli arthistorians, e cerchi i labels 


import csv
with open('birthplaces_creators.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    # write the column names
    my_writer.writerow(["historian", "historian_label", "birthplace", "birthplace_label"])
    
    # access the rows of the query results
    for historian, historian_label, birthplace, birthplace_label, coll in query_birthplaces:
        # write in the csv
        my_writer.writerow([historian, historian_label, birthplace, birthplace_label])
        

import pandas as pd
# parse the csv into a dataframe
data = pd.read_csv("birthplaces_creators.csv", encoding = 'Latin-1')
# print the first 5 rows
data.head()

#bene, mi dà una df vuota, ma non errore
