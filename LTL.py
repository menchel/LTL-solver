class Prop:
    def __init__(self, name):
        self.name = name

class Not:
    def __init__(self, inner):
        self.inner = inner

class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Next:
    def __init__(self, inner):
        self.inner = inner

class Eventually:
    def __init__(self, inner):
        self.inner = inner

class Always:
    def __init__(self, inner):
        self.inner = inner

class Until:
    def __init__(self, start, end):
        self.start = start
        self.end = end
