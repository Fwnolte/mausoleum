from game.Describable import Describable


class Item(Describable):
    def __init__(self, name, description, reference_description):
        super().__init__(name, description, reference_description)
