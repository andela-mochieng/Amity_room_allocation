from Tkinter import Tk
from db import save
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

class Amity(object):
    """Description for amity"""
    def __init__(self):
        # variable used in create_rooms
        self.rooms = {
        'O': [],
        'L':[]
        }
        # variable used in add_person
        self.people_data = {'Staff':[],
        'Fellow':[{}]
        }
        self.allocate ={
        'O' : {' ':[]},
        'L': {' ':[]}
        }
        # variable used in allocation
        self.offices = []
        self.full_name = []
        self.allocated_room = []

        # variables used in add_person
        self.name = ""
        self.personnel_type = ""
        self.want_accommodation = ""

        # variables used in print_allocation function
        self.room_name = ""
        self.room_type = ""
        self.people_room = ""
        self.people_in_room = []
        # variables used in print_allocation function
        self.person_name = []
        self.person_type = ""

        # used in create_rooms
        self.save_data = save.Save_data()
        save_data = self.save_data

        self.conn = sqlite3.connect("amity.sqlite")
        self.connect = self.conn.cursor()
        self.connect.execute(
                "CREATE TABLE IF NOT EXISTS Rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, type TEXT, capacity integer)")

        self.connect.execute(
                "CREATE TABLE IF NOT EXISTS Persons(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Personel_type TEXT, want_accommodation TEXT, office_accommodation TEXT , living_accomodation TEXT)")






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
                ipdb.set_trace()
            self.connect.execute("INSERT INTO Rooms (Name, type) VALUES (?, ?)", [room_name, room_type])
            self.conn.commit()
        return 'New rooms succesfully created'
        return self.rooms


    def allocations(self):
        ipdb.set_trace()
        self.rooms
        self.offices.append(self.rooms['O'])
        print self.Offices
        self.people_data
        self.allocate


    def allocate(self, **kwargs):
        """function allocates both staff & fellow office and only
        allocates fellow who want accommodation to living spaces """

        if kwargs['personnel_type'].upper() is 'STAFF' or 'FELLOW':
            connection.execute(
                "SELECT Name, capacity, available from Rooms where Room_type = \"O\"")
            for row in connection:
                spaces = row[2].encode('ascii').split(' ')
                for index, space in enumerate(spaces):
                    if '0' == space:
                        spaces[index] = kwargs['name']
                        new_spaces = (' ').join(str(item) for item in spaces)
                        connection.execute("UPDATE Rooms set available = ? where \
                                    Name = ?", (new_spaces, row[0]))
                        conn.commit()
                        break

        if kwargs['want_accommodation'].lower() == '--o=y' or kwargs['want_accommodation'].lower() == 'y':
            connection.execute(
                "SELECT Name, capacity, available from Rooms where Room_type = 'L' ")
            for row in connection:
                spaces = row[2].encode('ascii').split(' ')
            # if living space is empty
                for index, space in enumerate(spaces):
                    if '0' == space:
                        spaces[index] = kwargs['name']
                        new_spaces = (' ').join(str(item) for item in spaces)
                        connection.execute("UPDATE Rooms set available = ? where \
                                    Name = ?", (new_spaces, row[0]))
                        conn.commit()
                        break
        else:
            print "Fellow or staff not assigned living space "



    def add_person(self, first_name, last_name, person_type, want_housing):
        if type(first_name) != str or type(last_name) != str or type(living_space) != str:
            raise ValueError
        name = first_name + " " + last_name
        person_type = person_type
        want_accommodation = want_housing
        if person_type.upper() =='STAFF':
            self.people_data['Staff'].append(name)
        else:
            self.people_data['Fellow'].append({name:want_accommodation})
        #allocate rooms


        # insert_db(name=name, personnel_type=personnel_type,
        #           want_accommodation=want_accommodation)
        # allocate(name=name, personnel_type=personnel_type,
        #          want_accommodation=want_accommodation)
        return self.people_data
            # allocation of fellows to living_space




    def insert_db(self, **kwargs):
        if kwargs['personnel_type'].upper() is "FELLOW" or "STAFF":
            connection.execute("INSERT INTO Persons VALUES (?, ?, ?)",
                               (str(kwargs['name']), str(kwargs['personnel_type']),
                                str(kwargs['want_accommodation'])))
            conn.commit()


    def reallocate_person(self, first_name, last_name, new_room_name):
        self.full_name = first_name + " " + last_name
        self.allocated_room = new_room_name



        # connection.execute(
        #     "DELETE from Rooms where available = ?", [reallocate_details])
        # room = args.get('<new_room_name>')
        # ipdb.set_trace()
        # connection.execute(
        #     "UPDATE Rooms SET available = ? WHERE Name = ?",
        #     [reallocate_details, room])


    def load_people(args):
        load = Tk()
        load.withdraw()
        load.update()
        file = tkFileDialog.askopenfile(parent=load, mode='rb', title="Load file")
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
