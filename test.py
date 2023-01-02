class Pair:

    def __init__(self, x, y):
        self.a = x
        self.b = y

    def __str__(self):
        return str(self.a) + ", " + str(self.b)
    def opposite(self):
        if self.a < 0:
            x = self.a + 2 * self.a
        elif self.a > 0:
            x = self.a - 2 * self.a
            
        if self.b < 0:
            y = self.b + 2 * self.b
        elif self.b > 0:
            y = self.b - 2 * self.b
        return Pair(x,y)

paire = Pair(10,-2)
instance  = paire.opposite()
print(instance)