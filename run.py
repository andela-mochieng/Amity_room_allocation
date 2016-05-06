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
from app import *


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
        """Usage: add_person <persargon_fname> <person_lname>(FELLOW|STAFF)
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

if opt['--launch']:
    """ start the application """
    welcome_msg()
    Amity().cmdloop()

print(opt)
