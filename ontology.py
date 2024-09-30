from owlready2 import *
from rdflib import *
import json


mac = get_ontology("http://ifixit.org/mac.owl")

def parse_json_to_graph(file_path: str, graph: Graph):
    print(type(graph))
    try:
        with open(file_path, 'r') as file:
            for line in file:
                graph.add((URIRef("http://ifixit.org/mac.owl"), URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://www.w3.org/2002/07/owl#Ontology")))
                try:
                    entry = json.loads(line)
                    for key, value in entry.items():
                        # Add triples to the graph based on the JSON entry
                        graph.add((URIRef(f"http://ifixit.org/mac.owl#{key}"), URIRef("http://www.w3.org/2000/01/rdf-schema#label"), URIRef(Literal(value))))
                    input("Press spacebar to view the next entry...")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from line: {line.strip()}")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")

with mac:
    class Procedure(Thing):
        pass

    class Step(Thing):
        pass

    class Toolbox(Thing):
        pass

    class Tool(Thing):
        pass

    class Item(Thing):
        pass

    class Part(Thing):
        pass

    class Image(Thing):
        pass

    class Procedure(Thing):
        has_steps = [Step]
        has_toolbox = Toolbox

    class Toolbox(Thing):
        has_tools = [Tool]
        has_parts = [Part]
        has_items = [Item]

    class Step(Thing):
        has_images = [Image]

    mac.save("mac.owl")
    graph = default_world.as_rdflib_graph()
    parse_json_to_graph(
        "data.json", graph
    )
    print(graph.serialize(format="turtle"))







