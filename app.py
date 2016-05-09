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

conn = sqlite3.connect("amity.sqlite")
connection = conn.cursor()
connection.execute(
    "CREATE TABLE IF NOT EXISTS Rooms(Name TEXT, Room_type TEXT, capacity integer, available TEXT)")
connection.execute(
    "CREATE TABLE IF NOT EXISTS Persons(Name TEXT, Personel_type TEXT, want_accommodation TEXT)")


def create_rooms(args):
    """allows user to enter a list of room names specifying
        whether office or living spaces"""

    room = [room for room in args['<room_name>']]
    room_type = raw_input(
        "Enter room type: \n O: Office space \n L: Living space: \n")

    while room_type != "O" and room_type != "L":
        room_type = raw_input(
            "Try again. Enter Room Type:\n O: Office space \n L: Living space: \n")
    rooms = {room_type: room}
    print rooms
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
                connection.execute(
                    "INSERT INTO Rooms VALUES (?, ?, ?, ?)", (
                        str(x),
                        str(office_populate[0][1]),
                        str(office_populate[0][2]),
                        str(office_populate[0][3])))

        else:
            for x in living_populate[0][0]:
                connection.execute(
                    "INSERT INTO Rooms VALUES (?, ?, ?, ?)", (
                        str(x),
                        str(living_populate[0][1]),
                        str(living_populate[0][2]),
                        str(living_populate[0][3])))

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


def add_person(args):
    name = args['<person_fname>'] + " " + args['<person_lname>']
    personnel_type = 'FELLOW' if args['FELLOW'] else 'STAFF'
    want_accommodation = 'Y' if args[
        '--wa'] is not None and args['--wa'].lower() == 'y' else 'N'
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


def reallocate_person(args):
    fname = args.get('<person_fname>')
    lname = args.get('<person_lname>')
    reallocate_details = fname + " " + lname
    connection.execute(
        "DELETE from Rooms where available = ?", [reallocate_details])
    room = args.get('<new_room_name>')
    ipdb.set_trace()
    connection.execute(
        "UPDATE Rooms SET available = ? WHERE Name = ?",
        [reallocate_details, room])


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
