import rdflib
import csv


# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format
result = g.parse("artchives3_birthplaces.nq", format='nquads')


qres = g.query(
  """PREFIX wdt: <http://www.wikidata.org/prop/direct/>
  SELECT DISTINCT  ?historian ?birthplace
  WHERE { 
     ?historian wdt:P19 ?birthplace .
     }
    """)
#NOTA BENE: LA QUERY P170 NON C'è IN ARTCHIVES3_BIRTHPLACES, c'è in ARTCHIVES, bisogna combinare file e dataframes :) 
with open('FG_test_birth.csv', 'wt') as out_file:
    csv_writer = csv.writer(out_file, delimiter=';')
    csv_writer.writerow(['Historian', 'Birthplace'])
    for row in qres:
        csv_writer.writerow([row.historian, row.birthplace])
        
import pandas as pd
data = pd.read_csv('FG_test_birth.csv', encoding = 'Latin-1')
# print the first 5 rows
data.head()
