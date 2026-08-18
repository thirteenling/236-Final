from my_token import Token
from .fsa import FSA
from typing import Callable

class ColonDashFSA(FSA):
    def __init__(self):
        super().__init__()
        self.accept_states.add(self.s2)
        self.token_size = 2
        self.fsa_name = "COLON_DASH"
    
    def s0(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input == ':':
            next_state = self.s1
        else:
            next_state = self.s_err
        return next_state
    
    def s1(self) -> Callable:
        current_input: str = self.get_current_input()
        next_state: Callable = None
        if current_input == '-':
            next_state = self.s2
        else:
            next_state = self.s_err
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
        return super().make_token(":-", line_num)