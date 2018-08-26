class Formatter:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDCOLOR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    VOWELS = ["a", "e", "i", "o", "u"]
    LIST_SEPARATOR = ", "
    
    def __init__(self):
        pass
        
    def print_text(self, text):
        print(text)
        
    def print_error(self, text):
        #return self.FAIL + text + self.ENDCOLOR
        print("ERROR: " + text)
        
    def print_warning(self, text):
        #return self.WARNING + text + self.ENDCOLOR
        print("WARNING: " + text)
    
    def print_invalid_command(self, text=None):
        if text is None:
            print("Invalid command")
        else:
            print("Invalid command: " + text)
            
    def print_new_room(self, environment):
        print("\n")
        print(environment.name)
        print("====================================")
        print(environment.description)
        #TODO: Add "There is <items>" preamble
        
    def make_list(self, list):
        list = [add_preface(item) for item in list]
        
        if len(list) > 1:
            list[-1] = "and " + list[-1]
            
        return LIST_SEPARATOR.join(list)
        
    def add_preface(self, thing):
        #Check if the first character of the thing is a vowel.
        if thing[0].lower() in VOWELS:
            return ("an " + thing)
        else:
            return ("a" + thing)