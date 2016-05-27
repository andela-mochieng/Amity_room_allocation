import ipdb


class Room(object):
    """Room is the parent and Office and Living_space inherit from it"""
    members = []

    def __init__(self, name):
        self.name = name
        self.filled = False

    def room_name(self):
        return self.name

    def add_member(self, person):
        self.members.append(person)

    def is_filled(self, size):
        self.filled = size >= self.capacity
        return self.filled

    def __repr__(self):
        return "{}".format(self.is_filled())


class Office(Room):
    """office model has capacity of 6"""
    capacity = 6


class LivingSpace(Room):
    """Living_space model with a capacity of 4 """
    capacity = 4
