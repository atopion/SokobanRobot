from enum import Enum

class Directions(Enum):     
    """Define Up, Right, Down and Left for further movement controll"""
    up = 0
    right = 1
    down = 2
    left = 3

    def __sub__(self, y):
        """Method to subtract a Direction from another Direction"""
        return self.value - y.value
    
