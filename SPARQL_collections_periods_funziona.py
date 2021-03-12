#periodi artistici più rappresentati in ogni paese
import rdflib
from rdflib import Namespace , Literal , URIRef
from rdflib.namespace import RDF , RDFS

wd = Namespace("http://www.wikidata.org/entity/") 
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")

# create an empty Graph
g = rdflib.ConjunctiveGraph()


result = g.parse(r"D:\Università bologna cose mie\dhdk epds\resources\artchives.nq", format='nquads')



query_coll_periods_a = g.query("""
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wdp: <http://www.wikidata.org/wiki/Property:>
PREFIX art: <https://w3id.org/artchives/>
SELECT DISTINCT ?coll ?nameColl ?period ?periodLabel
WHERE {
 
 ?coll art:hasSubjectPeriod ?period .
 ?coll rdfs:label ?nameColl . 
 ?period rdfs:label ?periodLabel .
}
GROUP BY ?coll ?nameColl ?period ?periodLabel 
""")
#LA QUERY E' GIUSTA!


import csv
with open('coll_periods.csv', mode='w') as my_file:
    my_writer = csv.writer(my_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    #write the column names
    my_writer.writerow(['collection','collection_name', 'period', 'period_label'])
    
    #access the rows of the query results
    for coll, nameColl, period, periodLabel in query_coll_periods_a:
        #write in the csv
        my_writer.writerow([coll, nameColl, period, periodLabel])
        

import pandas as pd
patients_df = pd.read_csv("coll_periods.csv")
patients_df.head(30)
