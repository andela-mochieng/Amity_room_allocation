'''
Usage:
    app.py create_rooms (--office_name|--living_name)...
    app.py --version
Options:
    --version   Show version.
    --create    Create rooms
'''


from amity import Amity
from docopt import docopt





if __name__ == '__main__':
    main = Amity()
    arguments = docopt(__doc__, version='Amity Room Allocator 0.0.1')
    if arguments['create_rooms']:
        main.create_office(arguments['(--office_name|--living_name)'])


