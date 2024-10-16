from owlready2 import *
from rdflib import *

def add_procedure(form_data: dict, mac: Ontology, fix: Namespace):
    new_procedure_uri = fix + "Procedure/" + form_data["procedure_name"].replace('/','~').replace(" ", "_").replace('"', "")
    new_procedure = mac.Procedure(new_procedure_uri)
    new_procedure.has_name = form_data["procedure_name"]

    item_uri = fix + "Item/" + form_data["item_name"].replace('/','~').replace(" ", "_").replace('"', "")
    item = mac.Item(item_uri)
    item.has_name = form_data["item_name"] 
    item.has_procedure.append(new_procedure)

    #Add ancestor tree
    #TODO

    # Add part to graph
    part_uri = fix + "Part/" + form_data["part"].replace('/','~').replace(" ", "_").replace('"', "") + "_" + form_data["part_name"].replace('/','~').replace(" ", "_").replace('"', "")
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
    toolbox_uri = (new_procedure_uri + "/Toolbox").replace("#Procedure", "#Toolbox")
    toolbox = mac.Toolbox(toolbox_uri)
    new_procedure.has_toolbox.append(toolbox)
    
