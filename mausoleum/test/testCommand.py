import unittest
from unittest import SkipTest
from unittest.mock import Mock
from unittest.mock import patch
from unittest.mock import mock_open

from mausoleum.game.Command import Command


class TestCommand(unittest.TestCase):
    FILE_PATH = "./path/to/file/commands.txt"
    FORMATTER = None
    CURRENT_ENVIRONMENT = None
    WORLD = None

    def setUp(self):
        self.FORMATTER = Mock()
        self.CURRENT_ENVIRONMENT = Mock()
        self.WORLD = Mock(current_environment=self.CURRENT_ENVIRONMENT)
        self.command = Command(self.FILE_PATH, self.FORMATTER, self.WORLD)

    def skip_if_not_base_class(self):
        if self.__class__.__name__ != "TestCommand":
            raise SkipTest("Don't repeat tests!")

    """
    Test for the proper initialization of the Command object
    """
    def testInit(self):
        # Due to inheritance, we don't want to run the base class' test if we're testing a child object
        if self.__class__.__name__ != "TestCommand":
            raise SkipTest("Don't repeat tests!")

        self.assertEqual(self.command.formatter, self.FORMATTER)
        self.assertEqual(self.command.file_path, self.FILE_PATH)
        self.assertEqual(self.command.world, self.WORLD)


class TestCommandStock(TestCommand):

    def MOCK_OPEN(*args, **kargs):
        """
        Used to mock the open() function for iterative use.
        https://stackoverflow.com/questions/24779893/customizing-unittest-mock-mock-open-for-iteration
        """
        f_open = mock_open(*args, **kargs)
        f_open.return_value.__iter__ = lambda self: iter(self.readline, '')
        return f_open

    def setUp(self):
        super().setUp()

    """
    Tests for the "load_valid_command_list()" method
    """
    @patch('builtins.open', new_callable=MOCK_OPEN, read_data="valid\n")
    @patch('os.path.isfile', return_value=True)
    def testLoadValidCommandListLoadsSuccessfully(self, is_file_call, open_call):
        self.command.load_valid_command_list()

        is_file_call.assert_called_with(self.FILE_PATH)
        open_call.assert_called_with(self.FILE_PATH)

        self.assertListEqual(self.command.valid_command_list, ["valid"])

    @patch('builtins.exit')
    @patch('os.path.isfile', return_value=False)
    def testLoadValidCommandListWithNonExistentPathExits(self, is_file_call, exit_call):
        self.command.load_valid_command_list()

        is_file_call.assert_called_with(self.FILE_PATH)
        exit_call.assert_called()

    """
    Tests for the "get_command()" method
    """
    @patch('builtins.input', return_value="command string")
    def testGetCommandWorksOnLegalCommandString(self, input_call):
        self.command.parse_command = Mock(return_value=["command", "string"])
        self.command.is_legal_command = Mock(return_value=True)

        returned = self.command.get_command()

        input_call.assert_called()
        self.command.parse_command.assert_called_with("command string")
        self.command.is_legal_command.assert_called_with(["command", "string"])
        self.assertListEqual(returned, ["command", "string"])

    @patch('builtins.input', return_value="command string")
    def testGetCommandReturnsNoneOnIllegalCommand(self, input_call):
        self.command.parse_command = Mock(return_value=["command", "string"])
        self.command.is_legal_command = Mock(return_value=False)

        returned = self.command.get_command()

        input_call.assert_called()
        self.command.parse_command.assert_called_with("command string")
        self.command.is_legal_command.assert_called_with(["command", "string"])
        self.assertIsNone(returned)

    """
    Tests for the "parse_command(...)" method
    """
    def testParseCommandReturnsCommandString(self):
        returned = self.command.parse_command("command string")
        self.assertListEqual(returned, ["command", "string"])

    def testParseCommandRemovesFillerWords(self):
        returned = self.command.parse_command("the command at string and filler words")

        # Assert that none of the filler words show up in the returned command string
        for word in self.command.FILLER_WORDS:
            self.assertNotIn(word, returned)

    def testParseCommandConvertsPickUpToTake(self):
        returned = self.command.parse_command("pick up thing")
        self.assertListEqual(returned, ["take", "thing"])

    """
    Test for the "perform_command(["quit"])" call.
    Other perform_command(...) tests are located in separate classes, below.
    """
    def testPerformCommandQuit(self):
        mock = Mock()
        self.command.quit = mock

        self.command.perform_command(["quit"])

        mock.assert_called()


