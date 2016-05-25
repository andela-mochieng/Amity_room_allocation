import ipdb
class Room(object):
    """Room is the parent and Office and Living_space inherit from it"""
    members = []

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "{}".format(self.name)

    def add_member(self, person):
        if len(self.members) < self.capacity:
            print self.capacity
            self.members.append(person)
        return self.is_filled()

    def is_filled(self):
        return len(self.members) >= self.capacity


class Office(Room):
    """office model has capacity of 6"""
    capacity = 6


class LivingSpace(Room):
    """Living_space model with a capacity of 4 """
    capacity = 4
