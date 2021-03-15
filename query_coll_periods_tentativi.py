#periodi artistici più rappresentati in ogni paese
import rdflib
from rdflib import Namespace , Literal , URIRef
from rdflib import URIRef 
from rdflib.namespace import RDF , RDFS
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON, CSV
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

# get the endpoint API
wikidata_endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format into the graph
result = g.parse(r"D:\Università bologna cose mie\dhdk epds\resources\artchives.nq", format='nquads')

wd = Namespace("http://www.wikidata.org/entity/") 
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")

query_coll_periods = """
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wdp: <http://www.wikidata.org/wiki/Property:>
PREFIX art: <https://w3id.org/artchives/>
SELECT DISTINCT ?coll ?collName ?artHistorian ?nameHistorian ?period ?periodLabel
WHERE {
  ?coll wdt:P170 ?artHistorian ;
        rdfs:label ?collName ;
        art:hasSubjectPeriod ?period .
  ?artHistorian rdfs:label ?nameHistorian .
  ?period rdfs:label ?periodLabel . 

}
GROUP BY ?coll ?collName ?artHistorian ?nameHistorian ?period ?periodLabel
"""
#LA QUERY E' GIUSTA!

# set the endpoint 
sparql_wd = SPARQLWrapper(wikidata_endpoint)
# set the query
sparql_wd.setQuery(query_coll_periods)
# set the returned format
sparql_wd.setReturnFormat(JSON) 
# get the results
results = sparql_wd.query().convert()

import json
with open("data_query_coll_periods.json", "w") as write_file:
    json.dump(results, write_file)
    
with open("data_query_coll_periods.json", "r") as read_file:
    data = json.load(read_file)
    print(data)

#il risultato è un json vuoto :(   

#alternativo, con risultato in csv
#sparql_wd.setReturnFormat(CSV) 
#import csv
#with open("coll_historian_periods.csv", mode='w'):
    #my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    #write the column names
    #my_writer.writerow(['collection', 'collection_label', 'artHistorian', 'nameHistorian', 'period', 'period_label'])
    
    #access the rows of the query results
    #for coll, collName, artHistorian, nameHistorian, period, periodLabel in query_coll_periods:
        #write in the csv
        #my_writer.writerow([coll, collName, artHistorian, nameHistorian, period, periodLabel])
    
        #(#if ',' not in query_coll_periods:
             #continue
        #coll, collName, artHistorian, nameHistorian, period, periodLabel = line.strip().split(','))
        

#import pandas as pd
#hist_coll_per_df = pd.read_csv("coll_historian_periods.csv")
#hist_coll_per_df.head()
#il risultato è ValueError: I/O operation on closed file.
