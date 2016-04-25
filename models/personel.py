class Personel(object):
    """personel model"""

    def __init__(self, name, gender, position, want_accommodation=False):
        self.name = name


class staff(Personel):

    def __init__(self, name):
        self.name = name
        self.position = 'staff'


class fellow(Personel):

    def __init__(self, name, want_accommodation):
        self.name = name
        self.position = 'fellow'
        self.want_accommodation = want_accommodation
