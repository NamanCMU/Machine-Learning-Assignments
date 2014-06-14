import itertools
import time
import sys

start = time.time()
### Reading Training Data from '9Cat-Train.labeled' file
with open('4Cat-Train.labeled') as f:
	training_set = []
	for line in f:
		line = line.split()
		temparray = []	
		for i in xrange(0,len(line),2):
			temparray.append(line[i+1])
		training_set.append(temparray)
#print 'Training Set: ', training_set
###

### Reading Testing Data 
testfile = sys.argv[1]
with open(testfile) as f:
	testing_set = []
	for line in f:
		line = line.split()
		temparray = []	
		for i in xrange(0,len(line),2):
			temparray.append(line[i+1])
		testing_set.append(temparray)
#print 'Testing Set: ', testing_set
###

#### Generating Input Space
Gender = ['Male','Female']
Age = ['Young','Old']
Student = ['Yes','No']
PreviouslyDeclined =  ['Yes','No']

List1 = ["".join(seq) for seq in itertools.product("01", repeat=4)]
input_space = []
for i in range(0,len(List1)):
	templist = []
	templist.append(Gender[int(List1[i][0])])
	templist.append(Age[int(List1[i][1])])
	templist.append(Student[int(List1[i][2])])
	templist.append(PreviouslyDeclined[int(List1[i][3])])
	input_space.append(templist)

#print 'Input Space: ', input_space
####

#### Generating Concept Space
outputs = ["".join(seq) for seq in itertools.product("01", repeat=16)]
outputs = [list(sublist) for sublist in outputs]
final_output_labels = []
for i in range(0,len(outputs)):
	temp1 = [val.replace('0','low') for val in outputs[i]]
	temp = [val.replace('1','high') for val in temp1]
	final_output_labels.append(temp)

#print 'FOL Before: ', len(final_output_labels)
####

#### Removing all the hypothesis which are not consistent with the Training set
for i in range(0,len(training_set)):
	index_training = input_space.index(training_set[i][0:-1])
	j = 0	
	while 1:
		if j >= len(final_output_labels):
			break		
		if training_set[i][-1] != final_output_labels[j][index_training]:
			del final_output_labels[j]
		else:
			j = j + 1
		
end = time.time()
#print 'FOL After: ', len(final_output_labels)
#print 'Time: ', end - start
####

### Printing Output
print len(input_space) # Size of the Input Space 
print pow(2,16) # Size of the Concept Space
print len(final_output_labels) # Size of the Version Space
### 

#### Predicting on the Test Set
Count = []
for i in range(0,len(testing_set)):
	counttemp = [0,0]	
	index_testing = input_space.index(testing_set[i][0:-1])
	for j in range(0,len(final_output_labels)):
		if final_output_labels[j][index_testing] == 'high':
			counttemp[0] += 1
		else:
			counttemp[1] += 1
	print counttemp[0], counttemp[1] # Count number of highs and lows
	Count.append(counttemp)	
####

