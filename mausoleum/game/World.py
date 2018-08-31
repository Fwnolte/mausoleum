from mausoleum.game.Item import Item


class World:
    def __init__(self, environments, current_environment, inventory_list):
        self.environments = environments
        
        # TODO: Use formatter in here, or actually make this good.
        if current_environment not in self.environments:
            print("Error initializing world! Starting environment is not in environment list!")
            exit()

        self.current_environment = current_environment
        self.inventory = inventory_list if isinstance(inventory_list, list) else []

    # TODO: This should probably be removed in favor of passing the logic further up
    def get_current_environment_description(self):
        return self.current_environment.description
    
    def travel(self, direction):
        if direction in self.current_environment.travel_destinations:
            destination = self.current_environment.travel_destinations[direction]
            self.current_environment = destination
            return True

        return False
        
    def get_inventory(self):
        return [item.reference_description for item in self.inventory]

    # TODO: Remove this once debugging/tests are properly implemented. Call .append directly
    # TODO: Logic should be moved away from the World class
    def add_to_inventory(self, item):
        if item is None:
            print("DEBUG: Tried to add \"None\" to inventory")
            return False
        elif not isinstance(item, Item):
            print("DEBUG: Tried to add a non-Item to inventory")
            return False

        self.inventory.append(item)
        return True

    # TODO: Remove this once debugging/tests are properly implemented. Call find_in_inventory() followed by a .remove
    # TODO: Logic should be moved away from the World class
    def remove_from_inventory(self, item):
        if item is None:
            print("DEBUG: Tried to remove \"None\" from inventory")
            return False
        elif item not in self.inventory:
            print("DEBUG: Tried to remove nonexistent item from inventory: \"" + item.name + "\"")
            return False
        else:
            self.inventory.remove(item)
            return True

    # TODO: Perhaps combine this with the find method in Environment class?
    # TODO: Alternatively, make a find_in_current_location() method here to find items in current_environment
    def find_in_inventory(self, item_to_find):
        if not isinstance(item_to_find, str):
            print("DEBUG: Tried to find an item in the inventory by passing a non-string")
            return None

        item_to_find = item_to_find.lower()
        # Todo: Logic for two items with similar names/types.
        for thing in self.inventory:
            if thing.name.lower() == item_to_find:
                return thing

        return None
