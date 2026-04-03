"""
Panhathai Suporn
683040496-5
P1
"""

import room
if __name__ == "__main__":
    
    my_bedroom = room.Bedroom(11, 11, 6.3)
    print(my_bedroom.describe_room())
    print(my_bedroom.describe_room())
    print(f" The recommened light in the room is {my_bedroom.get_recommended_lighting()} lumens per square foot")
   
    print()
    
    my_kitchen = room.Kitchen(10, 12, True)
    print(my_kitchen.describe_room())
    print(my_kitchen.get_purpose())
    print(f"The recommened light in the room is {my_kitchen.get_recommended_lighting()} lumens per square foot")
    counter,wall = my_kitchen.calculate_counter_space()
    print(f"{counter} {wall}")
    print(room.Kitchen.calculate_counter_space.__doc__)
