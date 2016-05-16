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

from models.room import Office, LivingSpace
from util.File import FileParser
import ipdb



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
        # variables used in add_person
        self.name = ""
        name = self.name
        self.personnel_type = ""
        personnel_type = self.personnel_type
        self.want_accommodation = ""
        want_accommodation = self.want_accommodation
        # variable used in allocation
        self.offices = []
        self.full_name = []
        self.allocated_room = []

        # variables used in print_allocation function
        self.person_name = ""
        self.person_type = ""
        self.room_name = ""
        self.people_in_room = []
        # variables used in print_allocation function
        self.person_name = []
        self.person_type = ""

        # uded in add_person
        self._office = Office()
        self.living = LivingSpace()
        self.offices = []
        self.housing = []
        # reallocation variables
        self.available_office = []
        self.available_housing = []

        # data strutures in print_allocations
        self.office_allocations = []
        self.living_alllocations = []
        self.office_occupants = []
        self.unallocated_offices = []
        self.living_occupants = []
        self.unallocated_houses = []
        self.office = []
        self.housing = []
        # variable in count
        self.living_occupied = 0
        self.office_occupied = 0


        self.conn = sqlite3.connect("amity.sqlite")
        self.connect = self.conn.cursor()
        self.connect.execute(
            "CREATE TABLE IF NOT EXISTS Rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, type TEXT)")

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
        print('New rooms succesfully created')


    def office_space_count(self, off_name):
        ''' keep track of offices allocated'''
        off_name = str(off_name)
        office_space = self.connect.execute(
            "SELECT COUNT(*) AS office_occupants FROM Persons  WHERE Persons.office_accommodation = ?", [off_name]).fetchall()
        self.office_occupied = office_space[0][0]
        print(self.office_occupied)

        return self.office_occupied


    def living_space_count(self, liv_name):
        '''keep track of living space allocated'''
        # print(liv_name)
        living_space = self.connect.execute(
            "SELECT COUNT(*) AS living_occupants FROM Persons WHERE Persons.living_accomodation = ?", [liv_name]).fetchall()
        for liv_space in living_space:
            self.living_occupied = liv_space[0]
            print(self.living_occupied)
        return self.living_occupied


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

        self.allocation_rule(name, person_type,
                             want_accommodation)

    def allocation_rule(self, name, person_type, want_accommodation):
        '''to randomly allocate everyone an office'''
        office_name = self.connect.execute(
            "SELECT Name FROM Rooms where type = 'O'").fetchall()
        for off_name in office_name:
            off_name = off_name[0]
            ipdb.set_trace()
            office_occupied = self.office_space_count(off_name)

            if office_occupied < self._office.capacity:
                print(office_occupied)

                self.available_office.append(off_name)
                self.office = random.choice(self.available_office)
            else:
                print (name + " unallocated")


        if self.office:
            self.allocate_office(name, self.office)

        if person_type.upper() == 'FELLOW' and want_accommodation == 'Y':
            living_name = self.connect.execute(
                "SELECT Name FROM Rooms where type = 'L'").fetchall()
            for liv_name in living_name:
                liv_name = liv_name[0]
                liv_occupied = self.living_space_count(liv_name)
            if liv_occupied  < self.living.capacity:
                self.available_housing.append(liv_name)
                self.housing = random.choice(self.available_housing)
            else:
                print(" All living spaces are full")
            if self.housing:
                self.allocate_housing(name, self.housing)
        else:
            print("Personnel hasn't requested to be housed")
        # print self.people_data
        return self.people_data
            # allocation of fellows to living_space

    def insert_db(self, **kwargs):
        if kwargs['person_type'].upper() is "FELLOW" or "STAFF":
            self.connect.execute("INSERT INTO Persons (Name, Personnel_type, want_accommodation) VALUES (?, ?, ?)", [kwargs['name'], kwargs['person_type'], kwargs['want_accommodation']])
            self.conn.commit()

    def allocate_office(self, person_name, office_name):
        """function allocates both staff & fellow office"""
        self.person_name = person_name
        self.office_name = str(office_name).strip('[').strip(']').strip("'").strip("'")

        allocate = self.connect.execute(
            "UPDATE Persons set office_accommodation = ? WHERE Persons.Name = ?", [self.office_name, self.person_name])
        self.conn.commit()
        print(self.person_name + " successfully allocated to office: " + self.office_name)


    def allocate_housing(self, name, housing):
        '''only allocates fellow who want accommodation to living spaces'''
        self.name = name
        self.housing = str(housing).strip('[').strip(']').strip("'").strip("'")
        allocate = self.connect.execute(
            "UPDATE Persons set living_accomodation = ? WHERE Persons.Name = ?", [self.housing, self.name])
        self.conn.commit()
        print(self.name + " successfully allocated to house: " + self.housing)

    def reallocate_person(self, person_id, new_room_name):
        '''method searches the db for the personnel details, and the details of the new
        room to be allocated to and reallocates according to whether fellow or
        staff and alerts if person was already an occupant of that room'''

        person_allocate = self.connect.execute(
            "SELECT * FROM Persons WHERE Persons.id = ?", [person_id]).fetchall()
        self._id = person_allocate[0][0]
        self.person_name = person_allocate[0][1]
        self.person_type = person_allocate[0][2]
        self.want_housing = person_allocate[0][3]
        self.office_allocate = person_allocate[0][4]
        if person_allocate[0][5] != None:
            self.living_allocate = person_allocate[0][5]
            if new_room_name == self.living_allocate:
                print(str(self._id) + "is already allocated to " + new_room_name)

        if new_room_name == self.office_allocate:
            print(str(self._id) + "is already allocated to " + new_room_name)
        room_to_move = self.connect.execute(
            "SELECT * FROM Rooms WHERE Rooms.Name = ?", [new_room_name]).fetchall()
        print(room_to_move)
        self.room_id = room_to_move[0][0]
        self.room_name = room_to_move[0][1]
        self.room_type = room_to_move[0][2]
        if self.room_type.upper() == 'O':
            self.connect.execute("UPDATE Persons set office_accommodation = ? WHERE Persons.id = ?", [
                                 self.room_name, self._id])
            self.conn.commit()
            print(self.person_name + " successfully reallocated to " + self.room_name)

        if self.room_type.upper() == 'L':
            if self.person_type.upper() == 'FELLOW':
                if self.want_housing.upper() == 'Y':
                    update_living = self.connect.execute(
                        "UPDATE Persons set living_accomodation = ? WHERE Persons.id = ?", [self.room_name, self._id])
                    self.conn.commit()
                    print(self.person_name + " successfully reallocated to " + self.room_name)
            else:
                print(self.person_name + " not reallocated to " + self.room_name)

    def load_people(self, *args):
        load = Tk()
        load.withdraw()
        load.update()
        file = tkFileDialog.askopenfile(
            parent=load, mode='rb', title="Load file")
        if file:
            self.save_file_path(file.name)
            parser = FileParser(file.name)
            input_data = parser.read_file()
            for lines in input_data:
                print(lines)
                if len(lines) > 2:
                    name = lines[0].strip(',')
                    person_type = lines[1]
                    want_accommodation = lines[2]
                else:
                    name = lines[0]
                    person_type = lines[1]
                    want_accommodation = "N"
                self.insert_db(name=name, person_type=person_type,
                               want_accommodation=want_accommodation)
                self.allocation_rule(name, person_type, want_accommodation)

    def print_allocations(self, *args):
        """function screens data from db to the cmdline and into a file """

        self.office_allocations = self.connect.execute(
            "SELECT Persons.Name, Persons.Personnel_type, Persons.office_accommodation from Persons").fetchall()
        self.living_allocations = self.connect.execute(
            "SELECT Persons.Name, Persons.Personnel_type, Persons.living_accomodation from Persons ").fetchall()

        for items in self.office_allocations:
            item = list(items)
            if item[2] != None:
                item = map(lambda x: x.encode('ascii'), item)
                self.office_occupants.append(item)
            else:
                self.unallocated_offices.append(item)

        puts(colored.green('\n Below is list  of office personnel allocated offices: \n' ))
        officed = [ occupant for occupant in self.office_occupants]
        print('\n'.join(map(str, officed)))


        for items in self.living_allocations:
            item = list(items)
            if items[2] != None:
                item = map(lambda x: x.encode('ascii'), item)
                self.living_occupants.append(item)
            else:
                self.unallocated_houses.append(items)


        puts(colored.blue('\n Below is list of office personnel allocated houses: \n' ))
        housed = [ living for living in self.living_occupants]
        print('\n'.join(map(str, housed)))

        file = args[0]['--o']
        if file != 'None':
            filename = file
            f = open(filename, 'a+')
            # newdata = '\n'.join(map(str, officed))
            newdata = '\n'.join(map(str, housed)) + '\n' + '\n'.join(map(str, officed))
            f.write(newdata)
            f.close()
        else:
            print('No filename specificied')



    def print_unallocated(self, *args):
        allocations = self.print_allocations()
        unallocated = allocations. self.unallocated_offices
        puts(colored.red('Below is list  of office personnel unallocated offices:' '\n' ))
        for unallocated_offices in unallocated:
            personnel_officeless = unallocated_offices
        print('\n'.join(personnel_officeless))

        liv_unallocated = allocations.self.unallocated_houses
        puts(colored.green('Below is list of office personnel unallocated houses:' '\n' ))
        for unallocated_houses in liv_unallocated:
            personnel_unsheltered = unallocated_houses

        print('\n'.join(personnel_unsheltered))


        file = args[0]['--o']
        if file != 'None':
            filename = file
            f = open(filename, 'a+')
            newdata = str(personnel_officeless)
            newdata = str( personnel_unsheltered)
            f.write(newdata)
            f.close()
        else:
            print('No filename specificied')

    def print_room(self, room_name):
        """function prints out members of a room"""
        people_allocated = self.connect.execute(
            "SELECT Persons.Name from Persons WHERE office_accommodation or living_accomodation = ?", [room_name]).fetchall()
        print(str(people_allocated))

    def save_file_path(self, path):
        with open("filePath", "w+") as f:
            f.write(path)

    def load_state(self, args):
        puts(colored.green(" Data stored in the Rooms's table"))
        room_state = self.connect.execute("SELECT * FROM Rooms").fetchall()
        print('\n'.join(map(str, room_state)))
        puts(colored.blue(" Data stored in the Persons's table"))
        living_state = self.connect.execute("SELECT * FROM Persons").fetchall()
        print('\n'.join(map(str, living_state)))


def welcome_msg():
    init(strip=not sys.stdout.isatty())
    cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
    print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
          Style.DIM + '\n(type help to get a list of commands)' + Style.NORMAL)
