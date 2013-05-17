import csv
import datetime
def opencsv(filename):

	reader = csv.reader(open(filename, "rU"), dialect="excel") 

	times = []

	for line in reader:
		times.append(datetime.datetime.strptime(line[0], "%H:%M:%S"))
	
	return times