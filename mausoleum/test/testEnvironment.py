import unittest
import copy

from mausoleum.game.Environment import Environment
from mausoleum.game.Item import Item


class EnvironmentTest(unittest.TestCase):
    NAME = "Name"
    DESCRIPTION = "this is a description"
    REFERENCE_DESCRIPTION = "this is a reference description"
    ITEM = Item(name=NAME, description=DESCRIPTION, reference_description=REFERENCE_DESCRIPTION)
    CHARACTERS = []  # TODO: Add this
    INTERACTIBLES = []

    def setUp(self):
        self.environment = Environment(self.NAME,
                                       self.DESCRIPTION,
                                       self.REFERENCE_DESCRIPTION,
                                       [],
                                       [],
                                       [])
    """
    Test that the Environment gets initialized properly
    """
    def testInit(self):
        assert self.environment.name == self.NAME, '"Name" not initialized properly'
        assert self.environment.description == self.DESCRIPTION, '"Description" not initialized properly'
        assert self.environment.reference_description == self.REFERENCE_DESCRIPTION, '"Reference Description" not initialized properly'
        assert self.environment.items == [], '"Items" not initialized properly'
        assert self.environment.characters == [], '"Characters" not initialized properly'
        assert self.environment.interactibles == [], '"Travel Destinations not initialized properly'

    """
    Tests for method "add_travel_destination(...)"
    """
    def testAddTravelDestinationToEmptyDestinations(self):
        destination = copy.deepcopy(self.environment)
        self.environment.add_travel_destination("north", destination)

        self.assertDictEqual(self.environment.travel_destinations, {"north": destination})

    def testAddTravelDestinationAddsToExistingDestinations(self):
        destination = copy.deepcopy(self.environment)
        destination2 = copy.deepcopy(self.environment)
        self.environment.travel_destinations = {"north": destination}

        self.environment.add_travel_destination("south", destination2)

        self.assertDictEqual(self.environment.travel_destinations, {"north": destination, "south": destination2})

    def testAddTravelDestinationOverwritesProperly(self):
        destination = copy.deepcopy(self.environment)
        destination2 = copy.deepcopy(self.environment)
        self.environment.travel_destinations = {"north": destination}

        returned = self.environment.add_travel_destination("north", destination2)

        self.assertDictEqual(self.environment.travel_destinations, {"north": destination2})
        self.assertEqual(returned, destination)

    """
    Tests for method "find(...)"
    """
    def testFindFailsForEmptyItemList(self):
        item = self.ITEM

        self.assertIsNone(self.environment.find(item.name))

    def testFindItemInSingletonList(self):
        item = self.ITEM
        self.environment.items = [item]

        self.assertEqual(self.environment.find(item.name), item)

    def testFindItemInMultipleItemList(self):
        item = self.ITEM
        new_item = Item(name="Item2", description="test", reference_description="test")

        self.environment.items = [item, new_item, copy.deepcopy(new_item)]

        self.assertEqual(self.environment.find(item.name), item)

    def testFindItemAtEndOfMultipleItemList(self):
        item = self.ITEM
        new_item = Item(name="Item2", description="test", reference_description="test")

        self.environment.items = [new_item, copy.deepcopy(new_item), item]

        self.assertEqual(self.environment.find(item.name), item)

    """
    Tests for method "add_item(...)"
    """
    def testAddItem(self):
        self.environment.add_item(self.ITEM)
        self.assertListEqual(self.environment.items, [self.ITEM])

    """
    Tests for method "remove_item(...)"
    """
    def testRemoveItem(self):
        self.environment.items = [self.ITEM]
        self.environment.remove_item(self.ITEM)
        self.assertListEqual(self.environment.items, [])

    def testRemoveItemFromEmptyListFails(self):
        self.assertEqual(self.environment.remove_item(self.ITEM), False)

    # TODO: Add these methods in once their constructs are implemented
    # def testFindCharacter():
    #   pass
    #
    # def testFindInteractible():
    #   pass


if __name__ == "__main__":
    unittest.main()
