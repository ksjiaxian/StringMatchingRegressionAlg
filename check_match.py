import csv

checked_file = 'outputs/patent_matches.tsv'
orbis = 'inputs/orbis.tsv'
test_file = 'inputs/acquirer_test_list.tsv'
output_file_orbis_check = 'outputs/orbis_check.tsv'
output_file_test_check = 'outputs/test_check.tsv'

def check_orbis():
    orbis_dict = {}
    #returns a dictionary from subsidiary to acquiring company
    with open(orbis, encoding='utf-8-sig') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
    
        for row in reader:
            acquirer = row['acquirer_name']
            subsidiary = row['subsidiary_branch_name']
            city = row['subsidiary_branch_city']
            
            if subsidiary in orbis_dict:
                if city in orbis_dict[subsidiary]:
                    continue
                else:
                    orbis_dict[subsidiary][city] = acquirer
            else:
                orbis_dict[subsidiary] = {}
                orbis_dict[subsidiary][city] = acquirer
                
    return orbis_dict
                
def check_test_file():
    test_dict = {}
    #returns a dictionary from subsidiary to acquiring company
    with open(test_file, encoding='ISO-8859-1') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
    
        for row in reader:
            acquirer = row['acquirer_name']
            assignee = row['assignee_name']
            
            if assignee in orbis_dict:
                continue
            else:
                test_dict[assignee] = acquirer
                
    return test_dict

if __name__ == '__main__':
    orbis_dict = check_orbis()
    test_dict = check_test_file()
    print('Orbis dictionary size: ' + str(len(orbis_dict)))
    print('Test Input dictionary size: ' + str(len(test_dict)))
    
    #read the file to be checked
    
    #check with orbis
    with open(checked_file, encoding='csv-utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
    
        for row in reader:
            acquirer = row['acquirer_name']
            assignee = row['assignee_name']
            city = row['city']
            country = row['country']
            
            #TODO: implement exactly what will be checked, and how to record it
            
    #check with the test file
    with open(checked_file, encoding='csv-utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
    
        for row in reader:
            acquirer = row['acquirer_name']
            assignee = row['assignee_name']
            city = row['city']
            country = row['country']
            
            #TODO: implement exactly what will be checked, and how to record it