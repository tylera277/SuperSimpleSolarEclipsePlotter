import math

class AngleCalculations:

    def __init__(self, x_comp, y_comp, z_comp):

        self.x_comp = x_comp
        self.y_comp = y_comp
        self.z_comp = z_comp

    def theta(self):
        return math.atan(self.y_comp/self.x_comp)

    def phi(self):
        return math.atan((math.sqrt(self.x_comp ** 2.0 + self.y_comp ** 2.0)) / self.z_comp)


