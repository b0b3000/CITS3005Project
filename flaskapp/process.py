from owlready2 import *
from rdflib import *

def add_new_procedure(ontology_file_path: str, form_data: dict, mac: Ontology):
    new_procedure_uri = form_data["procedure_name"].replace('/','~').replace(" ", "_").replace('"', "")
    new_procedure = mac.Procedure(new_procedure_uri)
    new_procedure.has_name = form_data["procedure_name"]

    item_uri = form_data["item"].replace('/','~').replace(" ", "_").replace('"', "")
    item = mac.Item(item_uri)
    item.has_name = form_data["item"] 
    new_procedure.has_item.append(item)

    #Add ancestor tree
    ancestor = form_data["ancestor"]
    print("Ancestor: ", type(ancestor))
    if ancestor != "":
        print("Ancestor is not empty")
        ancestor = mac.search_one(iri="*" + ancestor)
        print(ancestor)
        item.part_of.append(ancestor)
        print(item.part_of)
    else:
        print("No ancestor")
        # Add to root

        # Root item
        root = mac.search_one(iri="*Root")
        item.part_of.append(root)

        print(item.part_of)
        # get root

    # Add part to graph
    part_uri = form_data["part"].replace('/','~').replace(" ", "_").replace('"', "")
    part = mac.Part(part_uri)
    part.has_name = form_data["part"]

    part.part_of.append(item)

    toolbox_uri = new_procedure_uri.replace("#Procedure", "#Toolbox") + "_toolbox"
    toolbox = mac.Toolbox(toolbox_uri)

    new_procedure.has_toolbox.append(toolbox)

    new_procedure.has_part.append(part)


    # Check for procedures with same item

    #Add toolbox
    

    # Add tool to graph
    toolbox_dict ={}
    for tool in form_data["toolbox"]:
        tool_uri = tool.replace('/','~').replace(" ", "_").replace('"', "")
        new_tool = mac.Tool(tool_uri)
        new_tool.has_name = tool
        toolbox.has_tool.append(new_tool)
        toolbox_dict[tool_uri] = new_tool
        
    # Add steps to procedure
    for step_index, step_data in form_data["step_data"].items():
        step_uri = new_procedure_uri + "/step" + step_index
        new_step = mac.Step(step_uri)
        new_procedure.has_step.append(new_step)
        new_step.step_description = step_data["step_description"]

        # Add the tools used in the step to the graph
        for tool in step_data["tools_used"]:
            # Add proper uri for tool 
            tool_uri = tool
            if tool_uri in toolbox_dict:
                matching_tool = toolbox_dict[tool_uri]
            else:
                new_tool = mac.Tool(tool_uri)
                toolbox.has_tool.append(new_tool)
                toolbox_dict[tool_uri] = new_tool
                matching_tool = new_tool

            matching_tool.used_in.append(new_step)

        image_uri = step_data['img']
        image = mac.Image(image_uri)
        new_step.has_image.append(image)
        
    mac.save(ontology_file_path)

    
def delete_procedure(ontology_file_path: str, procedure_uri: str, mac: Ontology):
    print(f"Searching for procedure: {procedure_uri}")
    procedure = mac.search_one(iri=procedure_uri)

    if procedure == None:
        return {"error": "Procedure not found"}
    return {"message": "Procedure deleted"}