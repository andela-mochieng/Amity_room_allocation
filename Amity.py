"""Amity room allocation application has the following 
Usage:
    Amity create_rooms <room_name>...
    Amity add_person <person_name> <FELLOW|STAFF> [wants_accommodation]
    Amity reallocate_person <person_identifier> <new_room_name> 
    Amity load_people  # add peopleto rooms from a txt file
    Amity (-l | --launch)
    Amity (-h | --help)
Options:
    -l --launch Launch the application.
    -h --help display a list of command to the user    
"""

import sys
import cmd
from termcolor import cprint
from colorama import init, Fore, Back, Style
from docopt import docopt, DocoptExit
# from room_model import Office, living_space
# import cmd
# import random



def comd(func):
    """function creates a decorator that checks if the correct 
    commands are passed to the commandline"""

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

    @comd
    def do_create_rooms(self, arg):
        """usage: create_rooms <room_name> """

        create_rooms(arg)

    def quit(self):
        self.root.destroy

    @comd
    def do_quit(self, arg):
        """Exit application"""
        print("Amity closed")
        exit()

opt = docopt(__doc__, sys.argv[1:])


rooms = []


def create_rooms(docopt_args):
    """ allows user to enter a list of room names """
    room = "room names:", docopt_args["<rname>"]
    print room
    

def welcome_msg():
    init(strip=not sys.stdout.isatty())
    cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
    print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
          style.DIM + '\n(type help to get a list of commands)' + Style.Normal)

if opt['--launch']:
    """ start the application """
    welcome_msg()
    Amity().cmdloop()

print(opt)
