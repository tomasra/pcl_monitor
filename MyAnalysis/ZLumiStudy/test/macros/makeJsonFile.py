
#function to get the RunNumber from the Json-File and save the LS
def get_RunNumber_LS(text):
	textpart = text.split("\":")
	runN = textpart[0][1:]
	lumiSection = textpart[1]
	return runN, lumiSection

dicty = {}

#read json-file and separte each run
read_file = open("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Prompt/Cert_190456-198485_8TeV_PromptReco_Collisions12_JSON.txt", "r")

for line in read_file:
	lineparts = line.split("]], ")
	for i in range(len(lineparts)):
		if lineparts[i][0] == "{":
			runNumber, ls = get_RunNumber_LS(lineparts[i][1:])
		else:
			runNumber, ls = get_RunNumber_LS(lineparts[i])
		dicty[runNumber] = ls

read_file.close()

#write dicty in different files
for key in dicty:
	write_file = open("/data1/ZLumiStudy/CalcLumi/JsonFiles/" + key + ".json", "w")
	write_file.write("{\"" + key + "\":" + dicty[key] + "]]}")
	write_file.close()


