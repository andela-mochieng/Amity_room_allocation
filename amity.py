"""Amity room allocation application has the following
Usage:
    Amity create_rooms <room_name>...
    Amity add_person  <person_fname> <person_lname>(FELLOW|STAFF) [--want_accommodation=n]
    Amity reallocate_person  <person_identifier> <new_room_name>
    Amity load_people
    Amity print_allocations [-o=filename]
    Amity print_unallocated [-o=filename]
    Amity print_room <room_name>
    Amity load_state <sqlite_database>
    Amity (-l | --launch)
    Amity (-h | --help)
Options:
    -l, --launch  Launch the application.
    -h,--help  display a list of command to the user
"""

import sys
import cmd
from Tkinter import Tk
import tkFileDialog
from util.File import fileParser
# from termcolor import cprint
from colorama import init, Back, Style  # Fore
from docopt import docopt, DocoptExit
# from pyfiglet import figlet_format
import sqlite3
from clint.textui import colored, puts
from models.room import Office, Living_space
import cmd
import random

conn = sqlite3.connect("amity.sqlite")
connection = conn.cursor()
connection.execute(
    "CREATE TABLE IF NOT EXISTS Rooms(Name TEXT, Room_type TEXT, capacity integer, available TEXT)")
connection.execute(
    "CREATE TABLE IF NOT EXISTS Persons(Name TEXT, Personel_type TEXT, want_accommodation TEXT)")


def comd(func):
    """function creates a decorator that checks if
    he correct commands are passed to the commandline"""

    def fn(self, arg):
        try:
            """ compares commands passed with the ones in the documentation
             if not found show an error message"""
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            print("Invalid command passed")
            print(e)
            return

        except SystemExit:
            return
        return func(self, opt)

    # __name__ calls the function
    fn.__name__ = func.__name__
    fn.__doc__ = func.__name__
    fn.__dict__.update(func.__dict__)
    return fn


