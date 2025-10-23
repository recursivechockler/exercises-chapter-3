from math import sqrt

class Circle:

    def __init__(self, centre, radius):
        if len(centre) != 2 or radius <= 0:
            return ValueError
        
        self.centre = centre
        self.radius = radius
    
    def __contains__(self, point):
        h, k = self.centre
        x, y = point

        return ((x - h)**2 + (y - k)**2 < self.radius**2)