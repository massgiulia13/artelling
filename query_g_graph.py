import rdflib
import requests

# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format
result = g.parse(r"C:\Users\giulm\OneDrive\Documenti\DHDK_EPDS\epds-main\resources\artchives.nq", format='nquads')


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
