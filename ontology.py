from owlready2 import *
import json

mac = get_ontology("http://ifixit.org/mac.owl")

def parse_json_to_graph(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    for key in entry.keys():
                        print(f"{key}")
                    input("press any button...")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from line: {line.strip()}")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")

with mac:
    class Procedure(Thing):
        pass

    class Step(Thing):
        pass

    class Toolbox(Thing):
        pass

    class Tool(Thing):
        pass

    class Item(Thing):
        pass

    class Part(Thing):
        pass

    class Image(Thing):
        pass

    class Procedure(Thing):
        has_steps = [Step]
        has_toolbox = Toolbox

    class Toolbox(Thing):
        has_tools = [Tool]
        has_parts = [Part]
        has_items = [Item]

    class Step(Thing):
        has_images = [Image]

    mac.save("mac.owl")
    graph = default_world.as_rdflib_graph()
    print(graph.serialize(format="turtle"))




if __name__ == "__main__":
     



