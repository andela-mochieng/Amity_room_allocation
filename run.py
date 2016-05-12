"""Amity room allocation application has the following
Usage:
    Amity create_rooms <room_name>...
    Amity add_person  <first_fname> <last_name> <person_type> [--wa=n]
    Amity reallocate_person  <first_fname> <last_name> <new_room_name>
    Amity load_people
    Amity print_allocations [--o=filename]
    Amity print_unallocated [--o=filename]
    Amity print_room <room_name>
    Amity load_state <sqlite_database>
    Amity (-l | --launch)
    Amity (-h | --help)
Options:
    -l, --launch  Launch the application.
    -h,--help  display a list of command to the user
"""
import ipdb
import sys
import cmd
from app import Amity, welcome_msg
# from Room import Rooms, welcome_msg
from docopt import docopt, DocoptExit

amity = Amity()


def parser_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Amity_function_call(cmd.Cmd):
    """ this class maps how input arguments
        are in relation to the methods """

    prompt = '(Amity): '

    @parser_cmd
    def do_create_rooms(self, arg):
        """Usage: create_rooms <room_name>..."""
        amity.create_rooms(arg['<room_name>'])

    @parser_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <person_type>
        [--wa=n]"""
        amity.add_person(arg['<first_name>'], arg['<last_name>'], arg['<person_type>'], arg['--wa'])



    @parser_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <first_name> <last_name> <new_room_name>"""
        reallocate_person(arg['<first_name>'], arg['<last_name>'], arg['<new_room_name>'])

    @parser_cmd
    def do_load_people(self, arg):
        """Usage: load_person"""

        load_people(arg)

    @parser_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=allocations.txt]"""

        print_allocations(arg)

    @parser_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""

        print_unallocated(arg)

    @parser_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""

        print_room(arg)

    @parser_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""

        amity.load_state(arg)

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
    Amity_function_call().cmdloop()

print(opt)
