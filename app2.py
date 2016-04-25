'''
Usage:
    app.py create_rooms <room_type>  <room_names>...
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
        premise.create_rooms(arguments['<room_type> <room_names>'])

    # if arguments['add_person']:
    #     premise.add_person(arguments['<add_person> <FELLOW|STAFF> [wants_accommodation]>'])
# app.py add_person <add_person> <FELLOW|STAFF> [wants_accommodation]
