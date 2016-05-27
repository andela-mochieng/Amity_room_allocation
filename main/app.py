from __future__ import print_function
import random
import sqlite3
import sys
import tkFileDialog
from Tkinter import Tk

from clint.textui import colored, puts
from colorama import init, Back, Style  # Fore
from pyfiglet import figlet_format
from termcolor import cprint
from .models.person import Person, Fellow, Staff
from .models.room import Office, LivingSpace
from .util.File import FileParser
import ipdb


class Amity(object):
    """Description for amity"""

    def __init__(self):
        self.rooms = {
            'O': {}, 'L': {}
        }
        self.people = {
            'staff and fellow': [],
            'fellow to house': []
        }
        # People who have not been allocated to an office or living space
        self.unallocated = {
            'O': [], 'L': []
        }

        # People that have been fully occupied
        self.allocated_office = {}
        self.allocated_living = {}

        self.space = {}

    def create_rooms(self, rooms, room_type=None):
        """Allows user to enter a list of room names specifying
                whether office or living spaces"""
        if room_type is None:

            room_type = raw_input(
                "Enter room type: \n O: Office space \n L: Living space: \n"
            )
            while room_type != "O" and room_type != "L":
                room_type = raw_input(
                    "Try again. Enter Room Type:\n O: Office space \n L: Living space: \n"
                )
        random.shuffle(rooms)
        for room_name in rooms:
            if room_type.upper() == 'O':
                self.space = Office(room_name)
                self.rooms['O'].update({room_name: []})

            else:
                self.space = LivingSpace(room_name)
                self.rooms['L'].update({room_name: []})
        print(self.rooms)
        print('New rooms succesfully created')

    def add_person(self, first_name, last_name, person_type, want_housing):
        name = first_name + " " + last_name
        person_type = person_type
        want_housing = want_housing
        person = Person.create_person(name, person_type, want_housing)
        if want_housing.upper() == 'Y':
            self.people['fellow to house'].append(person)
            self.allocate_room(person, 'L')
        else:
            self.people['staff and fellow'].append(person)
        self.allocate_room(person, 'O')


    def allocate_room(self, person, room_type):
        """
        Get the number of occupants,Alllocate the room till its full, if room
        filled remove it else alllocate room, store unallocated"""
        for room_name, people_space in self.rooms[room_type].iteritems():
            check_capacity = len(people_space)
            if not self.space.is_filled(check_capacity):
                people_space.append(person)
                print(self.rooms)
                print("Personnel saved")
                return self.rooms

        self.unallocated[room_type].append(person)
        print("The following are unallocated:'\n'")
        print(self.unallocated)

    def reallocate_person(self, person_id, room_moved_to):
        for room_type in self.rooms.keys():
            for room_name, room_people in self.rooms[room_type].iteritems():
                for person in room_people:
                    if person_id == str(person._id):
                        print(person)
                        if not room_name == room_moved_to:
                            self.rooms[room_type][room_name].remove(person)
                            print(str(person) + "   successfully unallocated from  " + room_name)
                            # allocate them to new room
                            for room_names, room_occupants in self.rooms[room_type].iteritems():
                                if room_moved_to == room_names:
                                    ipdb.set_trace()
                                    room_capacity = len(room_occupants)
                                    if not self.space.is_filled(room_capacity):
                                        room_occupants.append(person)
                                        print (room_occupants)
                                        print(str(person) + "successfully reallocated to " + room_moved_to)
                                        return room_moved_to
        print("not found")

    def load_people(self):
        pass

def welcome_msg():
    init(strip=not sys.stdout.isatty())
    # cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
    # print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
    # Style.DIM + '\n(type help to get a list of commands)' + Style.NORMAL)
