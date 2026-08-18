class Parameter:
    def __init__(self, val: str):
        self.value: str = val
        self.is_id: bool = self.check_if_id()
        
    def check_if_id(self) -> bool:
        quote_set = ["'", '"']
        if(self.value[0] in quote_set and self.value[len(self.value) - 1] in quote_set):
            return True
        return False
    
    def to_string(self) -> str:
        return self.value

class Predicate:
    def __init__(self, name: str, parameters: list[Parameter]):
        self.name: str = name
        self.num_paramaters: int = 0
        self.parameters: list[Parameter] = parameters
    
    def to_string(self):
        return f"{self.name}({','.join([para.to_string() for para in self.parameters])})"

class Rule:
    def __init__(self, head: Predicate, body: list[Predicate]):
        self.headPredicate: Predicate = head
        self.bodyPredicates: list[Predicate] = body
    
    def to_string(self) -> str:
        return f"{self.headPredicate.to_string()} :- {','.join([pred.to_string() for pred in self.bodyPredicates])}"

class DatalogProgram:
    def __init__(self, s_list, f_list, r_list, q_list):
        self.schemes: list[Predicate] = s_list
        self.facts: list[Predicate] = f_list
        self.rules: list[Predicate] = r_list
        self.queries: list[Predicate] = q_list
    
    def addScheme(self, name: str, parameters: list[Parameter]):
        self.schemes.append(Predicate(name, parameters))
    
    def addFact(self, name: str, parameters: list[Parameter]):
        self.facts.append(Predicate(name, parameters))
    
    def addRule(self, name: str, parameters: list[Parameter]):
        self.rules.append(Predicate(name, parameters))
    
    def addQuery(self, name: str, parameters: list[Parameter]):
        self.queries.append(Predicate(name, parameters))
    
    def getSchemes(self) -> list[Predicate]:
        return self.schemes
    
    def getFacts(self) -> list[Predicate]:
        return self.facts
    
    def getRules(self) -> list[Predicate]:
        return self.rules
    
    def getQueries(self) -> list[Predicate]:
        return self.queries
    
    def to_string(self) -> str:
        datalog_string = ""
        datalog_string += f"Schemes({len(self.schemes)}):\n"
        for scheme in self.schemes:
            datalog_string += f"  {scheme.to_string()}\n"
        datalog_string += f"Facts({len(self.facts)}):\n"
        domain_set = []
        for fact in self.facts:
            datalog_string += f"  {fact.to_string()}.\n"
            for param in fact.parameters:
                if(param.check_if_id() and not param.value in domain_set):
                    domain_set.append(param.value)
        domain_set.sort()
        datalog_string += f"Rules({len(self.rules)}):\n"
        for rule in self.rules:
            datalog_string += f"  {rule.to_string()}.\n"
        datalog_string += f"Queries({len(self.queries)}):\n"
        for query in self.queries:
            datalog_string += f"  {query.to_string()}?\n"
        datalog_string += f"Domain({len(domain_set)}):\n"
        for item in domain_set:
            datalog_string += f"  {item}\n"
        return datalog_string