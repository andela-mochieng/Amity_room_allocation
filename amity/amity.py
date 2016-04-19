""" Amity room allocation application has the following 
Usage:
Amity createrooms
"""
from docopt import docopt, DocoptExit
from . import Offices, living_space
import cmd

class Amity(cmd.Cmd):
    """ this class maps how input arguments 
    are in relation to the methods """


def create_rooms(self, arg):
    """usage: createrooms"""
