class FileParser(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        """Read content of the file and return a list"""
        allocations_list = []
        lines = [line.rstrip('\n') for line in open(self.file_path, 'r')]
        for line in lines:
            words = line.split(" ")
            name = words[0] + " " + words[1]
            personnel_type = words[2]
            if len(words) == 4:
                want_accommodation = words[3]
            else:
                want_accommodation = 'N'

            allocations_list.append(
                [name, personnel_type, want_accommodation])
        return len(allocations_list)
