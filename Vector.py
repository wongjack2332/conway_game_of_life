class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self) -> tuple:
        return (self.x, self.y)

    def add(self, a, b):
        self.x += a
        self.y += b
