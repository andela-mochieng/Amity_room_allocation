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
            'O': [], 'L': []
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

        self.filled_rooms = {
            'O': [], 'L': []
        }
        self.room_dict = {}
        self.space = {}
        self.full_populated_room = []

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
        for room_name in rooms:
            if room_type.upper() == 'O':
                self.space = Office(room_name)
                self.rooms['O'].append(self.space.room_name())
            else:
                self.space = LivingSpace(room_name)
                self.rooms['L'].append(self.space.room_name())

        random.shuffle(self.rooms['O'])
        random.shuffle(self.rooms['L'])
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
        print("Personnel saved")


    def allocate_room(self, person, room_type):
        ''' we get the name of the first available room, check if the room exist,
        Get the number of occupants,Alllocate the room till its full, if room filled remove it
        else alllocate room, store unallocated'''
        allocated = False
        if self.rooms[room_type] != []:
            room = self.rooms[room_type][0]
            if self.room_dict.get(room) is None:
                self.room_dict[room] = []
                check_capacity = len(self.room_dict[room])
                while not allocated:
                    if not self.space.is_filled(check_capacity):
                        self.room_dict[room].append(person)
                        allocated = True
                    print(self.room_dict)
                    self.full_populated_room.append(self.rooms[room_type].remove(room))
                    print("fullly")
                    print(self.full_populated_room)

                    if self.rooms[room_type] != []:
                        room = self.rooms[room_type][0]
                        self.room_dict[room] = []
                print(self.room_dict)
        if not allocated:
            self.unallocated[room_type].append(person)
            print("unallocated")
            print(self.unallocated)




def welcome_msg():
    init(strip=not sys.stdout.isatty())
    # cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
    # print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
    # Style.DIM + '\n(type help to get a list of commands)' + Style.NORMAL)
