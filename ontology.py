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
                    uri = fix + entry["Title"].replace(" ", "_").replace('"', "")
                    graph.add((URIRef(uri), RDF.type, URIRef(fix + "Procedure")))

                    # Add tool/item/part to graph
                    for tool in entry["Toolbox"]:

                        if tool['Url'] is not None:

                            tool_uri = tool['Url']

                            if "Item" in tool_uri:
                                tool_type = "Item"
                                print(tool_uri)
                                tool_uri = fix[:17] + tool_uri
                                print(tool_uri)
                            
                            elif "Parts" in tool_uri:
                                tool_type = "Part"
                            
                            elif "Tools" in tool_uri:
                                tool_type = "Tool"
                            
                            else:
                                print(tool_uri)
                                tool_type = "Unknown" #PLACEHOLDER
                                #What to do here?
                                #I suggest just deleting these from test set lmao.
              
                        else:
                            tool_type = "Unknown" #PLACEHOLDER
                            tool_uri = fix + "Tools/" + tool['Name'].replace(" ", "_").replace('"', "").capitalize()

                        graph.add((URIRef(tool_uri), RDF.type, URIRef(fix + tool_type)))

                    # Add step to procedure
                    for step in entry["Steps"]:
                        i = step["Order"]
                        step_uri = uri + "/" + f"step{i}".replace(" ", "_").replace('"', "")
                        graph.add((URIRef(step_uri), fix.is_step , URIRef(uri)))

                        '''if "Word_level_parts_clean" in step.keys():
                            print(step["Word_level_parts_clean"])
                            input()
                        if "Word_level_parts_raw" in step.keys():
                            print(step["Word_level_parts_raw"])
                            input()'''
                        
                        # Add the tools used in the step to the graph
                        for tool in step["Tools_extracted"]:
                            if tool is dict:
                                if tool['Url'] is not None:

                                    if "Item" in tool_uri:
                                        tool_uri = fix[:17] + tool_uri

                                    graph.add((URIRef(tool["Url"]), fix.used_in, URIRef(step_uri)))
                            else:
                                # Add proper uri for tool 
                                #WHAT IS THIS?????
                                graph.add((URIRef(fix + "Tools/" + tool.replace(" ", "_").replace('"', "").capitalize()), fix.used_in, URIRef(step_uri)))

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








