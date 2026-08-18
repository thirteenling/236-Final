from project1_classes.lexer_fsm import LexerFSM
from project2_classes.dl_parser import Parser
from my_token import Token
from project3_classes.database import *
from project3_classes.interpreter import *
from project3_classes.graph import Graph

#Return your program output here for grading (can treat this function as your "main")
def project5(input: str) -> str:
    lexer: LexerFSM = LexerFSM()
    lexer.run(input)
    tokens: list[Token] = lexer.tokens
    
    parser: Parser = Parser()
    parser.run(tokens)
    program: DatalogProgram = parser.program
    #print(program.to_string())
    
    interpreter: Interpreter = Interpreter()
    interpreter_result = interpreter.run(program)
    #print(interpreter_result)
    return interpreter_result

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents("project5-passoff/80/input0.txt")
    print(project5(input_contents))
