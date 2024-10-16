from owlready2 import *
from rdflib import *
import json

from shape_validation import validate_ontology_shacl


def parse_data_to_owl(json_file_path, onto_file_path, rdfxml_file_path, mac):
    with mac:
        with open(json_file_path, 'r') as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    procedure_uri =  entry["Title"].replace('/','~').replace(" ", "_").replace('"', "")

                    # Add procedure to graph
                    for p in mac.Procedure.instances():
                        if type(p) != None:
                            if p.has_name == procedure_uri:
                                print("PROC DUP", procedure_uri)
                    procedure = mac.Procedure(procedure_uri)
                    print(procedure_uri)
                    procedure.has_name = entry["Title"] #May cause a problem due to duplicates?

                    # Add item to graph
                    item_uri = entry["Category"].replace('/','~').replace(" ", "_").replace('"', "")
                    item = mac.Item(item_uri)
                    item.has_name = entry["Category"]
                    procedure.has_item.append(item)    

                    #Add ancestor tree
                    current_ancestor = item
                    for item_ancestor in entry["Ancestors"]:
                        item_ancestor_uri = item_ancestor.replace('/','~').replace(" ", "_").replace('"', "")
                        item_ancestor = mac.Item(item_ancestor_uri)
                        current_ancestor.part_of.append(item_ancestor)
                        current_ancestor = item_ancestor

                    # Add part to graph
                    part_uri = entry["Category"].replace('/','~').replace(" ", "_").replace('"', "") + "_" + entry["Subject"].replace('/','~').replace(" ", "_").replace('"', "")
                    part = mac.Part(part_uri)
                    part.has_name = entry["Category"] + " " + entry["Subject"]
                    part.part_of.append(item)
                    procedure.has_part.append(part)

                    #Add toolbox
                    toolbox_uri = procedure_uri + "_toolbox"
                    toolbox = mac.Toolbox(toolbox_uri)
                    procedure.has_toolbox.append(toolbox)

                    # Add tool to graph
                    toolbox_dict ={}
                    for tool in entry["Toolbox"]:
                        if tool['Url'] is not None:
                            tool_uri = tool['Name'].replace('/','~').replace(" ", "_").replace('"', "")
                            new_tool = mac.Tool(tool_uri)
                            new_tool.has_name = tool['Name']
                            toolbox.has_tool.append(new_tool)
                            toolbox_dict[tool_uri] = new_tool #used for searching tools when adding to step

                    # Add step to procedure
                    for step in entry["Steps"]:
                        i = step["Order"]
                        step_uri = procedure_uri + "/" + f"step{i}".replace('/','~').replace(" ", "_").replace('"', "").replace("#Procedure", "#Step")
                        new_step = mac.Step(step_uri)
                        procedure.has_step.append(new_step)
                        new_step.step_number = i
                        new_step.step_description = step["Text_raw"]


                        # Add the tools used in the step to the graph
                        for tool in step["Tools_extracted"]:
                                # Add proper uri for tool 
                                if tool != "NA":
                                    tool_uri =tool.replace('/','~').replace(" ", "_").replace('"', "")

                                    if tool_uri in toolbox_dict.keys():
                                        matching_tool = toolbox_dict[tool_uri]
                                    else:
                                        # Called when tool is not lsited in toolbox, but still referenced in steps
                                        # This is likely a result of human error upon construction of data

                                        new_tool = mac.Tool(tool_uri)
                                        toolbox.has_tool.append(new_tool)
                                        toolbox_dict[tool_uri] = new_tool
                                        matching_tool = new_tool
                                    
                                    matching_tool.used_in.append(new_step)

                        # Add the images used in the step to the graph
                        for image_uri in step["Images"]:
                            image = mac.Image(image_uri)
                            new_step.has_image.append(image)

                except json.JSONDecodeError:
                    print(f"Error decoding JSON from line: {line.strip()}")
        #sync_reasoner(infer_property_values=True)
        #print(list(default_world.inconsistent_classes()))
        #sync_reasoner_pellet(infer_property_values=True)

        #Save the ontology into an OWL file
        mac.save(onto_file_path)

        #APPLY SHACL CONSTRAINTS - IMPORTANT
        
        #Save the ontology as an RDF/XML file representing triples of a graph
        graph = default_world.as_rdflib_graph()
        file = open(rdfxml_file_path, mode="w", encoding='utf-8')  
        file.write(graph.serialize(format='turtle'))

        validate_ontology_shacl(graph)

        #Return the RDFLib graph, and OWLReady2 ontology
        return graph, mac


