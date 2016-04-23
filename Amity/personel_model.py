class Personel(object):
    """personel model"""

    def __init__(self, name, gender, position, want_accommodation=False):
        self.name = name
        self.gender = gender
        self.position = position
        self.want_accommodation = want_accommodation
        self.staff = []
        self.fellow = []

    def add_postion(self, position):
        """ method that separates fellows and staff"""
        if self.position == 's':
            self.staff.append(position)
        else:
            self.fellow.append(position)
