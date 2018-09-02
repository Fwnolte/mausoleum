from mausoleum.game.Describable import Describable
from mausoleum.game.Item import Item


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
        if not isinstance(item_to_find, str):
            print("DEBUG: Tried to find an item in the environment by passing a non-string")
            return None

        item_to_find = item_to_find.lower()
        all_searchable_things = self.items + self.characters + self.interactibles
        # Todo: Logic for two items with similar names/types.
        for thing in all_searchable_things:
            if thing.name.lower() == item_to_find:
                return thing

        return None

    def add_item(self, item):
        if item is None:
            print("DEBUG: Tried to add \"None\" to inventory")
            return False
        elif not isinstance(item, Item):
            print("DEBUG: Tried to add a non-Item to inventory")
            return False
        else:
            self.items.append(item)
            return True

    def remove_item(self, item):
        if item is None:
            print("DEBUG: Tried to remove item \"None\" from current environment")
            return False
        elif not isinstance(item, Item):
            print("DEBUG: Tried to remove a non-item from inventory: " + str(item))
            return False
        elif item not in self.items:
            print("DEBUG: Tried to remove nonexistent item from environment: \"" + item.name + "\"")
            return False
        else:
            self.items.remove(item)
            return True
