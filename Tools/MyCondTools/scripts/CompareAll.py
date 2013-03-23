#!/usr/bin/env python

import os

def fillIOVList(iovList, fileName):
    found = False
    for line in open(fileName):
        if line == "\n":
            break
        if found == True:
            iovList.append(line.split()[0])
        if line.find("--------------------") != -1:
            found = True

def compareIOVs(tag1, connect1, tag2, connect2):
    os.system("echo 'Comparing tags: " + tag1 + " " + tag2 + "'")
    os.system("cmscond_list_iov -c "+connect1+" -P /afs/cern.ch/cms/DB/conddb -t "+tag1+" > list1.txt")
    os.system("cmscond_list_iov -c "+connect2+" -P /afs/cern.ch/cms/DB/conddb -t "+tag2+" > list2.txt")

    # Build IOV lists for the two tags
    iovList1 = []
    fillIOVList(iovList1, "list1.txt")
    iovList2 = []
    fillIOVList(iovList2, "list2.txt")

    # Take the shortest
    iovList = iovList1
    if len(iovList1) > len(iovList2):
        iovList = iovList2

    # Dump the content of the common IOVs and compare them
    i=0
    for IOV in iovList:
        os.system("echo 'IOV = " + IOV + "'")
        end = str(long(IOV)+1)
        i+=1
        os.system("cmscond_2XML -c "+connect1+" -P /afs/cern.ch/cms/DB/conddb -t "+tag1+" -b " + IOV + " -e "+end +" > /dev/null")
        os.system("cmscond_2XML -c "+connect2+" -P /afs/cern.ch/cms/DB/conddb -t "+tag2+" -b " + IOV + " -e "+end +" > /dev/null")
        os.system("diff "+tag1+".xml "+tag2+".xml | grep -v created | grep -v '2,3c2,3'")
        os.system("rm -f "+tag1+".xml "+tag2+".xml")
        

tag1 = "AlCaRecoHLTpaths8e29_1e31_v16_offline"
connect1 = "frontier://FrontierArc/CMS_COND_31X_HLT_DB07"
tag2 = "AlCaRecoHLTpaths8e29_1e31_v15_offline"
connect2 = "frontier://FrontierArc/CMS_COND_31X_HLT_DA14"
compareIOVs(tag1, connect1, tag2, connect2)

tag1 = "HcalRespCorrs_v4.7_offline"
connect1 = "frontier://FrontierArc/CMS_COND_31X_HCAL_DB07"
tag2 = "HcalRespCorrs_v4.5_offline"
connect2 = "frontier://FrontierArc/CMS_COND_31X_HCAL_DA14"
compareIOVs(tag1, connect1, tag2, connect2)

tag1 = "HcalGains_v5.07_offline"
connect1 = "frontier://FrontierArc/CMS_COND_31X_HCAL_DB07"
tag2 = "HcalGains_v5.06_offline"
connect2 = "frontier://FrontierArc/CMS_COND_31X_HCAL_DA14"
compareIOVs(tag1, connect1, tag2, connect2)

tag1 = "SiPixelTemplateDBObject_38T_v6_offline"
connect1 = "frontier://FrontierArc/CMS_COND_31X_PIXEL_DB07"
tag2 = "SiPixelTemplateDBObject_38T_v4_offline"
connect2 = "frontier://FrontierArc/CMS_COND_31X_PIXEL_DA14"
compareIOVs(tag1, connect1, tag2, connect2)

tag1 = "EcalIntercalibConstants_2012ABCD_offline"
connect1 = "frontier://FrontierArc/CMS_COND_31X_ECAL_DB07"
tag2 = "EcalIntercalibConstants_V20121215_NLT_MeanPizPhiABC_EleABC_HR9EtaScABC_PhisymCor2_EoPCorAvg1_mixed"
connect2 = "frontier://FrontierArc/CMS_COND_31X_ECAL_DA14"
compareIOVs(tag1, connect1, tag2, connect2)

tag1 = "EcalADCToGeVConstant_Bon_RUN2012ABCD_V2_offline"
connect1 = "frontier://FrontierArc/CMS_COND_31X_ECAL_DB07"
tag2 = "EcalADCToGeVConstant_Bon_RUN2012ABC_offline_V2"
connect2 = "frontier://FrontierArc/CMS_COND_31X_ECAL_DA14"
compareIOVs(tag1, connect1, tag2, connect2)

tag1 = "EcalLaserAPDPNRatios_2012ABCD_offline_20130205"
connect1 = "frontier://FrontierArc/CMS_COND_42X_ECAL_LAS_DB07"
tag2 = "EcalLaserAPDPNRatios_20121020_447_p1_v2"
connect2 = "frontier://FrontierArc/CMS_COND_42X_ECAL_LAS_DA14"
compareIOVs(tag1, connect1, tag2, connect2)
