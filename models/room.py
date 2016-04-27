class Room(object):

    def __init__(self, name):
        self.name = name


class Office(Room):
    """office model"""
    room_type = 'O'
    capacity = 6
    available = ['0', '0', '0', '0', '0', '0']

    def __repr__(self):

        return '{"name": \"%s\", "room_type": \"%s\","capacity" :%d, \
        "available": %s}' % (self.name, self.room_type, self.capacity, self.available)


class Living_space(Room):
    room_type = 'L'
    capacity = 4
    available = ['0', '0', '0', '0']

    def __repr__(self):

        return '{"name": \"%s\", "room_type": \"%s\","capacity" :%d, \
        "available": %s}' % (self.name, self.room_type, self.capacity, self.available)
