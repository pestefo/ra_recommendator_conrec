
fileName = "/home/pestefo/projects/ra_recommendator_conrec/data/extracted_user_tags_non_extended_2.csv"
lineList = [line.rstrip('\n') for line in open(fileName)]
lineList = list(set(lineList))

for line in lineList:
	print(line)
