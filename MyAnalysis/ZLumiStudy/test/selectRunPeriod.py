# only use Run2012A or Run2012B


folder = '/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/'
inputFileNames = ''


read_file = open("TPV0_SingleMu_Run2012B-PromptReco-v1_sorted.h", "r")
for line in read_file:
	if line[0] == "}" or line[0] == "{" or line[0:8] == "inputDir":
		pass

	else:
		lineparts = line.split("\"")
		if len(lineparts) == 3:
			inputFileNames = inputFileNames + folder + lineparts[1] + "_lumi.root\n" 

read_file.close()

write_file = open("TagAndProbe/Run2012B.txt", "w")
write_file.write(inputFileNames)

write_file.close()

