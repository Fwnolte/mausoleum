import copy
import unittest

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
        self.assertEqual(self.environment.name, self.NAME)
        self.assertEqual(self.environment.description, self.DESCRIPTION)
        self.assertEqual(self.environment.reference_description, self.REFERENCE_DESCRIPTION)
        self.assertEqual(self.environment.items, [])
        self.assertEqual(self.environment.characters, [])
        self.assertEqual(self.environment.interactibles, [])

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
    def testFindItemInEmptyListReturnsNone(self):
        item = self.ITEM

        self.assertIsNone(self.environment.find(item.name))

    def testFindItemInSingletonListReturnsItem(self):
        item = self.ITEM
        self.environment.items = [item]

        self.assertEqual(self.environment.find(item.name), item)

    def testFindItemInMultipleItemListReturnsItem(self):
        item = self.ITEM
        new_item = Item(name="Item2", description="test", reference_description="test")

        self.environment.items = [item, new_item, copy.deepcopy(new_item)]

        self.assertEqual(self.environment.find(item.name), item)

    def testFindItemAtEndOfMultipleItemListReturnsItem(self):
        item = self.ITEM
        new_item = Item(name="Item2", description="test", reference_description="test")

        self.environment.items = [new_item, copy.deepcopy(new_item), item]

        self.assertEqual(self.environment.find(item.name), item)

    def testFindNonExistentItemReturnsNone(self):
        item = self.ITEM
        self.environment.items = [item]

        returned = self.environment.find("nameNotInList")

        self.assertIsNone(returned)

    def testFindNoneReturnsNone(self):
        self.environment.items = [self.ITEM]

        returned = self.environment.find(None)

        self.assertIsNone(returned)

    """
    Tests for method "add_item(...)"
    """
    def testAddItemSuccessfullyAddsItem(self):
        returned = self.environment.add_item(self.ITEM)
        self.assertListEqual(self.environment.items, [self.ITEM])
        self.assertTrue(returned)

    def testAddNonItemDoesNothing(self):
        self.environment.items = [self.ITEM]
        returned = self.environment.add_item("notAnItem")

        self.assertListEqual([self.ITEM], self.environment.items)
        self.assertNotIn(None, self.environment.items)  # Additional check because adding None to lists is weird
        self.assertFalse(returned)

    def testAddNoneDoesNothing(self):
        self.environment.items = [self.ITEM]
        returned = self.environment.add_item(None)

        self.assertListEqual([self.ITEM], self.environment.items)
        self.assertNotIn(None, self.environment.items)  # Additional check because adding None to lists is weird
        self.assertFalse(returned)


    """
    Tests for method "remove_item(...)"
    """
    def testRemoveItem(self):
        self.environment.items = [self.ITEM]
        returned = self.environment.remove_item(self.ITEM)

        self.assertTrue(returned)
        self.assertListEqual(self.environment.items, [])

    def testRemoveItemFromEmptyListDoesNothing(self):
        returned = self.environment.remove_item(self.ITEM)

        self.assertFalse(returned)
        self.assertListEqual(self.environment.items, [])

    def testRemoveNonExistentItemDoesNothing(self):
        self.environment.items = [self.ITEM]
        item = copy.deepcopy(self.ITEM)
        item.name = "Different Name"

        returned = self.environment.remove_item(item)

        self.assertFalse(returned)
        self.assertListEqual(self.environment.items, [self.ITEM])

    def testRemoveNoneDoesNothing(self):
        self.environment.items = [self.ITEM]

        returned = self.environment.remove_item(None)

        self.assertFalse(returned)
        self.assertListEqual(self.environment.items, [self.ITEM])

    def testRemoveNonItemDoesNothing(self):
        self.environment.items = [self.ITEM]

        returned = self.environment.remove_item("notAnItem")

        self.assertFalse(returned)
        self.assertListEqual(self.environment.items, [self.ITEM])


    # TODO: Add these methods in once their constructs are implemented
    # def testFindCharacter():
    #   pass
    #
    # def testFindInteractible():
    #   pass


if __name__ == "__main__":
    unittest.main()
