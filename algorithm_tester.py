import csv
import create_model
import math

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

test_file = 'files/data_frame_test.csv'
size = 0

data = 'files/data_frame_shortened.csv'
model = create_model.Model(data)

correct_num = 0
best_threshold = 0.0
best_percentage_correct = 0.0

for i in range(1000):
    print(i)
    threshold = float(i) / 1000

    with open(test_file, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
    
        for row in reader:
            size += 1
            is_match = int(row['is_match']) == 1
            
            string1 = row['acquirer_name']
            string2 = row['assignee_name']
            
            match = model.is_match(string1, string2, threshold)
            
            if (is_match and match) or (not is_match and not match):
                correct_num += 1
            
        percent_correct = float(correct_num) / size
        
        if percent_correct > best_percentage_correct:
            best_threshold = threshold
            best_percentage_correct = percent_correct
            
            
print('Best Threshold: ' + str(best_threshold))
print(str(truncate(best_percentage_correct * 100, 3)) + '% correct') 