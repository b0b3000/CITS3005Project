import build_old, ontology, queries, build
     
from owlready2 import *
from rdflib import *

ONTO_FILE_PATH = "mac.owl"
JSON_FILE_PATH = "data.json"
RDFXML_FILE_PATH = "rdf_out.xml"

fix = Namespace("http://ifixit.org/mac.owl#")
mac = get_ontology("http://ifixit.org/mac.owl")

ontology.create_ontology(mac, ONTO_FILE_PATH)
mac = get_ontology(ONTO_FILE_PATH).load()


graph, mac = build.parse_data_to_owl(JSON_FILE_PATH, ONTO_FILE_PATH, RDFXML_FILE_PATH, fix, mac)

#queries.run_queries(graph, mac)

