"""Amity room allocation application has the following 
Usage:
    Amity createrooms <room_name> <room_type>
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
from colorama import init, Fore, Back, Style
from docopt import docopt, DocoptExit
from room_model import Office, living_space
import cmd
import random


def cmd(command):
    """function creates a decorator that checks if the correct 
    commands are passed to the commandline"""

    def fn(self, args):
        try:
            """ compares commands passed with the ones in the documentation
             if not found show an error message"""
            doc = docopt(fn.__doc__, args)
        except DocoptExit as e:
            print("Invalid command passed")
            print(e)
        return command(self, doc)

        # __name__ calls the function
        fn.__name__ = command.__name__
        fn.__doc__ = command.__name__
        fn.__dict__.update(command.__dict__)
        return fn


class Amity(cmd.Cmd):
    """ this class maps how input arguments 
        are in relation to the methods """

    prompt = '(Amity): '

    @cmd
    def cmd_create_rooms(self, arg):
        """usage: createrooms <room_name> <room_type> """

        createrooms(arg)

    def quit(self):
        self.root.destroy


def welcome_msg():
    init(strip=not sys.stdout.isatty())
    cprint(figlet_format('Amity'), 'cyan', attrs=['bold'])
    print(Back.BLUE + 'Amity Room Allocation!' + Back.RESET +
          style.DIM + '\n(type help to get a list of commands)' + Style.Normal)

if doc['--launch']:
    """ start the application """
    welcome_msg()
    Amity().cmdloop()

print(doc)
