
class Room(object):
    """Room is the parent and Office and Living_space inherit from it"""

    def __init__(self, connection):
        '''Connection is used to connect to the cursor object so thatthe is_room_filled method works'''
        self.connect = connection

    def is_room_filled(self, room_name):
        count = self.connect.execute(
            "SELECT COUNT(*) AS office_occupants FROM Persons  WHERE Persons.office_accommodation = ?", [str(room_name)]).fetchall()

        return count[0][0] > self.capacity


class Office(Room):
    """office model has capacity of 6"""
    room_type = 'O'
    capacity = 6


class LivingSpace(Room):
    """Living_space model with a capacity of 4 """
    room_type = 'L'
    capacity = 4
