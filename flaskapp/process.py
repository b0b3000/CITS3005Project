from owlready2 import *
from rdflib import *

def add_new_procedure(ontology_file_path: str, rdfxml_file_path: str, form_data: dict,graph, mac: Ontology, fix: Namespace):
    new_procedure_uri = fix + "Procedure/" + form_data["procedure_name"].replace('/','~').replace(" ", "_").replace('"', "")
    new_procedure = mac.Procedure(new_procedure_uri)
    new_procedure.has_name = form_data["procedure_name"]

    item_uri = fix + "Item/" + form_data["item"].replace('/','~').replace(" ", "_").replace('"', "")
    item = mac.Item(item_uri)
    item.has_name = form_data["item"] 
    item.has_procedure.append(new_procedure)

    #Add ancestor tree
    #TODO

    # Add part to graph
    part_uri = fix + "Part/" + form_data["part"].replace('/','~').replace(" ", "_").replace('"', "")
    part = mac.Part(part_uri)
    part.has_name = form_data["item"] + " " + form_data["part"]

    part.part_of.append(item)
    part.has_procedure.append(new_procedure)


    # Check for procedures with same item
    same_item_procedures = item.has_procedure
    same_item_procedures = same_item_procedures + part.has_procedure

    for subprocedure in same_item_procedures:
        if (subprocedure not in new_procedure.subprocedure) and (new_procedure not in subprocedure.subprocedure): 
            if subprocedure != new_procedure:
                new_procedure.subprocedure.append(subprocedure)

    #Add toolbox
    toolbox_uri = new_procedure_uri.replace("#Procedure", "#Toolbox") + "_toolbox"
    print(toolbox_uri)
    toolbox = mac.Toolbox(toolbox_uri)
    new_procedure.has_toolbox.append(toolbox)

    # Add tool to graph
    toolbox_dict ={}
    for tool in form_data["toolbox"]:
        tool_uri = fix + tool.replace('/','~').replace(" ", "_").replace('"', "")
        new_tool = mac.Tool(tool_uri)
        new_tool.has_name = tool
        toolbox_dict[tool_uri] = new_tool
        
    # Add steps to procedure
    for step_index, step_data in form_data["step_data"].items():
        step_uri = fix + "Step/" + step_index
        new_step = mac.Step(step_uri)
        new_procedure.has_step.append(new_step)
        new_step.has_description = step_data["step_description"]

        # Add the tools used in the step to the graph
        for tool in step_data["tools_used"]:
            # Add proper uri for tool 
            tool_uri = fix + tool
            if tool_uri in toolbox_dict:
                matching_tool = toolbox_dict[tool_uri]
            else:
                new_tool = mac.Tool(tool_uri)
                new_tool.in_toolbox.append(toolbox)
                toolbox_dict[tool_uri] = new_tool
                matching_tool = new_tool

            matching_tool.used_in.append(new_step)

        image_uri = fix + "Image/" + step_data['img']
        image = mac.Image(image_uri)
        new_step.has_image.append(image)
        
    mac.save(ontology_file_path)
    graph = default_world.as_rdflib_graph()

    
