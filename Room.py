import sqlite3
from db.d_base import Dbase_centre
from models.room import Office, Living_space
from colorama import init
import sys
import ipdb

conn = sqlite3.connect("amity.sqlite")
connection = conn.cursor()

class Rooms(object):
    # classs variables

    def create_rooms(self, args):
        """functions takes multiple rooms of the
        same kind and store them in a db"""
        office_data = []
        living_data = []
        office_populate = []
        living_populate = []

        room_list = [room for room in args['room_name']]
        room_type = raw_input(
            "Enter room type: \n O: Office space \n L: Living space: \n")

        while room_type != "O" and room_type != "L":
            room_type = raw_input(
                "Try again. Enter Room Type:\n O: Office space \n L: Living space: \n")

        rooms = {room_type: room_list}
        print rooms
        for key, values in rooms.iteritems():
            for index, value in enumerate(values):
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

            db = Dbase_centre('amity.sqlite')

            query = 'INSERT INTO Rooms VALUES (?, ?, ?, ?)'
            if office_populate:
                off_record = []

                for x in office_populate[0][0]:
                    temp_tuple = (
                        str(x),
                        str(office_populate[0][1]),
                        str(office_populate[0][2]),
                        str(office_populate[0][3]))
                    off_record.append(temp_tuple)

                if db.query_db(query, off_record):
                    print 'New rooms created'
                else:
                    print'Duplicate entries: A room with that exists'

            else:
                for x in living_populate[0][0]:
                    liv_record = []
                    tem_tuple = (
                        str(x),
                        str(living_populate[0][1]),
                        str(living_populate[0][2]),
                        str(living_populate[0][3]))
                    liv_record.append(tem_tuple)
                if db.query_db(query, liv_record):
                    print 'New rooms created'
                else:
                    print'Duplicate entries: A room with that exists'


class Person():

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

def welcome_msg():
    init(strip=not sys.stdout.isatty())
# cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
# print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
# Style.DIM + '\n(type help to get a list of commands)'
# + Style.NORMAL)
