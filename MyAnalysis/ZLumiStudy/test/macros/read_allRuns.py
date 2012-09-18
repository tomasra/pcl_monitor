# produce allRuns.txt with: RecoLuminosity/LumiDB/scripts/lumiCalc2.py overview -i RecoLuminosity/LumiDB/Cert_190456-198485_8TeV_PromptReco_Collisions12_JSON.txt -o MyAnalysis/ZLumiStudy/test/macros/allRuns.txt

dicty = {}

read_file = open("MyAnalysis/ZLumiStudy/test/macros/allRuns.txt", "r")
for line in read_file:
	lineparts = line.split(",")
	runnumber, fill = lineparts[0].split(":")
	lumi = lineparts[len(lineparts)-1]
	#print "Runnumber", runnumber
	#print "lumi", lumi
	dicty[runnumber] = lumi

read_file.close()

write_file = open("MyAnalysis/ZLumiStudy/test/macros/runnumberSorted.txt", "w")
for w in sorted(dicty, key = dicty.get, reverse=True):
	if w != "Run":
		write_file.write(w + "\n")

write_file.close()
