from functools import total_ordering

@total_ordering
class mutableInt:
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        return self.value == other

    def __lt__(self, other):
        return self.value < other

    def __iadd__(self, other):
        self.value += other
        return self

    def __add__(self, other):
        return self.value + other

    def __isub__(self, other):
        self.value -= other
        return self

    def __sub__(self, other):
        return self.value - others