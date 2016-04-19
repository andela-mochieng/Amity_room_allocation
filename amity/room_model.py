class Room(object):
    
    def __init__(self, **kwargs):
        if kwargs:
            self.name = kwargs.get['name', '']
            self.type = kwargs.get['type', '']
            self.capacity = kwargs['capacity', 0]


class Offices(Room):
    """offices a class object inherits
     from Room it contains a  class variable capacity """
    capacity = 6
    type = 'Office'

    def __repr__(self):
        return 'name:{},room_type:{},capacity:{}'\
                .format(self.name, self.type, self.capacity)


class living_space(Room):
    """ living_space a class object inherits
     from Room, it contains a  class variable capacity """
    capacity = 4
    type = 'living_area'

    def __repr__(self):
        return 'name:{},room_type:{},capacity:{}'\
                .format(self.name, self.type, self.capacity)
