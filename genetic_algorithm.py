import random
import json
import itertools
from evaluate import Layout, Runner

population_size = 100
selection_num = 10
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

def calculate_fitness(result):
    distance = result['distance']
    effort = result['effort']
    position = result['position']

    distance_per_char = distance / position
    effort_per_char = effort / position

    distance_score = 1 / (distance_per_char + 1)
    effort_score = 1 / (effort_per_char + 1)

    fitness = (distance_score + effort_score) / 2

    return fitness

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
            totalFitness += calculate_fitness(result)
        average_fitness = totalFitness/data_size
        populationEvalScore.append(average_fitness)
        print(average_fitness)
    
    layouts_with_scores = list(zip(population, populationEvalScore))
    layouts_with_scores.sort(key=lambda x: x[1], reverse=True)
    selected_layouts = [layout for layout, _ in layouts_with_scores[:selection_num]]

    return selected_layouts

def order_crossover(p1, p2, cp1, cp2):
    offspring = [None] * len(p1)
    offspring[cp1:cp2+1] = p1[cp1:cp2+1]
    current_pos = (cp2 + 1) % len(p1)
    for item in p2:
        if item not in offspring:
            offspring[current_pos] = item
            current_pos = (current_pos + 1) % len(p1)
    return offspring

def population_crossover(population,currentCycle):
    new_population = population
    offspring_count = 0
    for layout1, layout2 in itertools.combinations(population, 2):
        layout1_string = layout1.get_layout_list()
        layout2_string = layout2.get_layout_list()
        crossover_point1 = random.randint(0, len(layout1_string) - 2)
        crossover_point2 = random.randint(crossover_point1 + 1, len(layout1_string) - 1)

        layout_offspring1 = order_crossover(layout1_string, layout2_string, crossover_point1, crossover_point2)
        layout_offspring2 = order_crossover(layout2_string, layout1_string, crossover_point1, crossover_point2)

        layout_offspring1_string = f"""
        {' '.join(layout_offspring1[0:13])}
          {' '.join(layout_offspring1[13:26])}
          {' '.join(layout_offspring1[26:38])}
          {' '.join(layout_offspring1[38:47])}
        """
        layout_offspring2_string = f"""
        {' '.join(layout_offspring2[0:13])}
          {' '.join(layout_offspring2[13:26])}
          {' '.join(layout_offspring2[26:38])}
          {' '.join(layout_offspring2[38:47])}
        """

        new_population.append(Layout(f"Layout_{offspring_count + (population_size * (currentCycle + 1))}" ,layout_offspring1_string))
        offspring_count += 1
        new_population.append(Layout(f"Layout_{offspring_count + (population_size * (currentCycle + 1))}" ,layout_offspring2_string))
        offspring_count += 1

if __name__ == "__main__":
    population = generate_starting_population(population_size)
    for i in range(cycles):
        selected_population = population_selection(population)
        new_population = population_crossover(selected_population,i)
        population = new_population