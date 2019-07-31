from csv import DictReader

class FileLengthChecker:
    def __init__(self, file):
        
        with open(file, encoding='utf-8-sig') as csvfile:
            self.size = len([1 for row in DictReader(csvfile, delimiter=',')])
        
    def get_size(self):
        return self.size