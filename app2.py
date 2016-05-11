''' room_data = {'O':['lilac', 'valhalla', 'camelot', 'krypton', 'oculus'],'L': ['Ruby', 'Emerald', 'Jade', 'shell', 'java']}

people_data = {'staff':['Cory Swanson', 'Kim Harmon', 'Judy Powell', 'Wiseman Said', 'Brian Idambo','Simon Giks', 'Joe Gikera'],'Fellow':[{'Margie rain':'y'},{'John kariuki':'N'},{'stanely ndagi':'y'},{'susu hajidi':'y'}]}

allocates = {
    'O': { 'lilac':['0','1','2','3','4','5'], 'valhalla':['6','7','8','9','10','11'], 'camelot':['12','13','14','15','16','17']},
    'L': {'Ruby':['0','1','2','3'], 'Emerald':['4','5','6','7'], 'Jade':['8','9','10','11'], 'shell':['12','13','14','15']}
}


'''
from app import *
class Amity(object):

    def __init__(self):
        self.room_data = {}
        self.people_data = {}
        self.allocations = {}

        self.office_data = []
        self.living_data = []
        self.office_populate = []
        self.living_populate = []
        # variables used in add_person
        self.name = ""
        self.personnel_type = ""
        self.want_accommodation = ""

        # variables used in print_allocation function
        self.room_name = ""
        self.room_type = ""
        self.people_room = ""
        self.people_in_room = []
        # variables used in print_allocation function
        self.person_name = []
        self.person_type = ""


    def create_room(self, room):
        pass

 for key, values in self.rooms.iteritems():
            for value, index in enumerate(values):
                if key.upper() == "O":
                    office_data.append(Office(values))
                else:
                    living_data.append(Living_space(values))

            for i, k in enumerate(office_data):
                self.office_populate.append((office_data[i].name,


        fice_data[i].room_type,

        self.people_data = {'staff':[],
        'Fellow':[{}]
        }
                                            office_data[i].capacity,
                                            office_data[i].available))
            for i, k in enumerate(living_data):
                self.living_populate.append((living_data[i].name,
                                            living_data[i].room_type,
                                            living_data[i].capacity,
                                            living_data[i].available))
            if self.office_populate:
                for x in self.office_populate[0][0]:
                    self.connection.execute(
                        "INSERT INTO Rooms VALUES (?, ?, ?, ?)", (
                            str(x),
                            str(self.office_populate[0][1]),
                            str(self.office_populate[0][2]),
                            str(self.office_populate[0][3])))

            else:
                for x in self.living_populate[0][0]:
                    self.connection.execute(
                        "INSERT INTO Rooms VALUES (?, ?, ?, ?)", (
                            str(x),
                            str(self.living_populate[0][1]),
                            str(self.living_populate[0][2]),
                            str(self.living_populate[0][3])))

            self.conn.commit()
            return rooms