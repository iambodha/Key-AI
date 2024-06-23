from typing import Dict, List, Tuple

def create_layout_data():
    EFFORTS = {
        (0, 0): 17, (0, 1): 14, (0, 2): 8, (0, 3): 8, (0, 4): 13, (0, 5): 16, (0, 6): 23, (0, 7): 19, (0, 8): 9, (0, 9): 8, (0, 10): 7, (0, 11): 15,
        (1, 0): 6, (1, 1): 2, (1, 2): 1, (1, 3): 6, (1, 4): 11, (1, 5): 14, (1, 6): 9, (1, 7): 1, (1, 8): 1, (1, 9): 7, (1, 10): 9, (1, 11): 13,
        (2, 0): 1, (2, 1): 0, (2, 2): 0, (2, 3): 0, (2, 4): 7, (2, 5): 7, (2, 6): 0, (2, 7): 0, (2, 8): 0, (2, 9): 1, (2, 10): 5,
        (3, 0): 7, (3, 1): 8, (3, 2): 10, (3, 3): 6, (3, 4): 10, (3, 5): 4, (3, 6): 2, (3, 7): 5, (3, 8): 5, (3, 9): 3
    }

    DISTANCES = {
        (0, 0): 28, (0, 1): 22, (0, 2): 22, (0, 3): 22, (0, 4): 22, (0, 5): 21, (0, 6): 28, (0, 7): 22, (0, 8): 22, (0, 9): 22, (0, 10): 22, (0, 11): 21,
        (1, 0): 11, (1, 1): 11, (1, 2): 11, (1, 3): 11, (1, 4): 13, (1, 5): 17, (1, 6): 11, (1, 7): 11, (1, 8): 11, (1, 9): 11, (1, 10): 13, (1, 11): 21,
        (2, 0): 0, (2, 1): 0, (2, 2): 0, (2, 3): 0, (2, 4): 10, (2, 5): 10, (2, 6): 0, (2, 7): 0, (2, 8): 0, (2, 9): 0, (2, 10): 10,
        (3, 0): 12, (3, 1): 12, (3, 2): 12, (3, 3): 12, (3, 4): 19, (3, 5): 12, (3, 6): 12, (3, 7): 12, (3, 8): 12, (3, 9): 12
    }

    FINGERS = {
        (0, 0): 'l-pinky', (0, 1): 'l-pinky', (0, 2): 'l-ring', (0, 3): 'l-middle', (0, 4): 'l-index', 
        (0, 5): 'r-index', (0, 6): 'r-middle', (0, 7): 'r-ring', (0, 8): 'r-pinky', (0, 9): 'r-pinky', (0, 10): 'r-pinky', (0, 11): 'r-pinky',
        (1, 0): 'l-pinky', (1, 1): 'l-ring', (1, 2): 'l-middle', (1, 3): 'l-index', (1, 4): 'l-index', 
        (1, 5): 'r-index', (1, 6): 'r-index', (1, 7): 'r-middle', (1, 8): 'r-ring', (1, 9): 'r-pinky', (1, 10): 'r-pinky', (1, 11): 'r-pinky',
        (2, 0): 'l-pinky', (2, 1): 'l-ring', (2, 2): 'l-middle', (2, 3): 'l-index', (2, 4): 'l-index', 
        (2, 5): 'r-index', (2, 6): 'r-index', (2, 7): 'r-middle', (2, 8): 'r-ring', (2, 9): 'r-pinky', (2, 10): 'r-pinky',
        (3, 0): 'l-pinky', (3, 1): 'l-ring', (3, 2): 'l-middle', (3, 3): 'l-index', (3, 4): 'l-index', 
        (3, 5): 'r-index', (3, 6): 'r-index', (3, 7): 'r-middle', (3, 8): 'r-ring', (3, 9): 'r-pinky'
    }

    return EFFORTS, DISTANCES, FINGERS

class Layout:
    def __init__(self, name: str, config: str):
        self.name = name
        self.config = config
        self.metrics = self.parse_config()

    def parse_config(self) -> Dict:
        EFFORTS, DISTANCES, FINGERS = create_layout_data()
        keys = {}
        lines = self.config.strip().split('\n')
        for row, line in enumerate(lines[::2]):
            for col, symbol in enumerate(line.split()):
                keys[symbol] = {
                    'effort': EFFORTS.get((row, col), 0),
                    'distance': DISTANCES.get((row, col), 0),
                    'finger': FINGERS.get((row, col), ''),
                    'hand': 'l' if col < 5 else 'r',
                    'row': row,
                    'shift': False
                }
        keys[' '] = {
            'effort': 0,
            'distance': 0,
            'finger': 'thumb',
            'hand': 'both',
            'row': 4,
            'shift': False
        }
        return keys
    
    def get_layout_list(self) -> List[str]:
        lines = self.config.strip().split('\n')
        config_list = []
        for line in lines:
            config_list.extend(line.split())
        return config_list

class Runner:
    def __init__(self, text: str, effort_limit: int = 3000000):
        self.text = text.strip()
        self.effort_limit = effort_limit
        self.same_finger_penalty = 10
        self.same_hand_penalty = 1

    def type_with(self, layout: Layout) -> Dict:
        position = 0
        distance = 0
        effort = 0
        prev_key = layout.metrics[' ']
        
        while effort < self.effort_limit:
            symbol = self.text[position % len(self.text)]
            key = layout.metrics.get(symbol)
            
            if key is None:
                prev_key = layout.metrics[' ']
                position += 1
                continue
            
            distance += key['distance']
            effort += key['effort']
            
            if key['hand'] != 'both' and key != prev_key:
                if key['finger'] == prev_key['finger']:
                    effort += (prev_key['effort'] + 1) * self.same_finger_penalty
                elif key['hand'] == prev_key['hand']:
                    effort += (prev_key['effort'] + 1) * self.same_hand_penalty
            
            prev_key = key
            position += 1

        return {
            'position': position,
            'distance': distance,
            'effort': round(effort)
        }

def print_results(layout_name: str, result: Dict):
    print(f"Layout: {layout_name}")
    print(f"Position reached: {result['position']}")
    print(f"Total distance: {result['distance']}")
    print(f"Total effort: {result['effort']}")
    print(f"Distance per symbol: {result['distance'] / result['position']:.3f}")
    print(f"Effort per symbol: {result['effort'] / result['position']:.3f}")

if __name__ == "__main__":
    qwerty_layout = Layout("QWERTY", """
    ` 1 2 3 4 5 6 7 8 9 0 - =
      q w e r t y u i o p [ ] \\
      a s d f g h j k l ; ' \\n
      z x c v b n m , . /
    """)

    print(qwerty_layout.get_layout_list())

    sample_text = "It was interesting to see how the grey fox tackled his brother"
    runner = Runner(sample_text)
    result = runner.type_with(qwerty_layout)

    print_results(qwerty_layout.name, result)