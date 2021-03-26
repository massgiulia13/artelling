#BIRTHPLACE
import rdflib
from rdflib import Namespace , Literal , URIRef
from rdflib import URIRef 
from rdflib.namespace import RDF , RDFS
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON, CSV
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# get the endpoint API
wikidata_endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"

wd = Namespace("http://www.wikidata.org/entity/") # remember that a prefix matches a URI until the last slash (or hashtag #)
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")

# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format into the graph
result = g.parse(r"D:\Università bologna cose mie\dhdk epds\resources\artchives.nq", format='nquads')

arthistorians_list = set() #crei il set così non ci sono le ripetizioni

for s,p,o in g.triples((None, wdt.P170, None)):
    if "www.wikidata.org/entity/" in str(o):
        arthistorians_list.add("<" +str(o) + ">")
        
#print(arthistorians_list) #questo ce lo dà come set, con risultati separate da virgole

arthistorians = ' '.join(arthistorians_list) #così unisci tutti i risultati
#print(arthistorians)

#len(arthistorians)

birthplace_query = """
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT DISTINCT ?historian ?historian_name ?birthplace ?birthplace_label
WHERE {
    VALUES ?historian {"""+arthistorians+"""} . # look how we include a variable in a query string!
    ?historian wdt:P19 ?birthplace ;
               rdfs:label ?historian_name . 
    ?birthplace rdfs:label ?birthplace_label .
    FILTER (langMatches(lang(?birthplace_label), "EN"))
    FILTER (langMatches(lang(?historian_name), "EN"))
    } 
"""
# set the endpoint 
sparql_wd = SPARQLWrapper(wikidata_endpoint)
# set the query
sparql_wd.setQuery(birthplace_query)
# set the returned format
sparql_wd.setReturnFormat(JSON)
# get the results
results = sparql_wd.query().convert()


#--------json result ------

#for result in results["results"]["bindings"]:
    #print(result)
    
import os.path  
import pandas as pd
import json
import pprint

#with open("data_query_birthplaces_a.json", "w") as write_file:
    #json.dump(results, write_file)
    
#with open("data_query_birthplaces_a.json", "r") as read_file:
    #data = json.load(read_file)
    #pprint.pprint(data)
    
save_path = r'C:\Users\Giulia\Desktop\tutorial'

name_of_file = 'data_query_birthplaces_a'

completeName = os.path.join(save_path, name_of_file+'.json')         


with open(completeName, "w")as write_file:
          json.dump(results, write_file)

with open("data_query_birthplaces_a.json", "r") as read_file:
    data = json.load(read_file)
    pprint.pprint(data)
    
#output=il file json nella directory che vuoi, metto tutto su github