class Amity(cmd.Cmd):
    """ this class maps how input arguments
        are in relation to the methods """

    prompt = '(Amity): '

    def do_create_rooms(self, arg):
        """Usage: create_rooms <room_name>"""

        create_rooms(arg)

    def do_add_person(self, arg):
        """Usage: add_person <person_fname> <person_lname>(FELLOW|STAFF)
        [--wants_accommodation=n]"""

        add_person(arg)

    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        reallocate_person(arg)

    def do_load_people(self, arg):
        """Usage: load_person"""

        load_people(arg)

    def do_print_allocations(self, arg):
        """Usage: print_allocations [-o=filename]"""

        print_allocations(arg)

    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [-o=filename]"""

        print_unallocated(arg)

    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""

        print_room(arg)

    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""

        load_state(arg)

    def quit(self):
        self.root.destroy

    def do_quit(self, arg):
        """Exit application"""
        print("Amity closed")
        exit()

opt = docopt(__doc__, sys.argv[1:])

# variables used in create_rooms
office_data = []
living_data = []
office_populate = []
living_populate = []
# variables used in add_person
name = ""
personnel_type = ""
want_accommodation = ""

# variables used in print_allocation function
room_name = ""
room_type = ""
people_room = ""
people_in_room = []
# variables used in print_allocation function
person_name = []
person_type = ""
person_accommodate = ""


def create_rooms(docopt_args):
    """allows user to enter a list of room names specifying
        whether office or living spaces"""

    room = docopt_args.split(' ')
    room_type = raw_input(
        "Enter room type: \n O: Office space \n L: Living space: \n")

    while room_type != "O" and room_type != "L":
        room_type = raw_input(
            "Try again. Enter Room Type:\n O: Office space \n L: Living space: \n")
    rooms = {room_type: room}

    for key, values in rooms.iteritems():
        for value, index in enumerate(values):
            if key.upper() == "O":
                office_data.append(Office(values))
            else:
                living_data.append(Living_space(values))

        for i, k in enumerate(office_data):
            office_populate.append((office_data[i].name,
                                    office_data[i].room_type,
                                    office_data[i].capacity,
                                    office_data[i].available))
        for i, k in enumerate(living_data):
            living_populate.append((living_data[i].name,
                                    living_data[i].room_type,
                                    living_data[i].capacity,
                                    living_data[i].available))
        if office_populate:
            for x in office_populate[0][0]:
                state = "INSERT INTO Rooms VALUES {} {} {} {}".format(
                    str(x), str(office_populate[0][1]),
                    str(office_populate[0][2]),
                    str(office_populate[0][3]))
                connection.execute(state)
        else:
            for x in living_populate[0][0]:
                statement = "INSERT INTO Rooms VALUES {} {} {} {}".format(
                    str(x), str(living_populate[0][1]),
                    str(living_populate[0][2]),
                    str(living_populate[0][3])
                )
                connection.execute(statement)
        conn.commit()
        return rooms


def allocate(**kwargs):
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

    if kwargs['want_accommodation'].upper() == 'Y':
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


def add_person(docopt_args):
    person = docopt_args.split(' ')
    # eg ['giant', 'gal', 'fellow', 'y']
    name = person[0] + " " + person[1]
    personnel_type = person[2]
    want_accommodation = person[3]

    insert_db(name=name, personnel_type=personnel_type,
              want_accommodation=want_accommodation)
    allocate(name=name, personnel_type=personnel_type,
             want_accommodation=want_accommodation)

    # allocation of fellows to living_space


def insert_db(**kwargs):
    if kwargs['personnel_type'].upper() is "FELLOW" or "STAFF":
        connection.execute("INSERT INTO Persons VALUES (?, ?, ?)",
                           (str(kwargs['name']), str(kwargs['personnel_type']),
                            str(kwargs['want_accommodation'])))
        conn.commit()


def reallocate_person(docopt_args):
    person_room = docopt_args.split(' ')
    person = person_room[:2]
    exists = False
    connention.execute(
        "SELECT Name, capacity, available FROM Rooms where Room_type = 'L' or 'O'")
    for row in connection:
        list_spaces = row[2].encode('ascii').split(',')
        if name in list_spaces:
            exists = True
            break
    if exists is False:
        unallocated_persons.append(name)


def load_people(docopt_args):
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


def print_allocations(docopt_args):
    """function screens data  from db to the cmdline and into a file """
    allocate = docopt_args.split(' ')
    connection.execute(
        "SELECT Name, Room_type, available from Rooms")
    """(u'lilac', u'O', u'lions sheila kiura alex margie 
    johns mtu mzima mtu mzima wacha tu')"""
    for i in connection:
        i = map(lambda x: x.encode('ascii'), i)
        room_name = i[0]
        room_type = i[1]
        people_room = i[2]
        print "-" * 30
        puts(colored.red(room_name))
        print "-" * 30
        puts(colored.white(room_type))
        print "-" * 3
        puts(colored.blue(people_room))

        people_in_room.append(people_room)
        if len(allocate) > 0:
            filename = allocate[-1]
            f = open(filename, 'a+')
            newdata = room_name + "', '" + \
                room_type + "', '" + people_room + '\n'
            f.write(newdata)
        else:
            print('No filename specificied')


def print_room(docopt_args):
    """function prints out members of a room"""
    room = docopt_args.split(' ')
    connection.execute(
        "SELECT Name, available from Rooms where Name = ?", (room))
    for allocated in connection:
        allocated = map(lambda x: x.encode('ascii'),
                        allocated)
        return puts(colored.blue(allocated[1]))
    print('No room with that name')


def print_unallocated(docopt_args):
    people_org = []
    unallocate = docopt_args.split(' ')
    connection.execute(
        "SELECT available from Rooms")
    for people_room in connection:
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
    # print people_org
    # import ipdb
    # ipdb.set_trace()
    for name in people_org:
        for names in people_in_room:
            if name in names == False and person_accommodate.upper() is 'N':
                puts(colored.white(person_name) + " " +
                     colored.red(person_type) + " " +
                     colored.blue(person_accommodate))
    print "Everyone allocated"

    if len(unallocate) > 0:
        filename = unallocate[-1]
        f = open(filename, 'a+')
        newdata = person_name + "', '" + \
            person_type + "', '" + person_accommodate + '\n'
        f.write(newdata)
    else:
        print('No filename specificied')


def save_file_path(path):
    with open("filePath", "w+") as f:
        f.write(path)


def load_state(docopt_args):
    connection.execute("SELECT * FROM Rooms")
    print connection.fetchall()
    connection.execute("SELECT * FROM Persons")
    print connection.fetchall()


def welcome_msg():
    init(strip=not sys.stdout.isatty())
    # cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
    # print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
    # Style.DIM + '\n(type help to get a list of commands)' + Style.NORMAL)

if opt['--launch']:
    """ start the application """
    welcome_msg()
    Amity().cmdloop()

print(opt)
