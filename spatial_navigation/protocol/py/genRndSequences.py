# _*_ coding: utf-8 _*_

import itertools
import random
from csv_io import write_to_csv as writeToFile
import cPickle

''' 
Sequences will be generated as lists, containing all possible combinations of intersections (4), directions (4) and targets (2) 
The sequences are encoded as follows: (intersection, direction (starting point), target); see defineOptions for the corresponding positions of each number
'''

numSeq = 50

# experimental condition

sequences_exp = ()

while len(sequences_exp) <= numSeq:
	
	seqFound = False
	i = 1

	print 'Start generating exp sequence...'

	while seqFound == False:
		
		sequence = list(itertools.product(range(4),range(4),range(2))) * 3
		
		random.shuffle(sequence)	
		duplFound = False
		
		i += 1
		
		for first, sec, third, fourth in zip(sequence, sequence[1:], sequence[2:],sequence[3:]):
			if first[0:2] == sec[0:2] or first [0:2] == third[0:2] or first[0:3] == sec[0:3] or first [0:3] == third[0:3] or first[0:3] == fourth[0:3]:
				duplFound = True
				break
		
		# if no adjacent duplicates are found, exit while loop
		if duplFound == False:
			seqFound = True
		
	
	sequences_exp = sequences_exp + (sequence, )
	
	writeToFile(sequence,'sequences_exp.csv')
	
	print 'Done..., it took ', i
	print len(sequences_exp)
	
output_exp = open('sequences_exp.pkl', 'wb')
cPickle.dump(sequences_exp,output_exp)
output_exp.close()

# control condition

sequences_ctrl = ()

while len(sequences_ctrl) <= numSeq:
	
	seqFound = False
	i = 1

	print 'Start generating ctrl sequence...'

	while seqFound == False:
		
		sequence = list(itertools.product(range(4),range(4),range(4)))
		
		random.shuffle(sequence)	
		duplFound = False
		
		i += 1
		
		for first, sec, third in zip(sequence, sequence[1:], sequence[2:]):
			if first[0:2] == sec[0:2] or first [0:2] == third[0:2]:
				duplFound = True
				break
		
		# if no adjacent duplicates are found, exit while loop
		if duplFound == False:
			seqFound = True
		
	
	sequences_ctrl = sequences_ctrl + (sequence, )
	
	writeToFile(sequence,'sequences_ctrl.csv')
	
	print 'Done..., it took ', i
	print len(sequences_ctrl)
	
output_ctrl = open('sequences_ctrl.pkl', 'wb')
cPickle.dump(sequences_ctrl,output_ctrl)
output_ctrl.close()



