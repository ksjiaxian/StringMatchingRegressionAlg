from csv import DictReader
file = 'files/data_frame_shortened.csv'
with open(file, encoding='utf-8-sig') as csvfile:
        print(len([1 for row in DictReader(csvfile, delimiter=',')]))