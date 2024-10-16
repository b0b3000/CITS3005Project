import rdflib
from pyshacl import validate

SHAPES_PATH = "shapes.ttl"


def validate_ontology_shacl(graph):
    #mac = rdflib.Graph()
    #mac.parse(ontology_path, format='turtle')

    shapes_graph = rdflib.Graph()
    shapes_graph.parse(SHAPES_PATH, format='turtle')
    conforms, report, report2 = validate(graph, shacl_graph=shapes_graph, ont_graph="test.owl")

    if conforms:
        print("Ontology conforms to SHACL shapes.")
    else:
        print("Ontology does not conform to SHACL shapes.")
        print(report, report2)
