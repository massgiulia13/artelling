import rdflib
from rdflib import Namespace , Literal , URIRef
from rdflib import URIRef 
from rdflib.namespace import RDF , RDFS
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
import json
import pandas as pd
import pprint
import os
import csv

ssl._create_default_https_context = ssl._create_unverified_context

# get the endpoint API
wikidata_endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format into the graph
result = g.parse(r"D:\Università bologna cose mie\dhdk epds\resources\artchives.nq", format='nquads')

wd = Namespace("http://www.wikidata.org/entity/") # remember that a prefix matches a URI until the last slash (or hashtag #)
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")

arthistorians_list = set() #crei il set così non ci sono le ripetizioni

for s,p,o in g.triples((None, wdt.P170, None)):
    if "www.wikidata.org/entity/" in str(o):
        arthistorians_list.add("<" +str(o) + ">")
        
#print(arthistorians_list) questo ce lo dà come set, con risultati separate da virgole

arthistorians = ' '.join(arthistorians_list) #così unisci tutti i risultati
#print(arthistorians)

birthplace_query = """
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT DISTINCT  ?historian ?historian_label ?birthplace ?birthplace_label
WHERE {
   VALUES ?historian {"""+arthistorians+"""} .  #include the variable in the query string
   ?historian rdfs:label ?historian_label .
   ?historian wdt:P19 ?birthplace .
   ?birthplace rdfs:label ?birthplace_label . 
   FILTER (langMatches(lang(?birthplace_label), "EN"))
   FILTER (langMatches(lang(?historian_label), "EN"))
   }
"""

endpoint = SPARQLWrapper(wikidata_endpoint)
endpoint.setQuery(birthplace_query)
endpoint.setReturnFormat(JSON)

results = endpoint.query().convert()

bindings = results["results"]["bindings"]
for binding in bindings:
    data = binding["historian_label"]["value"], binding["birthplace_label"]["value"]
    #for d in data:
        #if d not in data:
            #data.update(d)
    #print(data)
    
    df = pd.DataFrame([data], columns=["historian", "birthplace"])
#df = pd.read_json(data)
    df.to_csv()
    df.drop_duplicates("historian", keep = "last")
    df.drop_duplicates("birthplace", keep = "last")
    pprint.pprint(df)
