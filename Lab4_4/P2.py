"""
Panhathai Supporn
683040496-5
P2
"""


from abc import ABC, abstractmethod


class vehicle(ABC):
    def __init__(self, make, model, year, is_running = False):
        self.make = make
        self.model = model
        self.year = year
        self.is_running = is_running

    @abstractmethod
    def start_engine(self):
        """start enginee"""
        pass
    
    @abstractmethod
    def stop_engine(self):
        """stop the vehicle's engine"""
        pass

    def get_info(self):
        return f"Year: {self.year} \nMake: {self.make} \nModel: {self.model}"
    
class CommercialVehicle(vehicle):
    def __init__(self, license_number, max_load, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_load = max_load
        self.license_number = license_number
        self.current_load = 0
    def start_engine(self):
        self.is_running = True
        return "started"
    def stop_engine(self):
        self.is_running = False
        return "stopped"
    def load_cargo(self, weight):
        if weight > 0 and (self.current_load + weight <= self.max_load):
            self.current_load += weight
            return True
        return False
    def unload_cargo(self, weight):
        if weight > 0 and (self.current_load - weight >= 0):
            self.current_load -= weight
        self.current_load = 0
        return self.current_load
class Car(vehicle):
    def __init__(self, num_doors, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.num_doors = num_doors
    def start_engine(self):
        self.is_running = True
        return "start engine"
    def stop_engine(self):
        self.is_running = False
        return "stop engine"
    
class Trailer(CommercialVehicle):
    def __init__(self, num_axles = 2, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.num_axles = num_axles
    def get_weight_per_axles(self):
        if self.num_axles <=0:
            return 0
        return self.current_load / self.num_axles

class DeliveryVan(Car, CommercialVehicle):
    def __init__(self, make, model, year, license_number, max_load, num_doors, is_running = False):
        super().__init__(license_number=license_number, max_load=max_load, make=make, model=model, year=year, is_running=is_running, num_doors=num_doors)
        self.delivery_mode = False
    def toggle_delivery_mode(self):
        self.delivery_mode = not self.delivery_mode
        return f"Delivery mode is {self.delivery_mode}"
    def begin_service(self):
        print(self.get_info())
        print(f"Loading in a cargo: {self.load_cargo(5000)} kg")
        print(self.start_engine())
        print(self.toggle_delivery_mode())
        print(self.stop_engine())
        print(f"Unloading the cargo{self.unload_cargo(1000)} kg")
        print(self.toggle_delivery_mode())
if __name__ == "__main__":
    poom = DeliveryVan("R8", "Ton", 2007,"683040497-3", 10000, "4", is_running = False  )
    poom.begin_service()