class TestCommandLegality(TestCommand):
    """
    Tests for the "is_legal_command(...)" method
    """

    def setUp(self):
        super().setUp()
        self.command.valid_command_list = ["valid"]

    def testIsLegalCommandWithLegalCommand(self):
        returned = self.command.is_legal_command(["valid", "command"])
        self.assertTrue(returned)

    def testIsLegalCommandWithIllegalCommand(self):
        returned = self.command.is_legal_command(["illegal", "command"])
        # Verify our print method was called correctly
        self.FORMATTER.print_invalid_command.assert_called_with()

    def testIsLegalCommandWithEmptyCommand(self):
        returned = self.command.is_legal_command([""])

        # Verify our print method was called correctly
        self.FORMATTER.print_invalid_command.assert_called_with("Commands cannot be empty.")
        self.assertFalse(returned)

    def testIsLegalCommandWithNonList(self):
        returned = self.command.is_legal_command("not a list")
        self.assertFalse(returned)


class TestCommandPerformerLook(TestCommand):
    """
    Tests for the "look" command portion of the perform_command method.
    """
    def setUp(self):
        super().setUp()

        # Mock variable usable in this test class for testing successes.
        self.mock = Mock(return_value=True)
        self.command.describe = self.mock

    def testPerformCommandLookSucceeds(self):
        returned = self.command.perform_command(["look"])
        self.mock.assert_called_with()
        self.assertTrue(returned)

    def testPerformCommandLookAtItemSucceeds(self):
        returned = self.command.perform_command(["look", "item"])
        self.mock.assert_called_with("item")
        self.assertTrue(returned)

    def testPerformCommandDescribeMoreThanTwoThingsFails(self):
        returned = self.command.perform_command(["look", "item", "item2"])

        self.FORMATTER.print_warning.assert_called_with("You can't look at two things at once!")
        self.assertFalse(returned)


class TestCommandPerformerTake(TestCommand):
    """
    Tests for the "take" command portion of the perform_command method.
    """
    def setUp(self):
        super().setUp()

        # Mock variable usable in this test class for testing successes.
        self.mock = Mock(return_value=True)
        self.command.take = self.mock

    def testPerformCommandTakeSucceeds(self):
        returned = self.command.perform_command(["take", "item"])

        self.mock.assert_called_with("item")
        self.assertTrue(returned)

    def testPerformCommandTakeWithNoTargetFails(self):
        returned = self.command.perform_command(["take"])

        self.FORMATTER.print_warning.assert_called_with("You need to name the object you want to take.")
        self.assertFalse(returned)

    def testPerformCommandTakeWithMoreThanTwoThingsFails(self):
        returned = self.command.perform_command(["take", "item", "item2"])

        self.FORMATTER.print_warning.assert_called_with("You can't grab two things at once!")
        self.assertFalse(returned)


class TestCommandPerformerDrop(TestCommand):
    """
    Tests for the "drop" command portion of the perform_command method.
    """
    def setUp(self):
        super().setUp()

        # Mock variable usable in this test class for testing successes.
        self.mock = Mock(return_value=True)
        self.command.drop = self.mock

    def testPerformCommandDropSucceeds(self):
        returned = self.command.perform_command(["drop", "item"])

        self.mock.assert_called_with("item")
        self.assertTrue(returned)

    def testPerformCommandDropWithNoTargetFails(self):
        returned = self.command.perform_command(["drop"])

        self.FORMATTER.print_warning.assert_called_with("You need to name the object you want to drop.")
        self.assertFalse(returned)

    def testPerformCommandDropWithMoreThanTwoThingsFails(self):
        returned = self.command.perform_command(["drop", "item", "item2"])

        self.FORMATTER.print_warning.assert_called_with("You can't drop two things at once!")
        self.assertFalse(returned)


