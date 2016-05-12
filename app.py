from Tkinter import Tk
import tkFileDialog
from util.File import fileParser
from termcolor import cprint
from colorama import init, Back, Style  # Fore
from docopt import docopt, DocoptExit
from pyfiglet import figlet_format
import sqlite3
from clint.textui import colored, puts
from models.room import Office, Living_space
import cmd
import random
import sys
import ipdb
import random


class Amity(object):
    """Description for amity"""

    def __init__(self):
        # variable used in create_rooms
        self.rooms = {
            'O': [],
            'L': []
        }
        # variable used in add_person
        self.people_data = {'Staff': [],
                            'Fellow': []
                            }
        self.allocate = {
            'O': {' ': []},
            'L': {' ': []}
        }
        # variable used in allocation
        self.offices = []
        self.full_name = []
        self.allocated_room = []

        # variables used in add_person
        self.name = ""
        name = self.name
        self.personnel_type = ""
        personnel_type = self.personnel_type
        self.want_accommodation = ""
        want_accommodation = self.want_accommodation

        # variables used in print_allocation function
        self.room_name = ""
        self.room_type = ""
        self.people_room = ""
        self.people_in_room = []
        # variables used in print_allocation function
        self.person_name = []
        self.person_type = ""

        # uded in add_person
        self.office = Office()
        self.living = Living_space()

        self.conn = sqlite3.connect("amity.sqlite")
        self.connect = self.conn.cursor()
        self.connect.execute(
            "CREATE TABLE IF NOT EXISTS Rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, type TEXT, capacity integer)")

        self.connect.execute(
            "CREATE TABLE IF NOT EXISTS Persons(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Personnel_type TEXT, want_accommodation TEXT, office_accommodation TEXT , living_accomodation TEXT)")

    def create_rooms(self, room):
        """allows user to enter a list of room names specifying
            whether office or living spaces"""
        room_type = raw_input(
            "Enter room type: \n O: Office space \n L: Living space: \n")

        while room_type != "O" and room_type != "L":
            room_type = raw_input(
                "Try again. Enter Room Type:\n O: Office space \n L: Living space: \n")
        for room_name in room:
            if room_type.upper() == 'O':
                self.rooms[room_type.upper()].append(room_name)
            else:
                self.rooms['L'].append(room_name)
            self.connect.execute(
                "INSERT INTO Rooms (Name, type) VALUES (?, ?)", [room_name, room_type])
            self.conn.commit()
        return 'New rooms succesfully created'
        return self.rooms

    def office_space_count(self):
        ''' keep track of offices allocated'''
        office_space = self.connect.execute(
            "SELECT Rooms.id, Rooms.Name, Rooms.type, COUNT(*) AS office_occupants FROM Rooms LEFT JOIN Persons ON Rooms.Name = Persons.office_accommodation WHERE Rooms.type='O' GROUP BY Rooms.Name"
        )
        return office_space

    def living_space_count(self):
        '''keep track of living space allocated'''
        living_space = self.connect.execute(
            "SELECT Rooms.id, Rooms.Name, Rooms.type, COUNT(*) AS living_occupants FROM Rooms LEFT JOIN Persons ON Rooms.Name = Persons.living_accomodation WHERE Rooms.type='L' GROUP BY Rooms.Name")
        return living_space

    def add_person(self, first_name, last_name, person_type, want_housing):
        name = first_name + " " + last_name
        person_type = person_type
        want_accommodation = want_housing
        if person_type.upper() == 'STAFF':
            self.people_data['Staff'].append(name)
        else:
            self.people_data['Fellow'].append({name: want_accommodation})
        self.insert_db(name=name, person_type=person_type,
                       want_accommodation=want_accommodation)
        ipdb.set_trace()
        # to randomly allocate everyone an office
        office_name = self.connect.execute(
            "SELECT Name FROM Rooms where type = 'O'")
        for off_name in office_name:
            if self.office_space_count() < self.office.capacity:
                office = random.choice(off_name)
        self.allocate_office(name, office)

        # randomly accomodate fellows who want accommodation
        if person_type.upper() == 'FELLOW' and want_accommodation.upper() == 'Y':
            living_name = self.connect.execute(
                "SELECT Name FROM Rooms where type = 'L'")
            for liv_name in living_name:
                if self.living_space_count() < self.living.capacity:
                    housing = random.choice(liv_name)
            self.allocate_housing(name, housing)
        # print self.people_data
        return self.people_data
            # allocation of fellows to living_space

    def insert_db(self, **kwargs):
        if kwargs['person_type'].upper() is "FELLOW" or "STAFF":
            self.connect.execute("INSERT INTO Persons (Name, Personnel_type, want_accommodation) VALUES (?, ?, ?)",
                                 [kwargs['name'], kwargs['person_type'],
                                  kwargs['want_accommodation']])
            self.conn.commit()

    def allocate_office(self, person_name, office_name):
        """function allocates both staff & fellow office"""
        # allocate offices
        allocate = self.connect.execute(
            "UPDATE Persons set office_accommodation = ? where Name = ? ", (office_name, person_name))
        self.conn.commit()

    def allocate_housing(self, person_name, house_name):
        '''only allocates fellow who want accommodation to living spaces'''
        allocate = self.connect.execute(
            "UPDATE Persons set living_accomodation = ? where Name = ? ", (house_name, person_name))

    def reallocate_person(self, first_name, last_name, new_room_name):
        pass

    def load_people(args):
        load = Tk()
        load.withdraw()
        load.update()
        file = tkFileDialog.askopenfile(
            parent=load, mode='rb', title="Load file")
        if file:
            save_file_path(file.name)
            parser = fileParser(file.name)
            input_data = parser.read_file()
            for lines in input_data:
                print lines
                if len(lines) > 2:
                    name = lines[0]
                    personnel_type = lines[1]
                    want_accommodation = lines[2]
                    insert_db(name=name, personnel_type=personnel_type,
                              want_accommodation=want_accommodation)
                    allocate(name=name, personnel_type=personnel_type,
                             want_accommodation=want_accommodation)

    def print_allocations(args):
        """function screens data  from db to the cmdline and into a file """
        connection.execute(
            "SELECT Name, Room_type, available from Rooms")

        for items in connection:
            item = list(items)
            item = map(lambda x: x.encode('ascii'), item)
            room_name = item[0]
            room_type = item[1]
            people_room = item[2]
            print "-" * 30
            puts(colored.red(room_name))
            print "-" * 30
            puts(colored.white(room_type))
            print "-" * 3
            puts(colored.blue(people_room))
            people_in_room.append(people_room)
            file = args.get('--o')
            if file != 'None':
                filename = file
                f = open(filename, 'a+')
                newdata = "Room Name:" + room_name + ", " + \
                    " Room type:" + room_type + ", " + \
                    "Occupants: " + people_room + '\n'
                f.write(newdata)
            else:
                print('No filename specificied')

    def print_room(args):
        """function prints out members of a room"""
        room = args['<room_name>'].split(' ')
        connection.execute(
            "SELECT Name, available from Rooms where Name = ?", (room))
        for allocated in connection:
            allocated = map(lambda x: x.encode('ascii'),
                            allocated)
            return puts(colored.blue(allocated[1]))
        print('No room with that name')

    def print_unallocated(args):
        people_org = []

        connection.execute(
            "SELECT available from Rooms")
        for people_room in connection:
            if people_room != (None,):
                people_room = map(lambda x: x.encode('ascii'), people_room)
                people_in_room.extend(people_room)
            # print people_in_room
        connection.execute(
            "SELECT Name, Personel_type, want_accommodation from Persons")
        for name in connection:
            name = map(lambda x: x.encode('ascii'), name)
            person_name = name[0]
            person_type = name[1]
            person_accommodate = name[2]
            people_org.append(person_name)
        print people_org

        for name in people_org:
            for names in people_in_room:
                if name in names == False and person_accommodate.upper() is 'N':
                    puts(colored.white(person_name) + " " +
                         colored.red(person_type) + " " +
                         colored.blue(person_accommodate))
        print "Everyone allocated"

        file = args.get('--o')
        if file != None:
            filename = file
            f = open(filename, 'a+')
            newdata = person_name + ", " + \
                person_type + ", " + person_accommodate + '\n'
            f.write(newdata)
        else:
            print('No filename specificied')

    def save_file_path(path):
        with open("filePath", "w+") as f:
            f.write(path)

    def load_state(args):
        connection.execute("SELECT * FROM Rooms")
        print connection.fetchall()
        connection.execute("SELECT * FROM Persons")
        print connection.fetchall()


def welcome_msg():
    init(strip=not sys.stdout.isatty())
    cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
    print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
          Style.DIM + '\n(type help to get a list of commands)' + Style.NORMAL)
