from rdflib import *
from owlready2 import *


search_dict = {
    
}

def get_search_functions():
    return search_dict.keys()

def run_search(search_type: str, search_input: str,  graph: Graph):
    current_search = search_dict.get(search_type)
    return ["THIS IS", "A TEST"]

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
