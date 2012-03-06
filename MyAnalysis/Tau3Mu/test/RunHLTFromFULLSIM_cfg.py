# /users/cerminar/Tau3MuTest01/V24 (CMSSW_5_2_0_pre5_HLT8)

import FWCore.ParameterSet.Config as cms

process = cms.Process( "HLT" )

process.HLTConfigVersion = cms.PSet(
  tableName = cms.string('/users/cerminar/Tau3MuTest01/V24')
)

process.magfield = cms.ESSource( "XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring( 'Geometry/CMSCommonData/data/normal/cmsextent.xml',
      'Geometry/CMSCommonData/data/cms.xml',
      'Geometry/CMSCommonData/data/cmsMagneticField.xml',
      'MagneticField/GeomBuilder/data/MagneticFieldVolumes_1103l.xml',
      'MagneticField/GeomBuilder/data/MagneticFieldParameters_07_2pi.xml' ),
    rootNodeName = cms.string( "cmsMagneticField:MAGF" )
)
process.hltESSHcalSeverityLevel = cms.ESSource( "EmptyESSource",
    iovIsRunNotTime = cms.bool( True ),
    recordName = cms.string( "HcalSeverityLevelComputerRcd" ),
    firstValid = cms.vuint32( 1 )
)
process.hltESSEcalSeverityLevel = cms.ESSource( "EmptyESSource",
    iovIsRunNotTime = cms.bool( True ),
    recordName = cms.string( "EcalSeverityLevelAlgoRcd" ),
    firstValid = cms.vuint32( 1 )
)
process.hltESSBTagRecord = cms.ESSource( "EmptyESSource",
    iovIsRunNotTime = cms.bool( True ),
    recordName = cms.string( "JetTagComputerRecord" ),
    firstValid = cms.vuint32( 1 )
)
process.es_hardcode = cms.ESSource( "HcalHardcodeCalibrations",
    fromDDD = cms.untracked.bool( False ),
    toGet = cms.untracked.vstring( 'GainWidths' )
)
process.eegeom = cms.ESSource( "EmptyESSource",
    iovIsRunNotTime = cms.bool( True ),
    recordName = cms.string( "EcalMappingRcd" ),
    firstValid = cms.vuint32( 1 )
)
process.HepPDTESSource = cms.ESSource( "HepPDTESSource",
    pdtFileName = cms.FileInPath( "SimGeneral/HepPDTESSource/data/pythiaparticle.tbl" )
)
process.GlobalTag = cms.ESSource( "PoolDBESSource",
    BlobStreamerName = cms.untracked.string( "TBufferBlobStreamingService" ),
    DBParameters = cms.PSet( 
      authenticationPath = cms.untracked.string( "." ),
      connectionRetrialTimeOut = cms.untracked.int32( 60 ),
      idleConnectionCleanupPeriod = cms.untracked.int32( 10 ),
      messageLevel = cms.untracked.int32( 0 ),
      enablePoolAutomaticCleanUp = cms.untracked.bool( False ),
      enableConnectionSharing = cms.untracked.bool( True ),
      enableReadOnlySessionOnUpdateConnection = cms.untracked.bool( False ),
      connectionTimeOut = cms.untracked.int32( 0 ),
      connectionRetrialPeriod = cms.untracked.int32( 10 )
    ),
    toGet = cms.VPSet( 
    ),
    connect = cms.string( "frontier://(proxyurl=http://localhost:3128)(serverurl=http://localhost:8000/FrontierOnProd)(serverurl=http://localhost:8000/FrontierOnProd)(retrieve-ziplevel=0)/CMS_COND_31X_GLOBALTAG" ),
    globaltag = cms.string( "GR_H_V26::All" )
)

