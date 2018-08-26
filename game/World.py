class World:
    def __init__(self, environments, current_environment):
        self.environments = environments
        
        #TODO: Use formatter in here, or actually make this good.
        if current_environment not in self.environments:
            print("Error initializing world!")
            exit()
        
        self.current_environment = current_environment
        self.inventory = []
        
    def get_current_environment_description(self):
        return self.current_environment.description
    
    def travel(self, direction):
        destination = self.current_environment.travel_destinations[direction]
        self.current_environment = destination
        
    def get_inventory(self):
        names = []
        
        for item in self.inventory:
            names += item.name
        
        return names
        
    def add_to_inventory(self, item):
        self.inventory.push(item)
        
    def remove_from_inventory(self, item):
        if item not in inventory:
            print("DEBUG: Tried to remove nonexistent item from inventory: \"" + item.name + "\"")
