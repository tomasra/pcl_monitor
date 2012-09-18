import os

allRuns = True
maxCalc = 5
calc = 0

read_file = open("MyAnalysis/ZLumiStudy/test/macros/runnumberSorted.txt", "r")

#runs = [194050, 194051, 194052, 194424, 194428, 194429, 194455, 194464, 194479, 194480, 194691, 194699, 194702, 194711, 194712, 195396, 195397, 195398, 195399, 195947, 195928, 195950, 196452, 196453]

for lines in read_file:
#for line in runs:
	if (allRuns or calc < maxCalc):
		line = lines[0:len(lines)-1]
		print line
		command = str("RecoLuminosity/LumiDB/scripts/lumiCalc2.py lumibylsXing  -i /data1/ZLumiStudy/CalcLumi/JsonFiles/" + str(line) + ".json -o /data1/ZLumiStudy/CalcLumi/Version1/" + str(line) + ".csvt")
		print command
		os.system(command)
		calc += 1

read_file.close()