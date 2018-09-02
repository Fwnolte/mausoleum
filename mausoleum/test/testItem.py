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
        self.assertEqual(self.item.name, self.NAME)
        self.assertEqual(self.item.description, self.DESCRIPTION)
        self.assertEqual(self.item.reference_description, self.REFERENCE_DESCRIPTION)


if __name__ == "__main__":
    unittest.main()
