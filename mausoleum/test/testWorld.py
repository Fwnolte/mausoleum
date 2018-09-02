import unittest

from mausoleum.game.World import World
from mausoleum.game.Environment import Environment
from mausoleum.game.Item import Item


class VARS:
    ROOM1 = Environment("Room 1",
                        "Room 1 description",
                        "Room 1 reference description",
                        "room1_type",
                        [], [], [])
    ROOM2 = Environment("Room 2",
                        "Room 2 description",
                        "Room 2 reference description",
                        "room2_type",
                        [], [], [])

    # Set up room linkages
    ROOM1.add_travel_destination("north", ROOM2)
    ROOM2.add_travel_destination("south", ROOM1)

    SWORD = Item("sword", "sword description", "a sword")
    ROPE = Item("rope", "rope description", "a length of rope")
    LEVER = Item("lever", "lever description", "a broken lever handle")


class WorldTest(unittest.TestCase):
    """
        This class tests the functional/utility methods that are part of the World object
    """

    def setUp(self):
        self.world = World([VARS.ROOM1, VARS.ROOM2], VARS.ROOM1, [VARS.SWORD, VARS.ROPE, VARS.LEVER])

    """
    Tests for method "get_current_environment_description()"
    """
    def testGetCurrentEnvironmentDescription(self):
        returned = self.world.get_current_environment_description()
        self.assertEqual(returned, VARS.ROOM1.description)

    """
    Tests the "travel(...)" method
    """
    def testTravelInValidDirectionSuccessfullyTravels(self):
        returned = self.world.travel("north")
        self.assertEqual(self.world.current_environment, VARS.ROOM2)
        self.assertEqual(returned, VARS.ROOM2)

    def testTravelInInvalidDirectionDoesNothing(self):
        current_environment = self.world.current_environment

        returned = self.world.travel("everywhere")

        # Assert that the current_environment did not change
        self.assertEqual(current_environment, self.world.current_environment)
        self.assertIsNone(returned)

    """
    Tests the "get_inventory()" method
    """
    def testGetInventory(self):
        inventory = self.world.get_inventory()

        expected = [VARS.SWORD.reference_description, VARS.ROPE.reference_description, VARS.LEVER.reference_description]
        self.assertListEqual(inventory, expected)

    def testGetEmptyInventory(self):
        self.world.inventory = []
        inventory = self.world.get_inventory()
        self.assertListEqual(inventory, [])

    """
    Tests the "add_to_inventory(...)" method
    """
    def testAddItemToInventoryAddsItem(self):
        self.world.inventory = [VARS.SWORD, VARS.ROPE]

        returned = self.world.add_to_inventory(VARS.LEVER)

        self.assertListEqual(self.world.inventory, [VARS.SWORD, VARS.ROPE, VARS.LEVER])
        self.assertTrue(returned)

    def testAddNoneToInventoryDoesNothing(self):
        expected = self.world.inventory

        returned = self.world.add_to_inventory(None)

        self.assertListEqual(self.world.inventory, expected)
        self.assertNotIn(None, self.world.inventory)  # Appending "None" to a list does weird things
        self.assertFalse(returned)

    def testAddNonItemToInventoryDoesNothing(self):
        expected = self.world.inventory

        returned = self.world.add_to_inventory("not an item")

        self.assertListEqual(self.world.inventory, expected)
        self.assertNotIn(None, self.world.inventory)
        self.assertFalse(returned)

    """
    Tests the "remove_from_inventory(...)" method
    """
    def testRemoveItemFromInventoryRemovesItem(self):
        returned = self.world.remove_from_inventory(VARS.SWORD)

        expected = [VARS.ROPE, VARS.LEVER]
        self.assertTrue(returned)
        self.assertListEqual(self.world.inventory, expected)  # Test that the item was actually removed

    def testRemoveNonExistentItemFromInventoryDoesNothing(self):
        expected = self.world.inventory

        returned = self.world.remove_from_inventory(Item("new", "new", "new"))

        self.assertEqual(expected, self.world.inventory)  # Test that no other item was removed
        self.assertFalse(returned)

    def testRemoveNoneFromInventoryDoesNothing(self):
        expected = self.world.inventory

        returned = self.world.remove_from_inventory(None)

        self.assertEqual(expected, self.world.inventory)  # Test that no other item was removed
        self.assertFalse(returned)

    def testRemoveNonItemFromInventoryDoesNothing(self):
        expected = self.world.inventory

        returned = self.world.remove_from_inventory("notAnItem")

        self.assertEqual(expected, self.world.inventory)
        self.assertFalse(returned)

    """
    Tests the "find_in_inventory(...)" method
    """
    def testFindItemInInventoryReturnsItem(self):
        returned = self.world.find_in_inventory("sword")

        self.assertEqual(returned, VARS.SWORD)

    def testFindNonexistentItemInInventoryReturnsNone(self):
        returned = self.world.find_in_inventory("nonexistent")
        self.assertIsNone(returned)

    def testFindItemInEmptyInventoryReturnsNone(self):
        self.world.inventory = []

        returned = self.world.find_in_inventory("sword")
        self.assertIsNone(returned)

    def testFindByNonStringObjectInInventoryReturnsNone(self):
        returned = self.world.find_in_inventory([])
        self.assertIsNone(returned)

    def testFindNoneInInventoryReturnsNone(self):
        returned = self.world.find_in_inventory(None)
        self.assertIsNone(returned)


class WorldTestInit(unittest.TestCase):
    """
    This class tests the different initialization states of the World object
    """

    def testInit(self):
        self.world = World([VARS.ROOM1, VARS.ROOM2], VARS.ROOM1, [VARS.SWORD, VARS.ROPE, VARS.LEVER])

        self.assertListEqual(self.world.environments, [VARS.ROOM1, VARS.ROOM2])
        self.assertEqual(self.world.current_environment, VARS.ROOM1)
        self.assertListEqual(self.world.inventory, [VARS.SWORD, VARS.ROPE, VARS.LEVER])

    def testInventoryBecomesEmptyListWhenInitializingImproperly(self):
        self.world = World([VARS.ROOM1], VARS.ROOM1, "This should be a list")
        self.assertListEqual(self.world.inventory, [])

    def testGameExitsIfNoStartingRoom(self):
        with self.assertRaises(SystemExit):
            self.world = World([VARS.ROOM1], None, [])


if __name__ == "__main__":
    unittest.main()
