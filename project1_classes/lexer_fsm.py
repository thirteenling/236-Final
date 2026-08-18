from .fsa_classes.fsa import FSA
from .fsa_classes.colon_dash_fsa import ColonDashFSA
from .fsa_classes.colon_fsa import ColonFSA
from .fsa_classes.undefined_fsa import UndefinedFSA
from .fsa_classes.schemes_fsa import SchemesFSA
from .fsa_classes.facts_fsa import FactsFSA
from .fsa_classes.rules_fsa import RulesFSA
from .fsa_classes.queries_fsa import QueriesFSA
from .fsa_classes.id_fsa import IDFSA
from .fsa_classes.string_fsa import StringFSA
from .fsa_classes.comment_fsa import CommentFSA
from .fsa_classes.eof_fsa import EOFFSA
from .fsa_classes.add_fsa import AddFSA
from .fsa_classes.comma_fsa import CommaFSA
from .fsa_classes.left_paren_fsa import LeftParenFSA
from .fsa_classes.right_paren_fsa import RightParenFSA
from .fsa_classes.multiply_fsa import MultiplyFSA
from .fsa_classes.period_fsa import PeriodFSA
from .fsa_classes.q_mark_fsa import QMarkFSA
from my_token import Token

class LexerFSM:
    def __init__(self):
        self.line_num = 1
        self.untouched_input = ""
        
        self.tokens: list[Token] = []
        self.automata: list = []
        self.tokens: list[Token] = []
        
        # Adding all FSAs to the automata list
        self.add_fsa: AddFSA = AddFSA()
        self.automata.append(self.add_fsa)
        self.colon_dash_fsa: ColonDashFSA = ColonDashFSA()
        self.automata.append(self.colon_dash_fsa)
        self.colon_fsa: ColonFSA = ColonFSA()
        self.automata.append(self.colon_fsa)
        self.comma_fsa: CommaFSA = CommaFSA()
        self.automata.append(self.comma_fsa)
        self.comment_fsa: CommentFSA = CommentFSA()
        self.automata.append(self.comment_fsa)
        self.facts_fsa: FactsFSA = FactsFSA()
        self.automata.append(self.facts_fsa)
        self.left_paren_fsa: LeftParenFSA = LeftParenFSA()
        self.automata.append(self.left_paren_fsa)
        self.multiply_fsa: MultiplyFSA = MultiplyFSA()
        self.automata.append(self.multiply_fsa)
        self.period_fsa: PeriodFSA = PeriodFSA()
        self.automata.append(self.period_fsa)
        self.q_mark_fsa: QMarkFSA = QMarkFSA()
        self.automata.append(self.q_mark_fsa)
        self.queries_fsa: QueriesFSA = QueriesFSA()
        self.automata.append(self.queries_fsa)
        self.right_paren_fsa: RightParenFSA = RightParenFSA()
        self.automata.append(self.right_paren_fsa)
        self.rules_fsa: RulesFSA = RulesFSA()
        self.automata.append(self.rules_fsa)
        self.schemes_fsa: SchemesFSA = SchemesFSA()
        self.automata.append(self.schemes_fsa)
        self.string_fsa: StringFSA = StringFSA()
        self.automata.append(self.string_fsa)
        self.id_fsa: IDFSA = IDFSA()
        self.automata.append(self.id_fsa)
        # Undefined and EOF automata
        self.undefined_fsa: UndefinedFSA = UndefinedFSA()
        self.automata.append(self.undefined_fsa)
        self.eof_fsa: EOFFSA = EOFFSA()
        # other FSA classes and any other member variables you need
    
    # run handles full input string
    def run(self, input: str) -> str:
        self.undefined_error: bool = False
        self.untouched_input = input
        # Split the full input into lines to make it more manageable
        split_input: list[str] = input.splitlines()
        for line in split_input:
            # Iterate until line is fully lexed
            while(line.strip() != ""):
                # Clear the whitespace from the front of the line before each token read attempt
                while(line[0].isspace()):
                    line = line[1:]
                #assert(isinstance(line, str))
                lexed_token = self.lex(line)
                #print(line)
                # Don't append comments to list for ease of parsing
                if(lexed_token.getType() != "COMMENT"):
                    self.tokens.append(lexed_token)
                line = line[len(str(lexed_token.getValue())):]
                if(lexed_token.getType() == "UNDEFINED"): 
                    self.undefined_error = True
                    break
                for automaton in self.automata: automaton.reset()
            if(self.undefined_error): break    
            self.line_num += 1
        if(not self.undefined_error): 
            eof_token = self.eof_fsa.make_token(line_num=self.line_num)
            self.tokens.append(eof_token)
    
    # lex handles input lines
    def lex(self, input_str: str) -> Token:
        max_read: int = 0
        max_automata: FSA = self.automata[0]
        
        for automaton in self.automata:
            if(automaton.run(input_str)):
                if(len(str(automaton.make_token(input_str=input_str, line_num=self.line_num).getValue())) > max_read):
                    max_read = len(str(automaton.make_token(input_str=input_str, line_num=self.line_num).getValue()))
                    max_automata = automaton
        return max_automata.make_token(input_str=input_str, line_num=self.line_num)

    def __manager_fsm__(self) -> Token:
        ...

    def reset(self) -> None:
        self.line_num = 1
        self.untouched_input = ""
        self.tokens: list[Token] = []
        self.automata: list[FSA] = []
        self.tokens: list[Token] = []