import sys
import math

##### Reading the file and saving it in a list of lists
dataset_name = sys.argv[1]
with open(dataset_name) as f:
	array = []
	for line in f:
		line = line.split()
		if line:
			str_line =  ','.join(line)
			list_line = str_line.split(',')
			array.append(list_line)
array = array[1:]
#####

##### Finding number of yes and no in the labels
Number_yes = 0
Number_no = 0
Total_labels = len(array)
for i in xrange(0,Total_labels):
	if array[i][-1] =='yes' or array[i][-1] == "A":
		Number_yes += 1
	else:
		Number_no += 1
#####		

##### Finding Entropy and Error Rate
prob_negative = (Number_no*1.0/Total_labels)
prob_positive = (Number_yes*1.0/Total_labels)
entropy = -prob_negative*math.log(prob_negative,2) - prob_positive*math.log(prob_positive,2)
error_rate = min(Number_no,Number_yes)*1.0/Total_labels

print "entropy:", round(entropy,3) 
print "error:", round(error_rate,2)

#####



