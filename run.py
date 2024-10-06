import build, ontology, queries
     
from owlready2 import *
from rdflib import *

fix = Namespace("http://ifixit.org/mac.owl#")
mac = get_ontology("http://ifixit.org/mac.owl")

mac = ontology.create_ontology(mac)

graph = default_world.as_rdflib_graph()
graph = build.parse_json_to_graph("data.json", graph, fix, mac)

queries.run_queries(graph, mac)

