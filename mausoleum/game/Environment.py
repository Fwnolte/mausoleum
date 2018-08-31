from mausoleum.game.Describable import Describable


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
        
    def find(self, item_to_find):
        item_to_find = item_to_find.lower()
        all_searchable_things = self.items + self.characters + self.interactibles
        # TODO: Logic for two items with similar names/types.
        for thing in all_searchable_things:
            if thing.name.lower() == item_to_find:
                return thing

        return None

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item not in self.items:
            # TODO: Remove Debug statement
            print("DEBUG: Tried to remove nonexistent item from environment " + self.name + ": \"" + item.name + "\"")
            return False
        else:
            self.items.remove(item)
            return True