process.sistripconn = cms.ESProducer( "SiStripConnectivity" )
process.siStripLorentzAngleDepESProducer = cms.ESProducer( "SiStripLorentzAngleDepESProducer",
  LatencyRecord = cms.PSet( 
    record = cms.string( "SiStripLatencyRcd" ),
    label = cms.untracked.string( "" )
  ),
  LorentzAngleDeconvMode = cms.PSet( 
    record = cms.string( "SiStripLorentzAngleRcd" ),
    label = cms.untracked.string( "deconvolution" )
  ),
  LorentzAnglePeakMode = cms.PSet( 
    record = cms.string( "SiStripLorentzAngleRcd" ),
    label = cms.untracked.string( "peak" )
  )
)
process.siPixelTemplateDBObjectESProducer = cms.ESProducer( "SiPixelTemplateDBObjectESProducer" )
process.siPixelQualityESProducer = cms.ESProducer( "SiPixelQualityESProducer",
  ListOfRecordToMerge = cms.VPSet( 
    cms.PSet(  record = cms.string( "SiPixelQualityFromDbRcd" ),
      tag = cms.string( "" )
    ),
    cms.PSet(  record = cms.string( "SiPixelDetVOffRcd" ),
      tag = cms.string( "" )
    )
  )
)
process.preshowerDetIdAssociator = cms.ESProducer( "DetIdAssociatorESProducer",
  ComponentName = cms.string( "PreshowerDetIdAssociator" ),
  etaBinSize = cms.double( 0.1 ),
  nEta = cms.int32( 60 ),
  nPhi = cms.int32( 30 ),
  includeBadChambers = cms.bool( False )
)
process.navigationSchoolESProducer = cms.ESProducer( "NavigationSchoolESProducer",
  ComponentName = cms.string( "SimpleNavigationSchool" )
)
process.muonDetIdAssociator = cms.ESProducer( "DetIdAssociatorESProducer",
  ComponentName = cms.string( "MuonDetIdAssociator" ),
  etaBinSize = cms.double( 0.125 ),
  nEta = cms.int32( 48 ),
  nPhi = cms.int32( 48 ),
  includeBadChambers = cms.bool( False )
)
process.hoDetIdAssociator = cms.ESProducer( "DetIdAssociatorESProducer",
  ComponentName = cms.string( "HODetIdAssociator" ),
  etaBinSize = cms.double( 0.087 ),
  nEta = cms.int32( 30 ),
  nPhi = cms.int32( 72 ),
  includeBadChambers = cms.bool( False )
)
process.hltIter4ESPTrajectoryFilterIT = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 0.3 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 0 ),
    maxNumberOfHits = cms.int32( 100 ),
    maxConsecLostHits = cms.int32( 1 ),
    minimumNumberOfHits = cms.int32( 6 ),
    nSigmaMinPt = cms.double( 5.0 ),
    chargeSignificance = cms.double( -1.0 )
  ),
  ComponentName = cms.string( "hltIter4ESPTrajectoryFilterIT" )
)
process.hltIter4ESPTrajectoryBuilderIT = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltIter4ESPTrajectoryFilterIT" ),
  maxCand = cms.int32( 1 ),
  ComponentName = cms.string( "hltIter4ESPTrajectoryBuilderIT" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltIter4ESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator16" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( False ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 ),
  minNrOfHitsForRebuild = cms.untracked.int32( 4 )
)
process.hltIter4ESPPixelLayerPairs = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'TIB1+TIB2' ),
  ComponentName = cms.string( "hltIter4ESPPixelLayerPairs" ),
  TEC = cms.PSet(  ),
  FPix = cms.PSet(  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet(  ),
  TIB = cms.PSet(  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ) ),
  TOB = cms.PSet(  )
)
process.hltIter4ESPMeasurementTracker = cms.ESProducer( "MeasurementTrackerESProducer",
  StripCPE = cms.string( "StripCPEfromTrackAngle" ),
  inactivePixelDetectorLabels = cms.VInputTag(  ),
  PixelCPE = cms.string( "hltESPPixelCPEGeneric" ),
  stripLazyGetterProducer = cms.string( "hltSiStripRawToClustersFacility" ),
  OnDemand = cms.bool( True ),
  Regional = cms.bool( True ),
  UsePixelModuleQualityDB = cms.bool( True ),
  pixelClusterProducer = cms.string( "hltSiPixelClusters" ),
  switchOffPixelsIfEmpty = cms.bool( True ),
  inactiveStripDetectorLabels = cms.VInputTag( 'hltSiStripExcludedFEDListProducer' ),
  MaskBadAPVFibers = cms.bool( True ),
  UseStripStripQualityDB = cms.bool( True ),
  UsePixelROCQualityDB = cms.bool( True ),
  DebugPixelROCQualityDB = cms.untracked.bool( False ),
  UseStripAPVFiberQualityDB = cms.bool( True ),
  stripClusterProducer = cms.string( "hltIter4SiStripClusters" ),
  DebugStripAPVFiberQualityDB = cms.untracked.bool( False ),
  DebugStripStripQualityDB = cms.untracked.bool( False ),
  SiStripQualityLabel = cms.string( "" ),
  badStripCuts = cms.PSet( 
    TOB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TID = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TEC = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TIB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    )
  ),
  DebugStripModuleQualityDB = cms.untracked.bool( False ),
  ComponentName = cms.string( "hltIter4ESPMeasurementTracker" ),
  DebugPixelModuleQualityDB = cms.untracked.bool( False ),
  HitMatcher = cms.string( "StandardMatcher" ),
  skipClusters = cms.InputTag( "hltIter4ClustersRefRemoval" ),
  UseStripModuleQualityDB = cms.bool( True ),
  UseStripNoiseDB = cms.bool( False ),
  UseStripCablingDB = cms.bool( False )
)
process.hltIter3ESPTrajectoryFilterIT = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 0.3 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 0 ),
    maxNumberOfHits = cms.int32( 100 ),
    maxConsecLostHits = cms.int32( 1 ),
    minimumNumberOfHits = cms.int32( 3 ),
    nSigmaMinPt = cms.double( 5.0 ),
    chargeSignificance = cms.double( -1.0 )
  ),
  ComponentName = cms.string( "hltIter3ESPTrajectoryFilterIT" )
)
process.hltIter3ESPTrajectoryBuilderIT = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltIter3ESPTrajectoryFilterIT" ),
  maxCand = cms.int32( 1 ),
  ComponentName = cms.string( "hltIter3ESPTrajectoryBuilderIT" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltIter3ESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator16" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( False ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltIter3ESPMeasurementTracker = cms.ESProducer( "MeasurementTrackerESProducer",
  StripCPE = cms.string( "StripCPEfromTrackAngle" ),
  inactivePixelDetectorLabels = cms.VInputTag(  ),
  PixelCPE = cms.string( "hltESPPixelCPEGeneric" ),
  stripLazyGetterProducer = cms.string( "hltSiStripRawToClustersFacility" ),
  OnDemand = cms.bool( True ),
  Regional = cms.bool( True ),
  UsePixelModuleQualityDB = cms.bool( True ),
  pixelClusterProducer = cms.string( "hltSiPixelClusters" ),
  switchOffPixelsIfEmpty = cms.bool( True ),
  inactiveStripDetectorLabels = cms.VInputTag( 'hltSiStripExcludedFEDListProducer' ),
  MaskBadAPVFibers = cms.bool( True ),
  UseStripStripQualityDB = cms.bool( True ),
  UsePixelROCQualityDB = cms.bool( True ),
  DebugPixelROCQualityDB = cms.untracked.bool( False ),
  UseStripAPVFiberQualityDB = cms.bool( True ),
  stripClusterProducer = cms.string( "hltIter3SiStripClusters" ),
  DebugStripAPVFiberQualityDB = cms.untracked.bool( False ),
  DebugStripStripQualityDB = cms.untracked.bool( False ),
  SiStripQualityLabel = cms.string( "" ),
  badStripCuts = cms.PSet( 
    TOB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TID = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TEC = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TIB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    )
  ),
  DebugStripModuleQualityDB = cms.untracked.bool( False ),
  ComponentName = cms.string( "hltIter3ESPMeasurementTracker" ),
  DebugPixelModuleQualityDB = cms.untracked.bool( False ),
  HitMatcher = cms.string( "StandardMatcher" ),
  skipClusters = cms.InputTag( "hltIter3ClustersRefRemoval" ),
  UseStripModuleQualityDB = cms.bool( True ),
  UseStripNoiseDB = cms.bool( False ),
  UseStripCablingDB = cms.bool( False )
)
process.hltIter3ESPLayerTriplets = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2+BPix3',
    'BPix1+BPix2+FPix1_pos',
    'BPix1+BPix2+FPix1_neg',
    'BPix1+FPix1_pos+FPix2_pos',
    'BPix1+FPix1_neg+FPix2_neg',
    'BPix2+FPix1_pos+FPix2_pos',
    'BPix2+FPix1_neg+FPix2_neg',
    'FPix1_pos+FPix2_pos+TEC1_pos',
    'FPix1_neg+FPix2_neg+TEC1_neg',
    'FPix2_pos+TEC2_pos+TEC3_pos',
    'FPix2_neg+TEC2_neg+TEC3_neg',
    'BPix2+BPix3+TIB1',
    'BPix2+BPix3+TIB2',
    'BPix1+BPix3+TIB1',
    'BPix1+BPix3+TIB2',
    'BPix1+BPix2+TIB1',
    'BPix1+BPix2+TIB2' ),
  ComponentName = cms.string( "hltIter3ESPLayerTriplets" ),
  TEC = cms.PSet( 
    useRingSlector = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    minRing = cms.int32( 1 ),
    maxRing = cms.int32( 1 )
  ),
  FPix = cms.PSet( 
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0036 ),
    useErrorsFromParam = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    skipClusters = cms.InputTag( "hltIter3ClustersRefRemoval" ),
    hitErrorRPhi = cms.double( 0.0051 )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0060 ),
    useErrorsFromParam = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    skipClusters = cms.InputTag( "hltIter3ClustersRefRemoval" ),
    hitErrorRPhi = cms.double( 0.0027 )
  ),
  TIB = cms.PSet(  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ) ),
  TOB = cms.PSet(  )
)
process.hltIter2ESPTrajectoryFilterIT = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 0.3 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 1 ),
    maxNumberOfHits = cms.int32( 100 ),
    maxConsecLostHits = cms.int32( 1 ),
    minimumNumberOfHits = cms.int32( 3 ),
    nSigmaMinPt = cms.double( 5.0 ),
    chargeSignificance = cms.double( -1.0 )
  ),
  ComponentName = cms.string( "hltIter2ESPTrajectoryFilterIT" )
)
process.hltIter2ESPTrajectoryBuilderIT = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltIter2ESPTrajectoryFilterIT" ),
  maxCand = cms.int32( 2 ),
  ComponentName = cms.string( "hltIter2ESPTrajectoryBuilderIT" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltIter2ESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator16" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( False ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltIter2ESPPixelLayerPairs = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2',
    'BPix1+BPix3',
    'BPix2+BPix3',
    'BPix1+FPix1_pos',
    'BPix1+FPix1_neg',
    'BPix1+FPix2_pos',
    'BPix1+FPix2_neg',
    'BPix2+FPix1_pos',
    'BPix2+FPix1_neg',
    'BPix2+FPix2_pos',
    'BPix2+FPix2_neg',
    'FPix1_pos+FPix2_pos',
    'FPix1_neg+FPix2_neg' ),
  ComponentName = cms.string( "hltIter2ESPPixelLayerPairs" ),
  TEC = cms.PSet(  ),
  FPix = cms.PSet( 
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0036 ),
    useErrorsFromParam = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    skipClusters = cms.InputTag( "hltIter2ClustersRefRemoval" ),
    hitErrorRPhi = cms.double( 0.0051 )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0060 ),
    useErrorsFromParam = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    skipClusters = cms.InputTag( "hltIter2ClustersRefRemoval" ),
    hitErrorRPhi = cms.double( 0.0027 )
  ),
  TIB = cms.PSet(  ),
  TOB = cms.PSet(  )
)
process.hltIter2ESPMeasurementTracker = cms.ESProducer( "MeasurementTrackerESProducer",
  StripCPE = cms.string( "StripCPEfromTrackAngle" ),
  inactivePixelDetectorLabels = cms.VInputTag(  ),
  PixelCPE = cms.string( "hltESPPixelCPEGeneric" ),
  stripLazyGetterProducer = cms.string( "hltSiStripRawToClustersFacility" ),
  OnDemand = cms.bool( True ),
  Regional = cms.bool( True ),
  UsePixelModuleQualityDB = cms.bool( True ),
  pixelClusterProducer = cms.string( "hltSiPixelClusters" ),
  switchOffPixelsIfEmpty = cms.bool( True ),
  inactiveStripDetectorLabels = cms.VInputTag( 'hltSiStripExcludedFEDListProducer' ),
  MaskBadAPVFibers = cms.bool( True ),
  UseStripStripQualityDB = cms.bool( True ),
  UsePixelROCQualityDB = cms.bool( True ),
  DebugPixelROCQualityDB = cms.untracked.bool( False ),
  UseStripAPVFiberQualityDB = cms.bool( True ),
  stripClusterProducer = cms.string( "hltIter2SiStripClusters" ),
  DebugStripAPVFiberQualityDB = cms.untracked.bool( False ),
  DebugStripStripQualityDB = cms.untracked.bool( False ),
  SiStripQualityLabel = cms.string( "" ),
  badStripCuts = cms.PSet( 
    TOB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TID = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TEC = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TIB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    )
  ),
  DebugStripModuleQualityDB = cms.untracked.bool( False ),
  ComponentName = cms.string( "hltIter2ESPMeasurementTracker" ),
  DebugPixelModuleQualityDB = cms.untracked.bool( False ),
  HitMatcher = cms.string( "StandardMatcher" ),
  skipClusters = cms.InputTag( "hltIter2ClustersRefRemoval" ),
  UseStripModuleQualityDB = cms.bool( True ),
  UseStripNoiseDB = cms.bool( False ),
  UseStripCablingDB = cms.bool( False )
)
process.hltIter1ESPTrajectoryFilterIT = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 0.2 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 1 ),
    maxNumberOfHits = cms.int32( 100 ),
    maxConsecLostHits = cms.int32( 1 ),
    minimumNumberOfHits = cms.int32( 3 ),
    nSigmaMinPt = cms.double( 5.0 ),
    chargeSignificance = cms.double( -1.0 )
  ),
  ComponentName = cms.string( "hltIter1ESPTrajectoryFilterIT" )
)
process.hltIter1ESPTrajectoryBuilderIT = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltIter1ESPTrajectoryFilterIT" ),
  maxCand = cms.int32( 2 ),
  ComponentName = cms.string( "hltIter1ESPTrajectoryBuilderIT" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltIter1ESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator16" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( False ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltIter1ESPPixelLayerTriplets = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2+BPix3',
    'BPix1+BPix2+FPix1_pos',
    'BPix1+BPix2+FPix1_neg',
    'BPix1+FPix1_pos+FPix2_pos',
    'BPix1+FPix1_neg+FPix2_neg' ),
  ComponentName = cms.string( "hltIter1ESPPixelLayerTriplets" ),
  TEC = cms.PSet(  ),
  FPix = cms.PSet( 
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0036 ),
    useErrorsFromParam = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    skipClusters = cms.InputTag( "hltIter1ClustersRefRemoval" ),
    hitErrorRPhi = cms.double( 0.0051 )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0060 ),
    useErrorsFromParam = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    skipClusters = cms.InputTag( "hltIter1ClustersRefRemoval" ),
    hitErrorRPhi = cms.double( 0.0027 )
  ),
  TIB = cms.PSet(  ),
  TOB = cms.PSet(  )
)
process.hltIter1ESPMeasurementTracker = cms.ESProducer( "MeasurementTrackerESProducer",
  StripCPE = cms.string( "StripCPEfromTrackAngle" ),
  inactivePixelDetectorLabels = cms.VInputTag(  ),
  PixelCPE = cms.string( "hltESPPixelCPEGeneric" ),
  stripLazyGetterProducer = cms.string( "hltSiStripRawToClustersFacility" ),
  OnDemand = cms.bool( True ),
  Regional = cms.bool( True ),
  UsePixelModuleQualityDB = cms.bool( True ),
  pixelClusterProducer = cms.string( "hltSiPixelClusters" ),
  switchOffPixelsIfEmpty = cms.bool( True ),
  inactiveStripDetectorLabels = cms.VInputTag( 'hltSiStripExcludedFEDListProducer' ),
  MaskBadAPVFibers = cms.bool( True ),
  UseStripStripQualityDB = cms.bool( True ),
  UsePixelROCQualityDB = cms.bool( True ),
  DebugPixelROCQualityDB = cms.untracked.bool( False ),
  UseStripAPVFiberQualityDB = cms.bool( True ),
  stripClusterProducer = cms.string( "hltIter1SiStripClusters" ),
  DebugStripAPVFiberQualityDB = cms.untracked.bool( False ),
  DebugStripStripQualityDB = cms.untracked.bool( False ),
  SiStripQualityLabel = cms.string( "" ),
  badStripCuts = cms.PSet( 
    TOB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TID = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TEC = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TIB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    )
  ),
  DebugStripModuleQualityDB = cms.untracked.bool( False ),
  ComponentName = cms.string( "hltIter1ESPMeasurementTracker" ),
  DebugPixelModuleQualityDB = cms.untracked.bool( False ),
  HitMatcher = cms.string( "StandardMatcher" ),
  skipClusters = cms.InputTag( "hltIter1ClustersRefRemoval" ),
  UseStripModuleQualityDB = cms.bool( True ),
  UseStripNoiseDB = cms.bool( False ),
  UseStripCablingDB = cms.bool( False )
)
process.hltHIAllESPTrajectoryBuilderIT = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPTrajectoryFilterIT" ),
  maxCand = cms.int32( 5 ),
  ComponentName = cms.string( "hltHIAllESPTrajectoryBuilderIT" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltHIAllESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( False ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltHIAllESPMuonCkfTrajectoryBuilder = cms.ESProducer( "MuonCkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPMuonCkfTrajectoryFilter" ),
  maxCand = cms.int32( 5 ),
  ComponentName = cms.string( "hltHIAllESPMuonCkfTrajectoryBuilder" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  useSeedLayer = cms.bool( False ),
  deltaEta = cms.double( 0.1 ),
  deltaPhi = cms.double( 0.1 ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  rescaleErrorIfFail = cms.double( 1.0 ),
  propagatorProximity = cms.string( "SteppingHelixPropagatorAny" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( True ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  MeasurementTrackerName = cms.string( "hltHIAllESPMeasurementTracker" ),
  intermediateCleaning = cms.bool( False ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltHIAllESPMeasurementTracker = cms.ESProducer( "MeasurementTrackerESProducer",
  StripCPE = cms.string( "StripCPEfromTrackAngle" ),
  inactivePixelDetectorLabels = cms.VInputTag(  ),
  PixelCPE = cms.string( "hltESPPixelCPEGeneric" ),
  stripLazyGetterProducer = cms.string( "hltHISiStripRawToClustersFacility" ),
  OnDemand = cms.bool( True ),
  Regional = cms.bool( True ),
  UsePixelModuleQualityDB = cms.bool( True ),
  pixelClusterProducer = cms.string( "hltHISiPixelClusters" ),
  switchOffPixelsIfEmpty = cms.bool( True ),
  inactiveStripDetectorLabels = cms.VInputTag( 'hltSiStripExcludedFEDListProducer' ),
  MaskBadAPVFibers = cms.bool( True ),
  UseStripStripQualityDB = cms.bool( True ),
  UsePixelROCQualityDB = cms.bool( True ),
  DebugPixelROCQualityDB = cms.untracked.bool( False ),
  UseStripAPVFiberQualityDB = cms.bool( True ),
  stripClusterProducer = cms.string( "hltHISiStripClusters" ),
  DebugStripAPVFiberQualityDB = cms.untracked.bool( False ),
  DebugStripStripQualityDB = cms.untracked.bool( False ),
  SiStripQualityLabel = cms.string( "" ),
  badStripCuts = cms.PSet( 
    TID = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TOB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TEC = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TIB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    )
  ),
  DebugStripModuleQualityDB = cms.untracked.bool( False ),
  ComponentName = cms.string( "hltHIAllESPMeasurementTracker" ),
  DebugPixelModuleQualityDB = cms.untracked.bool( False ),
  HitMatcher = cms.string( "StandardMatcher" ),
  skipClusters = cms.InputTag( "" ),
  UseStripModuleQualityDB = cms.bool( True ),
  UseStripNoiseDB = cms.bool( False ),
  UseStripCablingDB = cms.bool( False )
)
process.hltHIAllESPCkfTrajectoryBuilder = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPCkfTrajectoryFilter" ),
  maxCand = cms.int32( 5 ),
  ComponentName = cms.string( "hltHIAllESPCkfTrajectoryBuilder" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltHIAllESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( True ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltHIAllESPCkf3HitTrajectoryBuilder = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPCkf3HitTrajectoryFilter" ),
  maxCand = cms.int32( 5 ),
  ComponentName = cms.string( "hltHIAllESPCkf3HitTrajectoryBuilder" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltHIAllESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( True ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltESPbJetRegionalTrajectoryFilter = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 1.0 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 1 ),
    maxNumberOfHits = cms.int32( 8 ),
    maxConsecLostHits = cms.int32( 1 ),
    minimumNumberOfHits = cms.int32( 5 ),
    nSigmaMinPt = cms.double( 5.0 ),
    chargeSignificance = cms.double( -1.0 )
  ),
  ComponentName = cms.string( "hltESPbJetRegionalTrajectoryFilter" )
)
process.hltESPbJetRegionalTrajectoryBuilder = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPbJetRegionalTrajectoryFilter" ),
  maxCand = cms.int32( 1 ),
  ComponentName = cms.string( "hltESPbJetRegionalTrajectoryBuilder" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( False ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltESPTrajectorySmootherRK = cms.ESProducer( "KFTrajectorySmootherESProducer",
  errorRescaling = cms.double( 100.0 ),
  minHits = cms.int32( 3 ),
  ComponentName = cms.string( "hltESPTrajectorySmootherRK" ),
  Estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  Updator = cms.string( "hltESPKFUpdator" ),
  Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
  RecoGeometry = cms.string( "hltESPDummyDetLayerGeometry" )
)
process.hltESPTrajectoryFitterRK = cms.ESProducer( "KFTrajectoryFitterESProducer",
  minHits = cms.int32( 3 ),
  ComponentName = cms.string( "hltESPTrajectoryFitterRK" ),
  Estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  Updator = cms.string( "hltESPKFUpdator" ),
  Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
  RecoGeometry = cms.string( "hltESPDummyDetLayerGeometry" )
)
process.hltESPTrajectoryFilterL3 = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 0.5 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 1 ),
    maxNumberOfHits = cms.int32( 1000000000 ),
    maxConsecLostHits = cms.int32( 1 ),
    minimumNumberOfHits = cms.int32( 5 ),
    nSigmaMinPt = cms.double( 5.0 ),
    chargeSignificance = cms.double( -1.0 )
  ),
  ComponentName = cms.string( "hltESPTrajectoryFilterL3" )
)
process.hltESPTrajectoryFilterIT = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 0.3 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 1 ),
    maxNumberOfHits = cms.int32( 100 ),
    maxConsecLostHits = cms.int32( 1 ),
    minimumNumberOfHits = cms.int32( 3 ),
    nSigmaMinPt = cms.double( 5.0 ),
    chargeSignificance = cms.double( -1.0 )
  ),
  ComponentName = cms.string( "hltESPTrajectoryFilterIT" )
)
process.hltESPTrajectoryCleanerBySharedSeeds = cms.ESProducer( "TrajectoryCleanerESProducer",
  ComponentName = cms.string( "hltESPTrajectoryCleanerBySharedSeeds" ),
  fractionShared = cms.double( 0.5 ),
  ValidHitBonus = cms.double( 5.0 ),
  ComponentType = cms.string( "TrajectoryCleanerBySharedSeeds" ),
  MissingHitPenalty = cms.double( 20.0 ),
  allowSharedFirstHit = cms.bool( True )
)
process.hltESPTrajectoryCleanerBySharedHits = cms.ESProducer( "TrajectoryCleanerESProducer",
  ComponentName = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
  fractionShared = cms.double( 0.5 ),
  ValidHitBonus = cms.double( 5.0 ),
  ComponentType = cms.string( "TrajectoryCleanerBySharedHits" ),
  MissingHitPenalty = cms.double( 20.0 ),
  allowSharedFirstHit = cms.bool( False )
)
process.hltESPTrajectoryBuilderL3 = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPTrajectoryFilterL3" ),
  maxCand = cms.int32( 5 ),
  ComponentName = cms.string( "hltESPTrajectoryBuilderL3" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( False ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltESPTrajectoryBuilderIT = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPTrajectoryFilterIT" ),
  maxCand = cms.int32( 2 ),
  ComponentName = cms.string( "hltESPTrajectoryBuilderIT" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator9" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( False ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltESPTrackerRecoGeometryESProducer = cms.ESProducer( "TrackerRecoGeometryESProducer",
  appendToDataLabel = cms.string( "" ),
  trackerGeometryLabel = cms.untracked.string( "" )
)
process.hltESPTrackCounting3D2nd = cms.ESProducer( "TrackCountingESProducer",
  deltaR = cms.double( -1.0 ),
  maximumDistanceToJetAxis = cms.double( 0.07 ),
  impactParameterType = cms.int32( 0 ),
  trackQualityClass = cms.string( "any" ),
  maximumDecayLength = cms.double( 5.0 ),
  nthTrack = cms.int32( 2 )
)
process.hltESPTrackCounting3D1st = cms.ESProducer( "TrackCountingESProducer",
  deltaR = cms.double( -1.0 ),
  maximumDistanceToJetAxis = cms.double( 0.07 ),
  impactParameterType = cms.int32( 0 ),
  trackQualityClass = cms.string( "any" ),
  maximumDecayLength = cms.double( 5.0 ),
  nthTrack = cms.int32( 1 )
)
process.hltESPTTRHBuilderWithoutAngle4PixelTriplets = cms.ESProducer( "TkTransientTrackingRecHitBuilderESProducer",
  StripCPE = cms.string( "Fake" ),
  Matcher = cms.string( "StandardMatcher" ),
  ComputeCoarseLocalPositionFromDisk = cms.bool( False ),
  PixelCPE = cms.string( "hltESPPixelCPEGeneric" ),
  ComponentName = cms.string( "hltESPTTRHBuilderWithoutAngle4PixelTriplets" )
)
process.hltESPTTRHBuilderPixelOnly = cms.ESProducer( "TkTransientTrackingRecHitBuilderESProducer",
  StripCPE = cms.string( "Fake" ),
  Matcher = cms.string( "StandardMatcher" ),
  ComputeCoarseLocalPositionFromDisk = cms.bool( False ),
  PixelCPE = cms.string( "hltESPPixelCPEGeneric" ),
  ComponentName = cms.string( "hltESPTTRHBuilderPixelOnly" )
)
process.hltESPTTRHBuilderAngleAndTemplate = cms.ESProducer( "TkTransientTrackingRecHitBuilderESProducer",
  StripCPE = cms.string( "StripCPEfromTrackAngle" ),
  Matcher = cms.string( "StandardMatcher" ),
  ComputeCoarseLocalPositionFromDisk = cms.bool( False ),
  PixelCPE = cms.string( "hltESPPixelCPETemplateReco" ),
  ComponentName = cms.string( "hltESPTTRHBuilderAngleAndTemplate" )
)
process.hltESPTTRHBWithTrackAngle = cms.ESProducer( "TkTransientTrackingRecHitBuilderESProducer",
  StripCPE = cms.string( "StripCPEfromTrackAngle" ),
  Matcher = cms.string( "StandardMatcher" ),
  ComputeCoarseLocalPositionFromDisk = cms.bool( False ),
  PixelCPE = cms.string( "hltESPPixelCPEGeneric" ),
  ComponentName = cms.string( "hltESPTTRHBWithTrackAngle" )
)
process.hltESPStraightLinePropagator = cms.ESProducer( "StraightLinePropagatorESProducer",
  ComponentName = cms.string( "hltESPStraightLinePropagator" ),
  PropagationDirection = cms.string( "alongMomentum" )
)
process.hltESPSteppingHelixPropagatorOpposite = cms.ESProducer( "SteppingHelixPropagatorESProducer",
  NoErrorPropagation = cms.bool( False ),
  endcapShiftInZPos = cms.double( 0.0 ),
  PropagationDirection = cms.string( "oppositeToMomentum" ),
  useTuningForL2Speed = cms.bool( False ),
  useIsYokeFlag = cms.bool( True ),
  endcapShiftInZNeg = cms.double( 0.0 ),
  SetVBFPointer = cms.bool( False ),
  AssumeNoMaterial = cms.bool( False ),
  returnTangentPlane = cms.bool( True ),
  useInTeslaFromMagField = cms.bool( False ),
  VBFName = cms.string( "VolumeBasedMagneticField" ),
  useEndcapShiftsInZ = cms.bool( False ),
  sendLogWarning = cms.bool( False ),
  useMatVolumes = cms.bool( True ),
  debug = cms.bool( False ),
  ApplyRadX0Correction = cms.bool( True ),
  useMagVolumes = cms.bool( True ),
  ComponentName = cms.string( "hltESPSteppingHelixPropagatorOpposite" )
)
process.hltESPSteppingHelixPropagatorAlong = cms.ESProducer( "SteppingHelixPropagatorESProducer",
  NoErrorPropagation = cms.bool( False ),
  endcapShiftInZPos = cms.double( 0.0 ),
  PropagationDirection = cms.string( "alongMomentum" ),
  useTuningForL2Speed = cms.bool( False ),
  useIsYokeFlag = cms.bool( True ),
  endcapShiftInZNeg = cms.double( 0.0 ),
  SetVBFPointer = cms.bool( False ),
  AssumeNoMaterial = cms.bool( False ),
  returnTangentPlane = cms.bool( True ),
  useInTeslaFromMagField = cms.bool( False ),
  VBFName = cms.string( "VolumeBasedMagneticField" ),
  useEndcapShiftsInZ = cms.bool( False ),
  sendLogWarning = cms.bool( False ),
  useMatVolumes = cms.bool( True ),
  debug = cms.bool( False ),
  ApplyRadX0Correction = cms.bool( True ),
  useMagVolumes = cms.bool( True ),
  ComponentName = cms.string( "hltESPSteppingHelixPropagatorAlong" )
)
process.hltESPSoftLeptonByPt = cms.ESProducer( "LeptonTaggerByPtESProducer",
  ipSign = cms.string( "any" )
)
process.hltESPSoftLeptonByDistance = cms.ESProducer( "LeptonTaggerByDistanceESProducer",
  distance = cms.double( 0.5 )
)
process.hltESPSmartPropagatorOpposite = cms.ESProducer( "SmartPropagatorESProducer",
  Epsilon = cms.double( 5.0 ),
  TrackerPropagator = cms.string( "PropagatorWithMaterialOpposite" ),
  MuonPropagator = cms.string( "hltESPSteppingHelixPropagatorOpposite" ),
  PropagationDirection = cms.string( "oppositeToMomentum" ),
  ComponentName = cms.string( "hltESPSmartPropagatorOpposite" )
)
process.hltESPSmartPropagatorAnyOpposite = cms.ESProducer( "SmartPropagatorESProducer",
  Epsilon = cms.double( 5.0 ),
  TrackerPropagator = cms.string( "PropagatorWithMaterialOpposite" ),
  MuonPropagator = cms.string( "SteppingHelixPropagatorAny" ),
  PropagationDirection = cms.string( "oppositeToMomentum" ),
  ComponentName = cms.string( "hltESPSmartPropagatorAnyOpposite" )
)
process.hltESPSmartPropagatorAny = cms.ESProducer( "SmartPropagatorESProducer",
  Epsilon = cms.double( 5.0 ),
  TrackerPropagator = cms.string( "PropagatorWithMaterial" ),
  MuonPropagator = cms.string( "SteppingHelixPropagatorAny" ),
  PropagationDirection = cms.string( "alongMomentum" ),
  ComponentName = cms.string( "hltESPSmartPropagatorAny" )
)
process.hltESPSmartPropagator = cms.ESProducer( "SmartPropagatorESProducer",
  Epsilon = cms.double( 5.0 ),
  TrackerPropagator = cms.string( "PropagatorWithMaterial" ),
  MuonPropagator = cms.string( "hltESPSteppingHelixPropagatorAlong" ),
  PropagationDirection = cms.string( "alongMomentum" ),
  ComponentName = cms.string( "hltESPSmartPropagator" )
)
process.hltESPSiStripRegionConnectivity = cms.ESProducer( "SiStripRegionConnectivity",
  EtaDivisions = cms.untracked.uint32( 20 ),
  PhiDivisions = cms.untracked.uint32( 20 ),
  EtaMax = cms.untracked.double( 2.5 )
)
process.hltESPRungeKuttaTrackerPropagator = cms.ESProducer( "PropagatorWithMaterialESProducer",
  PropagationDirection = cms.string( "alongMomentum" ),
  ComponentName = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
  Mass = cms.double( 0.105 ),
  ptMin = cms.double( -1.0 ),
  MaxDPhi = cms.double( 1.6 ),
  useRungeKutta = cms.bool( True )
)
process.hltESPRKTrajectorySmoother = cms.ESProducer( "KFTrajectorySmootherESProducer",
  errorRescaling = cms.double( 100.0 ),
  minHits = cms.int32( 3 ),
  ComponentName = cms.string( "hltESPRKSmoother" ),
  Estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  Updator = cms.string( "hltESPKFUpdator" ),
  Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
  RecoGeometry = cms.string( "hltESPGlobalDetLayerGeometry" )
)
process.hltESPRKTrajectoryFitter = cms.ESProducer( "KFTrajectoryFitterESProducer",
  minHits = cms.int32( 3 ),
  ComponentName = cms.string( "hltESPRKFitter" ),
  Estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  Updator = cms.string( "hltESPKFUpdator" ),
  Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
  RecoGeometry = cms.string( "hltESPGlobalDetLayerGeometry" )
)
process.hltESPPromptTrackCountingESProducer = cms.ESProducer( "PromptTrackCountingESProducer",
  maxImpactParameterSig = cms.double( 999999.0 ),
  deltaR = cms.double( -1.0 ),
  maximumDecayLength = cms.double( 999999.0 ),
  impactParameterType = cms.int32( 0 ),
  trackQualityClass = cms.string( "any" ),
  deltaRmin = cms.double( 0.0 ),
  maxImpactParameter = cms.double( 0.03 ),
  maximumDistanceToJetAxis = cms.double( 999999.0 ),
  nthTrack = cms.int32( -1 )
)
process.hltESPPixelLayerTripletsHITHE = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2+FPix1_pos',
    'BPix1+BPix2+FPix1_neg',
    'BPix1+FPix1_pos+FPix2_pos',
    'BPix1+FPix1_neg+FPix2_neg' ),
  ComponentName = cms.string( "hltESPPixelLayerTripletsHITHE" ),
  TEC = cms.PSet(  ),
  FPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0051 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0036 )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0027 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0060 )
  ),
  TIB = cms.PSet(  ),
  TOB = cms.PSet(  )
)
process.hltESPPixelLayerTripletsHITHB = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2+BPix3' ),
  ComponentName = cms.string( "hltESPPixelLayerTripletsHITHB" ),
  TEC = cms.PSet(  ),
  FPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0051 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0036 )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0027 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0060 )
  ),
  TIB = cms.PSet(  ),
  TOB = cms.PSet(  )
)
process.hltESPPixelLayerTriplets = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2+BPix3',
    'BPix1+BPix2+FPix1_pos',
    'BPix1+BPix2+FPix1_neg',
    'BPix1+FPix1_pos+FPix2_pos',
    'BPix1+FPix1_neg+FPix2_neg' ),
  ComponentName = cms.string( "hltESPPixelLayerTriplets" ),
  TEC = cms.PSet(  ),
  FPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0051 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0036 )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0027 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0060 )
  ),
  TIB = cms.PSet(  ),
  TOB = cms.PSet(  )
)
process.hltESPPixelLayerPairs = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2',
    'BPix1+BPix3',
    'BPix2+BPix3',
    'BPix1+FPix1_pos',
    'BPix1+FPix1_neg',
    'BPix1+FPix2_pos',
    'BPix1+FPix2_neg',
    'BPix2+FPix1_pos',
    'BPix2+FPix1_neg',
    'BPix2+FPix2_pos',
    'BPix2+FPix2_neg',
    'FPix1_pos+FPix2_pos',
    'FPix1_neg+FPix2_neg' ),
  ComponentName = cms.string( "hltESPPixelLayerPairs" ),
  TEC = cms.PSet(  ),
  FPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0051 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0036 )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0027 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0060 )
  ),
  TIB = cms.PSet(  ),
  TOB = cms.PSet(  )
)
process.hltESPPixelCPETemplateReco = cms.ESProducer( "PixelCPETemplateRecoESProducer",
  DoCosmics = cms.bool( False ),
  LoadTemplatesFromDB = cms.bool( True ),
  ComponentName = cms.string( "hltESPPixelCPETemplateReco" ),
  Alpha2Order = cms.bool( True ),
  ClusterProbComputationFlag = cms.int32( 0 ),
  speed = cms.int32( -2 ),
  UseClusterSplitter = cms.bool( False )
)
process.hltESPPixelCPEGeneric = cms.ESProducer( "PixelCPEGenericESProducer",
  EdgeClusterErrorX = cms.double( 50.0 ),
  DoCosmics = cms.bool( False ),
  LoadTemplatesFromDB = cms.bool( True ),
  UseErrorsFromTemplates = cms.bool( True ),
  eff_charge_cut_highX = cms.double( 1.0 ),
  TruncatePixelCharge = cms.bool( True ),
  size_cutY = cms.double( 3.0 ),
  size_cutX = cms.double( 3.0 ),
  inflate_all_errors_no_trk_angle = cms.bool( False ),
  IrradiationBiasCorrection = cms.bool( False ),
  TanLorentzAnglePerTesla = cms.double( 0.106 ),
  inflate_errors = cms.bool( False ),
  eff_charge_cut_lowX = cms.double( 0.0 ),
  eff_charge_cut_highY = cms.double( 1.0 ),
  ClusterProbComputationFlag = cms.int32( 0 ),
  EdgeClusterErrorY = cms.double( 85.0 ),
  ComponentName = cms.string( "hltESPPixelCPEGeneric" ),
  eff_charge_cut_lowY = cms.double( 0.0 ),
  PixelErrorParametrization = cms.string( "NOTcmsim" ),
  Alpha2Order = cms.bool( True )
)
process.hltESPMuonTransientTrackingRecHitBuilder = cms.ESProducer( "MuonTransientTrackingRecHitBuilderESProducer",
  ComponentName = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" )
)
process.hltESPMuonDetLayerGeometryESProducer = cms.ESProducer( "MuonDetLayerGeometryESProducer" )
process.hltESPMuonCkfTrajectoryFilter = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 0.9 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 1 ),
    maxNumberOfHits = cms.int32( -1 ),
    maxConsecLostHits = cms.int32( 1 ),
    chargeSignificance = cms.double( -1.0 ),
    nSigmaMinPt = cms.double( 5.0 ),
    minimumNumberOfHits = cms.int32( 5 )
  ),
  ComponentName = cms.string( "hltESPMuonCkfTrajectoryFilter" )
)
process.hltESPMuonCkfTrajectoryBuilderSeedHit = cms.ESProducer( "MuonCkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPMuonCkfTrajectoryFilter" ),
  maxCand = cms.int32( 5 ),
  ComponentName = cms.string( "hltESPMuonCkfTrajectoryBuilderSeedHit" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  useSeedLayer = cms.bool( True ),
  deltaEta = cms.double( 0.1 ),
  deltaPhi = cms.double( 0.1 ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  rescaleErrorIfFail = cms.double( 1.0 ),
  propagatorProximity = cms.string( "SteppingHelixPropagatorAny" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( True ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
  intermediateCleaning = cms.bool( False ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltESPMuonCkfTrajectoryBuilder = cms.ESProducer( "MuonCkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPMuonCkfTrajectoryFilter" ),
  maxCand = cms.int32( 5 ),
  ComponentName = cms.string( "hltESPMuonCkfTrajectoryBuilder" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  useSeedLayer = cms.bool( False ),
  deltaEta = cms.double( 0.1 ),
  deltaPhi = cms.double( 0.1 ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  rescaleErrorIfFail = cms.double( 1.0 ),
  propagatorProximity = cms.string( "SteppingHelixPropagatorAny" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( True ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
  intermediateCleaning = cms.bool( False ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltESPMuTrackJpsiTrajectoryFilter = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 1.0 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 1 ),
    maxNumberOfHits = cms.int32( 8 ),
    maxConsecLostHits = cms.int32( 1 ),
    minimumNumberOfHits = cms.int32( 5 ),
    nSigmaMinPt = cms.double( 5.0 ),
    chargeSignificance = cms.double( -1.0 )
  ),
  ComponentName = cms.string( "hltESPMuTrackJpsiTrajectoryFilter" )
)
process.hltESPMuTrackJpsiTrajectoryBuilder = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPMuTrackJpsiTrajectoryFilter" ),
  maxCand = cms.int32( 1 ),
  ComponentName = cms.string( "hltESPMuTrackJpsiTrajectoryBuilder" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( False ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltESPMixedLayerPairs = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2',
    'BPix1+BPix3',
    'BPix2+BPix3',
    'BPix1+FPix1_pos',
    'BPix1+FPix1_neg',
    'BPix1+FPix2_pos',
    'BPix1+FPix2_neg',
    'BPix2+FPix1_pos',
    'BPix2+FPix1_neg',
    'BPix2+FPix2_pos',
    'BPix2+FPix2_neg',
    'FPix1_pos+FPix2_pos',
    'FPix1_neg+FPix2_neg',
    'FPix2_pos+TEC1_pos',
    'FPix2_pos+TEC2_pos',
    'TEC1_pos+TEC2_pos',
    'TEC2_pos+TEC3_pos',
    'FPix2_neg+TEC1_neg',
    'FPix2_neg+TEC2_neg',
    'TEC1_neg+TEC2_neg',
    'TEC2_neg+TEC3_neg' ),
  ComponentName = cms.string( "hltESPMixedLayerPairs" ),
  TEC = cms.PSet( 
    useRingSlector = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    minRing = cms.int32( 1 ),
    maxRing = cms.int32( 1 )
  ),
  FPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0051 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0036 )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0027 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltSiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0060 )
  ),
  TIB = cms.PSet(  ),
  TOB = cms.PSet(  )
)
process.hltESPMeasurementTrackerForHI = cms.ESProducer( "MeasurementTrackerESProducer",
  StripCPE = cms.string( "StripCPEfromTrackAngle" ),
  inactivePixelDetectorLabels = cms.VInputTag(  ),
  PixelCPE = cms.string( "hltESPPixelCPEGeneric" ),
  stripLazyGetterProducer = cms.string( "hltSiStripRawToClustersFacility" ),
  OnDemand = cms.bool( False ),
  Regional = cms.bool( False ),
  UsePixelModuleQualityDB = cms.bool( True ),
  pixelClusterProducer = cms.string( "hltHISiPixelClusters" ),
  switchOffPixelsIfEmpty = cms.bool( True ),
  inactiveStripDetectorLabels = cms.VInputTag( 'hltSiStripRawToDigi' ),
  MaskBadAPVFibers = cms.bool( True ),
  UseStripStripQualityDB = cms.bool( True ),
  UsePixelROCQualityDB = cms.bool( True ),
  DebugPixelROCQualityDB = cms.untracked.bool( False ),
  UseStripAPVFiberQualityDB = cms.bool( True ),
  stripClusterProducer = cms.string( "hltHISiStripClustersNonRegional" ),
  DebugStripAPVFiberQualityDB = cms.untracked.bool( False ),
  DebugStripStripQualityDB = cms.untracked.bool( False ),
  SiStripQualityLabel = cms.string( "" ),
  badStripCuts = cms.PSet( 
    TOB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 2 ),
      maxBad = cms.uint32( 4 )
    ),
    TID = cms.PSet( 
      maxBad = cms.uint32( 4 ),
      maxConsecutiveBad = cms.uint32( 2 )
    ),
    TEC = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 2 ),
      maxBad = cms.uint32( 4 )
    ),
    TIB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 2 ),
      maxBad = cms.uint32( 4 )
    )
  ),
  DebugStripModuleQualityDB = cms.untracked.bool( False ),
  ComponentName = cms.string( "hltESPMeasurementTrackerForHI" ),
  DebugPixelModuleQualityDB = cms.untracked.bool( False ),
  HitMatcher = cms.string( "StandardMatcher" ),
  skipClusters = cms.InputTag( "" ),
  UseStripModuleQualityDB = cms.bool( True ),
  UseStripNoiseDB = cms.bool( False ),
  UseStripCablingDB = cms.bool( False )
)
process.hltESPMeasurementTracker = cms.ESProducer( "MeasurementTrackerESProducer",
  StripCPE = cms.string( "StripCPEfromTrackAngle" ),
  inactivePixelDetectorLabels = cms.VInputTag(  ),
  PixelCPE = cms.string( "hltESPPixelCPEGeneric" ),
  stripLazyGetterProducer = cms.string( "hltSiStripRawToClustersFacility" ),
  OnDemand = cms.bool( True ),
  Regional = cms.bool( True ),
  UsePixelModuleQualityDB = cms.bool( True ),
  pixelClusterProducer = cms.string( "hltSiPixelClusters" ),
  switchOffPixelsIfEmpty = cms.bool( True ),
  inactiveStripDetectorLabels = cms.VInputTag( 'hltSiStripExcludedFEDListProducer' ),
  MaskBadAPVFibers = cms.bool( True ),
  UseStripStripQualityDB = cms.bool( True ),
  UsePixelROCQualityDB = cms.bool( True ),
  DebugPixelROCQualityDB = cms.untracked.bool( False ),
  UseStripAPVFiberQualityDB = cms.bool( True ),
  stripClusterProducer = cms.string( "hltSiStripClusters" ),
  DebugStripAPVFiberQualityDB = cms.untracked.bool( False ),
  DebugStripStripQualityDB = cms.untracked.bool( False ),
  SiStripQualityLabel = cms.string( "" ),
  badStripCuts = cms.PSet( 
    TOB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TID = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TEC = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    ),
    TIB = cms.PSet( 
      maxConsecutiveBad = cms.uint32( 9999 ),
      maxBad = cms.uint32( 9999 )
    )
  ),
  DebugStripModuleQualityDB = cms.untracked.bool( False ),
  ComponentName = cms.string( "hltESPMeasurementTracker" ),
  DebugPixelModuleQualityDB = cms.untracked.bool( False ),
  HitMatcher = cms.string( "StandardMatcher" ),
  skipClusters = cms.InputTag( "" ),
  UseStripModuleQualityDB = cms.bool( True ),
  UseStripNoiseDB = cms.bool( False ),
  UseStripCablingDB = cms.bool( False )
)
process.hltESPL3MuKFTrajectoryFitter = cms.ESProducer( "KFTrajectoryFitterESProducer",
  minHits = cms.int32( 3 ),
  ComponentName = cms.string( "hltESPL3MuKFTrajectoryFitter" ),
  Estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  Updator = cms.string( "hltESPKFUpdator" ),
  Propagator = cms.string( "hltESPSmartPropagatorAny" ),
  RecoGeometry = cms.string( "hltESPDummyDetLayerGeometry" )
)
process.hltESPL3AbsoluteCorrectionESProducer = cms.ESProducer( "LXXXCorrectionESProducer",
  appendToDataLabel = cms.string( "" ),
  algorithm = cms.string( "AK5Calo" ),
  level = cms.string( "L3Absolute" )
)
process.hltESPL2RelativeCorrectionESProducer = cms.ESProducer( "LXXXCorrectionESProducer",
  appendToDataLabel = cms.string( "" ),
  algorithm = cms.string( "AK5Calo" ),
  level = cms.string( "L2Relative" )
)
process.hltESPL1FastJetCorrectionESProducer = cms.ESProducer( "L1FastjetCorrectionESProducer",
  appendToDataLabel = cms.string( "" ),
  srcRho = cms.InputTag( 'hltKT6CaloJets','rho' ),
  algorithm = cms.string( "AK5Calo" ),
  level = cms.string( "L1FastJet" )
)
process.hltESPKFUpdator = cms.ESProducer( "KFUpdatorESProducer",
  ComponentName = cms.string( "hltESPKFUpdator" )
)
process.hltESPKFTrajectorySmootherForMuonTrackLoader = cms.ESProducer( "KFTrajectorySmootherESProducer",
  errorRescaling = cms.double( 10.0 ),
  minHits = cms.int32( 3 ),
  ComponentName = cms.string( "hltESPKFTrajectorySmootherForMuonTrackLoader" ),
  Estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  Updator = cms.string( "hltESPKFUpdator" ),
  Propagator = cms.string( "hltESPSmartPropagatorAnyOpposite" ),
  RecoGeometry = cms.string( "hltESPDummyDetLayerGeometry" )
)
process.hltESPKFTrajectorySmootherForL2Muon = cms.ESProducer( "KFTrajectorySmootherESProducer",
  errorRescaling = cms.double( 100.0 ),
  minHits = cms.int32( 3 ),
  ComponentName = cms.string( "hltESPKFTrajectorySmootherForL2Muon" ),
  Estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  Updator = cms.string( "hltESPKFUpdator" ),
  Propagator = cms.string( "hltESPFastSteppingHelixPropagatorOpposite" ),
  RecoGeometry = cms.string( "hltESPDummyDetLayerGeometry" )
)
process.hltESPKFTrajectorySmoother = cms.ESProducer( "KFTrajectorySmootherESProducer",
  errorRescaling = cms.double( 100.0 ),
  minHits = cms.int32( 3 ),
  ComponentName = cms.string( "hltESPKFTrajectorySmoother" ),
  Estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  Updator = cms.string( "hltESPKFUpdator" ),
  Propagator = cms.string( "PropagatorWithMaterial" ),
  RecoGeometry = cms.string( "hltESPDummyDetLayerGeometry" )
)
process.hltESPKFTrajectoryFitterForL2Muon = cms.ESProducer( "KFTrajectoryFitterESProducer",
  minHits = cms.int32( 3 ),
  ComponentName = cms.string( "hltESPKFTrajectoryFitterForL2Muon" ),
  Estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  Updator = cms.string( "hltESPKFUpdator" ),
  Propagator = cms.string( "hltESPFastSteppingHelixPropagatorAny" ),
  RecoGeometry = cms.string( "hltESPDummyDetLayerGeometry" )
)
process.hltESPKFTrajectoryFitter = cms.ESProducer( "KFTrajectoryFitterESProducer",
  minHits = cms.int32( 3 ),
  ComponentName = cms.string( "hltESPKFTrajectoryFitter" ),
  Estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  Updator = cms.string( "hltESPKFUpdator" ),
  Propagator = cms.string( "PropagatorWithMaterial" ),
  RecoGeometry = cms.string( "hltESPDummyDetLayerGeometry" )
)
process.hltESPKFFittingSmootherWithOutliersRejectionAndRK = cms.ESProducer( "KFFittingSmootherESProducer",
  EstimateCut = cms.double( 20.0 ),
  LogPixelProbabilityCut = cms.double( -14.0 ),
  Fitter = cms.string( "hltESPRKFitter" ),
  MinNumberOfHits = cms.int32( 3 ),
  Smoother = cms.string( "hltESPRKSmoother" ),
  BreakTrajWith2ConsecutiveMissing = cms.bool( True ),
  ComponentName = cms.string( "hltESPKFFittingSmootherWithOutliersRejectionAndRK" ),
  NoInvalidHitsBeginEnd = cms.bool( True ),
  RejectTracks = cms.bool( True )
)
process.hltESPKFFittingSmootherForL2Muon = cms.ESProducer( "KFFittingSmootherESProducer",
  EstimateCut = cms.double( -1.0 ),
  LogPixelProbabilityCut = cms.double( -16.0 ),
  Fitter = cms.string( "hltESPKFTrajectoryFitterForL2Muon" ),
  MinNumberOfHits = cms.int32( 5 ),
  Smoother = cms.string( "hltESPKFTrajectorySmootherForL2Muon" ),
  BreakTrajWith2ConsecutiveMissing = cms.bool( False ),
  ComponentName = cms.string( "hltESPKFFittingSmootherForL2Muon" ),
  NoInvalidHitsBeginEnd = cms.bool( False ),
  RejectTracks = cms.bool( True )
)
process.hltESPKFFittingSmoother = cms.ESProducer( "KFFittingSmootherESProducer",
  EstimateCut = cms.double( -1.0 ),
  LogPixelProbabilityCut = cms.double( -16.0 ),
  Fitter = cms.string( "hltESPKFTrajectoryFitter" ),
  MinNumberOfHits = cms.int32( 5 ),
  Smoother = cms.string( "hltESPKFTrajectorySmoother" ),
  BreakTrajWith2ConsecutiveMissing = cms.bool( False ),
  ComponentName = cms.string( "hltESPKFFittingSmoother" ),
  NoInvalidHitsBeginEnd = cms.bool( False ),
  RejectTracks = cms.bool( True )
)
process.hltESPHITTRHBuilderWithoutRefit = cms.ESProducer( "TkTransientTrackingRecHitBuilderESProducer",
  StripCPE = cms.string( "Fake" ),
  Matcher = cms.string( "Fake" ),
  ComputeCoarseLocalPositionFromDisk = cms.bool( False ),
  PixelCPE = cms.string( "Fake" ),
  ComponentName = cms.string( "hltESPHITTRHBuilderWithoutRefit" )
)
process.hltESPHIPixelLayerTriplets = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2+BPix3',
    'BPix1+BPix2+FPix1_pos',
    'BPix1+BPix2+FPix1_neg',
    'BPix1+FPix1_pos+FPix2_pos',
    'BPix1+FPix1_neg+FPix2_neg' ),
  ComponentName = cms.string( "hltESPHIPixelLayerTriplets" ),
  TEC = cms.PSet(  ),
  FPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0051 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltHISiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0036 )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0027 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltHISiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0060 )
  ),
  TIB = cms.PSet(  ),
  TOB = cms.PSet(  )
)
process.hltESPHIPixelLayerPairs = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2',
    'BPix1+BPix3',
    'BPix2+BPix3',
    'BPix1+FPix1_pos',
    'BPix1+FPix1_neg',
    'BPix1+FPix2_pos',
    'BPix1+FPix2_neg',
    'BPix2+FPix1_pos',
    'BPix2+FPix1_neg',
    'BPix2+FPix2_pos',
    'BPix2+FPix2_neg',
    'FPix1_pos+FPix2_pos',
    'FPix1_neg+FPix2_neg' ),
  ComponentName = cms.string( "hltESPHIPixelLayerPairs" ),
  TEC = cms.PSet(  ),
  FPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0051 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltHISiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0036 )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    useErrorsFromParam = cms.bool( True ),
    hitErrorRPhi = cms.double( 0.0027 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltHISiPixelRecHits" ),
    hitErrorRZ = cms.double( 0.0060 )
  ),
  TIB = cms.PSet(  ),
  TOB = cms.PSet(  )
)
process.hltESPHIMixedLayerPairs = cms.ESProducer( "SeedingLayersESProducer",
  layerList = cms.vstring( 'BPix1+BPix2',
    'BPix1+BPix3',
    'BPix2+BPix3',
    'BPix1+FPix1_pos',
    'BPix1+FPix1_neg',
    'BPix1+FPix2_pos',
    'BPix1+FPix2_neg',
    'BPix2+FPix1_pos',
    'BPix2+FPix1_neg',
    'BPix2+FPix2_pos',
    'BPix2+FPix2_neg',
    'FPix1_pos+FPix2_pos',
    'FPix1_neg+FPix2_neg',
    'FPix2_pos+TEC1_pos',
    'FPix2_pos+TEC2_pos',
    'TEC1_pos+TEC2_pos',
    'TEC2_pos+TEC3_pos',
    'FPix2_neg+TEC1_neg',
    'FPix2_neg+TEC2_neg',
    'TEC1_neg+TEC2_neg',
    'TEC2_neg+TEC3_neg' ),
  ComponentName = cms.string( "hltESPHIMixedLayerPairs" ),
  TEC = cms.PSet( 
    useRingSlector = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    minRing = cms.int32( 1 ),
    maxRing = cms.int32( 1 )
  ),
  FPix = cms.PSet( 
    hitErrorRZ = cms.double( 0.0036 ),
    hitErrorRPhi = cms.double( 0.0051 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltHISiPixelRecHits" ),
    useErrorsFromParam = cms.bool( True )
  ),
  TID = cms.PSet(  ),
  BPix = cms.PSet( 
    hitErrorRZ = cms.double( 0.0060 ),
    hitErrorRPhi = cms.double( 0.0027 ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    HitProducer = cms.string( "hltHISiPixelRecHits" ),
    useErrorsFromParam = cms.bool( True )
  ),
  TIB = cms.PSet(  ),
  TOB = cms.PSet(  )
)
process.hltESPGlobalTrackingGeometryESProducer = cms.ESProducer( "GlobalTrackingGeometryESProducer" )
process.hltESPGlobalDetLayerGeometry = cms.ESProducer( "GlobalDetLayerGeometryESProducer",
  ComponentName = cms.string( "hltESPGlobalDetLayerGeometry" )
)
process.hltESPFittingSmootherRK = cms.ESProducer( "KFFittingSmootherESProducer",
  EstimateCut = cms.double( -1.0 ),
  LogPixelProbabilityCut = cms.double( -16.0 ),
  Fitter = cms.string( "hltESPTrajectoryFitterRK" ),
  MinNumberOfHits = cms.int32( 5 ),
  Smoother = cms.string( "hltESPTrajectorySmootherRK" ),
  BreakTrajWith2ConsecutiveMissing = cms.bool( False ),
  ComponentName = cms.string( "hltESPFittingSmootherRK" ),
  NoInvalidHitsBeginEnd = cms.bool( False ),
  RejectTracks = cms.bool( True )
)
process.hltESPFittingSmootherIT = cms.ESProducer( "KFFittingSmootherESProducer",
  EstimateCut = cms.double( 10.0 ),
  LogPixelProbabilityCut = cms.double( -16.0 ),
  Fitter = cms.string( "hltESPTrajectoryFitterRK" ),
  MinNumberOfHits = cms.int32( 3 ),
  Smoother = cms.string( "hltESPTrajectorySmootherRK" ),
  BreakTrajWith2ConsecutiveMissing = cms.bool( True ),
  ComponentName = cms.string( "hltESPFittingSmootherIT" ),
  NoInvalidHitsBeginEnd = cms.bool( True ),
  RejectTracks = cms.bool( True )
)
process.hltESPFastSteppingHelixPropagatorOpposite = cms.ESProducer( "SteppingHelixPropagatorESProducer",
  NoErrorPropagation = cms.bool( False ),
  endcapShiftInZPos = cms.double( 0.0 ),
  PropagationDirection = cms.string( "oppositeToMomentum" ),
  useTuningForL2Speed = cms.bool( True ),
  useIsYokeFlag = cms.bool( True ),
  endcapShiftInZNeg = cms.double( 0.0 ),
  SetVBFPointer = cms.bool( False ),
  AssumeNoMaterial = cms.bool( False ),
  returnTangentPlane = cms.bool( True ),
  useInTeslaFromMagField = cms.bool( False ),
  VBFName = cms.string( "VolumeBasedMagneticField" ),
  useEndcapShiftsInZ = cms.bool( False ),
  sendLogWarning = cms.bool( False ),
  useMatVolumes = cms.bool( True ),
  debug = cms.bool( False ),
  ApplyRadX0Correction = cms.bool( True ),
  useMagVolumes = cms.bool( True ),
  ComponentName = cms.string( "hltESPFastSteppingHelixPropagatorOpposite" )
)
process.hltESPFastSteppingHelixPropagatorAny = cms.ESProducer( "SteppingHelixPropagatorESProducer",
  NoErrorPropagation = cms.bool( False ),
  endcapShiftInZPos = cms.double( 0.0 ),
  PropagationDirection = cms.string( "anyDirection" ),
  useTuningForL2Speed = cms.bool( True ),
  useIsYokeFlag = cms.bool( True ),
  endcapShiftInZNeg = cms.double( 0.0 ),
  SetVBFPointer = cms.bool( False ),
  AssumeNoMaterial = cms.bool( False ),
  returnTangentPlane = cms.bool( True ),
  useInTeslaFromMagField = cms.bool( False ),
  VBFName = cms.string( "VolumeBasedMagneticField" ),
  useEndcapShiftsInZ = cms.bool( False ),
  sendLogWarning = cms.bool( False ),
  useMatVolumes = cms.bool( True ),
  debug = cms.bool( False ),
  ApplyRadX0Correction = cms.bool( True ),
  useMagVolumes = cms.bool( True ),
  ComponentName = cms.string( "hltESPFastSteppingHelixPropagatorAny" )
)
process.hltESPEcalTrigTowerConstituentsMapBuilder = cms.ESProducer( "EcalTrigTowerConstituentsMapBuilder",
  MapFile = cms.untracked.string( "Geometry/EcalMapping/data/EndCap_TTMap.txt" )
)
process.hltESPEcalRegionCablingESProducer = cms.ESProducer( "EcalRegionCablingESProducer",
  esMapping = cms.PSet(  LookupTable = cms.FileInPath( "EventFilter/ESDigiToRaw/data/ES_lookup_table.dat" ) )
)
process.hltESPESUnpackerWorker = cms.ESProducer( "ESUnpackerWorkerESProducer",
  RHAlgo = cms.PSet( 
    ESRecoAlgo = cms.int32( 0 ),
    Type = cms.string( "ESRecHitWorker" )
  ),
  DCCDataUnpacker = cms.PSet(  LookupTable = cms.FileInPath( "EventFilter/ESDigiToRaw/data/ES_lookup_table.dat" ) ),
  ComponentName = cms.string( "hltESPESUnpackerWorker" )
)
process.hltESPDummyDetLayerGeometry = cms.ESProducer( "DetLayerGeometryESProducer",
  ComponentName = cms.string( "hltESPDummyDetLayerGeometry" )
)
process.hltESPCkfTrajectoryFilterForHI = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minimumNumberOfHits = cms.int32( 6 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 1 ),
    maxNumberOfHits = cms.int32( -1 ),
    maxConsecLostHits = cms.int32( 1 ),
    chargeSignificance = cms.double( -1.0 ),
    nSigmaMinPt = cms.double( 5.0 ),
    minPt = cms.double( 11.0 )
  ),
  ComponentName = cms.string( "hltESPCkfTrajectoryFilterForHI" )
)
process.hltESPCkfTrajectoryFilter = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 0.9 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 1 ),
    maxNumberOfHits = cms.int32( -1 ),
    maxConsecLostHits = cms.int32( 1 ),
    minimumNumberOfHits = cms.int32( 5 ),
    nSigmaMinPt = cms.double( 5.0 ),
    chargeSignificance = cms.double( -1.0 )
  ),
  ComponentName = cms.string( "hltESPCkfTrajectoryFilter" )
)
process.hltESPCkfTrajectoryBuilderForHI = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterialForHI" ),
  trajectoryFilterName = cms.string( "hltESPCkfTrajectoryFilterForHI" ),
  maxCand = cms.int32( 5 ),
  ComponentName = cms.string( "hltESPCkfTrajectoryBuilderForHI" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOppositeForHI" ),
  MeasurementTrackerName = cms.string( "hltESPMeasurementTrackerForHI" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( False ),
  intermediateCleaning = cms.bool( False ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltESPCkfTrajectoryBuilder = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPCkfTrajectoryFilter" ),
  maxCand = cms.int32( 5 ),
  ComponentName = cms.string( "hltESPCkfTrajectoryBuilder" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( True ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltESPCkf3HitTrajectoryFilter = cms.ESProducer( "TrajectoryFilterESProducer",
  filterPset = cms.PSet( 
    minPt = cms.double( 0.9 ),
    minHitsMinPt = cms.int32( 3 ),
    ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
    maxLostHits = cms.int32( 1 ),
    maxNumberOfHits = cms.int32( -1 ),
    maxConsecLostHits = cms.int32( 1 ),
    minimumNumberOfHits = cms.int32( 3 ),
    nSigmaMinPt = cms.double( 5.0 ),
    chargeSignificance = cms.double( -1.0 )
  ),
  ComponentName = cms.string( "hltESPCkf3HitTrajectoryFilter" )
)
process.hltESPCkf3HitTrajectoryBuilder = cms.ESProducer( "CkfTrajectoryBuilderESProducer",
  propagatorAlong = cms.string( "PropagatorWithMaterial" ),
  trajectoryFilterName = cms.string( "hltESPCkf3HitTrajectoryFilter" ),
  maxCand = cms.int32( 5 ),
  ComponentName = cms.string( "hltESPCkf3HitTrajectoryBuilder" ),
  propagatorOpposite = cms.string( "PropagatorWithMaterialOpposite" ),
  MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
  estimator = cms.string( "hltESPChi2MeasurementEstimator" ),
  TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
  updator = cms.string( "hltESPKFUpdator" ),
  alwaysUseInvalidHits = cms.bool( True ),
  intermediateCleaning = cms.bool( True ),
  lostHitPenalty = cms.double( 30.0 )
)
process.hltESPChi2MeasurementEstimator9 = cms.ESProducer( "Chi2MeasurementEstimatorESProducer",
  MaxChi2 = cms.double( 9.0 ),
  nSigma = cms.double( 3.0 ),
  ComponentName = cms.string( "hltESPChi2MeasurementEstimator9" )
)
process.hltESPChi2MeasurementEstimator16 = cms.ESProducer( "Chi2MeasurementEstimatorESProducer",
  MaxChi2 = cms.double( 16.0 ),
  nSigma = cms.double( 3.0 ),
  ComponentName = cms.string( "hltESPChi2MeasurementEstimator16" )
)
process.hltESPChi2MeasurementEstimator = cms.ESProducer( "Chi2MeasurementEstimatorESProducer",
  MaxChi2 = cms.double( 30.0 ),
  nSigma = cms.double( 3.0 ),
  ComponentName = cms.string( "hltESPChi2MeasurementEstimator" )
)
process.hltESPChi2EstimatorForRefit = cms.ESProducer( "Chi2MeasurementEstimatorESProducer",
  MaxChi2 = cms.double( 100000.0 ),
  nSigma = cms.double( 3.0 ),
  ComponentName = cms.string( "hltESPChi2EstimatorForRefit" )
)
process.hltESPAnalyticalPropagator = cms.ESProducer( "AnalyticalPropagatorESProducer",
  MaxDPhi = cms.double( 1.6 ),
  ComponentName = cms.string( "hltESPAnalyticalPropagator" ),
  PropagationDirection = cms.string( "alongMomentum" )
)
process.hltESPAK5CaloL2L3 = cms.ESProducer( "JetCorrectionESChain",
  correctors = cms.vstring( 'hltESPL2RelativeCorrectionESProducer',
    'hltESPL3AbsoluteCorrectionESProducer' ),
  appendToDataLabel = cms.string( "" )
)
process.hltESPAK5CaloL1L2L3 = cms.ESProducer( "JetCorrectionESChain",
  correctors = cms.vstring( 'hltESPL1FastJetCorrectionESProducer',
    'hltESPL2RelativeCorrectionESProducer',
    'hltESPL3AbsoluteCorrectionESProducer' ),
  appendToDataLabel = cms.string( "" )
)
process.hcal_db_producer = cms.ESProducer( "HcalDbProducer" )
process.hcalRecAlgos = cms.ESProducer( "HcalRecAlgoESProducer",
  RecoveredRecHitBits = cms.vstring( 'TimingAddedBit',
    'TimingSubtractedBit' ),
  SeverityLevels = cms.VPSet( 
    cms.PSet(  RecHitFlags = cms.vstring(  ),
      ChannelStatus = cms.vstring(  ),
      Level = cms.int32( 0 )
    ),
    cms.PSet(  RecHitFlags = cms.vstring(  ),
      ChannelStatus = cms.vstring( 'HcalCellCaloTowerProb' ),
      Level = cms.int32( 1 )
    ),
    cms.PSet(  RecHitFlags = cms.vstring( 'HSCP_R1R2',
  'HSCP_FracLeader',
  'HSCP_OuterEnergy',
  'HSCP_ExpFit',
  'ADCSaturationBit' ),
      ChannelStatus = cms.vstring(  ),
      Level = cms.int32( 5 )
    ),
    cms.PSet(  RecHitFlags = cms.vstring( 'HBHEHpdHitMultiplicity',
  'HFDigiTime',
  'HBHEPulseShape',
  'HOBit',
  'HFInTimeWindow',
  'ZDCBit',
  'CalibrationBit',
  'TimingErrorBit' ),
      ChannelStatus = cms.vstring(  ),
      Level = cms.int32( 8 )
    ),
    cms.PSet(  RecHitFlags = cms.vstring( 'HFLongShort',
  'HFS8S1Ratio',
  'HFPET' ),
      ChannelStatus = cms.vstring(  ),
      Level = cms.int32( 11 )
    ),
    cms.PSet(  RecHitFlags = cms.vstring(  ),
      ChannelStatus = cms.vstring( 'HcalCellCaloTowerMask' ),
      Level = cms.int32( 12 )
    ),
    cms.PSet(  RecHitFlags = cms.vstring(  ),
      ChannelStatus = cms.vstring( 'HcalCellHot' ),
      Level = cms.int32( 15 )
    ),
    cms.PSet(  RecHitFlags = cms.vstring(  ),
      ChannelStatus = cms.vstring( 'HcalCellOff',
        'HcalCellDead' ),
      Level = cms.int32( 20 )
    )
  ),
  DropChannelStatusBits = cms.vstring( 'HcalCellMask',
    'HcalCellOff',
    'HcalCellDead' )
)
process.hcalDetIdAssociator = cms.ESProducer( "DetIdAssociatorESProducer",
  ComponentName = cms.string( "HcalDetIdAssociator" ),
  etaBinSize = cms.double( 0.087 ),
  nEta = cms.int32( 70 ),
  nPhi = cms.int32( 72 ),
  includeBadChambers = cms.bool( False )
)
process.ecalSeverityLevel = cms.ESProducer( "EcalSeverityLevelESProducer",
  dbstatusMask = cms.PSet( 
    kGood = cms.vuint32( 0 ),
    kProblematic = cms.vuint32( 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ),
    kRecovered = cms.vuint32(  ),
    kTime = cms.vuint32(  ),
    kWeird = cms.vuint32(  ),
    kBad = cms.vuint32( 11, 12, 13, 14, 15, 16 )
  ),
  timeThresh = cms.double( 2.0 ),
  flagMask = cms.PSet( 
    kGood = cms.vstring( 'kGood' ),
    kProblematic = cms.vstring( 'kPoorReco',
      'kPoorCalib',
      'kNoisy',
      'kSaturated' ),
    kRecovered = cms.vstring( 'kLeadingEdgeRecovered',
      'kTowerRecovered' ),
    kTime = cms.vstring( 'kOutOfTime' ),
    kWeird = cms.vstring( 'kWeird',
      'kDiWeird' ),
    kBad = cms.vstring( 'kFaultyHardware',
      'kDead',
      'kKilled' )
  )
)
process.ecalDetIdAssociator = cms.ESProducer( "DetIdAssociatorESProducer",
  ComponentName = cms.string( "EcalDetIdAssociator" ),
  etaBinSize = cms.double( 0.02 ),
  nEta = cms.int32( 300 ),
  nPhi = cms.int32( 360 ),
  includeBadChambers = cms.bool( False )
)
process.cosmicsNavigationSchoolESProducer = cms.ESProducer( "NavigationSchoolESProducer",
  ComponentName = cms.string( "CosmicNavigationSchool" )
)
process.caloDetIdAssociator = cms.ESProducer( "DetIdAssociatorESProducer",
  ComponentName = cms.string( "CaloDetIdAssociator" ),
  etaBinSize = cms.double( 0.087 ),
  nEta = cms.int32( 70 ),
  nPhi = cms.int32( 72 ),
  includeBadChambers = cms.bool( False )
)
process.ZdcGeometryFromDBEP = cms.ESProducer( "ZdcGeometryFromDBEP",
  applyAlignment = cms.bool( False )
)
process.VBF40 = cms.ESProducer( "VolumeBasedMagneticFieldESProducer",
  scalingVolumes = cms.vint32(  ),
  overrideMasterSector = cms.bool( True ),
  useParametrizedTrackerField = cms.bool( True ),
  scalingFactors = cms.vdouble(  ),
  label = cms.untracked.string( "071212_4t" ),
  version = cms.string( "grid_1103l_071212_4t" ),
  debugBuilder = cms.untracked.bool( False ),
  paramLabel = cms.string( "slave_40" ),
  cacheLastVolume = cms.untracked.bool( True )
)
process.VBF38 = cms.ESProducer( "VolumeBasedMagneticFieldESProducer",
  scalingVolumes = cms.vint32( 14100, 14200, 17600, 17800, 17900, 18100, 18300, 18400, 18600, 23100, 23300, 23400, 23600, 23800, 23900, 24100, 28600, 28800, 28900, 29100, 29300, 29400, 29600, 28609, 28809, 28909, 29109, 29309, 29409, 29609, 28610, 28810, 28910, 29110, 29310, 29410, 29610, 28611, 28811, 28911, 29111, 29311, 29411, 29611 ),
  overrideMasterSector = cms.bool( False ),
  useParametrizedTrackerField = cms.bool( True ),
  scalingFactors = cms.vdouble( 1.0, 1.0, 0.994, 1.004, 1.004, 1.005, 1.004, 1.004, 0.994, 0.965, 0.958, 0.958, 0.953, 0.958, 0.958, 0.965, 0.918, 0.924, 0.924, 0.906, 0.924, 0.924, 0.918, 0.991, 0.998, 0.998, 0.978, 0.998, 0.998, 0.991, 0.991, 0.998, 0.998, 0.978, 0.998, 0.998, 0.991, 0.991, 0.998, 0.998, 0.978, 0.998, 0.998, 0.991 ),
  label = cms.untracked.string( "090322_3_8t" ),
  version = cms.string( "grid_1103l_090322_3_8t" ),
  debugBuilder = cms.untracked.bool( False ),
  paramLabel = cms.string( "slave_38" ),
  cacheLastVolume = cms.untracked.bool( True )
)
process.VBF35 = cms.ESProducer( "VolumeBasedMagneticFieldESProducer",
  scalingVolumes = cms.vint32(  ),
  overrideMasterSector = cms.bool( True ),
  useParametrizedTrackerField = cms.bool( True ),
  scalingFactors = cms.vdouble(  ),
  label = cms.untracked.string( "071212_3_5t" ),
  version = cms.string( "grid_1103l_071212_3_5t" ),
  debugBuilder = cms.untracked.bool( False ),
  paramLabel = cms.string( "slave_35" ),
  cacheLastVolume = cms.untracked.bool( True )
)
process.VBF30 = cms.ESProducer( "VolumeBasedMagneticFieldESProducer",
  scalingVolumes = cms.vint32(  ),
  overrideMasterSector = cms.bool( True ),
  useParametrizedTrackerField = cms.bool( True ),
  scalingFactors = cms.vdouble(  ),
  label = cms.untracked.string( "071212_3t" ),
  version = cms.string( "grid_1103l_071212_3t" ),
  debugBuilder = cms.untracked.bool( False ),
  paramLabel = cms.string( "slave_30" ),
  cacheLastVolume = cms.untracked.bool( True )
)
process.VBF20 = cms.ESProducer( "VolumeBasedMagneticFieldESProducer",
  scalingVolumes = cms.vint32(  ),
  overrideMasterSector = cms.bool( True ),
  useParametrizedTrackerField = cms.bool( True ),
  scalingFactors = cms.vdouble(  ),
  label = cms.untracked.string( "071212_2t" ),
  version = cms.string( "grid_1103l_071212_2t" ),
  debugBuilder = cms.untracked.bool( False ),
  paramLabel = cms.string( "slave_20" ),
  cacheLastVolume = cms.untracked.bool( True )
)
process.VBF0 = cms.ESProducer( "VolumeBasedMagneticFieldESProducer",
  scalingVolumes = cms.vint32(  ),
  overrideMasterSector = cms.bool( True ),
  useParametrizedTrackerField = cms.bool( True ),
  scalingFactors = cms.vdouble(  ),
  label = cms.untracked.string( "0t" ),
  version = cms.string( "grid_1103l_071212_2t" ),
  debugBuilder = cms.untracked.bool( False ),
  paramLabel = cms.string( "slave_0" ),
  cacheLastVolume = cms.untracked.bool( True )
)
process.TransientTrackBuilderESProducer = cms.ESProducer( "TransientTrackBuilderESProducer",
  ComponentName = cms.string( "TransientTrackBuilder" )
)
process.TrackerGeometricDetESModule = cms.ESProducer( "TrackerGeometricDetESModule",
  fromDDD = cms.bool( False )
)
process.TrackerDigiGeometryESModule = cms.ESProducer( "TrackerDigiGeometryESModule",
  appendToDataLabel = cms.string( "" ),
  fromDDD = cms.bool( False ),
  applyAlignment = cms.bool( True ),
  alignmentsLabel = cms.string( "" )
)
process.StripCPEfromTrackAngleESProducer = cms.ESProducer( "StripCPEESProducer",
  TanDiffusionAngle = cms.double( 0.01 ),
  UncertaintyScaling = cms.double( 1.42 ),
  ThicknessRelativeUncertainty = cms.double( 0.02 ),
  MaybeNoiseThreshold = cms.double( 3.5 ),
  ComponentName = cms.string( "StripCPEfromTrackAngle" ),
  MinimumUncertainty = cms.double( 0.01 ),
  NoiseThreshold = cms.double( 2.3 )
)
process.SteppingHelixPropagatorAny = cms.ESProducer( "SteppingHelixPropagatorESProducer",
  NoErrorPropagation = cms.bool( False ),
  endcapShiftInZPos = cms.double( 0.0 ),
  PropagationDirection = cms.string( "anyDirection" ),
  useTuningForL2Speed = cms.bool( False ),
  useIsYokeFlag = cms.bool( True ),
  endcapShiftInZNeg = cms.double( 0.0 ),
  SetVBFPointer = cms.bool( False ),
  AssumeNoMaterial = cms.bool( False ),
  returnTangentPlane = cms.bool( True ),
  useInTeslaFromMagField = cms.bool( False ),
  VBFName = cms.string( "VolumeBasedMagneticField" ),
  useEndcapShiftsInZ = cms.bool( False ),
  sendLogWarning = cms.bool( False ),
  useMatVolumes = cms.bool( True ),
  debug = cms.bool( False ),
  ApplyRadX0Correction = cms.bool( True ),
  useMagVolumes = cms.bool( True ),
  ComponentName = cms.string( "SteppingHelixPropagatorAny" )
)
process.SlaveField40 = cms.ESProducer( "ParametrizedMagneticFieldProducer",
  version = cms.string( "OAE_1103l_071212" ),
  parameters = cms.PSet(  BValue = cms.string( "4_0T" ) ),
  label = cms.untracked.string( "slave_40" )
)
process.SlaveField38 = cms.ESProducer( "ParametrizedMagneticFieldProducer",
  version = cms.string( "OAE_1103l_071212" ),
  parameters = cms.PSet(  BValue = cms.string( "3_8T" ) ),
  label = cms.untracked.string( "slave_38" )
)
process.SlaveField35 = cms.ESProducer( "ParametrizedMagneticFieldProducer",
  version = cms.string( "OAE_1103l_071212" ),
  parameters = cms.PSet(  BValue = cms.string( "3_5T" ) ),
  label = cms.untracked.string( "slave_35" )
)
process.SlaveField30 = cms.ESProducer( "ParametrizedMagneticFieldProducer",
  version = cms.string( "OAE_1103l_071212" ),
  parameters = cms.PSet(  BValue = cms.string( "3_0T" ) ),
  label = cms.untracked.string( "slave_30" )
)
process.SlaveField20 = cms.ESProducer( "ParametrizedMagneticFieldProducer",
  version = cms.string( "OAE_1103l_071212" ),
  parameters = cms.PSet(  BValue = cms.string( "2_0T" ) ),
  label = cms.untracked.string( "slave_20" )
)
process.SlaveField0 = cms.ESProducer( "UniformMagneticFieldESProducer",
  ZFieldInTesla = cms.double( 0.0 ),
  label = cms.untracked.string( "slave_0" )
)
process.SiStripRecHitMatcherESProducer = cms.ESProducer( "SiStripRecHitMatcherESProducer",
  ComponentName = cms.string( "StandardMatcher" ),
  NSigmaInside = cms.double( 3.0 )
)
process.SiStripQualityESProducer = cms.ESProducer( "SiStripQualityESProducer",
  appendToDataLabel = cms.string( "" ),
  PrintDebugOutput = cms.bool( False ),
  ThresholdForReducedGranularity = cms.double( 0.3 ),
  UseEmptyRunInfo = cms.bool( False ),
  ReduceGranularity = cms.bool( False ),
  ListOfRecordToMerge = cms.VPSet( 
    cms.PSet(  record = cms.string( "SiStripDetVOffRcd" ),
      tag = cms.string( "" )
    ),
    cms.PSet(  record = cms.string( "SiStripDetCablingRcd" ),
      tag = cms.string( "" )
    ),
    cms.PSet(  record = cms.string( "SiStripBadChannelRcd" ),
      tag = cms.string( "" )
    ),
    cms.PSet(  record = cms.string( "SiStripBadFiberRcd" ),
      tag = cms.string( "" )
    ),
    cms.PSet(  record = cms.string( "SiStripBadModuleRcd" ),
      tag = cms.string( "" )
    )
  )
)
process.SiStripGainESProducer = cms.ESProducer( "SiStripGainESProducer",
  printDebug = cms.untracked.bool( False ),
  appendToDataLabel = cms.string( "" ),
  APVGain = cms.VPSet( 
    cms.PSet(  Record = cms.string( "SiStripApvGainRcd" ),
      NormalizationFactor = cms.untracked.double( 1.0 ),
      Label = cms.untracked.string( "" )
    ),
    cms.PSet(  Record = cms.string( "SiStripApvGain2Rcd" ),
      NormalizationFactor = cms.untracked.double( 1.0 ),
      Label = cms.untracked.string( "" )
    )
  ),
  AutomaticNormalization = cms.bool( False )
)
process.RPCGeometryESModule = cms.ESProducer( "RPCGeometryESModule",
  useDDD = cms.untracked.bool( False ),
  compatibiltyWith11 = cms.untracked.bool( True )
)
process.OppositeMaterialPropagatorForHI = cms.ESProducer( "PropagatorWithMaterialESProducer",
  PropagationDirection = cms.string( "oppositeToMomentum" ),
  ComponentName = cms.string( "PropagatorWithMaterialOppositeForHI" ),
  Mass = cms.double( 0.139 ),
  ptMin = cms.double( -1.0 ),
  MaxDPhi = cms.double( 1.6 ),
  useRungeKutta = cms.bool( False )
)
process.OppositeMaterialPropagator = cms.ESProducer( "PropagatorWithMaterialESProducer",
  PropagationDirection = cms.string( "oppositeToMomentum" ),
  ComponentName = cms.string( "PropagatorWithMaterialOpposite" ),
  Mass = cms.double( 0.105 ),
  ptMin = cms.double( -1.0 ),
  MaxDPhi = cms.double( 1.6 ),
  useRungeKutta = cms.bool( False )
)
process.MaterialPropagatorForHI = cms.ESProducer( "PropagatorWithMaterialESProducer",
  PropagationDirection = cms.string( "alongMomentum" ),
  ComponentName = cms.string( "PropagatorWithMaterialForHI" ),
  Mass = cms.double( 0.139 ),
  ptMin = cms.double( -1.0 ),
  MaxDPhi = cms.double( 1.6 ),
  useRungeKutta = cms.bool( False )
)
process.MaterialPropagator = cms.ESProducer( "PropagatorWithMaterialESProducer",
  PropagationDirection = cms.string( "alongMomentum" ),
  ComponentName = cms.string( "PropagatorWithMaterial" ),
  Mass = cms.double( 0.105 ),
  ptMin = cms.double( -1.0 ),
  MaxDPhi = cms.double( 1.6 ),
  useRungeKutta = cms.bool( False )
)
process.L1GtTriggerMaskTechTrigTrivialProducer = cms.ESProducer( "L1GtTriggerMaskTechTrigTrivialProducer",
  TriggerMask = cms.vuint32( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 )
)
process.L1GtTriggerMaskAlgoTrigTrivialProducer = cms.ESProducer( "L1GtTriggerMaskAlgoTrigTrivialProducer",
  TriggerMask = cms.vuint32( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 )
)
process.HcalTopologyIdealEP = cms.ESProducer( "HcalTopologyIdealEP" )
process.HcalGeometryFromDBEP = cms.ESProducer( "HcalGeometryFromDBEP",
  applyAlignment = cms.bool( False )
)
process.EcalUnpackerWorkerESProducer = cms.ESProducer( "EcalUnpackerWorkerESProducer",
  CalibRHAlgo = cms.PSet( 
    flagsMapDBReco = cms.vint32( 0, 0, 0, 0, 4, -1, -1, -1, 4, 4, 7, 7, 7, 8, 9 ),
    Type = cms.string( "EcalRecHitWorkerSimple" ),
    killDeadChannels = cms.bool( True ),
    ChannelStatusToBeExcluded = cms.vint32( 10, 11, 12, 13, 14 ),
    laserCorrection = cms.bool( False ),
    EBLaserMIN = cms.double( 0.5 ),
    EELaserMIN = cms.double( 0.5 ),
    EBLaserMAX = cms.double( 2.0 ),
    EELaserMAX = cms.double( 3.0 )
  ),
  ComponentName = cms.string( "" ),
  UncalibRHAlgo = cms.PSet(  Type = cms.string( "EcalUncalibRecHitWorkerWeights" ) ),
  DCCDataUnpacker = cms.PSet( 
    orderedDCCIdList = cms.vint32( 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54 ),
    tccUnpacking = cms.bool( False ),
    srpUnpacking = cms.bool( False ),
    syncCheck = cms.bool( False ),
    feIdCheck = cms.bool( True ),
    headerUnpacking = cms.bool( True ),
    orderedFedList = cms.vint32( 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654 ),
    feUnpacking = cms.bool( True ),
    forceKeepFRData = cms.bool( False ),
    memUnpacking = cms.bool( True )
  ),
  ElectronicsMapper = cms.PSet( 
    numbXtalTSamples = cms.uint32( 10 ),
    numbTriggerTSamples = cms.uint32( 1 )
  )
)
process.EcalPreshowerGeometryFromDBEP = cms.ESProducer( "EcalPreshowerGeometryFromDBEP",
  applyAlignment = cms.bool( True )
)
process.EcalLaserCorrectionService = cms.ESProducer( "EcalLaserCorrectionService" )
process.EcalEndcapGeometryFromDBEP = cms.ESProducer( "EcalEndcapGeometryFromDBEP",
  applyAlignment = cms.bool( True )
)
process.EcalElectronicsMappingBuilder = cms.ESProducer( "EcalElectronicsMappingBuilder" )
process.EcalBarrelGeometryFromDBEP = cms.ESProducer( "EcalBarrelGeometryFromDBEP",
  applyAlignment = cms.bool( True )
)
process.DTGeometryESModule = cms.ESProducer( "DTGeometryESModule",
  appendToDataLabel = cms.string( "" ),
  fromDDD = cms.bool( False ),
  applyAlignment = cms.bool( True ),
  alignmentsLabel = cms.string( "" )
)
process.ClusterShapeHitFilterESProducer = cms.ESProducer( "ClusterShapeHitFilterESProducer",
  ComponentName = cms.string( "ClusterShapeHitFilter" )
)
process.CastorDbProducer = cms.ESProducer( "CastorDbProducer",
  appendToDataLabel = cms.string( "" )
)
process.CaloTowerGeometryFromDBEP = cms.ESProducer( "CaloTowerGeometryFromDBEP",
  applyAlignment = cms.bool( False )
)
process.CaloTowerConstituentsMapBuilder = cms.ESProducer( "CaloTowerConstituentsMapBuilder",
  MapFile = cms.untracked.string( "Geometry/CaloTopology/data/CaloTowerEEGeometric.map.gz" )
)
process.CaloTopologyBuilder = cms.ESProducer( "CaloTopologyBuilder" )
process.CaloGeometryBuilder = cms.ESProducer( "CaloGeometryBuilder",
  SelectedCalos = cms.vstring( 'HCAL',
    'ZDC',
    'EcalBarrel',
    'EcalEndcap',
    'EcalPreshower',
    'TOWER' )
)
process.CSCGeometryESModule = cms.ESProducer( "CSCGeometryESModule",
  useRealWireGeometry = cms.bool( True ),
  appendToDataLabel = cms.string( "" ),
  alignmentsLabel = cms.string( "" ),
  useGangedStripsInME1a = cms.bool( True ),
  debugV = cms.untracked.bool( False ),
  useOnlyWiresInME1a = cms.bool( False ),
  useDDD = cms.bool( False ),
  useCentreTIOffsets = cms.bool( False ),
  applyAlignment = cms.bool( True )
)
process.AutoMagneticFieldESProducer = cms.ESProducer( "AutoMagneticFieldESProducer",
  label = cms.untracked.string( "" ),
  nominalCurrents = cms.untracked.vint32( -1, 0, 9558, 14416, 16819, 18268, 19262 ),
  valueOverride = cms.int32( -1 ),
  mapLabels = cms.untracked.vstring( '090322_3_8t',
    '0t',
    '071212_2t',
    '071212_3t',
    '071212_3_5t',
    '090322_3_8t',
    '071212_4t' )
)
process.AnyDirectionAnalyticalPropagator = cms.ESProducer( "AnalyticalPropagatorESProducer",
  MaxDPhi = cms.double( 1.6 ),
  ComponentName = cms.string( "AnyDirectionAnalyticalPropagator" ),
  PropagationDirection = cms.string( "anyDirection" )
)

process.UpdaterService = cms.Service( "UpdaterService",
)
process.PrescaleService = cms.Service( "PrescaleService",
    prescaleTable = cms.VPSet(  *(
      cms.PSet(  pathName = cms.string( "HLT_Activity_Ecal_SC7_v9" ),
        prescales = cms.vuint32( 150, 100, 75, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1SingleJet16_v5" ),
        prescales = cms.vuint32( 50, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1SingleJet36_v5" ),
        prescales = cms.vuint32( 500, 500, 500, 500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet30_v10" ),
        prescales = cms.vuint32( 40, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet30_L1FastJet_v4" ),
        prescales = cms.vuint32( 40, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet60_v10" ),
        prescales = cms.vuint32( 80, 80, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet60_L1FastJet_v4" ),
        prescales = cms.vuint32( 80, 80, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet110_v10" ),
        prescales = cms.vuint32( 80, 80, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet190_v10" ),
        prescales = cms.vuint32( 10, 100, 100, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet240_v10" ),
        prescales = cms.vuint32( 2, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet240_L1FastJet_v4" ),
        prescales = cms.vuint32( 2, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet300_v10" ),
        prescales = cms.vuint32( 10, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet300_L1FastJet_v4" ),
        prescales = cms.vuint32( 10, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet370_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet370_L1FastJet_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet370_NoJetID_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Jet800_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiJetAve30_v10" ),
        prescales = cms.vuint32( 20, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiJetAve60_v10" ),
        prescales = cms.vuint32( 40, 40, 40, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiJetAve110_v10" ),
        prescales = cms.vuint32( 40, 40, 40, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiJetAve190_v10" ),
        prescales = cms.vuint32( 5, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiJetAve240_v10" ),
        prescales = cms.vuint32( 1, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiJetAve300_v11" ),
        prescales = cms.vuint32( 5, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiJetAve370_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "DST_FatJetMass300_DR1p1_Deta2p0_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "DST_FatJetMass400_DR1p1_Deta2p0_RunPF_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_FatJetMass850_DR1p1_Deta2p0_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleJet30_ForwardBackward_v11" ),
        prescales = cms.vuint32( 840, 360, 90, 90, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleJet60_ForwardBackward_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleJet70_ForwardBackward_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleJet80_ForwardBackward_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiJet130_PT130_v10" ),
        prescales = cms.vuint32( 50, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiJet160_PT160_v10" ),
        prescales = cms.vuint32( 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_CentralJet80_MET65_v11" ),
        prescales = cms.vuint32( 600, 200, 150, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_CentralJet80_MET80_v10" ),
        prescales = cms.vuint32( 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_CentralJet80_MET95_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_CentralJet80_MET110_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiJet60_MET45_v11" ),
        prescales = cms.vuint32( 10, 10, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiCentralJet20_MET100_HBHENoiseFiltered_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiCentralJet20_MET80_v9" ),
        prescales = cms.vuint32( 10, 10, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiCentralJet20_BTagIP_MET65_v12" ),
        prescales = cms.vuint32( 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiCentralJet36_BTagIP3DLoose_v6" ),
        prescales = cms.vuint32( 500, 600, 1800, 5400, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_CentralJet46_CentralJet38_DiBTagIP3D_v8" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_CentralJet60_CentralJet53_DiBTagIP3D_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet40_v12" ),
        prescales = cms.vuint32( 1400, 1400, 700, 700, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet45_DiJet40_v4" ),
        prescales = cms.vuint32( 50, 40, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet50_DiJet40_v6" ),
        prescales = cms.vuint32( 20, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet50_DiJet40_L1FastJet_v3" ),
        prescales = cms.vuint32( 20, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet40_IsoPFTau40_v19" ),
        prescales = cms.vuint32( 60, 45, 45, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet45_IsoPFTau45_v14" ),
        prescales = cms.vuint32( 10, 10, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet50_IsoPFTau50_v8" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet70_v11" ),
        prescales = cms.vuint32( 200, 150, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet80_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet80_L1FastJet_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_QuadJet90_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_SixJet45_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_SixJet45_L1FastJet_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_EightJet35_v4" ),
        prescales = cms.vuint32( 50, 40, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_EightJet35_L1FastJet_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_EightJet40_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_EightJet40_L1FastJet_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_EightJet120_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_70Jet10_v5" ),
        prescales = cms.vuint32( 0, 50000, 250, 250, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_70Jet13_v5" ),
        prescales = cms.vuint32( 300000, 1500, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_300Tower0p5_v2" ),
        prescales = cms.vuint32( 80000, 8000, 400, 400, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_300Tower0p6_v2" ),
        prescales = cms.vuint32( 1500, 1500, 180, 180, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_300Tower0p7_v2" ),
        prescales = cms.vuint32( 500, 500, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_300Tower0p8_v2" ),
        prescales = cms.vuint32( 200, 200, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_ExclDiJet60_HFOR_v10" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_ExclDiJet60_HFAND_v10" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_JetE30_NoBPTX_v9" ),
        prescales = cms.vuint32( 60, 30, 24, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_JetE30_NoBPTX_NoHalo_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_JetE30_NoBPTX3BX_NoHalo_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_JetE50_NoBPTX3BX_NoHalo_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT150_v12" ),
        prescales = cms.vuint32( 2000, 1250, 1250, 1250, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT200_v12" ),
        prescales = cms.vuint32( 1000, 500, 1000, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT250_v12" ),
        prescales = cms.vuint32( 7000, 2100, 2000, 2000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT250_AlphaT0p58_v4" ),
        prescales = cms.vuint32( 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT250_AlphaT0p60_v4" ),
        prescales = cms.vuint32( 20, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT250_AlphaT0p65_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT300_v13" ),
        prescales = cms.vuint32( 5000, 1000, 1000, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT300_AlphaT0p54_v6" ),
        prescales = cms.vuint32( 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT300_AlphaT0p55_v4" ),
        prescales = cms.vuint32( 20, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT300_AlphaT0p60_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT350_v12" ),
        prescales = cms.vuint32( 4000, 600, 600, 600, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "DST_HT350_RunPF_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT350_MHT100_v4" ),
        prescales = cms.vuint32( 20, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT350_MHT110_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT350_L1FastJet_v4" ),
        prescales = cms.vuint32( 4000, 600, 600, 600, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT350_L1FastJet_MHT100_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT350_L1FastJet_MHT110_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT350_AlphaT0p53_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_v12" ),
        prescales = cms.vuint32( 1000, 400, 400, 400, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_MHT90_v4" ),
        prescales = cms.vuint32( 20, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_MHT100_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_L1FastJet_v4" ),
        prescales = cms.vuint32( 1000, 400, 400, 400, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_L1FastJet_MHT90_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_L1FastJet_MHT100_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_AlphaT0p51_v11" ),
        prescales = cms.vuint32( 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_AlphaT0p52_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT450_v12" ),
        prescales = cms.vuint32( 500, 200, 200, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT450_AlphaT0p51_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT500_v12" ),
        prescales = cms.vuint32( 120, 90, 60, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT550_v12" ),
        prescales = cms.vuint32( 90, 60, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT600_v5" ),
        prescales = cms.vuint32( 40, 30, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT650_v5" ),
        prescales = cms.vuint32( 30, 20, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT700_v3" ),
        prescales = cms.vuint32( 10, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT750_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT750_L1FastJet_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT2000_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_PFHT650_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_PFHT350_PFMHT90_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_PFHT350_PFMHT100_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_PFHT400_PFMHT80_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_PFHT400_PFMHT90_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_PFMHT150_v18" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiCentralPFJet30_PFMHT80_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DiCentralPFJet50_PFMHT80_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_MET120_v8" ),
        prescales = cms.vuint32( 8, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_MET120_HBHENoiseFiltered_v7" ),
        prescales = cms.vuint32( 8, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_MET200_v8" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_MET200_HBHENoiseFiltered_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_MET400_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R014_MR150_v11" ),
        prescales = cms.vuint32( 4800, 4200, 3000, 3000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R020_MR150_v11" ),
        prescales = cms.vuint32( 2400, 2100, 1500, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R020_MR550_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R025_MR150_v11" ),
        prescales = cms.vuint32( 800, 600, 500, 500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R025_MR450_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R033_MR350_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R038_MR250_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R038_MR300_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_RMR65_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R014_MR200_CentralJet40_BTagIP_v5" ),
        prescales = cms.vuint32( 300, 240, 180, 180, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R014_MR400_CentralJet40_BTagIP_v5" ),
        prescales = cms.vuint32( 20, 10, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R014_MR450_CentralJet40_BTagIP_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R020_MR300_CentralJet40_BTagIP_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R020_MR350_CentralJet40_BTagIP_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R030_MR200_CentralJet40_BTagIP_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_R030_MR250_CentralJet40_BTagIP_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1SingleMuOpen_v5" ),
        prescales = cms.vuint32( 600, 600, 600, 600, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1SingleMuOpen_DT_v5" ),
        prescales = cms.vuint32( 75, 75, 75, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1SingleMu10_v5" ),
        prescales = cms.vuint32( 4500, 4500, 4500, 4500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1SingleMu20_v5" ),
        prescales = cms.vuint32( 3750, 4000, 45000, 45000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1DoubleMu0_v5" ),
        prescales = cms.vuint32( 1500, 1500, 1500, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L2Mu10_v7" ),
        prescales = cms.vuint32( 270, 640, 640, 640, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L2Mu20_v7" ),
        prescales = cms.vuint32( 180, 420, 420, 420, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L2Mu60_1Hit_MET40_v7" ),
        prescales = cms.vuint32( 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L2Mu60_1Hit_MET60_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L2DoubleMu0_v8" ),
        prescales = cms.vuint32( 470, 470, 470, 470, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu5_v15" ),
        prescales = cms.vuint32( 320, 640, 640, 640, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu8_v13" ),
        prescales = cms.vuint32( 40, 40, 40, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu12_v13" ),
        prescales = cms.vuint32( 70, 70, 70, 70, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu15_v14" ),
        prescales = cms.vuint32( 25, 65, 65, 65, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu20_v13" ),
        prescales = cms.vuint32( 10, 60, 60, 900, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu24_v13" ),
        prescales = cms.vuint32( 35, 35, 200, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu30_v13" ),
        prescales = cms.vuint32( 4, 20, 20, 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu40_v11" ),
        prescales = cms.vuint32( 10, 10, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu40_eta2p1_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu50_eta2p1_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu60_eta2p1_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu100_eta2p1_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu200_eta2p1_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu15_v19" ),
        prescales = cms.vuint32( 15, 30, 40, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu15_eta2p1_v6" ),
        prescales = cms.vuint32( 140, 560, 400, 400, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu20_v14" ),
        prescales = cms.vuint32( 8, 16, 16, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu24_v14" ),
        prescales = cms.vuint32( 12, 16, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu24_eta2p1_v8" ),
        prescales = cms.vuint32( 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu30_eta2p1_v8" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu34_eta2p1_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu40_eta2p1_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L2DoubleMu23_NoVertex_v9" ),
        prescales = cms.vuint32( 20, 20, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L2DoubleMu30_NoVertex_v5" ),
        prescales = cms.vuint32( 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L2DoubleMu30_NoVertex_dPhi2p5_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu3_v15" ),
        prescales = cms.vuint32( 45, 45, 45, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu5_v6" ),
        prescales = cms.vuint32( 20, 15, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu7_v13" ),
        prescales = cms.vuint32( 100, 70, 60, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu45_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu7_Acoplanarity03_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu4_Jpsi_Displaced_v6" ),
        prescales = cms.vuint32( 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu5_Jpsi_Displaced_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu4_Dimuon4_Bs_Barrel_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu4_Dimuon6_Bs_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu4p5_LowMass_Displaced_v6" ),
        prescales = cms.vuint32( 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu5_LowMass_Displaced_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon0_Omega_Phi_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon0_Jpsi_v11" ),
        prescales = cms.vuint32( 200, 160, 120, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon0_Jpsi_NoVertexing_v8" ),
        prescales = cms.vuint32( 200, 160, 120, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon0_Upsilon_v11" ),
        prescales = cms.vuint32( 200, 160, 120, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon6_LowMass_v6" ),
        prescales = cms.vuint32( 1, 5, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon7_Upsilon_Barrel_v6" ),
        prescales = cms.vuint32( 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon9_Upsilon_Barrel_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon9_PsiPrime_v6" ),
        prescales = cms.vuint32( 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon10_Jpsi_Barrel_v11" ),
        prescales = cms.vuint32( 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon11_PsiPrime_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon13_Jpsi_Barrel_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon0_Jpsi_Muon_v12" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Dimuon0_Upsilon_Muon_v12" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_TripleMu0_TauTo3Mu_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu13_Mu8_v12" ),
        prescales = cms.vuint32( 40, 30, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_Mu8_v12" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_TkMu8_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_TripleMu5_v14" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu5_IsoMu5_v13" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu5_TkMu0_OST_Jpsi_Tight_B5Q7_v14" ),
        prescales = cms.vuint32( 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu5_L2Mu2_Jpsi_v14" ),
        prescales = cms.vuint32( 320, 320, 240, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu5_Track2_Jpsi_v14" ),
        prescales = cms.vuint32( 6, 6, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu7_Track7_Jpsi_v15" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon20_CaloIdVL_IsoL_v10" ),
        prescales = cms.vuint32( 100, 100, 100, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon20_R9Id_Photon18_R9Id_v8" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon20_CaloIdVT_IsoT_Ele8_CaloIdL_CaloIsoVL_v12" ),
        prescales = cms.vuint32( 75, 60, 45, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon26_Photon18_v8" ),
        prescales = cms.vuint32( 600, 450, 340, 340, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon26_CaloIdXL_IsoXL_Photon18_v5" ),
        prescales = cms.vuint32( 190, 150, 110, 110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon26_CaloIdXL_IsoXL_Photon18_R9IdT_Mass60_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon26_CaloIdXL_IsoXL_Photon18_CaloIdXL_IsoXL_Mass60_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon26_R9IdT_Photon18_CaloIdXL_IsoXL_Mass60_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon26_R9IdT_Photon18_R9IdT_Mass60_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon30_CaloIdVL_v9" ),
        prescales = cms.vuint32( 7000, 5600, 4200, 4200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon30_CaloIdVL_IsoL_v12" ),
        prescales = cms.vuint32( 2500, 2000, 1500, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon36_Photon22_v2" ),
        prescales = cms.vuint32( 300, 240, 180, 180, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon36_CaloIdVL_Photon22_CaloIdVL_v3" ),
        prescales = cms.vuint32( 40, 30, 22, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon36_CaloIdL_IsoVL_Photon22_v9" ),
        prescales = cms.vuint32( 75, 60, 45, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon36_CaloIdL_IsoVL_Photon22_CaloIdL_IsoVL_v8" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon36_CaloIdL_IsoVL_Photon22_R9Id_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon36_R9Id_Photon22_CaloIdL_IsoVL_v8" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon36_R9Id_Photon22_R9Id_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon50_CaloIdVL_v5" ),
        prescales = cms.vuint32( 900, 720, 540, 540, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon50_CaloIdVL_IsoL_v10" ),
        prescales = cms.vuint32( 330, 270, 200, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon60_CaloIdL_HT300_v4" ),
        prescales = cms.vuint32( 9, 6, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon60_CaloIdL_MHT70_v4" ),
        prescales = cms.vuint32( 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon70_CaloIdXL_HT400_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon70_CaloIdXL_HT500_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon70_CaloIdXL_MHT90_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon70_CaloIdXL_MHT100_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon75_CaloIdVL_v8" ),
        prescales = cms.vuint32( 150, 120, 90, 90, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon75_CaloIdVL_IsoL_v11" ),
        prescales = cms.vuint32( 60, 45, 35, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon90_CaloIdVL_v5" ),
        prescales = cms.vuint32( 75, 60, 45, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon90_CaloIdVL_IsoL_v8" ),
        prescales = cms.vuint32( 20, 15, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon90EBOnly_CaloIdVL_IsoL_TriPFJet25_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon90EBOnly_CaloIdVL_IsoL_TriPFJet30_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon135_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon225_NoHE_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon400_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon200_NoHE_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoublePhoton43_HEVT_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoublePhoton48_HEVT_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoublePhoton70_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoublePhoton80_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoublePhoton5_IsoVL_CEP_v10" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1SingleEG5_v4" ),
        prescales = cms.vuint32( 1800, 1800, 1800, 1800, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1SingleEG12_v4" ),
        prescales = cms.vuint32( 220, 220, 220, 220, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele8_v11" ),
        prescales = cms.vuint32( 150, 150, 150, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele8_CaloIdL_CaloIsoVL_v11" ),
        prescales = cms.vuint32( 30, 30, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele8_CaloIdL_TrkIdVL_v11" ),
        prescales = cms.vuint32( 15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v9" ),
        prescales = cms.vuint32( 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_v5" ),
        prescales = cms.vuint32( 17, 17, 17, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele17_CaloIdL_CaloIsoVL_v11" ),
        prescales = cms.vuint32( 110, 110, 110, 110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_SC8_Mass30_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v11" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_Ele8_Mass30_v10" ),
        prescales = cms.vuint32( 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele22_CaloIdL_CaloIsoVL_Ele15_HFT_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele27_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_v4" ),
        prescales = cms.vuint32( 1250, 1000, 750, 750, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele27_WP80_v4" ),
        prescales = cms.vuint32( 200, 160, 120, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele27_WP80_PFMT50_v10" ),
        prescales = cms.vuint32( 100, 80, 60, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele32_WP70_v4" ),
        prescales = cms.vuint32( 25, 20, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele32_WP70_PFMT50_v10" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele32_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_v4" ),
        prescales = cms.vuint32( 250, 150, 150, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_SC17_v9" ),
        prescales = cms.vuint32( 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_Ele17_v4" ),
        prescales = cms.vuint32( 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele65_CaloIdVT_TrkIdT_v7" ),
        prescales = cms.vuint32( 30, 25, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele80_CaloIdVT_TrkIdT_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele100_CaloIdVT_TrkIdT_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleEle8_CaloIdT_TrkIdVL_v6" ),
        prescales = cms.vuint32( 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleEle33_CaloIdL_v8" ),
        prescales = cms.vuint32( 50, 40, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleEle33_CaloIdL_CaloIsoT_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleEle33_CaloIdT_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleEle45_CaloIdL_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_MediumIsoPFTau35_Trk20_v7" ),
        prescales = cms.vuint32( 1, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_MediumIsoPFTau35_Trk20_MET60_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_MediumIsoPFTau35_Trk20_MET70_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleIsoPFTau45_Trk5_eta2p1_v9" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleIsoPFTau55_Trk5_eta2p1_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT350_DoubleIsoPFTau10_Trk3_PFMHT45_v14" ),
        prescales = cms.vuint32( 20, 15, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_DoubleIsoPFTau10_Trk3_PFMHT50_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_BTagMu_DiJet20_Mu5_v15" ),
        prescales = cms.vuint32( 60, 60, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_BTagMu_DiJet40_Mu5_v15" ),
        prescales = cms.vuint32( 30, 30, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_BTagMu_DiJet70_Mu5_v15" ),
        prescales = cms.vuint32( 10, 8, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_BTagMu_DiJet110_Mu5_v15" ),
        prescales = cms.vuint32( 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu10_R014_MR200_v6" ),
        prescales = cms.vuint32( 30, 15, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu10_R025_MR200_v7" ),
        prescales = cms.vuint32( 20, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu10_R029_MR200_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu10_R033_MR200_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT300_Mu15_PFMHT40_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT300_Mu15_PFMHT50_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT350_Mu5_PFMHT45_v14" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_Mu5_PFMHT50_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu5_DoubleEle8_CaloIdT_TrkIdVL_v9" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu5_Ele8_CaloIdT_CaloIsoVL_v6" ),
        prescales = cms.vuint32( 300, 300, 300, 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu5_Ele8_CaloIdT_TrkIdVL_Mass8_HT150_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu8_Ele8_CaloIdT_TrkIdVL_Mass8_HT150_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu8_Ele8_CaloIdT_TrkIdVL_Mass8_HT200_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_TkIso10Mu5_Ele8_CaloIdT_CaloIsoVVL_TrkIdVL_Mass8_HT150_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_TkIso10Mu5_Ele8_CaloIdT_CaloIsoVVL_TrkIdVL_Mass8_HT200_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu5_Ele8_CaloIdT_TrkIdVL_Ele8_CaloIdL_TrkIdVL_v9" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu8_Ele17_CaloIdL_v14" ),
        prescales = cms.vuint32( 100, 80, 60, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v9" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu8_Photon20_CaloIdVT_IsoT_v14" ),
        prescales = cms.vuint32( 20, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu8_Jet40_v16" ),
        prescales = cms.vuint32( 2300, 2300, 2300, 2300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu15_L1ETM20_v5" ),
        prescales = cms.vuint32( 40, 40, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu15_Photon20_CaloIdL_v15" ),
        prescales = cms.vuint32( 20, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu15_DoublePhoton15_CaloIdL_v15" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu15_LooseIsoPFTau15_v15" ),
        prescales = cms.vuint32( 0, 0, 110, 110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_eta2p1_CentralPFJet30_v4" ),
        prescales = cms.vuint32( 800, 600, 480, 480, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_eta2p1_DiCentralPFJet30_v4" ),
        prescales = cms.vuint32( 400, 300, 240, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_eta2p1_TriCentralPFJet30_v4" ),
        prescales = cms.vuint32( 120, 100, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_eta2p1_QuadCentralPFJet30_v4" ),
        prescales = cms.vuint32( 30, 25, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_eta2p1_CentralJet30_BTagIP_v7" ),
        prescales = cms.vuint32( 120, 100, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_Ele8_CaloIdL_v14" ),
        prescales = cms.vuint32( 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v9" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu12_eta2p1_DiCentralJet20_BTagIP3D1stTrack_v7" ),
        prescales = cms.vuint32( 250, 200, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu12_eta2p1_DiCentralJet20_DiBTagIP3D1stTrack_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu40_HT300_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu60_HT300_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu15_L1ETM20_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu15_eta2p1_LooseIsoPFTau20_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu15_eta2p1_MediumIsoPFTau20_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu15_eta2p1_TightIsoPFTau20_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_CentralJet30_v7" ),
        prescales = cms.vuint32( 150, 40, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_CentralPFJet30_v4" ),
        prescales = cms.vuint32( 50, 40, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_DiCentralPFJet30_v4" ),
        prescales = cms.vuint32( 50, 10, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_TriCentralPFJet30_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_QuadCentralPFJet30_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_CentralJet30_BTagIP_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_eta2p1_DiCentralPFJet25_PFMHT15_v6" ),
        prescales = cms.vuint32( 100, 80, 60, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_DiCentralPFJet25_v6" ),
        prescales = cms.vuint32( 25, 20, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_DiCentralPFJet25_PFMHT15_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_DiCentralPFJet25_PFMHT25_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Mu17_eta2p1_DiPFJet25_Deta3_v6" ),
        prescales = cms.vuint32( 100, 80, 60, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_DiPFJet25_Deta3_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoMu17_eta2p1_DiPFJet25_Deta3_PFJet25_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu5_Mass8_HT150_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu8_Mass8_HT150_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu8_Mass8_HT200_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleTkIso10Mu5_Mass8_HT150_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleTkIso10Mu5_Mass8_HT200_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu5_Ele8_CaloIdT_TrkIdVL_v9" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleMu5_Ele8_CaloIdT_TrkIdT_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon40_CaloIdL_R014_MR150_v2" ),
        prescales = cms.vuint32( 300, 240, 180, 180, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon40_CaloIdL_R017_MR500_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon40_CaloIdL_R023_MR350_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon40_CaloIdL_R029_MR250_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon40_CaloIdL_R042_MR200_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoublePhoton40_CaloIdL_MR150_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoublePhoton40_CaloIdL_R014_MR150_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon55_CaloIdL_R017_MR500_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon55_CaloIdL_R023_MR350_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon55_CaloIdL_R029_MR250_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon55_CaloIdL_R042_MR200_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT350_Ele5_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_PFMHT45_v12" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_Ele5_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_PFMHT50_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT400_Ele60_CaloIdT_TrkIdT_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HT450_Ele60_CaloIdT_TrkIdT_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele8_CaloIdT_TrkIdT_DiJet30_v10" ),
        prescales = cms.vuint32( 1500, 1200, 900, 900, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele8_CaloIdT_TrkIdT_TriJet30_v10" ),
        prescales = cms.vuint32( 150, 120, 90, 90, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele8_CaloIdT_TrkIdT_QuadJet30_v10" ),
        prescales = cms.vuint32( 10, 8, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele8_CaloIdL_CaloIsoVL_Jet40_v13" ),
        prescales = cms.vuint32( 15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT250_PFMHT40_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT250_PFMHT50_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R014_MR200_v5" ),
        prescales = cms.vuint32( 50, 40, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R025_MR200_v6" ),
        prescales = cms.vuint32( 10, 8, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R029_MR200_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R033_MR200_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele18_CaloIdVT_TrkIdT_MediumIsoPFTau20_v7" ),
        prescales = cms.vuint32( 1, 1, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20_v7" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau25_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_BTagIP_v14" ),
        prescales = cms.vuint32( 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_TrkIdT_CentralPFJet30_v4" ),
        prescales = cms.vuint32( 400, 240, 240, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_TrkIdT_DiCentralPFJet30_v4" ),
        prescales = cms.vuint32( 200, 120, 120, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_TrkIdT_TriCentralPFJet30_v4" ),
        prescales = cms.vuint32( 60, 60, 60, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_TrkIdT_QuadCentralPFJet30_v4" ),
        prescales = cms.vuint32( 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_v10" ),
        prescales = cms.vuint32( 120, 120, 120, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralPFJet30_v4" ),
        prescales = cms.vuint32( 200, 120, 120, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralPFJet30_v4" ),
        prescales = cms.vuint32( 60, 60, 60, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralPFJet30_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_QuadCentralPFJet30_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_BTagIP_v10" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele27_WP80_DiCentralPFJet25_PFMHT15_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele27_WP80_DiCentralPFJet25_v6" ),
        prescales = cms.vuint32( 10, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele27_WP80_DiPFJet25_Deta3_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele27_CaloIdVT_TrkIdT_DiCentralPFJet25_v6" ),
        prescales = cms.vuint32( 40, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele27_CaloIdVT_TrkIdT_DiPFJet25_Deta3_v6" ),
        prescales = cms.vuint32( 50, 25, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele32_WP80_DiCentralPFJet25_PFMHT25_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Ele32_WP80_DiPFJet25_Deta3p5_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Photon30_CaloIdVT_CentralJet20_BTagIP_v8" ),
        prescales = cms.vuint32( 0, 40, 30, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleEle8_CaloIdT_TrkIdVL_Mass8_HT150_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleEle8_CaloIdT_TrkIdVL_Mass8_HT200_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DoubleEle10_CaloIdL_TrkIdVL_Ele10_CaloIdT_TrkIdVL_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_TripleEle10_CaloIdL_TrkIdVL_v12" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_PixelTracks_Multiplicity80_v9" ),
        prescales = cms.vuint32( 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_PixelTracks_Multiplicity100_v9" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_BeamGas_HF_Beam1_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_BeamGas_HF_Beam2_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_BeamHalo_v9" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1Tech_CASTOR_HaloMuon_v2" ),
        prescales = cms.vuint32( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1Tech_DT_GlobalOR_v2" ),
        prescales = cms.vuint32( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1_PreCollisions_v4" ),
        prescales = cms.vuint32( 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1_Interbunch_BSC_v4" ),
        prescales = cms.vuint32( 100, 100, 100, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoTrackHE_v11" ),
        prescales = cms.vuint32( 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_IsoTrackHB_v10" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HcalPhiSym_v9" ),
        prescales = cms.vuint32( 15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HcalNZS_v8" ),
        prescales = cms.vuint32( 15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_GlobalRunHPDNoise_v6" ),
        prescales = cms.vuint32( 1500, 1500, 1500, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 40 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1Tech_HBHEHO_totalOR_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1Tech_HCAL_HF_single_channel_v2" ),
        prescales = cms.vuint32( 500, 500, 500, 500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_ZeroBias_v5" ),
        prescales = cms.vuint32( 50, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 50 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Physics_v3" ),
        prescales = cms.vuint32( 8000, 8000, 8000, 8000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 80 )
      ),
      cms.PSet(  pathName = cms.string( "DST_Physics_v3" ),
        prescales = cms.vuint32( 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DTCalibration_v1" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_EcalCalibration_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_HcalCalibration_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_TrackerCalibration_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_Random_v1" ),
        prescales = cms.vuint32( 600, 600, 600, 600, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 10000 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1SingleMuOpen_AntiBPTX_v4" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1TrackerCosmics_v5" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_RegionalCosmicTracking_v10" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L3MuonsCosmicTracking_v6" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_LogMonitor_v1" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_DTErrors_v2" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLT_L1DoubleJet36Central_v5" ),
        prescales = cms.vuint32( 6000, 6000, 6000, 18000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "AlCa_EcalPi0_v11" ),
        prescales = cms.vuint32( 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "AlCa_EcalEta_v10" ),
        prescales = cms.vuint32( 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "AlCa_EcalPhiSym_v8" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "AlCa_RPCMuonNoTriggers_v7" ),
        prescales = cms.vuint32( 9, 7, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "AlCa_RPCMuonNoHits_v7" ),
        prescales = cms.vuint32( 9, 7, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "AlCa_RPCMuonNormalisation_v7" ),
        prescales = cms.vuint32( 9, 7, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "AlCa_LumiPixels_v3" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "DQM_FEDIntegrity_v6" ),
        prescales = cms.vuint32( 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10 )
      ),
      cms.PSet(  pathName = cms.string( "AForPPOutput" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "DQMForPPOutput" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "ExpressForPPOutput" ),
        prescales = cms.vuint32( 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 )
      ),
      cms.PSet(  pathName = cms.string( "HLTMONOutput" ),
        prescales = cms.vuint32( 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100 )
      )
) ),
    lvl1Labels = cms.vstring( '5e33',
      '4e33',
      '3e33',
      '2.5e33',
      '6000Hz',
      '5000Hz',
      '4000Hz',
      '3000Hz',
      '2000Hz',
      '1500Hz',
      '1000Hz',
      '500Hz',
      'EM1',
      'EM2',
      'Cosmics',
      'Cosmics + High Random' ),
    lvl1DefaultLabel = cms.untracked.string( "3e33" )
)
process.ModuleWebRegistry = cms.Service( "ModuleWebRegistry",
)
process.MicroStateService = cms.Service( "MicroStateService",
)
process.MessageLogger = cms.Service( "MessageLogger",
    debugs = cms.untracked.PSet( 
      threshold = cms.untracked.string( "INFO" ),
      placeholder = cms.untracked.bool( True ),
    ),
    cout = cms.untracked.PSet( 
      threshold = cms.untracked.string( "ERROR" ),
    ),
    cerr_stats = cms.untracked.PSet( 
      threshold = cms.untracked.string( "WARNING" ),
      output = cms.untracked.string( "cerr" ),
      optionalPSet = cms.untracked.bool( True )
    ),
    warnings = cms.untracked.PSet( 
      threshold = cms.untracked.string( "INFO" ),
      placeholder = cms.untracked.bool( True ),
    ),
    statistics = cms.untracked.vstring( 'cerr' ),
    cerr = cms.untracked.PSet( 
      INFO = cms.untracked.PSet(  limit = cms.untracked.int32( 0 ) ),
      noTimeStamps = cms.untracked.bool( False ),
      FwkReport = cms.untracked.PSet( 
        reportEvery = cms.untracked.int32( 1 ),
        limit = cms.untracked.int32( 0 )
      ),
      default = cms.untracked.PSet(  limit = cms.untracked.int32( 10000000 ) ),
      Root_NoDictionary = cms.untracked.PSet(  limit = cms.untracked.int32( 0 ) ),
      FwkJob = cms.untracked.PSet(  limit = cms.untracked.int32( 0 ) ),
      FwkSummary = cms.untracked.PSet( 
        reportEvery = cms.untracked.int32( 1 ),
        limit = cms.untracked.int32( 10000000 )
      ),
      threshold = cms.untracked.string( "INFO" ),
    ),
    FrameworkJobReport = cms.untracked.PSet( 
      default = cms.untracked.PSet(  limit = cms.untracked.int32( 0 ) ),
      FwkJob = cms.untracked.PSet(  limit = cms.untracked.int32( 10000000 ) )
    ),
    suppressWarning = cms.untracked.vstring( 'hltL3MuonsOIState',
      'hltPixelVertices3DbbPhi',
      'hltSiPixelDigis',
      'hltPixelTracksForHighMult',
      'hltSiPixelClusters',
      'hltLightPFTracks',
      'hltPixelTracks',
      'hltOnlineBeamSpot',
      'hltL3MuonsOIHit',
      'hltHITPixelTracksHE',
      'hltHITPixelTracksHB',
      'hltL3MuonsIOHit' ),
    errors = cms.untracked.PSet( 
      threshold = cms.untracked.string( "INFO" ),
      placeholder = cms.untracked.bool( True ),
    ),
    fwkJobReports = cms.untracked.vstring( 'FrameworkJobReport' ),
    infos = cms.untracked.PSet( 
      threshold = cms.untracked.string( "INFO" ),
      Root_NoDictionary = cms.untracked.PSet(  limit = cms.untracked.int32( 0 ) ),
      placeholder = cms.untracked.bool( True ),
    ),
    categories = cms.untracked.vstring( 'FwkJob',
      'FwkReport',
      'FwkSummary',
      'Root_NoDictionary' ),
    destinations = cms.untracked.vstring( 'warnings',
      'errors',
      'infos',
      'debugs',
      'cout',
      'cerr' ),
    threshold = cms.untracked.string( "INFO" ),
    suppressError = cms.untracked.vstring( 'hltOnlineBeamSpot' )
)
process.DTDataIntegrityTask = cms.Service( "DTDataIntegrityTask",
    processingMode = cms.untracked.string( "HLT" ),
    fedIntegrityFolder = cms.untracked.string( "DT/FEDIntegrity_EvF" ),
    getSCInfo = cms.untracked.bool( True )
)
process.DQMStore = cms.Service( "DQMStore",
)
process.DQM = cms.Service( "DQM",
    publishFrequency = cms.untracked.double( 5.0 ),
    debug = cms.untracked.bool( False ),
    collectorPort = cms.untracked.int32( 9190 ),
    collectorHost = cms.untracked.string( "lxplus444.cern.ch" )
)
process.FastTimerService = cms.Service( "FastTimerService",
    dqmPath = cms.untracked.string( "HLT/TimerService" ),
    useRealTimeClock = cms.untracked.bool( True ),
    dqmTimeResolution = cms.untracked.double( 1.0 ),
    enableDQMbyLumi = cms.untracked.bool( False ),
    enableTimingPaths = cms.untracked.bool( True ),
    enableTimingModules = cms.untracked.bool( True ),
    enableDQM = cms.untracked.bool( True ),
    dqmTimeRange = cms.untracked.double( 200.0 ),
    enableTimingSummary = cms.untracked.bool( True )
)

process.hltTriggerType = cms.EDFilter( "HLTTriggerTypeFilter",
    SelectedTriggerType = cms.int32( 1 )
)
process.hltGtDigis = cms.EDProducer( "L1GlobalTriggerRawToDigi",
    DaqGtFedId = cms.untracked.int32( 813 ),
    DaqGtInputTag = cms.InputTag( "rawDataCollector" ),
    UnpackBxInEvent = cms.int32( 5 ),
    ActiveBoardsMask = cms.uint32( 0xffff )
)
process.hltGctDigis = cms.EDProducer( "GctRawToDigi",
    unpackSharedRegions = cms.bool( False ),
    numberOfGctSamplesToUnpack = cms.uint32( 1 ),
    verbose = cms.untracked.bool( False ),
    numberOfRctSamplesToUnpack = cms.uint32( 1 ),
    inputLabel = cms.InputTag( "rawDataCollector" ),
    unpackerVersion = cms.uint32( 0 ),
    gctFedId = cms.untracked.int32( 745 ),
    hltMode = cms.bool( True )
)
process.hltL1GtObjectMap = cms.EDProducer( "L1GlobalTrigger",
    TechnicalTriggersUnprescaled = cms.bool( True ),
    ProduceL1GtObjectMapRecord = cms.bool( True ),
    AlgorithmTriggersUnmasked = cms.bool( False ),
    EmulateBxInEvent = cms.int32( 1 ),
    AlgorithmTriggersUnprescaled = cms.bool( True ),
    ProduceL1GtDaqRecord = cms.bool( False ),
    ReadTechnicalTriggerRecords = cms.bool( True ),
    RecordLength = cms.vint32( 3, 0 ),
    TechnicalTriggersUnmasked = cms.bool( False ),
    ProduceL1GtEvmRecord = cms.bool( False ),
    GmtInputTag = cms.InputTag( "hltGtDigis" ),
    TechnicalTriggersVetoUnmasked = cms.bool( True ),
    AlternativeNrBxBoardEvm = cms.uint32( 0 ),
    TechnicalTriggersInputTags = cms.VInputTag( 'simBscDigis' ),
    CastorInputTag = cms.InputTag( "castorL1Digis" ),
    GctInputTag = cms.InputTag( "hltGctDigis" ),
    AlternativeNrBxBoardDaq = cms.uint32( 0 ),
    WritePsbL1GtDaqRecord = cms.bool( False ),
    BstLengthBytes = cms.int32( -1 )
)
process.hltL1extraParticles = cms.EDProducer( "L1ExtraParticlesProd",
    tauJetSource = cms.InputTag( 'hltGctDigis','tauJets' ),
    etHadSource = cms.InputTag( "hltGctDigis" ),
    etTotalSource = cms.InputTag( "hltGctDigis" ),
    centralBxOnly = cms.bool( True ),
    centralJetSource = cms.InputTag( 'hltGctDigis','cenJets' ),
    etMissSource = cms.InputTag( "hltGctDigis" ),
    hfRingEtSumsSource = cms.InputTag( "hltGctDigis" ),
    produceMuonParticles = cms.bool( True ),
    forwardJetSource = cms.InputTag( 'hltGctDigis','forJets' ),
    ignoreHtMiss = cms.bool( False ),
    htMissSource = cms.InputTag( "hltGctDigis" ),
    produceCaloParticles = cms.bool( True ),
    muonSource = cms.InputTag( "hltGtDigis" ),
    isolatedEmSource = cms.InputTag( 'hltGctDigis','isoEm' ),
    nonIsolatedEmSource = cms.InputTag( 'hltGctDigis','nonIsoEm' ),
    hfRingBitCountsSource = cms.InputTag( "hltGctDigis" )
)
process.hltScalersRawToDigi = cms.EDProducer( "ScalersRawToDigi",
    scalersInputTag = cms.InputTag( "rawDataCollector" )
)
process.hltOnlineBeamSpot = cms.EDProducer( "BeamSpotOnlineProducer",
    maxZ = cms.double( 40.0 ),
    src = cms.InputTag( "hltScalersRawToDigi" ),
    gtEvmLabel = cms.InputTag( "" ),
    changeToCMSCoordinates = cms.bool( False ),
    setSigmaZ = cms.double( 0.0 ),
    maxRadius = cms.double( 2.0 )
)
process.hltOfflineBeamSpot = cms.EDProducer( "BeamSpotProducer" )
process.hltL1sL1DoubleMu0HighQ = cms.EDFilter( "HLTLevel1GTSeed",
    saveTags = cms.bool( True ),
    L1SeedsLogicalExpression = cms.string( "L1_DoubleMu0er_HighQ" ),
    L1MuonCollectionTag = cms.InputTag( "hltL1extraParticles" ),
    L1UseL1TriggerObjectMaps = cms.bool( True ),
    L1UseAliasesForSeeding = cms.bool( True ),
    L1GtReadoutRecordTag = cms.InputTag( "hltGtDigis" ),
    L1CollectionsTag = cms.InputTag( "hltL1extraParticles" ),
    L1NrBxInEvent = cms.int32( 3 ),
    L1GtObjectMapTag = cms.InputTag( "hltL1GtObjectMap" ),
    L1TechTriggerSeeding = cms.bool( False )
)
process.hltPreTau2MuRegPixTrack = cms.EDFilter( "HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag( "hltGtDigis" ),
    offset = cms.uint32( 0 )
)
process.hltDimuonL1Filtered0 = cms.EDFilter( "HLTMuonL1Filter",
    saveTags = cms.bool( True ),
    CSCTFtag = cms.InputTag( "unused" ),
    PreviousCandTag = cms.InputTag( "hltL1sL1DoubleMu0HighQ" ),
    MinPt = cms.double( 0.0 ),
    MinN = cms.int32( 2 ),
    MaxEta = cms.double( 2.5 ),
    SelectQualities = cms.vint32(  ),
    CandTag = cms.InputTag( "hltL1extraParticles" ),
    ExcludeSingleSegmentCSC = cms.bool( False )
)
process.hltMuonDTDigis = cms.EDProducer( "DTUnpackingModule",
    useStandardFEDid = cms.bool( True ),
    inputLabel = cms.InputTag( "rawDataCollector" ),
    dataType = cms.string( "DDU" ),
    fedbyType = cms.bool( False ),
    readOutParameters = cms.PSet( 
      debug = cms.untracked.bool( False ),
      rosParameters = cms.PSet( 
        writeSC = cms.untracked.bool( True ),
        readingDDU = cms.untracked.bool( True ),
        performDataIntegrityMonitor = cms.untracked.bool( False ),
        readDDUIDfromDDU = cms.untracked.bool( True ),
        debug = cms.untracked.bool( False ),
        localDAQ = cms.untracked.bool( False )
      ),
      localDAQ = cms.untracked.bool( False ),
      performDataIntegrityMonitor = cms.untracked.bool( False )
    ),
    dqmOnly = cms.bool( False )
)
process.hltDt1DRecHits = cms.EDProducer( "DTRecHitProducer",
    debug = cms.untracked.bool( False ),
    recAlgoConfig = cms.PSet( 
      tTrigMode = cms.string( "DTTTrigSyncFromDB" ),
      minTime = cms.double( -3.0 ),
      stepTwoFromDigi = cms.bool( False ),
      doVdriftCorr = cms.bool( False ),
      debug = cms.untracked.bool( False ),
      maxTime = cms.double( 420.0 ),
      tTrigModeConfig = cms.PSet( 
        vPropWire = cms.double( 24.4 ),
        doTOFCorrection = cms.bool( True ),
        tofCorrType = cms.int32( 0 ),
        wirePropCorrType = cms.int32( 0 ),
        tTrigLabel = cms.string( "" ),
        doWirePropCorrection = cms.bool( True ),
        doT0Correction = cms.bool( True ),
        debug = cms.untracked.bool( False )
      )
    ),
    dtDigiLabel = cms.InputTag( "hltMuonDTDigis" ),
    recAlgo = cms.string( "DTLinearDriftFromDBAlgo" )
)
process.hltDt4DSegments = cms.EDProducer( "DTRecSegment4DProducer",
    debug = cms.untracked.bool( False ),
    Reco4DAlgoName = cms.string( "DTCombinatorialPatternReco4D" ),
    recHits2DLabel = cms.InputTag( "dt2DSegments" ),
    recHits1DLabel = cms.InputTag( "hltDt1DRecHits" ),
    Reco4DAlgoConfig = cms.PSet( 
      segmCleanerMode = cms.int32( 2 ),
      Reco2DAlgoName = cms.string( "DTCombinatorialPatternReco" ),
      recAlgoConfig = cms.PSet( 
        tTrigMode = cms.string( "DTTTrigSyncFromDB" ),
        minTime = cms.double( -3.0 ),
        stepTwoFromDigi = cms.bool( False ),
        doVdriftCorr = cms.bool( False ),
        debug = cms.untracked.bool( False ),
        maxTime = cms.double( 420.0 ),
        tTrigModeConfig = cms.PSet( 
          vPropWire = cms.double( 24.4 ),
          doTOFCorrection = cms.bool( True ),
          tofCorrType = cms.int32( 0 ),
          wirePropCorrType = cms.int32( 0 ),
          tTrigLabel = cms.string( "" ),
          doWirePropCorrection = cms.bool( True ),
          doT0Correction = cms.bool( True ),
          debug = cms.untracked.bool( False )
        )
      ),
      nSharedHitsMax = cms.int32( 2 ),
      hit_afterT0_resolution = cms.double( 0.03 ),
      Reco2DAlgoConfig = cms.PSet( 
        segmCleanerMode = cms.int32( 2 ),
        recAlgoConfig = cms.PSet( 
          tTrigMode = cms.string( "DTTTrigSyncFromDB" ),
          minTime = cms.double( -3.0 ),
          stepTwoFromDigi = cms.bool( False ),
          doVdriftCorr = cms.bool( False ),
          debug = cms.untracked.bool( False ),
          maxTime = cms.double( 420.0 ),
          tTrigModeConfig = cms.PSet( 
            vPropWire = cms.double( 24.4 ),
            doTOFCorrection = cms.bool( True ),
            tofCorrType = cms.int32( 0 ),
            wirePropCorrType = cms.int32( 0 ),
            tTrigLabel = cms.string( "" ),
            doWirePropCorrection = cms.bool( True ),
            doT0Correction = cms.bool( True ),
            debug = cms.untracked.bool( False )
          )
        ),
        nSharedHitsMax = cms.int32( 2 ),
        AlphaMaxPhi = cms.double( 1.0 ),
        hit_afterT0_resolution = cms.double( 0.03 ),
        MaxAllowedHits = cms.uint32( 50 ),
        performT0_vdriftSegCorrection = cms.bool( False ),
        AlphaMaxTheta = cms.double( 0.9 ),
        debug = cms.untracked.bool( False ),
        recAlgo = cms.string( "DTLinearDriftFromDBAlgo" ),
        nUnSharedHitsMin = cms.int32( 2 ),
        performT0SegCorrection = cms.bool( False ),
        perform_delta_rejecting = cms.bool( False )
      ),
      performT0_vdriftSegCorrection = cms.bool( False ),
      debug = cms.untracked.bool( False ),
      recAlgo = cms.string( "DTLinearDriftFromDBAlgo" ),
      nUnSharedHitsMin = cms.int32( 2 ),
      AllDTRecHits = cms.bool( True ),
      performT0SegCorrection = cms.bool( False ),
      perform_delta_rejecting = cms.bool( False )
    )
)
process.hltMuonCSCDigis = cms.EDProducer( "CSCDCCUnpacker",
    PrintEventNumber = cms.untracked.bool( False ),
    UseSelectiveUnpacking = cms.bool( True ),
    UseExaminer = cms.bool( True ),
    ErrorMask = cms.uint32( 0x0 ),
    InputObjects = cms.InputTag( "rawDataCollector" ),
    UseFormatStatus = cms.bool( True ),
    ExaminerMask = cms.uint32( 0x1febf3f6 ),
    UnpackStatusDigis = cms.bool( False ),
    VisualFEDInspect = cms.untracked.bool( False ),
    FormatedEventDump = cms.untracked.bool( False ),
    Debug = cms.untracked.bool( False ),
    VisualFEDShort = cms.untracked.bool( False )
)
process.hltCsc2DRecHits = cms.EDProducer( "CSCRecHitDProducer",
    XTasymmetry_ME1b = cms.double( 0.0 ),
    XTasymmetry_ME1a = cms.double( 0.0 ),
    ConstSyst_ME1a = cms.double( 0.022 ),
    ConstSyst_ME1b = cms.double( 0.0070 ),
    XTasymmetry_ME41 = cms.double( 0.0 ),
    CSCStripxtalksOffset = cms.double( 0.03 ),
    CSCUseCalibrations = cms.bool( True ),
    CSCUseTimingCorrections = cms.bool( True ),
    CSCNoOfTimeBinsForDynamicPedestal = cms.int32( 2 ),
    XTasymmetry_ME22 = cms.double( 0.0 ),
    UseFivePoleFit = cms.bool( True ),
    XTasymmetry_ME21 = cms.double( 0.0 ),
    ConstSyst_ME21 = cms.double( 0.0 ),
    CSCDebug = cms.untracked.bool( False ),
    ConstSyst_ME22 = cms.double( 0.0 ),
    CSCUseGasGainCorrections = cms.bool( False ),
    XTasymmetry_ME31 = cms.double( 0.0 ),
    readBadChambers = cms.bool( True ),
    NoiseLevel_ME13 = cms.double( 8.0 ),
    NoiseLevel_ME12 = cms.double( 9.0 ),
    NoiseLevel_ME32 = cms.double( 9.0 ),
    NoiseLevel_ME31 = cms.double( 9.0 ),
    XTasymmetry_ME32 = cms.double( 0.0 ),
    ConstSyst_ME41 = cms.double( 0.0 ),
    CSCStripClusterSize = cms.untracked.int32( 3 ),
    CSCStripClusterChargeCut = cms.double( 25.0 ),
    CSCStripPeakThreshold = cms.double( 10.0 ),
    readBadChannels = cms.bool( True ),
    UseParabolaFit = cms.bool( False ),
    XTasymmetry_ME13 = cms.double( 0.0 ),
    XTasymmetry_ME12 = cms.double( 0.0 ),
    wireDigiTag = cms.InputTag( 'hltMuonCSCDigis','MuonCSCWireDigi' ),
    ConstSyst_ME12 = cms.double( 0.0 ),
    ConstSyst_ME13 = cms.double( 0.0 ),
    ConstSyst_ME32 = cms.double( 0.0 ),
    ConstSyst_ME31 = cms.double( 0.0 ),
    UseAverageTime = cms.bool( False ),
    NoiseLevel_ME1a = cms.double( 7.0 ),
    NoiseLevel_ME1b = cms.double( 8.0 ),
    CSCWireClusterDeltaT = cms.int32( 1 ),
    CSCUseStaticPedestals = cms.bool( False ),
    stripDigiTag = cms.InputTag( 'hltMuonCSCDigis','MuonCSCStripDigi' ),
    CSCstripWireDeltaTime = cms.int32( 8 ),
    NoiseLevel_ME21 = cms.double( 9.0 ),
    NoiseLevel_ME22 = cms.double( 9.0 ),
    NoiseLevel_ME41 = cms.double( 9.0 )
)
process.hltCscSegments = cms.EDProducer( "CSCSegmentProducer",
    inputObjects = cms.InputTag( "hltCsc2DRecHits" ),
    algo_psets = cms.VPSet( 
      cms.PSet(  chamber_types = cms.vstring( 'ME1/a',
  'ME1/b',
  'ME1/2',
  'ME1/3',
  'ME2/1',
  'ME2/2',
  'ME3/1',
  'ME3/2',
  'ME4/1',
  'ME4/2' ),
        algo_name = cms.string( "CSCSegAlgoST" ),
        parameters_per_chamber_type = cms.vint32( 2, 1, 1, 1, 1, 1, 1, 1, 1, 1 ),
        algo_psets = cms.VPSet( 
          cms.PSet(  maxRatioResidualPrune = cms.double( 3.0 ),
            yweightPenalty = cms.double( 1.5 ),
            maxRecHitsInCluster = cms.int32( 20 ),
            dPhiFineMax = cms.double( 0.025 ),
            preClusteringUseChaining = cms.bool( True ),
            ForceCovariance = cms.bool( False ),
            hitDropLimit6Hits = cms.double( 0.3333 ),
            NormChi2Cut2D = cms.double( 20.0 ),
            BPMinImprovement = cms.double( 10000.0 ),
            Covariance = cms.double( 0.0 ),
            tanPhiMax = cms.double( 0.5 ),
            SeedBig = cms.double( 0.0015 ),
            onlyBestSegment = cms.bool( False ),
            dRPhiFineMax = cms.double( 8.0 ),
            SeedSmall = cms.double( 2.0E-4 ),
            curvePenalty = cms.double( 2.0 ),
            dXclusBoxMax = cms.double( 4.0 ),
            BrutePruning = cms.bool( True ),
            curvePenaltyThreshold = cms.double( 0.85 ),
            CorrectTheErrors = cms.bool( True ),
            hitDropLimit4Hits = cms.double( 0.6 ),
            useShowering = cms.bool( False ),
            CSCDebug = cms.untracked.bool( False ),
            tanThetaMax = cms.double( 1.2 ),
            NormChi2Cut3D = cms.double( 10.0 ),
            minHitsPerSegment = cms.int32( 3 ),
            ForceCovarianceAll = cms.bool( False ),
            yweightPenaltyThreshold = cms.double( 1.0 ),
            prePrunLimit = cms.double( 3.17 ),
            hitDropLimit5Hits = cms.double( 0.8 ),
            preClustering = cms.bool( True ),
            prePrun = cms.bool( True ),
            maxDPhi = cms.double( 999.0 ),
            maxDTheta = cms.double( 999.0 ),
            Pruning = cms.bool( True ),
            dYclusBoxMax = cms.double( 8.0 )
          ),
          cms.PSet(  maxRatioResidualPrune = cms.double( 3.0 ),
            yweightPenalty = cms.double( 1.5 ),
            maxRecHitsInCluster = cms.int32( 24 ),
            dPhiFineMax = cms.double( 0.025 ),
            preClusteringUseChaining = cms.bool( True ),
            ForceCovariance = cms.bool( False ),
            hitDropLimit6Hits = cms.double( 0.3333 ),
            NormChi2Cut2D = cms.double( 20.0 ),
            BPMinImprovement = cms.double( 10000.0 ),
            Covariance = cms.double( 0.0 ),
            tanPhiMax = cms.double( 0.5 ),
            SeedBig = cms.double( 0.0015 ),
            onlyBestSegment = cms.bool( False ),
            dRPhiFineMax = cms.double( 8.0 ),
            SeedSmall = cms.double( 2.0E-4 ),
            curvePenalty = cms.double( 2.0 ),
            dXclusBoxMax = cms.double( 4.0 ),
            BrutePruning = cms.bool( True ),
            curvePenaltyThreshold = cms.double( 0.85 ),
            CorrectTheErrors = cms.bool( True ),
            hitDropLimit4Hits = cms.double( 0.6 ),
            useShowering = cms.bool( False ),
            CSCDebug = cms.untracked.bool( False ),
            tanThetaMax = cms.double( 1.2 ),
            NormChi2Cut3D = cms.double( 10.0 ),
            minHitsPerSegment = cms.int32( 3 ),
            ForceCovarianceAll = cms.bool( False ),
            yweightPenaltyThreshold = cms.double( 1.0 ),
            prePrunLimit = cms.double( 3.17 ),
            hitDropLimit5Hits = cms.double( 0.8 ),
            preClustering = cms.bool( True ),
            prePrun = cms.bool( True ),
            maxDPhi = cms.double( 999.0 ),
            maxDTheta = cms.double( 999.0 ),
            Pruning = cms.bool( True ),
            dYclusBoxMax = cms.double( 8.0 )
          )
        )
      )
    ),
    algo_type = cms.int32( 1 )
)
process.hltMuonRPCDigis = cms.EDProducer( "RPCUnpackingModule",
    InputLabel = cms.InputTag( "rawDataCollector" ),
    doSynchro = cms.bool( False )
)
process.hltRpcRecHits = cms.EDProducer( "RPCRecHitProducer",
    recAlgoConfig = cms.PSet(  ),
    deadvecfile = cms.FileInPath( "RecoLocalMuon/RPCRecHit/data/RPCDeadVec.dat" ),
    rpcDigiLabel = cms.InputTag( "hltMuonRPCDigis" ),
    maskvecfile = cms.FileInPath( "RecoLocalMuon/RPCRecHit/data/RPCMaskVec.dat" ),
    recAlgo = cms.string( "RPCRecHitStandardAlgo" ),
    deadSource = cms.string( "File" ),
    maskSource = cms.string( "File" )
)
process.hltL2MuonSeeds = cms.EDProducer( "L2MuonSeedGenerator",
    ServiceParameters = cms.PSet( 
      Propagators = cms.untracked.vstring( 'SteppingHelixPropagatorAny' ),
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True )
    ),
    InputObjects = cms.InputTag( "hltL1extraParticles" ),
    L1MaxEta = cms.double( 2.5 ),
    OfflineSeedLabel = cms.untracked.InputTag( "hltL2OfflineMuonSeeds" ),
    L1MinPt = cms.double( 0.0 ),
    L1MinQuality = cms.uint32( 1 ),
    GMTReadoutCollection = cms.InputTag( "hltGtDigis" ),
    UseOfflineSeed = cms.untracked.bool( False ),
    Propagator = cms.string( "SteppingHelixPropagatorAny" )
)
process.hltL2Muons = cms.EDProducer( "L2MuonProducer",
    ServiceParameters = cms.PSet( 
      Propagators = cms.untracked.vstring( 'hltESPFastSteppingHelixPropagatorAny',
        'hltESPFastSteppingHelixPropagatorOpposite' ),
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True )
    ),
    InputObjects = cms.InputTag( "hltL2MuonSeeds" ),
    SeedTransformerParameters = cms.PSet( 
      Fitter = cms.string( "hltESPKFFittingSmootherForL2Muon" ),
      MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
      NMinRecHits = cms.uint32( 2 ),
      UseSubRecHits = cms.bool( False ),
      Propagator = cms.string( "hltESPFastSteppingHelixPropagatorAny" ),
      RescaleError = cms.double( 100.0 )
    ),
    L2TrajBuilderParameters = cms.PSet( 
      DoRefit = cms.bool( False ),
      SeedPropagator = cms.string( "hltESPFastSteppingHelixPropagatorAny" ),
      FilterParameters = cms.PSet( 
        NumberOfSigma = cms.double( 3.0 ),
        FitDirection = cms.string( "insideOut" ),
        DTRecSegmentLabel = cms.InputTag( "hltDt4DSegments" ),
        MaxChi2 = cms.double( 1000.0 ),
        MuonTrajectoryUpdatorParameters = cms.PSet( 
          MaxChi2 = cms.double( 25.0 ),
          RescaleErrorFactor = cms.double( 100.0 ),
          Granularity = cms.int32( 0 ),
          ExcludeRPCFromFit = cms.bool( False ),
          UseInvalidHits = cms.bool( True ),
          RescaleError = cms.bool( False )
        ),
        EnableRPCMeasurement = cms.bool( True ),
        CSCRecSegmentLabel = cms.InputTag( "hltCscSegments" ),
        EnableDTMeasurement = cms.bool( True ),
        RPCRecSegmentLabel = cms.InputTag( "hltRpcRecHits" ),
        Propagator = cms.string( "hltESPFastSteppingHelixPropagatorAny" ),
        EnableCSCMeasurement = cms.bool( True )
      ),
      NavigationType = cms.string( "Standard" ),
      SeedTransformerParameters = cms.PSet( 
        Fitter = cms.string( "hltESPKFFittingSmootherForL2Muon" ),
        MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
        NMinRecHits = cms.uint32( 2 ),
        UseSubRecHits = cms.bool( False ),
        Propagator = cms.string( "hltESPFastSteppingHelixPropagatorAny" ),
        RescaleError = cms.double( 100.0 )
      ),
      DoBackwardFilter = cms.bool( True ),
      SeedPosition = cms.string( "in" ),
      BWFilterParameters = cms.PSet( 
        NumberOfSigma = cms.double( 3.0 ),
        CSCRecSegmentLabel = cms.InputTag( "hltCscSegments" ),
        FitDirection = cms.string( "outsideIn" ),
        DTRecSegmentLabel = cms.InputTag( "hltDt4DSegments" ),
        MaxChi2 = cms.double( 100.0 ),
        MuonTrajectoryUpdatorParameters = cms.PSet( 
          MaxChi2 = cms.double( 25.0 ),
          RescaleErrorFactor = cms.double( 100.0 ),
          Granularity = cms.int32( 2 ),
          ExcludeRPCFromFit = cms.bool( False ),
          UseInvalidHits = cms.bool( True ),
          RescaleError = cms.bool( False )
        ),
        EnableRPCMeasurement = cms.bool( True ),
        BWSeedType = cms.string( "fromGenerator" ),
        EnableDTMeasurement = cms.bool( True ),
        RPCRecSegmentLabel = cms.InputTag( "hltRpcRecHits" ),
        Propagator = cms.string( "hltESPFastSteppingHelixPropagatorAny" ),
        EnableCSCMeasurement = cms.bool( True )
      ),
      DoSeedRefit = cms.bool( False )
    ),
    DoSeedRefit = cms.bool( False ),
    TrackLoaderParameters = cms.PSet( 
      Smoother = cms.string( "hltESPKFTrajectorySmootherForMuonTrackLoader" ),
      DoSmoothing = cms.bool( False ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      MuonUpdatorAtVertexParameters = cms.PSet( 
        MaxChi2 = cms.double( 1000000.0 ),
        BeamSpotPosition = cms.vdouble( 0.0, 0.0, 0.0 ),
        Propagator = cms.string( "hltESPFastSteppingHelixPropagatorOpposite" ),
        BeamSpotPositionErrors = cms.vdouble( 0.1, 0.1, 5.3 )
      ),
      VertexConstraint = cms.bool( True )
    )
)
process.hltL2MuonCandidates = cms.EDProducer( "L2MuonCandidateProducer",
    InputObjects = cms.InputTag( 'hltL2Muons','UpdatedAtVtx' )
)
process.hltDimuonL2PreFiltered0 = cms.EDFilter( "HLTMuonL2PreFilter",
    saveTags = cms.bool( True ),
    MaxDr = cms.double( 9999.0 ),
    CutOnChambers = cms.bool( False ),
    PreviousCandTag = cms.InputTag( "hltDimuonL1Filtered0" ),
    MinPt = cms.double( 0.0 ),
    MinN = cms.int32( 2 ),
    SeedMapTag = cms.InputTag( "hltL2Muons" ),
    MaxEta = cms.double( 2.5 ),
    MinNhits = cms.vint32( 0 ),
    MinDxySig = cms.double( -1.0 ),
    MinNchambers = cms.vint32( 0 ),
    AbsEtaBins = cms.vdouble( 5.0 ),
    MaxDz = cms.double( 9999.0 ),
    CandTag = cms.InputTag( "hltL2MuonCandidates" ),
    BeamSpotTag = cms.InputTag( "hltOnlineBeamSpot" ),
    MinDr = cms.double( -1.0 ),
    NSigmaPt = cms.double( 0.0 ),
    MinNstations = cms.vint32( 0 )
)
process.hltSiPixelDigis = cms.EDProducer( "SiPixelRawToDigi",
    UseQualityInfo = cms.bool( False ),
    CheckPixelOrder = cms.bool( False ),
    InputLabel = cms.InputTag( "rawDataCollector" ),
    UseCablingTree = cms.untracked.bool( True ),
    IncludeErrors = cms.bool( False ),
    ErrorList = cms.vint32(  ),
    Timing = cms.untracked.bool( False )
)
process.hltSiPixelClusters = cms.EDProducer( "SiPixelClusterProducer",
    src = cms.InputTag( "hltSiPixelDigis" ),
    ChannelThreshold = cms.int32( 1000 ),
    maxNumberOfClusters = cms.int32( 20000 ),
    VCaltoElectronGain = cms.int32( 65 ),
    MissCalibrate = cms.untracked.bool( True ),
    SplitClusters = cms.bool( False ),
    VCaltoElectronOffset = cms.int32( -414 ),
    payloadType = cms.string( "HLT" ),
    SeedThreshold = cms.int32( 1000 ),
    ClusterThreshold = cms.double( 4000.0 )
)
process.hltSiPixelRecHits = cms.EDProducer( "SiPixelRecHitConverter",
    VerboseLevel = cms.untracked.int32( 0 ),
    src = cms.InputTag( "hltSiPixelClusters" ),
    CPE = cms.string( "hltESPPixelCPEGeneric" )
)
process.hltSiStripExcludedFEDListProducer = cms.EDProducer( "SiStripExcludedFEDListProducer",
    ProductLabel = cms.InputTag( "rawDataCollector" )
)
process.hltSiStripRawToClustersFacility = cms.EDProducer( "SiStripRawToClusters",
    ProductLabel = cms.InputTag( "rawDataCollector" ),
    Algorithms = cms.PSet( 
      SiStripFedZeroSuppressionMode = cms.uint32( 4 ),
      CommonModeNoiseSubtractionMode = cms.string( "Median" ),
      PedestalSubtractionFedMode = cms.bool( True ),
      TruncateInSuppressor = cms.bool( True ),
      doAPVRestore = cms.bool( False ),
      useCMMeanMap = cms.bool( False )
    ),
    Clusterizer = cms.PSet( 
      ChannelThreshold = cms.double( 2.0 ),
      MaxSequentialBad = cms.uint32( 1 ),
      MaxSequentialHoles = cms.uint32( 0 ),
      Algorithm = cms.string( "ThreeThresholdAlgorithm" ),
      MaxAdjacentBad = cms.uint32( 0 ),
      QualityLabel = cms.string( "" ),
      SeedThreshold = cms.double( 3.0 ),
      ClusterThreshold = cms.double( 5.0 ),
      setDetId = cms.bool( True )
    )
)
process.hltSiStripClusters = cms.EDProducer( "MeasurementTrackerSiStripRefGetterProducer",
    InputModuleLabel = cms.InputTag( "hltSiStripRawToClustersFacility" ),
    measurementTrackerName = cms.string( "hltESPMeasurementTracker" )
)
process.hltL3TrajSeedOIState = cms.EDProducer( "TSGFromL2Muon",
    TkSeedGenerator = cms.PSet( 
      propagatorCompatibleName = cms.string( "hltESPSteppingHelixPropagatorOpposite" ),
      option = cms.uint32( 3 ),
      maxChi2 = cms.double( 40.0 ),
      errorMatrixPset = cms.PSet( 
        atIP = cms.bool( True ),
        action = cms.string( "use" ),
        errorMatrixValuesPSet = cms.PSet( 
          pf3_V12 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
          ),
          pf3_V13 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
          ),
          pf3_V11 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 3.0, 3.0, 3.0, 5.0, 4.0, 5.0, 10.0, 7.0, 10.0, 10.0, 10.0, 10.0 )
          ),
          pf3_V14 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
          ),
          pf3_V15 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
          ),
          yAxis = cms.vdouble( 0.0, 1.0, 1.4, 10.0 ),
          pf3_V33 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 3.0, 3.0, 3.0, 5.0, 4.0, 5.0, 10.0, 7.0, 10.0, 10.0, 10.0, 10.0 )
          ),
          zAxis = cms.vdouble( -3.14159, 3.14159 ),
          pf3_V44 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 3.0, 3.0, 3.0, 5.0, 4.0, 5.0, 10.0, 7.0, 10.0, 10.0, 10.0, 10.0 )
          ),
          xAxis = cms.vdouble( 0.0, 13.0, 30.0, 70.0, 1000.0 ),
          pf3_V22 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 3.0, 3.0, 3.0, 5.0, 4.0, 5.0, 10.0, 7.0, 10.0, 10.0, 10.0, 10.0 )
          ),
          pf3_V23 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
          ),
          pf3_V45 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
          ),
          pf3_V55 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 3.0, 3.0, 3.0, 5.0, 4.0, 5.0, 10.0, 7.0, 10.0, 10.0, 10.0, 10.0 )
          ),
          pf3_V34 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
          ),
          pf3_V35 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
          ),
          pf3_V25 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
          ),
          pf3_V24 = cms.PSet( 
            action = cms.string( "scale" ),
            values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
          )
        )
      ),
      propagatorName = cms.string( "hltESPSteppingHelixPropagatorAlong" ),
      manySeeds = cms.bool( False ),
      copyMuonRecHit = cms.bool( False ),
      ComponentName = cms.string( "TSGForRoadSearch" )
    ),
    ServiceParameters = cms.PSet( 
      Propagators = cms.untracked.vstring( 'hltESPSteppingHelixPropagatorOpposite',
        'hltESPSteppingHelixPropagatorAlong' ),
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True )
    ),
    MuonCollectionLabel = cms.InputTag( 'hltL2Muons','UpdatedAtVtx' ),
    MuonTrackingRegionBuilder = cms.PSet(  ),
    PCut = cms.double( 2.5 ),
    TrackerSeedCleaner = cms.PSet(  ),
    PtCut = cms.double( 1.0 )
)
process.hltL3TrackCandidateFromL2OIState = cms.EDProducer( "CkfTrajectoryMaker",
    src = cms.InputTag( "hltL3TrajSeedOIState" ),
    reverseTrajectories = cms.bool( True ),
    TransientInitialStateEstimatorParameters = cms.PSet( 
      propagatorAlongTISE = cms.string( "PropagatorWithMaterial" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialOpposite" )
    ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    cleanTrajectoryAfterInOut = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    doSeedingRegionRebuilding = cms.bool( False ),
    trackCandidateAlso = cms.bool( True ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    TrajectoryBuilder = cms.string( "hltESPMuonCkfTrajectoryBuilderSeedHit" ),
    maxNSeeds = cms.uint32( 100000 )
)
process.hltL3TkTracksFromL2OIState = cms.EDProducer( "TrackProducer",
    src = cms.InputTag( "hltL3TrackCandidateFromL2OIState" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPKFFittingSmoother" ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTracker = cms.string( "" ),
    alias = cms.untracked.string( "" ),
    NavigationSchool = cms.string( "" ),
    TrajectoryInEvent = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "undefAlgorithm" ),
    Propagator = cms.string( "PropagatorWithMaterial" )
)
process.hltL3MuonsOIState = cms.EDProducer( "L3MuonProducer",
    ServiceParameters = cms.PSet( 
      Propagators = cms.untracked.vstring( 'hltESPSmartPropagatorAny',
        'SteppingHelixPropagatorAny',
        'hltESPSmartPropagator',
        'hltESPSteppingHelixPropagatorOpposite' ),
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True )
    ),
    L3TrajBuilderParameters = cms.PSet( 
      ScaleTECyFactor = cms.double( -1.0 ),
      GlbRefitterParameters = cms.PSet( 
        TrackerSkipSection = cms.int32( -1 ),
        DoPredictionsOnly = cms.bool( False ),
        PropDirForCosmics = cms.bool( False ),
        HitThreshold = cms.int32( 1 ),
        MuonHitsOption = cms.int32( 1 ),
        Chi2CutRPC = cms.double( 1.0 ),
        Fitter = cms.string( "hltESPL3MuKFTrajectoryFitter" ),
        DTRecSegmentLabel = cms.InputTag( "hltDt4DSegments" ),
        TrackerRecHitBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
        MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
        RefitDirection = cms.string( "insideOut" ),
        CSCRecSegmentLabel = cms.InputTag( "hltCscSegments" ),
        Chi2CutCSC = cms.double( 150.0 ),
        Chi2CutDT = cms.double( 10.0 ),
        RefitRPCHits = cms.bool( True ),
        SkipStation = cms.int32( -1 ),
        Propagator = cms.string( "hltESPSmartPropagatorAny" ),
        TrackerSkipSystem = cms.int32( -1 ),
        DYTthrs = cms.vint32( 30, 15 )
      ),
      ScaleTECxFactor = cms.double( -1.0 ),
      TrackerRecHitBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
      MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
      MuonTrackingRegionBuilder = cms.PSet( 
        EtaR_UpperLimit_Par1 = cms.double( 0.25 ),
        EtaR_UpperLimit_Par2 = cms.double( 0.15 ),
        OnDemand = cms.double( -1.0 ),
        Rescale_Dz = cms.double( 3.0 ),
        vertexCollection = cms.InputTag( "pixelVertices" ),
        Rescale_phi = cms.double( 3.0 ),
        Eta_fixed = cms.double( 0.2 ),
        DeltaZ_Region = cms.double( 15.9 ),
        MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
        PhiR_UpperLimit_Par2 = cms.double( 0.2 ),
        Eta_min = cms.double( 0.05 ),
        Phi_fixed = cms.double( 0.2 ),
        DeltaR = cms.double( 0.2 ),
        EscapePt = cms.double( 1.5 ),
        UseFixedRegion = cms.bool( False ),
        PhiR_UpperLimit_Par1 = cms.double( 0.6 ),
        Rescale_eta = cms.double( 3.0 ),
        Phi_min = cms.double( 0.05 ),
        UseVertex = cms.bool( False ),
        beamSpot = cms.InputTag( "hltOnlineBeamSpot" )
      ),
      RefitRPCHits = cms.bool( True ),
      PCut = cms.double( 2.5 ),
      TrackTransformer = cms.PSet( 
        DoPredictionsOnly = cms.bool( False ),
        Fitter = cms.string( "hltESPL3MuKFTrajectoryFitter" ),
        TrackerRecHitBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
        Smoother = cms.string( "hltESPKFTrajectorySmootherForMuonTrackLoader" ),
        MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
        RefitDirection = cms.string( "insideOut" ),
        RefitRPCHits = cms.bool( True ),
        Propagator = cms.string( "hltESPSmartPropagatorAny" )
      ),
      GlobalMuonTrackMatcher = cms.PSet( 
        Pt_threshold1 = cms.double( 0.0 ),
        DeltaDCut_3 = cms.double( 15.0 ),
        MinP = cms.double( 2.5 ),
        MinPt = cms.double( 1.0 ),
        Chi2Cut_1 = cms.double( 50.0 ),
        Pt_threshold2 = cms.double( 9.99999999E8 ),
        LocChi2Cut = cms.double( 0.0010 ),
        Eta_threshold = cms.double( 1.2 ),
        Quality_3 = cms.double( 7.0 ),
        Quality_2 = cms.double( 15.0 ),
        Chi2Cut_2 = cms.double( 50.0 ),
        Chi2Cut_3 = cms.double( 200.0 ),
        DeltaDCut_1 = cms.double( 40.0 ),
        DeltaRCut_2 = cms.double( 0.2 ),
        DeltaRCut_3 = cms.double( 1.0 ),
        DeltaDCut_2 = cms.double( 10.0 ),
        DeltaRCut_1 = cms.double( 0.1 ),
        Propagator = cms.string( "hltESPSmartPropagator" ),
        Quality_1 = cms.double( 20.0 )
      ),
      PtCut = cms.double( 1.0 ),
      TrackerPropagator = cms.string( "SteppingHelixPropagatorAny" ),
      tkTrajLabel = cms.InputTag( "hltL3TkTracksFromL2OIState" )
    ),
    TrackLoaderParameters = cms.PSet( 
      PutTkTrackIntoEvent = cms.untracked.bool( False ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      SmoothTkTrack = cms.untracked.bool( False ),
      MuonSeededTracksInstance = cms.untracked.string( "L2Seeded" ),
      Smoother = cms.string( "hltESPKFTrajectorySmootherForMuonTrackLoader" ),
      MuonUpdatorAtVertexParameters = cms.PSet( 
        MaxChi2 = cms.double( 1000000.0 ),
        Propagator = cms.string( "hltESPSteppingHelixPropagatorOpposite" ),
        BeamSpotPositionErrors = cms.vdouble( 0.1, 0.1, 5.3 )
      ),
      VertexConstraint = cms.bool( False ),
      DoSmoothing = cms.bool( True )
    ),
    MuonCollectionLabel = cms.InputTag( 'hltL2Muons','UpdatedAtVtx' )
)
process.hltL3TrajSeedOIHit = cms.EDProducer( "TSGFromL2Muon",
    TkSeedGenerator = cms.PSet( 
      PSetNames = cms.vstring( 'skipTSG',
        'iterativeTSG' ),
      L3TkCollectionA = cms.InputTag( "hltL3MuonsOIState" ),
      iterativeTSG = cms.PSet( 
        ErrorRescaling = cms.double( 3.0 ),
        beamSpot = cms.InputTag( "offlineBeamSpot" ),
        MaxChi2 = cms.double( 40.0 ),
        errorMatrixPset = cms.PSet( 
          atIP = cms.bool( True ),
          action = cms.string( "use" ),
          errorMatrixValuesPSet = cms.PSet( 
            pf3_V12 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
            ),
            pf3_V13 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
            ),
            pf3_V11 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 3.0, 3.0, 3.0, 5.0, 4.0, 5.0, 10.0, 7.0, 10.0, 10.0, 10.0, 10.0 )
            ),
            pf3_V14 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
            ),
            pf3_V15 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
            ),
            yAxis = cms.vdouble( 0.0, 1.0, 1.4, 10.0 ),
            pf3_V33 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 3.0, 3.0, 3.0, 5.0, 4.0, 5.0, 10.0, 7.0, 10.0, 10.0, 10.0, 10.0 )
            ),
            zAxis = cms.vdouble( -3.14159, 3.14159 ),
            pf3_V44 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 3.0, 3.0, 3.0, 5.0, 4.0, 5.0, 10.0, 7.0, 10.0, 10.0, 10.0, 10.0 )
            ),
            xAxis = cms.vdouble( 0.0, 13.0, 30.0, 70.0, 1000.0 ),
            pf3_V22 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 3.0, 3.0, 3.0, 5.0, 4.0, 5.0, 10.0, 7.0, 10.0, 10.0, 10.0, 10.0 )
            ),
            pf3_V23 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
            ),
            pf3_V45 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
            ),
            pf3_V55 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 3.0, 3.0, 3.0, 5.0, 4.0, 5.0, 10.0, 7.0, 10.0, 10.0, 10.0, 10.0 )
            ),
            pf3_V34 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
            ),
            pf3_V35 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
            ),
            pf3_V25 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
            ),
            pf3_V24 = cms.PSet( 
              action = cms.string( "scale" ),
              values = cms.vdouble( 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 )
            )
          )
        ),
        UpdateState = cms.bool( True ),
        MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
        SelectState = cms.bool( False ),
        SigmaZ = cms.double( 25.0 ),
        ResetMethod = cms.string( "matrix" ),
        ComponentName = cms.string( "TSGFromPropagation" ),
        UseVertexState = cms.bool( True ),
        Propagator = cms.string( "hltESPSmartPropagatorAnyOpposite" )
      ),
      skipTSG = cms.PSet(  ),
      ComponentName = cms.string( "DualByL2TSG" )
    ),
    ServiceParameters = cms.PSet( 
      Propagators = cms.untracked.vstring( 'PropagatorWithMaterial',
        'hltESPSmartPropagatorAnyOpposite' ),
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True )
    ),
    MuonCollectionLabel = cms.InputTag( 'hltL2Muons','UpdatedAtVtx' ),
    MuonTrackingRegionBuilder = cms.PSet(  ),
    PCut = cms.double( 2.5 ),
    TrackerSeedCleaner = cms.PSet( 
      cleanerFromSharedHits = cms.bool( True ),
      ptCleaner = cms.bool( True ),
      TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      directionCleaner = cms.bool( True )
    ),
    PtCut = cms.double( 1.0 )
)
process.hltL3TrackCandidateFromL2OIHit = cms.EDProducer( "CkfTrajectoryMaker",
    src = cms.InputTag( "hltL3TrajSeedOIHit" ),
    reverseTrajectories = cms.bool( True ),
    TransientInitialStateEstimatorParameters = cms.PSet( 
      propagatorAlongTISE = cms.string( "PropagatorWithMaterial" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialOpposite" )
    ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    cleanTrajectoryAfterInOut = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    doSeedingRegionRebuilding = cms.bool( False ),
    trackCandidateAlso = cms.bool( True ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    TrajectoryBuilder = cms.string( "hltESPMuonCkfTrajectoryBuilder" ),
    maxNSeeds = cms.uint32( 100000 )
)
process.hltL3TkTracksFromL2OIHit = cms.EDProducer( "TrackProducer",
    src = cms.InputTag( "hltL3TrackCandidateFromL2OIHit" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPKFFittingSmoother" ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTracker = cms.string( "" ),
    alias = cms.untracked.string( "" ),
    NavigationSchool = cms.string( "" ),
    TrajectoryInEvent = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "undefAlgorithm" ),
    Propagator = cms.string( "PropagatorWithMaterial" )
)
process.hltL3MuonsOIHit = cms.EDProducer( "L3MuonProducer",
    ServiceParameters = cms.PSet( 
      Propagators = cms.untracked.vstring( 'hltESPSmartPropagatorAny',
        'SteppingHelixPropagatorAny',
        'hltESPSmartPropagator',
        'hltESPSteppingHelixPropagatorOpposite' ),
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True )
    ),
    L3TrajBuilderParameters = cms.PSet( 
      ScaleTECyFactor = cms.double( -1.0 ),
      GlbRefitterParameters = cms.PSet( 
        TrackerSkipSection = cms.int32( -1 ),
        DoPredictionsOnly = cms.bool( False ),
        PropDirForCosmics = cms.bool( False ),
        HitThreshold = cms.int32( 1 ),
        MuonHitsOption = cms.int32( 1 ),
        Chi2CutRPC = cms.double( 1.0 ),
        Fitter = cms.string( "hltESPL3MuKFTrajectoryFitter" ),
        DTRecSegmentLabel = cms.InputTag( "hltDt4DSegments" ),
        TrackerRecHitBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
        MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
        RefitDirection = cms.string( "insideOut" ),
        CSCRecSegmentLabel = cms.InputTag( "hltCscSegments" ),
        Chi2CutCSC = cms.double( 150.0 ),
        Chi2CutDT = cms.double( 10.0 ),
        RefitRPCHits = cms.bool( True ),
        SkipStation = cms.int32( -1 ),
        Propagator = cms.string( "hltESPSmartPropagatorAny" ),
        TrackerSkipSystem = cms.int32( -1 ),
        DYTthrs = cms.vint32( 30, 15 )
      ),
      ScaleTECxFactor = cms.double( -1.0 ),
      TrackerRecHitBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
      MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
      MuonTrackingRegionBuilder = cms.PSet( 
        EtaR_UpperLimit_Par1 = cms.double( 0.25 ),
        EtaR_UpperLimit_Par2 = cms.double( 0.15 ),
        OnDemand = cms.double( -1.0 ),
        Rescale_Dz = cms.double( 3.0 ),
        vertexCollection = cms.InputTag( "pixelVertices" ),
        Rescale_phi = cms.double( 3.0 ),
        Eta_fixed = cms.double( 0.2 ),
        DeltaZ_Region = cms.double( 15.9 ),
        MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
        PhiR_UpperLimit_Par2 = cms.double( 0.2 ),
        Eta_min = cms.double( 0.05 ),
        Phi_fixed = cms.double( 0.2 ),
        DeltaR = cms.double( 0.2 ),
        EscapePt = cms.double( 1.5 ),
        UseFixedRegion = cms.bool( False ),
        PhiR_UpperLimit_Par1 = cms.double( 0.6 ),
        Rescale_eta = cms.double( 3.0 ),
        Phi_min = cms.double( 0.05 ),
        UseVertex = cms.bool( False ),
        beamSpot = cms.InputTag( "hltOnlineBeamSpot" )
      ),
      RefitRPCHits = cms.bool( True ),
      PCut = cms.double( 2.5 ),
      TrackTransformer = cms.PSet( 
        DoPredictionsOnly = cms.bool( False ),
        Fitter = cms.string( "hltESPL3MuKFTrajectoryFitter" ),
        TrackerRecHitBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
        Smoother = cms.string( "hltESPKFTrajectorySmootherForMuonTrackLoader" ),
        MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
        RefitDirection = cms.string( "insideOut" ),
        RefitRPCHits = cms.bool( True ),
        Propagator = cms.string( "hltESPSmartPropagatorAny" )
      ),
      GlobalMuonTrackMatcher = cms.PSet( 
        Pt_threshold1 = cms.double( 0.0 ),
        DeltaDCut_3 = cms.double( 15.0 ),
        MinP = cms.double( 2.5 ),
        MinPt = cms.double( 1.0 ),
        Chi2Cut_1 = cms.double( 50.0 ),
        Pt_threshold2 = cms.double( 9.99999999E8 ),
        LocChi2Cut = cms.double( 0.0010 ),
        Eta_threshold = cms.double( 1.2 ),
        Quality_3 = cms.double( 7.0 ),
        Quality_2 = cms.double( 15.0 ),
        Chi2Cut_2 = cms.double( 50.0 ),
        Chi2Cut_3 = cms.double( 200.0 ),
        DeltaDCut_1 = cms.double( 40.0 ),
        DeltaRCut_2 = cms.double( 0.2 ),
        DeltaRCut_3 = cms.double( 1.0 ),
        DeltaDCut_2 = cms.double( 10.0 ),
        DeltaRCut_1 = cms.double( 0.1 ),
        Propagator = cms.string( "hltESPSmartPropagator" ),
        Quality_1 = cms.double( 20.0 )
      ),
      PtCut = cms.double( 1.0 ),
      TrackerPropagator = cms.string( "SteppingHelixPropagatorAny" ),
      tkTrajLabel = cms.InputTag( "hltL3TkTracksFromL2OIHit" )
    ),
    TrackLoaderParameters = cms.PSet( 
      PutTkTrackIntoEvent = cms.untracked.bool( False ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      SmoothTkTrack = cms.untracked.bool( False ),
      MuonSeededTracksInstance = cms.untracked.string( "L2Seeded" ),
      Smoother = cms.string( "hltESPKFTrajectorySmootherForMuonTrackLoader" ),
      MuonUpdatorAtVertexParameters = cms.PSet( 
        MaxChi2 = cms.double( 1000000.0 ),
        Propagator = cms.string( "hltESPSteppingHelixPropagatorOpposite" ),
        BeamSpotPositionErrors = cms.vdouble( 0.1, 0.1, 5.3 )
      ),
      VertexConstraint = cms.bool( False ),
      DoSmoothing = cms.bool( True )
    ),
    MuonCollectionLabel = cms.InputTag( 'hltL2Muons','UpdatedAtVtx' )
)
process.hltL3TkFromL2OICombination = cms.EDProducer( "L3TrackCombiner",
    labels = cms.VInputTag( 'hltL3MuonsOIState','hltL3MuonsOIHit' )
)
process.hltL3TrajSeedIOHit = cms.EDProducer( "TSGFromL2Muon",
    TkSeedGenerator = cms.PSet( 
      PSetNames = cms.vstring( 'skipTSG',
        'iterativeTSG' ),
      L3TkCollectionA = cms.InputTag( "hltL3TkFromL2OICombination" ),
      iterativeTSG = cms.PSet( 
        firstTSG = cms.PSet( 
          ComponentName = cms.string( "TSGFromOrderedHits" ),
          OrderedHitsFactoryPSet = cms.PSet( 
            ComponentName = cms.string( "StandardHitTripletGenerator" ),
            GeneratorPSet = cms.PSet( 
              useBending = cms.bool( True ),
              useFixedPreFiltering = cms.bool( False ),
              maxElement = cms.uint32( 0 ),
              phiPreFiltering = cms.double( 0.3 ),
              extraHitRPhitolerance = cms.double( 0.06 ),
              useMultScattering = cms.bool( True ),
              ComponentName = cms.string( "PixelTripletHLTGenerator" ),
              extraHitRZtolerance = cms.double( 0.06 ),
              SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) )
            ),
            SeedingLayers = cms.string( "hltESPPixelLayerTriplets" )
          ),
          TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" )
        ),
        PSetNames = cms.vstring( 'firstTSG',
          'secondTSG' ),
        ComponentName = cms.string( "CombinedTSG" ),
        thirdTSG = cms.PSet( 
          PSetNames = cms.vstring( 'endcapTSG',
            'barrelTSG' ),
          barrelTSG = cms.PSet(  ),
          endcapTSG = cms.PSet( 
            ComponentName = cms.string( "TSGFromOrderedHits" ),
            OrderedHitsFactoryPSet = cms.PSet( 
              maxElement = cms.uint32( 0 ),
              ComponentName = cms.string( "StandardHitPairGenerator" ),
              SeedingLayers = cms.string( "hltESPMixedLayerPairs" ),
              useOnDemandTracker = cms.untracked.int32( 0 )
            ),
            TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" )
          ),
          etaSeparation = cms.double( 2.0 ),
          ComponentName = cms.string( "DualByEtaTSG" )
        ),
        secondTSG = cms.PSet( 
          ComponentName = cms.string( "TSGFromOrderedHits" ),
          OrderedHitsFactoryPSet = cms.PSet( 
            maxElement = cms.uint32( 0 ),
            ComponentName = cms.string( "StandardHitPairGenerator" ),
            SeedingLayers = cms.string( "hltESPPixelLayerPairs" ),
            useOnDemandTracker = cms.untracked.int32( 0 )
          ),
          TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" )
        )
      ),
      skipTSG = cms.PSet(  ),
      ComponentName = cms.string( "DualByL2TSG" )
    ),
    ServiceParameters = cms.PSet( 
      Propagators = cms.untracked.vstring( 'PropagatorWithMaterial' ),
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True )
    ),
    MuonCollectionLabel = cms.InputTag( 'hltL2Muons','UpdatedAtVtx' ),
    MuonTrackingRegionBuilder = cms.PSet( 
      EtaR_UpperLimit_Par1 = cms.double( 0.25 ),
      EtaR_UpperLimit_Par2 = cms.double( 0.15 ),
      OnDemand = cms.double( -1.0 ),
      Rescale_Dz = cms.double( 3.0 ),
      vertexCollection = cms.InputTag( "pixelVertices" ),
      Rescale_phi = cms.double( 3.0 ),
      Eta_fixed = cms.double( 0.2 ),
      DeltaZ_Region = cms.double( 15.9 ),
      MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
      PhiR_UpperLimit_Par2 = cms.double( 0.2 ),
      Eta_min = cms.double( 0.1 ),
      Phi_fixed = cms.double( 0.2 ),
      DeltaR = cms.double( 0.2 ),
      EscapePt = cms.double( 1.5 ),
      UseFixedRegion = cms.bool( False ),
      PhiR_UpperLimit_Par1 = cms.double( 0.6 ),
      Rescale_eta = cms.double( 3.0 ),
      Phi_min = cms.double( 0.1 ),
      UseVertex = cms.bool( False ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" )
    ),
    PCut = cms.double( 2.5 ),
    TrackerSeedCleaner = cms.PSet( 
      cleanerFromSharedHits = cms.bool( True ),
      ptCleaner = cms.bool( True ),
      TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      directionCleaner = cms.bool( True )
    ),
    PtCut = cms.double( 1.0 )
)
process.hltL3TrackCandidateFromL2IOHit = cms.EDProducer( "CkfTrajectoryMaker",
    src = cms.InputTag( "hltL3TrajSeedIOHit" ),
    reverseTrajectories = cms.bool( False ),
    TransientInitialStateEstimatorParameters = cms.PSet( 
      propagatorAlongTISE = cms.string( "PropagatorWithMaterial" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialOpposite" )
    ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    cleanTrajectoryAfterInOut = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    doSeedingRegionRebuilding = cms.bool( False ),
    trackCandidateAlso = cms.bool( True ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    TrajectoryBuilder = cms.string( "hltESPMuonCkfTrajectoryBuilder" ),
    maxNSeeds = cms.uint32( 100000 )
)
process.hltL3TkTracksFromL2IOHit = cms.EDProducer( "TrackProducer",
    src = cms.InputTag( "hltL3TrackCandidateFromL2IOHit" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPKFFittingSmoother" ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTracker = cms.string( "" ),
    alias = cms.untracked.string( "" ),
    NavigationSchool = cms.string( "" ),
    TrajectoryInEvent = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "undefAlgorithm" ),
    Propagator = cms.string( "PropagatorWithMaterial" )
)
process.hltL3MuonsIOHit = cms.EDProducer( "L3MuonProducer",
    ServiceParameters = cms.PSet( 
      Propagators = cms.untracked.vstring( 'hltESPSmartPropagatorAny',
        'SteppingHelixPropagatorAny',
        'hltESPSmartPropagator',
        'hltESPSteppingHelixPropagatorOpposite' ),
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True )
    ),
    L3TrajBuilderParameters = cms.PSet( 
      ScaleTECyFactor = cms.double( -1.0 ),
      GlbRefitterParameters = cms.PSet( 
        TrackerSkipSection = cms.int32( -1 ),
        DoPredictionsOnly = cms.bool( False ),
        PropDirForCosmics = cms.bool( False ),
        HitThreshold = cms.int32( 1 ),
        MuonHitsOption = cms.int32( 1 ),
        Chi2CutRPC = cms.double( 1.0 ),
        Fitter = cms.string( "hltESPL3MuKFTrajectoryFitter" ),
        DTRecSegmentLabel = cms.InputTag( "hltDt4DSegments" ),
        TrackerRecHitBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
        MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
        RefitDirection = cms.string( "insideOut" ),
        CSCRecSegmentLabel = cms.InputTag( "hltCscSegments" ),
        Chi2CutCSC = cms.double( 150.0 ),
        Chi2CutDT = cms.double( 10.0 ),
        RefitRPCHits = cms.bool( True ),
        SkipStation = cms.int32( -1 ),
        Propagator = cms.string( "hltESPSmartPropagatorAny" ),
        TrackerSkipSystem = cms.int32( -1 ),
        DYTthrs = cms.vint32( 30, 15 )
      ),
      ScaleTECxFactor = cms.double( -1.0 ),
      TrackerRecHitBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
      MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
      MuonTrackingRegionBuilder = cms.PSet( 
        EtaR_UpperLimit_Par1 = cms.double( 0.25 ),
        EtaR_UpperLimit_Par2 = cms.double( 0.15 ),
        OnDemand = cms.double( -1.0 ),
        Rescale_Dz = cms.double( 3.0 ),
        vertexCollection = cms.InputTag( "pixelVertices" ),
        Rescale_phi = cms.double( 3.0 ),
        Eta_fixed = cms.double( 0.2 ),
        DeltaZ_Region = cms.double( 15.9 ),
        MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
        PhiR_UpperLimit_Par2 = cms.double( 0.2 ),
        Eta_min = cms.double( 0.05 ),
        Phi_fixed = cms.double( 0.2 ),
        DeltaR = cms.double( 0.2 ),
        EscapePt = cms.double( 1.5 ),
        UseFixedRegion = cms.bool( False ),
        PhiR_UpperLimit_Par1 = cms.double( 0.6 ),
        Rescale_eta = cms.double( 3.0 ),
        Phi_min = cms.double( 0.05 ),
        UseVertex = cms.bool( False ),
        beamSpot = cms.InputTag( "hltOnlineBeamSpot" )
      ),
      RefitRPCHits = cms.bool( True ),
      PCut = cms.double( 2.5 ),
      TrackTransformer = cms.PSet( 
        DoPredictionsOnly = cms.bool( False ),
        Fitter = cms.string( "hltESPL3MuKFTrajectoryFitter" ),
        TrackerRecHitBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
        Smoother = cms.string( "hltESPKFTrajectorySmootherForMuonTrackLoader" ),
        MuonRecHitBuilder = cms.string( "hltESPMuonTransientTrackingRecHitBuilder" ),
        RefitDirection = cms.string( "insideOut" ),
        RefitRPCHits = cms.bool( True ),
        Propagator = cms.string( "hltESPSmartPropagatorAny" )
      ),
      GlobalMuonTrackMatcher = cms.PSet( 
        Pt_threshold1 = cms.double( 0.0 ),
        DeltaDCut_3 = cms.double( 15.0 ),
        MinP = cms.double( 2.5 ),
        MinPt = cms.double( 1.0 ),
        Chi2Cut_1 = cms.double( 50.0 ),
        Pt_threshold2 = cms.double( 9.99999999E8 ),
        LocChi2Cut = cms.double( 0.0010 ),
        Eta_threshold = cms.double( 1.2 ),
        Quality_3 = cms.double( 7.0 ),
        Quality_2 = cms.double( 15.0 ),
        Chi2Cut_2 = cms.double( 50.0 ),
        Chi2Cut_3 = cms.double( 200.0 ),
        DeltaDCut_1 = cms.double( 40.0 ),
        DeltaRCut_2 = cms.double( 0.2 ),
        DeltaRCut_3 = cms.double( 1.0 ),
        DeltaDCut_2 = cms.double( 10.0 ),
        DeltaRCut_1 = cms.double( 0.1 ),
        Propagator = cms.string( "hltESPSmartPropagator" ),
        Quality_1 = cms.double( 20.0 )
      ),
      PtCut = cms.double( 1.0 ),
      TrackerPropagator = cms.string( "SteppingHelixPropagatorAny" ),
      tkTrajLabel = cms.InputTag( "hltL3TkTracksFromL2IOHit" )
    ),
    TrackLoaderParameters = cms.PSet( 
      PutTkTrackIntoEvent = cms.untracked.bool( False ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      SmoothTkTrack = cms.untracked.bool( False ),
      MuonSeededTracksInstance = cms.untracked.string( "L2Seeded" ),
      Smoother = cms.string( "hltESPKFTrajectorySmootherForMuonTrackLoader" ),
      MuonUpdatorAtVertexParameters = cms.PSet( 
        MaxChi2 = cms.double( 1000000.0 ),
        Propagator = cms.string( "hltESPSteppingHelixPropagatorOpposite" ),
        BeamSpotPositionErrors = cms.vdouble( 0.1, 0.1, 5.3 )
      ),
      VertexConstraint = cms.bool( False ),
      DoSmoothing = cms.bool( True )
    ),
    MuonCollectionLabel = cms.InputTag( 'hltL2Muons','UpdatedAtVtx' )
)
process.hltL3TrajectorySeed = cms.EDProducer( "L3MuonTrajectorySeedCombiner",
    labels = cms.VInputTag( 'hltL3TrajSeedIOHit','hltL3TrajSeedOIState','hltL3TrajSeedOIHit' )
)
process.hltL3TrackCandidateFromL2 = cms.EDProducer( "L3TrackCandCombiner",
    labels = cms.VInputTag( 'hltL3TrackCandidateFromL2IOHit','hltL3TrackCandidateFromL2OIHit','hltL3TrackCandidateFromL2OIState' )
)
process.hltL3TkTracksFromL2 = cms.EDProducer( "L3TrackCombiner",
    labels = cms.VInputTag( 'hltL3TkTracksFromL2IOHit','hltL3TkTracksFromL2OIHit','hltL3TkTracksFromL2OIState' )
)
process.hltL3MuonsLinksCombination = cms.EDProducer( "L3TrackLinksCombiner",
    labels = cms.VInputTag( 'hltL3MuonsOIState','hltL3MuonsOIHit','hltL3MuonsIOHit' )
)
process.hltL3Muons = cms.EDProducer( "L3TrackCombiner",
    labels = cms.VInputTag( 'hltL3MuonsOIState','hltL3MuonsOIHit','hltL3MuonsIOHit' )
)
process.hltL3MuonCandidates = cms.EDProducer( "L3MuonCandidateProducer",
    InputLinksObjects = cms.InputTag( "hltL3MuonsLinksCombination" ),
    InputObjects = cms.InputTag( "hltL3Muons" ),
    MuonPtOption = cms.string( "Tracker" )
)
process.hltTauTo2MuL3Filtered = cms.EDFilter( "HLTMuonDimuonL3Filter",
    saveTags = cms.bool( False ),
    ChargeOpt = cms.int32( 0 ),
    MaxPtMin = cms.vdouble( 1.0E125 ),
    FastAccept = cms.bool( False ),
    CandTag = cms.InputTag( "hltL3MuonCandidates" ),
    PreviousCandTag = cms.InputTag( "hltDimuonL2PreFiltered0" ),
    MaxPtBalance = cms.double( 999999.0 ),
    MaxPtPair = cms.vdouble( 1.0E125 ),
    MaxAcop = cms.double( 999.0 ),
    MinPtMin = cms.vdouble( 0.0 ),
    MaxInvMass = cms.vdouble( 1.7 ),
    MinPtMax = cms.vdouble( 0.0 ),
    BeamSpotTag = cms.InputTag( "hltOfflineBeamSpot" ),
    MaxDz = cms.double( 9999.0 ),
    MinPtPair = cms.vdouble( 0.0 ),
    MaxDr = cms.double( 2.0 ),
    MinAcop = cms.double( -1.0 ),
    MaxDCAMuMu = cms.double( 0.5 ),
    MinNhits = cms.int32( 0 ),
    NSigmaPt = cms.double( 0.0 ),
    MinPtBalance = cms.double( -1.0 ),
    MaxEta = cms.double( 2.5 ),
    MaxRapidityPair = cms.double( 999999.0 ),
    CutCowboys = cms.bool( False ),
    MinInvMass = cms.vdouble( 0.0 )
)
process.hltDisplacedmumuVtxProducerTauTo2Mu = cms.EDProducer( "HLTDisplacedmumuVtxProducer",
    Src = cms.InputTag( "hltL3MuonCandidates" ),
    PreviousCandTag = cms.InputTag( "hltTauTo2MuL3Filtered" ),
    MinPt = cms.double( 0.0 ),
    ChargeOpt = cms.int32( 0 ),
    MaxEta = cms.double( 2.5 ),
    MaxInvMass = cms.double( 1.7 ),
    MinPtPair = cms.double( 0.0 ),
    MinInvMass = cms.double( 0.0 )
)
process.hltDisplacedmumuFilterTauTo2Mu = cms.EDFilter( "HLTDisplacedmumuFilter",
    saveTags = cms.bool( True ),
    FastAccept = cms.bool( True ),
    BeamSpotTag = cms.InputTag( "hltOnlineBeamSpot" ),
    MinVtxProbability = cms.double( 0.15 ),
    MaxLxySignificance = cms.double( -1.0 ),
    DisplacedVertexTag = cms.InputTag( "hltDisplacedmumuVtxProducerTauTo2Mu" ),
    MuonTag = cms.InputTag( "hltL3MuonCandidates" ),
    MinCosinePointingAngle = cms.double( -2.0 ),
    MaxNormalisedChi2 = cms.double( 999999.0 ),
    MinLxySignificance = cms.double( 3.0 )
)
process.hltRegionalPixelTracks = cms.EDProducer( "PixelTrackProducer",
    FilterPSet = cms.PSet( 
      chi2 = cms.double( 1000.0 ),
      nSigmaTipMaxTolerance = cms.double( 0.0 ),
      ComponentName = cms.string( "PixelTrackFilterByKinematics" ),
      nSigmaInvPtTolerance = cms.double( 0.0 ),
      ptMin = cms.double( 0.1 ),
      tipMax = cms.double( 1.0 )
    ),
    useFilterWithES = cms.bool( False ),
    passLabel = cms.string( "pixelTracksL2Tau" ),
    FitterPSet = cms.PSet( 
      ComponentName = cms.string( "PixelFitterByHelixProjections" ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      fixImpactParameter = cms.double( 0.0 )
    ),
    RegionFactoryPSet = cms.PSet( 
      ComponentName = cms.string( "L3MumuTrackingRegion" ),
      RegionPSet = cms.PSet( 
        originRadius = cms.double( 1.0 ),
        ptMin = cms.double( 0.5 ),
        originHalfLength = cms.double( 15.0 ),
        vertexZDefault = cms.double( 0.0 ),
        vertexSrc = cms.string( "hltDisplacedmumuVtxProducerTauTo2Mu" ),
        deltaEtaRegion = cms.double( 0.5 ),
        deltaPhiRegion = cms.double( 0.5 ),
        TrkSrc = cms.InputTag( "hltL3Muons" ),
        UseVtxTks = cms.bool( False )
      )
    ),
    CleanerPSet = cms.PSet(  ComponentName = cms.string( "PixelTrackCleanerBySharedHits" ) ),
    OrderedHitsFactoryPSet = cms.PSet( 
      ComponentName = cms.string( "StandardHitTripletGenerator" ),
      GeneratorPSet = cms.PSet( 
        useBending = cms.bool( True ),
        useFixedPreFiltering = cms.bool( False ),
        maxElement = cms.uint32( 100000 ),
        phiPreFiltering = cms.double( 0.3 ),
        extraHitRPhitolerance = cms.double( 0.06 ),
        useMultScattering = cms.bool( True ),
        SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "LowPtClusterShapeSeedComparitor" ) ),
        extraHitRZtolerance = cms.double( 0.06 ),
        ComponentName = cms.string( "PixelTripletHLTGenerator" )
      ),
      SeedingLayers = cms.string( "hltESPPixelLayerTriplets" )
    )
)
process.hltTrackTauRegionalPixelTrackSelector = cms.EDProducer( "QuarkoniaTrackSelector",
    MinTrackPt = cms.double( 0.0 ),
    muonCandidates = cms.InputTag( "hltL3MuonCandidates" ),
    MaxTrackEta = cms.double( 999.0 ),
    tracks = cms.InputTag( "hltRegionalPixelTracks" ),
    MaxMasses = cms.vdouble( 2.7 ),
    checkCharge = cms.bool( False ),
    MinMasses = cms.vdouble( 1.1 ),
    MinTrackP = cms.double( 1.0 )
)
process.hltTrackTauPixelTrackCands = cms.EDProducer( "ConcreteChargedCandidateProducer",
    src = cms.InputTag( "hltTrackTauRegionalPixelTrackSelector" ),
    particleType = cms.string( "e-" )
)
process.hltTauTo2MuTrackFilter = cms.EDFilter( "HLTmmkFilter",
    saveTags = cms.bool( True ),
    MinD0Significance = cms.double( 0.0 ),
    MinLxySignificance = cms.double( 0.0 ),
    MinPt = cms.double( 0.5 ),
    TrackCand = cms.InputTag( "hltTrackTauPixelTrackCands" ),
    MaxEta = cms.double( 2.5 ),
    ThirdTrackMass = cms.double( 0.106 ),
    FastAccept = cms.bool( True ),
    MaxInvMass = cms.double( 999.0 ),
    MinCosinePointingAngle = cms.double( 0.9 ),
    MaxNormalisedChi2 = cms.double( 10.0 ),
    BeamSpotTag = cms.InputTag( "hltOnlineBeamSpot" ),
    MinInvMass = cms.double( 0.0 ),
    MuCand = cms.InputTag( "hltL3MuonCandidates" )
)
process.hltBoolEnd = cms.EDFilter( "HLTBool",
    result = cms.bool( True )
)
process.hltPreTau2MuRegPixTrackTight = cms.EDFilter( "HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag( "hltGtDigis" ),
    offset = cms.uint32( 0 )
)
process.hltDisplacedmumuFilterTauTo2MuTight = cms.EDFilter( "HLTDisplacedmumuFilter",
    saveTags = cms.bool( True ),
    FastAccept = cms.bool( True ),
    BeamSpotTag = cms.InputTag( "hltOnlineBeamSpot" ),
    MinVtxProbability = cms.double( 0.15 ),
    MaxLxySignificance = cms.double( -1.0 ),
    DisplacedVertexTag = cms.InputTag( "hltDisplacedmumuVtxProducerTauTo2Mu" ),
    MuonTag = cms.InputTag( "hltL3MuonCandidates" ),
    MinCosinePointingAngle = cms.double( -2.0 ),
    MaxNormalisedChi2 = cms.double( 999999.0 ),
    MinLxySignificance = cms.double( 3.0 )
)
process.hltPreTau2MuItTrack = cms.EDFilter( "HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag( "hltGtDigis" ),
    offset = cms.uint32( 0 )
)
process.hltDoubleMuTau2MuL3Filtered = cms.EDFilter( "HLTMuonDimuonL3Filter",
    saveTags = cms.bool( True ),
    ChargeOpt = cms.int32( 0 ),
    MaxPtMin = cms.vdouble( 1.0E125 ),
    FastAccept = cms.bool( False ),
    CandTag = cms.InputTag( "hltL3MuonCandidates" ),
    PreviousCandTag = cms.InputTag( "hltDimuonL2PreFiltered0" ),
    MaxPtBalance = cms.double( 999999.0 ),
    MaxPtPair = cms.vdouble( 1.0E125 ),
    MaxAcop = cms.double( 999.0 ),
    MinPtMin = cms.vdouble( 0.0 ),
    MaxInvMass = cms.vdouble( 1.7 ),
    MinPtMax = cms.vdouble( 0.0 ),
    BeamSpotTag = cms.InputTag( "hltOnlineBeamSpot" ),
    MaxDz = cms.double( 9999.0 ),
    MinPtPair = cms.vdouble( 0.0 ),
    MaxDr = cms.double( 2.0 ),
    MinAcop = cms.double( -999.0 ),
    MaxDCAMuMu = cms.double( 0.5 ),
    MinNhits = cms.int32( 0 ),
    NSigmaPt = cms.double( 0.0 ),
    MinPtBalance = cms.double( -1.0 ),
    MaxEta = cms.double( 2.2 ),
    MaxRapidityPair = cms.double( 999999.0 ),
    CutCowboys = cms.bool( False ),
    MinInvMass = cms.vdouble( 0.0 )
)
process.hltDisplacedmumuVtxProducerDoubleMuTau2Mu = cms.EDProducer( "HLTDisplacedmumuVtxProducer",
    Src = cms.InputTag( "hltL3MuonCandidates" ),
    PreviousCandTag = cms.InputTag( "hltDoubleMuTau2MuL3Filtered" ),
    MinPt = cms.double( 0.0 ),
    ChargeOpt = cms.int32( 0 ),
    MaxEta = cms.double( 2.5 ),
    MaxInvMass = cms.double( 1.7 ),
    MinPtPair = cms.double( 0.0 ),
    MinInvMass = cms.double( 0.0 )
)
process.hltDisplacedmumuFilterDoubleMuTau2Mu = cms.EDFilter( "HLTDisplacedmumuFilter",
    saveTags = cms.bool( True ),
    FastAccept = cms.bool( True ),
    BeamSpotTag = cms.InputTag( "hltOnlineBeamSpot" ),
    MinVtxProbability = cms.double( 0.15 ),
    MaxLxySignificance = cms.double( -1.0 ),
    DisplacedVertexTag = cms.InputTag( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" ),
    MuonTag = cms.InputTag( "hltL3MuonCandidates" ),
    MinCosinePointingAngle = cms.double( -2.0 ),
    MaxNormalisedChi2 = cms.double( 999999.0 ),
    MinLxySignificance = cms.double( 3.0 )
)
process.hltMyPixelTracks = cms.EDProducer( "PixelTrackProducer",
    FilterPSet = cms.PSet( 
      chi2 = cms.double( 1000.0 ),
      nSigmaTipMaxTolerance = cms.double( 0.0 ),
      ComponentName = cms.string( "PixelTrackFilterByKinematics" ),
      nSigmaInvPtTolerance = cms.double( 0.0 ),
      ptMin = cms.double( 0.1 ),
      tipMax = cms.double( 1.0 )
    ),
    useFilterWithES = cms.bool( False ),
    passLabel = cms.string( "Pixel triplet primary tracks with vertex constraint" ),
    FitterPSet = cms.PSet( 
      ComponentName = cms.string( "PixelFitterByHelixProjections" ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      fixImpactParameter = cms.double( 0.0 )
    ),
    RegionFactoryPSet = cms.PSet( 
      ComponentName = cms.string( "GlobalRegionProducerFromBeamSpot" ),
      RegionPSet = cms.PSet( 
        precise = cms.bool( True ),
        originRadius = cms.double( 0.2 ),
        ptMin = cms.double( 0.9 ),
        originHalfLength = cms.double( 24.0 ),
        beamSpot = cms.InputTag( "hltOnlineBeamSpot" )
      )
    ),
    CleanerPSet = cms.PSet(  ComponentName = cms.string( "PixelTrackCleanerBySharedHits" ) ),
    OrderedHitsFactoryPSet = cms.PSet( 
      ComponentName = cms.string( "StandardHitTripletGenerator" ),
      GeneratorPSet = cms.PSet( 
        useBending = cms.bool( True ),
        useFixedPreFiltering = cms.bool( False ),
        maxElement = cms.uint32( 100000 ),
        phiPreFiltering = cms.double( 0.3 ),
        extraHitRPhitolerance = cms.double( 0.06 ),
        useMultScattering = cms.bool( True ),
        SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "LowPtClusterShapeSeedComparitor" ) ),
        extraHitRZtolerance = cms.double( 0.06 ),
        ComponentName = cms.string( "PixelTripletHLTGenerator" )
      ),
      SeedingLayers = cms.string( "hltESPPixelLayerTriplets" )
    )
)
process.hltPFJetPixelSeedsFromPixelTracks = cms.EDProducer( "SeedGeneratorFromProtoTracksEDProducer",
    useEventsWithNoVertex = cms.bool( True ),
    originHalfLength = cms.double( 0.3 ),
    useProtoTrackKinematics = cms.bool( False ),
    InputVertexCollection = cms.InputTag( "hltDisplacedmumuFilterDoubleMuTau2Mu" ),
    TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    InputCollection = cms.InputTag( "hltMyPixelTracks" ),
    originRadius = cms.double( 0.1 )
)
process.hltPFJetCkfTrackCandidates = cms.EDProducer( "CkfTrackCandidateMaker",
    src = cms.InputTag( "hltPFJetPixelSeedsFromPixelTracks" ),
    maxSeedsBeforeCleaning = cms.uint32( 1000 ),
    TransientInitialStateEstimatorParameters = cms.PSet( 
      propagatorAlongTISE = cms.string( "PropagatorWithMaterial" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialOpposite" )
    ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    cleanTrajectoryAfterInOut = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    doSeedingRegionRebuilding = cms.bool( False ),
    maxNSeeds = cms.uint32( 100000 ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    TrajectoryBuilder = cms.string( "hltESPTrajectoryBuilderIT" )
)
process.hltPFJetCtfWithMaterialTracks = cms.EDProducer( "TrackProducer",
    src = cms.InputTag( "hltPFJetCkfTrackCandidates" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPFittingSmootherIT" ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTracker = cms.string( "" ),
    alias = cms.untracked.string( "ctfWithMaterialTracks" ),
    NavigationSchool = cms.string( "" ),
    TrajectoryInEvent = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "iter0" ),
    Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" )
)
process.hltPFlowTrackSelectionHighPurity = cms.EDProducer( "AnalyticalTrackSelector",
    max_d0 = cms.double( 100.0 ),
    minNumber3DLayers = cms.uint32( 0 ),
    applyAbsCutsIfNoPV = cms.bool( False ),
    qualityBit = cms.string( "highPurity" ),
    minNumberLayers = cms.uint32( 3 ),
    chi2n_par = cms.double( 0.7 ),
    useVtxError = cms.bool( False ),
    nSigmaZ = cms.double( 3.0 ),
    dz_par2 = cms.vdouble( 0.4, 4.0 ),
    applyAdaptedPVCuts = cms.bool( True ),
    dz_par1 = cms.vdouble( 0.35, 4.0 ),
    copyTrajectories = cms.untracked.bool( True ),
    vtxNumber = cms.int32( -1 ),
    max_d0NoPV = cms.double( 100.0 ),
    keepAllTracks = cms.bool( False ),
    maxNumberLostLayers = cms.uint32( 1 ),
    beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
    max_relpterr = cms.double( 9999.0 ),
    copyExtras = cms.untracked.bool( True ),
    max_z0NoPV = cms.double( 100.0 ),
    vertexCut = cms.string( "tracksSize>=3" ),
    max_z0 = cms.double( 100.0 ),
    useVertices = cms.bool( True ),
    min_nhits = cms.uint32( 0 ),
    src = cms.InputTag( "hltPFJetCtfWithMaterialTracks" ),
    chi2n_no1Dmod_par = cms.double( 9999.0 ),
    vertices = cms.InputTag( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" ),
    d0_par2 = cms.vdouble( 0.4, 4.0 ),
    d0_par1 = cms.vdouble( 0.3, 4.0 ),
    res_par = cms.vdouble( 0.0030, 0.0010 ),
    minHitsToBypassChecks = cms.uint32( 20 )
)
process.hltIter1ClustersRefRemoval = cms.EDProducer( "HLTTrackClusterRemover",
    doStrip = cms.bool( True ),
    trajectories = cms.InputTag( "hltPFlowTrackSelectionHighPurity" ),
    oldClusterRemovalInfo = cms.InputTag( "" ),
    stripClusters = cms.InputTag( "hltSiStripRawToClustersFacility" ),
    pixelClusters = cms.InputTag( "hltSiPixelClusters" ),
    Common = cms.PSet(  maxChi2 = cms.double( 9.0 ) ),
    doPixel = cms.bool( True )
)
process.hltIter1SiStripClusters = cms.EDProducer( "MeasurementTrackerSiStripRefGetterProducer",
    InputModuleLabel = cms.InputTag( "hltSiStripRawToClustersFacility" ),
    measurementTrackerName = cms.string( "hltIter1ESPMeasurementTracker" )
)
process.hltIter1PFJetPixelSeeds = cms.EDProducer( "SeedGeneratorFromRegionHitsEDProducer",
    RegionFactoryPSet = cms.PSet( 
      ComponentName = cms.string( "L3MumuTrackingRegion" ),
      RegionPSet = cms.PSet( 
        ptMin = cms.double( 0.5 ),
        vertexZDefault = cms.double( 0.0 ),
        vertexSrc = cms.string( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" ),
        originRadius = cms.double( 1.0 ),
        originHalfLength = cms.double( 15.0 ),
        deltaEtaRegion = cms.double( 0.5 ),
        deltaPhiRegion = cms.double( 0.5 ),
        UseVtxTks = cms.bool( True ),
        TrkSrc = cms.InputTag( "hltL3Muons" ),
        measurementTrackerName = cms.string( "hltIter1ESPMeasurementTracker" ),
        searchOpt = cms.bool( True )
      )
    ),
    SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) ),
    ClusterCheckPSet = cms.PSet( 
      PixelClusterCollectionLabel = cms.InputTag( "hltSiPixelClusters" ),
      MaxNumberOfCosmicClusters = cms.uint32( 50000 ),
      doClusterCheck = cms.bool( False ),
      ClusterCollectionLabel = cms.InputTag( "hltSiStripClusters" ),
      MaxNumberOfPixelClusters = cms.uint32( 10000 )
    ),
    OrderedHitsFactoryPSet = cms.PSet( 
      maxElement = cms.uint32( 0 ),
      ComponentName = cms.string( "StandardHitTripletGenerator" ),
      GeneratorPSet = cms.PSet( 
        useBending = cms.bool( True ),
        useFixedPreFiltering = cms.bool( False ),
        maxElement = cms.uint32( 100000 ),
        phiPreFiltering = cms.double( 0.3 ),
        extraHitRPhitolerance = cms.double( 0.032 ),
        useMultScattering = cms.bool( True ),
        ComponentName = cms.string( "PixelTripletHLTGenerator" ),
        extraHitRZtolerance = cms.double( 0.037 ),
        SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) )
      ),
      SeedingLayers = cms.string( "hltIter1ESPPixelLayerTriplets" )
    ),
    SeedCreatorPSet = cms.PSet( 
      ComponentName = cms.string( "SeedFromConsecutiveHitsTripletOnlyCreator" ),
      propagator = cms.string( "PropagatorWithMaterial" )
    ),
    TTRHBuilder = cms.string( "WithTrackAngle" )
)
process.hltIter1PFJetCkfTrackCandidates = cms.EDProducer( "CkfTrackCandidateMaker",
    src = cms.InputTag( "hltIter1PFJetPixelSeeds" ),
    maxSeedsBeforeCleaning = cms.uint32( 1000 ),
    TransientInitialStateEstimatorParameters = cms.PSet( 
      propagatorAlongTISE = cms.string( "PropagatorWithMaterial" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialOpposite" )
    ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    cleanTrajectoryAfterInOut = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    doSeedingRegionRebuilding = cms.bool( False ),
    maxNSeeds = cms.uint32( 100000 ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    TrajectoryBuilder = cms.string( "hltIter1ESPTrajectoryBuilderIT" )
)
process.hltIter1PFJetCtfWithMaterialTracks = cms.EDProducer( "TrackProducer",
    src = cms.InputTag( "hltIter1PFJetCkfTrackCandidates" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPFittingSmootherIT" ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTracker = cms.string( "" ),
    alias = cms.untracked.string( "ctfWithMaterialTracks" ),
    NavigationSchool = cms.string( "" ),
    TrajectoryInEvent = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "iter1" ),
    Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" )
)
process.hltIter1PFlowTrackSelectionHighPurityLoose = cms.EDProducer( "AnalyticalTrackSelector",
    max_d0 = cms.double( 100.0 ),
    minNumber3DLayers = cms.uint32( 0 ),
    applyAbsCutsIfNoPV = cms.bool( False ),
    qualityBit = cms.string( "highPurity" ),
    minNumberLayers = cms.uint32( 3 ),
    chi2n_par = cms.double( 0.7 ),
    useVtxError = cms.bool( False ),
    nSigmaZ = cms.double( 3.0 ),
    dz_par2 = cms.vdouble( 0.9, 3.0 ),
    applyAdaptedPVCuts = cms.bool( True ),
    dz_par1 = cms.vdouble( 0.8, 3.0 ),
    copyTrajectories = cms.untracked.bool( True ),
    vtxNumber = cms.int32( -1 ),
    max_d0NoPV = cms.double( 100.0 ),
    keepAllTracks = cms.bool( False ),
    maxNumberLostLayers = cms.uint32( 1 ),
    beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
    max_relpterr = cms.double( 9999.0 ),
    copyExtras = cms.untracked.bool( True ),
    max_z0NoPV = cms.double( 100.0 ),
    vertexCut = cms.string( "tracksSize>=3" ),
    max_z0 = cms.double( 100.0 ),
    useVertices = cms.bool( True ),
    min_nhits = cms.uint32( 0 ),
    src = cms.InputTag( "hltIter1PFJetCtfWithMaterialTracks" ),
    chi2n_no1Dmod_par = cms.double( 9999.0 ),
    vertices = cms.InputTag( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" ),
    d0_par2 = cms.vdouble( 0.9, 3.0 ),
    d0_par1 = cms.vdouble( 0.85, 3.0 ),
    res_par = cms.vdouble( 0.0030, 0.0010 ),
    minHitsToBypassChecks = cms.uint32( 20 )
)
process.hltIter1PFlowTrackSelectionHighPurityTight = cms.EDProducer( "AnalyticalTrackSelector",
    max_d0 = cms.double( 100.0 ),
    minNumber3DLayers = cms.uint32( 0 ),
    applyAbsCutsIfNoPV = cms.bool( False ),
    qualityBit = cms.string( "highPurity" ),
    minNumberLayers = cms.uint32( 5 ),
    chi2n_par = cms.double( 0.4 ),
    useVtxError = cms.bool( False ),
    nSigmaZ = cms.double( 3.0 ),
    dz_par2 = cms.vdouble( 1.0, 4.0 ),
    applyAdaptedPVCuts = cms.bool( True ),
    dz_par1 = cms.vdouble( 1.0, 4.0 ),
    copyTrajectories = cms.untracked.bool( True ),
    vtxNumber = cms.int32( -1 ),
    max_d0NoPV = cms.double( 100.0 ),
    keepAllTracks = cms.bool( False ),
    maxNumberLostLayers = cms.uint32( 1 ),
    beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
    max_relpterr = cms.double( 9999.0 ),
    copyExtras = cms.untracked.bool( True ),
    max_z0NoPV = cms.double( 100.0 ),
    vertexCut = cms.string( "tracksSize>=3" ),
    max_z0 = cms.double( 100.0 ),
    useVertices = cms.bool( True ),
    min_nhits = cms.uint32( 0 ),
    src = cms.InputTag( "hltIter1PFJetCtfWithMaterialTracks" ),
    chi2n_no1Dmod_par = cms.double( 9999.0 ),
    vertices = cms.InputTag( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" ),
    d0_par2 = cms.vdouble( 1.0, 4.0 ),
    d0_par1 = cms.vdouble( 1.0, 4.0 ),
    res_par = cms.vdouble( 0.0030, 0.0010 ),
    minHitsToBypassChecks = cms.uint32( 20 )
)
process.hltIter1PFlowTrackSelectionHighPurity = cms.EDProducer( "SimpleTrackListMerger",
    ShareFrac = cms.double( 0.19 ),
    promoteTrackQuality = cms.bool( True ),
    MinPT = cms.double( 0.05 ),
    copyExtras = cms.untracked.bool( True ),
    Epsilon = cms.double( -0.0010 ),
    allowFirstHitShare = cms.bool( True ),
    newQuality = cms.string( "confirmed" ),
    MaxNormalizedChisq = cms.double( 1000.0 ),
    TrackProducer1 = cms.string( "hltIter1PFlowTrackSelectionHighPurityLoose" ),
    MinFound = cms.int32( 3 ),
    TrackProducer2 = cms.string( "hltIter1PFlowTrackSelectionHighPurityTight" ),
    LostHitPenalty = cms.double( 20.0 ),
    FoundHitBonus = cms.double( 5.0 )
)
process.hltIter1Merged = cms.EDProducer( "SimpleTrackListMerger",
    ShareFrac = cms.double( 0.19 ),
    promoteTrackQuality = cms.bool( True ),
    MinPT = cms.double( 0.05 ),
    copyExtras = cms.untracked.bool( True ),
    Epsilon = cms.double( -0.0010 ),
    allowFirstHitShare = cms.bool( True ),
    newQuality = cms.string( "confirmed" ),
    MaxNormalizedChisq = cms.double( 1000.0 ),
    TrackProducer1 = cms.string( "hltPFlowTrackSelectionHighPurity" ),
    MinFound = cms.int32( 3 ),
    TrackProducer2 = cms.string( "hltIter1PFlowTrackSelectionHighPurity" ),
    LostHitPenalty = cms.double( 20.0 ),
    FoundHitBonus = cms.double( 5.0 )
)
process.hltIter2ClustersRefRemoval = cms.EDProducer( "HLTTrackClusterRemover",
    doStrip = cms.bool( True ),
    trajectories = cms.InputTag( "hltIter1PFlowTrackSelectionHighPurity" ),
    oldClusterRemovalInfo = cms.InputTag( "hltIter1ClustersRefRemoval" ),
    stripClusters = cms.InputTag( "hltSiStripRawToClustersFacility" ),
    pixelClusters = cms.InputTag( "hltSiPixelClusters" ),
    Common = cms.PSet(  maxChi2 = cms.double( 16.0 ) ),
    doPixel = cms.bool( True )
)
process.hltIter2SiStripClusters = cms.EDProducer( "MeasurementTrackerSiStripRefGetterProducer",
    InputModuleLabel = cms.InputTag( "hltSiStripRawToClustersFacility" ),
    measurementTrackerName = cms.string( "hltIter2ESPMeasurementTracker" )
)
process.hltIter2PFJetPixelSeeds = cms.EDProducer( "SeedGeneratorFromRegionHitsEDProducer",
    RegionFactoryPSet = cms.PSet( 
      ComponentName = cms.string( "L3MumuTrackingRegion" ),
      RegionPSet = cms.PSet( 
        deltaPhiRegion = cms.double( 0.5 ),
        originHalfLength = cms.double( 1.0 ),
        originRadius = cms.double( 15.0 ),
        measurementTrackerName = cms.string( "hltIter2ESPMeasurementTracker" ),
        deltaEtaRegion = cms.double( 0.5 ),
        searchOpt = cms.bool( True ),
        ptMin = cms.double( 0.5 ),
        vertexZDefault = cms.double( 0.0 ),
        TrkSrc = cms.InputTag( "hltL3Muons" ),
        UseVtxTks = cms.bool( True ),
        vertexSrc = cms.string( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" )
      )
    ),
    SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) ),
    ClusterCheckPSet = cms.PSet( 
      PixelClusterCollectionLabel = cms.InputTag( "hltSiPixelClusters" ),
      MaxNumberOfCosmicClusters = cms.uint32( 50000 ),
      doClusterCheck = cms.bool( False ),
      ClusterCollectionLabel = cms.InputTag( "hltSiStripClusters" ),
      MaxNumberOfPixelClusters = cms.uint32( 10000 )
    ),
    OrderedHitsFactoryPSet = cms.PSet( 
      maxElement = cms.uint32( 0 ),
      ComponentName = cms.string( "StandardHitPairGenerator" ),
      GeneratorPSet = cms.PSet( 
        maxElement = cms.uint32( 100000 ),
        SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) )
      ),
      SeedingLayers = cms.string( "hltIter2ESPPixelLayerPairs" )
    ),
    SeedCreatorPSet = cms.PSet( 
      ComponentName = cms.string( "SeedFromConsecutiveHitsCreator" ),
      propagator = cms.string( "PropagatorWithMaterial" )
    ),
    TTRHBuilder = cms.string( "WithTrackAngle" )
)
process.hltIter2PFJetCkfTrackCandidates = cms.EDProducer( "CkfTrackCandidateMaker",
    src = cms.InputTag( "hltIter2PFJetPixelSeeds" ),
    maxSeedsBeforeCleaning = cms.uint32( 1000 ),
    TransientInitialStateEstimatorParameters = cms.PSet( 
      propagatorAlongTISE = cms.string( "PropagatorWithMaterial" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialOpposite" )
    ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    cleanTrajectoryAfterInOut = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    doSeedingRegionRebuilding = cms.bool( False ),
    maxNSeeds = cms.uint32( 100000 ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    TrajectoryBuilder = cms.string( "hltIter2ESPTrajectoryBuilderIT" )
)
process.hltIter2PFJetCtfWithMaterialTracks = cms.EDProducer( "TrackProducer",
    src = cms.InputTag( "hltIter2PFJetCkfTrackCandidates" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPFittingSmootherIT" ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTracker = cms.string( "" ),
    alias = cms.untracked.string( "ctfWithMaterialTracks" ),
    NavigationSchool = cms.string( "" ),
    TrajectoryInEvent = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "iter2" ),
    Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" )
)
process.hltIter2PFlowTrackSelectionHighPurity = cms.EDProducer( "AnalyticalTrackSelector",
    max_d0 = cms.double( 100.0 ),
    minNumber3DLayers = cms.uint32( 0 ),
    applyAbsCutsIfNoPV = cms.bool( False ),
    qualityBit = cms.string( "highPurity" ),
    minNumberLayers = cms.uint32( 3 ),
    chi2n_par = cms.double( 0.7 ),
    useVtxError = cms.bool( False ),
    nSigmaZ = cms.double( 3.0 ),
    dz_par2 = cms.vdouble( 0.4, 4.0 ),
    applyAdaptedPVCuts = cms.bool( True ),
    dz_par1 = cms.vdouble( 0.35, 4.0 ),
    copyTrajectories = cms.untracked.bool( True ),
    vtxNumber = cms.int32( -1 ),
    max_d0NoPV = cms.double( 100.0 ),
    keepAllTracks = cms.bool( False ),
    maxNumberLostLayers = cms.uint32( 1 ),
    beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
    max_relpterr = cms.double( 9999.0 ),
    copyExtras = cms.untracked.bool( True ),
    max_z0NoPV = cms.double( 100.0 ),
    vertexCut = cms.string( "tracksSize>=3" ),
    max_z0 = cms.double( 100.0 ),
    useVertices = cms.bool( True ),
    min_nhits = cms.uint32( 0 ),
    src = cms.InputTag( "hltIter2PFJetCtfWithMaterialTracks" ),
    chi2n_no1Dmod_par = cms.double( 9999.0 ),
    vertices = cms.InputTag( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" ),
    d0_par2 = cms.vdouble( 0.4, 4.0 ),
    d0_par1 = cms.vdouble( 0.3, 4.0 ),
    res_par = cms.vdouble( 0.0030, 0.0010 ),
    minHitsToBypassChecks = cms.uint32( 20 )
)
process.hltIter2Merged = cms.EDProducer( "SimpleTrackListMerger",
    ShareFrac = cms.double( 0.19 ),
    promoteTrackQuality = cms.bool( True ),
    MinPT = cms.double( 0.05 ),
    copyExtras = cms.untracked.bool( True ),
    Epsilon = cms.double( -0.0010 ),
    allowFirstHitShare = cms.bool( True ),
    newQuality = cms.string( "confirmed" ),
    MaxNormalizedChisq = cms.double( 1000.0 ),
    TrackProducer1 = cms.string( "hltIter1Merged" ),
    MinFound = cms.int32( 3 ),
    TrackProducer2 = cms.string( "hltIter2PFlowTrackSelectionHighPurity" ),
    LostHitPenalty = cms.double( 20.0 ),
    FoundHitBonus = cms.double( 5.0 )
)
process.hltIter3ClustersRefRemoval = cms.EDProducer( "HLTTrackClusterRemover",
    doStrip = cms.bool( True ),
    trajectories = cms.InputTag( "hltIter2PFlowTrackSelectionHighPurity" ),
    oldClusterRemovalInfo = cms.InputTag( "hltIter2ClustersRefRemoval" ),
    stripClusters = cms.InputTag( "hltSiStripRawToClustersFacility" ),
    pixelClusters = cms.InputTag( "hltSiPixelClusters" ),
    Common = cms.PSet(  maxChi2 = cms.double( 16.0 ) ),
    doPixel = cms.bool( True )
)
process.hltIter3SiStripClusters = cms.EDProducer( "MeasurementTrackerSiStripRefGetterProducer",
    InputModuleLabel = cms.InputTag( "hltSiStripRawToClustersFacility" ),
    measurementTrackerName = cms.string( "hltIter3ESPMeasurementTracker" )
)
process.hltIter3PFJetMixedSeeds = cms.EDProducer( "SeedGeneratorFromRegionHitsEDProducer",
    RegionFactoryPSet = cms.PSet( 
      ComponentName = cms.string( "L3MumuTrackingRegion" ),
      RegionPSet = cms.PSet( 
        deltaPhiRegion = cms.double( 0.5 ),
        originHalfLength = cms.double( 15.0 ),
        originRadius = cms.double( 1.0 ),
        measurementTrackerName = cms.string( "hltIter3ESPMeasurementTracker" ),
        deltaEtaRegion = cms.double( 0.5 ),
        searchOpt = cms.bool( True ),
        ptMin = cms.double( 0.5 ),
        TrkSrc = cms.InputTag( "hltL3Muons" ),
        UseVtxTks = cms.bool( True ),
        vertexZDefault = cms.double( 0.0 ),
        vertexSrc = cms.string( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" )
      )
    ),
    SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) ),
    ClusterCheckPSet = cms.PSet( 
      PixelClusterCollectionLabel = cms.InputTag( "hltSiPixelClusters" ),
      MaxNumberOfCosmicClusters = cms.uint32( 50000 ),
      doClusterCheck = cms.bool( False ),
      ClusterCollectionLabel = cms.InputTag( "hltSiStripClusters" ),
      MaxNumberOfPixelClusters = cms.uint32( 10000 )
    ),
    OrderedHitsFactoryPSet = cms.PSet( 
      maxElement = cms.uint32( 0 ),
      ComponentName = cms.string( "StandardHitTripletGenerator" ),
      GeneratorPSet = cms.PSet( 
        useBending = cms.bool( True ),
        useFixedPreFiltering = cms.bool( False ),
        maxElement = cms.uint32( 100000 ),
        phiPreFiltering = cms.double( 0.3 ),
        extraHitRPhitolerance = cms.double( 0.032 ),
        useMultScattering = cms.bool( True ),
        ComponentName = cms.string( "PixelTripletHLTGenerator" ),
        extraHitRZtolerance = cms.double( 0.037 ),
        SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) )
      ),
      SeedingLayers = cms.string( "hltIter3ESPLayerTriplets" )
    ),
    SeedCreatorPSet = cms.PSet( 
      ComponentName = cms.string( "SeedFromConsecutiveHitsTripletOnlyCreator" ),
      propagator = cms.string( "PropagatorWithMaterial" )
    ),
    TTRHBuilder = cms.string( "WithTrackAngle" )
)
process.hltIter3PFJetCkfTrackCandidates = cms.EDProducer( "CkfTrackCandidateMaker",
    src = cms.InputTag( "hltIter3PFJetMixedSeeds" ),
    maxSeedsBeforeCleaning = cms.uint32( 1000 ),
    TransientInitialStateEstimatorParameters = cms.PSet( 
      propagatorAlongTISE = cms.string( "PropagatorWithMaterial" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialOpposite" )
    ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    cleanTrajectoryAfterInOut = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    doSeedingRegionRebuilding = cms.bool( False ),
    maxNSeeds = cms.uint32( 100000 ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    TrajectoryBuilder = cms.string( "hltIter3ESPTrajectoryBuilderIT" )
)
process.hltIter3PFJetCtfWithMaterialTracks = cms.EDProducer( "TrackProducer",
    src = cms.InputTag( "hltIter3PFJetCkfTrackCandidates" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPFittingSmootherIT" ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTracker = cms.string( "" ),
    alias = cms.untracked.string( "ctfWithMaterialTracks" ),
    NavigationSchool = cms.string( "" ),
    TrajectoryInEvent = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "iter3" ),
    Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" )
)
process.hltIter3PFlowTrackSelectionHighPurityLoose = cms.EDProducer( "AnalyticalTrackSelector",
    max_d0 = cms.double( 100.0 ),
    minNumber3DLayers = cms.uint32( 0 ),
    applyAbsCutsIfNoPV = cms.bool( False ),
    qualityBit = cms.string( "highPurity" ),
    minNumberLayers = cms.uint32( 3 ),
    chi2n_par = cms.double( 0.7 ),
    useVtxError = cms.bool( False ),
    nSigmaZ = cms.double( 3.0 ),
    dz_par2 = cms.vdouble( 0.9, 3.0 ),
    applyAdaptedPVCuts = cms.bool( True ),
    dz_par1 = cms.vdouble( 0.85, 3.0 ),
    copyTrajectories = cms.untracked.bool( True ),
    vtxNumber = cms.int32( -1 ),
    max_d0NoPV = cms.double( 100.0 ),
    keepAllTracks = cms.bool( False ),
    maxNumberLostLayers = cms.uint32( 1 ),
    beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
    max_relpterr = cms.double( 9999.0 ),
    copyExtras = cms.untracked.bool( True ),
    max_z0NoPV = cms.double( 100.0 ),
    vertexCut = cms.string( "tracksSize>=3" ),
    max_z0 = cms.double( 100.0 ),
    useVertices = cms.bool( True ),
    min_nhits = cms.uint32( 0 ),
    src = cms.InputTag( "hltIter3PFJetCtfWithMaterialTracks" ),
    chi2n_no1Dmod_par = cms.double( 9999.0 ),
    vertices = cms.InputTag( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" ),
    d0_par2 = cms.vdouble( 0.9, 3.0 ),
    d0_par1 = cms.vdouble( 0.85, 3.0 ),
    res_par = cms.vdouble( 0.0030, 0.0010 ),
    minHitsToBypassChecks = cms.uint32( 20 )
)
process.hltIter3PFlowTrackSelectionHighPurityTight = cms.EDProducer( "AnalyticalTrackSelector",
    max_d0 = cms.double( 100.0 ),
    minNumber3DLayers = cms.uint32( 0 ),
    applyAbsCutsIfNoPV = cms.bool( False ),
    qualityBit = cms.string( "highPurity" ),
    minNumberLayers = cms.uint32( 5 ),
    chi2n_par = cms.double( 0.4 ),
    useVtxError = cms.bool( False ),
    nSigmaZ = cms.double( 3.0 ),
    dz_par2 = cms.vdouble( 1.0, 4.0 ),
    applyAdaptedPVCuts = cms.bool( True ),
    dz_par1 = cms.vdouble( 1.0, 4.0 ),
    copyTrajectories = cms.untracked.bool( True ),
    vtxNumber = cms.int32( -1 ),
    max_d0NoPV = cms.double( 100.0 ),
    keepAllTracks = cms.bool( False ),
    maxNumberLostLayers = cms.uint32( 1 ),
    beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
    max_relpterr = cms.double( 9999.0 ),
    copyExtras = cms.untracked.bool( True ),
    max_z0NoPV = cms.double( 100.0 ),
    vertexCut = cms.string( "tracksSize>=3" ),
    max_z0 = cms.double( 100.0 ),
    useVertices = cms.bool( True ),
    min_nhits = cms.uint32( 0 ),
    src = cms.InputTag( "hltIter3PFJetCtfWithMaterialTracks" ),
    chi2n_no1Dmod_par = cms.double( 9999.0 ),
    vertices = cms.InputTag( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" ),
    d0_par2 = cms.vdouble( 1.0, 4.0 ),
    d0_par1 = cms.vdouble( 1.0, 4.0 ),
    res_par = cms.vdouble( 0.0030, 0.0010 ),
    minHitsToBypassChecks = cms.uint32( 20 )
)
process.hltIter3PFlowTrackSelectionHighPurity = cms.EDProducer( "SimpleTrackListMerger",
    ShareFrac = cms.double( 0.19 ),
    promoteTrackQuality = cms.bool( True ),
    MinPT = cms.double( 0.05 ),
    copyExtras = cms.untracked.bool( True ),
    Epsilon = cms.double( -0.0010 ),
    allowFirstHitShare = cms.bool( True ),
    newQuality = cms.string( "confirmed" ),
    MaxNormalizedChisq = cms.double( 1000.0 ),
    TrackProducer1 = cms.string( "hltIter3PFlowTrackSelectionHighPurityLoose" ),
    MinFound = cms.int32( 3 ),
    TrackProducer2 = cms.string( "hltIter3PFlowTrackSelectionHighPurityTight" ),
    LostHitPenalty = cms.double( 20.0 ),
    FoundHitBonus = cms.double( 5.0 )
)
process.hltIter3Merged = cms.EDProducer( "SimpleTrackListMerger",
    ShareFrac = cms.double( 0.19 ),
    promoteTrackQuality = cms.bool( True ),
    MinPT = cms.double( 0.05 ),
    copyExtras = cms.untracked.bool( True ),
    Epsilon = cms.double( -0.0010 ),
    allowFirstHitShare = cms.bool( True ),
    newQuality = cms.string( "confirmed" ),
    MaxNormalizedChisq = cms.double( 1000.0 ),
    TrackProducer1 = cms.string( "hltIter2Merged" ),
    MinFound = cms.int32( 3 ),
    TrackProducer2 = cms.string( "hltIter3PFlowTrackSelectionHighPurity" ),
    LostHitPenalty = cms.double( 20.0 ),
    FoundHitBonus = cms.double( 5.0 )
)
process.hltIter4ClustersRefRemoval = cms.EDProducer( "HLTTrackClusterRemover",
    doStrip = cms.bool( True ),
    trajectories = cms.InputTag( "hltIter3PFlowTrackSelectionHighPurity" ),
    oldClusterRemovalInfo = cms.InputTag( "hltIter3ClustersRefRemoval" ),
    stripClusters = cms.InputTag( "hltSiStripRawToClustersFacility" ),
    pixelClusters = cms.InputTag( "hltSiPixelClusters" ),
    Common = cms.PSet(  maxChi2 = cms.double( 16.0 ) ),
    doPixel = cms.bool( True )
)
process.hltIter4SiStripClusters = cms.EDProducer( "MeasurementTrackerSiStripRefGetterProducer",
    InputModuleLabel = cms.InputTag( "hltSiStripRawToClustersFacility" ),
    measurementTrackerName = cms.string( "hltIter4ESPMeasurementTracker" )
)
process.hltIter4PFJetPixelLessSeeds = cms.EDProducer( "SeedGeneratorFromRegionHitsEDProducer",
    RegionFactoryPSet = cms.PSet( 
      ComponentName = cms.string( "L3MumuTrackingRegion" ),
      RegionPSet = cms.PSet( 
        deltaPhiRegion = cms.double( 0.5 ),
        originHalfLength = cms.double( 1.0 ),
        originRadius = cms.double( 15.0 ),
        measurementTrackerName = cms.string( "hltIter4ESPMeasurementTracker" ),
        deltaEtaRegion = cms.double( 0.5 ),
        searchOpt = cms.bool( True ),
        ptMin = cms.double( 0.5 ),
        UseVtxTks = cms.bool( True ),
        vertexZDefault = cms.double( 0.0 ),
        TrkSrc = cms.InputTag( "hltL3Muons" ),
        vertexSrc = cms.string( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" )
      )
    ),
    SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) ),
    ClusterCheckPSet = cms.PSet( 
      PixelClusterCollectionLabel = cms.InputTag( "hltSiPixelClusters" ),
      MaxNumberOfCosmicClusters = cms.uint32( 50000 ),
      doClusterCheck = cms.bool( False ),
      ClusterCollectionLabel = cms.InputTag( "hltSiStripClusters" ),
      MaxNumberOfPixelClusters = cms.uint32( 10000 )
    ),
    OrderedHitsFactoryPSet = cms.PSet( 
      maxElement = cms.uint32( 0 ),
      ComponentName = cms.string( "StandardHitPairGenerator" ),
      GeneratorPSet = cms.PSet( 
        maxElement = cms.uint32( 100000 ),
        SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) )
      ),
      SeedingLayers = cms.string( "hltIter4ESPPixelLayerPairs" )
    ),
    SeedCreatorPSet = cms.PSet( 
      ComponentName = cms.string( "SeedFromConsecutiveHitsCreator" ),
      propagator = cms.string( "PropagatorWithMaterial" )
    ),
    TTRHBuilder = cms.string( "WithTrackAngle" )
)
process.hltIter4PFJetCkfTrackCandidates = cms.EDProducer( "CkfTrackCandidateMaker",
    src = cms.InputTag( "hltIter4PFJetPixelLessSeeds" ),
    maxSeedsBeforeCleaning = cms.uint32( 1000 ),
    TransientInitialStateEstimatorParameters = cms.PSet( 
      propagatorAlongTISE = cms.string( "PropagatorWithMaterial" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialOpposite" )
    ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    cleanTrajectoryAfterInOut = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    doSeedingRegionRebuilding = cms.bool( False ),
    maxNSeeds = cms.uint32( 100000 ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    TrajectoryBuilder = cms.string( "hltIter4ESPTrajectoryBuilderIT" )
)
process.hltIter4PFJetCtfWithMaterialTracks = cms.EDProducer( "TrackProducer",
    src = cms.InputTag( "hltIter4PFJetCkfTrackCandidates" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPFittingSmootherIT" ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTracker = cms.string( "" ),
    alias = cms.untracked.string( "ctfWithMaterialTracks" ),
    NavigationSchool = cms.string( "" ),
    TrajectoryInEvent = cms.bool( True ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "iter4" ),
    Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" )
)
process.hltIter4PFlowTrackSelectionHighPurity = cms.EDProducer( "AnalyticalTrackSelector",
    max_d0 = cms.double( 100.0 ),
    minNumber3DLayers = cms.uint32( 0 ),
    applyAbsCutsIfNoPV = cms.bool( False ),
    qualityBit = cms.string( "highPurity" ),
    minNumberLayers = cms.uint32( 5 ),
    chi2n_par = cms.double( 0.25 ),
    useVtxError = cms.bool( False ),
    nSigmaZ = cms.double( 3.0 ),
    dz_par2 = cms.vdouble( 1.0, 4.0 ),
    applyAdaptedPVCuts = cms.bool( True ),
    dz_par1 = cms.vdouble( 1.0, 4.0 ),
    copyTrajectories = cms.untracked.bool( True ),
    vtxNumber = cms.int32( -1 ),
    max_d0NoPV = cms.double( 100.0 ),
    keepAllTracks = cms.bool( False ),
    maxNumberLostLayers = cms.uint32( 0 ),
    beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
    max_relpterr = cms.double( 9999.0 ),
    copyExtras = cms.untracked.bool( True ),
    max_z0NoPV = cms.double( 100.0 ),
    vertexCut = cms.string( "tracksSize>=3" ),
    max_z0 = cms.double( 100.0 ),
    useVertices = cms.bool( True ),
    min_nhits = cms.uint32( 0 ),
    src = cms.InputTag( "hltIter4PFJetCtfWithMaterialTracks" ),
    chi2n_no1Dmod_par = cms.double( 9999.0 ),
    vertices = cms.InputTag( "hltDisplacedmumuVtxProducerDoubleMuTau2Mu" ),
    d0_par2 = cms.vdouble( 1.0, 4.0 ),
    d0_par1 = cms.vdouble( 1.0, 4.0 ),
    res_par = cms.vdouble( 0.0030, 0.0010 ),
    minHitsToBypassChecks = cms.uint32( 20 )
)
process.hltIter4Merged = cms.EDProducer( "SimpleTrackListMerger",
    ShareFrac = cms.double( 0.19 ),
    promoteTrackQuality = cms.bool( True ),
    MinPT = cms.double( 0.05 ),
    copyExtras = cms.untracked.bool( True ),
    Epsilon = cms.double( -0.0010 ),
    allowFirstHitShare = cms.bool( True ),
    newQuality = cms.string( "confirmed" ),
    MaxNormalizedChisq = cms.double( 1000.0 ),
    TrackProducer1 = cms.string( "hltIter3Merged" ),
    MinFound = cms.int32( 3 ),
    TrackProducer2 = cms.string( "hltIter4PFlowTrackSelectionHighPurity" ),
    LostHitPenalty = cms.double( 20.0 ),
    FoundHitBonus = cms.double( 5.0 )
)
process.hltTau2MuTkAllTracks = cms.EDProducer( "ConcreteChargedCandidateProducer",
    src = cms.InputTag( "hltIter4Merged" ),
    particleType = cms.string( "pi-" )
)
process.hltTau2MuTkMuMuTkFilter = cms.EDFilter( "HLTmmkFilter",
    saveTags = cms.bool( True ),
    MinD0Significance = cms.double( 0.5 ),
    MinLxySignificance = cms.double( 3.0 ),
    MinPt = cms.double( 0.0 ),
    TrackCand = cms.InputTag( "hltTau2MuTkAllTracks" ),
    MaxEta = cms.double( 2.5 ),
    ThirdTrackMass = cms.double( 0.1 ),
    FastAccept = cms.bool( False ),
    MaxInvMass = cms.double( 999.9 ),
    MinCosinePointingAngle = cms.double( 0.9 ),
    MaxNormalisedChi2 = cms.double( 10.0 ),
    BeamSpotTag = cms.InputTag( "hltOnlineBeamSpot" ),
    MinInvMass = cms.double( 0.0 ),
    MuCand = cms.InputTag( "hltL3MuonCandidates" )
)

process.HLTL1UnpackerSequence = cms.Sequence( process.hltGtDigis + process.hltGctDigis + process.hltL1GtObjectMap + process.hltL1extraParticles )
process.HLTBeamSpot = cms.Sequence( process.hltScalersRawToDigi + process.hltOnlineBeamSpot + process.hltOfflineBeamSpot )
process.HLTBeginSequence = cms.Sequence( process.hltTriggerType + process.HLTL1UnpackerSequence + process.HLTBeamSpot )
process.HLTMuonLocalRecoSequence = cms.Sequence( process.hltMuonDTDigis + process.hltDt1DRecHits + process.hltDt4DSegments + process.hltMuonCSCDigis + process.hltCsc2DRecHits + process.hltCscSegments + process.hltMuonRPCDigis + process.hltRpcRecHits )
process.HLTL2muonrecoNocandSequence = cms.Sequence( process.HLTMuonLocalRecoSequence + process.hltL2MuonSeeds + process.hltL2Muons )
process.HLTL2muonrecoSequence = cms.Sequence( process.HLTL2muonrecoNocandSequence + process.hltL2MuonCandidates )
process.HLTDoLocalPixelSequence = cms.Sequence( process.hltSiPixelDigis + process.hltSiPixelClusters + process.hltSiPixelRecHits )
process.HLTDoLocalStripSequence = cms.Sequence( process.hltSiStripExcludedFEDListProducer + process.hltSiStripRawToClustersFacility + process.hltSiStripClusters )
process.HLTL3muonTkCandidateSequence = cms.Sequence( process.HLTDoLocalPixelSequence + process.HLTDoLocalStripSequence + process.hltL3TrajSeedOIState + process.hltL3TrackCandidateFromL2OIState + process.hltL3TkTracksFromL2OIState + process.hltL3MuonsOIState + process.hltL3TrajSeedOIHit + process.hltL3TrackCandidateFromL2OIHit + process.hltL3TkTracksFromL2OIHit + process.hltL3MuonsOIHit + process.hltL3TkFromL2OICombination + process.hltL3TrajSeedIOHit + process.hltL3TrackCandidateFromL2IOHit + process.hltL3TkTracksFromL2IOHit + process.hltL3MuonsIOHit + process.hltL3TrajectorySeed + process.hltL3TrackCandidateFromL2 )
process.HLTL3muonrecoNocandSequence = cms.Sequence( process.HLTL3muonTkCandidateSequence + process.hltL3TkTracksFromL2 + process.hltL3MuonsLinksCombination + process.hltL3Muons )
process.HLTL3muonrecoSequence = cms.Sequence( process.HLTL3muonrecoNocandSequence + process.hltL3MuonCandidates )
process.HLTTauTo2MuRegionalPixelRecoSequence = cms.Sequence( process.HLTDoLocalPixelSequence + process.hltRegionalPixelTracks + process.hltTrackTauRegionalPixelTrackSelector + process.hltTrackTauPixelTrackCands )
process.HLTEndSequence = cms.Sequence( process.hltBoolEnd )
process.HLTRecopixelSequence = cms.Sequence( process.hltMyPixelTracks )
process.HLTIterativeTrackingIteration0 = cms.Sequence( process.hltPFJetPixelSeedsFromPixelTracks + process.hltPFJetCkfTrackCandidates + process.hltPFJetCtfWithMaterialTracks + process.hltPFlowTrackSelectionHighPurity )
process.HLTIterativeTrackingIteration1 = cms.Sequence( process.hltIter1ClustersRefRemoval + process.hltIter1SiStripClusters + process.hltIter1PFJetPixelSeeds + process.hltIter1PFJetCkfTrackCandidates + process.hltIter1PFJetCtfWithMaterialTracks + process.hltIter1PFlowTrackSelectionHighPurityLoose + process.hltIter1PFlowTrackSelectionHighPurityTight + process.hltIter1PFlowTrackSelectionHighPurity + process.hltIter1Merged )
process.HLTIterativeTrackingIteration2 = cms.Sequence( process.hltIter2ClustersRefRemoval + process.hltIter2SiStripClusters + process.hltIter2PFJetPixelSeeds + process.hltIter2PFJetCkfTrackCandidates + process.hltIter2PFJetCtfWithMaterialTracks + process.hltIter2PFlowTrackSelectionHighPurity + process.hltIter2Merged )
process.HLTIterativeTrackingIteration3 = cms.Sequence( process.hltIter3ClustersRefRemoval + process.hltIter3SiStripClusters + process.hltIter3PFJetMixedSeeds + process.hltIter3PFJetCkfTrackCandidates + process.hltIter3PFJetCtfWithMaterialTracks + process.hltIter3PFlowTrackSelectionHighPurityLoose + process.hltIter3PFlowTrackSelectionHighPurityTight + process.hltIter3PFlowTrackSelectionHighPurity + process.hltIter3Merged )
process.HLTIterativeTrackingIteration4 = cms.Sequence( process.hltIter4ClustersRefRemoval + process.hltIter4SiStripClusters + process.hltIter4PFJetPixelLessSeeds + process.hltIter4PFJetCkfTrackCandidates + process.hltIter4PFJetCtfWithMaterialTracks + process.hltIter4PFlowTrackSelectionHighPurity + process.hltIter4Merged )
process.HLTIterativeTracking = cms.Sequence( process.HLTIterativeTrackingIteration0 + process.HLTIterativeTrackingIteration1 + process.HLTIterativeTrackingIteration2 + process.HLTIterativeTrackingIteration3 + process.HLTIterativeTrackingIteration4 )

process.HLT_Tau2Mu_RegPixTrack_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1DoubleMu0HighQ + process.hltPreTau2MuRegPixTrack + process.hltDimuonL1Filtered0 + process.HLTL2muonrecoSequence + process.hltDimuonL2PreFiltered0 + process.HLTL3muonrecoSequence + process.hltTauTo2MuL3Filtered + process.hltDisplacedmumuVtxProducerTauTo2Mu + process.hltDisplacedmumuFilterTauTo2Mu + process.HLTTauTo2MuRegionalPixelRecoSequence + process.hltTauTo2MuTrackFilter + process.HLTEndSequence )
process.HLT_Tau2Mu_RegPixTrack_Tight_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1DoubleMu0HighQ + process.hltPreTau2MuRegPixTrackTight + process.hltDimuonL1Filtered0 + process.HLTL2muonrecoSequence + process.hltDimuonL2PreFiltered0 + process.HLTL3muonrecoSequence + process.hltTauTo2MuL3Filtered + process.hltDisplacedmumuVtxProducerTauTo2Mu + process.hltDisplacedmumuFilterTauTo2Mu + process.hltDisplacedmumuFilterTauTo2MuTight + process.HLTTauTo2MuRegionalPixelRecoSequence + process.hltTauTo2MuTrackFilter + process.HLTEndSequence )
process.HLT_Tau2Mu_ItTrack_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1DoubleMu0HighQ + process.hltPreTau2MuItTrack + process.hltDimuonL1Filtered0 + process.HLTL2muonrecoSequence + process.hltDimuonL2PreFiltered0 + process.HLTL3muonrecoSequence + process.hltDoubleMuTau2MuL3Filtered + process.hltDisplacedmumuVtxProducerDoubleMuTau2Mu + process.hltDisplacedmumuFilterDoubleMuTau2Mu + process.HLTDoLocalPixelSequence + process.HLTRecopixelSequence + process.HLTDoLocalStripSequence + process.HLTIterativeTracking + process.hltTau2MuTkAllTracks + process.hltTau2MuTkMuMuTkFilter + process.HLTEndSequence )


process.source = cms.Source( "PoolSource",
    fileNames = cms.untracked.vstring(
        'file:/data1/Tau3Mu/52X/SIM/v1/DsTau3Mu-SIM/fullSimRaw_SIM_DIGI_L1_DIGI2RAW_2.root',
    ),
    secondaryFileNames = cms.untracked.vstring(
    ),
    inputCommands = cms.untracked.vstring(
        'keep *'
    )
)

# En-able HF Noise filters in GRun menu
if 'hltHfreco' in process.__dict__:
    process.hltHfreco.setNoiseFlags = cms.bool( True )

# override the L1 menu from an Xml file
process.l1GtTriggerMenuXml = cms.ESProducer("L1GtTriggerMenuXmlProducer",
  TriggerMenuLuminosity = cms.string('startup'),
  DefXmlFile = cms.string('L1Menu_Collisions2012_v0_L1T_Scales_20101224_Imp0_0x1027.xml'),
  VmeXmlFile = cms.string('')
)
process.L1GtTriggerMenuRcdSource = cms.ESSource("EmptyESSource",
  recordName = cms.string('L1GtTriggerMenuRcd'),
  iovIsRunNotTime = cms.bool(True),
  firstValid = cms.vuint32(1)
)
process.es_prefer_l1GtParameters = cms.ESPrefer('L1GtTriggerMenuXmlProducer','l1GtTriggerMenuXml') 

# remove the HLT prescales
if 'PrescaleService' in process.__dict__:
    process.PrescaleService.lvl1DefaultLabel = cms.untracked.string( '0' )
    process.PrescaleService.lvl1Labels       = cms.vstring( '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' )
    process.PrescaleService.prescaleTable    = cms.VPSet( )

# CMSSW version specific customizations
import os
cmsswVersion = os.environ['CMSSW_VERSION']

# override the process name
process.setName_('HLTX')

# adapt HLT modules to the correct process name
if 'hltTrigReport' in process.__dict__:
    process.hltTrigReport.HLTriggerResults                    = cms.InputTag( 'TriggerResults', '', 'HLTX' )

if 'hltPreExpressCosmicsOutputSmart' in process.__dict__:
    process.hltPreExpressCosmicsOutputSmart.TriggerResultsTag = cms.InputTag( 'TriggerResults', '', 'HLTX' )

if 'hltPreExpressOutputSmart' in process.__dict__:
    process.hltPreExpressOutputSmart.TriggerResultsTag        = cms.InputTag( 'TriggerResults', '', 'HLTX' )

if 'hltPreDQMForHIOutputSmart' in process.__dict__:
    process.hltPreDQMForHIOutputSmart.TriggerResultsTag       = cms.InputTag( 'TriggerResults', '', 'HLTX' )

if 'hltPreDQMForPPOutputSmart' in process.__dict__:
    process.hltPreDQMForPPOutputSmart.TriggerResultsTag       = cms.InputTag( 'TriggerResults', '', 'HLTX' )

if 'hltPreHLTDQMResultsOutputSmart' in process.__dict__:
    process.hltPreHLTDQMResultsOutputSmart.TriggerResultsTag  = cms.InputTag( 'TriggerResults', '', 'HLTX' )

if 'hltPreHLTDQMOutputSmart' in process.__dict__:
    process.hltPreHLTDQMOutputSmart.TriggerResultsTag         = cms.InputTag( 'TriggerResults', '', 'HLTX' )

if 'hltPreHLTMONOutputSmart' in process.__dict__:
    process.hltPreHLTMONOutputSmart.TriggerResultsTag         = cms.InputTag( 'TriggerResults', '', 'HLTX' )

if 'hltDQMHLTScalers' in process.__dict__:
    process.hltDQMHLTScalers.triggerResults                   = cms.InputTag( 'TriggerResults', '', 'HLTX' )
    process.hltDQMHLTScalers.processname                      = 'HLTX'

if 'hltDQML1SeedLogicScalers' in process.__dict__:
    process.hltDQML1SeedLogicScalers.processname              = 'HLTX'

# add a single "keep *" output
process.hltOutputFULL = cms.OutputModule( "PoolOutputModule",
    fileName = cms.untracked.string( "outputFULL.root" ),
    fastCloning = cms.untracked.bool( False ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string( 'RECO' ),
        filterName = cms.untracked.string( '' )
    ),
    outputCommands = cms.untracked.vstring( 'keep *' )
)
process.FULLOutput = cms.EndPath( process.hltOutputFULL )

# limit the number of events to be processed
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( 100 )
)

# enable the TrigReport and TimeReport
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool( True )
)

# override the GlobalTag, connection string and pfnPrefix
if 'GlobalTag' in process.__dict__:
    process.GlobalTag.connect   = 'frontier://FrontierProd/CMS_COND_31X_GLOBALTAG'
    process.GlobalTag.pfnPrefix = cms.untracked.string('frontier://FrontierProd/')
    process.GlobalTag.globaltag = 'START52_V2A::All'

# customize the L1 emulator to run customiseL1GtEmulatorFromRaw with HLT to switchToSimGtDigis
process.load( 'Configuration.StandardSequences.RawToDigi_cff' )
process.load( 'Configuration.StandardSequences.SimL1Emulator_cff' )
import L1Trigger.Configuration.L1Trigger_custom
process = L1Trigger.Configuration.L1Trigger_custom.customiseL1GtEmulatorFromRaw( process )
process = L1Trigger.Configuration.L1Trigger_custom.customiseResetPrescalesAndMasks( process )

# customize the HLT to use the emulated results
import HLTrigger.Configuration.customizeHLTforL1Emulator
process = HLTrigger.Configuration.customizeHLTforL1Emulator.switchToL1Emulator( process )
process = HLTrigger.Configuration.customizeHLTforL1Emulator.switchToSimGtDigis( process )

if 'MessageLogger' in process.__dict__:
    process.MessageLogger.categories.append('TriggerSummaryProducerAOD')
    process.MessageLogger.categories.append('L1GtTrigReport')
    process.MessageLogger.categories.append('HLTrigReport')

