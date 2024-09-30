from owlready2 import *
from rdflib import *
import json


mac = get_ontology("http://ifixit.org/mac.owl")

def parse_json_to_graph(file_path: str, graph: Graph):
    print(type(graph))
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    uri = URIRef("http://ifixit.org/" + entry["Title"].replace(" ", "_").replace('"', ""))
                    graph.add((uri, RDF.type, URIRef("http://ifixit.org/Procedure")))
                    for key,value in entry.items():
                        print()
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







