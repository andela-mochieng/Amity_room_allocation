from itertools import count

class Person(object):
    person_id = count(1)

    def __init__(self, name, want_housing):
        self.name = name
        self.want_housing = want_housing
        self.assigned_room = None
        self.assigned_office = None
        self._id = next(self.person_id)


    @classmethod
    def create_person(cls, name, type, want_housing):
        person = Fellow(name, want_housing) if type.lower(
        ) == "fellow" else Staff(name)
        return person

    def __repr__(self):
        return "#-{} {} {}". format(self._id, self.name, self.want_housing)

    @property
    def person_type(self):
        return self.__class__.__name__


class Fellow(Person):
    pass


class Staff(Person):
    def __init__(self, name):
        super(Staff, self).__init__(name, "N")
