import numpy as np
from pandas import DataFrame
import csv

data = 'files/data_frame.csv'

#is it a match 
is_match = []

#singular variables
simple_ratio = []
partial_ratio = []
sort_ratio = []
set_ratio = []

#cross-interaction variables
simple_partial = []
simple_sort = []
simple_set = []
partial_sort = []
partial_set = []
sort_set = []

#higher degree terms
simple2 = []
partial2 = []
sort2 = []
set2 = []
            
with open(data, encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    
    for row in reader:
        is_match.append(float(row['is_match']))
        simple_ratio.append(float(row['simple_ratio']))
        partial_ratio.append(float(row['partial_ratio']))
        sort_ratio.append(float(row['sort_ratio']))
        set_ratio.append(float(row['set_ratio']))
        
        #cross-interaction variables
        simple_partial.append(float(row['simple*partial']))
        simple_sort.append(float(row['simple*sort']))
        simple_set.append(float(row['simple*set']))
        partial_sort.append(float(row['partial*sort']))
        partial_set.append(float(row['partial*set']))
        sort_set.append(float(row['sort*set']))
        
        #higher degree terms
        simple2.append(float(row['simple^2']))
        partial2.append(float(row['partial^2']))
        sort2.append(float(row['sort^2']))
        set2.append(float(row['set^2']))
        
print(len(simple_ratio))
print(len(partial_ratio))
print(len(sort_ratio))
print(len(set_ratio))

matching_data = {'is_match': is_match, 'simple_ratio': simple_ratio, 'partial_ratio': partial_ratio, 
                 'sort_ratio': sort_ratio, 'set_ratio': set_ratio, 'simple*partial': simple_partial,
                 'simple*sort': simple_sort, 'simple*set': simple_set, 'partial*sort': partial_sort,
                 'partial*set': partial_set, 'sort*set': sort_set, 'simple^2': simple2, 
                 'partial^2': partial2, 'sort^2':sort2, 'set^2': set2}
    
df = DataFrame(matching_data, columns = ['is_match', 'simple_ratio', 'partial_ratio', 'sort_ratio', 'set_ratio', 'simple*partial',
              'simple*sort', 'simple*set', 'partial*sort', 'partial*set', 'sort*set', 'simple^2', 'partial^2', 'sort^2', 'set^2'])
print(df)
print()
print(df.info())
print()
print(df.corr(method = 'pearson'))