import csv, os

def getTransitionsFromCsv(filename):
	
	main_dir = os.path.split(os.path.abspath(__file__))[0]
	csvfile = open(os.path.join(main_dir, filename))
	
	reader = csv.DictReader(csvfile)
	transitions=[]
	
	for row in reader:
		drow=dict(row) #dict row
		for k, v in drow.items():
			if v=='None' or v=='':
				drow[k]=None
		transitions.append(drow)
		#print(drow)
	
	return transitions