class TestCommandPerformerGo(TestCommand):
    """
    Tests for the "go" command portion of the perform_command method.
    """
    def setUp(self):
        super().setUp()

        # Mock variable usable in this test class for testing successes.
        self.mock = Mock(return_value=True)
        self.command.go = self.mock

    def testPerformCommandGoSucceeds(self):
        returned = self.command.perform_command(["go", "direction"])

        self.mock.assert_called_with("direction")
        self.assertTrue(returned)

    def testPerformCommandGoWithNoTargetFails(self):
        returned = self.command.perform_command(["go"])

        self.FORMATTER.print_warning.assert_called_with("You need to specify somewhere to go.")
        self.assertFalse(returned)

    def testPerformCommandGoWithMoreThanTwoThingsFails(self):
        returned = self.command.perform_command(["go", "direction", "direction2"])

        self.FORMATTER.print_warning.assert_called_with("You can't go two places at once!")
        self.assertFalse(returned)


class TestCommandDescribe(TestCommand):
    """
    Tests for the "describe(...)" method
    """
    def testDescribeWithNoArgumentsDescribesRoom(self):
        returned = self.command.describe()
        self.FORMATTER.print_room_description.assert_called_with(self.CURRENT_ENVIRONMENT)
        self.assertTrue(returned)

    def testDescribeWithNoneArgumentDescribesRoom(self):
        returned = self.command.describe(None)
        self.FORMATTER.print_room_description.assert_called_with(self.CURRENT_ENVIRONMENT)
        self.assertTrue(returned)

    def testDescribeWithRoomArgumentDescribesRoom(self):
        returned = self.command.describe("room")
        self.FORMATTER.print_room_description.assert_called_with(self.CURRENT_ENVIRONMENT)
        self.assertTrue(returned)

    def testDescribeWithInventoryArgumentDescribesEmptyInventory(self):
        self.WORLD.get_inventory = Mock(return_value=[])

        returned = self.command.describe("inventory")

        self.FORMATTER.print_text.assert_called_with("There's nothing in your inventory right now.")
        self.assertTrue(returned)

    def testDescribeWithInventoryArgumentDescribesPopulatedInventory(self):
        self.WORLD.get_inventory = Mock(return_value=["an item"])
        self.FORMATTER.make_item_list = Mock(return_value="an item.")

        returned = self.command.describe("inventory")

        self.FORMATTER.make_item_list.assert_called_with(["an item"])
        self.FORMATTER.print_text.assert_called_with("Your inventory contains an item.")
        self.assertTrue(returned)

    def testDescribeWithItemArgumentFindsItemInRoom(self):
        item = Mock(description="An item.")
        self.CURRENT_ENVIRONMENT.find = Mock(return_value=item)

        returned = self.command.describe("item")

        self.FORMATTER.print_text.assert_called_with("An item.")
        self.assertTrue(returned)

    def testDescribeWithItemArgumentFindsItemInInventory(self):
        item = Mock(description="An item.")
        self.CURRENT_ENVIRONMENT.find = Mock(return_value=None)
        self.WORLD.find_in_inventory = Mock(return_value=item)

        returned = self.command.describe("item")

        self.FORMATTER.print_text.assert_called_with("An item. This item is in your inventory.")
        self.assertTrue(returned)

    def testDescribeWithItemArgumentFindsItemInRoomFirst(self):
        item = Mock(description="An item.")
        self.CURRENT_ENVIRONMENT.find = Mock(return_value=item)
        self.WORLD.find_in_inventory = Mock(return_value=item)

        returned = self.command.describe("item")

        self.FORMATTER.print_text.assert_called_with("An item.")
        self.assertTrue(returned)

    def testDescribeWithItemArgumentDoesNotFindItem(self):
        self.CURRENT_ENVIRONMENT.find = Mock(return_value=None)
        self.WORLD.find_in_inventory = Mock(return_value=None)

        returned = self.command.describe("item")

        self.FORMATTER.print_item_not_found.assert_called_with("item")
        self.assertFalse(returned)

    def testDescribeWithIllegalArgumentFails(self):
        returned = self.command.describe(1)
        self.assertFalse(returned)


