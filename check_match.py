import csv
import length_checker

checked_file = 'outputs/patent_matches.tsv'
orbis = 'inputs/orbis.tsv'
test_file = 'inputs/acquirer_test_list.tsv'
output_file_orbis_check = 'outputs/orbis_check.tsv'
output_file_test_check = 'outputs/test_check.tsv'

def check_orbis():
    orbis_dict = {}
    #returns a dictionary from acquiring company to set of subsidiary and city pairs
    with open(orbis, encoding='utf-8-sig') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
    
        for row in reader:
            acquirer = row['acquirer_name'].lower()
            subsidiary = row['subsidiary_branch_name'].lower()
            city = row['subsidiary_branch_city'].lower()
            
            if acquirer in orbis_dict:
                orbis_dict[acquirer].append((subsidiary, city))
            else:
                orbis_dict[acquirer] = [(subsidiary, city)]
                
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

def check_input_file():
    input_dict = {}
    
    #returns a dictionary from subsidiary to acquiring company
    with open(checked_file, encoding='ISO-8859-1') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
    
        for row in reader:
            acquirer = row['acquirer_name']
            assignee = row['assignee_name']
            
            if acquirer in input_dict:
                input_dict[acquirer].add(assignee)
            else:
                input_dict[acquirer] = set()
                input_dict[acquirer].add(assignee)
                
    return test_dict

if __name__ == '__main__':
    orbis_dict = check_orbis()
    test_dict = check_test_file()
    input_dict = check_input_file()
    
    input_file_size = length_checker.FileLengthChecker(checked_file).get_size()
    
    #read the file to be checked
    orbis_incorrect_cnt = 0
    #check with orbis
    with open(checked_file, encoding='csv-utf-8') as tsvfile:
        with open(output_file_orbis_check, 'w', newline="\n", encoding='utf-8-sig') as out_file: 
            csv_writer = csv.writer(out_file, delimiter=',')
            header = ['acquirer_name', 'assignee_name', 'city', 'country']
            csv_writer.writerow(header)
            
            reader = csv.DictReader(tsvfile, delimiter='\t')
        
            for row in reader:
                acquirer = row['acquirer_name']
                assignee = row['assignee_name']
                city = row['city']
                country = row['country']
                
                set_of_subs = orbis_dict[acquirer]
                
                if not (assignee.lower(), city.lower()) in set_of_subs:
                    csv_writer.writerow([acquirer, assignee, city, country])
                    orbis_incorrect_cnt += 1
                    
    print('Percentage of input file that is not in Orbis: ' + str(float(orbis_incorrect_cnt) / input_file_size))
                
    test_file_size = length_checker.FileLengthChecker(test_file).get_size()
    
    test_incorrect_cnt = 0
    #check with the test file
    with open(test_file, encoding='csv-utf-8') as tsvfile:
        with open(output_file_test_check, 'w', newline="\n", encoding='utf-8-sig') as out_file: 
            csv_writer = csv.writer(out_file, delimiter=',')
            header = ['acquirer_name', 'assignee_name']
            csv_writer.writerow(header)
            
            reader = csv.DictReader(tsvfile, delimiter='\t')
        
            for row in reader:
                acquirer = row['acquirer_name']
                assignee = row['assignee_name']
                
                set_of_assignees = test_dict[acquirer]
                
                if not assignee in set_of_assignees:
                    csv_writer.writerow([acquirer, assignee])
                    test_incorrect_cnt += 1
                    
    print('Percentage of the test file that is not in the input file: ' + str(float(test_incorrect_cnt) / test_file_size))
    
                
            