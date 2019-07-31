import csv
from fuzzywuzzy import fuzz
import math
from fastnumbers import fast_real


assign_dict = {}
copy_assign_dict = {}

#read in acquirer
with open('inputs/acquirer_test_list.tsv', encoding='ISO-8859-1') as tsvfile:
    reader = csv.DictReader(tsvfile, delimiter='\t')
    # id to row

    for row in reader:
        row_dict = dict(row)
        assign_dict[row_dict['acquirer_uuid']] = row_dict
        copy_assign_dict[row_dict['acquirer_uuid']] = [row_dict['acquirer_name'], row_dict['acquirer_uuid']]

remove_str = set()
#replace words with blanks
with open('generic_words/chars.csv', encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        print(row)
        remove_str.add(row[0])

replace_str = {}
with open('generic_words/replace_str.csv', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        replace_str[row[0]] = row[1]

with open('inputs/assignee.tsv', encoding='utf-8-sig') as tsvfile:
    reader = csv.DictReader(tsvfile, delimiter='\t')
    list_of_dict = {}
    
    # 'type', 'name_first', 'name_last', 'organization', 'location_id', 'city', 'state', 'country', 'latitude', longitude', 'county', 'state_fips', 'county_fips'
    
    

    
    for row in reader:
        print(reader.line_num)
        print(row)
        assignee_dict = dict(row)
        assignee_id = row['id']
        assignee_type = row['assignee_type']
        name_first = row['name_first']
        name_last = row['name_last']
        org_og = row['organization']
        org = row['organization']
        #loc_id = row['location_id']
        '''city = row['city']
        state = row['state']
        country = row['country']
        lat = row['latitude']
        lng = row['longitude']
        county = row['county']
        state_fips = row['state_fips']
        county_fips = row['country_fips']'''
        
        
        matched_name = ''
        matched_id = ''
        
        if name_first != '' and name_last != '':
            continue
        
        # replace words
        for word, rep in replace_str.items():
            org = org.replace(' ' + word + ' ', ' ' + rep + ' ')
        
        # ignore special char
        for ign in remove_str:
            org = org.replace(ign, '')
            
        
        # if there's a 99 percent string match   
        for ac_id, ac_dict in assign_dict.items():
            ac_name = ac_dict['acquirer_name']
            ac_mod = ac_dict['acquirer_name']
            
            # replace words
            for word, rep in replace_str.items():
                ac_mod = ac_mod.replace(' ' + word + ' ', ' ' + rep + ' ')
            
            # ignore special char
            for ign in remove_str:
                ac_mod = ac_mod.replace(ign, '')
          
            if fuzz.token_set_ratio(ac_mod, org) >= 99:
                if fuzz.token_set_ratio(ac_mod, org) > fuzz.token_set_ratio(matched_name, org):
                    matched_name = ac_mod
                    matched_id = ac_dict['acquirer_uuid']
                    print(matched_id)
        if matched_id != '':
            print(matched_name)
            match_list = copy_assign_dict[matched_id]
            if len(match_list) > 2:
                assignee_list = match_list[2] 
                assignee_list.append(assignee_dict)
                match_list[2] = assignee_list
                copy_assign_dict[matched_id] = match_list
            else:
                assignee_list = [assignee_dict]
                match_list.append(assignee_list)
                copy_assign_dict[matched_id] = match_list
            print(match_list)
        
                    
                    
           
            
with open('outputs/assignee_matched.tsv', 'w', newline="\n", encoding='utf-8') as out_file:
        writer = csv.writer(out_file, delimiter = '\t')
        writer.writerow(['acquirer_name', 'acquirer_uuid', 'assignee_id', 'assignee_name']) 
        for idx, match_list in copy_assign_dict.items():
            writer.writerow(match_list)                     
                     
                