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
        assert self.describable.name == self.NAME, '"Name" not initialized properly'
        assert self.describable.description == self.DESCRIPTION, '"Description" not initialized properly'
        assert self.describable.reference_description == self.REFERENCE_DESCRIPTION, '"Reference Description" not initialized properly'


if __name__ == "__main__":
    unittest.main()