class TestCommandTake(TestCommand):
    """
    Tests for the "take(...)" method
    """

    def testTakeWithItemArgumentCannotFindItem(self):
        self.CURRENT_ENVIRONMENT.find = Mock(return_value=None)

        returned = self.command.take("item")

        self.CURRENT_ENVIRONMENT.find.assert_called_with("item")
        self.FORMATTER.print_item_not_found.assert_called_with("item")
        self.assertFalse(returned)

    def testTakeWithItemArgumentSucceeds(self):
        item = Mock()
        self.CURRENT_ENVIRONMENT.find = Mock(return_value=item)

        returned = self.command.take("item")

        self.CURRENT_ENVIRONMENT.find.assert_called_with("item")
        self.CURRENT_ENVIRONMENT.remove_item.assert_called_with(item)
        self.WORLD.add_to_inventory.assert_called_with(item)
        self.FORMATTER.print_item_taken.assert_called_with(item)
        self.assertTrue(returned)

    def testTakeWithIllegalArgumentFails(self):
        returned = self.command.take(1)
        self.assertFalse(returned)


class TestCommandDrop(TestCommand):
    """
    Tests for the "drop(...)" method
    """

    def testDropWithItemArgumentCannotFindItem(self):
        self.WORLD.find_in_inventory = Mock(return_value=None)

        returned = self.command.drop("item")

        self.WORLD.find_in_inventory.assert_called_with("item")
        self.FORMATTER.print_item_not_found_in_inventory.assert_called_with("item")
        self.assertFalse(returned)

    def testDropWithItemArgumentSucceeds(self):
        item = Mock()
        self.WORLD.find_in_inventory = Mock(return_value=item)

        returned = self.command.drop("item")

        self.WORLD.remove_from_inventory.assert_called_with(item)
        self.CURRENT_ENVIRONMENT.add_item.assert_called_with(item)
        self.FORMATTER.print_item_dropped.assert_called_with(item)
        self.assertTrue(returned)

    def testDropWithIllegalArgumentFails(self):
        returned = self.command.drop(1)
        self.assertFalse(returned)


class TestCommandGo(TestCommand):
    """
    Tests for the "go(...)" method
    """

    def setUp(self):
        super().setUp()
        self.DESTINATION = Mock()
        self.CURRENT_ENVIRONMENT.travel_destinations = {"direction": self.DESTINATION}

    def testGoWithDirectionArgumentSucceeds(self):
        returned = self.command.go("direction")

        self.command.world.travel.assert_called_with("direction")

        # TODO: Currently ignoring this line due to no clear way of simulating the state change of the
        # TODO: World's "current_environment" object
        # self.FORMATTER.print_new_room.assert_called_with(self.DESTINATION)
        self.assertTrue(returned)

    def testGoWithNonExistentDirectionArgumentFails(self):
        returned = self.command.go("invalidDirection")

        self.FORMATTER.print_warning.assert_called_with("\"invalidDirection\" is not a valid direction!")
        self.WORLD.travel.assert_not_called()
        self.assertFalse(returned)

    def testGoWithNoneArgumentFails(self):
        returned = self.command.go(None)
        self.WORLD.travel.assert_not_called()
        self.assertFalse(returned)

    def testGoWithIllegalArgumentFails(self):
        returned = self.command.go(1)
        self.WORLD.travel.assert_not_called()
        self.assertFalse(returned)


if __name__ == "__main__":
    unittest.main()
