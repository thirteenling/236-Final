from .tuple import Tuple
from .header import Header

class Relation:
    def __init__(self, name: str, header: Header, tuples: set = set()):
        self.name: str = name
        self.header: Header = header
        self.tuples: set[Tuple] = set()
        if len(tuples) > 0: self.tuples = tuples
    
    def __str__(self) -> str:
        output_str: str = ""
        for t in sorted(self.tuples):
            if len(t.values) == 0: continue
            separator: str = ""
            output_str += "  "
            for i in range(len(self.header.values)):
                output_str += separator
                output_str += self.header.values[i]
                output_str += "="
                output_str += t.values[i]
                separator = ", "
            output_str += "\n"
        return output_str
        
    def add_tuple(self, new_tuple: Tuple):
        if len(new_tuple.values) != len(self.header.values):
            raise ValueError(f"ERROR: Row (length {len(new_tuple.values)} was not the same length as Header (length {len(self.header.values)})")
        self.tuples.add(new_tuple)
    
    def num_tuples(self) -> int:
        return len(self.tuples)
    
    # Two forms of select
    def select_has_value(self, index: int, constant: str) -> 'Relation':
        new_tuples: set[Tuple] = set()
        for t in self.tuples:
            if t.values[index] == constant:
                new_tuples.add(t)
        return Relation(self.name,self.header,new_tuples)
    
    def select_matches_value(self, index1: int, index2: int):
        new_tuples: set[Tuple] = set()
        for t in self.tuples:
            if t.values[index1] == t.values[index2]:
                new_tuples.add(t)
        return Relation(self.name,self.header,new_tuples)
    
    def project(self, indices: list[int]):
        new_header_values: list[str] = []
        new_tuples: set[Tuple] = set()
        for index in indices:
            new_header_values.append(self.header.values[index])
        for t in self.tuples:
            value_list: list[str] = []
            for index in indices:
                value_list.append(t.values[index])
            new_tuples.add(Tuple(value_list))
        new_header: Header = Header(new_header_values)
        return Relation(self.name, new_header, new_tuples)
        
    def rename(self, index: int, new_name: str):
        value_list: list[str] = []
        for item in self.header.values:
            value_list.append(item)
        new_header: Header = Header(value_list)
        new_header.values[index] = new_name
        return Relation(self.name, new_header, self.tuples)
    
    def join(self, other: 'Relation') -> 'Relation':
        new_header_values: list[str] = []
        joinable_columns = []
        for item in self.header.values:
            new_header_values.append(item)
            for item2 in other.header.values:
                if item == item2:
                    joinable_columns.append(item)
        for item in other.header.values:
            if not (item in new_header_values):
                new_header_values.append(item)
        new_header = Header(new_header_values)
        new_relation = Relation(self.name, new_header)
        
        
        # join_i1 = []
        # print(f"Iterating over {self.header.values}")
        # for i in range(len(self.header.values)):
        #     if self.header.values[i] in joinable_columns:
        #         join_i1.append(i)
        # join_i2 = []
        # print(f"Iterating over {other.header.values}")
        # for i in range(len(other.header.values)):
        #     if other.header.values[i] in joinable_columns:
        #         join_i2.append(i)
        join_i1 = []
        join_i2 = []
        for col in joinable_columns:
            join_i1.append(self.header.values.index(col))
            join_i2.append(other.header.values.index(col))
        
        can_add = True
        for t1 in self.tuples:
            for t2 in other.tuples:
                can_add = True
                for i in range(len(joinable_columns)):
                    if t1.values[join_i1[i]] != t2.values[join_i2[i]]:
                        can_add = False
                if can_add:
                    new_tuple_list = []
                    for i in range(len(new_header_values)):
                        if new_header_values[i] in self.header.values:
                            new_tuple_list.append(t1.values[self.header.values.index(new_header_values[i])])
                        elif new_header_values[i] in other.header.values:
                            new_tuple_list.append(t2.values[other.header.values.index(new_header_values[i])])
                    new_relation.add_tuple(Tuple(new_tuple_list))
        
        return new_relation
    
    def union(self, other: 'Relation') -> 'Relation':
        if [v for v in self.header.values] != [v for v in other.header.values]:
            raise ValueError("The headers for unioning do not match!")
        new_relation = Relation(self.name, self.header)
        for t in self.tuples:
            new_relation.add_tuple(t)
        for t in other.tuples:
            new_relation.add_tuple(t)
        return new_relation
