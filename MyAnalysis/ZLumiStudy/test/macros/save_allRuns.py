# produce allRuns.txt with: RecoLuminosity/LumiDB/scripts/lumiCalc2.py overview -i RecoLuminosity/LumiDB/Cert_190456-198485_8TeV_PromptReco_Collisions12_JSON.txt -o MyAnalysis/ZLumiStudy/test/macros/allRuns.txt

numbers = []

read_file = open("allRuns.txt", "r")
for line in read_file:
	lineparts = line.split(",")
	runnumber, fill = lineparts[0].split(":")
	if runnumber != "Run":
		numbers.append(runnumber)
	

read_file.close()

write_file = open("runnumberSorted_Number.txt", "w")
for n in numbers:
	write_file.write(n + '\n')

write_file.close()

