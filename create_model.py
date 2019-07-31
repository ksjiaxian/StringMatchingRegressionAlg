from pandas import DataFrame
import csv
from sklearn import linear_model
import math
from fuzzywuzzy import fuzz

class Model:
    def __init__(self, data):

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
                
        self.size = len(simple_ratio)
        
        matching_data = {'is_match': is_match, 'simple_ratio': simple_ratio, 'partial_ratio': partial_ratio, 
                         'sort_ratio': sort_ratio, 'set_ratio': set_ratio, 'simple*partial': simple_partial,
                         'simple*sort': simple_sort, 'simple*set': simple_set, 'partial*sort': partial_sort,
                         'partial*set': partial_set, 'sort*set': sort_set, 'simple^2': simple2, 
                         'partial^2': partial2, 'sort^2':sort2, 'set^2': set2}
            
        df = DataFrame(matching_data, columns = ['is_match', 'simple_ratio', 'partial_ratio', 'sort_ratio', 'set_ratio', 'simple*partial',
                      'simple*sort', 'simple*set', 'partial*sort', 'partial*set', 'sort*set', 'simple^2', 'partial^2', 'sort^2', 'set^2'])
        
        var_names = ['simple_ratio', 'partial_ratio', 'sort_ratio', 'set_ratio', 'simple*partial', 'simple*sort', 'simple*set', 
                'partial*sort', 'partial*set', 'sort*set', 'simple^2', 'partial^2', 'sort^2', 'set^2']
        
        X = df[var_names] 
        Y = df['is_match']
         
        # with sklearn
        regr = linear_model.LogisticRegression(solver='lbfgs')
        regr.fit(X, Y)

        print('Model Specifications:')
        print()
        print('Intercept:')
        print(regr.intercept_[0])
        print()
        
        coefficients = list(list(regr.coef_)[0])
        coeff_string = ''
        for i in range(len(var_names)):
            var = var_names[i]
            co = coefficients[i]
            coeff_string += str(var) + ': ' + str(co) + '\n'
            
        print('Coefficients:')
        print(coeff_string)
        print('R^2:')
        print(regr.score(X, Y))
        print()
        print('R:')
        print(math.sqrt(regr.score(X, Y)))
        print()
        
        self.model = regr
        
    def make_prediction(self, string1, string2):
            #singular variables
            simple_ratio = float(fuzz.ratio(string1, string2)) / 100
            partial_ratio = float(fuzz.partial_ratio(string1, string2)) / 100
            sort_ratio = float(fuzz.token_sort_ratio(string1, string2)) / 100
            set_ratio = float(fuzz.token_set_ratio(string1, string2)) / 100
            
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
            
            sample = [[simple_ratio, partial_ratio, sort_ratio, set_ratio,simple_partial, simple_sort, simple_set, partial_sort, partial_set, sort_set, simple2, partial2, sort2, set2]]
            
            return self.model.predict_proba(sample)[:,1]
        
    def is_match(self, string1, string2, threshold):
        confidence = self.make_prediction(string1, string2)
        return confidence > threshold
        
    def test(self, test):
        return self.model.predict_proba(test)[:,1]