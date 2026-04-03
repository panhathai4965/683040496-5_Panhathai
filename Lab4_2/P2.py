"""
Panhathai Suporn
683040496-5
P2
"""
from datetime import datetime

class Cat:
    species = "Felic catus"
    total_cats = 0
    average_lifespan =15

    def __init__(self, name, age, breed, color, weight):
        if not name:
            raise ValueError("Name is reqiured")
        
        #Instance attr
        self.name = name
        self.age = age
        self.breed = breed
        self.color = color
        self.weight = weight

        # stack
        self.hungry = False
        self.happiness = 100
        self.energy = 100

    def meow(self):
        if self.hungry:
            return "MEOW meow---OWO (hungry)"
        
        elif self.happiness < 15:
            return "Mew....prr....(need more fun)"
        
        elif self.happiness > 80:
            return "MEOW ^^ prr----(So happy!!)"
        
        elif self.energy < 30:
            return "meow........(need sleep)"
        
        else:
            return "Meow..."
        

    def eat(self, food_amount):
        if food_amount < 0:
            return "No Food????"
        

        self.hungry = False
        self.energy = min(100, self.energy + food_amount * 2)
        self.happiness = min(100, self.happiness + food_amount)

        return f"{self.name} Enjoin MEOW mOWOm"
    
    def play(self, play_time):
        if play_time < 0:
            return "meow..... (No play?)"
        
        self.energy = max(0, self.energy - play_time * 10)
        self.happiness = max(100, self.happiness + play_time * 5)

        if self.energy < 30:
            self.hungry = True

        return f"{self.name} have played for {play_time} hours."
    
    def sleep(self, hours):
        if hours <= 0:
            return "No sleep hours"
        
        self.energy = min(100, self.energy + hours * 15)
        self.hungry = True

        return f"{self.name} have slept for {hours} hours."
    
    def get_status(self):
        return {
            "name": self.name,
            "age": self.age,
            "breed": self.breed,
            "color": self.color,
            "hungry": self.hungry,
            "energy": self.energy,
            "happiness": self.happiness
        }
    

    @classmethod
    def from_birth_year(cls, name, birth_year, breed, weight):
        current_year = datetime.now().year
        age = current_year - birth_year
        
        return cls(name, age, breed, weight)
    
    @classmethod
    def get_species_info(cls):
        return {
            "species": cls.species,
            "total_cats": cls.total_cats,
            "average_lifespan": cls.average_lifespan
        }
    
    @staticmethod
    def in_senior(age):
        return age > 7
    
    def calculate_healthy_food_amount(weight):
        return weight * 20



