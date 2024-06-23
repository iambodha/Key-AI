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

