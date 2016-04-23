import pickle

class Amity(object):
    rooms = []

    def save_rooms(self, rooms):
        
        outFile = open('rooms.pkl', 'wb')
        pickle.dump(rooms, outFile)
        outFile.close()           
        return(rooms)

    def create_rooms(self, room_names):
        """ allows user to enter a list of room names """
        print room_names
        for rname in zip(room_names):
            self.rooms.append(rname)
            print rname, ' successful created'
        self.save_rooms(self.rooms)
        # self.list_rooms()
