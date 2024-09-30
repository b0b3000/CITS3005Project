from owlready2 import *
from rdflib import *
import json

fix = Namespace("http://ifixit.org/")

mac = get_ontology("http://ifixit.org/mac.owl")

def parse_json_to_graph(file_path: str, graph: Graph):
    graph.bind("fix", fix)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    uri = URIRef("http://ifixit.org/" + entry["Title"].replace(" ", "_").replace('"', ""))
                    graph.add((uri, RDF.type, URIRef("http://ifixit.org/Procedure")))

                    # Add tool to graph
                    for tool in entry["Toolbox"]:
                        if tool['Url'] is not None:
                            tool_type = "Tools"
                            tool_uri = tool["Url"]
                            if "Item" in tool["Url"]:
                                tool_type = "Items"
                                tool_uri = "http://ifixit.org" + tool["Url"]
                            graph.add((URIRef(tool_uri), RDF.type, URIRef(f"http://ifixit.org/{tool_type}")))
                        else:
                            graph.add((URIRef("http://ifixit.org/Tools/" + tool['Name'].replace(" ", "_").replace('"', "").capitalize()), RDF.type, URIRef("http://ifixit.org/Tools")))
                    
                    # Add step to procedure
                    for step in entry["Steps"]:
                        i = step["Order"]
                        step_uri = uri + "/" + f"step{i}".replace(" ", "_").replace('"', "")
                        graph.add((step_uri, fix.is_step , uri))
                        # Add the tools used in the step to the graph
                        for tool in step["Tools_extracted"]:
                            if tool is dict:
                                if tool['Url'] is not None:
                                    graph.add((URIRef(tool["Url"]), fix.used_in, step_uri))
                            else:
                                # Add proper uri for tool
                                graph.add((URIRef("http://ifixit.org/Tools/" + tool.replace(" ", "_").replace('"', "").capitalize()), fix.used_in, URIRef("http://ifixit.org/Tools")))

                        # Add the images used in the step to the graph
                        for image in step["Images"]:
                            graph.add((URIRef(image), fix.refImage, step_uri))
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

    file = open("output.txt", mode="w")
    file.write(graph.serialize(format='turtle'))








