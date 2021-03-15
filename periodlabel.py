import rdflib
from rdflib import Namespace , Literal , URIRef
from rdflib.namespace import RDF , RDFS

wd = Namespace("http://www.wikidata.org/entity/") # remember that a prefix matches a URI until the last slash (or hashtag #)
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")

# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format into the graph
result = g.parse(r"C:\Users\diego\Desktop\dhdk_epds\resources\artchives_birthdates.nq", format='nquads')
query_coll_periods = g.query("""
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wdp: <http://www.wikidata.org/wiki/Property:>
PREFIX art: <https://w3id.org/artchives/>
SELECT DISTINCT ?coll ?artHistorian ?nameHistorian ?nameColl ?period ?periodLabel
WHERE {
 
 ?coll wdt:P170 ?artHistorian .
 ?artHistorian rdfs:label ?nameHistorian .
 ?coll rdfs:label ?nameColl .
 ?coll art:hasSubjectPeriod ?period .
 ?period rdfs:label ?periodLabel .
}
""")
#LA QUERY E' GIUSTA!


import csv
with open('artperiod.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    # write the column names
    my_writer.writerow(['collection', 'artHistorian', 'nameHistorian', 'collection_name', 'period', 'period_label'])
    
    # access the rows of the query results
    for coll, artHistorian, nameHistorian, nameColl, period, periodLabel in query_coll_periods:
        # write in the csv
        my_writer.writerow([coll, artHistorian, nameHistorian, nameColl, period, periodLabel])
        

import pandas as pd
# parse the csv into a dataframe
data = pd.read_csv("artperiod.csv", encoding = 'Latin-1')
# print the first 5 rows
data.head()
import rdflib
import requests

# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format
result = g.parse(r"C:\Users\diego\Desktop\dhdk_epds\resources\artchives.nq", format='nquads')


query_coll_periods = g.query("""
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
GROUP BY ?coll ?collName ?artHistorian ?nameHistorian ?period ?periodLabel""")


for query_res in query_coll_periods:
    print(query_res["coll"], query_res["collName"], query_res["artHistorian"], query_res["nameHistorian"], query_res["period"], query_res["periodLabel"])
