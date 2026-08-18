from typing import Callable
from my_token import Token

class FSA:
    def __init__(self):
        self.start_state: Callable = self.s0
        self.accept_states: set[Callable] = set()
        
        self.input_string: str = ""
        self.fsa_name: str = ""
        self.chars_read: int = 0
        self.token_size = 0
        
    
    def s0(self) -> Callable:
        raise NotImplementedError()
    
    def run(self, input_str: str) -> bool:
        self.input_string = input_str
        current_state: Callable = self.start_state
        while self.chars_read < len(self.input_string):
            current_state = current_state()
        outcome: bool = False
        if current_state in self.accept_states: outcome = True
        return outcome

    def reset(self) -> None:
        self.chars_read = 0

    def get_name(self) -> str: 
        return self.fsa_name

    def set_name(self, FSA_name: str) -> None:
        self.fsa_name = FSA_name

    def get_current_input(self) -> str:  # The double underscore makes the method private
        current_input: str = self.input_string[self.chars_read]
        self.chars_read += 1
        return current_input
    
    def make_token(self, value: str = "", line_num: int = 0, input_str: str = "") -> Token:
        if(self.fsa_name == "ID"): self.run(input_str)
        return Token(self.fsa_name, value, line_num)