from my_token import Token
from .fsa import FSA
from typing import Callable

class IDFSA(FSA):
    def __init__(self):
        super().__init__()
        self.stop_point = 1
        self.accept_states.add(self.s1)
        self.accept_states.add(self.s2)
        
        self.token_size = 1
        self.fsa_name = "ID"
    
    def s0(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input.isalpha():
            self.stop_point = self.chars_read
            next_state = self.s1
        else:
            next_state = self.s_err
        return next_state
    
    def s1(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input.isalnum():
            self.stop_point = self.chars_read
            next_state = self.s1
        else:# current_input.isspace():
            #self.stop_point = self.chars_read
            next_state = self.s2
        #else:
            #next_state = self.s_err
        return next_state
    
    def s2(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = self.s2
        return next_state
    
    def s_err(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = self.s_err
        return next_state
    
    def make_token(self, input_str: str = "", line_num: int = 0) -> Token:
        return super().make_token(input_str=input_str, value=self.input_string[:self.stop_point], line_num=line_num)