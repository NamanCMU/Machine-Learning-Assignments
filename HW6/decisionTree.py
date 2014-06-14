import math
import sys

##### Reading the training file and saving it in a list of lists
dataset_name = sys.argv[1]
with open(dataset_name) as f:
  array_initial = []
  for line in f:
    line = line.split()
    if line:
      str_line =  ','.join(line)
      list_line = str_line.split(',')
      array_initial.append(list_line)
#####

##### Reading the testing dataset file and saving it in a list of lists
dataset_name = sys.argv[2]
with open(dataset_name) as f:
  array_test = []
  for line in f:
    line = line.split()
    if line:
      str_line =  ','.join(line)
      list_line = str_line.split(',')
      array_test.append(list_line)
#####

##### Output Labels for different datasets
if array_initial[1][-1] == "yes" or array_initial[1][-1] == "no":
	boolean_hit = ["yes","no"]
else:
	boolean_hit = ["A","notA"]
#####	

##### Finding Entropy
def entropy(node):
  		Total_labels = node[0] + node[1]
  		if node[0] == 0 or node[1] == 0:
  			return 0
  		prob_negative = (node[0]*1.0/Total_labels)
  		prob_positive = (node[1]*1.0/Total_labels)
  		entropy_value = -prob_negative*math.log(prob_negative,2) - prob_positive*math.log(prob_positive,2)
  		return entropy_value
#####

##### Finding Mutual Information		
def mutual_information(examples,parent_label,attribute):
		attribute_index = array_initial[0].index(attribute)
		attribute_children = {}
		right_child = [0,0]
		left_child = [0,0]
		value = examples[1][attribute_index]
		for i in xrange(0,len(examples)):
			if examples[i][attribute_index] == value and examples[i][-1] == boolean_hit[0]:
					right_child[0] += 1
			elif examples[i][attribute_index] == value and examples[i][-1] == boolean_hit[1]:
					right_child[1] += 1
			elif examples[i][attribute_index] != value and examples[i][-1] == boolean_hit[0]:
					left_child[0] += 1
			elif examples[i][attribute_index] != value and examples[i][-1] == boolean_hit[1]:
					left_child[1] += 1
    
		attribute_children['left'] = left_child
		attribute_children['right'] = right_child
		left_child_entropy = entropy(left_child) 
		right_child_entropy = entropy(right_child) 
		left_child_prob = sum(left_child)*1.0/len(examples)
		right_child_prob = sum(right_child)*1.0/len(examples)
		mutualinfo = entropy(parent_label) - left_child_prob*left_child_entropy - right_child_prob*right_child_entropy
		return mutualinfo
#####

##### It returns children of the attribute and different labels
def train_stump(examples,attribute):
	attribute_index = array_initial[0].index(attribute)
	children = []
	child_right = [0,0]
	child_left = [0,0]
	value1 = examples[1][attribute_index]	
	value2 = 0	
	for i in xrange(0,len(examples)):
		if examples[i][attribute_index] == value1 and examples[i][-1] == boolean_hit[0]:
				child_right[0] += 1
		elif examples[i][attribute_index] == value1 and examples[i][-1] == boolean_hit[1]:
				child_right[1] += 1
		elif examples[i][attribute_index] != value1 and examples[i][-1] == boolean_hit[0]:
				child_left[0] += 1
				value2 = examples[i][attribute_index]
		elif examples[i][attribute_index] != value1 and examples[i][-1] == boolean_hit[1]:
				child_left[1] += 1
				value2 = examples[i][attribute_index]
	children.append(child_left)
	children.append(child_right)	
	return [children,value2,value1]
#####

##### It returns the best attribute which has maximum information
def best_attribute(examples,attributes,parent_label):
	max_minfo = -10
	for attr in attributes:
		minfo = mutual_information(examples,parent_label,attr)
		if minfo >= max_minfo:
			max_minfo = minfo
			best_attr = attr
	return best_attr
#####

##### It generates a subset of the examples which is to be used in the next stage
def examples_subset(examples,attribute,boolean_label):
	examples_sub = []
	attribute_index = array_initial[0].index(attribute)
	for i in xrange(0,len(examples)):
		if examples[i][attribute_index] == boolean_label:
			examples_sub.append(examples[i])
	return examples_sub		
#####

##### It returns the label
def get_label(list_label):
	if list_label[0] > list_label[1]:
		return boolean_hit[0]
	else: 
		return boolean_hit[1]
#####

##### It predicts the label based on the training set
def testing(test_example):
	for i in xrange(0,len(test_example)):
		if array_initial[0][i] == node1.attr:
			if test_example[i] == node1.lvalue:
				for j in xrange(0,len(test_example)):
					if array_initial[0][j] == node2.attr:
						if test_example[j] == node2.lvalue:
							predicted_label = get_label(node2.lcn)
						else:
							predicted_label = get_label(node2.rcn)
			elif test_example[i] == node1.rvalue:
				for j in xrange(0,len(test_example)):
					if array_initial[0][j] == node3.attr:
						if test_example[j] == node3.lvalue:
							predicted_label = get_label(node3.lcn)
						else:
							predicted_label = get_label(node3.rcn)
	return predicted_label
