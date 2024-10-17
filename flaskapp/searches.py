from rdflib import *
from owlready2 import *


search_dict = {}

search_dict["Search procedures"] = """
PREFIX ns: <http://ifixit.org/mac.owl#>
SELECT ?procedure
WHERE {
    ?procedure a ns:Procedure .
    ?procedure ns:has_name ?name .
    FILTER(CONTAINS(LCASE(STR(?name)), LCASE("keyword"))) .
}
"""


search_dict["Steps with a keyword in their description"] = """PREFIX ns: <http://ifixit.org/mac.owl#>
SELECT ?step    ?description

WHERE {
    ?step a ns:Step .
    ?step ns:step_description ?description .
    FILTER(CONTAINS(LCASE(STR(?description)), LCASE("keyword")))
}"""

search_dict["Items containing a keyword or substring"] = """PREFIX ns: <http://ifixit.org/mac.owl#>
SELECT ?item    ?name
WHERE {
    ?item a ns:Item .
    ?item ns:has_name ?name .
    FILTER(CONTAINS(LCASE(STR(?name)), LCASE("keyword")))
}"""

search_dict["Parts containing a keyword or substring"] = """PREFIX ns: <http://ifixit.org/mac.owl#>
SELECT ?part    ?name
WHERE {
    ?part a ns:Part .
    ?part ns:has_name ?name .
    FILTER(CONTAINS(LCASE(STR(?name)), LCASE("keyword")))
}"""

search_dict["Tools containing a keyword or substring"] = """PREFIX ns: <http://ifixit.org/mac.owl#>
SELECT ?tool    ?name
WHERE {
    ?tool a ns:Tool .
    ?tool ns:has_name ?name .
    FILTER(CONTAINS(LCASE(STR(?name)), LCASE("keyword")))
}"""

def get_search_functions():
    functions = [func for func in search_dict.keys() if func != "Search procedures"]
    return functions

def get_procedure_search():
    return "Search procedures"

def run_search(search_type: str, search_input: str, graph: Graph, mac: Ontology):
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
        text = ""
        for item in row:
            item = str(item).removeprefix("http://ifixit.org/mac.owl#")
            text += item + " "
        results_list.append({"text" : str(text)})

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
    query_uri = "http://ifixit.org/mac.owl#" + procedure_uri
    print(f"Query URI: {query_uri}")
    procedure = mac.search_one(iri=query_uri)
    print(f"Procedure: {procedure}")

    if procedure == None:
        return {"error": "Procedure not found"}
    
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
        tools.append(tool.has_name)

    steps = []
    for i, step in enumerate(procedure.has_step):
        current_step = mac.search_one(iri=step.iri)

        step_info = {
            "number": i+ 1,
            "description": current_step.step_description,
            "img": str(current_step.has_image[0].iri).removeprefix("http://ifixit.org/mac.owl#"),
        }
        steps.append(step_info)

    results = {
        "name": name,
        "item": item,
        "toolbox": tools,
        "part": part,
        "steps": steps,
    }
    return results
