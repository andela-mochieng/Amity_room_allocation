''' class that creates office and living space properties'''


class Office(object):
    """initialises a capacity of 6 to be occupated by staff and fellows """

    def __init__(self, name, capacity=6):
        self.name = name
        self.capacity = capacity
        self.roomOccupants = []

    def add_member(self, occupant):
        """ method that appends/adds new occupant to roomOccupants """
        self.roomOccupants.append(occupant)


class living_space(Office):
    """this clas inherits from Office """

    def __init__(self, roomtype, name, capacity=4):
        """this __init__ override the init in the Office """
        super(living_space, self).__init__(roomtype, name)
        self.roomtype = roomtype
        self.name = name
        self.capacity = capacity
        self.male = []
        self.female = []

    def add_fellow(self, occupant):
        """method adds fellows according to they gender to a room"""
        if self.roomtype == 'm':
            self.male.append(occupant)
        else:
            self.female.append(occupant)
