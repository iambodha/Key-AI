import random
import json
import itertools
import os
from evaluate import Layout, Runner
import multiprocessing
from functools import partial

population_size = 100
selection_num = 10
cycles = 100

data_path = 'Data/'
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

def reservoir_sampling(data_directory, data_size):
    files = [f for f in os.listdir(data_directory) if f.endswith('.json')]
    random_file = random.choice(files)
    file_path = os.path.join(data_directory, random_file)
    
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

def evaluate_layout(layout, runners):
    results = []
    for runner in runners:
        result = runner.type_with(layout)
        results.append(result)
    totalFitness = sum(calculate_fitness(result) for result in results)
    average_fitness = totalFitness / len(runners)
    return layout, average_fitness

def population_selection(population):
    populationEvalScore = []
    texts = reservoir_sampling(data_path, data_size)
    runners = [Runner(text) for text in texts]

    # Use multiprocessing to evaluate fitness in parallel
    with multiprocessing.Pool() as pool:
        evaluate_func = partial(evaluate_layout, runners=runners)
        results = pool.map(evaluate_func, population)
    
    # Extract fitness scores from results
    populationEvalScore = [fitness for layout, fitness in results]
    total_eval_score = sum(populationEvalScore)
    print("\033[92m" + str(total_eval_score/population_size) + "\033[0m")
    
    # Sort layouts by fitness
    layouts_with_scores = list(zip(population, populationEvalScore))
    layouts_with_scores.sort(key=lambda x: x[1], reverse=True)
    selected_layouts = [layout for layout, _ in layouts_with_scores[:selection_num]]
    
    # Print best layout
    best_layout_list = selected_layouts[0].get_layout_list()
    best_layout_spring = f"""
    {' '.join(best_layout_list[0:13])}
      {' '.join(best_layout_list[13:26])}
      {' '.join(best_layout_list[26:38])}
      {' '.join(best_layout_list[38:47])}
    """
    print("\033[92m" + best_layout_spring + "\033[0m")

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

def crossover_layouts(layout1, layout2, crossover_point1, crossover_point2, currentCycle):
    layout1_string = layout1.get_layout_list()
    layout2_string = layout2.get_layout_list()

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

    return Layout(f"Layout_{currentCycle + population_size}",layout_offspring1_string), Layout(f"Layout_{currentCycle + population_size}",layout_offspring2_string)

def population_crossover(population, currentCycle):
    new_population = []

    # Use multiprocessing to perform crossover in parallel
    with multiprocessing.Pool() as pool:
        results = []
        for layout1, layout2 in itertools.combinations(population, 2):
            crossover_point1 = random.randint(0, len(layout1.get_layout_list()) - 2)
            crossover_point2 = random.randint(crossover_point1 + 1, len(layout1.get_layout_list()) - 1)
            results.append(pool.apply_async(crossover_layouts, (layout1, layout2, crossover_point1, crossover_point2, currentCycle)))
        
        for result in results:
            layout_offspring1, layout_offspring2 = result.get()
            new_population.append(layout_offspring1)
            new_population.append(layout_offspring2)
    
    return new_population

if __name__ == "__main__":
    population = generate_starting_population(population_size)
    
    with multiprocessing.get_context("spawn").Pool() as pool:
        for i in range(cycles):
            selected_population = population_selection(population)
            new_population = population_crossover(selected_population, i)
            population = new_population
