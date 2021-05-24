import rdflib
import csv
from rdflib import Namespace , Literal , URIRef
from rdflib.namespace import RDF , RDFS


wd = Namespace("http://www.wikidata.org/entity/") # remember that a prefix matches a URI until the last slash (or hashtag #)
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")
#we do not need to use sparqlwrapper wikidata endpoint!

# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format
result = g.parse("artchives.nq", format='nquads')

set_keepers = set()
for s,p,o in g.triples((None, None , wd.Q31855)):   
    for s1,p1,o1 in g.triples(( o, RDFS.label, None)):  
        set_keepers.add(o1.strip())
for keepers in set_keepers:
    print(keepers)

query_keepers = g.query('''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wdp: <http://www.wikidata.org/wiki/Property:>
PREFIX art: <https://w3id.org/artchives/>

SELECT * 
WHERE {
 ?keeper a wd:Q31855 ; rdfs:label ?nameKeeper . 
 ?keeper wdt:P17 ?country .
 ?country rdfs:label ?nameCountry .
 ?collection wdt:P170 ?artHistorian .
 ?artHistorian rdfs:label ?nameHistorian . 
 ?collection rdfs:label ?nameCollection .
}
''') 

with open('keepers.csv', 'wt') as out_file:
    csv_writer = csv.writer(out_file, delimiter=';')
    csv_writer.writerow(['keeper', 'name_keeper', 'country', 'name_country', 'collection', 'artHistorian', 'name_Historian', 'name_collection'])
    for row in query_result:
        csv_writer.writerow([row.name.strip(), row.ind]) #se metto row.name mi da i nomi dei paesi, ma non leva i doppioni
        
import pandas as pd
data = pd.read_csv('keepers.csv', encoding = 'Latin-1')
# print the first 5 rows
data.head()
