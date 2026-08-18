from typing import Dict
from .relation import *
class Database:
    def __init__(self):
        self.dict: Dict[str, Relation] = {}
        
    def __str__(self):
        output_str = ""
        for key in self.dict.keys():
            output_str += key
            output_str += " | "
            output_str += self.dict[key].header.__str__()
            output_str += "\n"
            output_str += str(self.dict[key])
        return output_str
    
    def add_relation(self, name: str, relation: Relation):
        self.dict[name] = relation
    
    def get_relation(self, name: str) -> Relation:
        if name in self.dict.keys():
            return self.dict[name]
        #print(f"Error: Relation with name {name} does not exist!")
        return Relation("NotFoundError",Header([]))
    
    def get_num_tuples(self) -> int:
        result = 0
        for key in self.dict.keys():
            result += len(self.dict[key].tuples)
        return result