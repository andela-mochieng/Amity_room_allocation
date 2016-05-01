"""Amity room allocation application has the following 
Usage:
    Amity create_rooms <room_name>...
    Amity add_person  <person_fname> <person_lname>(FELLOW|STAFF) [wants_accommodation]
    Amity reallocate_person  <person_identifier> <new_room_name> 
    Amity load_people  
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
# from termcolor import cprint
from colorama import init, Back, Style  # Fore
from docopt import docopt, DocoptExit
# from pyfiglet import figlet_format
# from db.dbase import DataManager
import sqlite3
# from clint.textui import colored, puts
from models.room import Office, Living_space
import cmd
import random

conn = sqlite3.connect("amity.sqlite")
c = conn.cursor()
c.execute(
    "CREATE TABLE IF NOT EXISTS Rooms(Name TEXT, Room_type TEXT, capacity integer, available TEXT)")
c.execute(
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
        """Usage: add_person <person_fname> <person_lname>(FELLOW|STAFF)[--wants_accommodation]"""

        add_person(arg)

    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        reallocate_person(arg)

    def do_load_people(self, arg):
        """Usage: load_person"""

        load_people(arg)

    def quit(self):
        self.root.destroy

    def do_quit(self, arg):
        """Exit application"""
        print("Amity closed")
        exit()

opt = docopt(__doc__, sys.argv[1:])


office_data = []
living_data = []
office_populate = []
living_populate = []


def create_rooms(docopt_args):
    """allows user to enter a list of room names"""

    room = docopt_args.split(' ')
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
                                    ",".join(office_data[i].available)))
        for i, k in enumerate(living_data):
            living_populate.append((living_data[i].name,
                                    living_data[i].room_type,
                                    living_data[i].capacity,
                                    ",".join(living_data[i].available)))
        if office_populate:
            for x in office_populate[0][0]:
                c.execute(
                    "INSERT INTO Rooms VALUES (?, ?, ?, ?)", (str(x), str(office_populate[0][1]), str(office_populate[0][2]), str(office_populate[0][3])))
        else:
            for x in living_populate[0][0]:
                c.execute(
                    "INSERT INTO Rooms VALUES (?, ?, ?, ?)", (str(x), str(living_populate[0][1]), str(living_populate[0][2]), str(living_populate[0][3])))
        conn.commit()


def add_person(docopt_args):
    person = docopt_args.split(' ')
    # print person # eg ['giant', 'gal', 'fellow', 'y']
    name = person[:2]
    personnel_type = person[2]
    want_accommodation = person[3]
    if personnel_type.upper() == "fellow":
        c.execute("INSERT INTO Persons VALUES (?, ?, ?)",
                  (str(name), str(personnel_type), str(want_accommodation)))
    else:
        c.execute("INSERT INTO Persons VALUES (?, ?, ?)",
                  (str(name), str(personnel_type), str(None)))

    conn.commit()

    # allocation of fellows to living_space
    if want_accommodation.upper() == "Y":
        c.execute(
            "SELECT Name, capacity, available from Rooms where Room_type = 'L' ")
        for row in c:
            spaces = row[2].split(',')
            spaces = map(lambda x: x.encode('ascii'), spaces)
            spaces = list(spaces)
            # if living space is empty
            for index, space in enumerate(spaces):
                if space == '0':
                    spaces[index] = name
                    new_spaces = " ".join(str(item) for item in spaces)
                    c.execute("UPDATE Rooms set available = ? where \
                                Name = ?", (new_spaces, row[0]))
                    conn.commit()
                    break

    if personnel_type.upper() == "STAFF" or personnel_type.upper() == "FELLOW":
        c.execute(
            "SELECT Name, capacity, available from Rooms where Room_type = 'O' ")
        for row in c:
            spaces = row[2].split(',')
            spaces = map(lambda x: x.encode('ascii'), spaces)
            spaces = list(spaces)
            for index, space in enumerate(spaces):
                if space == '0':
                    spaces[index] = name
                    new_spaces = " ".join(str(item) for item in spaces)
                    c.execute("UPDATE Rooms set available = ? where \
                                Name = ?", (new_spaces, row[0]))
                    conn.commit()
                    break
            break


def reallocate_person(docopt_args):
    pass


def load_people(docopt_args):
    load = Tk()
    load.withdraw()
    load.update()
    file = tkFileDialog.askopenfile(parent=load, mode='rb', title="Load file")
    if file:
        save_file_path(file.name)
    import ipdb
    ipdb.set_trace()
    filelines = []
    with open("file", "r+") as f:
        for line in f:
            if len(line) > 2:
                filelines.append(line.split())
    random.shuffle(filelines)

    for line in filelines:
        load_personnel = add_person(line)
        print load_personnel
        
def save_file_path(path):
    with open("filePath", "w+") as f:
        f.write(path)


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
