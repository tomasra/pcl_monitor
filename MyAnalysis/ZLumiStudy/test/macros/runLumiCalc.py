import os


maxCalc = 5
calc = 0

read_file = open("MyAnalysis/ZLumiStudy/test/macros/runnumberSorted.txt", "r")

for lines in read_file:
	if calc < maxCalc:
		line = lines[0:len(lines)-1]
		print line
		befehl = str("RecoLuminosity/LumiDB/scripts/lumiCalc2.py lumibylsXing -r " + str(line) + " -i RecoLuminosity/LumiDB/Cert_190456-198485_8TeV_PromptReco_Collisions12_JSON.txt -o /data1/ZLumiStudy/CalcLumi/Version0/" + str(line) + ".csvt")
		print befehl
		os.system(befehl)
		calc += 1

read_file.close()