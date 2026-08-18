class Token():
    def __init__(self, token_type: str, value: str, line_num: int):
        self.token_type = token_type
        self.value = value
        self.line = line_num

    def getLine(self) -> int:
        return self.line
    
    def getValue(self) -> str:
        return self.value
    
    def getType(self) -> str:
        return self.token_type
    
    def to_string(self) -> str:
        return f"({self.getType()},\"{self.getValue()}\",{self.getLine()})"