import csv

checked_file = 'outputs/patent_matches.tsv'
orbis = 'inputs/orbis.tsv'
test_file = 'inputs/acquirer_test_list.tsv'

def check_orbis():
    orbis_dict = {}
    #returns a dictionary from subsidiary to acquiring company
    with open(orbis, encoding='csv-utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
    
        for row in reader:
            acquirer = row['acquirer_name']
            subsidiary = row['subsidiary_branch_name']
            
            if subsidiary in orbis_dict:
                
            
            
    
def check_test_file():
    #returns a dictionary from alias to acquiring company
    with open(orbis, encoding='csv-utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
    
        for row in reader:


if __name__ == '__main__':
    #read the input file
    with open(checked_file, encoding='csv-utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
    
        for row in reader:
            acquirer = row['acquirer_name']
            assignee = row['assignee_name']
            city = row['city']
            country = row['country']