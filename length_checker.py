from csv import DictReader
file = 'files/data_frame.csv'
with open(file, encoding='utf-8-sig') as tsvfile:
        print(len([1 for row in DictReader(tsvfile, delimiter=',')]))