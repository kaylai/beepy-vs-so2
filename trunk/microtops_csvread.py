import csv
import datetime
def opencsv(filename):

	csvfile = open(filename, "rU")
	#dialect = csv.Sniffer().sniff(csvfile.read(2048))
	csvfile.seek(0)
	reader = csv.reader(csvfile, dialect = "excel")

	micro_times = []
	aot = []
	aot_440 = []
	aot_675 = []
	aot_870 = []
	aot_1020 = []
	firstline = True
	for line in reader:
		if firstline:
			firstline = False
			continue
		#micro_times.append(datetime.datetime.strptime(line[2] + line[3], "%m/%d/%y%H:%M:%S")) #<-- normally, in cleared files time and date are columns 2 & 3. Change the date format accordingly
		micro_times.append(datetime.datetime.strptime(line[2] + line[3], "%m/%d/%y%H:%M:%S"))
		#aot.append(float(line[23])) #<-- normally, in cleared files the AOT380 column is line 23
		aot.append(float(line[23]))
		aot_440.append(float(line[24]))
		aot_675.append(float(line[25]))
		aot_870.append(float(line[26]))
		aot_1020.append(float(line[27]))
	
	return(micro_times, aot, aot_440, aot_675, aot_870, aot_1020)