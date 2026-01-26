"""
Panhathai Suporn
683040496-5
P1
"""

from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    @abstractmethod
    def get_purpose(self):
        """Returns a string describing purposes of the room"""
        pass

    @abstractmethod
    def get_recommended_lighting(self):
        """Returns recommended lighting in lumens per square foot"""
        pass

    def calculate_area(self):
        return self.length * self.width
    
    def describe_room(self):
        area = self.calculate_area()
        return f"A {self.__class__.__name__} of {area} sq ft used for {self.get_purpose()}"

class Bedroom(Room):
    def __init__(self, length, width, bed_size):
        super().__init__(length, width)
        self.bed_size = bed_size
    def get_purpose(self):
        return f"I am sleeping here on a {self.bed_size} ft bed"
    def get_recommended_lighting(self):
        return 15
class Kitchen(Room):
    def __init__(self, length, width, has_island = True):
        super().__init__(length, width)
        self.has_island = has_island
    def get_purpose(self):
        return "I make food and enjoy cooking here"
    def get_recommended_lighting(self):
        return 75
     
    def calculate_counter_space(self):
        """ Calculates the area of island and wall.
        Args: 
            None
        Returns:
            float: The area of the island_counter 
            float: The area of the wall_counter
        Raises:
            ValueError: If the calculated area is zero or negative, we cannot detemine the counter space.
        Examples:
            >>> obj.calculate_counter_space(11, 12, True)
        """
        area = self.calculate_area()
        if self.has_island:
            self.island_counter_area = area / 5
            self.wall_counter_area = area / 4
        else:
            self.island_counter_area = 0
            self.wall_counter_area = area / 2
        return self.island_counter_area , self.wall_counter_area
                
    
        
