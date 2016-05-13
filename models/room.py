
class Room(object):
    """Room is the parent and Office and Living_space inherit from it"""

    def __init__(self):
        """both Office and Living_space have access to name"""
        pass



class Office(Room):
    """office model has capacity of 6"""
    room_type = 'O'
    capacity = 6


    def __repr__(self):

        return '{"name": \"%s\", "room_type": \"%s\","capacity" :%d, \
        "available": %s}' % (self.name, self.room_type, self.capacity, self.available)


class Living_space(Room):
    """Living_space model with a capacity of 4 """
    room_type = 'L'
    capacity = 4

    def __repr__(self):
        """this it is the dictionary format that will be printed"""
        return '{"name": \"%s\", "room_type": \"%s\","capacity" :%d, \
        "available": %s}' % (self.name, self.room_type, self.capacity, self.available)


