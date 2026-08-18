from .data_structures import *
from .database import *
from .graph import Graph
class Interpreter:
    def __init__(self):
        self.output_str = ""
        self.database = Database()
        self.rules_passes = 0
        self.rules_added_tuples = []
        
    def run(self, dl_program: DatalogProgram):
        self.program: DatalogProgram = dl_program
        self.evaluate_schemes()
        self.evaluate_facts()
        self.rules_passes = 0
        self.rules_added_tuples = []
        # Create dependency graph
        rule_list = self.program.getRules()
        rule_graph = Graph(len(rule_list))
        for r in range(len(rule_list)):
            for p in rule_list[r].bodyPredicates:
                for h in range(len(rule_list)):
                    if p.name == rule_list[h].headPredicate.name:
                        rule_graph.add_edge(r,h)
        self.output_str += "Dependency Graph\n"
        self.output_str += str(rule_graph)
        self.output_str += "\n"
        # Create reverse dependency graph
        reverse_graph = rule_graph.make_reverse()
        self.output_str += "Rule Evaluation\n"
        # Rule evaluation algorithm
        reverse_graph.dfs_forest()
        rev_postorder = reverse_graph.postorder
        rev_postorder.reverse()
        sccs = rule_graph.dfs_forest_scc(rev_postorder)
        for scc in sccs:
            input_list = [rule_list[num] for num in scc]
            self.output_str += f"SCC: R{',R'.join([str(num) for num in scc])}\n"
            self.rules_passes = 0
            self.evaluate_rules(input_list)
            self.output_str += f"{self.rules_passes} passes: R{',R'.join([str(num) for num in scc])}\n"
        self.output_str += "\nQuery Evaluation\n"
        self.evaluate_queries()
        return self.output_str
        
    def evaluate_schemes(self):
        #Start with an empty Database. 
        self.database: Database = Database()
        # For each scheme in the Datalog program,
        for scheme in self.program.getSchemes():
        #   add an empty Relation to the Database. 
            param_list = []
            for param in scheme.parameters:
                param_list.append(param.value)
            self.database.add_relation(scheme.name, Relation(scheme.name, Header(param_list),set()))
        #   Use the scheme name as the name of the relation 
        #   Use the attribute list from the scheme as the header of the relation.
    
    def evaluate_facts(self):
        # For each fact in the Datalog program, 
        for fact in self.program.getFacts():
        #   add a Tuple to a Relation. 
            param_list: list[str] = []
            for param in fact.parameters:
                param_list.append(param.value)
            self.database.get_relation(fact.name).add_tuple(Tuple(param_list))
        #   Use the predicate name from the fact to 
        #   determine the Relation to which the Tuple should be added. 
        #   Use the values listed in the fact to provide the values for the Tuple.
    
    def evaluate_queries(self):
        # for each query in the datalog_program call evaluate predicate.
            # append the predicate returned by this function to the output string
        for query in self.program.getQueries():
            self.output_str += query.to_string()
            self.output_str += "? "
            query_output = self.evaluate_predicate(query)
            if query_output.num_tuples() == 0:
                self.output_str += "No"
            else:
                self.output_str += f"Yes({query_output.num_tuples()})"
            self.output_str += "\n"
            self.output_str += query_output.__str__()
        # output notes:
        # For each query, output the query and a space. 
        # If the relation resulting from evaluating the query is empty, output 'No'. 
        # If the resulting relation is not empty, output 'Yes(n)' where n is the number of tuples in the resulting relation.
        
        # If there are variables in the query, output the tuples from the resulting relation.

        # Output each tuple on a separate line as a comma-space-separated list of pairs.
        # Each pair has the form N='V', 
        # where N is the attribute name from the header and V is the value from the tuple. 
        # Output the name-value pairs in the same order as the variable names appear in the query. 
        # Indent the output of each tuple by two spaces.
        
        # some of this output code was given to you in the Relation.__str__() function. 
        # It may need to be modified slightly

        # Output the tuples in sorted order. 
        # Sort the tuples alphabetically based on the values in the tuples. 
        # Sort first by the value in the first position and if needed up to the value in the nth position.
    
    def evaluate_predicate(self, predicate: Predicate) -> Relation:
        # For this predicate you need to
        #   use a sequence of select, project, and rename operations on the Database 
        #   to evaluate the query. Evaluate the queries in the order given in the input.
        # Get the Relation from the Database with the 
        #   same name as the predicate name in the query.
        curr_relation = self.database.get_relation(predicate.name)
        # Use one or more select operations to select 
        #   the tuples from the Relation that match the query. 
        #   Iterate over the parameters of the query: 
        value_list = [param.value for param in predicate.parameters]
        for i in range(len(predicate.parameters)):
            if predicate.parameters[i].is_id:
        #       If the parameter is a constant, 
                curr_relation = curr_relation.select_has_value(i,predicate.parameters[i].value)
        #           select the tuples from the Relation that have the same value as the constant in the same position as the constant. 
            elif (not predicate.parameters[i].is_id) and (i-1 < len(value_list) and predicate.parameters[i].value in value_list[i+1:]): 
        #       If the parameter is a variable and the same variable name appears later in the query, 
                #print(value_list)
                matching_indexes = [index for index, value in enumerate(value_list[i+1:]) if value == value_list[i]]
                #print(matching_indexes)
                #print(f"Matching with {i} ({predicate.parameters[i].value}) and {i+1+matching_indexes[0]} ({predicate.parameters[i+1+matching_indexes[0]].value})")
                curr_relation = curr_relation.select_matches_value(i,i+1+matching_indexes[0])
        #           select the tuples from the Relation that have the same value in both positions where the variable name appears.
        # After selecting the matching tuples, use the project operation 
        value_list = [param.value for param in predicate.parameters]
        column_list = []
        matching_indexes = []
        for i in range(len(predicate.parameters)):
            if (not predicate.parameters[i].is_id) and (not (predicate.parameters[i].value in column_list)):
                matching_indexes.append(i)
                column_list.append(predicate.parameters[i].value)
        curr_relation = curr_relation.project(matching_indexes)
        #   to keep only the columns from the Relation that correspond to the 
        #   positions of the variables in the query. Make sure that each variable name appears only once in the resulting relation. 
        #   If the same name appears more than once, keep the first column where the name appears and remove any later columns where the same name appears. 
        #   (This makes a difference when there are other columns in between the ones with the same name.)
        # After projecting, use the rename operation to 
        #   rename the header of the Relation to the
        #   names of the variables found in the query.
        header_list = []
        for i in range(len(predicate.parameters)):
            if i in matching_indexes and (not predicate.parameters[i].is_id):
                header_list.append(predicate.parameters[i].value)
        for i in range(len(header_list)):
            #print(f"Renaming position {i} to {header_list[i]}")
            curr_relation = curr_relation.rename(i,header_list[i])
        # The operations must be done in the order described above: 
        #   any selects, 
        #   followed by a project, 
        #   followed by a rename.
        # return the new predicate
        self.current_relation = curr_relation
        return curr_relation
    
    def evaluate_rules(self, rule_list: list[Rule]):
        #print(self.database.__str__())
        # Check how many tuples are in the database
        num_tuples = self.database.get_num_tuples()
        self.rules_passes += 1
        result_str = ""
        
        for rule in rule_list:
            self.output_str += rule.to_string()
            self.output_str += ".\n"
            # Step 1: Evaluate every body predicate in the rule
            relation_list: list[Relation] = []
            for predicate in rule.bodyPredicates:
                relation_list.append(self.evaluate_predicate(predicate))
                #print(self.evaluate_predicate(predicate).__str__())
            # Step 2: Join all the resulting relations (if only one relation, just leave it)
            joined_relation = relation_list[0]
            if len(relation_list) > 1:
                for rel in relation_list[1:]:
                    joined_relation = joined_relation.join(rel)
            # Step 3: Use Project to make the header of new relation match the head predicate
            index_list = []
            for param in rule.headPredicate.parameters:
                index_list.append(joined_relation.header.values.index(param.value))
            joined_relation = joined_relation.project(index_list)
            # Step 4: Rename the new relation to match the relation in database with same name as head predicate
            db_relation = self.database.get_relation(rule.headPredicate.name)
            for i in range(len(db_relation.header.values)):
                joined_relation = joined_relation.rename(i, db_relation.header.values[i])
            
            temp = self.database.get_num_tuples()
            # Step 5: Union the new relation with the relation in the database that has the same name as the new relation
            db_relation = db_relation.union(joined_relation)
            str_relation = Relation(joined_relation.name, joined_relation.header)
            for tuple in joined_relation.tuples:
                if not (tuple in self.database.get_relation(db_relation.name).tuples):
                    str_relation.add_tuple(tuple)
            self.database.add_relation(db_relation.name, db_relation)
            #if temp < self.database.get_num_tuples():
            
            self.output_str += str_relation.__str__()
        # Check how many tuples are in the database
        if num_tuples < self.database.get_num_tuples():
            # If there are more tuples now than before, evaluate rules again
            self_dependant = False
            if len(rule_list) == 1:
                # if there is only one rule in scc:
                for b in rule_list[0].bodyPredicates:
                #     loop over body predicates of that rule:
                    if b.name == rule_list[0].headPredicate.name:
                #         if a body predicate has the same name as the head predicate:
                #             self_dependant = True
                        self_dependant = True
                if self_dependant: self.evaluate_rules(rule_list)
                return
            if not self_dependant: self.evaluate_rules(rule_list)