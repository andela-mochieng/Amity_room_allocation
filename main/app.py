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
import ipdb


class Amity(object):
    """Description for amity"""

    def __init__(self, db_name="amity.sqlite"):

        self.conn = sqlite3.connect(db_name)
        self.connect = self.conn.cursor()
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
        Get the number of occupants,Alllocate the room till they are full, if room
        filled remove it else alllocate room, then store unallocated"""
        for room_name, people_space in self.rooms[room_type].iteritems():
            check_capacity = len(people_space)
            if not self.space.is_filled(check_capacity):
                people_space.append(person)
                return self.rooms
        self.unallocated[room_type].append(person)

    def reallocate_person(self, person_id, room_moved_to):
        ''' Enables users to reallocate personnel to rooms '''
        for room_type in self.rooms.keys():
            for room_name, room_people in self.rooms[room_type].iteritems():
                for person in room_people:
                    if person_id == str(person._id):
                        print(person)
                        if not room_name == room_moved_to:
                            self.rooms[room_type][room_name].remove(person)
                            for room_names, room_occupants in self.rooms[room_type].iteritems():
                                if room_moved_to == room_names:
                                    room_capacity = len(room_occupants)
                                    if not self.space.is_filled(room_capacity):
                                        room_occupants.append(person)
                                        print (room_occupants)
                                        print(
                                            str(person) + "successfully reallocated to " + room_moved_to)
                                        return room_moved_to
        print("not found")

    def load_people(self, load_file):
        '''Allows user to allocate people by loading data from a file '''
        if len(load_file) < 1:
            load = Tk()
            load.withdraw()
            load.update()
            load_file = tkFileDialog.askopenfile(
                parent=load, mode='rb', title="Load file")
            filename = load_file.name
        else:
            filename = load_file
        lines = [line.rstrip('\n') for line in open(filename, 'r')]

        for line in lines:
            words = line.split(" ")
            first_name = words[0]
            last_name = words[1]
            personnel_type = words[2]
            if len(words) == 4:
                want_housing = words[3]
            else:
                want_housing = 'N'
            self.add_person(first_name, last_name,
                            personnel_type, want_housing)

    def print_allocations(self, *args):
        """function prints to the screen people allocated to rooms as well
        as to a file if specified"""
        try:
            file_name = args[0]['--o']
        except IndexError:
            file_name = None
        if file_name:
            with open(file_name, 'a+') as f:
                 for room_type in self.rooms.keys():
                    for room_name, room_people in self.rooms[room_type].iteritems():
                        f.write(room_name + '\n' + str(room_people).strip('[').strip(']') + '\n')
        else:
            puts(colored.green(
                '\n Below is list of personnel allocated to rooms: \n'))
            self.allocations()

    def allocations(self):
        '''Help method called by  print_allocations'''
        for room_type in self.rooms.keys():
            for room_name, room_people in self.rooms[room_type].iteritems():
                line = len(str(room_people))
                print(room_name + '\n' + '-' * line + '\n' +
                      str(room_people).strip('[').strip(']'))

    def print_unallocated(self, *args):
        '''Prints the people unallocated rooms'''
        try:
            file_name = args[0]['--o']
        except IndexError:
            file_name = None
        if file_name:
            with open(file_name, 'a+') as f:
                for room_type, unallocated in self.unallocated.iteritems():
                    f.write(room_type + '\n' + str(unallocated).strip('[').strip(']') + '\n')

        else:
            puts(colored.green(
                '\n Below is list of personnel unallocated to rooms: \n'))
            for room_type, unallocated in self.unallocated.iteritems():
                line = len(str(unallocated))
                print(room_type + '\n' + '-' * line + '\n' +
                      str(unallocated).strip('[').strip(']'))

    def print_room(self, room):
        ''' Prints people allocated to rooms'''
        for room_type in self.rooms.keys():
            for room_name, room_people in self.rooms[room_type].iteritems():
                if room == room_name:
                    print(room_people)

    def create_tables(self):
        '''Creates the database tables'''
        try:
            self.connect.execute(
                "CREATE TABLE IF NOT EXISTS Allocations(id INTEGER PRIMARY KEY AUTOINCREMENT, Room_names TEXT, Occupants TEXT)")

            self.connect.execute(
                "CREATE TABLE IF NOT EXISTS Unallocated(id INTEGER PRIMARY KEY AUTOINCREMENT, Room_type TEXT, unallocated TEXT)")
        except sqlite3.IntegrityError:
            return False

    def save_state(self, *args):
        '''persists data to the database'''
        self.create_tables()
        for room_type in self.rooms.keys():
            for room_name, room_people in self.rooms[room_type].iteritems():
                self.connect.execute(
                    "INSERT INTO Allocations(Room_names, Occupants) VALUES(?, ?)",
                    [str(room_name), str(room_people)])
            self.conn.commit()
        for room_type, unallocated in self.unallocated.iteritems():
            self.connect.execute(
                "INSERT INTO Unallocated(Room_type, unallocated) VALUES(?, ?)",
                [str(room_type), str(unallocated)])
            self.conn.commit()

    def load_state(self, args):
        '''loads data from the database'''
        puts(colored.green(" Data stored in the Allocation's table"))
        allocations = self.connect.execute(
            "SELECT * FROM Allocations").fetchall()
        for room in allocations:
            room = list(room)
            print(' '.join([str(i) for i in room]))

        puts(colored.green(" Data stored in the Unallocated table"))
        unallocated = self.connect.execute(
            "SELECT * FROM Unallocated").fetchall()
        for room_type in unallocated:
            room_type = list(room_type)
            print(' '.join([str(i) for i in room_type]))

def welcome_msg():
    init(strip=not sys.stdout.isatty())
    # cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
    # print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
    # Style.DIM + '\n(type help to get a list of commands)' + Style.NORMAL)
