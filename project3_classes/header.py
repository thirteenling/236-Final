class Header:
    def __init__(self, values: list[str]):
        self.values: list[str] = values
    
    def __str__(self):
        return ",".join(self.values)