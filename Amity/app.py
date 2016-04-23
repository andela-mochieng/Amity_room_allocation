'''
Usage:
    app.py create_rooms <create_rooms>...
    app.py --version
Options:
    --version   Show version.
'''


from amity import Amity
from docopt import docopt


def init_app():
    '''
    Returns an Amity object populated
    with all rooms
    '''
    return Amity()

if __name__ == '__main__':
    premise = init_app()
    arguments = docopt(__doc__, version='Amity Room Allocator 0.0.1')
    if arguments['create_rooms']:
        premise.create_rooms(arguments['<create_rooms>'])

    