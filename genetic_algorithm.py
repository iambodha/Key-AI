import random
import json
from evaluate import Layout, Runner

population_size = 2
selection_num = 20
cycles = 10

data_path = 'abstracts.json'
data_size = 10

def generate_random_layout(name):
    keys = [
        '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", '\\n',
        'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'
    ]
    
    random.shuffle(keys)
    print(keys)
    
    layout_string = f"""
    {' '.join(keys[0:13])}
      {' '.join(keys[13:26])}
      {' '.join(keys[26:38])}
      {' '.join(keys[38:47])}
    """
    
    return Layout(name, layout_string)

def generate_starting_population(population_size):
    population = []
    for i in range(population_size):
        layout = generate_random_layout(f"Layout_{i}")
        population.append(layout)
    return population

def reservoir_sampling(file_path, data_size):
    sample = []
    with open(file_path, 'r') as infile:
        data = json.load(infile)
        for i, entry in enumerate(data):
            if i < data_size:
                sample.append(entry['abstract'])
            else:
                j = random.randint(0, i)
                if j < data_size:
                    sample[j] = entry['abstract']
    return sample



def population_selection(population):
    populationEvalScore = []
    runners = []
    texts = reservoir_sampling(data_path,data_size)

    for text in texts:
        runner = Runner(text)
        runners.append(runner)

    for layout in population:
        results = []
        totalFitness = 0
        for runner in runners:
            result = runner.type_with(layout)
            results.append(result)
        for result in results:


if __name__ == "__main__":
    population = generate_starting_population(population_size)
    population_selection(population)