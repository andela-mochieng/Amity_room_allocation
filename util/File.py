class fileParser(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        """read content of the file and return a list"""
        allocations_list = []
        lines = [line.rstrip('\n') for line in open(self.file_path, 'r')]
        for line in lines:
            words = line.split(" ")
            name = words[0].replace("'", "") + " " + words[1].replace("'", "")
            personnel_type = words[2]
            want_accommodation = 'N'
            if len(words) == 4:
                want_accommodation = 'Y'
            allocations_list.append(
                [name, personnel_type, want_accommodation])
        return allocations_list
