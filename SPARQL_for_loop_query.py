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

for result in results["results"]["bindings"]: #si sta iterando nel risultato della query che è nella variabile results! 
        collection = result["coll"]["value"]
        if "collName" in result:
            collName = result["collName"]["value"]
            print(collName + ":" , collection)
        if "artHistorian" in results:
            artHistorian_uri = result["artHistorian"]["value"]
            if "nameHistorian" in result:
                print(nameHistorian + ":", historian_uri)
        if "period" in result:
            period = result["period"]["value"]
            if "periodLabel" in result:
                periodLabel = result["periodLabel"]["value"]
            print(periodLabel + ":", period)
            #se ci stanno sia URI CHE LABEL DEL NOME nel grph
            g.add((URIRef(coll) , URIRef(wdt.P170) , URIRef(artHistorian) ))
            g.add((URIRef(artHistorian) , RDFS.label , Literal(nameHistorian) ))
            g.add((URIRef(coll) , RDFS.label , Literal(collName) ))
            g.add((URIRef(coll) , URIRef(art.hasSubjectPeriod) , URIRef(period) ))
            g.add((URIRef(period) , RDFS.label , Literal(periodLabel) ))

        else:
            print("Non ce n'è, non ce niente!")
            
            #il risultato è una roba vuota 
#poi si deve serializzare 
