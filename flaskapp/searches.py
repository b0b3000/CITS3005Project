from rdflib import *
from owlready2 import *


search_dict = {}

search_dict[
    "Search procedures by item"
] = """
PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?procedure
                WHERE {
                    ?procedure a ns:Procedure .
                    ?procedure ns:has_name ?name .
                    FILTER(CONTAINS(STR(?name), "keyword")) .
                }
"""

search_dict["Search parts"] = """
PREFIX ns: <http://ifixit.org/mac.owl#>
SELECT ?partName
WHERE {
    ?part a ns:Part .
    ?part ns:has_name ?partName .
    FILTER(CONTAINS(STR(?partName), "keyword")) .
}
"""


def get_search_functions():
    return search_dict.keys()


def run_search(search_type: str, search_input: str, graph: Graph):
    current_search = search_dict.get(search_type)
    current_query = current_search.replace("keyword", search_input)
    print(current_query)
    if current_query == None:
        return ["Query not found"]
    results_list = []
    try:
        results = graph.query(current_query)
    except:
        return ["Query has no results"]
    print(f"Results: {results}")
    if len(results) == 0:
        return ["Query has no results"]
    
    for result in results:
        print(result)
    for row in results:
        print(f"Row: {row}")
        uri = ""
        for item in row:
            item = str(item).removeprefix("http://ifixit.org/mac.owl#")
            results_list.append(str(item))
    return results_list


def get_ancestors(item_name: str, mac: Ontology):
    if item_name == "":
        return []
    sub_words = item_name.split(" ")
    possible_ancestors = []
    # get all items
    items = list(mac.Item.instances())
    print(type(items))
    print(items)
    for sub_word in sub_words:
        for item in items:
            current_item_name = str(item).replace("mac.", "")
            if sub_word.lower() in current_item_name.lower():
                if current_item_name not in possible_ancestors:
                    possible_ancestors.append(current_item_name)
    return possible_ancestors


def get_procedure_info(procedure_uri: str, mac: Ontology):
    print(f"URI: {procedure_uri}")
    query_uri = "http://ifixit.org/mac.owl#" + procedure_uri
    procedure = mac.search_one(iri=query_uri)


    name = procedure.has_name
    item_iri = procedure.has_item[0].iri
    item = mac.search_one(iri=item_iri).has_name

    part_iri = procedure.has_part[0].iri
    part = mac.search_one(iri=part_iri).has_name
    toolbox_ref = procedure.has_toolbox
    
    # get toolbox
    toolbox_uri = toolbox_ref[0].iri
    toolbox = mac.search_one(iri=toolbox_uri)
    tools = []
    for tool in toolbox.has_tool:
        print(f"Tool {tool.has_name}")
        tools.append(tool.has_name)

    print(f"Steps: {procedure.has_step}")
    steps = []
    for i, step in enumerate(procedure.has_step):
        current_step = mac.search_one(iri=step.iri)

        step_info = {
            "number": i+ 1,
            "description": current_step.step_description,
            "img": current_step.has_image,
        }

        print(f"INFO: {step_info}")
        steps.append(step_info)

    results = {
        "name": name,
        "item": item,
        "toolbox": tools,
        "part": part,
        "steps": steps,
    }
    return results
