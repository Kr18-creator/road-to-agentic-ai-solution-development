from enum import Enum
import math

class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2

class Point:
    # def __init__(self, a, b, system=CoordinateSystem.CARTESIAN):
    #     if system == CoordinateSystem.CARTESIAN:
    #         self.x = a
    #         self.y = b
    #     elif system == CoordinateSystem.POLAR:
    #         self.x = a * math.cos(b)
    #         self.y = a * math.sin(b)
    ### Above initialization method can quickly get complex
    ### Using Factory Method
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'

    @staticmethod
    def new_cartesian_point(x, y):
        return Point(x, y)
    
    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho * math.cos(theta), rho * math.sin(theta))
    
if __name__ == "__main__":
    p = Point(2, 3)
    p2 = Point.new_polar_point(1, 2)
    print(p, p2)