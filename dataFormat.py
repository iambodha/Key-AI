import json

input_file_path = 'data.json'
output_file_path = 'abstracts.json'

def extract_abstracts(input_file, output_file):
    abstracts = []
    with open(input_file, 'r', encoding = 'utf-8') as infile:
        for line in infile:
            try:
                data = json.loads(line.strip())
                abstract = data.get('abstract', '')
                if abstract:
                    abstracts.append({"abstract": abstract})
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    
    with open(output_file, 'w', encoding = 'utf-8') as outfile:
        json.dump(abstracts, outfile, indent=4)

extract_abstracts(input_file_path, output_file_path)