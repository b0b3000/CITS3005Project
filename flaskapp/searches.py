from rdflib import Graph


search_dict = {
    
}

def get_search_functions():
    return search_dict.keys()

def run_search(search_type: str, search_input: str,  graph: Graph):
    current_search = search_dict.get(search_type)
    return ["THIS IS", "A TEST"]
        