#####

class node:
	def __init__(self):
		self.lcn = [0,0]
		self.rcn = [0,0]
		self.data = [0,0]
		self.entropy = 0
		self.minfo = 0
		self.lvalue = 0
		self.rvalue = 0
		self.lattr = 0
		self.rattr = 0
		self.attr = 0

if __name__ == '__main__':
	
	##### NODE 1
	node1 = node()
	node1.data = [0,0]
	for i in xrange(1,len(array_initial)):
		if array_initial[i][-1] == boolean_hit[1]:
			node1.data[1] += 1
		else:
			node1.data[0] += 1
	
	attributes_initial = []
	for attr in (array_initial[0][:-1]):
		attributes_initial.append(attr)		
	best_attr = best_attribute(array_initial,attributes_initial,node1.data)
	
	node1.attr = best_attr
	parent_attr = best_attr
	children_parent = train_stump(array_initial,best_attr)
	node1.lcn = children_parent[0][0]
	node1.rcn = children_parent[0][1]
	node1.lvalue = children_parent[1]
	node1.rvalue = children_parent[2]
	node1.entropy = entropy(node1.data)
	node1.minfo = mutual_information(array_initial,node1.data,best_attr)
	#####

	##### NODE 2
	node2 = node()
	node2.data = node1.lcn
	examples_sub = examples_subset(array_initial,parent_attr,node1.lvalue)
	
	best_attr = best_attribute(examples_sub,attributes_initial,node1.data)
	
	node1.lattr = best_attr
	node2.attr = best_attr
	children_parent = train_stump(examples_sub,best_attr)
	node2.lcn = children_parent[0][0]
	node2.rcn = children_parent[0][1]
	node2.lvalue = children_parent[1]
	node2.rvalue = children_parent[2]
	node2.entropy = entropy(node2.data)
	node2.minfo = mutual_information(examples_sub,node2.data,best_attr)
	##### 

	##### NODE 3
	node3 = node()
	node3.data = node1.rcn
	examples_sub = examples_subset(array_initial,parent_attr,node1.rvalue)
	
	best_attr = best_attribute(examples_sub,attributes_initial,node1.data)
	node1.rattr = best_attr
	node3.attr = best_attr

	children_parent = train_stump(examples_sub,best_attr)
	node3.lcn = children_parent[0][0]
	node3.rcn = children_parent[0][1]
	node3.lvalue = children_parent[1]
	node3.rvalue = children_parent[2]
	node3.entropy = entropy(node3.data)
	node3.minfo = mutual_information(examples_sub,node3.data,best_attr)
	#####

	##### Training error
	predicted_label = []
	given_label = []
	for eg in array_initial[1:]:
		predicted_label.append(testing(eg))
		given_label.append(eg[-1])
	
	count1 = 0
	for i in xrange(0,len(given_label)):
		if predicted_label[i] == given_label[i]:
			count1 += 1
	count1 = count1*1.0/len(array_initial)
	#####

	##### Testing error
	predicted_label = []
	given_label = []
	for eg in array_test[1:]:
		predicted_label.append(testing(eg))
		given_label.append(eg[-1])
	
	count2 = 0
	for i in xrange(0,len(given_label)):
		if predicted_label[i] == given_label[i]:
			count2 += 1
	count2 = count2*1.0/len(array_initial)
	#####

	##### Printing the output
	print "[",node1.data[0],"+/",node1.data[1],"-]"
	if node1.minfo >= 0.1:
		print node1.attr, " = " , node1.lvalue, ":", "[",node1.lcn[0],"+/",node1.lcn[1],"-]"
		if node2.minfo >= 0.1:
			print "| ", node1.lattr, " = ", node2.lvalue, ":" , "[",node2.lcn[0],"+/",node2.lcn[1],"-]"
		if node2.minfo >= 0.1:
			print "| ", node1.lattr, " = ", node2.rvalue, ":" , "[",node2.rcn[0],"+/",node2.rcn[1],"-]"
		print node1.attr, " = " , node1.rvalue, ":", "[",node1.rcn[0],"+/",node1.rcn[1],"-]"
		if node3.minfo >= 0.1:	
			print "| ", node1.rattr, " = ", node3.lvalue, ":" , "[",node3.lcn[0],"+/",node3.lcn[1],"-]"
		if node3.minfo >= 0.1:	
			print "| ", node1.rattr, " = ", node3.rvalue, ":" , "[",node3.rcn[0],"+/",node3.rcn[1],"-]"
	print "error(train): " , 1 - count1
	print "error(test): " , 1 - count2
	#####