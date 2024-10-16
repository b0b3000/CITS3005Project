from owlready2 import *
from rdflib import *

import json

def parse_json_to_graph(file_path, graph, fix, mac):
    graph.bind("fix", fix)
    with mac:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    
                    entry = json.loads(line)
                    procedure_uri = fix +"Procedure/"+ entry["Title"].replace(" ", "_").replace('"', "")

                    # Add procedure to graph
                    graph.add((URIRef(procedure_uri), RDF.type, URIRef(fix + "Procedure")))

                    # Add item to graph
                    item_uri = fix + "Item/" + entry["Category"].replace(" ", "_").replace('"', "")
                    graph.add((URIRef(item_uri), RDF.type, URIRef(fix + "Item")))
                    graph.add((URIRef(item_uri), fix.has_procedure, URIRef(procedure_uri)))       

                    #Add ancestor tree
                    current_ancestor_uri = item_uri
                    for item_ancestor in entry["Ancestors"]:
                        item_ancestor_uri = fix + "Item/" + item_ancestor.replace(" ", "_").replace('"', "")
                        graph.add((URIRef(item_ancestor_uri), RDF.type, URIRef(fix + "Item")))
                        graph.add((URIRef(current_ancestor_uri), fix.part_of, URIRef(item_ancestor_uri)))
                        current_ancestor_uri = item_ancestor_uri

                    # Add part to graph
                    part_uri = fix + "Part/" + entry["Category"].replace(" ", "_").replace('"', "") + "_" + entry["Subject"].replace(" ", "_").replace('"', "")
                    graph.add((URIRef(part_uri), RDF.type, URIRef(fix + "Part")))
                    graph.add((URIRef(part_uri), fix.part_of, URIRef(item_uri)))
                    graph.add((URIRef(part_uri), fix.has_procedure, URIRef(procedure_uri)))

                    # Check for procedures with same item
                    same_item_triples = list(graph.triples((URIRef(item_uri), fix.has_procedure, None)))
                    same_item_triples = same_item_triples + list(graph.triples((URIRef(part_uri), fix.has_procedure, None)))
                    for triple in same_item_triples:
                        subprocedure = triple[2]
                        if (not (URIRef(subprocedure), fix.subprocedure, URIRef(procedure_uri)) in graph) and (not (URIRef(procedure_uri), fix.subprocedure, URIRef(subprocedure)) in graph): 
                            if not str(subprocedure) == str(procedure_uri):
                                # avoid duplicates & redundancy
                                graph.add((URIRef(subprocedure), fix.subprocedure, URIRef(procedure_uri)))

                    #Add toolbox
                    toolbox_uri = procedure_uri + "/Toolbox".replace("#Procedure", "#Toolbox")
                    graph.add((URIRef(toolbox_uri), RDF.type, URIRef(fix + "Toolbox")))
                    graph.add((URIRef(procedure_uri), fix.has_toolbox, URIRef(toolbox_uri)))

                    # Add tool to graph
                    for tool in entry["Toolbox"]:
                        if tool['Url'] is not None:
                            tool_uri = fix + tool['Name'].replace(" ", "_").replace('"', "")
                            graph.add((URIRef(tool_uri), RDF.type, URIRef(fix + "Tool")))
                            graph.add((URIRef(tool_uri), fix.in_toolbox, URIRef(toolbox_uri)))

                    # Add step to procedure
                    for step in entry["Steps"]:
                        i = step["Order"]
                        step_uri = procedure_uri + "/" + f"step{i}".replace(" ", "_").replace('"', "").replace("#Procedure", "#Step")
                        graph.add((URIRef(step_uri), RDF.type, URIRef(fix + "Step")))
                        graph.add((URIRef(procedure_uri), fix.has_step, URIRef(step_uri)))
                        graph.add((URIRef(step_uri), fix.step_number, Literal(i))) 
                        graph.add((URIRef(step_uri), fix.step_description, Literal(step["Text_raw"])))

                        # Add the tools used in the step to the graph
                        for tool in step["Tools_extracted"]:
                                # Add proper uri for tool 
                                if tool != "NA":
                                    graph.add((URIRef((fix + tool).replace(" ", "_").replace('"', "")), fix.used_in, URIRef(step_uri)))

                        # Add the images used in the step to the graph
                        for image in step["Images"]:
                            graph.add((URIRef(step_uri), fix.has_images, URIRef(image)))
            
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from line: {line.strip()}")

            file = open("output.xml", mode="w")
            file.write(graph.serialize(format='turtle'))

            return graph