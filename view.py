import json

def view_entries(file_path):
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

if __name__ == "__main__":
    view_entries('data.json')