import random


class Room():
    room_type = ''
    OFFICE = 'OFFICE'
    LIVING_SPACE = 'LIVING_SPACE'
    capacity = 0


    def __init__(self, name):
        self.name = name
        self.members = []



    def allocate(self, person):
        if self.filled():
            return False

        if person.person_type.upper() == "FELLOW" and person.living_space:
                self.check_member_exists(person)
                return True
        else:
            if person.is_staff():
                self.check_member_exists(person)
                return False


    def check_member_exists(self, person):
        if person not in self.members:
            self.members.append(person)
            person.set_allocation(self)

    def get_members(self):
        member_list = ''
        for person in self.members:
            member_list += person.name + ', '

        return member_list[:-1]

    def info(self):
        return self.name + '(' + self.room_type + ') ' + str(len(self.members)) + ' members'

    def filled(self):
        return len(self.members) >= self.capacity

    def is_office(self):
        return self.room_type == self.OFFICE

    @classmethod
    def instance(cls, name, room_type):
        if room_type.upper() == cls.OFFICE:
            return Office(name)
        else:
            return LivingSpace(name)


class LivingSpace(Room):
    capacity = 6
    room_type = Room.LIVING_SPACE


class Office(Room):
    capacity = 4
    room_type = Room.OFFICE
