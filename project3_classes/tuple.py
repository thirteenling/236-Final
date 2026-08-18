class Tuple:
    def __init__(self, values: list[str]):
        self.values: list[str] = values

    def __eq__(self, other):
        return self.values == other.values
    
    def __lt__(self, other):
        return self.values < other.values
    
    def __hash__(self):
        return hash(tuple(self.values))
    
    