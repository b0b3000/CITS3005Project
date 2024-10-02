from owlready2 import *
from rdflib import *

import json

fix = Namespace("http://ifixit.org/mac.owl#")

mac = get_ontology("http://ifixit.org/mac.owl")

def parse_json_to_graph(file_path: str, graph: Graph):
    graph.bind("fix", fix)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    procedure_uri = fix +"Procedure/"+ entry["Title"].replace(" ", "_").replace('"', "")

                    # Add procedure to graph
                    graph.add((URIRef(procedure_uri), RDF.type, URIRef(fix + "Procedure")))

                    # Add item to procedure, and add it to its ancestors
                    item_uri = fix + "Item/" + entry["Category"].replace(" ", "_").replace('"', "")
                    graph.add((URIRef(item_uri), RDF.type, URIRef(fix + "Item")))
                    current_ancestor_uri = item_uri
                    for item_ancestor in entry["Ancestors"]:
                        item_ancestor_uri = fix + "Item/" + item_ancestor.replace(" ", "_").replace('"', "")
                        graph.add((URIRef(item_ancestor_uri), RDF.type, URIRef(fix + "Item")))
                        graph.add((URIRef(current_ancestor_uri), RDFS.subClassOf , URIRef(item_ancestor_uri)))
                        current_ancestor_uri = item_ancestor_uri
                        

                    # Add part to graph
                    part_uri = fix + "Part/" + entry["Category"].replace(" ", "_").replace('"', "") + "_" + entry["Subject"].replace(" ", "_").replace('"', "")
                    graph.add((URIRef(part_uri), RDF.type, URIRef(fix + "Part")))

                    # Add tool to graph
                    for tool in entry["Toolbox"]:
                        if tool['Url'] is not None:
                            tool_uri = tool['Name'].replace(" ", "_").replace('"', "")
                            graph.add((URIRef(fix + tool_uri), RDF.type, URIRef(fix + "Tool")))

                    # Add step to procedure
                    for step in entry["Steps"]:
                        i = step["Order"]
                        step_uri = procedure_uri + "/" + f"step{i}".replace(" ", "_").replace('"', "")
                        graph.add((URIRef(step_uri), fix.is_step , URIRef(procedure_uri)))

                        '''if "Word_level_parts_clean" in step.keys():
                            print(step["Word_level_parts_clean"])
                            input()
                        if "Word_level_parts_raw" in step.keys():
                            print(step["Word_level_parts_raw"])
                            input()'''
                        
                        # Add the tools used in the step to the graph
                        for tool in step["Tools_extracted"]:
                                # Add proper uri for tool 
                                if tool != "NA":
                                    graph.add((URIRef((fix + tool).replace(" ", "_").replace('"', "")), fix.used_in, URIRef(step_uri)))

                        # Add the images used in the step to the graph
                        for image in step["Images"]:
                            graph.add((URIRef(image), fix.refImage, URIRef(step_uri)))
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

    class Step(Thing):
        has_images = [Image]

    class Item(Thing):
        partof = Item

    
    mac.save("mac.owl")
    graph = default_world.as_rdflib_graph()
    parse_json_to_graph(
        "temp.json", graph
    )

    file = open("output.txt", mode="w")
    file.write(graph.serialize(format='turtle'))








