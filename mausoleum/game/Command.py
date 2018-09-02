import os.path
# from resources.GameFormatter import Formatter


class Command:
    FILLER_WORDS = ["the", "at", "and"]
    
    def __init__(self, file_path, formatter, world):
        self.file_path = file_path
        self.formatter = formatter
        self.world = world
        self.valid_command_list = []

    def load_valid_command_list(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path) as f:
                result = [line.rstrip('\n') for line in f]

            # TODO: Validate no improper commands in the list
            self.valid_command_list = result
        else:
            self.formatter.print_error("Fatal error! Command file \"" + str(self.file_path) + "\" not found.")
            exit()

    def get_command(self):
        command = input("\n>> ")
        
        command = self.parse_command(command)
        
        if self.is_legal_command(command):
            return command
        
        return None

    def parse_command(self, command):
        command_tokens = command.lower().split()
        
        # Convert "pick up" to "take"
        if len(command_tokens) > 2 and command_tokens[0] == "pick" and command_tokens[1] == "up":
            del command_tokens[0]
            command_tokens[0] = "take"
        
        # Removes all "filler words" from our command syntax
        return [token for token in command_tokens if token not in self.FILLER_WORDS]

    def is_legal_command(self, command_tokens):
        # TODO: Add more logic to this to detect more cases where a command is invalid

        if not isinstance(command_tokens, list):
            print("DEBUG: Called 'is_legal_command()' with a non-list.")
            return False

        if len(command_tokens) == 1 and command_tokens[0] == "":
            self.formatter.print_invalid_command("Commands cannot be empty.")
            return False
        
        if command_tokens[0] not in self.valid_command_list:
            self.formatter.print_invalid_command()
            return False
        
        return True

    def perform_command(self, command_tokens):
        command = command_tokens[0]
        command_args = command_tokens[1:]
        
        if command == "quit":
            self.quit()

        # TODO: Convert command list to JSON and implement synonym detection
        if command == "look" or command == "describe":
            if len(command_args) > 1:
                # TODO: Make it so you can look at more than one thing
                self.formatter.print_warning("You can't look at two things at once!")
                return False
            elif len(command_args) == 0:
                return self.describe()
            else:
                # TODO: Can we make this a single line through overloading/ternary?
                return self.describe(command_args[0])
                
        elif command == "take" or command == "grab" or command == "get":
            if len(command_args) == 0:
                self.formatter.print_warning("You need to name the object you want to take.")
                return False
            elif len(command_args) > 1:
                # TODO: Make it so you can grab more than one thing
                self.formatter.print_warning("You can't grab two things at once!")
                return False
            
            return self.take(command_args[0])

        elif command == "drop" or command == "discard":
            if len(command_args) == 0:
                self.formatter.print_warning("You need to name the object you want to drop.")
                return False
            elif len(command_args) > 1:
                # TODO: Make it so you can drop more than one thing
                self.formatter.print_warning("You can't drop two things at once!")
                return False

            return self.drop(command_args[0])

        elif command == "go":
            if len(command_args) == 0:
                self.formatter.print_warning("You need to specify somewhere to go.")
                return False
            elif len(command_args) != 1:
                self.formatter.print_warning("You can't go two places at once!")
                return False
                
            return self.go(command_args[0])

        else:
            self.formatter.print_warning("You need to specify a valid command.")
            return False

    # COMMANDS
    def quit(self):
        self.formatter.print_text("See you later!")
        exit()
    
    # TODO: Needs better logic
    def describe(self, thing=None):
        if thing is not None and not isinstance(thing, str):
            print("DEBUG: Illegal argument passed to describe method")
            return False

        # TODO: Better synonym detection
        if thing is None or thing == "room" or thing == "area" or thing == "surroundings":
            self.formatter.print_room_description(self.world.current_environment)
            return True
        
        if thing == "inventory" or thing == "items":
            inventory = self.world.get_inventory()
            if not inventory: 
                self.formatter.print_text("There's nothing in your inventory right now.")
                return True
            else:
                items = self.formatter.make_item_list(inventory)
                self.formatter.print_text("Your inventory contains " + items)
                return True

        # Determine if the item is in the current_environment
        item_in_room = self.world.current_environment.find(thing)
        if item_in_room is not None:
            self.formatter.print_text(item_in_room.description)
            return True

        # Determine if the item is in the player's inventory
        item_in_inventory = self.world.find_in_inventory(thing)
        if item_in_inventory is not None:
            # TODO: Can we do any better with this?
            self.formatter.print_text(item_in_inventory.description + " This item is in your inventory.")
            return True

        self.formatter.print_item_not_found(thing)
        return False
    
    def take(self, item_name):
        if not isinstance(item_name, str):
            print("DEBUG: Illegal argument passed to take method.")
            return False

        item_to_take = self.world.current_environment.find(item_name)
        
        if item_to_take is None:
            self.formatter.print_item_not_found(item_name)
            return False
        else:
            self.world.current_environment.remove_item(item_to_take)
            self.world.add_to_inventory(item_to_take)
            self.formatter.print_item_taken(item_to_take)
            return True

    def drop(self, item_name):
        if not isinstance(item_name, str):
            print("DEBUG: Illegal argument passed to drop method.")
            return False

        item_to_remove = self.world.find_in_inventory(item_name)

        if item_to_remove is None:
            self.formatter.print_item_not_found_in_inventory(item_name)
            return False
        else:
            self.world.remove_from_inventory(item_to_remove)
            self.world.current_environment.add_item(item_to_remove)
            self.formatter.print_item_dropped(item_to_remove)
            return True

    def go(self, direction):
        if not isinstance(direction, str):
            print("DEBUG: Illegal argument passed to go method.")
            return False

        if direction not in self.world.current_environment.travel_destinations:
            self.formatter.print_warning("\"" + direction + "\" is not a valid direction!")
            return False

        # TODO: Add in logic to check for blocked/locked/unavailable passageways.
        self.world.travel(direction)

        self.formatter.print_new_room(self.world.current_environment)

        return True
