from owlready2 import *
from rdflib import *

import json

fix = Namespace("http://ifixit.org/mac.owl#")

mac = get_ontology("http://ifixit.org/mac.owl")

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

    class Part(Item):
        pass

    class Image(Thing):
        pass

    class Procedure(Thing):
        pass

    class has_steps(ObjectProperty):
        domain = [Procedure]
        range = [Step]

    class in_toolbox(ObjectProperty):
        domain = [Toolbox]
        range = [Tool]

    class has_tools(ObjectProperty):
        domain = [Tool]
        range = [Toolbox]

    class has_images(ObjectProperty):
        domain = [Step]
        range = [Image]

    class part_of(ObjectProperty):
        domain = [Item]
        range = [Item]
        is_transitive = True

    #SUB PROCEDURE ???

    mac.save("mac.owl")

    

def parse_json_to_graph(file_path: str, graph: Graph):
    graph.bind("fix", fix)
    with mac:
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
                        graph.add((URIRef(current_ancestor_uri), fix.part_of, URIRef(item_ancestor_uri)))
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

            file = open("output.xml", mode="w")
            file.write(graph.serialize(format='turtle'))

            return graph
                    
graph = default_world.as_rdflib_graph()
print(graph)

graph = parse_json_to_graph("data.json", graph)
print(graph)


def run_queries(graph):
    with mac:
        query1 = """
            PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?procedure
                WHERE {
                    ?procedure a ns:Procedure .
                    ?step ns:is_step ?Procedure .
                }
                GROUP BY ?procedure
                HAVING (COUNT(?step) > 6)
            """
        result = graph.query(query1)

        print
        for row in result:
            procedure_title = row.split("/")[-1] #Outputs just the part im interested in
            print(procedure_title)

        query2 = """
            PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?item
                WHERE {
                    ?procedure a ns:Procedure .
                    ?step ns:is_step ?Procedure .
                }
                GROUP BY ?procedure
                HAVING (COUNT(?step) > 6)
            """
        result = graph.query(query1)

        print
        for row in result:
            procedure_title = row.split("/")[-1] #Outputs just the part im interested in
            print(procedure_title)

run_queries(graph)
