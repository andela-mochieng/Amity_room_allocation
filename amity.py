'''
Usage:
    app.py create_rooms <room_type> <room_names>...
    app.py --version
Options:
    --version   Show version.
    -h --help   Show help
'''


import pickle
import os
# from room_model import Room, Office, Living_space


class Amity(object):

    def __init__(self, d_path=os.path.dirname(os.path.abspath(__file__))):
        self.offices = []
        self.person = []
        self.office_name = ""
        self.d_path = d_path
        self.room_file = os.path.join(self.d_path, "data/rooms.pkl")
        self.personel = os.path.join(self.d_path, "data/personel.pkl")

    def save_office(self, rooms):

        outFile = open(self.room_file, 'wb')
        pickle.dump(rooms, outFile)
        outFile.close()
        return(rooms)

    def save_persons(self, persons):
        outFile = open('self.personel', 'wb')
        pickle.dump(persons, outFile)
        outFile.close()
        return(persons)

    def create_office(self):
        """ allows user to enter a list of room names """
        self.offices.append(self.office_name)
        print self.offices
        self.save_office

    def create_living_space(living_name):
        print "living_name: %s" % living_name

        # self.rooms.append(room)
        # self.save_rooms()

    # def add_person(self, personel, ptype, want_accommodation):
    #     print personel, ptype, want_accommodation
    #     person = {
    #         "personnel": personel,
    #         "ptype": ptype,
    #         "want_accommodation": want_accommodation

    #     }
    #     persons.append(person)
    #     print person, "successful added"
