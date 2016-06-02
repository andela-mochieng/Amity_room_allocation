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
from .models.person import Person
from .models.room import Room
import ipdb


class Amity(object):
    """Description for amity"""
    people = []
    rooms = []

    def __init__(self, db_name="amity.sqlite"):

        self.conn = sqlite3.connect(db_name)
        self.connect = self.conn.cursor()
        self.remove_from_room = ''

    def create_rooms(self, args):
        """Allows user to enter a list of room names specifying
                whether office or living spaces"""
        for index, room_name in enumerate(args['<room_name>']):
            room = Room.instance(room_name, args['<room_type>'][index])
            self.rooms.append(room)
            print(room.name + ' (' + room.room_type + ') ' +
                  ' successfully created')

    def get_available_rooms(self, room_type):
        available_rooms = [room for room in self.rooms if not room.filled(
        ) and room.room_type == room_type.upper()]
        return available_rooms

    def get_random_available_room(self, room_type):
        available_rooms = self.get_available_rooms(room_type)
        selected = None
        if available_rooms:
            selected = random.choice(available_rooms)
        return selected

    def add_person(self, first_name, last_name, person_type, want_housing):
        """ adds personnel calls allocate method """
        name = first_name + " " + last_name
        person = Person.instance(name, person_type, want_housing)
        self.people.append(person)
        if self.rooms:
            room = self.get_random_available_room(Room.OFFICE)

        if not room:
            print('no room')
            return False
        if not room.allocate(person):
            print('unable to allocate ' + person.name)
        else:
            print(person.name + ' allocated to ' + room.name)
        if person.person_type.lower() == 'fellow' and person.living_space:
            living_room = self.get_random_available_room(Room.LIVING_SPACE)
            if living_room:
                if not living_room.allocate(person):
                    print('unable to allocate ' + person.name)
                else:
                    print(person.name + ' allocated to ' + room.name)
        else:
            print("Person doesn't require housing")

    def reallocate_person(self, arg):
        """Reallocate person from one room to another"""
        room_name = arg['<new_room_name>'].upper()
        person_id = arg['<person_id>'].upper()
        room_type = 'OFFICE' if not arg['-l'] else 'LIVINGSPACE'
        import ipdb
        ipdb.set_trace()
        person = self.get_person_id(person_id)
        if not person:
            print('No person with ID: ' + person_id)
            return False

        if not person.allocated:
            person.name() + ' has not been allocated to a room'
            answer = print('Do you want to allocate ' +
                           person.name() + ' to ' + room_name + '? Y/N: ')
            if answer == 'N':
                return False

        if room_name in person.allocation.values():
            print(person.name() + ' already allocated to ' + room_name)
            return False
        for room_kind, name_of_room in person.allocation.iteritems():
            if room_name == name_of_room:
                room = self.remove_person_from_room(person, room_kind)
                if not room:
                    print('Unable to find person in a room')
                    return False
        person.living_space = True if room_kind == 'LIVINGSPACE' else False
        if not person.allocated(person, room_name):
            msg = person.name() + ' cannot be allocated to ' + room_name
            msg += '; verify that ' + room_name + ' is a/an ' + room_type
            print(msg)
            if room:
                room.allocate(person)
                print(person.name() + ' has been moved to ' + room.name)

    def get_room_name(self, room_name):
        """
        This method will return a room corresponding to the room name parameter
        """
        return [room for room in self.rooms if room.name.lower() == room_name.lower()]

    def get_person_id(self, person_id):
        """Return person instance with corresponding person_id"""

        for person in self.people:
            for pers_id in str(person._id):
                if person_id == pers_id:
                    print(person)
                    return person
        return False

    def remove_person_from_room(self, person, room_type):
        """Remove person from a room"""
        room_name = person.allocation[room_type]
        room = self.get_room_name(room_name)
        if room:
            if room[0]:
                self.remove_person(person)
                self.remove_from_room = room[0]
                return room[0]
        return False

    def remove_person(self, person):
        """Removes person from people list """

        for index, person_in in enumerate(self.people):
            if person_in.name == person.name:
                self.people.pop(index)
                del person.allocation[self.room_type]
                if self.room_type == 'LIVINGSPACE':
                    person.living_space = False
                if not person.allocation:
                    person.allocated = False
                return True

        return False

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
            print('print_allocations and unallocated to view allocations')

    def print_allocations(self, *args):
        """function prints to the screen people allocated to rooms as well
        as to a file if specified"""
        try:
            file_name = args[0]['--o']
        except TypeError:
            file_name = None
        if file_name:
            with open(file_name, 'a+') as f:
                for room in self.rooms:
                    if len(room.members):
                        f.write(room.info() + '\n' + room.get_members() + '\n')
        else:
            puts(colored.green(
                '\n Below is list of personnel allocated to rooms: \n'))
            self.allocations()

    def allocations(self):
        '''Help method called by  print_allocations'''
        for room in self.rooms:
            if len(room.members):
                print(room.info())
                print(room.get_members())

    def print_unallocated(self, *args):
        '''Prints the people unallocated rooms'''
        try:
            file_name = args[0]['--o']
        except TypeError:
            file_name = None
        if file_name:
            with open(file_name, 'a+') as f:
                for room_type, unallocated in self.unallocated.iteritems():
                    f.write(room_type + '\n' +
                            str(unallocated).strip('[').strip(']') + '\n')

        else:
            puts(colored.green(
                '\n Below is list of personnel unallocated to rooms: \n'))
            for room_type, unallocated in self.unallocated.iteritems():
                line = len(str(unallocated))
                print(room_type + '\n' + '-' * line + '\n' +
                      str(unallocated).strip('[').strip(']'))

    def print_room(self, view_room_members):
        ''' Prints people allocated to rooms'''
        for room in self.rooms:
            if room.name.lower() == view_room_members.lower():
                print(room.members)

    def create_tables(self):
        '''Creates the database tables'''
        try:
            self.connect.execute(
                "CREATE TABLE IF NOT EXISTS People(id INTEGER PRIMARY KEY AUTOINCREMENT, Names TEXT)")

            self.connect.execute(
                "CREATE TABLE IF NOT EXISTS Rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, Room_name TEXT)")
        except sqlite3.IntegrityError:
            return False

    def save_state(self, *args):
        '''persists data to the database'''
        self.create_tables()
        for room_type in self.rooms.keys():
            for room_name, room_people in self.rooms[room_type].iteritems():
                self.connect.execute(
                    "INSERT INTO People(Names) VALUES(?)",
                    [str(self.people)])
            self.conn.commit()
        for room_type, unallocated in self.unallocated.iteritems():
            self.connect.execute(
                "INSERT INTO Rooms(Room_name) VALUES(?)", [str(self.rooms)])
            self.conn.commit()

    def load_state(self, args):
        '''loads data from the database'''
        puts(colored.green(" Data stored in the Allocation's table"))
        people = self.connect.execute(
            "SELECT * FROM People").fetchall()
        for person in people:
            person = list(person)
            print(' '.join([str(i) for i in person]))

        puts(colored.green(" Data stored in the Unallocated table"))
        rooms = self.connect.execute(
            "SELECT * FROM Rooms").fetchall()
        for room in rooms:
            room = list(room)
            print(' '.join([str(i) for i in room]))


def welcome_msg():
    init(strip=not sys.stdout.isatty())
    # cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
    # print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
    # Style.DIM + '\n(type help to get a list of commands)' + Style.NORMAL)
