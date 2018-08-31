from resources.GameFormatter import Formatter

from game.Command import Command
from game.World import World
from game.Environment import Environment
from game.Item import Item

def start_game():
    #Initialize world
    sword = Item("Sword", "A plain-looking sword with a leather-wrapped hilt", "a sword")
    room1 = Environment("Stone Room", "A small room constructed of ancient stone and mortar. Moss grows in the cracks of the stone. It smells damp.", "", [sword], [], [])
    room2 = Environment("Storage Room", "A small abandoned storage room. Several crates and barrels lie forgotten and rotting.", [], [], [], [])
    world = World([room1, room2], room1, [])
    
    #Set up room linkages
    room1.add_travel_destination("north", room2)
    room2.add_travel_destination("south", room1)
    
    #Set up objects
    formatter = Formatter()
    command_module = Command("./game/commands.txt", formatter, world)
    
    while(True):
        command = command_module.get_command()
        
        if command is None:
            continue; #Already printed a warning. Try to grab the next command
        
        command_performed = command_module.perform_command(command)
        if command_performed:
            print("DEBUG: Successfully performed command")

start_game()
