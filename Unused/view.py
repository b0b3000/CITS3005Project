import json

def parse_json_to_graph(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    for key, value in entry.items():
                        print(f"{key}")
                    input("press any button...")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from line: {line.strip()}")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")


parse_json_to_graph("temp.json")