import unittest

from mausoleum.game.Describable import Describable


class EnvironmentTest(unittest.TestCase):
    NAME = "Name"
    DESCRIPTION = "this is a description"
    REFERENCE_DESCRIPTION = "this is a reference description"

    def setUp(self):
        self.describable = Describable(self.NAME, self.DESCRIPTION, self.REFERENCE_DESCRIPTION)

    """
    Test that the Describable gets initialized properly
    """
    def testInit(self):
        self.assertEqual(self.describable.name, self.NAME)
        self.assertEqual(self.describable.description, self.DESCRIPTION)
        self.assertEqual(self.describable.reference_description, self.REFERENCE_DESCRIPTION)


if __name__ == "__main__":
    unittest.main()
