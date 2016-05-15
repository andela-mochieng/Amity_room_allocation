
class Room(object):
    """Room is the parent and Office and Living_space inherit from it"""

    def __init__(self):
        """both Office and Living_space have access to name"""
        pass


class Office(Room):
    """office model has capacity of 6"""
    room_type = 'O'
    capacity = 6


class Living_space(Room):
    """Living_space model with a capacity of 4 """
    room_type = 'L'
    capacity = 4
