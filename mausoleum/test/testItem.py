import unittest

from mausoleum.game.Item import Item


class ItemTest(unittest.TestCase):
    NAME = "Name"
    DESCRIPTION = "this is a description"
    REFERENCE_DESCRIPTION = "this is a reference description"

    def setUp(self):
        self.item = Item(self.NAME, self.DESCRIPTION, self.REFERENCE_DESCRIPTION)

    """
    Test that the Item gets initialized properly
    """
    def testInit(self):
        assert self.item.name == self.NAME, '"Name" not initialized properly'
        assert self.item.description == self.DESCRIPTION, '"Description" not initialized properly'
        assert self.item.reference_description == self.REFERENCE_DESCRIPTION, '"Reference Description" not initialized properly'


if __name__ == "__main__":
    unittest.main()
