class Personel(object):
    """personel model"""

    def __init__(self, name):
        self.name = name
        want_accommodation = 'N'


class staff(Personel):

    def __init__(self, name):
        self.name = name
        self.position = 'staff'


class fellow(Personel):

    def __init__(self, name, want_accommodation):
        self.name = name
        self.position = 'fellow'
        self.want_accommodation = want_accommodation
