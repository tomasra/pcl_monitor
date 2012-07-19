from ROOT import *


maxRunNumber = 5
run_Number = 0

chain = TChain("Z2muTree/candTree")
chain.Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuA/ZLumiStudy.root")
chain.Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB1/ZLumiStudy.root")
chain.Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB2/ZLumiStudy.root")
#chain.Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB3/ZLumiStudy.root")
#chain.Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB4/ZLumiStudy.root")
#chain.Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB5/ZLumiStudy.root")
#chain.Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB6/ZLumiStudy.root")
#chain.Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB7/ZLumiStudy.root")
#chain.Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB8/ZLumiStudy.root")
#chain.Add("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB9/ZLumiStudy.root")


read_file = open("runnumberSorted.txt", "r")
for line in read_file:
	if run_Number < maxRunNumber:
		runnumber = line[0:len(line)-1]
		run_Number += 1
		print "Run Number: ", runnumber
		chain.Process("ZlumiTreeReader.C+", runnumber)


