from typing import Callable
from .data_structures import Predicate, Rule, Parameter, DatalogProgram
from my_token import Token

class Parser():
    def __init__(self):
        pass#self.program: DatalogProgram = DatalogProgram([], [], [], [])
    
    def run(self, tokens: list[Token]) -> str:
        self.index: int = 0
        self.tokens: list[Token] = tokens
        try:
            self.program = self.datalogProgram()
            return "Success!"
        except ValueError as ve:
            return f"Failure!\n  {ve}"
        
    def throw_error(self):
        raise ValueError(self.get_curr_token().to_string())
    
    def get_curr_token(self) -> Token:
        if(self.index >= len(self.tokens)):
            self.index = len(self.tokens) - 1
            self.throw_error()
        return self.tokens[self.index]
    
    def get_prev_token_val(self) -> str:
        return self.tokens[self.index - 1].getValue()
    
    def advance(self):
        self.index += 1
        
    def match(self, expected_type: str):
        if(self.get_curr_token().token_type == expected_type):
            #print(f"Matched {self.get_curr_token().token_type} with {expected_type}")
            self.advance()
        else:
            self.throw_error()

    #datalogProgram	->	SCHEMES COLON scheme schemeList FACTS COLON factList RULES COLON ruleList QUERIES COLON query queryList EOF
    def datalogProgram(self) -> DatalogProgram:
        scheme_list = []
        fact_list = []
        # Chips ahoyeth, landlubbers! I see thou hast foundeth mine LISTE OF THE MOST HIGHETH GRANDEUR!
        rule_list = []
        query_list = []
        self.match("SCHEMES")
        self.match("COLON")
        scheme_list.append(self.scheme())
        self.schemeList(scheme_list)
        self.match("FACTS")
        self.match("COLON")
        self.factList(fact_list)
        self.match("RULES")
        self.match("COLON")
        self.ruleList(rule_list)
        self.match("QUERIES")
        self.match("COLON")
        query_list.append(self.query())
        self.queryList(query_list)
        self.match("EOF")
        
        # Print statements to test stuff
        """
        print("\nSchemes:")
        for scheme in scheme_list: 
            print(scheme.to_string())
        print("\nFacts:")
        for fact in fact_list:
            print(fact.to_string())
        print("\nRules:")
        for rule in rule_list:
            print(rule.to_string())
        print("\nQueries:")
        for query in query_list:
            print(query.to_string())
        """
        return DatalogProgram(scheme_list, fact_list, rule_list, query_list)

    # schemeList	->	scheme schemeList | lambda
    def schemeList(self, s_list: list[Predicate]):
        # FIRST(scheme) = {"ID"}
        if(self.get_curr_token().getType() == "ID"):
            s_list.append(self.scheme())
            self.schemeList(s_list)
        else:
            # lambda
            return

    # factList	->	fact factList | lambda
    def factList(self, f_list: list[Predicate]):
        # FIRST(fact) = {"ID"}
        if(self.get_curr_token().getType() == "ID"):
            f_list.append(self.fact())
            self.factList(f_list)
        else:
            # lambda
            return

    # ruleList	->	rule ruleList | lambda
    def ruleList(self, r_list):
        # FIRST(rule) = {"ID"}
        if(self.get_curr_token().getType() == "ID"):
            r_list.append(self.rule())
            self.ruleList(r_list)
        else:
            # lambda
            return

    # queryList	->	query queryList | lambda
    def queryList(self, q_list):
        # FIRST(query) = {"ID"}
        if(self.get_curr_token().getType() == "ID"):
            q_list.append(self.query())
            self.queryList(q_list)
        else:
            # lambda
            return

    # scheme   	-> 	ID LEFT_PAREN ID idList RIGHT_PAREN
    def scheme(self) -> Predicate:
        s_name = ""
        s_parameters = []
        self.match("ID")
        s_name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        self.match("ID")
        s_parameters.append(Parameter(self.get_prev_token_val()))
        self.idList(s_parameters)
        self.match("RIGHT_PAREN")
        return Predicate(s_name, s_parameters)

    # fact    	->	ID LEFT_PAREN STRING stringList RIGHT_PAREN PERIOD
    def fact(self) -> Predicate:
        f_name = ""
        f_parameters = []
        self.match("ID")
        f_name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        self.match("STRING")
        f_parameters.append(Parameter(self.get_prev_token_val()))
        self.stringList(f_parameters)
        self.match("RIGHT_PAREN")
        self.match("PERIOD")
        return Predicate(f_name, f_parameters)

    # rule    	->	headPredicate COLON_DASH predicate predicateList PERIOD
    def rule(self) -> Rule:
        r_head = ""
        r_body = []
        r_head = self.headPredicate()
        self.match("COLON_DASH")
        r_body.append(self.predicate())
        self.predicateList(r_body)
        self.match("PERIOD")
        return Rule(r_head, r_body)

    # query	        ->      predicate Q_MARK
    def query(self) -> Predicate:
        query = self.predicate()
        self.match("Q_MARK")
        return query

    # headPredicate	->	ID LEFT_PAREN ID idList RIGHT_PAREN
    def headPredicate(self) -> Predicate:
        hp_name = ""
        hp_list = []
        self.match("ID")
        hp_name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        self.match("ID")
        hp_list.append(Parameter(self.get_prev_token_val()))
        self.idList(hp_list)
        self.match("RIGHT_PAREN")
        return Predicate(hp_name, hp_list)

    # predicate	->	ID LEFT_PAREN parameter parameterList RIGHT_PAREN
    def predicate(self) -> Predicate:
        p_name = ""
        p_list = []
        self.match("ID")
        p_name = self.get_prev_token_val()
        self.match("LEFT_PAREN")
        p_list.append(self.parameter())
        self.parameterList(p_list)
        self.match("RIGHT_PAREN")
        return Predicate(p_name, p_list)

    # predicateList	->	COMMA predicate predicateList | lambda
    def predicateList(self, p_list):
        # FIRST(predicateList) = {"COMMA"}
        if(self.get_curr_token().getType() == "COMMA"):
            self.match("COMMA")
            p_list.append(self.predicate())
            self.predicateList(p_list)
        else:
            # lambda
            return

    # parameterList	-> 	COMMA parameter parameterList | lambda
    def parameterList(self, p_list):
        # FIRST(parameterList) = {"COMMA"}
        if(self.get_curr_token().getType() == "COMMA"):
            self.match("COMMA")
            p_list.append(self.parameter())
            self.parameterList(p_list)
        else:
            # lambda
            return

    # stringList	-> 	COMMA STRING stringList | lambda
    def stringList(self, list: list[Parameter]):
        # FIRST(stringList) = {"COMMA"}
        if(self.get_curr_token().getType() == "COMMA"):
            self.match("COMMA")
            self.match("STRING")
            list.append(Parameter(self.get_prev_token_val()))
            self.stringList(list)
        else:
            # lambda
            return

    # idList  	-> 	COMMA ID idList | lambda
    def idList(self, list: list[Parameter]):
        if(self.get_curr_token().getType() == "COMMA"):
            self.match("COMMA")
            self.match("ID")
            list.append(Parameter(self.get_prev_token_val()))
            self.idList(list)
        else:
            # lambda
            return

    # parameter	->	STRING | ID
    def parameter(self) -> Parameter:
        # FIRST(predicateList) = {"STRING", "ID"}
        if(self.get_curr_token().getType() == "STRING"):
            self.match("STRING")
            return Parameter(self.get_prev_token_val())
        elif(self.get_curr_token().getType() == "ID"):
            self.match("ID")
            return Parameter(self.get_prev_token_val())
        else:
            self.throw_error()