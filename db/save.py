import sqlite3
from models.room import Office, Living_space
import ipdb

class Save_data(object):
    def __init__(self):
        self.conn = sqlite3.connect("amity.sqlite")
        self.connect = self.conn.cursor()
        self.create_tables()


    def create_tables(self):
        """creates tables if non_exists"""
        with self.conn:
            self.connect.execute(
                "CREATE TABLE IF NOT EXISTS Rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, type TEXT, capacity integer)")

            self.connect.execute(
                "CREATE TABLE IF NOT EXISTS Persons(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Personel_type TEXT, want_accommodation TEXT, office_accommodation TEXT , living_accomodation TEXT)")



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
