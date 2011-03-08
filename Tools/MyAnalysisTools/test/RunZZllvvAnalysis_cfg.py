import FWCore.ParameterSet.Config as cms
# import commands
# import os
# import FWCore.ParameterSet.VarParsing as VarParsing
# options = VarParsing.VarParsing()
# options.register('selection',
#                 "", #default value
#                 VarParsing.VarParsing.multiplicity.singleton,
#                 VarParsing.VarParsing.varType.string,
#                 "Selection pass")
# options.register('sample',
#                 "", #default value
#                 VarParsing.VarParsing.multiplicity.singleton,
#                 VarParsing.VarParsing.varType.string,
#                 "Sample")

# options.parseArguments()


#---------------------------------------------

#---------------------------------------------

process = cms.Process("ANALYSIS")

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring()#firstRun = cms.untracked.uint32(10)
                            )


#process.source.fileNames.append('/store/cmst3/user/cerminar/Analysis/ZZllvv_v01/sel0/ZJetsPU/cmgTuple_0.root')


process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(100)
)



process.zzllvvAnalyzer = cms.EDAnalyzer("ZZllvvAnalyzer")



#output file for histograms etc
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("pippo.root"))


process.analysisSequence = cms.Sequence(process.zzllvvAnalyzer)

process.p = cms.Path(process.analysisSequence)
#process.MessageLogger.cerr.FwkReport.reportEvery = 100

# build the file list

# if options.selection and options.sample:

#     basedir = '/castor/cern.ch/cms/store/cmst3/user/cerminar/Analysis/ZZllvv_v01/'
#     inputDir = basedir + options.selection + "/" + options.sample + "/"



#     castorDir_cmd = "rfdir " + inputDir
#     castorDir_out = commands.getstatusoutput(castorDir_cmd)
#     if castorDir_out[0] != 0:
#         print castorDir_out[1]



#     storeDir = inputDir.split("cern.ch/cms")[1]
#     #storeDir = "rfio://" + inputDir
#     for castorFileLine in castorDir_out[1].split("\n"):
#         castorFile = castorFileLine.split()[8]
#         if "root" in castorFile:
#             process.source.fileNames.append(storeDir + castorFile)

# else :
process.source.fileNames.append('/store/cmst3/user/cerminar/Analysis/ZZllvv_v01/sel0/ZJetsPU/cmgTuple_0.root')
