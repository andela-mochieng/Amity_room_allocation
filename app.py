'''
Usage:
    app.py create_rooms (office_name|living_name)...
    app.py --version
Options:
    --version   Show version.
'''


from amity import Amity
from docopt import docopt

main = Amity()


def init_app():
    '''
    Returns an Amity object populated
    with all rooms
    '''
    main.create_office()
    main.create_living_space()




init_app()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Amity Room Allocator 0.0.1')
    if arguments['office_name']:
        create_office()
      

    # if arguments['living_name']:
    #     create_living_space()
