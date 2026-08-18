from my_token import Token
from .fsa import FSA
from typing import Callable

class QueriesFSA(FSA):
    def __init__(self):
        super().__init__()
        self.accept_states.add(self.s7)
        self.token_size = 1
        self.fsa_name = "QUERIES"
    
    def s0(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input == 'Q':
            next_state = self.s1
        else:
            next_state = self.s_err
        return next_state
    
    def s1(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input == 'u':
            next_state = self.s2
        else:
            next_state = self.s_err
        return next_state
    
    def s2(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input == 'e':
            next_state = self.s3
        else:
            next_state = self.s_err
        return next_state
    
    def s3(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input == 'r':
            next_state = self.s4
        else:
            next_state = self.s_err
        return next_state
    
    def s4(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input == 'i':
            next_state = self.s5
        else:
            next_state = self.s_err
        return next_state
    
    def s5(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input == 'e':
            next_state = self.s6
        else:
            next_state = self.s_err
        return next_state
    
    def s6(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input == 's':
            next_state = self.s7
        else:
            next_state = self.s_err
        return next_state
    
    def s7(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = self.s7
        return next_state
    
    def s_err(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = self.s_err
        return next_state
    
    def make_token(self, input_str: str = "", line_num: int = 0) -> Token:
        return super().make_token("Queries", line_num)