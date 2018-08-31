import os.path
# from resources.GameFormatter import Formatter


class Command:
    filler_words = ["the", "at", "and"]
    
    def __init__(self, file_path, formatter, world):
        self.formatter = formatter
        self.valid_command_list = self.load_valid_command_list(file_path)
        self.world = world
        self.current_environment = world.current_environment


    def load_valid_command_list(self, file_path):
        command_file = file_path
        
        if os.path.isfile(command_file):
            with open(command_file) as f:
                result = [line.rstrip('\n') for line in f]

            return result

        # TODO: Validate no improper commands in the list
        else:
            self.formatter.print_error("Fatal error! Command file \"" + str(command_file) + "\" not found.")
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
        return [token for token in command_tokens if token not in self.filler_words]

    def is_legal_command(self, command_tokens):
        # TODO: Add more logic to this to detect more cases where a command is invalid
        if len(command_tokens) == 1 and command_tokens[0] == "":
            self.formatter.print_invalid_command("Commands cannot be empty.")
            return False
        
        if command_tokens[0] not in self.valid_command_list:
            self.formatter.print_invalid_command()
            return False
        
        return command_tokens

    def perform_command(self, command_tokens):
        print("DEBUG: " + str(command_tokens))
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
                result = self.describe()
            else:
                # TODO: Can we make this a single line through overloading/ternary?
                result = self.describe(command_args[0])
                
        elif command == "take" or command == "grab" or command == "get":
            if len(command_args) != 1:
                # TODO: Make it so you can grab more than one thing
                self.formatter.print_warning("You can't grab two things at once!")
                return False
            
            result = self.take(command_args[0])

        elif command == "drop" or command == "discard":
            if len(command_args) != 1:
                # TODO: Make it so you can drop more than one thing
                self.formatter.print_warning("You can't drop two things at once!")
                return False

            result = self.drop(command_args[0])

        elif command == "go":
            if len(command_args) == 0:
                self.formatter.print_warning("You need to specify somewhere to go!")
            elif len(command_args) != 1:
                self.formatter.print_warning("You can't go two places at once!")
                return False
                
            result = self.go(command_args[0])

        else:
            return False

        return result
        
    # COMMANDS
    def quit(self):
        self.formatter.print_text("See you later!")
        exit()
    
    # TODO: Needs better logic
    def describe(self, thing=None):
        # TODO: Better synonym detection
        if thing is None or thing == "room" or thing == "area" or thing == "surroundings":
            self.formatter.print_room_description(self.current_environment)
            return True
        
        if thing == "inventory" or thing == "items":
            inventory = self.world.get_inventory()
            if not inventory: 
                self.formatter.print_text("There's nothing in your inventory right now.")
            else:
                items = self.formatter.make_item_list(inventory)
                self.formatter.print_text("Your inventory contains " + items)
                return True
            
        found_item = self.current_room.find(thing)
        
        if found_item is not None:
            self.formatter.print_text(found_item.description)
            return True
            
        return False
    
    def take(self, item):
        item_to_take = self.current_environment.find(item)
        
        if item_to_take is None:
            self.formatter.print_item_not_found(item)
            return False
        else:
            self.current_environment.remove_item(item_to_take)
            self.world.add_to_inventory(item_to_take)
            self.formatter.print_item_taken(item_to_take)
            return True

    def drop(self, item_name):
        item_to_remove = self.world.find_in_inventory(item_name)

        if item_to_remove is None:
            self.formatter.print_item_not_found_in_inventory(item_name)
            return False
        else:
            self.world.remove_from_inventory(item_to_remove)
            self.current_environment.add_item(item_to_remove)
            self.formatter.print_item_dropped(item_to_remove)
            return True

    def go(self, direction):
        if direction not in self.current_environment.travel_destinations:
            self.formatter.print_warning("\"" + direction + "\" is not a valid direction!")
            return False
        
        # TODO: Add in logic to check for blocked/locked/unavailable passageways.
        
        self.world.travel(direction)

        # Update the current environment to the one we just traveled to
        self.current_environment = self.world.current_environment
        self.formatter.print_new_room(self.current_environment)
        return True
