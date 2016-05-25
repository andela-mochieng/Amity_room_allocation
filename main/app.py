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
        self.all_personnel = []
        # People that have been fully occupied
        self.allocated_office = {}
        self.allocated_living = {}

        self.filled_rooms = {
            'O': [], 'L': []
        }
        self.room_dict = {}

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
                room = Office(room_name)
                self.rooms['O'].append(room)
            else:
                room = LivingSpace(room_name)
                self.rooms['L'].append(room)

        random.shuffle(self.rooms['O'])
        random.shuffle(self.rooms['L'])
        # print(self.rooms)
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
        allocated = False
        index = 0
        while index < len(self.rooms[room_type]) and not allocated:
            print('room_len')
            print(len(self.rooms[room_type]))
            room = self.rooms[room_type][index]
            if not room.is_filled():
                is_filled_after_allocation = room.add_member(person)
                if self.room_dict.get(room):
                    self.room_dict[room].append(person)

                print(self.room_dict)
                allocated = True
                index += 1
            else:
                self.populate_allocated_rooms(room_type, index)

        if not allocated:
            self.unallocated[room_type] = [person]
            print(self.unallocated)

    def populate_allocated_rooms(self, room_type, room_index):
        allocated_room = self.rooms[room_type].pop(room_index)
        self.filled_rooms[room_type].append(allocated_room)



def welcome_msg():
    init(strip=not sys.stdout.isatty())
    # cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
    # print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
    # Style.DIM + '\n(type help to get a list of commands)' + Style.NORMAL)
