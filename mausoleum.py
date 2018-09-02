from mausoleum.game.GameFormatter import GameFormatter

from mausoleum.game.Command import Command
from mausoleum.game.World import World
from mausoleum.game.Environment import Environment
from mausoleum.game.Item import Item


def start_game():
    # Initialize world
    sword = Item("sword", "A plain-looking sword with a leather-wrapped hilt.", "a sword")
    rope = Item("rope", "A dirty, fraying rope, about 15 feet long.", "a length of rope")
    lever = Item("lever", "A lever handle made of smooth round wood. One end is broken.", "a broken lever handle")
    room1 = Environment("Stone Room", "A small room constructed of ancient stone and mortar. Moss grows in the cracks of the stone. It smells damp.", "", [sword, rope, lever], [], [])
    room2 = Environment("Storage Room", "An abandoned storage room. Several crates and barrels lie forgotten and rotting.", [], [], [], [])
    world = World([room1, room2], room1, [])
    
    # Set up room linkages
    room1.add_travel_destination("north", room2)
    room2.add_travel_destination("south", room1)
    
    # Set up objects
    formatter = GameFormatter()
    command_module = Command("./mausoleum/game/commands.txt", formatter, world)
    command_module.load_valid_command_list()
    
    while True:
        command = command_module.get_command()
        
        if command is None:
            continue  # Already printed a warning. Try to grab the next command
        
        command_performed = command_module.perform_command(command)
        if not command_performed:
            print("DEBUG: Failed to perform command")


start_game()
