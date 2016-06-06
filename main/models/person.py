from itertools import count


class Person():
    person_type = ''
    person_id = count(1)
    FELLOW = 'FELLOW'
    STAFF = 'STAFF'

    def __init__(self, name, living_space=False):
        self.name = name
        self.living_space = living_space
        self._id = next(self.person_id)
        self.allocation = {}
        self.allocated = False

    def is_staff(self):
        return self.person_type == self.STAFF

    def set_allocation(self, room):
        self.allocation[room.room_type] = room.name
        self.allocated = True

    @classmethod
    def instance(cls, name, person_type, want_housing='N'):
        living_space = True if want_housing == 'Y' else False
        if person_type.upper() == Person.STAFF:
            return Staff(name, False)
        else:
            return Fellow(name, living_space)



class Fellow(Person):
    person_type = Person.FELLOW


class Staff(Person):
    person_type = Person.STAFF
