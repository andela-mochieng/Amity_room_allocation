class Room(object):
    pass


class Office(Room):
    """office model"""
    room_type = 'OFFICE'
    capacity = 6


class Living_space(Room):
    room_type = 'LIVING_SPACE'
    capacity = 4
