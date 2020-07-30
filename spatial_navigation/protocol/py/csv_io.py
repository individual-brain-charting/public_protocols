# _*_ coding: utf-8 _*_
'''
Define two simple functions to write and read from csv/text files.
'''
import csv

# define a function to write to a file
def write_to_csv(data, csvfile, delimiter=','):
	'''Simply write a row of data to csvfile appending
	contents. There is another method to write several
	rows (csv.writerows).
	The delimiter can be changed from , to any other passing
	the delimiter argument. By default is ','.
	'''
	# windows is a nightmare, normally in serious OS
	# you just write 'ab' in the write options
	with open(csvfile, 'a+b') as f:
		writer = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
		writer.writerow(data)

# define a function to read the data
def read_from_csv(csvfile):
	'''Read contents from the CSV file csvfile.
	returns : a list with data
	'''
	data = []
	add_to_data = data.append
	with open(csvfile, 'r+b') as f:
		reader = csv.reader(f)
		for row in reader:
			add_to_data(row)
	return data
			
	if __name__ == '__main__':
		import os
		# a header
		h = ['one', 'two', 'three', 'four', 'five']
		# create a couple of rows
		r1 = range(1, 6)
		r2 = range(6, 11)
		# define a file
		commafile = 'test.csv'
		if os.path.exists(commafile):
			os.remove(commafile)
		# write to it
		write_to_csv(h, commafile)
		write_to_csv(r1, commafile)
		write_to_csv(r2, commafile)
		# read the contents
		really_important_data = read_from_csv(commafile)
		# see if it worked
		print('Reading {}...'.format(commafile))
		for row in really_important_data:
			print(', '.join(row))
		# test another delimiter, e.g. the subptimal TAB
		tabfile = 'test_tab.txt'
		if os.path.exists(tabfile):
			os.remove(tabfile)
		write_to_csv(h, tabfile, delimiter='\t')
		write_to_csv(r1, tabfile, delimiter='\t')
		tab_data = read_from_csv(tabfile)
		print('Reading {}...'.format(tabfile))
		for row in tab_data:
			print('\t'.join(row))