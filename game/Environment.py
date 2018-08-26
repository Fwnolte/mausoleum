from game.Describable import Describable

class Environment(Describable):
    def __init__(self, name, description, reference_description, items, characters, interactibles):
        super().__init__(name, description, reference_description)
        self.items = items
        self.characters = characters
        self.interactibles = interactibles
        self.travel_destinations = {}
    
    def add_travel_destination(self, direction, environment):
        old_environment = None
        
        if direction in self.travel_destinations:
            old_environment = self.travel_destinations[direction]
            
        self.travel_destinations[direction] = environment
        
        return old_environment
        
    def find(self, object):
        list = self.items + self.characters + self.interactibles
        for item in list:
            if item.name == object:
               return item
        
        return None
        
