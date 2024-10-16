from rdflib import *
from owlready2 import *


search_dict = {}

search_dict[
    "Search procedures by item"
] = """
PREFIX ns: <http://ifixit.org/mac.owl#>
                SELECT ?name
                WHERE {
                    ?procedure a ns:Procedure .
                    ?procedure ns:has_name ?name .
                    FILTER(CONTAINS(STR(?name), "Fan")) .
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
    print(results)
    for result in results:
        print(result)
    for row in results:
        uri = ""
        for item in row:
            item = str(item).split("/")[-1].replace("_", " ")
            uri += item + "/"
        results_list.append(uri)

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
                possible_ancestors.append(current_item_name)
    return possible_ancestors
