import itertools
import sys

##### Reading data from a text file
path_to_file = sys.argv[1]
with open(path_to_file) as f:
	array = []
	for line in f:
		line = line.split()
		if line:
			line = [str(i) for i in line]
			array.append(line)
array = list(itertools.chain(*array))
##### 

##### Quicksort subroutine
def quicksort(array):
	length = len(array)	
	if length < 2:
		return array
	pivot = array[0]
	i = 1
	for j in range(1,length):
		if array[j] < pivot:
			temp = array[j]
			array[j] = array[i]
			array[i] = temp
			i = i + 1
	temp = array[i-1]
	array[i-1] = pivot
	array[0] = temp
	return quicksort(array[0:i-1]) + [pivot] + quicksort(array[i:])
#####

array = [val.lower() for val in array] # Convert to Lower Case
array = quicksort(array)

##### Removing duplicates from the output and printing the output
final_output = []
for word in array:
	if word.lower() not in final_output:
		final_output.append(word.lower())
sys.stdout.write(','.join(final_output))
#####
