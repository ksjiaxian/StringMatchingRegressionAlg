import csv
from fuzzywuzzy import fuzz
import random

input_file = 'inputs/acquirer_test_list.tsv'
output_file = 'files/data_frame_test.csv'

#keep track of all the aliases and subsidiaries for a given company
other_names = {}

#read in acquirer
#create real matches
with open(output_file, 'w', newline="\n", encoding='utf-8-sig') as out_file: 
    csv_writer = csv.writer(out_file, delimiter=',')
    header = ['acquirer_name', 'assignee_name', 'is_match', 'simple_ratio', 'partial_ratio', 'sort_ratio', 'set_ratio', 'simple*partial',
              'simple*sort', 'simple*set', 'partial*sort', 'partial*set', 'sort*set', 'simple^2', 'partial^2', 'sort^2', 'set^2']
    csv_writer.writerow(header)
    
    with open(input_file, encoding='ISO-8859-1') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
    
        for row in reader:
            row_dict = dict(row)
            acquirer = row['acquirer_name']
            assignee = row['assignee_name']
            
            if acquirer in other_names:
                other_names[acquirer].add(assignee)
            else:
                other_names[acquirer] = {assignee}
            
            #singular variables
            simple_ratio = float(fuzz.ratio(acquirer, assignee)) / 100
            partial_ratio = float(fuzz.partial_ratio(acquirer, assignee)) / 100
            sort_ratio = float(fuzz.token_sort_ratio(acquirer, assignee)) / 100
            set_ratio = float(fuzz.token_set_ratio(acquirer, assignee)) / 100
            
            #cross-interaction variables
            simple_partial = simple_ratio * partial_ratio
            simple_sort = simple_ratio * sort_ratio
            simple_set = simple_ratio * set_ratio
            partial_sort = partial_ratio * sort_ratio
            partial_set = partial_ratio * set_ratio
            sort_set = sort_ratio * set_ratio
            
            #higher degree terms
            simple2 = simple_ratio ** 2
            partial2 = partial_ratio ** 2
            sort2 = sort_ratio ** 2
            set2 = set_ratio ** 2
            
            csv_writer.writerow([acquirer, assignee, '1', simple_ratio, partial_ratio, sort_ratio, set_ratio,
                                 simple_partial, simple_sort, simple_set, partial_sort, partial_set, sort_set,
                                 simple2, partial2, sort2, set2])
            
print(len(other_names))


#create non-matches
with open(output_file, 'a', newline="\n", encoding='utf-8-sig') as out_file: 
    csv_writer = csv.writer(out_file, delimiter=',')
    cnt = 0
    # for each acquirer pair with all assignees of other acquirers
    for acquirer, assignees in other_names.items():
        cnt += 1
        print(float(cnt) / 702)
        
        #set of other acquirers
        other_acquirers = set(other_names.keys()).copy()
        other_acquirers.remove(acquirer)
        
        for other_acquirer in other_acquirers:
            for assignee_of_other_acquirer in other_names[other_acquirer]:
                #use this line of code to help reduce the number of non-match data points
                if random.random() < .998:
                    continue
                #singular variables
                simple_ratio = float(fuzz.ratio(acquirer, assignee_of_other_acquirer)) / 100
                partial_ratio = float(fuzz.partial_ratio(acquirer, assignee_of_other_acquirer)) / 100
                sort_ratio = float(fuzz.token_sort_ratio(acquirer, assignee_of_other_acquirer)) / 100
                set_ratio = float(fuzz.token_set_ratio(acquirer, assignee_of_other_acquirer)) / 100
                
                #cross-interaction variables
                simple_partial = simple_ratio * partial_ratio
                simple_sort = simple_ratio * sort_ratio
                simple_set = simple_ratio * set_ratio
                partial_sort = partial_ratio * sort_ratio
                partial_set = partial_ratio * set_ratio
                sort_set = sort_ratio * set_ratio
                
                #higher degree terms
                simple2 = simple_ratio ** 2
                partial2 = partial_ratio ** 2
                sort2 = sort_ratio ** 2
                set2 = set_ratio ** 2
            
                csv_writer.writerow([acquirer, assignee_of_other_acquirer, '0', simple_ratio, partial_ratio, sort_ratio, set_ratio,
                                 simple_partial, simple_sort, simple_set, partial_sort, partial_set, sort_set,
                                 simple2, partial2, sort2, set2])
                
            
        