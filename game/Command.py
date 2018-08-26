import os.path
from resources.GameFormatter import Formatter

class Command:
    filler_words = ["the", "at", "and"]
    
    def __init__(self, file_path, formatter, world):
        self.formatter =  formatter
        self.load_valid_command_list(file_path)
        self.world = world

    def load_valid_command_list(self, file_path):
        self.command_file = file_path
        
        if os.path.isfile(self.command_file):
            with open(self.command_file) as f:
                self.valid_command_list = [line.rstrip('\n') for line in f]

                #TODO: Validate no improper commands in the list
        else:
            self.formatter.print_error("Fatal error! Command file \"" + str(self.command_file) + "\" not found.")
            exit()


    def get_command(self):
        command = input("\n>> ")
        
        command = self.parse_command(command)
        
        if self.is_legal_command(command):
            return command
        
        return None

    def parse_command(self, command):
        command_tokens = command.lower().split()
        
        #Convert "pick up" to "take"
        if len(command_tokens) > 2 and command_tokens[0] == "pick" and command_tokens[1] == "up":
            del command_tokens[0]
            command_tokens[0] = "take"
        
        #Removes all "filler words" from our command syntax
        return [token for token in command_tokens if token not in self.filler_words]

    def is_legal_command(self, command_tokens):
        #TODO: Add more logic to this to detect more cases where a command is invalid
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
        
        if command == "look" or command == "describe": #TODO: Convert command list to JSON and implement synonym detection
            if len(command_args) > 1:
                self.formatter.print_warning("You can't look at two things at once!") #TODO: Make it so you can look at more than one thing
                return False
            elif len(command_args) == 0:
                result = self.describe()
            else:
                result = self.describe(command_args[0])
                
        if command == "take" or command == "grab" or command == "get":
            if len(command_args) != 1:
                self.formatter.print_warning("You can't grab two things at once!") #TODO: Make it so you can grab more than one thing
                return False
            
            result = self.take(command_args[0])
                
        if command == "go":
            if len(command_args) == 0:
                self.formatter.print_warning("You need to specify somewhere to go!")
            elif len(command_args) != 1:
                self.formatter.print_warning("You can't go two places at once!")
                return False
                
            result = self.go(command_args[0])
                
        return result
        
    #COMMANDS
    def quit(self):
        self.formatter.print_text("See you later!")
        exit()
    
    #TODO: Needs better logic
    def describe(self, thing=None):
        current_room = self.world.current_environment
        
        if thing is None or thing == "room" or thing == "area" or thing == "surroundings": #TODO: Synonym detection
            self.formatter.print_text(current_room.description)
            return True
        
        if thing == "inventory" or thing == "items":
            inventory = self.world.get_inventory()
            if not inventory: 
                self.formatter.print_text("There's nothing in your inventory right now.")
            else:
                items = self.formatter.make_list(inventory)
                self.formatter.print_text("Your inventory contains " + items)
            return True
            
        object = current_room.find(thing)
        
        if object is not None:
            self.formatter.print_text(object.description)
            return True
            
        return False
    
    
    def take(self, item):
        current_room = self.world.current_environment
        
        object = current_room.find(item)
        
        if object is None:
            print("DEBUG: Could not find \"" + item + "\" in room")
            return False
        else:
            print("DEBUG: " + item.name + " taken!") #TODO: Add inventory
            return True
        
        return False
        
        
    def go(self, direction):
        if direction not in self.world.current_environment.travel_destinations:
            self.formatter.print_warning("\"" + direction + "\" is not a valid direction!")
            return False
        
        #TODO: Add in logic to check for blocked/locked/unavailable passageways.
        
        self.world.travel(direction)
        
        current_room = self.world.current_environment
        self.formatter.print_new_room(current_room.name, current_room.description)
        return True
        
        