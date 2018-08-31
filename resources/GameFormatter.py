class Formatter:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDCOLOR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    LIST_SEPARATOR = ", "
    SPACE = " "
    
    def __init__(self):
        pass
        
    def print_text(self, text):
        print(text)
        
    def print_error(self, text):
        # return self.FAIL + text + self.ENDCOLOR
        print("ERROR: " + text)
        
    def print_warning(self, text):
        # return self.WARNING + text + self.ENDCOLOR
        print("WARNING: " + text)
    
    def print_invalid_command(self, text=None):
        if text is None:
            print("Invalid command")
        else:
            print("Invalid command: " + text)
            
    def print_new_room(self, environment):
        print_items = True if environment.items else False

        print("\n")
        print(environment.name)
        print("====================================")
        print(environment.description)
        if print_items:
            item_text = "The room contains " + self.make_item_list([item.reference_description for item in environment.items])
            print(item_text)

    def print_room_description(self, environment):
        print_items = True if environment.items else False

        print("\n")
        print(environment.description)
        if print_items:
            item_text = "The room contains " + self.make_item_list([item.reference_description for item in environment.items])
            print(item_text)

    def print_item_taken(self, item):
        print("\n")
        print("Took " + item.name + ".")

    def print_item_dropped(self, item):
        print("\n")
        print("Dropped " + item.name + ".")

    def print_item_not_found(self, item_name):
        print("\n")
        print("There's no " + item_name + " around here...")

    def print_item_not_found_in_inventory(self, item_name):
        print("\n")
        print("There's no " + item_name + " in your inventory...")

    def make_item_list(self, item_list):
        # TODO: Add underline formatting to words in item.reference_description that are usable to reference the item
        # TODO: Alternatively, DON'T add an underline for true-to-form 80's difficulty
        if len(item_list) > 1:
            item_list[-1] = "and " + item_list[-1]

        item_list[-1] = item_list[-1] + "."

        if len(item_list) == 2:
            return self.SPACE.join(item_list)

        return self.LIST_SEPARATOR.join(item_list)
