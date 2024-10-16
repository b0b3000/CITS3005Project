from owlready2 import *
from rdflib import *

import json

def parse_data_to_owl(json_file_path, onto_file_path, rdfxml_file_path, fix, mac):
    with mac:
        with open(json_file_path, 'r') as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    procedure_uri = fix + "Procedure/" + entry["Title"].replace('/','~').replace(" ", "_").replace('"', "")

                    # Add procedure to graph
                    procedure = mac.Procedure(procedure_uri)
                    procedure.has_name = entry["Title"] #May cause a problem due to duplicates?

                    # Add item to graph
                    item_uri = fix + "Item/" + entry["Category"].replace('/','~').replace(" ", "_").replace('"', "")
                    item = mac.Item(item_uri)
                    item.has_name = entry["Category"]
                    procedure.has_item.append(item)    

                    #Add ancestor tree
                    current_ancestor = item
                    for item_ancestor in entry["Ancestors"]:
                        item_ancestor_uri = fix + "Item/" + item_ancestor.replace('/','~').replace(" ", "_").replace('"', "")
                        item_ancestor = mac.Item(item_ancestor_uri)
                        current_ancestor.part_of.append(item_ancestor)
                        current_ancestor = item_ancestor

                    # Add part to graph
                    part_uri = fix + "Part/" + entry["Category"].replace('/','~').replace(" ", "_").replace('"', "") + "_" + entry["Subject"].replace('/','~').replace(" ", "_").replace('"', "")
                    part = mac.Part(part_uri)
                    part.has_name = entry["Category"] + " " + entry["Subject"]
                    part.part_of.append(item)
                    procedure.has_part.append(part)

                    # Check for procedures with same item
            

                    #Add toolbox
                    toolbox_uri = procedure_uri + "/Toolbox".replace("#Procedure", "#Toolbox")
                    toolbox = mac.Toolbox(toolbox_uri)
                    procedure.has_toolbox.append(toolbox)

                    # Add tool to graph
                    toolbox_dict ={}
                    for tool in entry["Toolbox"]:
                        if tool['Url'] is not None:
                            tool_uri = fix + tool['Name'].replace('/','~').replace(" ", "_").replace('"', "")
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
                                    tool_uri = fix + tool.replace('/','~').replace(" ", "_").replace('"', "")

                                    if tool_uri in toolbox_dict.keys():
                                        matching_tool = toolbox_dict[tool_uri]
                                    else:
                                        # Called when tool is not lsited in toolbox, but still referenced in steps
                                        # This is likely a result of human error upon construction of data
                                        print("TOOL NOT IN TOOLBOX. ADDING NOW", tool_uri, procedure_uri)
                                        
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
        """
            for p1 in mac.Procedure.instances():
                for p2 in mac.Procedure.instances():
                        if mac.Procedure in p1.is_a and mac.Procedure in p2.is_a: #check both types
                            if p2 not in p1.subprocedure: #check duplicates
                                if p1.has_item == p2.has_item:
                                        #print("procedures for same item")
                                        #print(p1, p2)
                                        #print(p1.has_item)
                                        p1.subprocedure.append(p2)
                                elif p1.has_part in p2.has_item[0].part_of or p1.has_item in p2.has_item[0].part_of:
                                    print("P1 part/item is a part of p2 item")
                                    p1.subprocedure.append(p2)
        """
        sync_reasoner_pellet(infer_property_values = True)
        #Save the ontology into an OWL file
        mac.save(onto_file_path)
        
        #Save the ontology as an RDF/XML file representing triples of a graph
        graph = default_world.as_rdflib_graph()
        graph.bind("fix", fix)
        file = open(rdfxml_file_path, mode="w")  
        file.write(graph.serialize(format='turtle'))

        #Return the RDFLib graph, and OWLReady2 ontology
        return graph, mac


