#BIRTHPLACE
import rdflib
from rdflib import Namespace , Literal , URIRef
from rdflib import URIRef 
from rdflib.namespace import RDF , RDFS
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# get the endpoint API
wikidata_endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format into the graph
result = g.parse("artchives.nq", format='nquads')

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
SELECT DISTINCT ?birthplace ?birthplace_label ?historian ?historian_label 
WHERE {
   VALUES ?historian {"""+arthistorians+"""} .  #include the variable in the query string
   ?historian rdfs:label ?historian_label .
   ?historian wdt:P19 ?birthplace .
   ?birthplace rdfs:label ?birthplace_label . 
   FILTER (langMatches(lang(?birthplace_label), "EN"))
   FILTER (langMatches(lang(?historian_label), "EN"))
   }
"""

#wikidata_endpoint = "https://query.wikidata.org/" o questo?

# set the endpoint 
sparql_wd = SPARQLWrapper(wikidata_endpoint)
# set the query
sparql_wd.setQuery(birthplace_query)
# set the returned format
sparql_wd.setReturnFormat(JSON)
# get the results
results = sparql_wd.query().convert() 
for result in results["results"]["bindings"]:
    historian_uri = result ["historian"]["value"]
    if "historian_label" in result:
        historian_label = result["historian_label"]["value"]
    print(historian_label + ":", historian_uri)
    if "birthplace" in result:
        birthplace = result["birthplace"]["value"]
        if "birthplace_label" in result:
            birthplace_label = result["birthplace_label"]["value"]
            print("born in:", birthplace, birthplace_label)
            #se ci stanno sia URI CHE LABEL DEL NOME nel grph
            g.add((URIRef(historian_uri) , URIRef(wdt.P19) , URIRef(birthplace) ))
            g.add((URIRef(birthplace) , RDFS.label , Literal(birthplace_label) ))
        
    else:
        print("Non ce n'è, non ce niente!")



g.serialize(destination= r'C:\Users\Giulia\Desktop\tutorial\artchives3_birthplaces.nq', format='nquads') #su questo artchives3 sono serializzate le proprietà birthplacesp19
#lo carico qua su github 

