import FWCore.ParameterSet.Config as cms

process = cms.Process("DTOffAna")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/data/c/cerminar/data/GlobalRun/run61642_BeamSplash/Run61642_EventNumberSkim_RAW.root')
)
process.muonsEndCapsOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('inner tracks', 
        'links', 
        'outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("ctfWithMaterialTracksP5", "globalCosmicMuonsEndCapsOnly", "cosmicMuonsEndCapsOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.STAMuonsNoDriftBarrelOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("cosmicMuonsNoDriftBarrelOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.cosmicBasicClusters = cms.EDProducer("CosmicClusterProducer",
    endcapUnHitCollection = cms.string('EcalUncalibRecHitsEE'),
    endcapHitProducer = cms.string('ecalRecHit'),
    barrelUnHitProducer = cms.string('ecalFixedAlphaBetaFitUncalibRecHit'),
    barrelUHitProducer = cms.string('ecalFixedAlphaBetaFitUncalibRecHit'),
    EndcapSecondThr = cms.double(9.99),
    VerbosityLevel = cms.string('ERROR'),
    barrelUHitCollection = cms.string('EcalUncalibRecHitsEB'),
    posCalc_t0_endcPresh = cms.double(1.2),
    posCalc_logweight = cms.bool(True),
    BarrelSingleThr = cms.double(14.99),
    barrelHitCollection = cms.string('EcalRecHitsEB'),
    barrelShapeAssociation = cms.string('CosmicBarrelShapeAssoc'),
    posCalc_w0 = cms.double(4.2),
    clustershapecollectionEE = cms.string('CosmicEndcapShape'),
    clustershapecollectionEB = cms.string('CosmicBarrelShape'),
    EndcapSingleThr = cms.double(25.99),
    endcapClusterCollection = cms.string('CosmicEndcapBasicClusters'),
    BarrelSecondThr = cms.double(4.99),
    EndcapSeedThr = cms.double(9.99),
    barrelUnHitCollection = cms.string('EcalUncalibRecHitsEB'),
    posCalc_t0_endc = cms.double(3.1),
    endcapUnHitProducer = cms.string('ecalFixedAlphaBetaFitUncalibRecHit'),
    posCalc_t0_barl = cms.double(7.4),
    endcapUHitProducer = cms.string('ecalFixedAlphaBetaFitUncalibRecHit'),
    EndcapSupThr = cms.double(3.0),
    posCalc_x0 = cms.double(0.89),
    endcapHitCollection = cms.string('EcalRecHitsEE'),
    BarrelSeedThr = cms.double(4.99),
    endcapShapeAssociation = cms.string('CosmicEndcapShapeAssoc'),
    BarrelSupThr = cms.double(2.0),
    barrelHitProducer = cms.string('ecalRecHit'),
    barrelClusterCollection = cms.string('CosmicBarrelBasicClusters'),
    endcapUHitCollection = cms.string('EcalUncalibRecHitsEB')
)


process.thPLSeeds = cms.EDProducer("SeedGeneratorFromRegionHitsEDProducer",
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            originHalfLength = cms.double(17.5),
            originZPos = cms.double(0.0),
            originYPos = cms.double(0.0),
            ptMin = cms.double(0.3),
            originXPos = cms.double(0.0),
            originRadius = cms.double(0.2)
        ),
        ComponentName = cms.string('GlobalRegionProducer')
    ),
    TTRHBuilder = cms.string('WithTrackAngle'),
    OrderedHitsFactoryPSet = cms.PSet(
        ComponentName = cms.string('StandardHitPairGenerator'),
        SeedingLayers = cms.string('ThLayerPairs')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    )
)


process.TKMuons = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('inner tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("ctfWithMaterialTracksP5"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.dedxHarmonic2 = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    MeVperADCStrip = cms.double(0.0009025),
    tracks = cms.InputTag("generalTracks"),
    UsePixel = cms.bool(True),
    estimator = cms.string('generic'),
    trajectoryTrackAssociation = cms.InputTag("generalTracks"),
    exponent = cms.double(-2.0)
)


process.muParamGlobalIsoDepositCalByAssociatorHits = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(True),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        ),
        Threshold_HO = cms.double(0.1),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.1),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.025),
        Noise_HO = cms.double(0.2)
    )
)


process.htMetIC5 = cms.EDProducer("METProducer",
    src = cms.InputTag("iterativeCone5CaloJets"),
    METType = cms.string('MET'),
    alias = cms.string('HTMETIC5'),
    noHF = cms.bool(False),
    globalThreshold = cms.double(5.0),
    InputType = cms.string('CaloJetCollection')
)


process.siPixelClusters = cms.EDProducer("SiPixelClusterProducer",
    src = cms.InputTag("siPixelDigis"),
    ChannelThreshold = cms.int32(2500),
    MissCalibrate = cms.untracked.bool(True),
    VCaltoElectronGain = cms.int32(65),
    VCaltoElectronOffset = cms.int32(0),
    payloadType = cms.string('Offline'),
    SeedThreshold = cms.int32(3000),
    ClusterThreshold = cms.double(5050.0)
)


process.photons = cms.EDProducer("PhotonProducer",
    scHybridBarrelProducer = cms.InputTag("cosmicSuperClusters","CosmicBarrelSuperClusters"),
    minR9 = cms.double(0.93),
    usePrimaryVertex = cms.bool(False),
    conversionCollection = cms.string(''),
    primaryVertexProducer = cms.string('offlinePrimaryVerticesWithBS'),
    scIslandEndcapProducer = cms.InputTag("cosmicSuperClusters","CosmicEndcapSuperClusters"),
    posCalc_t0_endcPresh = cms.double(3.6),
    posCalc_logweight = cms.bool(True),
    posCalc_w0 = cms.double(4.2),
    photonCollection = cms.string(''),
    pixelSeedProducer = cms.string('electronPixelSeeds'),
    risolveConversionAmbiguity = cms.bool(True),
    conversionProducer = cms.string('conversions'),
    hbheInstance = cms.string(''),
    posCalc_t0_endc = cms.double(6.3),
    barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    hbheModule = cms.string('hbhereco'),
    endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    minSCEt = cms.double(0.0),
    maxHOverE = cms.double(999.0),
    hOverEConeSize = cms.double(0.1),
    posCalc_x0 = cms.double(0.89),
    MVA_weights_location = cms.string('RecoEgamma/EgammaTools/data/TMVAnalysis_Likelihood.weights.txt'),
    posCalc_t0_barl = cms.double(7.7)
)


process.GLBMuons = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('links'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("globalCosmicMuons"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.cosmicMuons = cms.EDProducer("CosmicMuonProducer",
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        BackwardMuonTrajectoryUpdatorParameters = cms.PSet(
            MaxChi2 = cms.double(100.0),
            RescaleError = cms.bool(False),
            RescaleErrorFactor = cms.double(1.0),
            Granularity = cms.int32(2)
        ),
        MuonSmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SteppingHelixPropagatorAlong'),
            PropagatorOpposite = cms.string('SteppingHelixPropagatorOpposite')
        ),
        MuonTrajectoryUpdatorParameters = cms.PSet(
            MaxChi2 = cms.double(30000.0),
            RescaleError = cms.bool(False),
            RescaleErrorFactor = cms.double(1.0),
            Granularity = cms.int32(0)
        ),
        EnableRPCMeasurement = cms.untracked.bool(True),
        CSCRecSegmentLabel = cms.InputTag("cscSegments"),
        BuildTraversingMuon = cms.untracked.bool(False),
        EnableDTMeasurement = cms.untracked.bool(True),
        RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
        DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
        Propagator = cms.string('SteppingHelixPropagatorAny'),
        EnableCSCMeasurement = cms.untracked.bool(True),
        MuonNavigationParameters = cms.untracked.PSet(
            Barrel = cms.untracked.bool(True),
            Endcap = cms.untracked.bool(True)
        )
    ),
    MuonSeedCollectionLabel = cms.untracked.string('CosmicMuonSeed')
)


process.globalPixelSeeds = cms.EDProducer("SeedGeneratorFromRegionHitsEDProducer",
    OrderedHitsFactoryPSet = cms.PSet(
        ComponentName = cms.string('StandardHitPairGenerator'),
        SeedingLayers = cms.string('PixelLayerPairs')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            originHalfLength = cms.double(15.9),
            originZPos = cms.double(0.0),
            originYPos = cms.double(0.0),
            ptMin = cms.double(0.9),
            originXPos = cms.double(0.0),
            originRadius = cms.double(0.2)
        ),
        ComponentName = cms.string('GlobalRegionProducer')
    ),
    TTRHBuilder = cms.string('WithTrackAngle'),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    )
)


process.htMetKT4 = cms.EDProducer("METProducer",
    src = cms.InputTag("kt4CaloJets"),
    METType = cms.string('MET'),
    alias = cms.string('HTMETKT4'),
    noHF = cms.bool(False),
    globalThreshold = cms.double(5.0),
    InputType = cms.string('CaloJetCollection')
)


process.STAMuons = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("cosmicMuons"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.htMetKT6 = cms.EDProducer("METProducer",
    src = cms.InputTag("kt6CaloJets"),
    METType = cms.string('MET'),
    alias = cms.string('HTMETKT6'),
    noHF = cms.bool(False),
    globalThreshold = cms.double(5.0),
    InputType = cms.string('CaloJetCollection')
)


process.muonsNoDriftBarrelOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('inner tracks', 
        'links', 
        'outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("ctfWithMaterialTracksP5", "globalCosmicMuonsNoDriftBarrelOnly", "cosmicMuonsNoDriftBarrelOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.siStripElectrons = cms.EDProducer("SiStripElectronProducer",
    siStereoHitCollection = cms.string('stereoRecHit'),
    maxHitsOnDetId = cms.int32(4),
    minHits = cms.int32(5),
    trackCandidatesLabel = cms.string(''),
    superClusterProducer = cms.string('correctedHybridSuperClusters'),
    phiBandWidth = cms.double(0.01),
    siStripElectronsLabel = cms.string(''),
    maxNormResid = cms.double(10.0),
    siHitProducer = cms.string('siStripMatchedRecHits'),
    maxReducedChi2 = cms.double(10000.0),
    siRphiHitCollection = cms.string('rphiRecHit'),
    originUncertainty = cms.double(15.0),
    siMatchedHitCollection = cms.string('matchedRecHit'),
    superClusterCollection = cms.string('')
)


process.thWithMaterialTracks = cms.EDProducer("TrackProducer",
    src = cms.InputTag("thTrackCandidates"),
    clusterRemovalInfo = cms.InputTag("thClusters"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    Fitter = cms.string('KFFittingSmootherWithOutliersRejectionAndRK'),
    useHitsSplitting = cms.bool(False),
    alias = cms.untracked.string('ctfWithMaterialTracks'),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithAngleAndTemplate'),
    AlgorithmName = cms.string('undefAlgorithm'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.ctfWithMaterialTracksBeamHaloMuon = cms.EDProducer("TrackProducer",
    src = cms.InputTag("ckfTrackCandidatesBeamHaloMuon"),
    clusterRemovalInfo = cms.InputTag(""),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    Fitter = cms.string('KFFittingSmootherBH'),
    useHitsSplitting = cms.bool(False),
    alias = cms.untracked.string('ctfWithMaterialTracks'),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithAngleAndTemplate'),
    AlgorithmName = cms.string('beamhalo'),
    Propagator = cms.string('BeamHaloPropagatorAlong')
)


process.muonsBarrelOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('inner tracks', 
        'links', 
        'outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("ctfWithMaterialTracksP5", "globalCosmicMuonsBarrelOnly", "cosmicMuonsBarrelOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.muonsFromCosmics = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('inner tracks', 
        'links', 
        'outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("generalTracks", "globalCosmicMuons", "cosmicMuons"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.pixelMatchGsfFit = cms.EDProducer("GsfTrackProducer",
    src = cms.InputTag("egammaCkfTrackCandidates"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    producer = cms.string(''),
    Fitter = cms.string('GsfElectronFittingSmoother'),
    useHitsSplitting = cms.bool(False),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    Propagator = cms.string('fwdGsfElectronPropagator')
)


process.globalMixedSeeds = cms.EDProducer("SeedGeneratorFromRegionHitsEDProducer",
    OrderedHitsFactoryPSet = cms.PSet(
        ComponentName = cms.string('StandardHitPairGenerator'),
        SeedingLayers = cms.string('MixedLayerPairs')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            originHalfLength = cms.double(15.9),
            originZPos = cms.double(0.0),
            originYPos = cms.double(0.0),
            ptMin = cms.double(0.9),
            originXPos = cms.double(0.0),
            originRadius = cms.double(0.2)
        ),
        ComponentName = cms.string('GlobalRegionProducer')
    ),
    TTRHBuilder = cms.string('WithTrackAngle'),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    )
)


process.htMetSC5 = cms.EDProducer("METProducer",
    src = cms.InputTag("sisCone5CaloJets"),
    METType = cms.string('MET'),
    alias = cms.string('HTMETSC5'),
    noHF = cms.bool(False),
    globalThreshold = cms.double(5.0),
    InputType = cms.string('CaloJetCollection')
)


process.htMetSC7 = cms.EDProducer("METProducer",
    src = cms.InputTag("sisCone7CaloJets"),
    METType = cms.string('MET'),
    alias = cms.string('HTMETSC7'),
    noHF = cms.bool(False),
    globalThreshold = cms.double(5.0),
    InputType = cms.string('CaloJetCollection')
)


process.metOptNoHFHO = cms.EDProducer("METProducer",
    src = cms.InputTag("calotoweroptmakerWithHO"),
    METType = cms.string('CaloMET'),
    alias = cms.string('RawCaloMETOptNoHFHO'),
    noHF = cms.bool(True),
    globalThreshold = cms.double(0.0),
    InputType = cms.string('CandidateCollection')
)


process.preFilterFirstStepTracks = cms.EDProducer("TrackProducer",
    src = cms.InputTag("newTrackCandidateMaker"),
    clusterRemovalInfo = cms.InputTag(""),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    Fitter = cms.string('KFFittingSmootherWithOutliersRejectionAndRK'),
    useHitsSplitting = cms.bool(False),
    alias = cms.untracked.string('ctfWithMaterialTracks'),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithAngleAndTemplate'),
    AlgorithmName = cms.string('ctf'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.muParamGlobalIsoDepositCalEcal = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('track'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        DR_Veto_H = cms.double(0.1),
        Vertex_Constraint_Z = cms.bool(False),
        Threshold_H = cms.double(0.5),
        ComponentName = cms.string('CaloExtractor'),
        Threshold_E = cms.double(0.2),
        DR_Max = cms.double(1.0),
        DR_Veto_E = cms.double(0.07),
        Weight_E = cms.double(1.0),
        Vertex_Constraint_XY = cms.bool(False),
        DepositLabel = cms.untracked.string('EcalPlusHcal'),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        Weight_H = cms.double(0.0)
    )
)


process.cosmicMuonsEndCapsOnly = cms.EDProducer("CosmicMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        BackwardMuonTrajectoryUpdatorParameters = cms.PSet(
            MaxChi2 = cms.double(100.0),
            RescaleError = cms.bool(False),
            RescaleErrorFactor = cms.double(1.0),
            Granularity = cms.int32(2)
        ),
        MuonSmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SteppingHelixPropagatorAlong'),
            PropagatorOpposite = cms.string('SteppingHelixPropagatorOpposite')
        ),
        MuonTrajectoryUpdatorParameters = cms.PSet(
            MaxChi2 = cms.double(30000.0),
            RescaleError = cms.bool(False),
            RescaleErrorFactor = cms.double(1.0),
            Granularity = cms.int32(0)
        ),
        EnableRPCMeasurement = cms.untracked.bool(True),
        CSCRecSegmentLabel = cms.InputTag("cscSegments"),
        BuildTraversingMuon = cms.untracked.bool(False),
        EnableDTMeasurement = cms.untracked.bool(False),
        RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
        DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
        Propagator = cms.string('SteppingHelixPropagatorAny'),
        EnableCSCMeasurement = cms.untracked.bool(True),
        MuonNavigationParameters = cms.untracked.PSet(
            Barrel = cms.untracked.bool(False),
            Endcap = cms.untracked.bool(True)
        )
    ),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    MuonSeedCollectionLabel = cms.untracked.string('CosmicMuonSeedEndCapsOnly')
)


process.cosmicMuonsNoDriftBarrelOnly = cms.EDProducer("CosmicMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        BackwardMuonTrajectoryUpdatorParameters = cms.PSet(
            MaxChi2 = cms.double(100.0),
            RescaleError = cms.bool(False),
            RescaleErrorFactor = cms.double(1.0),
            Granularity = cms.int32(2)
        ),
        MuonSmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SteppingHelixPropagatorAlong'),
            PropagatorOpposite = cms.string('SteppingHelixPropagatorOpposite')
        ),
        MuonTrajectoryUpdatorParameters = cms.PSet(
            MaxChi2 = cms.double(30000.0),
            RescaleError = cms.bool(False),
            RescaleErrorFactor = cms.double(1.0),
            Granularity = cms.int32(0)
        ),
        EnableRPCMeasurement = cms.untracked.bool(True),
        CSCRecSegmentLabel = cms.InputTag("cscSegments"),
        BuildTraversingMuon = cms.untracked.bool(True),
        EnableDTMeasurement = cms.untracked.bool(True),
        RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
        DTRecSegmentLabel = cms.InputTag("dt4DSegmentsNoDrift"),
        Propagator = cms.string('SteppingHelixPropagatorAny'),
        EnableCSCMeasurement = cms.untracked.bool(False),
        MuonNavigationParameters = cms.untracked.PSet(
            Barrel = cms.untracked.bool(True),
            Endcap = cms.untracked.bool(False)
        )
    ),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    MuonSeedCollectionLabel = cms.untracked.string('CosmicMuonSeedNoDriftBarrelOnly')
)


process.conversions = cms.EDProducer("ConvertedPhotonProducer",
    scHybridBarrelProducer = cms.InputTag("cosmicSuperClusters","CosmicBarrelSuperClusters"),
    convertedPhotonCollection = cms.string(''),
    outInTrackCollection = cms.string(''),
    conversionIOTrackProducer = cms.string('ckfInOutTracksFromConversions'),
    inOutTrackCollection = cms.string(''),
    bcEndcapCollection = cms.InputTag("cosmicBasicClusters","CosmicEndcapBasicClusters"),
    bcBarrelCollection = cms.InputTag("cosmicBasicClusters","CosmicBarrelBasicClusters"),
    scIslandEndcapProducer = cms.InputTag("cosmicSuperClusters","CosmicEndcapSuperClusters"),
    outInTrackSCAssociation = cms.string('outInTrackSCAssociationCollection'),
    inOutTrackSCAssociation = cms.string('inOutTrackSCAssociationCollection'),
    conversionOITrackProducer = cms.string('ckfOutInTracksFromConversions')
)


process.dtunpacker = cms.EDProducer("DTUnpackingModule",
    useStandardFEDid = cms.untracked.bool(True),
    dataType = cms.string('DDU'),
    fedbyType = cms.untracked.bool(True),
    readOutParameters = cms.PSet(
        debug = cms.untracked.bool(False),
        rosParameters = cms.PSet(
            writeSC = cms.untracked.bool(True),
            readingDDU = cms.untracked.bool(True),
            performDataIntegrityMonitor = cms.untracked.bool(False),
            readDDUIDfromDDU = cms.untracked.bool(True),
            debug = cms.untracked.bool(False),
            localDAQ = cms.untracked.bool(False)
        ),
        performDataIntegrityMonitor = cms.untracked.bool(False),
        localDAQ = cms.untracked.bool(False)
    )
)


process.dedxMedian = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    MeVperADCStrip = cms.double(0.0009025),
    tracks = cms.InputTag("generalTracks"),
    UsePixel = cms.bool(True),
    estimator = cms.string('median'),
    trajectoryTrackAssociation = cms.InputTag("generalTracks")
)


process.dedxHarmonic2RS = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    MeVperADCStrip = cms.double(0.0009025),
    tracks = cms.InputTag("rsWithMaterialTracksP5"),
    UsePixel = cms.bool(True),
    estimator = cms.string('generic'),
    exponent = cms.double(-2.0),
    trajectoryTrackAssociation = cms.InputTag("rsWithMaterialTracksP5")
)


process.cosmicMuonsBarrelOnly = cms.EDProducer("CosmicMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        BackwardMuonTrajectoryUpdatorParameters = cms.PSet(
            MaxChi2 = cms.double(100.0),
            RescaleError = cms.bool(False),
            RescaleErrorFactor = cms.double(1.0),
            Granularity = cms.int32(2)
        ),
        MuonSmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SteppingHelixPropagatorAlong'),
            PropagatorOpposite = cms.string('SteppingHelixPropagatorOpposite')
        ),
        MuonTrajectoryUpdatorParameters = cms.PSet(
            MaxChi2 = cms.double(30000.0),
            RescaleError = cms.bool(False),
            RescaleErrorFactor = cms.double(1.0),
            Granularity = cms.int32(0)
        ),
        EnableRPCMeasurement = cms.untracked.bool(True),
        CSCRecSegmentLabel = cms.InputTag("cscSegments"),
        BuildTraversingMuon = cms.untracked.bool(False),
        EnableDTMeasurement = cms.untracked.bool(True),
        RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
        DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
        Propagator = cms.string('SteppingHelixPropagatorAny'),
        EnableCSCMeasurement = cms.untracked.bool(False),
        MuonNavigationParameters = cms.untracked.PSet(
            Barrel = cms.untracked.bool(True),
            Endcap = cms.untracked.bool(False)
        )
    ),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    MuonSeedCollectionLabel = cms.untracked.string('CosmicMuonSeedBarrelOnly')
)


process.STAMuonsBarrelOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("cosmicMuonsBarrelOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.dedxHarmonic2CTF = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    MeVperADCStrip = cms.double(0.0009025),
    tracks = cms.InputTag("ctfWithMaterialTracksP5"),
    UsePixel = cms.bool(True),
    estimator = cms.string('generic'),
    exponent = cms.double(-2.0),
    trajectoryTrackAssociation = cms.InputTag("ctfWithMaterialTracksP5")
)


process.sisCone5CaloJets = cms.EDProducer("SISConeJetProducer",
    src = cms.InputTag("towerMaker"),
    verbose = cms.untracked.bool(False),
    inputEtMin = cms.double(0.5),
    jetPtMin = cms.double(0.0),
    jetType = cms.untracked.string('CaloJet'),
    inputEMin = cms.double(0.0),
    maxPasses = cms.int32(0),
    JetPtMin = cms.double(1.0),
    coneOverlapThreshold = cms.double(0.75),
    caching = cms.bool(False),
    protojetPtMin = cms.double(0.0),
    splitMergeScale = cms.string('pttilde'),
    Active_Area_Repeats = cms.int32(0),
    UE_Subtraction = cms.string('no'),
    Ghost_EtaMax = cms.double(0.0),
    GhostArea = cms.double(1.0),
    coneRadius = cms.double(0.5),
    alias = cms.untracked.string('SISC5CaloJet')
)


process.dedxTruncated40CosmicTF = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    tracks = cms.InputTag("cosmictrackfinderP5"),
    estimator = cms.string('truncated'),
    fraction = cms.double(0.4),
    MeVperADCStrip = cms.double(0.0009025),
    UsePixel = cms.bool(True),
    trajectoryTrackAssociation = cms.InputTag("cosmictrackfinderP5")
)


process.dedxTruncated40RS = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    tracks = cms.InputTag("rsWithMaterialTracksP5"),
    estimator = cms.string('truncated'),
    fraction = cms.double(0.4),
    MeVperADCStrip = cms.double(0.0009025),
    UsePixel = cms.bool(True),
    trajectoryTrackAssociation = cms.InputTag("rsWithMaterialTracksP5")
)


process.muIsoDepositCalByAssociatorHits = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("muons"),
        MultipleDepositsFlag = cms.bool(True),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        ),
        Threshold_HO = cms.double(0.1),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.1),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.025),
        Noise_HO = cms.double(0.2)
    )
)


process.muParamGlobalIsoDepositCalByAssociatorTowers = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(True),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    )
)


process.fourthWithMaterialTracks = cms.EDProducer("TrackProducer",
    src = cms.InputTag("fourthTrackCandidates"),
    clusterRemovalInfo = cms.InputTag("fourthClusters"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    Fitter = cms.string('KFFittingSmootherWithOutliersRejectionAndRK'),
    useHitsSplitting = cms.bool(False),
    alias = cms.untracked.string('ctfWithMaterialTracks'),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithAngleAndTemplate'),
    AlgorithmName = cms.string('iter4'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.metNoHFHO = cms.EDProducer("METProducer",
    src = cms.InputTag("towerMakerWithHO"),
    METType = cms.string('CaloMET'),
    alias = cms.string('RawCaloMETNoHFHO'),
    noHF = cms.bool(True),
    globalThreshold = cms.double(0.5),
    InputType = cms.string('CandidateCollection')
)


process.STAMuonsEndCapsOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("cosmicMuonsEndCapsOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.muParamGlobalIsoDepositCtfTk = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("ctfGSWithMaterialTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    )
)


process.PhotonIDProd = cms.EDProducer("PhotonIDProducer",
    LoosePhotonHollowNTrkEB = cms.int32(999),
    LoosePhotonHollowNTrkEE = cms.int32(999),
    barrelEcalRecHitCollection = cms.string('EcalRecHitsEB'),
    EcalRecHitInnerRadius = cms.double(0.0),
    HcalRecHitCollection = cms.string(''),
    DoSolidConeTrackIsolationCut = cms.bool(False),
    LoosePhotonEtaWidthEB = cms.double(999.9),
    RequireNotElectron = cms.bool(False),
    LooseEMSolidTrkEB = cms.double(999.9),
    LooseEMHcalRecHitIsoEB = cms.double(10.0),
    LooseEMHcalRecHitIsoEE = cms.double(10.0),
    LooseEMSolidTrkEE = cms.double(999.9),
    trackProducer = cms.InputTag("generalTracks"),
    LoosePhotonEtaWidthEE = cms.double(999.9),
    DoSolidConeNTrkCut = cms.bool(False),
    TightPhotonSolidTrkEB = cms.double(999.9),
    HcalRecHitInnerRadius = cms.double(0.1),
    TightPhotonSolidTrkEE = cms.double(999.9),
    TightPhotonEcalRecHitIsoEB = cms.double(20.0),
    TightPhotonHadOverEMEE = cms.double(999.9),
    LoosePhotonSolidTrkEB = cms.double(999.9),
    GsfRecoCollection = cms.InputTag("pixelMatchGsfElectrons"),
    LoosePhotonSolidTrkEE = cms.double(999.9),
    TightPhotonHadOverEMEB = cms.double(999.9),
    TightPhotonEcalRecHitIsoEE = cms.double(20.0),
    TightPhotonHollowNTrkEB = cms.int32(999),
    TightPhotonHcalRecHitIsoEB = cms.double(10.0),
    HcalRecHitThresh = cms.double(0.0),
    barrelEcalRecHitProducer = cms.string('ecalRecHit'),
    TightPhotonHcalRecHitIsoEE = cms.double(10.0),
    DoHcalRecHitIsolationCut = cms.bool(True),
    isolationtrackThreshold = cms.double(0.0),
    HcalRecHitEtaSlice = cms.double(0.0),
    TightPhotonHollowNTrkEE = cms.int32(999),
    photonLabel = cms.string(''),
    DoHollowConeNTrkCut = cms.bool(False),
    doCutBased = cms.bool(True),
    LoosePhotonR9CutEE = cms.double(0.0),
    LoosePhotonR9CutEB = cms.double(0.0),
    RequireFiducial = cms.bool(False),
    LoosePhotonHcalRecHitIsoEB = cms.double(10.0),
    LoosePhotonHcalRecHitIsoEE = cms.double(10.0),
    LoosePhotonEcalRecHitIsoEE = cms.double(20.0),
    LoosePhotonEcalRecHitIsoEB = cms.double(20.0),
    TrackConeOuterRadius = cms.double(0.4),
    LooseEMEcalRecHitIsoEE = cms.double(20.0),
    LooseEMEcalRecHitIsoEB = cms.double(20.0),
    EcalRecHitOuterRadius = cms.double(0.4),
    LooseEMHollowNTrkEB = cms.int32(999),
    DoEcalRecHitIsolationCut = cms.bool(True),
    modulePhiBoundary = cms.double(0.0087),
    LooseEMHollowNTrkEE = cms.int32(999),
    LooseEMR9CutEE = cms.double(0.0),
    LooseEMR9CutEB = cms.double(0.0),
    LooseEMHadOverEMEE = cms.double(999.9),
    LooseEMHadOverEMEB = cms.double(999.9),
    TightPhotonSolidNTrkEE = cms.int32(999),
    TightPhotonSolidNTrkEB = cms.int32(999),
    photonIDAssociationLabel = cms.string('PhotonAssociatedID'),
    DoR9Cut = cms.bool(True),
    HcalRecHitOuterRadius = cms.double(0.4),
    moduleEtaBoundary = cms.vdouble(0.0, 0.05, 0.4, 0.5, 0.75, 
        0.85, 1.1, 1.2, 1.4, 1.6),
    TightPhotonEtaWidthEB = cms.double(999.9),
    TightPhotonEtaWidthEE = cms.double(999.9),
    EcalRecHitEtaSlice = cms.double(0.0),
    DoHollowConeTrackIsolationCut = cms.bool(True),
    LooseEMHollowTrkEE = cms.double(999.9),
    LooseEMHollowTrkEB = cms.double(999.9),
    DoHadOverEMCut = cms.bool(False),
    endcapEcalRecHitCollection = cms.string('EcalRecHitsEE'),
    HcalRecHitProducer = cms.string('hbhereco'),
    TightPhotonHollowTrkEE = cms.double(30.0),
    TightPhotonHollowTrkEB = cms.double(30.0),
    DoEtaWidthCut = cms.bool(False),
    TightPhotonR9CutEE = cms.double(0.8),
    TightPhotonR9CutEB = cms.double(0.8),
    photonProducer = cms.string('photons'),
    LooseEMSolidNTrkEE = cms.int32(999),
    LooseEMSolidNTrkEB = cms.int32(999),
    TrackConeInnerRadius = cms.double(0.04),
    LooseEMEtaWidthEB = cms.double(999.9),
    LooseEMEtaWidthEE = cms.double(999.9),
    photonIDLabel = cms.string('PhotonIDCutBasedProducer'),
    LoosePhotonHadOverEMEE = cms.double(999.9),
    LoosePhotonHadOverEMEB = cms.double(999.9),
    endcapEcalRecHitProducer = cms.string('ecalRecHit'),
    EcalRecThresh = cms.double(0.0),
    LoosePhotonHollowTrkEE = cms.double(30.0),
    LoosePhotonHollowTrkEB = cms.double(30.0),
    LoosePhotonSolidNTrkEE = cms.int32(999),
    LoosePhotonSolidNTrkEB = cms.int32(999)
)


process.rsWithMaterialTracksP5 = cms.EDProducer("TrackProducer",
    src = cms.InputTag("rsTrackCandidatesP5"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    Fitter = cms.string('RKFittingSmoother'),
    useHitsSplitting = cms.bool(False),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithAngleAndTemplate'),
    AlgorithmName = cms.string('rs'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.met = cms.EDProducer("METProducer",
    src = cms.InputTag("towerMaker"),
    METType = cms.string('CaloMET'),
    alias = cms.string('RawCaloMET'),
    noHF = cms.bool(False),
    globalThreshold = cms.double(0.5),
    InputType = cms.string('CandidateCollection')
)


process.htMet = cms.EDProducer("METProducer",
    src = cms.InputTag("midPointCone5CaloJets"),
    METType = cms.string('MET'),
    alias = cms.string('HTMET'),
    noHF = cms.bool(False),
    globalThreshold = cms.double(5.0),
    InputType = cms.string('CaloJetCollection')
)


process.hybridSuperClusters = cms.EDProducer("HybridClusterProducer",
    eThreshA = cms.double(0.003),
    basicclusterCollection = cms.string('hybridBarrelBasicClusters'),
    clustershapecollection = cms.string(''),
    ethresh = cms.double(0.1),
    ewing = cms.double(0.0),
    HybridBarrelSeedThr = cms.double(1.0),
    ecalhitcollection = cms.string('EcalRecHitsEB'),
    dynamicPhiRoad = cms.bool(False),
    posCalc_x0 = cms.double(0.89),
    posCalc_w0 = cms.double(4.2),
    step = cms.int32(17),
    eseed = cms.double(0.35),
    ecalhitproducer = cms.string('ecalRecHit'),
    posCalc_t0 = cms.double(7.4),
    debugLevel = cms.string('INFO'),
    dynamicEThresh = cms.bool(False),
    shapeAssociation = cms.string('hybridShapeAssoc'),
    superclusterCollection = cms.string(''),
    eThreshB = cms.double(0.1),
    posCalc_logweight = cms.bool(True)
)


process.cosmicMuons1LegBarrelOnly = cms.EDProducer("CosmicMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        BackwardMuonTrajectoryUpdatorParameters = cms.PSet(
            MaxChi2 = cms.double(100.0),
            RescaleError = cms.bool(False),
            RescaleErrorFactor = cms.double(1.0),
            Granularity = cms.int32(2)
        ),
        MuonSmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SteppingHelixPropagatorAlong'),
            PropagatorOpposite = cms.string('SteppingHelixPropagatorOpposite')
        ),
        MuonTrajectoryUpdatorParameters = cms.PSet(
            MaxChi2 = cms.double(30000.0),
            RescaleError = cms.bool(False),
            RescaleErrorFactor = cms.double(1.0),
            Granularity = cms.int32(0)
        ),
        EnableRPCMeasurement = cms.untracked.bool(True),
        CSCRecSegmentLabel = cms.InputTag("cscSegments"),
        BuildTraversingMuon = cms.untracked.bool(True),
        EnableDTMeasurement = cms.untracked.bool(True),
        RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
        DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
        Propagator = cms.string('SteppingHelixPropagatorAny'),
        EnableCSCMeasurement = cms.untracked.bool(False),
        MuonNavigationParameters = cms.untracked.PSet(
            Barrel = cms.untracked.bool(True),
            Endcap = cms.untracked.bool(False)
        )
    ),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    MuonSeedCollectionLabel = cms.untracked.string('CosmicMuonSeedBarrelOnly')
)


process.lhcSTAMuonsEndCapsOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("lhcStandAloneMuonsEndCapsOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.globalSeedsFromPairsWithVertices = cms.EDProducer("SeedGeneratorFromRegionHitsEDProducer",
    OrderedHitsFactoryPSet = cms.PSet(
        ComponentName = cms.string('StandardHitPairGenerator'),
        SeedingLayers = cms.string('MixedLayerPairs')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            beamSpot = cms.InputTag("offlineBeamSpot"),
            useFixedError = cms.bool(True),
            originRadius = cms.double(0.2),
            sigmaZVertex = cms.double(3.0),
            fixedError = cms.double(0.2),
            VertexCollection = cms.InputTag("pixelVertices"),
            ptMin = cms.double(0.9),
            useFoundVertices = cms.bool(True),
            nSigmaZ = cms.double(3.0)
        ),
        ComponentName = cms.string('GlobalTrackingRegionWithVerticesProducer')
    ),
    TTRHBuilder = cms.string('WithTrackAngle'),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    )
)


process.lhcSTAMuonsBarrelOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("lhcStandAloneMuonsBarrelOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.muIsoDepositJets = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("muons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    )
)


process.muIsoDepositTk = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("muons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    )
)


process.pixelMatchGsfElectrons = cms.EDProducer("GsfElectronProducer",
    endcapSuperClusters = cms.InputTag("cosmicSuperClusters","CosmicEndcapSuperClusters"),
    maxDeltaPhi = cms.double(0.1),
    minEOverPEndcaps = cms.double(0.0),
    TransientInitialStateEstimatorParameters = cms.PSet(
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    minEOverPBarrel = cms.double(0.0),
    barrelSuperClusters = cms.InputTag("cosmicSuperClusters","CosmicBarrelSuperClusters"),
    applyEtaCorrection = cms.bool(False),
    applyAmbResolution = cms.bool(True),
    tracks = cms.InputTag("pixelMatchGsfFit"),
    maxDeltaEta = cms.double(0.02),
    ElectronType = cms.string(''),
    maxEOverPBarrel = cms.double(10000.0),
    highPtPreselection = cms.bool(False),
    hcalRecHits = cms.InputTag("hbhereco"),
    highPtMin = cms.double(150.0),
    maxEOverPEndcaps = cms.double(10000.0),
    barrelClusterShapes = cms.InputTag("cosmicSuperClusters","CosmicBarrelSuperClusters"),
    endcapClusterShapes = cms.InputTag("cosmicSuperClusters","CosmicEndcapSuperClusters")
)


process.dedxMedianRS = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    MeVperADCStrip = cms.double(0.0009025),
    tracks = cms.InputTag("rsWithMaterialTracksP5"),
    UsePixel = cms.bool(True),
    estimator = cms.string('median'),
    trajectoryTrackAssociation = cms.InputTag("rsWithMaterialTracksP5")
)


process.dedxMedianCosmicTF = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    MeVperADCStrip = cms.double(0.0009025),
    tracks = cms.InputTag("cosmictrackfinderP5"),
    UsePixel = cms.bool(True),
    estimator = cms.string('median'),
    trajectoryTrackAssociation = cms.InputTag("cosmictrackfinderP5")
)


process.sisCone7CaloJets = cms.EDProducer("SISConeJetProducer",
    src = cms.InputTag("towerMaker"),
    verbose = cms.untracked.bool(False),
    inputEtMin = cms.double(0.5),
    jetPtMin = cms.double(0.0),
    jetType = cms.untracked.string('CaloJet'),
    inputEMin = cms.double(0.0),
    maxPasses = cms.int32(0),
    JetPtMin = cms.double(1.0),
    coneOverlapThreshold = cms.double(0.75),
    caching = cms.bool(False),
    protojetPtMin = cms.double(0.0),
    splitMergeScale = cms.string('pttilde'),
    Active_Area_Repeats = cms.int32(0),
    UE_Subtraction = cms.string('no'),
    Ghost_EtaMax = cms.double(0.0),
    GhostArea = cms.double(1.0),
    coneRadius = cms.double(0.7),
    alias = cms.untracked.string('SISC7CaloJet')
)


process.tevMuons = cms.EDProducer("TevMuonProducer",
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorOpposite'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(True),
        VertexConstraint = cms.bool(False)
    ),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    RefitIndex = cms.vint32(1, 2, 3),
    RefitterParameters = cms.PSet(
        Chi2ProbabilityCut = cms.double(30.0),
        Direction = cms.int32(0),
        Chi2CutCSC = cms.double(150.0),
        HitThreshold = cms.int32(1),
        MuonHitsOption = cms.int32(1),
        Chi2CutRPC = cms.double(1.0),
        Fitter = cms.string('KFFitterForRefitInsideOut'),
        RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
        TrackerRecHitBuilder = cms.string('WithTrackAngle'),
        Smoother = cms.string('KFSmootherForRefitInsideOut'),
        MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
        RefitDirection = cms.string('insideOut'),
        CSCRecSegmentLabel = cms.InputTag("cscSegments"),
        RefitRPCHits = cms.bool(True),
        Chi2CutDT = cms.double(10.0),
        PtCut = cms.double(1.0),
        DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
        Propagator = cms.string('SmartPropagatorAnyRK')
    ),
    Refits = cms.vstring('default', 
        'firstHit', 
        'picky'),
    MuonCollectionLabel = cms.InputTag("globalMuons")
)


process.dt2DSegments = cms.EDProducer("DTRecSegment2DProducer",
    Reco2DAlgoConfig = cms.PSet(
        recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
        recAlgoConfig = cms.PSet(
            debug = cms.untracked.bool(False),
            minTime = cms.double(-3.0),
            maxTime = cms.double(420.0),
            tTrigModeConfig = cms.PSet(
                vPropWire = cms.double(24.4),
                doTOFCorrection = cms.bool(False),
                tofCorrType = cms.int32(0),
                kFactor = cms.double(-1.3),
                wirePropCorrType = cms.int32(0),
                doWirePropCorrection = cms.bool(False),
                doT0Correction = cms.bool(True),
                debug = cms.untracked.bool(False)
            ),
            tTrigMode = cms.string('DTTTrigSyncFromDB')
        ),
        T0SegCorrectionDebug = cms.untracked.bool(False),
        segmCleanerMode = cms.int32(1),
        nSharedHitsMax = cms.int32(2),
        AlphaMaxPhi = cms.double(100.0),
        hit_afterT0_resolution = cms.double(0.03),
        MaxAllowedHits = cms.uint32(50),
        performT0_vdriftSegCorrection = cms.bool(False),
        AlphaMaxTheta = cms.double(100.0),
        debug = cms.untracked.bool(False),
        nUnSharedHitsMin = cms.int32(2),
        performT0SegCorrection = cms.bool(False)
    ),
    Reco2DAlgoName = cms.string('DTCombinatorialPatternReco'),
    debug = cms.untracked.bool(False),
    recHits1DLabel = cms.InputTag("dt1DRecHits")
)


process.electronPixelSeeds = cms.EDProducer("ElectronPixelSeedProducer",
    endcapSuperClusters = cms.InputTag("cosmicSuperClusters","CosmicEndcapSuperClusters"),
    SeedConfiguration = cms.PSet(
        searchInTIDTEC = cms.bool(True),
        HighPtThreshold = cms.double(35.0),
        r2MinF = cms.double(-0.15),
        DeltaPhi1Low = cms.double(0.23),
        DeltaPhi1High = cms.double(0.08),
        ePhiMin1 = cms.double(-0.125),
        PhiMin2 = cms.double(-0.002),
        LowPtThreshold = cms.double(5.0),
        maxHOverE = cms.double(0.1),
        dynamicPhiRoad = cms.bool(True),
        ePhiMax1 = cms.double(0.075),
        DeltaPhi2 = cms.double(0.004),
        SizeWindowENeg = cms.double(0.675),
        rMaxI = cms.double(0.2),
        PhiMax2 = cms.double(0.002),
        preFilteredSeeds = cms.bool(False),
        r2MaxF = cms.double(0.15),
        pPhiMin1 = cms.double(-0.075),
        initialSeeds = cms.InputTag("newCombinedSeeds"),
        pPhiMax1 = cms.double(0.125),
        SCEtCut = cms.double(4.0),
        z2MaxB = cms.double(0.09),
        fromTrackerSeeds = cms.bool(False),
        hcalRecHits = cms.InputTag("hbhereco"),
        z2MinB = cms.double(-0.09),
        rMinI = cms.double(-0.2),
        OrderedHitsFactoryPSet = cms.PSet(
            ComponentName = cms.string('StandardHitPairGenerator'),
            SeedingLayers = cms.string('MixedLayerPairs')
        ),
        TTRHBuilder = cms.string('WithTrackAngle'),
        RegionPSet = cms.PSet(
            deltaPhiRegion = cms.double(0.7),
            originHalfLength = cms.double(15.0),
            useZInVertex = cms.bool(True),
            deltaEtaRegion = cms.double(0.3),
            ptMin = cms.double(1.5),
            originRadius = cms.double(0.2),
            VertexProducer = cms.InputTag("pixelVertices")
        )
    ),
    barrelSuperClusters = cms.InputTag("cosmicSuperClusters","CosmicBarrelSuperClusters")
)


process.kt4CaloJets = cms.EDProducer("KtJetProducer",
    Active_Area_Repeats = cms.int32(0),
    UE_Subtraction = cms.string('no'),
    Ghost_EtaMax = cms.double(0.0),
    GhostArea = cms.double(1.0),
    Strategy = cms.string('Best'),
    src = cms.InputTag("towerMaker"),
    verbose = cms.untracked.bool(False),
    inputEtMin = cms.double(0.5),
    jetPtMin = cms.double(0.0),
    jetType = cms.untracked.string('CaloJet'),
    inputEMin = cms.double(0.0),
    FJ_ktRParam = cms.double(0.4),
    alias = cms.untracked.string('KT4CaloJet'),
    JetPtMin = cms.double(1.0)
)


process.rpcRecHits = cms.EDProducer("RPCRecHitProducer",
    recAlgoConfig = cms.PSet(

    ),
    recAlgo = cms.string('RPCRecHitStandardAlgo'),
    rpcDigiLabel = cms.InputTag("muonRPCDigis")
)


process.muonsBeamHaloEndCapsOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('inner tracks', 
        'links', 
        'outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("ctfWithMaterialTracksBeamHaloMuon", "globalBeamHaloMuonEndCapslOnly", "cosmicMuonsEndCapsOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.dt4DSegmentsNoDrift = cms.EDProducer("DTRecSegment4DProducer",
    debug = cms.untracked.bool(False),
    Reco4DAlgoName = cms.string('DTCombinatorialPatternReco4D'),
    recHits2DLabel = cms.InputTag("dt2DSegments"),
    recHits1DLabel = cms.InputTag("dt1DRecHits"),
    Reco4DAlgoConfig = cms.PSet(
        recAlgo = cms.string('DTNoDriftAlgo'),
        recAlgoConfig = cms.PSet(
            fixedDrift = cms.double(1.0),
            tTrigMode = cms.string('DTTTrigSyncFromDB'),
            minTime = cms.double(1000.0),
            hitResolution = cms.double(1.0),
            debug = cms.untracked.bool(False),
            maxTime = cms.double(3500.0),
            tTrigModeConfig = cms.PSet(
                vPropWire = cms.double(24.4),
                doTOFCorrection = cms.bool(False),
                tofCorrType = cms.int32(0),
                kFactor = cms.double(-1.3),
                wirePropCorrType = cms.int32(0),
                doWirePropCorrection = cms.bool(False),
                doT0Correction = cms.bool(False),
                debug = cms.untracked.bool(False)
            )
        ),
        Reco2DAlgoConfig = cms.PSet(
            recAlgo = cms.string('DTNoDriftAlgo'),
            recAlgoConfig = cms.PSet(
                fixedDrift = cms.double(1.0),
                tTrigMode = cms.string('DTTTrigSyncFromDB'),
                minTime = cms.double(1000.0),
                hitResolution = cms.double(1.0),
                debug = cms.untracked.bool(False),
                maxTime = cms.double(3500.0),
                tTrigModeConfig = cms.PSet(
                    vPropWire = cms.double(24.4),
                    doTOFCorrection = cms.bool(False),
                    tofCorrType = cms.int32(0),
                    kFactor = cms.double(-1.3),
                    wirePropCorrType = cms.int32(0),
                    doWirePropCorrection = cms.bool(False),
                    doT0Correction = cms.bool(False),
                    debug = cms.untracked.bool(False)
                )
            ),
            T0SegCorrectionDebug = cms.untracked.bool(False),
            segmCleanerMode = cms.int32(1),
            nSharedHitsMax = cms.int32(2),
            AlphaMaxPhi = cms.double(100.0),
            hit_afterT0_resolution = cms.double(0.03),
            MaxAllowedHits = cms.uint32(50),
            performT0_vdriftSegCorrection = cms.bool(False),
            AlphaMaxTheta = cms.double(100.0),
            debug = cms.untracked.bool(False),
            nUnSharedHitsMin = cms.int32(2),
            performT0SegCorrection = cms.bool(False)
        ),
        Reco2DAlgoName = cms.string('DTCombinatorialPatternReco'),
        T0SegCorrectionDebug = cms.untracked.bool(False),
        segmCleanerMode = cms.int32(1),
        nSharedHitsMax = cms.int32(2),
        hit_afterT0_resolution = cms.double(0.03),
        performT0_vdriftSegCorrection = cms.bool(False),
        debug = cms.untracked.bool(False),
        nUnSharedHitsMin = cms.int32(2),
        AllDTRecHits = cms.bool(True),
        performT0SegCorrection = cms.bool(False)
    )
)


process.globalMuons = cms.EDProducer("GlobalMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorOpposite'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(True),
        VertexConstraint = cms.bool(False)
    ),
    GLBTrajBuilderParameters = cms.PSet(
        Chi2ProbabilityCut = cms.double(30.0),
        Direction = cms.int32(0),
        Chi2CutCSC = cms.double(150.0),
        HitThreshold = cms.int32(1),
        MuonHitsOption = cms.int32(1),
        Chi2CutRPC = cms.double(1.0),
        RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
        TrackRecHitBuilder = cms.string('WithTrackAngle'),
        CSCRecSegmentLabel = cms.InputTag("cscSegments"),
        MuonTrackingRegionBuilder = cms.PSet(
            EtaR_UpperLimit_Par1 = cms.double(0.25),
            Eta_fixed = cms.double(0.2),
            OnDemand = cms.double(-1.0),
            Rescale_Dz = cms.double(3.0),
            Eta_min = cms.double(0.1),
            Rescale_phi = cms.double(3.0),
            EtaR_UpperLimit_Par2 = cms.double(0.15),
            DeltaZ_Region = cms.double(15.9),
            Rescale_eta = cms.double(3.0),
            PhiR_UpperLimit_Par2 = cms.double(0.2),
            vertexCollection = cms.InputTag("pixelVertices"),
            Phi_fixed = cms.double(0.2),
            DeltaR = cms.double(0.2),
            EscapePt = cms.double(1.5),
            UseFixedRegion = cms.bool(False),
            PhiR_UpperLimit_Par1 = cms.double(0.6),
            Phi_min = cms.double(0.1),
            UseVertex = cms.bool(False),
            beamSpot = cms.InputTag("offlineBeamSpot")
        ),
        Chi2CutDT = cms.double(10.0),
        TrackTransformer = cms.PSet(
            Fitter = cms.string('KFFitterForRefitInsideOut'),
            TrackerRecHitBuilder = cms.string('WithTrackAngle'),
            Smoother = cms.string('KFSmootherForRefitInsideOut'),
            MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
            RefitDirection = cms.string('insideOut'),
            RefitRPCHits = cms.bool(True)
        ),
        GlobalMuonTrackMatcher = cms.PSet(
            MinP = cms.double(2.5),
            DeltaDCut = cms.double(10.0),
            DeltaRCut = cms.double(0.2),
            Chi2Cut = cms.double(50.0),
            MinPt = cms.double(1.0)
        ),
        PtCut = cms.double(1.0),
        TrackerPropagator = cms.string('SteppingHelixPropagatorAny'),
        DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
        TransformerOutPropagator = cms.string('SmartPropagatorAnyRK'),
        MatcherOutPropagator = cms.string('SmartPropagatorRK'),
        KFFitter = cms.string('GlbMuKFFitter')
    ),
    TrackerCollectionLabel = cms.InputTag("generalTracks"),
    MuonCollectionLabel = cms.InputTag("standAloneMuons","UpdatedAtVtx")
)


process.lhcStandAloneMuonsEndCapsOnly = cms.EDProducer("StandAloneMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    InputObjects = cms.InputTag("lhcMuonSeedEndCapsOnly"),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorOpposite'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(True)
    ),
    STATrajBuilderParameters = cms.PSet(
        DoRefit = cms.bool(False),
        FilterParameters = cms.PSet(
            NumberOfSigma = cms.double(3.0),
            FitDirection = cms.string('insideOut'),
            DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
            MaxChi2 = cms.double(1000.0),
            MuonTrajectoryUpdatorParameters = cms.PSet(
                MaxChi2 = cms.double(1000.0),
                RescaleError = cms.bool(False),
                RescaleErrorFactor = cms.double(100.0),
                Granularity = cms.int32(0)
            ),
            EnableRPCMeasurement = cms.bool(True),
            CSCRecSegmentLabel = cms.InputTag("cscSegments"),
            EnableDTMeasurement = cms.bool(True),
            RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            EnableCSCMeasurement = cms.bool(True)
        ),
        SeedPropagator = cms.string('SteppingHelixPropagatorAny'),
        NavigationType = cms.string('Standard'),
        DoBackwardFilter = cms.bool(True),
        SeedPosition = cms.string('in'),
        BWFilterParameters = cms.PSet(
            NumberOfSigma = cms.double(3.0),
            BWSeedType = cms.string('fromGenerator'),
            FitDirection = cms.string('outsideIn'),
            DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
            MaxChi2 = cms.double(100.0),
            MuonTrajectoryUpdatorParameters = cms.PSet(
                MaxChi2 = cms.double(100.0),
                RescaleError = cms.bool(False),
                RescaleErrorFactor = cms.double(100.0),
                Granularity = cms.int32(2)
            ),
            EnableRPCMeasurement = cms.bool(True),
            CSCRecSegmentLabel = cms.InputTag("cscSegments"),
            EnableDTMeasurement = cms.bool(False),
            RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            EnableCSCMeasurement = cms.bool(True)
        ),
        RefitterParameters = cms.PSet(
            FitterName = cms.string('KFFitterSmootherSTA'),
            Option = cms.int32(1)
        )
    )
)


process.muons = cms.EDProducer("MuonIdProducer",
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillEnergy = cms.bool(True),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    inputCollectionTypes = cms.vstring('inner tracks', 
        'links', 
        'outer tracks'),
    inputCollectionLabels = cms.VInputTag("ctfWithMaterialTracksP5", "globalCosmicMuons", "cosmicMuons"),
    fillCaloCompatibility = cms.bool(True),
    maxAbsEta = cms.double(3.0),
    debugWithTruthMatching = cms.bool(False),
    minP = cms.double(3.0),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    fillIsolation = cms.bool(False),
    minNumberOfMatches = cms.int32(1),
    fillMatching = cms.bool(True)
)


process.dedxTruncated40 = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    tracks = cms.InputTag("generalTracks"),
    estimator = cms.string('truncated'),
    fraction = cms.double(0.4),
    MeVperADCStrip = cms.double(0.0009025),
    UsePixel = cms.bool(True),
    trajectoryTrackAssociation = cms.InputTag("generalTracks")
)


process.ecalRecHit = cms.EDProducer("EcalRecHitProducer",
    EEuncalibRecHitCollection = cms.InputTag("ecalFixedAlphaBetaFitUncalibRecHit","EcalUncalibRecHitsEE"),
    ChannelStatusToBeExcluded = cms.vint32(1),
    EBuncalibRecHitCollection = cms.InputTag("ecalFixedAlphaBetaFitUncalibRecHit","EcalUncalibRecHitsEB"),
    EBrechitCollection = cms.string('EcalRecHitsEB'),
    EErechitCollection = cms.string('EcalRecHitsEE')
)


process.globalCosmicMuons = cms.EDProducer("GlobalCosmicMuonProducer",
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
        TrackerRecHitBuilder = cms.string('WithTrackAngle'),
        TkTrackCollectionLabel = cms.string('ctfWithMaterialTracksP5'),
        SmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SmartPropagatorAny'),
            PropagatorOpposite = cms.string('SmartPropagatorAnyOpposite')
        ),
        Propagator = cms.string('SteppingHelixPropagatorAny')
    ),
    MuonCollectionLabel = cms.InputTag("cosmicMuons")
)


process.kt6CaloJets = cms.EDProducer("KtJetProducer",
    Active_Area_Repeats = cms.int32(0),
    UE_Subtraction = cms.string('no'),
    Ghost_EtaMax = cms.double(0.0),
    GhostArea = cms.double(1.0),
    Strategy = cms.string('Best'),
    src = cms.InputTag("towerMaker"),
    verbose = cms.untracked.bool(False),
    inputEtMin = cms.double(0.5),
    jetPtMin = cms.double(0.0),
    jetType = cms.untracked.string('CaloJet'),
    inputEMin = cms.double(0.0),
    FJ_ktRParam = cms.double(0.6),
    alias = cms.untracked.string('KT6CaloJet'),
    JetPtMin = cms.double(1.0)
)


process.egammaCTFFinalFitWithMaterial = cms.EDProducer("TrackProducer",
    src = cms.InputTag("siStripElectrons"),
    clusterRemovalInfo = cms.InputTag(""),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    Fitter = cms.string('KFFittingSmoother'),
    useHitsSplitting = cms.bool(False),
    alias = cms.untracked.string('egammaCTFWithMaterialTracks'),
    TrajectoryInEvent = cms.bool(False),
    TTRHBuilder = cms.string('WithTrackAngle'),
    AlgorithmName = cms.string('undefAlgorithm'),
    Propagator = cms.string('PropagatorWithMaterial')
)


process.iterativeCone5CaloJets = cms.EDProducer("IterativeConeJetProducer",
    src = cms.InputTag("towerMaker"),
    verbose = cms.untracked.bool(False),
    inputEtMin = cms.double(0.5),
    jetPtMin = cms.double(0.0),
    jetType = cms.untracked.string('CaloJet'),
    inputEMin = cms.double(0.0),
    seedThreshold = cms.double(1.0),
    debugLevel = cms.untracked.int32(0),
    coneRadius = cms.double(0.5),
    alias = cms.untracked.string('IC5CaloJet')
)


process.GsfGlobalElectronTest = cms.EDProducer("GsfTrackProducer",
    src = cms.InputTag("CkfElectronCandidates"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    producer = cms.string(''),
    Fitter = cms.string('GsfElectronFittingSmoother'),
    useHitsSplitting = cms.bool(False),
    TrajectoryInEvent = cms.bool(False),
    TTRHBuilder = cms.string('WithTrackAngle'),
    Propagator = cms.string('fwdElectronPropagator')
)


process.ctfWithMaterialTracks = cms.EDProducer("TrackProducer",
    src = cms.InputTag("ckfTrackCandidates"),
    clusterRemovalInfo = cms.InputTag(""),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    Fitter = cms.string('KFFittingSmootherWithOutliersRejectionAndRK'),
    useHitsSplitting = cms.bool(False),
    alias = cms.untracked.string('ctfWithMaterialTracks'),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithAngleAndTemplate'),
    AlgorithmName = cms.string('undefAlgorithm'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.globalCosmicMuonsEndCapsOnly = cms.EDProducer("GlobalCosmicMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
        TrackerRecHitBuilder = cms.string('WithTrackAngle'),
        TkTrackCollectionLabel = cms.string('ctfWithMaterialTracksP5'),
        SmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SmartPropagatorAny'),
            PropagatorOpposite = cms.string('SmartPropagatorAnyOpposite')
        ),
        Propagator = cms.string('SteppingHelixPropagatorAny')
    ),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    MuonCollectionLabel = cms.InputTag("cosmicMuonsEndCapsOnly")
)


process.globalBeamHaloMuonEndCapslOnly = cms.EDProducer("GlobalCosmicMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
        TrackerRecHitBuilder = cms.string('WithTrackAngle'),
        TkTrackCollectionLabel = cms.string('ctfWithMaterialTracksBeamHaloMuon'),
        SmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SmartPropagatorAny'),
            PropagatorOpposite = cms.string('SmartPropagatorAnyOpposite')
        ),
        Propagator = cms.string('SteppingHelixPropagatorAny')
    ),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    MuonCollectionLabel = cms.InputTag("cosmicMuonsEndCapsOnly")
)


process.muons1LegBarrelOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('inner tracks', 
        'links', 
        'outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("ctfWithMaterialTracksP5", "globalCosmicMuons1LegBarrelOnly", "cosmicMuons1LegBarrelOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.fourthPLSeeds = cms.EDProducer("SeedGeneratorFromRegionHitsEDProducer",
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            originHalfLength = cms.double(25.0),
            originZPos = cms.double(0.0),
            originYPos = cms.double(0.0),
            ptMin = cms.double(0.9),
            originXPos = cms.double(0.0),
            originRadius = cms.double(1.0)
        ),
        ComponentName = cms.string('GlobalRegionProducer')
    ),
    TTRHBuilder = cms.string('WithTrackAngle'),
    OrderedHitsFactoryPSet = cms.PSet(
        ComponentName = cms.string('StandardHitPairGenerator'),
        SeedingLayers = cms.string('FourthLayerPairs')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    )
)


process.GLBMuonsNoDriftBarrelOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('links'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("globalCosmicMuonsNoDriftBarrelOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.metOpt = cms.EDProducer("METProducer",
    src = cms.InputTag("calotoweroptmaker"),
    METType = cms.string('CaloMET'),
    alias = cms.string('RawCaloMETOpt'),
    noHF = cms.bool(False),
    globalThreshold = cms.double(0.0),
    InputType = cms.string('CandidateCollection')
)


process.dt1DRecHitsNoDrift = cms.EDProducer("DTRecHitProducer",
    debug = cms.untracked.bool(False),
    recAlgoConfig = cms.PSet(
        fixedDrift = cms.double(1.0),
        tTrigMode = cms.string('DTTTrigSyncFromDB'),
        minTime = cms.double(1000.0),
        hitResolution = cms.double(1.0),
        debug = cms.untracked.bool(False),
        maxTime = cms.double(3500.0),
        tTrigModeConfig = cms.PSet(
            vPropWire = cms.double(24.4),
            doTOFCorrection = cms.bool(False),
            tofCorrType = cms.int32(0),
            kFactor = cms.double(-1.3),
            wirePropCorrType = cms.int32(0),
            doWirePropCorrection = cms.bool(False),
            doT0Correction = cms.bool(False),
            debug = cms.untracked.bool(False)
        )
    ),
    dtDigiLabel = cms.InputTag("muonDTDigis"),
    recAlgo = cms.string('DTNoDriftAlgo')
)


process.globalCosmicMuonsBarrelOnly = cms.EDProducer("GlobalCosmicMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
        TrackerRecHitBuilder = cms.string('WithTrackAngle'),
        TkTrackCollectionLabel = cms.string('ctfWithMaterialTracksP5'),
        SmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SmartPropagatorAny'),
            PropagatorOpposite = cms.string('SmartPropagatorAnyOpposite')
        ),
        Propagator = cms.string('SteppingHelixPropagatorAny')
    ),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    MuonCollectionLabel = cms.InputTag("cosmicMuonsBarrelOnly")
)


process.GLBMuonsEndCapsOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('links'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("globalCosmicMuonsEndCapsOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.metOptHO = cms.EDProducer("METProducer",
    src = cms.InputTag("calotoweroptmakerWithHO"),
    METType = cms.string('CaloMET'),
    alias = cms.string('RawCaloMETOptHO'),
    noHF = cms.bool(False),
    globalThreshold = cms.double(0.0),
    InputType = cms.string('CandidateCollection')
)


process.simpleCosmicBONSeeds = cms.EDProducer("SimpleCosmicBONSeeder",
    helixDebugLevel = cms.untracked.uint32(0),
    RegionPSet = cms.PSet(
        originRadius = cms.double(150.0),
        ptMin = cms.double(0.1),
        originZPosition = cms.double(0.0),
        originHalfLength = cms.double(90.0)
    ),
    ClusterCheckPSet = cms.PSet(
        MaxNumberOfCosmicClusters = cms.uint32(300),
        ClusterCollectionLabel = cms.InputTag("siStripClusters"),
        doClusterCheck = cms.bool(True)
    ),
    seedOnMiddle = cms.bool(False),
    maxTriplets = cms.int32(50000),
    TripletsPSet = cms.PSet(
        TOB5 = cms.PSet(
            TTRHBuilder = cms.string('WithTrackAngle'),
            rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
        ),
        TOB4 = cms.PSet(
            TTRHBuilder = cms.string('WithTrackAngle'),
            rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
        ),
        TIB1 = cms.PSet(
            matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
            TTRHBuilder = cms.string('WithTrackAngle')
        ),
        TOB6 = cms.PSet(
            TTRHBuilder = cms.string('WithTrackAngle'),
            rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
        ),
        TOB1 = cms.PSet(
            matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
            TTRHBuilder = cms.string('WithTrackAngle')
        ),
        TOB3 = cms.PSet(
            TTRHBuilder = cms.string('WithTrackAngle'),
            rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
        ),
        TOB2 = cms.PSet(
            matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
            TTRHBuilder = cms.string('WithTrackAngle')
        ),
        TEC = cms.PSet(
            useSimpleRphiHitsCleaner = cms.untracked.bool(False),
            minRing = cms.int32(5),
            matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
            useRingSlector = cms.untracked.bool(False),
            TTRHBuilder = cms.string('WithTrackAngle'),
            rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
            maxRing = cms.int32(7)
        ),
        TIB2 = cms.PSet(
            matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
            TTRHBuilder = cms.string('WithTrackAngle')
        ),
        TIB3 = cms.PSet(
            TTRHBuilder = cms.string('WithTrackAngle'),
            rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
        ),
        layerList = cms.vstring('TOB4+TOB5+TOB6', 
            'TOB3+TOB5+TOB6', 
            'TOB3+TOB4+TOB5', 
            'TOB3+TOB4+TOB6', 
            'TOB2+TOB4+TOB5', 
            'TOB2+TOB3+TOB5', 
            'TEC7_pos+TEC8_pos+TEC9_pos', 
            'TEC6_pos+TEC7_pos+TEC8_pos', 
            'TEC5_pos+TEC6_pos+TEC7_pos', 
            'TEC4_pos+TEC5_pos+TEC6_pos', 
            'TEC3_pos+TEC4_pos+TEC5_pos', 
            'TEC2_pos+TEC3_pos+TEC4_pos', 
            'TEC1_pos+TEC2_pos+TEC3_pos', 
            'TEC7_neg+TEC8_neg+TEC9_neg', 
            'TEC6_neg+TEC7_neg+TEC8_neg', 
            'TEC5_neg+TEC6_neg+TEC7_neg', 
            'TEC4_neg+TEC5_neg+TEC6_neg', 
            'TEC3_neg+TEC4_neg+TEC5_neg', 
            'TEC2_neg+TEC3_neg+TEC4_neg', 
            'TEC1_neg+TEC2_neg+TEC3_neg', 
            'TEC6_pos+TEC8_pos+TEC9_pos', 
            'TEC5_pos+TEC7_pos+TEC8_pos', 
            'TEC4_pos+TEC6_pos+TEC7_pos', 
            'TEC3_pos+TEC5_pos+TEC6_pos', 
            'TEC2_pos+TEC4_pos+TEC5_pos', 
            'TEC1_pos+TEC3_pos+TEC4_pos', 
            'TEC6_pos+TEC7_pos+TEC9_pos', 
            'TEC5_pos+TEC6_pos+TEC8_pos', 
            'TEC4_pos+TEC5_pos+TEC7_pos', 
            'TEC3_pos+TEC4_pos+TEC6_pos', 
            'TEC2_pos+TEC3_pos+TEC5_pos', 
            'TEC1_pos+TEC2_pos+TEC4_pos', 
            'TEC6_neg+TEC8_neg+TEC9_neg', 
            'TEC5_neg+TEC7_neg+TEC8_neg', 
            'TEC4_neg+TEC6_neg+TEC7_neg', 
            'TEC3_neg+TEC5_neg+TEC6_neg', 
            'TEC2_neg+TEC4_neg+TEC5_neg', 
            'TEC1_neg+TEC3_neg+TEC4_neg', 
            'TEC6_neg+TEC7_neg+TEC9_neg', 
            'TEC5_neg+TEC6_neg+TEC8_neg', 
            'TEC4_neg+TEC5_neg+TEC7_neg', 
            'TEC3_neg+TEC4_neg+TEC6_neg', 
            'TEC2_neg+TEC3_neg+TEC5_neg', 
            'TEC1_neg+TEC2_neg+TEC4_neg', 
            'TOB6+TEC1_pos+TEC2_pos', 
            'TOB6+TEC1_neg+TEC2_neg', 
            'TOB6+TOB5+TEC1_pos', 
            'TOB6+TOB5+TEC1_neg'),
        debugLevel = cms.untracked.uint32(0)
    ),
    seedDebugLevel = cms.untracked.uint32(0),
    TTRHBuilder = cms.string('WithTrackAngle'),
    writeTriplets = cms.bool(False),
    maxSeeds = cms.int32(10000),
    rescaleError = cms.double(50)
)


process.dt1DRecHits = cms.EDProducer("DTRecHitProducer",
    recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
    recAlgoConfig = cms.PSet(
        debug = cms.untracked.bool(False),
        minTime = cms.double(-3.0),
        maxTime = cms.double(420.0),
        tTrigModeConfig = cms.PSet(
            vPropWire = cms.double(24.4),
            doTOFCorrection = cms.bool(False),
            tofCorrType = cms.int32(0),
            kFactor = cms.double(-1.3),
            wirePropCorrType = cms.int32(0),
            doWirePropCorrection = cms.bool(False),
            doT0Correction = cms.bool(True),
            debug = cms.untracked.bool(False)
        ),
        tTrigMode = cms.string('DTTTrigSyncFromDB')
    ),
    debug = cms.untracked.bool(False),
    dtDigiLabel = cms.InputTag("dtunpacker")
)


process.muParamGlobalIsoDepositTk = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('track'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    )
)


process.calomuons = cms.EDProducer("CaloMuonProducer",
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputMuons = cms.InputTag("muons"),
    inputTracks = cms.InputTag("generalTracks"),
    minCaloCompatibility = cms.double(0.6)
)


process.metNoHF = cms.EDProducer("METProducer",
    src = cms.InputTag("towerMaker"),
    METType = cms.string('CaloMET'),
    alias = cms.string('RawCaloMETNoHF'),
    noHF = cms.bool(True),
    globalThreshold = cms.double(0.5),
    InputType = cms.string('CandidateCollection')
)


process.newSeedFromPairs = cms.EDProducer("SeedGeneratorFromRegionHitsEDProducer",
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            beamSpot = cms.InputTag("offlineBeamSpot"),
            useFixedError = cms.bool(True),
            originRadius = cms.double(0.2),
            sigmaZVertex = cms.double(3.0),
            fixedError = cms.double(0.2),
            VertexCollection = cms.InputTag("pixelVertices"),
            ptMin = cms.double(0.9),
            useFoundVertices = cms.bool(True),
            nSigmaZ = cms.double(3.0)
        ),
        ComponentName = cms.string('GlobalTrackingRegionWithVerticesProducer')
    ),
    TTRHBuilder = cms.string('WithTrackAngle'),
    OrderedHitsFactoryPSet = cms.PSet(
        ComponentName = cms.string('StandardHitPairGenerator'),
        SeedingLayers = cms.string('MixedLayerPairs')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    )
)


process.rsWithMaterialTracks = cms.EDProducer("TrackProducer",
    src = cms.InputTag("rsTrackCandidates"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    Fitter = cms.string('RKFittingSmoother'),
    useHitsSplitting = cms.bool(False),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithAngleAndTemplate'),
    AlgorithmName = cms.string('rs'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.dt4DSegments = cms.EDProducer("DTRecSegment4DProducer",
    Reco4DAlgoName = cms.string('DTCombinatorialPatternReco4D'),
    Reco4DAlgoConfig = cms.PSet(
        Reco2DAlgoConfig = cms.PSet(
            recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
            recAlgoConfig = cms.PSet(
                debug = cms.untracked.bool(False),
                minTime = cms.double(-3.0),
                maxTime = cms.double(420.0),
                tTrigModeConfig = cms.PSet(
                    vPropWire = cms.double(24.4),
                    doTOFCorrection = cms.bool(False),
                    tofCorrType = cms.int32(0),
                    kFactor = cms.double(-1.3),
                    wirePropCorrType = cms.int32(0),
                    doWirePropCorrection = cms.bool(False),
                    doT0Correction = cms.bool(True),
                    debug = cms.untracked.bool(False)
                ),
                tTrigMode = cms.string('DTTTrigSyncFromDB')
            ),
            T0SegCorrectionDebug = cms.untracked.bool(False),
            segmCleanerMode = cms.int32(1),
            nSharedHitsMax = cms.int32(2),
            AlphaMaxPhi = cms.double(100.0),
            hit_afterT0_resolution = cms.double(0.03),
            MaxAllowedHits = cms.uint32(50),
            performT0_vdriftSegCorrection = cms.bool(False),
            AlphaMaxTheta = cms.double(100.0),
            debug = cms.untracked.bool(False),
            nUnSharedHitsMin = cms.int32(2),
            performT0SegCorrection = cms.bool(False)
        ),
        Reco2DAlgoName = cms.string('DTCombinatorialPatternReco'),
        recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
        recAlgoConfig = cms.PSet(
            debug = cms.untracked.bool(False),
            minTime = cms.double(-3.0),
            maxTime = cms.double(420.0),
            tTrigModeConfig = cms.PSet(
                vPropWire = cms.double(24.4),
                doTOFCorrection = cms.bool(False),
                tofCorrType = cms.int32(0),
                kFactor = cms.double(-1.3),
                wirePropCorrType = cms.int32(0),
                doWirePropCorrection = cms.bool(False),
                doT0Correction = cms.bool(True),
                debug = cms.untracked.bool(False)
            ),
            tTrigMode = cms.string('DTTTrigSyncFromDB')
        ),
        T0SegCorrectionDebug = cms.untracked.bool(False),
        segmCleanerMode = cms.int32(1),
        nSharedHitsMax = cms.int32(2),
        hit_afterT0_resolution = cms.double(0.03),
        performT0_vdriftSegCorrection = cms.bool(False),
        debug = cms.untracked.bool(False),
        nUnSharedHitsMin = cms.int32(2),
        AllDTRecHits = cms.bool(True),
        performT0SegCorrection = cms.bool(False)
    ),
    debug = cms.untracked.bool(False),
    recHits1DLabel = cms.InputTag("dt1DRecHits"),
    recHits2DLabel = cms.InputTag("dt2DSegments")
)


process.GLBMuonsBarrelOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('links'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("globalCosmicMuonsBarrelOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.metHO = cms.EDProducer("METProducer",
    src = cms.InputTag("towerMakerWithHO"),
    METType = cms.string('CaloMET'),
    alias = cms.string('RawCaloMETHO'),
    noHF = cms.bool(False),
    globalThreshold = cms.double(0.5),
    InputType = cms.string('CandidateCollection')
)


process.ecalPreshowerRecHit = cms.EDProducer("ESRecHitProducer",
    ESrechitCollection = cms.string('EcalRecHitsES'),
    ESdigiCollection = cms.InputTag("ecalPreshowerDigis")
)


process.STAMuons1LegBarrelOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('outer tracks'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("cosmicMuons1LegBarrelOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.iterativeCone15CaloJets = cms.EDProducer("IterativeConeJetProducer",
    src = cms.InputTag("towerMaker"),
    verbose = cms.untracked.bool(False),
    inputEtMin = cms.double(0.5),
    jetPtMin = cms.double(0.0),
    jetType = cms.untracked.string('CaloJet'),
    inputEMin = cms.double(0.0),
    coneRadius = cms.double(0.15),
    alias = cms.untracked.string('IC15CaloJet'),
    seedThreshold = cms.double(0.5),
    debugLevel = cms.untracked.int32(0)
)


process.GLBMuons1LegBarrelOnly = cms.EDProducer("MuonIdProducer",
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    maxAbsEta = cms.double(3.0),
    trackPtThresholdToFillCandidateP4WithGlobalFit = cms.double(0.0),
    addExtraSoftMuons = cms.bool(False),
    debugWithTruthMatching = cms.bool(False),
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    fillEnergy = cms.bool(True),
    inputCollectionTypes = cms.vstring('links'),
    fillCaloCompatibility = cms.bool(True),
    minP = cms.double(3.0),
    fillIsolation = cms.bool(False),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minPt = cms.double(1.5),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    ),
    fillMatching = cms.bool(True),
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    ),
    inputCollectionLabels = cms.VInputTag("globalCosmicMuons1LegBarrelOnly"),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    minNumberOfMatches = cms.int32(1)
)


process.newSeedFromTriplets = cms.EDProducer("SeedGeneratorFromRegionHitsEDProducer",
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            originHalfLength = cms.double(15.9),
            originZPos = cms.double(0.0),
            originYPos = cms.double(0.0),
            ptMin = cms.double(0.5),
            originXPos = cms.double(0.0),
            originRadius = cms.double(0.2)
        ),
        ComponentName = cms.string('GlobalRegionProducer')
    ),
    TTRHBuilder = cms.string('WithTrackAngle'),
    OrderedHitsFactoryPSet = cms.PSet(
        ComponentName = cms.string('StandardHitTripletGenerator'),
        GeneratorPSet = cms.PSet(
            useBending = cms.bool(True),
            useFixedPreFiltering = cms.bool(False),
            ComponentName = cms.string('PixelTripletHLTGenerator'),
            extraHitRPhitolerance = cms.double(0.032),
            useMultScattering = cms.bool(True),
            phiPreFiltering = cms.double(0.3),
            extraHitRZtolerance = cms.double(0.037)
        ),
        SeedingLayers = cms.string('PixelLayerTriplets')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    )
)


process.conversionTrackCandidates = cms.EDProducer("ConversionTrackCandidateProducer",
    scHybridBarrelProducer = cms.InputTag("cosmicSuperClusters","CosmicBarrelSuperClusters"),
    inOutTrackCandidateSCAssociationCollection = cms.string('inOutTrackCandidateSCAssociationCollection'),
    hbheModule = cms.string('hbhereco'),
    inOutTrackCandidateCollection = cms.string('inOutTracksFromConversions'),
    maxHOverE = cms.double(0.2),
    minSCEt = cms.double(5.0),
    MeasurementTrackerName = cms.string(''),
    InOutRedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    bcEndcapCollection = cms.InputTag("cosmicBasicClusters","CosmicEndcapBasicClusters"),
    outInTrackCandidateSCAssociationCollection = cms.string('outInTrackCandidateSCAssociationCollection'),
    bcBarrelCollection = cms.InputTag("cosmicBasicClusters","CosmicBarrelBasicClusters"),
    scIslandEndcapProducer = cms.InputTag("cosmicSuperClusters","CosmicEndcapSuperClusters"),
    TransientInitialStateEstimatorParameters = cms.PSet(
        propagatorAlongTISE = cms.string('alongMomElePropagator'),
        propagatorOppositeTISE = cms.string('oppositeToMomElePropagator')
    ),
    OutInRedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    outInTrackCandidateCollection = cms.string('outInTracksFromConversions'),
    hbheInstance = cms.string(''),
    TrajectoryBuilder = cms.string('TrajectoryBuilderForConversions'),
    hOverEConeSize = cms.double(0.1)
)


process.globalCosmicMuons1LegBarrelOnly = cms.EDProducer("GlobalCosmicMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
        TrackerRecHitBuilder = cms.string('WithTrackAngle'),
        TkTrackCollectionLabel = cms.string('ctfWithMaterialTracksP5'),
        SmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SmartPropagatorAny'),
            PropagatorOpposite = cms.string('SmartPropagatorAnyOpposite')
        ),
        Propagator = cms.string('SteppingHelixPropagatorAny')
    ),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    MuonCollectionLabel = cms.InputTag("cosmicMuons1LegBarrelOnly")
)


process.cosmicSuperClusters = cms.EDProducer("SuperClusterProducer",
    barrelSuperclusterCollection = cms.string('CosmicBarrelSuperClusters'),
    endcapEtaSearchRoad = cms.double(0.14),
    barrelClusterCollection = cms.string('CosmicBarrelBasicClusters'),
    endcapClusterProducer = cms.string('cosmicBasicClusters'),
    barrelPhiSearchRoad = cms.double(0.55),
    endcapPhiSearchRoad = cms.double(0.6),
    VerbosityLevel = cms.string('ERROR'),
    seedTransverseEnergyThreshold = cms.double(0.0),
    barrelClusterProducer = cms.string('cosmicBasicClusters'),
    endcapSuperclusterCollection = cms.string('CosmicEndcapSuperClusters'),
    barrelEtaSearchRoad = cms.double(0.2),
    doEndcaps = cms.bool(True),
    endcapClusterCollection = cms.string('CosmicEndcapBasicClusters'),
    doBarrel = cms.bool(True)
)


process.cscSegments = cms.EDProducer("CSCSegmentProducer",
    inputObjects = cms.InputTag("csc2DRecHits"),
    algo_psets = cms.VPSet(cms.PSet(
        chamber_types = cms.vstring('ME1/a', 
            'ME1/b', 
            'ME1/2', 
            'ME1/3', 
            'ME2/1', 
            'ME2/2', 
            'ME3/1', 
            'ME3/2', 
            'ME4/1'),
        algo_name = cms.string('CSCSegAlgoSK'),
        parameters_per_chamber_type = cms.vint32(2, 1, 1, 1, 1, 
            1, 1, 1, 1),
        algo_psets = cms.VPSet(cms.PSet(
            dPhiFineMax = cms.double(0.025),
            verboseInfo = cms.untracked.bool(True),
            chi2Max = cms.double(99999.0),
            dPhiMax = cms.double(0.003),
            wideSeg = cms.double(3.0),
            minLayersApart = cms.int32(2),
            dRPhiFineMax = cms.double(8.0),
            dRPhiMax = cms.double(8.0)
        ), 
            cms.PSet(
                dPhiFineMax = cms.double(0.025),
                verboseInfo = cms.untracked.bool(True),
                chi2Max = cms.double(99999.0),
                dPhiMax = cms.double(0.025),
                wideSeg = cms.double(3.0),
                minLayersApart = cms.int32(2),
                dRPhiFineMax = cms.double(3.0),
                dRPhiMax = cms.double(8.0)
            ))
    ), 
        cms.PSet(
            chamber_types = cms.vstring('ME1/a', 
                'ME1/b', 
                'ME1/2', 
                'ME1/3', 
                'ME2/1', 
                'ME2/2', 
                'ME3/1', 
                'ME3/2', 
                'ME4/1'),
            algo_name = cms.string('CSCSegAlgoTC'),
            parameters_per_chamber_type = cms.vint32(2, 1, 1, 1, 1, 
                1, 1, 1, 1),
            algo_psets = cms.VPSet(cms.PSet(
                dPhiFineMax = cms.double(0.02),
                verboseInfo = cms.untracked.bool(True),
                SegmentSorting = cms.int32(1),
                chi2Max = cms.double(6000.0),
                dPhiMax = cms.double(0.003),
                chi2ndfProbMin = cms.double(0.0001),
                minLayersApart = cms.int32(2),
                dRPhiFineMax = cms.double(6.0),
                dRPhiMax = cms.double(1.2)
            ), 
                cms.PSet(
                    dPhiFineMax = cms.double(0.013),
                    verboseInfo = cms.untracked.bool(True),
                    SegmentSorting = cms.int32(1),
                    chi2Max = cms.double(6000.0),
                    dPhiMax = cms.double(0.00198),
                    chi2ndfProbMin = cms.double(0.0001),
                    minLayersApart = cms.int32(2),
                    dRPhiFineMax = cms.double(3.0),
                    dRPhiMax = cms.double(0.6)
                ))
        ), 
        cms.PSet(
            chamber_types = cms.vstring('ME1/a', 
                'ME1/b', 
                'ME1/2', 
                'ME1/3', 
                'ME2/1', 
                'ME2/2', 
                'ME3/1', 
                'ME3/2', 
                'ME4/1'),
            algo_name = cms.string('CSCSegAlgoDF'),
            parameters_per_chamber_type = cms.vint32(3, 1, 2, 2, 1, 
                2, 1, 2, 1),
            algo_psets = cms.VPSet(cms.PSet(
                tanThetaMax = cms.double(1.2),
                maxRatioResidualPrune = cms.double(3.0),
                dPhiFineMax = cms.double(0.025),
                tanPhiMax = cms.double(0.5),
                dXclusBoxMax = cms.double(8.0),
                preClustering = cms.untracked.bool(False),
                chi2Max = cms.double(5000.0),
                minHitsPerSegment = cms.int32(3),
                minHitsForPreClustering = cms.int32(10),
                minLayersApart = cms.int32(2),
                dRPhiFineMax = cms.double(8.0),
                nHitsPerClusterIsShower = cms.int32(20),
                CSCSegmentDebug = cms.untracked.bool(False),
                Pruning = cms.untracked.bool(False),
                dYclusBoxMax = cms.double(8.0)
            ), 
                cms.PSet(
                    tanThetaMax = cms.double(2.0),
                    maxRatioResidualPrune = cms.double(3.0),
                    dPhiFineMax = cms.double(0.025),
                    tanPhiMax = cms.double(0.8),
                    dXclusBoxMax = cms.double(8.0),
                    preClustering = cms.untracked.bool(False),
                    chi2Max = cms.double(5000.0),
                    minHitsPerSegment = cms.int32(3),
                    minHitsForPreClustering = cms.int32(10),
                    minLayersApart = cms.int32(2),
                    dRPhiFineMax = cms.double(12.0),
                    nHitsPerClusterIsShower = cms.int32(20),
                    CSCSegmentDebug = cms.untracked.bool(False),
                    Pruning = cms.untracked.bool(False),
                    dYclusBoxMax = cms.double(12.0)
                ), 
                cms.PSet(
                    tanThetaMax = cms.double(1.2),
                    maxRatioResidualPrune = cms.double(3.0),
                    dPhiFineMax = cms.double(0.025),
                    tanPhiMax = cms.double(0.5),
                    dXclusBoxMax = cms.double(8.0),
                    preClustering = cms.untracked.bool(False),
                    chi2Max = cms.double(5000.0),
                    minHitsPerSegment = cms.int32(3),
                    minHitsForPreClustering = cms.int32(30),
                    minLayersApart = cms.int32(2),
                    dRPhiFineMax = cms.double(8.0),
                    nHitsPerClusterIsShower = cms.int32(20),
                    CSCSegmentDebug = cms.untracked.bool(False),
                    Pruning = cms.untracked.bool(False),
                    dYclusBoxMax = cms.double(8.0)
                ))
        ), 
        cms.PSet(
            chamber_types = cms.vstring('ME1/a', 
                'ME1/b', 
                'ME1/2', 
                'ME1/3', 
                'ME2/1', 
                'ME2/2', 
                'ME3/1', 
                'ME3/2', 
                'ME4/1'),
            algo_name = cms.string('CSCSegAlgoST'),
            parameters_per_chamber_type = cms.vint32(2, 1, 1, 1, 1, 
                1, 1, 1, 1),
            algo_psets = cms.VPSet(cms.PSet(
                preClustering = cms.untracked.bool(True),
                minHitsPerSegment = cms.untracked.int32(3),
                yweightPenaltyThreshold = cms.untracked.double(1.0),
                curvePenalty = cms.untracked.double(2.0),
                dXclusBoxMax = cms.untracked.double(4.0),
                hitDropLimit5Hits = cms.untracked.double(0.8),
                yweightPenalty = cms.untracked.double(1.5),
                BrutePruning = cms.untracked.bool(False),
                curvePenaltyThreshold = cms.untracked.double(0.85),
                hitDropLimit4Hits = cms.untracked.double(0.6),
                hitDropLimit6Hits = cms.untracked.double(0.3333),
                maxRecHitsInCluster = cms.untracked.int32(20),
                CSCDebug = cms.untracked.bool(False),
                onlyBestSegment = cms.untracked.bool(False),
                Pruning = cms.untracked.bool(False),
                dYclusBoxMax = cms.untracked.double(8.0)
            ), 
                cms.PSet(
                    preClustering = cms.untracked.bool(True),
                    minHitsPerSegment = cms.untracked.int32(3),
                    yweightPenaltyThreshold = cms.untracked.double(1.0),
                    curvePenalty = cms.untracked.double(2.0),
                    dXclusBoxMax = cms.untracked.double(4.0),
                    hitDropLimit5Hits = cms.untracked.double(0.8),
                    yweightPenalty = cms.untracked.double(1.5),
                    BrutePruning = cms.untracked.bool(False),
                    curvePenaltyThreshold = cms.untracked.double(0.85),
                    hitDropLimit4Hits = cms.untracked.double(0.6),
                    hitDropLimit6Hits = cms.untracked.double(0.3333),
                    maxRecHitsInCluster = cms.untracked.int32(24),
                    CSCDebug = cms.untracked.bool(False),
                    onlyBestSegment = cms.untracked.bool(False),
                    Pruning = cms.untracked.bool(False),
                    dYclusBoxMax = cms.untracked.double(8.0)
                ))
        )),
    algo_type = cms.int32(4)
)


process.muIsoDepositCalByAssociatorTowers = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("muons"),
        MultipleDepositsFlag = cms.bool(True),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    )
)


process.metOptNoHF = cms.EDProducer("METProducer",
    src = cms.InputTag("calotoweroptmaker"),
    METType = cms.string('CaloMET'),
    alias = cms.string('RawCaloMETOptNoHF'),
    noHF = cms.bool(True),
    globalThreshold = cms.double(0.0),
    InputType = cms.string('CandidateCollection')
)


process.globalCosmicMuonsNoDriftBarrelOnly = cms.EDProducer("GlobalCosmicMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrajectoryBuilderParameters = cms.PSet(
        MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
        TrackerRecHitBuilder = cms.string('WithTrackAngle'),
        TkTrackCollectionLabel = cms.string('ctfWithMaterialTracksP5'),
        SmootherParameters = cms.PSet(
            PropagatorAlong = cms.string('SmartPropagatorAny'),
            PropagatorOpposite = cms.string('SmartPropagatorAnyOpposite')
        ),
        Propagator = cms.string('SteppingHelixPropagatorAny')
    ),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    ),
    MuonCollectionLabel = cms.InputTag("cosmicMuonsNoDriftBarrelOnly")
)


process.secTriplets = cms.EDProducer("SeedGeneratorFromRegionHitsEDProducer",
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            originHalfLength = cms.double(17.5),
            originZPos = cms.double(0.0),
            originYPos = cms.double(0.0),
            ptMin = cms.double(0.3),
            originXPos = cms.double(0.0),
            originRadius = cms.double(0.2)
        ),
        ComponentName = cms.string('GlobalRegionProducer')
    ),
    TTRHBuilder = cms.string('WithTrackAngle'),
    OrderedHitsFactoryPSet = cms.PSet(
        ComponentName = cms.string('StandardHitTripletGenerator'),
        GeneratorPSet = cms.PSet(
            useBending = cms.bool(True),
            useFixedPreFiltering = cms.bool(False),
            ComponentName = cms.string('PixelTripletHLTGenerator'),
            extraHitRPhitolerance = cms.double(0.032),
            useMultScattering = cms.bool(True),
            phiPreFiltering = cms.double(0.3),
            extraHitRZtolerance = cms.double(0.037)
        ),
        SeedingLayers = cms.string('SecLayerTriplets')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    )
)


process.globalSeedsFromTripletsWithVertices = cms.EDProducer("SeedGeneratorFromRegionHitsEDProducer",
    OrderedHitsFactoryPSet = cms.PSet(
        ComponentName = cms.string('StandardHitTripletGenerator'),
        GeneratorPSet = cms.PSet(
            useBending = cms.bool(True),
            useFixedPreFiltering = cms.bool(False),
            ComponentName = cms.string('PixelTripletHLTGenerator'),
            extraHitRPhitolerance = cms.double(0.032),
            useMultScattering = cms.bool(True),
            phiPreFiltering = cms.double(0.3),
            extraHitRZtolerance = cms.double(0.037)
        ),
        SeedingLayers = cms.string('PixelLayerTriplets')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            originHalfLength = cms.double(15.9),
            originZPos = cms.double(0.0),
            originYPos = cms.double(0.0),
            ptMin = cms.double(0.9),
            originXPos = cms.double(0.0),
            originRadius = cms.double(0.2)
        ),
        ComponentName = cms.string('GlobalRegionProducer')
    ),
    TTRHBuilder = cms.string('WithTrackAngle'),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    )
)


process.muParamGlobalIsoDepositGsTk = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('track'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("ctfGSWithMaterialTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    )
)


process.dedxMedianCTF = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    MeVperADCStrip = cms.double(0.0009025),
    tracks = cms.InputTag("ctfWithMaterialTracksP5"),
    UsePixel = cms.bool(True),
    estimator = cms.string('median'),
    trajectoryTrackAssociation = cms.InputTag("ctfWithMaterialTracksP5")
)


process.dedxTruncated40CTF = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    tracks = cms.InputTag("ctfWithMaterialTracksP5"),
    estimator = cms.string('truncated'),
    fraction = cms.double(0.4),
    MeVperADCStrip = cms.double(0.0009025),
    UsePixel = cms.bool(True),
    trajectoryTrackAssociation = cms.InputTag("ctfWithMaterialTracksP5")
)


process.muParamGlobalIsoDepositCalHcal = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('track'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        DR_Veto_H = cms.double(0.1),
        Vertex_Constraint_Z = cms.bool(False),
        Threshold_H = cms.double(0.5),
        ComponentName = cms.string('CaloExtractor'),
        Threshold_E = cms.double(0.2),
        DR_Max = cms.double(1.0),
        DR_Veto_E = cms.double(0.07),
        Weight_E = cms.double(0.0),
        Vertex_Constraint_XY = cms.bool(False),
        DepositLabel = cms.untracked.string('EcalPlusHcal'),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        Weight_H = cms.double(1.0)
    )
)


process.muParamGlobalIsoDepositJets = cms.EDProducer("MuIsoDepositProducer",
    IOPSet = cms.PSet(
        ExtractForCandidate = cms.bool(False),
        inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
        MultipleDepositsFlag = cms.bool(False),
        MuonTrackRefType = cms.string('bestTrkSta'),
        InputType = cms.string('MuonCollection')
    ),
    ExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    )
)


process.secWithMaterialTracks = cms.EDProducer("TrackProducer",
    src = cms.InputTag("secTrackCandidates"),
    clusterRemovalInfo = cms.InputTag("secClusters"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    Fitter = cms.string('KFFittingSmootherWithOutliersRejectionAndRK'),
    useHitsSplitting = cms.bool(False),
    alias = cms.untracked.string('ctfWithMaterialTracks'),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithAngleAndTemplate'),
    AlgorithmName = cms.string('undefAlgorithm'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.ctfWithMaterialTracksP5 = cms.EDProducer("TrackProducer",
    src = cms.InputTag("ckfTrackCandidatesP5"),
    clusterRemovalInfo = cms.InputTag(""),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    Fitter = cms.string('FittingSmootherRKP5'),
    useHitsSplitting = cms.bool(False),
    alias = cms.untracked.string('ctfWithMaterialTracks'),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithAngleAndTemplate'),
    AlgorithmName = cms.string('undefAlgorithm'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.ecalFixedAlphaBetaFitUncalibRecHit = cms.EDProducer("EcalFixedAlphaBetaFitUncalibRecHitProducer",
    EEdigiCollection = cms.InputTag("ecalDigis","eeDigis"),
    betaEE = cms.double(1.37),
    betaEB = cms.double(1.7),
    EBdigiCollection = cms.InputTag("ecalDigis","ebDigis"),
    EEhitCollection = cms.string('EcalUncalibRecHitsEE'),
    AlphaBetaFilename = cms.untracked.string('NOFILE'),
    alphaEE = cms.double(1.63),
    MinAmplEndcap = cms.double(14.0),
    MinAmplBarrel = cms.double(8.0),
    alphaEB = cms.double(1.2),
    UseDynamicPedestal = cms.bool(True),
    EBhitCollection = cms.string('EcalUncalibRecHitsEB')
)


process.offlineBeamSpot = cms.EDProducer("BeamSpotProducer")


process.lhcStandAloneMuonsBarrelOnly = cms.EDProducer("StandAloneMuonProducer",
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    InputObjects = cms.InputTag("lhcMuonSeedBarrelOnly"),
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorOpposite'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(True)
    ),
    STATrajBuilderParameters = cms.PSet(
        DoRefit = cms.bool(False),
        FilterParameters = cms.PSet(
            NumberOfSigma = cms.double(3.0),
            FitDirection = cms.string('insideOut'),
            DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
            MaxChi2 = cms.double(1000.0),
            MuonTrajectoryUpdatorParameters = cms.PSet(
                MaxChi2 = cms.double(1000.0),
                RescaleError = cms.bool(False),
                RescaleErrorFactor = cms.double(100.0),
                Granularity = cms.int32(0)
            ),
            EnableRPCMeasurement = cms.bool(True),
            CSCRecSegmentLabel = cms.InputTag("cscSegments"),
            EnableDTMeasurement = cms.bool(True),
            RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            EnableCSCMeasurement = cms.bool(True)
        ),
        SeedPropagator = cms.string('SteppingHelixPropagatorAny'),
        NavigationType = cms.string('Standard'),
        DoBackwardFilter = cms.bool(True),
        SeedPosition = cms.string('in'),
        BWFilterParameters = cms.PSet(
            NumberOfSigma = cms.double(3.0),
            BWSeedType = cms.string('fromGenerator'),
            FitDirection = cms.string('outsideIn'),
            DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
            MaxChi2 = cms.double(100.0),
            MuonTrajectoryUpdatorParameters = cms.PSet(
                MaxChi2 = cms.double(100.0),
                RescaleError = cms.bool(False),
                RescaleErrorFactor = cms.double(100.0),
                Granularity = cms.int32(2)
            ),
            EnableRPCMeasurement = cms.bool(True),
            CSCRecSegmentLabel = cms.InputTag("cscSegments"),
            EnableDTMeasurement = cms.bool(True),
            RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            EnableCSCMeasurement = cms.bool(False)
        ),
        RefitterParameters = cms.PSet(
            FitterName = cms.string('KFFitterSmootherSTA'),
            Option = cms.int32(1)
        )
    )
)


process.ecalWeightUncalibRecHit = cms.EDProducer("EcalWeightUncalibRecHitProducer",
    EBdigiCollection = cms.InputTag("ecalDigis","ebDigis"),
    EEhitCollection = cms.string('EcalUncalibRecHitsEE'),
    EEdigiCollection = cms.InputTag("ecalDigis","eeDigis"),
    EBhitCollection = cms.string('EcalUncalibRecHitsEB')
)


process.standAloneMuons = cms.EDProducer("StandAloneMuonProducer",
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorOpposite'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(True)
    ),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    InputObjects = cms.InputTag("MuonSeed"),
    STATrajBuilderParameters = cms.PSet(
        DoRefit = cms.bool(False),
        FilterParameters = cms.PSet(
            NumberOfSigma = cms.double(3.0),
            FitDirection = cms.string('insideOut'),
            DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
            MaxChi2 = cms.double(1000.0),
            MuonTrajectoryUpdatorParameters = cms.PSet(
                MaxChi2 = cms.double(1000.0),
                RescaleError = cms.bool(False),
                RescaleErrorFactor = cms.double(100.0),
                Granularity = cms.int32(0)
            ),
            EnableRPCMeasurement = cms.bool(True),
            CSCRecSegmentLabel = cms.InputTag("cscSegments"),
            EnableDTMeasurement = cms.bool(True),
            RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            EnableCSCMeasurement = cms.bool(True)
        ),
        SeedPropagator = cms.string('SteppingHelixPropagatorAny'),
        NavigationType = cms.string('Standard'),
        DoBackwardFilter = cms.bool(True),
        SeedPosition = cms.string('in'),
        BWFilterParameters = cms.PSet(
            NumberOfSigma = cms.double(3.0),
            BWSeedType = cms.string('fromGenerator'),
            FitDirection = cms.string('outsideIn'),
            DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
            MaxChi2 = cms.double(100.0),
            MuonTrajectoryUpdatorParameters = cms.PSet(
                MaxChi2 = cms.double(100.0),
                RescaleError = cms.bool(False),
                RescaleErrorFactor = cms.double(100.0),
                Granularity = cms.int32(2)
            ),
            EnableRPCMeasurement = cms.bool(True),
            CSCRecSegmentLabel = cms.InputTag("cscSegments"),
            EnableDTMeasurement = cms.bool(True),
            RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            EnableCSCMeasurement = cms.bool(True)
        ),
        RefitterParameters = cms.PSet(
            FitterName = cms.string('KFFitterSmootherSTA'),
            Option = cms.int32(1)
        )
    )
)


process.csc2DRecHits = cms.EDProducer("CSCRecHitDProducer",
    XTasymmetry_ME1b = cms.untracked.double(0.0),
    XTasymmetry_ME1a = cms.untracked.double(0.0),
    ConstSyst_ME1a = cms.untracked.double(0.022),
    ConstSyst_ME41 = cms.untracked.double(0.0),
    XTasymmetry_ME41 = cms.untracked.double(0.0),
    XTasymmetry_ME22 = cms.untracked.double(0.0),
    XTasymmetry_ME21 = cms.untracked.double(0.0),
    ConstSyst_ME21 = cms.untracked.double(0.0),
    ConstSyst_ME22 = cms.untracked.double(0.0),
    XTasymmetry_ME31 = cms.untracked.double(0.0),
    NoiseLevel_ME13 = cms.untracked.double(8.0),
    NoiseLevel_ME12 = cms.untracked.double(9.0),
    NoiseLevel_ME32 = cms.untracked.double(9.0),
    NoiseLevel_ME31 = cms.untracked.double(9.0),
    XTasymmetry_ME32 = cms.untracked.double(0.0),
    ConstSyst_ME1b = cms.untracked.double(0.007),
    XTasymmetry_ME13 = cms.untracked.double(0.0),
    XTasymmetry_ME12 = cms.untracked.double(0.0),
    ConstSyst_ME12 = cms.untracked.double(0.0),
    ConstSyst_ME13 = cms.untracked.double(0.0),
    ConstSyst_ME32 = cms.untracked.double(0.0),
    ConstSyst_ME31 = cms.untracked.double(0.0),
    NoiseLevel_ME1a = cms.untracked.double(7.0),
    NoiseLevel_ME1b = cms.untracked.double(8.0),
    NoiseLevel_ME21 = cms.untracked.double(9.0),
    NoiseLevel_ME22 = cms.untracked.double(9.0),
    NoiseLevel_ME41 = cms.untracked.double(9.0),
    CSCStripClusterSize = cms.untracked.int32(3),
    CSCStripPeakThreshold = cms.untracked.double(10.0),
    readBadChannels = cms.bool(False),
    stripDigiTag = cms.InputTag("muonCSCDigis","MuonCSCStripDigi"),
    CSCStripxtalksOffset = cms.untracked.double(0.03),
    CSCstripWireDeltaTime = cms.untracked.int32(8),
    CSCUseCalibrations = cms.untracked.bool(True),
    wireDigiTag = cms.InputTag("muonCSCDigis","MuonCSCWireDigi"),
    CSCDebug = cms.untracked.bool(False),
    CSCWireClusterDeltaT = cms.untracked.int32(1),
    CSCStripClusterChargeCut = cms.untracked.double(25.0)
)


process.dedxHarmonic2CosmicTF = cms.EDProducer("DeDxEstimatorProducer",
    UseStrip = cms.bool(True),
    MeVperADCPixel = cms.double(3.61e-06),
    MeVperADCStrip = cms.double(0.0009025),
    tracks = cms.InputTag("cosmictrackfinderP5"),
    UsePixel = cms.bool(True),
    estimator = cms.string('generic'),
    exponent = cms.double(-2.0),
    trajectoryTrackAssociation = cms.InputTag("cosmictrackfinderP5")
)


process.horeco = cms.EDFilter("HcalSimpleReconstructor",
    correctionPhaseNS = cms.double(10.0),
    digiLabel = cms.InputTag("hcalDigis"),
    samplesToAdd = cms.int32(8),
    Subdetector = cms.string('HO'),
    correctForTimeslew = cms.bool(True),
    correctForPhaseContainment = cms.bool(True),
    firstSample = cms.int32(1)
)


process.CosmicMuonSeed = cms.EDFilter("CosmicMuonSeedGenerator",
    MaxSeeds = cms.int32(10),
    CSCRecSegmentLabel = cms.untracked.InputTag("cscSegments"),
    EnableDTMeasurement = cms.untracked.bool(True),
    MaxCSCChi2 = cms.double(300.0),
    MaxDTChi2 = cms.double(300.0),
    DTRecSegmentLabel = cms.untracked.InputTag("dt4DSegments"),
    EnableCSCMeasurement = cms.untracked.bool(True)
)


process.firstfilter = cms.EDFilter("QualityFilter",
    TrackQuality = cms.string('highPurity'),
    recTracks = cms.InputTag("firstStepTracksWithQuality")
)


process.secClusters = cms.EDFilter("TrackClusterRemover",
    trajectories = cms.InputTag("firstfilter"),
    pixelClusters = cms.InputTag("siPixelClusters"),
    Common = cms.PSet(
        maxChi2 = cms.double(30.0)
    ),
    stripClusters = cms.InputTag("siStripClusters")
)


process.cosmictrackfinder = cms.EDFilter("CosmicTrackFinder",
    TrajInEvents = cms.bool(True),
    MinHits = cms.int32(4),
    HitProducer = cms.string('siStripRecHits'),
    pixelRecHits = cms.InputTag("siPixelRecHits"),
    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
    stereorecHits = cms.InputTag("siStripMatchedRecHits","stereoRecHit"),
    Chi2Cut = cms.double(30.0),
    TTRHBuilder = cms.string('WithTrackAngle'),
    rphirecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
    debug = cms.untracked.bool(True),
    GeometricStructure = cms.untracked.string('MTCC'),
    cosmicSeeds = cms.InputTag("cosmicseedfinder")
)


process.secTrackCandidates = cms.EDFilter("CkfTrackCandidateMaker",
    TransientInitialStateEstimatorParameters = cms.PSet(
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    SeedLabel = cms.string(''),
    useHitsSplitting = cms.bool(True),
    doSeedingRegionRebuilding = cms.bool(True),
    SeedProducer = cms.string('secTriplets'),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    TrajectoryBuilder = cms.string('secCkfTrajectoryBuilder'),
    TrajectoryCleaner = cms.string('TrajectoryCleanerBySharedHits')
)


process.newTrackCandidateMaker = cms.EDFilter("CkfTrackCandidateMaker",
    TransientInitialStateEstimatorParameters = cms.PSet(
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    SeedLabel = cms.string(''),
    useHitsSplitting = cms.bool(True),
    doSeedingRegionRebuilding = cms.bool(True),
    SeedProducer = cms.string('newCombinedSeeds'),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    TrajectoryBuilder = cms.string('newTrajectoryBuilder'),
    TrajectoryCleaner = cms.string('TrajectoryCleanerBySharedHits')
)


process.hbhereco = cms.EDFilter("HcalSimpleReconstructor",
    correctionPhaseNS = cms.double(10.0),
    digiLabel = cms.InputTag("hcalDigis"),
    samplesToAdd = cms.int32(8),
    Subdetector = cms.string('HBHE'),
    correctForTimeslew = cms.bool(True),
    correctForPhaseContainment = cms.bool(True),
    firstSample = cms.int32(1)
)


process.siStripMatchedRecHits = cms.EDFilter("SiStripRecHitConverter",
    StripCPE = cms.string('StripCPEfromTrackAngle'),
    Regional = cms.bool(False),
    stereoRecHits = cms.string('stereoRecHit'),
    useSiStripQuality = cms.bool(False),
    matchedRecHits = cms.string('matchedRecHit'),
    LazyGetterProducer = cms.string('SiStripRawToClustersFacility'),
    ClusterProducer = cms.string('siStripClusters'),
    VerbosityLevel = cms.untracked.int32(1),
    rphiRecHits = cms.string('rphiRecHit'),
    Matcher = cms.string('StandardMatcher'),
    siStripQualityLabel = cms.string(''),
    MaskBadAPVFibers = cms.bool(False)
)


process.CosmicMuonSeedBarrelOnly = cms.EDFilter("CosmicMuonSeedGenerator",
    DTRecSegmentLabel = cms.untracked.InputTag("dt4DSegments"),
    CSCRecSegmentLabel = cms.untracked.InputTag("cscSegments"),
    EnableDTMeasurement = cms.untracked.bool(True),
    MaxCSCChi2 = cms.double(300.0),
    MaxDTChi2 = cms.double(300.0),
    MaxSeeds = cms.int32(10),
    EnableCSCMeasurement = cms.untracked.bool(False)
)


process.withTightQuality = cms.EDFilter("AnalyticalTrackSelector",
    keepAllTracks = cms.bool(True),
    beamspot = cms.InputTag("offlineBeamSpot"),
    vtxTracks = cms.uint32(3),
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(True),
    vertices = cms.InputTag("pixelVertices"),
    qualityBit = cms.string('tight'),
    vtxNumber = cms.int32(-1),
    vtxChi2Prob = cms.double(0.01),
    minNumberLayers = cms.uint32(0),
    chi2n_par = cms.double(0.9),
    d0_par2 = cms.vdouble(0.4, 4.0),
    d0_par1 = cms.vdouble(0.3, 4.0),
    src = cms.InputTag("withLooseQuality"),
    dz_par1 = cms.vdouble(0.35, 4.0),
    res_par = cms.vdouble(0.003, 0.01),
    dz_par2 = cms.vdouble(0.4, 4.0)
)


process.correctedHybridSuperClusters = cms.EDFilter("EgammaSCCorrectionMaker",
    corectedSuperClusterCollection = cms.string(''),
    sigmaElectronicNoise = cms.double(0.03),
    superClusterAlgo = cms.string('Hybrid'),
    etThresh = cms.double(0.0),
    rawSuperClusterProducer = cms.InputTag("hybridSuperClusters"),
    applyEnergyCorrection = cms.bool(True),
    VerbosityLevel = cms.string('ERROR'),
    hyb_fCorrPset = cms.PSet(
        brLinearLowThr = cms.double(1.1),
        fEtEtaVec = cms.vdouble(1.0012, -0.5714, 0, 0, 0, 
            0.5549, 12.74, 1.0448, 0, 0, 
            0, 0, 8.0, 1.023, -0.00181, 
            0, 0),
        brLinearHighThr = cms.double(8.0),
        fBremVec = cms.vdouble(-0.05208, 0.1331, 0.9196, -0.0005735, 1.343)
    ),
    recHitProducer = cms.InputTag("ecalRecHit","EcalRecHitsEB")
)


process.fourthClusters = cms.EDFilter("TrackClusterRemover",
    oldClusterRemovalInfo = cms.InputTag("thClusters"),
    trajectories = cms.InputTag("thStep"),
    pixelClusters = cms.InputTag("thClusters"),
    Common = cms.PSet(
        maxChi2 = cms.double(30.0)
    ),
    stripClusters = cms.InputTag("thClusters")
)


process.generalTracks = cms.EDFilter("SimpleTrackListMerger",
    ShareFrac = cms.double(0.66),
    newQuality = cms.string('confirmed'),
    promoteTrackQuality = cms.bool(True),
    MinPT = cms.double(0.05),
    Epsilon = cms.double(-0.001),
    MaxNormalizedChisq = cms.double(1000.0),
    MinFound = cms.int32(3),
    TrackProducer2 = cms.string('thStep'),
    TrackProducer1 = cms.string('mergeFirstTwoSteps')
)


process.secStep = cms.EDFilter("VertexFilter",
    TrackAlgorithm = cms.string('iter2'),
    recVertices = cms.InputTag("pixelVertices"),
    TrackQualities = cms.vstring('loose', 
        'tight', 
        'highPurity'),
    DistRhoFromVertex = cms.double(0.1),
    DistZFromVertex = cms.double(0.4),
    recTracks = cms.InputTag("secWithMaterialTracks"),
    UseQuality = cms.bool(True),
    ChiCut = cms.double(130.0),
    VertexCut = cms.bool(True),
    MinHits = cms.int32(3)
)


process.thPixelRecHits = cms.EDFilter("SiPixelRecHitConverter",
    eff_charge_cut_lowY = cms.untracked.double(0.0),
    eff_charge_cut_lowX = cms.untracked.double(0.0),
    src = cms.InputTag("thClusters"),
    eff_charge_cut_highX = cms.untracked.double(1.0),
    eff_charge_cut_highY = cms.untracked.double(1.0),
    size_cutY = cms.untracked.double(3.0),
    size_cutX = cms.untracked.double(3.0),
    CPE = cms.string('PixelCPEGeneric'),
    VerboseLevel = cms.untracked.int32(0),
    TanLorentzAnglePerTesla = cms.double(0.106),
    Alpha2Order = cms.bool(True),
    speed = cms.int32(0)
)


process.calotoweroptmaker = cms.EDFilter("CaloTowersCreator",
    MomEmDepth = cms.double(0.0),
    EBSumThreshold = cms.double(0.2),
    EBWeight = cms.double(1.0),
    hfInput = cms.InputTag("hfreco"),
    EESumThreshold = cms.double(0.45),
    HOThreshold = cms.double(0.5),
    HBGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    HBThreshold = cms.double(0.5),
    MomConstrMethod = cms.int32(0),
    HcalThreshold = cms.double(-1000.0),
    HF2Weights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    HOWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    EEGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    HEDWeight = cms.double(1.0),
    EEWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    EEWeight = cms.double(1.0),
    UseHO = cms.bool(False),
    HBWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    HESWeight = cms.double(1.0),
    HF1Weight = cms.double(1.0),
    HF2Grid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    HEDWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    HF1Grid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    MomHadDepth = cms.double(0.0),
    HOWeight = cms.double(1.0),
    EBThreshold = cms.double(0.09),
    hbheInput = cms.InputTag("hbhereco"),
    HF2Weight = cms.double(1.0),
    HF2Threshold = cms.double(1.8),
    EEThreshold = cms.double(0.45),
    HESThreshold = cms.double(0.7),
    HF1Weights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    hoInput = cms.InputTag("horeco"),
    HF1Threshold = cms.double(1.2),
    HESGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    EBWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    MomTotDepth = cms.double(0.0),
    HESWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    HEDThreshold = cms.double(0.5),
    EcutTower = cms.double(-1000.0),
    HEDGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    ecalInputs = cms.VInputTag(cms.InputTag("ecalRecHit","EcalRecHitsEB"), cms.InputTag("ecalRecHit","EcalRecHitsEE")),
    HBWeight = cms.double(1.0),
    HOGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    EBGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0)
)


process.roadSearchClouds = cms.EDFilter("RoadSearchCloudMaker",
    MinimalFractionOfUsedLayersPerCloud = cms.double(0.5),
    pixelRecHits = cms.InputTag("siPixelRecHits"),
    MergingFraction = cms.double(0.8),
    MaxDetHitsInCloudPerDetId = cms.uint32(32),
    SeedProducer = cms.InputTag("roadSearchSeeds"),
    DoCloudCleaning = cms.bool(True),
    IncreaseMaxNumberOfConsecutiveMissedLayersPerCloud = cms.uint32(4),
    rphiStripRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
    UseStereoRecHits = cms.bool(False),
    ZPhiRoadSize = cms.double(0.06),
    MaximalFractionOfConsecutiveMissedLayersPerCloud = cms.double(0.15),
    stereoStripRecHits = cms.InputTag("siStripMatchedRecHits","stereoRecHit"),
    MaximalFractionOfMissedLayersPerCloud = cms.double(0.3),
    scalefactorRoadSeedWindow = cms.double(1.5),
    UsePixelsinRS = cms.bool(True),
    IncreaseMaxNumberOfMissedLayersPerCloud = cms.uint32(3),
    RoadsLabel = cms.string(''),
    MaxRecHitsInCloud = cms.int32(100),
    UseRphiRecHits = cms.bool(False),
    StraightLineNoBeamSpotCloud = cms.bool(False),
    RPhiRoadSize = cms.double(0.02),
    matchedStripRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
    MinimumHalfRoad = cms.double(0.55)
)


process.cosmicseedfinder = cms.EDFilter("CosmicSeedGenerator",
    maxSeeds = cms.int32(10000),
    originHalfLength = cms.double(90.0),
    originZPosition = cms.double(0.0),
    GeometricStructure = cms.untracked.string('STANDARD'),
    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
    MaxNumberOfCosmicClusters = cms.uint32(300),
    SeedPt = cms.double(5.0),
    HitsForSeeds = cms.untracked.string('pairs'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    ptMin = cms.double(0.9),
    rphirecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
    doClusterCheck = cms.bool(True),
    originRadius = cms.double(150.0),
    ClusterCollectionLabel = cms.InputTag("siStripClusters"),
    stereorecHits = cms.InputTag("siStripMatchedRecHits","stereoRecHit")
)


process.roadSearchSeeds = cms.EDFilter("RoadSearchSeedFinder",
    OuterSeedRecHitAccessMode = cms.string('RPHI'),
    pixelRecHits = cms.InputTag("siPixelRecHits"),
    MaximalEndcapImpactParameter = cms.double(1.2),
    MaxNumberOfCosmicClusters = cms.uint32(300),
    MergeSeedsCenterCut_B = cms.double(0.25),
    MergeSeedsCenterCut_A = cms.double(0.05),
    MergeSeedsDifferentHitsCut = cms.uint32(1),
    rphiStripRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
    MaximalBarrelImpactParameter = cms.double(0.2),
    doClusterCheck = cms.bool(False),
    stereoStripRecHits = cms.InputTag("siStripMatchedRecHits","stereoRecHit"),
    ClusterCollectionLabel = cms.InputTag("siStripClusters"),
    OuterSeedRecHitAccessUseStereo = cms.bool(False),
    MergeSeedsCenterCut_C = cms.double(0.4),
    MinimalReconstructedTransverseMomentum = cms.double(1.5),
    PhiRangeForDetIdLookupInRings = cms.double(0.5),
    Mode = cms.string('STANDARD'),
    RoadsLabel = cms.string(''),
    InnerSeedRecHitAccessMode = cms.string('RPHI'),
    InnerSeedRecHitAccessUseStereo = cms.bool(False),
    OuterSeedRecHitAccessUseRPhi = cms.bool(False),
    MergeSeedsRadiusCut_B = cms.double(0.25),
    MergeSeedsRadiusCut_C = cms.double(0.4),
    matchedStripRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
    MergeSeedsRadiusCut_A = cms.double(0.05),
    InnerSeedRecHitAccessUseRPhi = cms.bool(False)
)


process.ckfTrackCandidates = cms.EDFilter("CkfTrackCandidateMaker",
    TransientInitialStateEstimatorParameters = cms.PSet(
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    SeedLabel = cms.string(''),
    useHitsSplitting = cms.bool(True),
    doSeedingRegionRebuilding = cms.bool(True),
    SeedProducer = cms.string('globalMixedSeeds'),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    TrajectoryBuilder = cms.string('GroupedCkfTrajectoryBuilder'),
    TrajectoryCleaner = cms.string('TrajectoryCleanerBySharedHits')
)


process.fourthStripRecHits = cms.EDFilter("SiStripRecHitConverter",
    StripCPE = cms.string('StripCPEfromTrackAngle'),
    LazyGetterProducer = cms.string('SiStripRawToClustersFacility'),
    stereoRecHits = cms.string('stereoRecHit'),
    useSiStripQuality = cms.bool(False),
    matchedRecHits = cms.string('matchedRecHit'),
    Regional = cms.bool(False),
    ClusterProducer = cms.string('fourthClusters'),
    VerbosityLevel = cms.untracked.int32(1),
    rphiRecHits = cms.string('rphiRecHit'),
    Matcher = cms.string('StandardMatcher'),
    siStripQualityLabel = cms.string(''),
    MaskBadAPVFibers = cms.bool(False)
)


process.combinatorialbeamhaloseedfinder = cms.EDFilter("CtfSpecialSeedGenerator",
    ErrorRescaling = cms.double(50.0),
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            originHalfLength = cms.double(15.9),
            originZPos = cms.double(0.0),
            originYPos = cms.double(0.0),
            ptMin = cms.double(0.9),
            originXPos = cms.double(0.0),
            originRadius = cms.double(0.2)
        ),
        ComponentName = cms.string('GlobalRegionProducer')
    ),
    Charges = cms.vint32(-1, 1),
    OrderedHitsFactoryPSets = cms.VPSet(cms.PSet(
        ComponentName = cms.string('BeamHaloPairGenerator'),
        maxTheta = cms.double(1.0),
        NavigationDirection = cms.string('outsideIn'),
        LayerPSet = cms.PSet(
            TEC4 = cms.PSet(
                minRing = cms.int32(1),
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                useRingSlector = cms.untracked.bool(True),
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                maxRing = cms.int32(2)
            ),
            TEC5 = cms.PSet(
                minRing = cms.int32(1),
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                useRingSlector = cms.untracked.bool(True),
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                maxRing = cms.int32(2)
            ),
            TEC6 = cms.PSet(
                minRing = cms.int32(1),
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                useRingSlector = cms.untracked.bool(True),
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                maxRing = cms.int32(2)
            ),
            TEC = cms.PSet(
                minRing = cms.int32(5),
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                useRingSlector = cms.untracked.bool(False),
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                maxRing = cms.int32(7)
            ),
            TEC1 = cms.PSet(
                minRing = cms.int32(1),
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                useRingSlector = cms.untracked.bool(True),
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                maxRing = cms.int32(2)
            ),
            TEC2 = cms.PSet(
                minRing = cms.int32(1),
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                useRingSlector = cms.untracked.bool(True),
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                maxRing = cms.int32(2)
            ),
            TEC3 = cms.PSet(
                minRing = cms.int32(1),
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                useRingSlector = cms.untracked.bool(True),
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                maxRing = cms.int32(2)
            ),
            FPix = cms.PSet(
                hitErrorRZ = cms.double(0.0036),
                hitErrorRPhi = cms.double(0.0051),
                TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelPairs'),
                HitProducer = cms.string('siPixelRecHits'),
                useErrorsFromParam = cms.untracked.bool(True)
            ),
            TID = cms.PSet(
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                useRingSlector = cms.untracked.bool(False),
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            layerList = cms.vstring('FPix1_pos+FPix2_pos', 
                'FPix1_neg+FPix2_neg', 
                'TID2_pos+TID3_pos', 
                'TID2_neg+TID3_neg', 
                'TEC1_neg+TEC2_neg', 
                'TEC1_pos+TEC2_pos', 
                'TEC2_neg+TEC3_neg', 
                'TEC2_pos+TEC3_pos', 
                'TEC3_neg+TEC4_neg', 
                'TEC3_pos+TEC4_pos', 
                'TEC4_neg+TEC5_neg', 
                'TEC4_pos+TEC5_pos', 
                'TEC5_neg+TEC6_neg', 
                'TEC5_pos+TEC6_pos', 
                'TEC7_neg+TEC8_neg', 
                'TEC7_pos+TEC8_pos', 
                'TEC8_neg+TEC9_neg', 
                'TEC8_pos+TEC9_pos')
        ),
        PropagationDirection = cms.string('alongMomentum')
    ), 
        cms.PSet(
            ComponentName = cms.string('BeamHaloPairGenerator'),
            maxTheta = cms.double(1.0),
            NavigationDirection = cms.string('outsideIn'),
            LayerPSet = cms.PSet(
                TEC4 = cms.PSet(
                    minRing = cms.int32(1),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(True),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(2)
                ),
                TEC5 = cms.PSet(
                    minRing = cms.int32(1),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(True),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(2)
                ),
                TEC6 = cms.PSet(
                    minRing = cms.int32(1),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(True),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(2)
                ),
                TEC = cms.PSet(
                    minRing = cms.int32(5),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(False),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(7)
                ),
                TEC1 = cms.PSet(
                    minRing = cms.int32(1),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(True),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(2)
                ),
                TEC2 = cms.PSet(
                    minRing = cms.int32(1),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(True),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(2)
                ),
                TEC3 = cms.PSet(
                    minRing = cms.int32(1),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(True),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(2)
                ),
                FPix = cms.PSet(
                    hitErrorRZ = cms.double(0.0036),
                    hitErrorRPhi = cms.double(0.0051),
                    TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelPairs'),
                    HitProducer = cms.string('siPixelRecHits'),
                    useErrorsFromParam = cms.untracked.bool(True)
                ),
                TID = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(False),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                layerList = cms.vstring('FPix1_pos+FPix2_pos', 
                    'FPix1_neg+FPix2_neg', 
                    'TID2_pos+TID3_pos', 
                    'TID2_neg+TID3_neg', 
                    'TEC1_neg+TEC2_neg', 
                    'TEC1_pos+TEC2_pos', 
                    'TEC2_neg+TEC3_neg', 
                    'TEC2_pos+TEC3_pos', 
                    'TEC3_neg+TEC4_neg', 
                    'TEC3_pos+TEC4_pos', 
                    'TEC4_neg+TEC5_neg', 
                    'TEC4_pos+TEC5_pos', 
                    'TEC5_neg+TEC6_neg', 
                    'TEC5_pos+TEC6_pos', 
                    'TEC7_neg+TEC8_neg', 
                    'TEC7_pos+TEC8_pos', 
                    'TEC8_neg+TEC9_neg', 
                    'TEC8_pos+TEC9_pos')
            ),
            PropagationDirection = cms.string('oppositeToMomentum')
        )),
    MaxNumberOfCosmicClusters = cms.uint32(1000),
    UseScintillatorsConstraint = cms.bool(False),
    SetMomentum = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    SeedsFromPositiveY = cms.bool(False),
    doClusterCheck = cms.bool(True),
    SeedMomentum = cms.double(15.0),
    maxSeeds = cms.int32(10000),
    CheckHitsAreOnDifferentLayers = cms.bool(False),
    ClusterCollectionLabel = cms.InputTag("siStripClusters"),
    requireBOFF = cms.bool(False)
)


process.firstStepTracksWithQuality = cms.EDFilter("AnalyticalTrackSelector",
    keepAllTracks = cms.bool(True),
    beamspot = cms.InputTag("offlineBeamSpot"),
    vtxTracks = cms.uint32(3),
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(True),
    vertices = cms.InputTag("pixelVertices"),
    qualityBit = cms.string('highPurity'),
    vtxNumber = cms.int32(-1),
    vtxChi2Prob = cms.double(0.01),
    minNumberLayers = cms.uint32(0),
    chi2n_par = cms.double(0.9),
    d0_par2 = cms.vdouble(0.4, 4.0),
    d0_par1 = cms.vdouble(0.3, 4.0),
    src = cms.InputTag("withTightQuality"),
    dz_par1 = cms.vdouble(0.35, 4.0),
    res_par = cms.vdouble(0.003, 0.001),
    dz_par2 = cms.vdouble(0.4, 4.0)
)


process.egammaCkfTrackCandidates = cms.EDFilter("CkfTrackCandidateMaker",
    TransientInitialStateEstimatorParameters = cms.PSet(
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    SeedLabel = cms.string(''),
    useHitsSplitting = cms.bool(True),
    doSeedingRegionRebuilding = cms.bool(True),
    SeedProducer = cms.string('electronPixelSeeds'),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    TrajectoryBuilder = cms.string('TrajectoryBuilderForPixelMatchGsfElectrons'),
    TrajectoryCleaner = cms.string('TrajectoryCleanerBySharedHits')
)


process.ckfTrackCandidatesP5 = cms.EDFilter("CkfTrackCandidateMaker",
    TransientInitialStateEstimatorParameters = cms.PSet(
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    SeedLabel = cms.string(''),
    useHitsSplitting = cms.bool(True),
    doSeedingRegionRebuilding = cms.bool(True),
    SeedProducer = cms.string('combinedP5SeedsForCTF'),
    NavigationSchool = cms.string('CosmicNavigationSchool'),
    TrajectoryBuilder = cms.string('GroupedCkfTrajectoryBuilderP5'),
    TrajectoryCleaner = cms.string('TrajectoryCleanerBySharedHits')
)


process.thStripRecHits = cms.EDFilter("SiStripRecHitConverter",
    StripCPE = cms.string('StripCPEfromTrackAngle'),
    LazyGetterProducer = cms.string('SiStripRawToClustersFacility'),
    stereoRecHits = cms.string('stereoRecHit'),
    useSiStripQuality = cms.bool(False),
    matchedRecHits = cms.string('matchedRecHit'),
    Regional = cms.bool(False),
    ClusterProducer = cms.string('thClusters'),
    VerbosityLevel = cms.untracked.int32(1),
    rphiRecHits = cms.string('rphiRecHit'),
    Matcher = cms.string('StandardMatcher'),
    siStripQualityLabel = cms.string(''),
    MaskBadAPVFibers = cms.bool(False)
)


process.secStripRecHits = cms.EDFilter("SiStripRecHitConverter",
    StripCPE = cms.string('StripCPEfromTrackAngle'),
    LazyGetterProducer = cms.string('SiStripRawToClustersFacility'),
    stereoRecHits = cms.string('stereoRecHit'),
    useSiStripQuality = cms.bool(False),
    matchedRecHits = cms.string('matchedRecHit'),
    Regional = cms.bool(False),
    ClusterProducer = cms.string('secClusters'),
    VerbosityLevel = cms.untracked.int32(1),
    rphiRecHits = cms.string('rphiRecHit'),
    Matcher = cms.string('StandardMatcher'),
    siStripQualityLabel = cms.string(''),
    MaskBadAPVFibers = cms.bool(False)
)


process.towerMaker = cms.EDFilter("CaloTowersCreator",
    MomEmDepth = cms.double(0),
    EBSumThreshold = cms.double(0.2),
    EBWeight = cms.double(1.0),
    hfInput = cms.InputTag("hfreco"),
    AllowMissingInputs = cms.untracked.bool(False),
    EESumThreshold = cms.double(0.45),
    HOThreshold = cms.double(1.1),
    HBThreshold = cms.double(0.6),
    EBThreshold = cms.double(0.09),
    MomConstrMethod = cms.int32(0),
    HcalThreshold = cms.double(-1000.0),
    HF1Threshold = cms.double(1.2),
    HEDWeight = cms.double(1.0),
    EEWeight = cms.double(1.0),
    UseHO = cms.bool(True),
    HF1Weight = cms.double(1.0),
    MomHadDepth = cms.double(0),
    HOWeight = cms.double(1e-99),
    HESWeight = cms.double(1.0),
    hbheInput = cms.InputTag("hbhereco"),
    HF2Weight = cms.double(1.0),
    HF2Threshold = cms.double(1.8),
    EEThreshold = cms.double(0.45),
    HESThreshold = cms.double(1.4),
    hoInput = cms.InputTag("horeco"),
    MomTotDepth = cms.double(0),
    HEDThreshold = cms.double(1.4),
    EcutTower = cms.double(-1000.0),
    ecalInputs = cms.VInputTag(cms.InputTag("ecalRecHit","EcalRecHitsEB"), cms.InputTag("ecalRecHit","EcalRecHitsEE")),
    HBWeight = cms.double(1.0)
)


process.roadSearchSeedsP5 = cms.EDFilter("RoadSearchSeedFinder",
    OuterSeedRecHitAccessMode = cms.string('STANDARD'),
    pixelRecHits = cms.InputTag("siPixelRecHits"),
    MaximalEndcapImpactParameter = cms.double(1.2),
    MaxNumberOfCosmicClusters = cms.uint32(300),
    MergeSeedsCenterCut_B = cms.double(0.25),
    MergeSeedsCenterCut_A = cms.double(0.05),
    MergeSeedsDifferentHitsCut = cms.uint32(1),
    rphiStripRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
    MaximalBarrelImpactParameter = cms.double(0.2),
    doClusterCheck = cms.bool(True),
    stereoStripRecHits = cms.InputTag("siStripMatchedRecHits","stereoRecHit"),
    ClusterCollectionLabel = cms.InputTag("siStripClusters"),
    OuterSeedRecHitAccessUseStereo = cms.bool(True),
    MergeSeedsCenterCut_C = cms.double(0.4),
    MinimalReconstructedTransverseMomentum = cms.double(1.5),
    PhiRangeForDetIdLookupInRings = cms.double(0.5),
    Mode = cms.string('STRAIGHT-LINE'),
    RoadsLabel = cms.string('P5'),
    InnerSeedRecHitAccessMode = cms.string('STANDARD'),
    InnerSeedRecHitAccessUseStereo = cms.bool(True),
    OuterSeedRecHitAccessUseRPhi = cms.bool(True),
    MergeSeedsRadiusCut_B = cms.double(0.25),
    MergeSeedsRadiusCut_C = cms.double(0.4),
    matchedStripRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
    MergeSeedsRadiusCut_A = cms.double(0.05),
    InnerSeedRecHitAccessUseRPhi = cms.bool(True)
)


process.towerMakerWithHO = cms.EDFilter("CaloTowersCreator",
    MomEmDepth = cms.double(0),
    EBSumThreshold = cms.double(0.2),
    EBWeight = cms.double(1.0),
    hfInput = cms.InputTag("hfreco"),
    AllowMissingInputs = cms.untracked.bool(False),
    EESumThreshold = cms.double(0.45),
    HOThreshold = cms.double(1.1),
    HBThreshold = cms.double(0.9),
    EcutTower = cms.double(-1000.0),
    MomConstrMethod = cms.int32(0),
    HcalThreshold = cms.double(-1000.0),
    HF1Threshold = cms.double(1.2),
    HEDWeight = cms.double(1.0),
    EEWeight = cms.double(1.0),
    UseHO = cms.bool(True),
    HF1Weight = cms.double(1.0),
    MomHadDepth = cms.double(0),
    HOWeight = cms.double(1.0),
    HESWeight = cms.double(1.0),
    hbheInput = cms.InputTag("hbhereco"),
    HF2Weight = cms.double(1.0),
    HF2Threshold = cms.double(1.8),
    EEThreshold = cms.double(0.45),
    HESThreshold = cms.double(1.4),
    hoInput = cms.InputTag("horeco"),
    MomTotDepth = cms.double(0),
    HEDThreshold = cms.double(1.4),
    EBThreshold = cms.double(0.09),
    ecalInputs = cms.VInputTag(cms.InputTag("ecalRecHit","EcalRecHitsEB"), cms.InputTag("ecalRecHit","EcalRecHitsEE")),
    HBWeight = cms.double(1.0)
)


process.withLooseQuality = cms.EDFilter("AnalyticalTrackSelector",
    keepAllTracks = cms.bool(False),
    beamspot = cms.InputTag("offlineBeamSpot"),
    vtxTracks = cms.uint32(3),
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(True),
    vertices = cms.InputTag("pixelVertices"),
    qualityBit = cms.string('loose'),
    vtxNumber = cms.int32(-1),
    vtxChi2Prob = cms.double(0.01),
    minNumberLayers = cms.uint32(0),
    chi2n_par = cms.double(2.0),
    d0_par2 = cms.vdouble(0.55, 4.0),
    d0_par1 = cms.vdouble(0.55, 4.0),
    src = cms.InputTag("preFilterFirstStepTracks"),
    dz_par1 = cms.vdouble(0.65, 4.0),
    res_par = cms.vdouble(0.003, 0.01),
    dz_par2 = cms.vdouble(0.45, 4.0)
)


process.siStripClusters = cms.EDFilter("SiStripClusterizer",
    MaxHolesInCluster = cms.int32(0),
    ChannelThreshold = cms.double(2.0),
    DigiProducersList = cms.VPSet(cms.PSet(
        DigiLabel = cms.string('ZeroSuppressed'),
        DigiProducer = cms.string('siStripDigis')
    ), 
        cms.PSet(
            DigiLabel = cms.string('VirginRaw'),
            DigiProducer = cms.string('siStripZeroSuppression')
        ), 
        cms.PSet(
            DigiLabel = cms.string('ProcessedRaw'),
            DigiProducer = cms.string('siStripZeroSuppression')
        ), 
        cms.PSet(
            DigiLabel = cms.string('ScopeMode'),
            DigiProducer = cms.string('siStripZeroSuppression')
        )),
    ClusterMode = cms.string('ThreeThresholdClusterizer'),
    SeedThreshold = cms.double(3.0),
    SiStripQualityLabel = cms.string(''),
    ClusterThreshold = cms.double(5.0)
)


process.calotoweroptmakerWithHO = cms.EDFilter("CaloTowersCreator",
    MomEmDepth = cms.double(0.0),
    EBSumThreshold = cms.double(0.2),
    EBWeight = cms.double(1.0),
    hfInput = cms.InputTag("hfreco"),
    EESumThreshold = cms.double(0.45),
    HOThreshold = cms.double(0.5),
    HBGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    HBThreshold = cms.double(0.5),
    EcutTower = cms.double(-1000.0),
    EEWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    HcalThreshold = cms.double(-1000.0),
    HF2Weights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    HOWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    EEGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    HEDWeight = cms.double(1.0),
    MomConstrMethod = cms.int32(0),
    EEWeight = cms.double(1.0),
    UseHO = cms.bool(True),
    HBWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    HF1Weight = cms.double(1.0),
    HF2Grid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    HEDWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    HF1Grid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    MomHadDepth = cms.double(0.0),
    HOWeight = cms.double(1.0),
    HESWeight = cms.double(1.0),
    hbheInput = cms.InputTag("hbhereco"),
    HF2Weight = cms.double(1.0),
    HF2Threshold = cms.double(1.8),
    EEThreshold = cms.double(0.45),
    HESThreshold = cms.double(0.7),
    HF1Weights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    hoInput = cms.InputTag("horeco"),
    HF1Threshold = cms.double(1.2),
    HESGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    EBWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    MomTotDepth = cms.double(0.0),
    HESWeights = cms.untracked.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
    HEDThreshold = cms.double(0.5),
    EBThreshold = cms.double(0.09),
    HEDGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    ecalInputs = cms.VInputTag(cms.InputTag("ecalRecHit","EcalRecHitsEB"), cms.InputTag("ecalRecHit","EcalRecHitsEE")),
    HBWeight = cms.double(1.0),
    HOGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
    EBGrid = cms.untracked.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0)
)


process.MuonSeed = cms.EDFilter("MuonSeedGenerator",
    SMB_21 = cms.vdouble(0.918425, -0.141199, 0.0, 0.254515, -0.111848, 
        0.0),
    SMB_20 = cms.vdouble(0.861314, -0.16233, 0.0, 0.248879, -0.113879, 
        0.0),
    SMB_22 = cms.vdouble(1.308565, -0.701634, 0.0, -0.302861, 0.675785, 
        0.0),
    OL_2213 = cms.vdouble(0.563218, -0.493991, 0.0, 0.943776, -0.591751, 
        0.0),
    SME_11 = cms.vdouble(2.39479, -0.888663, 0.0, -4.604546, 3.623464, 
        0.0),
    SME_13 = cms.vdouble(0.398851, 0.028176, 0.0, 0.567015, 2.623232, 
        0.0),
    SMB_31 = cms.vdouble(0.398661, -0.024853, 0.0, 0.863324, -0.413048, 
        0.0),
    SME_32 = cms.vdouble(-0.021912, -0.008995, 0.0, -49.779764, 30.780972, 
        0.0),
    SME_31 = cms.vdouble(-0.588188, 0.316961, 0.0, -95.261732, 45.444051, 
        0.0),
    OL_1213 = cms.vdouble(0.960544, -0.75644, 0.0, 0.1636, 0.114178, 
        0.0),
    DT_13 = cms.vdouble(0.298842, 0.076531, -0.14293, 0.219923, -0.145026, 
        0.155638),
    DT_12 = cms.vdouble(0.176182, 0.058535, -0.090549, 0.202363, -0.203126, 
        0.222219),
    DT_14 = cms.vdouble(0.388423, 0.068698, -0.145925, 0.159515, 0.124299, 
        -0.133269),
    OL_1232 = cms.vdouble(0.162626, 0.000843, 0.0, 0.396271, 0.002791, 
        0.0),
    CSC_23 = cms.vdouble(-0.095236, 0.122061, -0.029852, -11.396689, 15.933598, 
        -4.267065),
    CSC_24 = cms.vdouble(-0.049769, 0.063087, -0.011029, -13.765978, 16.296143, 
        -4.241835),
    CSC_03 = cms.vdouble(0.498992, -0.086235, -0.025772, 2.761006, -2.667607, 
        0.72802),
    CSC_01 = cms.vdouble(0.155906, -0.000406, 0.0, 0.194022, -0.010181, 
        0.0),
    SMB_32 = cms.vdouble(0.421649, -0.111654, 0.0, -0.044613, 1.134858, 
        0.0),
    SMB_30 = cms.vdouble(0.399628, 0.014922, 0.0, 0.665622, 0.358439, 
        0.0),
    OL_2222 = cms.vdouble(0.087587, 0.005729, 0.0, 0.535169, -0.087675, 
        0.0),
    SMB_10 = cms.vdouble(1.160532, 0.148991, 0.0, 0.182785, -0.093776, 
        0.0),
    SMB_11 = cms.vdouble(1.289468, -0.139653, 0.0, 0.137191, 0.01217, 
        0.0),
    SMB_12 = cms.vdouble(1.923091, -0.913204, 0.0, 0.161556, 0.020215, 
        0.0),
    DT_23 = cms.vdouble(0.120647, 0.034743, -0.070855, 0.302427, -0.21417, 
        0.261012),
    DT_24 = cms.vdouble(0.189527, 0.037328, -0.088523, 0.251936, 0.032411, 
        0.010984),
    SME_21 = cms.vdouble(0.64895, -0.148762, 0.0, -5.07676, 6.284227, 
        0.0),
    SME_22 = cms.vdouble(-0.624708, 0.641043, 0.0, 32.581295, -19.604264, 
        0.0),
    CSC_34 = cms.vdouble(0.144321, -0.142283, 0.035636, 190.260708, -180.888643, 
        43.430395),
    CSC_02 = cms.vdouble(0.600235, -0.205683, 0.001113, 0.655625, -0.682129, 
        0.253916),
    SME_41 = cms.vdouble(-0.187116, 0.076415, 0.0, -58.552583, 27.933864, 
        0.0),
    SME_12 = cms.vdouble(-0.277294, 0.7616, 0.0, -0.243326, 1.446792, 
        0.0),
    DT_34 = cms.vdouble(0.049146, -0.003494, -0.010099, 0.672095, 0.36459, 
        -0.304346),
    CSC_14 = cms.vdouble(0.952517, -0.532733, 0.084601, 1.615881, -1.630744, 
        0.514139),
    OL_1222 = cms.vdouble(0.215915, 0.002556, 0.0, 0.313596, -0.021465, 
        0.0),
    CSC_13 = cms.vdouble(1.22495, -1.792358, 0.711378, 5.271848, -6.280625, 
        2.0142),
    CSC_12 = cms.vdouble(-0.363549, 0.569552, -0.173186, 7.777069, -10.203618, 
        3.478874),
    crackWindow = cms.double(0.04),
    crackEtas = cms.vdouble(0.2, 1.6, 1.7),
    CSCRecSegmentLabel = cms.InputTag("cscSegments"),
    EnableDTMeasurement = cms.bool(True),
    DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
    EnableCSCMeasurement = cms.bool(True)
)


process.calibrationEventsFilter = cms.EDFilter("TriggerTypeFilter",
    TriggerFedId = cms.int32(812),
    InputLabel = cms.string('source'),
    SelectedTriggerType = cms.int32(1)
)


process.hfreco = cms.EDFilter("HcalSimpleReconstructor",
    correctionPhaseNS = cms.double(10.0),
    digiLabel = cms.InputTag("hcalDigis"),
    samplesToAdd = cms.int32(8),
    Subdetector = cms.string('HF'),
    correctForTimeslew = cms.bool(True),
    correctForPhaseContainment = cms.bool(True),
    firstSample = cms.int32(1)
)


process.globalCombinedSeeds = cms.EDFilter("SeedCombiner",
    TripletCollection = cms.InputTag("globalSeedsFromTripletsWithVertices"),
    PairCollection = cms.InputTag("globalSeedsFromPairsWithVertices")
)


process.thStep = cms.EDFilter("VertexFilter",
    TrackAlgorithm = cms.string('iter3'),
    recVertices = cms.InputTag("pixelVertices"),
    TrackQualities = cms.vstring('loose', 
        'tight', 
        'highPurity'),
    DistRhoFromVertex = cms.double(0.1),
    DistZFromVertex = cms.double(0.1),
    recTracks = cms.InputTag("thWithMaterialTracks"),
    UseQuality = cms.bool(True),
    ChiCut = cms.double(130.0),
    VertexCut = cms.bool(True),
    MinHits = cms.int32(3)
)


process.lhcMuonSeedEndCapsOnly = cms.EDFilter("MuonSeedGenerator",
    SMB_21 = cms.vdouble(0.918425, -0.141199, 0.0, 0.254515, -0.111848, 
        0.0),
    SMB_20 = cms.vdouble(0.861314, -0.16233, 0.0, 0.248879, -0.113879, 
        0.0),
    SMB_22 = cms.vdouble(1.308565, -0.701634, 0.0, -0.302861, 0.675785, 
        0.0),
    OL_2213 = cms.vdouble(0.563218, -0.493991, 0.0, 0.943776, -0.591751, 
        0.0),
    SME_11 = cms.vdouble(2.39479, -0.888663, 0.0, -4.604546, 3.623464, 
        0.0),
    SME_13 = cms.vdouble(0.398851, 0.028176, 0.0, 0.567015, 2.623232, 
        0.0),
    SMB_31 = cms.vdouble(0.398661, -0.024853, 0.0, 0.863324, -0.413048, 
        0.0),
    SME_32 = cms.vdouble(-0.021912, -0.008995, 0.0, -49.779764, 30.780972, 
        0.0),
    SME_31 = cms.vdouble(-0.588188, 0.316961, 0.0, -95.261732, 45.444051, 
        0.0),
    OL_1213 = cms.vdouble(0.960544, -0.75644, 0.0, 0.1636, 0.114178, 
        0.0),
    crackEtas = cms.vdouble(0.2, 1.6, 1.7),
    DT_13 = cms.vdouble(0.298842, 0.076531, -0.14293, 0.219923, -0.145026, 
        0.155638),
    DT_12 = cms.vdouble(0.176182, 0.058535, -0.090549, 0.202363, -0.203126, 
        0.222219),
    DT_14 = cms.vdouble(0.388423, 0.068698, -0.145925, 0.159515, 0.124299, 
        -0.133269),
    OL_1232 = cms.vdouble(0.162626, 0.000843, 0.0, 0.396271, 0.002791, 
        0.0),
    CSC_23 = cms.vdouble(-0.095236, 0.122061, -0.029852, -11.396689, 15.933598, 
        -4.267065),
    CSC_24 = cms.vdouble(-0.049769, 0.063087, -0.011029, -13.765978, 16.296143, 
        -4.241835),
    CSC_03 = cms.vdouble(0.498992, -0.086235, -0.025772, 2.761006, -2.667607, 
        0.72802),
    CSC_01 = cms.vdouble(0.155906, -0.000406, 0.0, 0.194022, -0.010181, 
        0.0),
    SMB_32 = cms.vdouble(0.421649, -0.111654, 0.0, -0.044613, 1.134858, 
        0.0),
    SMB_30 = cms.vdouble(0.399628, 0.014922, 0.0, 0.665622, 0.358439, 
        0.0),
    OL_2222 = cms.vdouble(0.087587, 0.005729, 0.0, 0.535169, -0.087675, 
        0.0),
    crackWindow = cms.double(0.04),
    EnableDTMeasurement = cms.bool(False),
    SMB_10 = cms.vdouble(1.160532, 0.148991, 0.0, 0.182785, -0.093776, 
        0.0),
    SMB_11 = cms.vdouble(1.289468, -0.139653, 0.0, 0.137191, 0.01217, 
        0.0),
    SMB_12 = cms.vdouble(1.923091, -0.913204, 0.0, 0.161556, 0.020215, 
        0.0),
    DT_23 = cms.vdouble(0.120647, 0.034743, -0.070855, 0.302427, -0.21417, 
        0.261012),
    DT_24 = cms.vdouble(0.189527, 0.037328, -0.088523, 0.251936, 0.032411, 
        0.010984),
    SME_21 = cms.vdouble(0.64895, -0.148762, 0.0, -5.07676, 6.284227, 
        0.0),
    SME_22 = cms.vdouble(-0.624708, 0.641043, 0.0, 32.581295, -19.604264, 
        0.0),
    CSCRecSegmentLabel = cms.InputTag("cscSegments"),
    CSC_34 = cms.vdouble(0.144321, -0.142283, 0.035636, 190.260708, -180.888643, 
        43.430395),
    DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
    SME_41 = cms.vdouble(-0.187116, 0.076415, 0.0, -58.552583, 27.933864, 
        0.0),
    SME_12 = cms.vdouble(-0.277294, 0.7616, 0.0, -0.243326, 1.446792, 
        0.0),
    EnableCSCMeasurement = cms.bool(True),
    DT_34 = cms.vdouble(0.049146, -0.003494, -0.010099, 0.672095, 0.36459, 
        -0.304346),
    CSC_14 = cms.vdouble(0.952517, -0.532733, 0.084601, 1.615881, -1.630744, 
        0.514139),
    OL_1222 = cms.vdouble(0.215915, 0.002556, 0.0, 0.313596, -0.021465, 
        0.0),
    CSC_02 = cms.vdouble(0.600235, -0.205683, 0.001113, 0.655625, -0.682129, 
        0.253916),
    CSC_13 = cms.vdouble(1.22495, -1.792358, 0.711378, 5.271848, -6.280625, 
        2.0142),
    CSC_12 = cms.vdouble(-0.363549, 0.569552, -0.173186, 7.777069, -10.203618, 
        3.478874)
)


process.fourthTrackCandidates = cms.EDFilter("CkfTrackCandidateMaker",
    TransientInitialStateEstimatorParameters = cms.PSet(
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    SeedLabel = cms.string(''),
    useHitsSplitting = cms.bool(True),
    doSeedingRegionRebuilding = cms.bool(True),
    SeedProducer = cms.string('fourthPLSeeds'),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    TrajectoryBuilder = cms.string('fourthCkfTrajectoryBuilder'),
    TrajectoryCleaner = cms.string('TrajectoryCleanerBySharedHits')
)


process.combinatorialcosmicseedfinder = cms.EDFilter("CtfSpecialSeedGenerator",
    ErrorRescaling = cms.double(50.0),
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            originHalfLength = cms.double(15.9),
            originZPos = cms.double(0.0),
            originYPos = cms.double(0.0),
            ptMin = cms.double(0.9),
            originXPos = cms.double(0.0),
            originRadius = cms.double(0.2)
        ),
        ComponentName = cms.string('GlobalRegionProducer')
    ),
    UpperScintillatorParameters = cms.PSet(
        GlobalX = cms.double(0.0),
        GlobalY = cms.double(300.0),
        GlobalZ = cms.double(50.0),
        WidthInX = cms.double(100.0),
        LenghtInZ = cms.double(100.0)
    ),
    Charges = cms.vint32(-1),
    OrderedHitsFactoryPSets = cms.VPSet(cms.PSet(
        ComponentName = cms.string('GenericTripletGenerator'),
        LayerPSet = cms.PSet(
            TOB5 = cms.PSet(
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            TOB4 = cms.PSet(
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            TIB1 = cms.PSet(
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                TTRHBuilder = cms.string('WithTrackAngle')
            ),
            TOB6 = cms.PSet(
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            TOB1 = cms.PSet(
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                TTRHBuilder = cms.string('WithTrackAngle')
            ),
            TOB3 = cms.PSet(
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            TOB2 = cms.PSet(
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                TTRHBuilder = cms.string('WithTrackAngle')
            ),
            TEC = cms.PSet(
                useSimpleRphiHitsCleaner = cms.untracked.bool(True),
                minRing = cms.int32(5),
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                useRingSlector = cms.untracked.bool(False),
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                maxRing = cms.int32(7)
            ),
            TIB2 = cms.PSet(
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                TTRHBuilder = cms.string('WithTrackAngle')
            ),
            TIB3 = cms.PSet(
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            layerList = cms.vstring('TOB4+TOB5+TOB6', 
                'TOB3+TOB5+TOB6', 
                'TOB3+TOB4+TOB5', 
                'TOB2+TOB4+TOB5', 
                'TOB3+TOB4+TOB6', 
                'TOB2+TOB4+TOB6')
        ),
        PropagationDirection = cms.string('alongMomentum'),
        NavigationDirection = cms.string('outsideIn')
    ), 
        cms.PSet(
            ComponentName = cms.string('GenericPairGenerator'),
            LayerPSet = cms.PSet(
                TOB5 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TOB4 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TIB1 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TOB6 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TOB1 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TOB3 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TOB2 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TEC = cms.PSet(
                    useSimpleRphiHitsCleaner = cms.untracked.bool(True),
                    minRing = cms.int32(5),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(False),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(7)
                ),
                TIB2 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TIB3 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                layerList = cms.vstring('TEC1_pos+TEC2_pos', 
                    'TEC2_pos+TEC3_pos', 
                    'TEC3_pos+TEC4_pos', 
                    'TEC4_pos+TEC5_pos', 
                    'TEC5_pos+TEC6_pos', 
                    'TEC6_pos+TEC7_pos', 
                    'TEC7_pos+TEC8_pos', 
                    'TEC8_pos+TEC9_pos')
            ),
            PropagationDirection = cms.string('alongMomentum'),
            NavigationDirection = cms.string('outsideIn')
        ), 
        cms.PSet(
            ComponentName = cms.string('GenericTripletGenerator'),
            LayerPSet = cms.PSet(
                TOB5 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TOB4 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TIB1 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TOB6 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TOB1 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TOB3 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TOB2 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TEC = cms.PSet(
                    useSimpleRphiHitsCleaner = cms.untracked.bool(True),
                    minRing = cms.int32(5),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(False),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(7)
                ),
                TIB2 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TIB3 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                layerList = cms.vstring('TIB1+TIB2+TIB3')
            ),
            PropagationDirection = cms.string('oppositeToMomentum'),
            NavigationDirection = cms.string('insideOut')
        )),
    MaxNumberOfCosmicClusters = cms.uint32(300),
    UseScintillatorsConstraint = cms.bool(True),
    SetMomentum = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    LowerScintillatorParameters = cms.PSet(
        GlobalX = cms.double(0.0),
        GlobalY = cms.double(-100.0),
        GlobalZ = cms.double(50.0),
        WidthInX = cms.double(100.0),
        LenghtInZ = cms.double(100.0)
    ),
    SeedsFromPositiveY = cms.bool(True),
    doClusterCheck = cms.bool(True),
    SeedMomentum = cms.double(5.0),
    maxSeeds = cms.int32(10000),
    CheckHitsAreOnDifferentLayers = cms.bool(False),
    ClusterCollectionLabel = cms.InputTag("siStripClusters"),
    requireBOFF = cms.bool(False)
)


process.cosmictrackfinderP5 = cms.EDFilter("CosmicTrackFinder",
    TrajInEvents = cms.bool(True),
    MinHits = cms.int32(4),
    HitProducer = cms.string('siStripRecHits'),
    pixelRecHits = cms.InputTag("siPixelRecHits"),
    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
    stereorecHits = cms.InputTag("siStripMatchedRecHits","stereoRecHit"),
    Chi2Cut = cms.double(30.0),
    TTRHBuilder = cms.string('WithTrackAngle'),
    rphirecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
    debug = cms.untracked.bool(True),
    GeometricStructure = cms.untracked.string('STANDARD'),
    cosmicSeeds = cms.InputTag("cosmicseedfinderP5")
)


process.rsTrackCandidates = cms.EDFilter("RoadSearchTrackCandidateMaker",
    NumHitCut = cms.int32(5),
    InitialVertexErrorXY = cms.double(0.2),
    HitChi2Cut = cms.double(30.0),
    StraightLineNoBeamSpotCloud = cms.bool(False),
    nFoundMin = cms.int32(4),
    MinimumChunkLength = cms.int32(7),
    TTRHBuilder = cms.string('WithTrackAngle'),
    CosmicTrackMerging = cms.bool(False),
    MeasurementTrackerName = cms.string(''),
    CloudProducer = cms.InputTag("roadSearchClouds"),
    CosmicSeedPt = cms.double(5.0),
    SplitMatchedHits = cms.bool(False)
)


process.ckfTrackCandidatesBeamHaloMuon = cms.EDFilter("CkfTrackCandidateMaker",
    TransientInitialStateEstimatorParameters = cms.PSet(
        propagatorAlongTISE = cms.string('BeamHaloPropagatorAlong'),
        propagatorOppositeTISE = cms.string('BeamHaloPropagatorOpposite')
    ),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    SeedLabel = cms.string(''),
    useHitsSplitting = cms.bool(True),
    doSeedingRegionRebuilding = cms.bool(True),
    SeedProducer = cms.string('combinatorialbeamhaloseedfinder'),
    NavigationSchool = cms.string('BeamHaloNavigationSchool'),
    TrajectoryBuilder = cms.string('CkfTrajectoryBuilderBH'),
    TrajectoryCleaner = cms.string('TrajectoryCleanerBySharedHits')
)


process.fourthPixelRecHits = cms.EDFilter("SiPixelRecHitConverter",
    eff_charge_cut_lowY = cms.untracked.double(0.0),
    eff_charge_cut_lowX = cms.untracked.double(0.0),
    src = cms.InputTag("fourthClusters"),
    eff_charge_cut_highX = cms.untracked.double(1.0),
    eff_charge_cut_highY = cms.untracked.double(1.0),
    size_cutY = cms.untracked.double(3.0),
    size_cutX = cms.untracked.double(3.0),
    CPE = cms.string('PixelCPEGeneric'),
    VerboseLevel = cms.untracked.int32(0),
    TanLorentzAnglePerTesla = cms.double(0.106),
    Alpha2Order = cms.bool(True),
    speed = cms.int32(0)
)


process.CosmicMuonSeedNoDriftBarrelOnly = cms.EDFilter("CosmicMuonSeedGenerator",
    DTRecSegmentLabel = cms.untracked.InputTag("dt4DSegmentsNoDrift"),
    CSCRecSegmentLabel = cms.untracked.InputTag("cscSegments"),
    EnableDTMeasurement = cms.untracked.bool(True),
    MaxCSCChi2 = cms.double(300.0),
    MaxDTChi2 = cms.double(300.0),
    MaxSeeds = cms.int32(10),
    EnableCSCMeasurement = cms.untracked.bool(False)
)


process.dtRecoFilter = cms.EDFilter("DTRecoEventFilter",
    recHits4DLabel = cms.string('dt4DSegments'),
    dtDigiLabel = cms.InputTag("dtunpacker")
)


process.thClusters = cms.EDFilter("TrackClusterRemover",
    oldClusterRemovalInfo = cms.InputTag("secClusters"),
    trajectories = cms.InputTag("secStep"),
    pixelClusters = cms.InputTag("secClusters"),
    Common = cms.PSet(
        maxChi2 = cms.double(30.0)
    ),
    stripClusters = cms.InputTag("secClusters")
)


process.ckfInOutTracksFromConversions = cms.EDFilter("TrackProducerWithSCAssociation",
    src = cms.InputTag("conversionTrackCandidates","inOutTracksFromConversions"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    producer = cms.string('conversionTrackCandidates'),
    Fitter = cms.string('KFFittingSmootherForInOut'),
    useHitsSplitting = cms.bool(False),
    trackCandidateSCAssociationCollection = cms.string('inOutTrackCandidateSCAssociationCollection'),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    AlgorithmName = cms.string('undefAlgorithm'),
    ComponentName = cms.string('ckfInOutTracksFromConversions'),
    Propagator = cms.string('alongMomElePropagator'),
    recoTrackSCAssociationCollection = cms.string('inOutTrackSCAssociationCollection')
)


process.CosmicMuonSeedEndCapsOnly = cms.EDFilter("CosmicMuonSeedGenerator",
    DTRecSegmentLabel = cms.untracked.InputTag("dt4DSegments"),
    CSCRecSegmentLabel = cms.untracked.InputTag("cscSegments"),
    EnableDTMeasurement = cms.untracked.bool(False),
    MaxCSCChi2 = cms.double(300.0),
    MaxDTChi2 = cms.double(300.0),
    MaxSeeds = cms.int32(10),
    EnableCSCMeasurement = cms.untracked.bool(True)
)


process.combinedP5SeedsForCTF = cms.EDFilter("SeedCombiner",
    TripletCollection = cms.InputTag("simpleCosmicBONSeeds"),
    PairCollection = cms.InputTag("combinatorialcosmicseedfinderP5")
)


process.mergeFirstTwoSteps = cms.EDFilter("SimpleTrackListMerger",
    ShareFrac = cms.double(0.66),
    newQuality = cms.string('confirmed'),
    promoteTrackQuality = cms.bool(True),
    MinPT = cms.double(0.05),
    Epsilon = cms.double(-0.001),
    MaxNormalizedChisq = cms.double(1000.0),
    MinFound = cms.int32(3),
    TrackProducer2 = cms.string('secStep'),
    TrackProducer1 = cms.string('firstStepTracksWithQuality')
)


process.siStripZeroSuppression = cms.EDFilter("SiStripZeroSuppression",
    RawDigiProducersList = cms.VPSet(cms.PSet(
        RawDigiProducer = cms.string('siStripDigis'),
        RawDigiLabel = cms.string('VirginRaw')
    ), 
        cms.PSet(
            RawDigiProducer = cms.string('siStripDigis'),
            RawDigiLabel = cms.string('ProcessedRaw')
        ), 
        cms.PSet(
            RawDigiProducer = cms.string('siStripDigis'),
            RawDigiLabel = cms.string('ScopeMode')
        )),
    FEDalgorithm = cms.uint32(4),
    CommonModeNoiseSubtractionMode = cms.string('Median'),
    CutToAvoidSignal = cms.double(3.0),
    ZeroSuppressionMode = cms.string('SiStripFedZeroSuppression')
)


process.thTrackCandidates = cms.EDFilter("CkfTrackCandidateMaker",
    TransientInitialStateEstimatorParameters = cms.PSet(
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    SeedLabel = cms.string(''),
    useHitsSplitting = cms.bool(True),
    doSeedingRegionRebuilding = cms.bool(True),
    SeedProducer = cms.string('thPLSeeds'),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    TrajectoryBuilder = cms.string('thCkfTrajectoryBuilder'),
    TrajectoryCleaner = cms.string('TrajectoryCleanerBySharedHits')
)


process.combinatorialcosmicseedfinderP5 = cms.EDFilter("CtfSpecialSeedGenerator",
    ErrorRescaling = cms.double(50.0),
    RegionFactoryPSet = cms.PSet(
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            originHalfLength = cms.double(15.9),
            originZPos = cms.double(0.0),
            originYPos = cms.double(0.0),
            ptMin = cms.double(0.9),
            originXPos = cms.double(0.0),
            originRadius = cms.double(0.2)
        ),
        ComponentName = cms.string('GlobalRegionProducer')
    ),
    UpperScintillatorParameters = cms.PSet(
        GlobalX = cms.double(0.0),
        GlobalY = cms.double(300.0),
        GlobalZ = cms.double(50.0),
        WidthInX = cms.double(100.0),
        LenghtInZ = cms.double(100.0)
    ),
    Charges = cms.vint32(-1),
    OrderedHitsFactoryPSets = cms.VPSet(cms.PSet(
        ComponentName = cms.string('GenericTripletGenerator'),
        LayerPSet = cms.PSet(
            TOB5 = cms.PSet(
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            TOB4 = cms.PSet(
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            TIB1 = cms.PSet(
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                TTRHBuilder = cms.string('WithTrackAngle')
            ),
            TOB6 = cms.PSet(
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            TOB1 = cms.PSet(
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                TTRHBuilder = cms.string('WithTrackAngle')
            ),
            TOB3 = cms.PSet(
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            TOB2 = cms.PSet(
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                TTRHBuilder = cms.string('WithTrackAngle')
            ),
            TEC = cms.PSet(
                useSimpleRphiHitsCleaner = cms.untracked.bool(True),
                minRing = cms.int32(5),
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                useRingSlector = cms.untracked.bool(False),
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                maxRing = cms.int32(7)
            ),
            TIB2 = cms.PSet(
                matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                TTRHBuilder = cms.string('WithTrackAngle')
            ),
            TIB3 = cms.PSet(
                TTRHBuilder = cms.string('WithTrackAngle'),
                rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
            ),
            layerList = cms.vstring('TOB4+TOB5+TOB6', 
                'TOB3+TOB5+TOB6', 
                'TOB3+TOB4+TOB5', 
                'TOB2+TOB4+TOB5', 
                'TOB3+TOB4+TOB6', 
                'TOB2+TOB4+TOB6')
        ),
        PropagationDirection = cms.string('alongMomentum'),
        NavigationDirection = cms.string('outsideIn')
    ), 
        cms.PSet(
            ComponentName = cms.string('GenericPairGenerator'),
            LayerPSet = cms.PSet(
                TOB5 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TOB4 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TIB1 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TOB6 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TOB1 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TOB3 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                TOB2 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TEC = cms.PSet(
                    useSimpleRphiHitsCleaner = cms.untracked.bool(True),
                    minRing = cms.int32(5),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(False),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(7)
                ),
                TIB2 = cms.PSet(
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    TTRHBuilder = cms.string('WithTrackAngle')
                ),
                TIB3 = cms.PSet(
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
                ),
                layerList = cms.vstring('TOB5+TOB6', 
                    'TOB4+TOB5')
            ),
            PropagationDirection = cms.string('alongMomentum'),
            NavigationDirection = cms.string('outsideIn')
        ), 
        cms.PSet(
            ComponentName = cms.string('GenericPairGenerator'),
            LayerPSet = cms.PSet(
                layerList = cms.vstring('TEC1_pos+TEC2_pos', 
                    'TEC2_pos+TEC3_pos', 
                    'TEC3_pos+TEC4_pos', 
                    'TEC4_pos+TEC5_pos', 
                    'TEC5_pos+TEC6_pos', 
                    'TEC6_pos+TEC7_pos', 
                    'TEC7_pos+TEC8_pos', 
                    'TEC8_pos+TEC9_pos'),
                TEC = cms.PSet(
                    minRing = cms.int32(5),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(True),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(7)
                )
            ),
            PropagationDirection = cms.string('alongMomentum'),
            NavigationDirection = cms.string('outsideIn')
        ), 
        cms.PSet(
            ComponentName = cms.string('GenericPairGenerator'),
            LayerPSet = cms.PSet(
                layerList = cms.vstring('TEC1_pos+TEC2_pos', 
                    'TEC2_pos+TEC3_pos', 
                    'TEC3_pos+TEC4_pos', 
                    'TEC4_pos+TEC5_pos', 
                    'TEC5_pos+TEC6_pos', 
                    'TEC6_pos+TEC7_pos', 
                    'TEC7_pos+TEC8_pos', 
                    'TEC8_pos+TEC9_pos'),
                TEC = cms.PSet(
                    minRing = cms.int32(5),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(True),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(7)
                )
            ),
            PropagationDirection = cms.string('alongMomentum'),
            NavigationDirection = cms.string('insideOut')
        ), 
        cms.PSet(
            ComponentName = cms.string('GenericPairGenerator'),
            LayerPSet = cms.PSet(
                layerList = cms.vstring('TEC1_neg+TEC2_neg', 
                    'TEC2_neg+TEC3_neg', 
                    'TEC3_neg+TEC4_neg', 
                    'TEC4_neg+TEC5_neg', 
                    'TEC5_neg+TEC6_neg', 
                    'TEC6_neg+TEC7_neg', 
                    'TEC7_neg+TEC8_neg', 
                    'TEC8_neg+TEC9_neg'),
                TEC = cms.PSet(
                    minRing = cms.int32(5),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(True),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(7)
                )
            ),
            PropagationDirection = cms.string('alongMomentum'),
            NavigationDirection = cms.string('outsideIn')
        ), 
        cms.PSet(
            ComponentName = cms.string('GenericPairGenerator'),
            LayerPSet = cms.PSet(
                layerList = cms.vstring('TEC1_neg+TEC2_neg', 
                    'TEC2_neg+TEC3_neg', 
                    'TEC3_neg+TEC4_neg', 
                    'TEC4_neg+TEC5_neg', 
                    'TEC5_neg+TEC6_neg', 
                    'TEC6_neg+TEC7_neg', 
                    'TEC7_neg+TEC8_neg', 
                    'TEC8_neg+TEC9_neg'),
                TEC = cms.PSet(
                    minRing = cms.int32(5),
                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                    useRingSlector = cms.untracked.bool(True),
                    TTRHBuilder = cms.string('WithTrackAngle'),
                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                    maxRing = cms.int32(7)
                )
            ),
            PropagationDirection = cms.string('alongMomentum'),
            NavigationDirection = cms.string('insideOut')
        )),
    MaxNumberOfCosmicClusters = cms.uint32(300),
    UseScintillatorsConstraint = cms.bool(False),
    SetMomentum = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    LowerScintillatorParameters = cms.PSet(
        GlobalX = cms.double(0.0),
        GlobalY = cms.double(-100.0),
        GlobalZ = cms.double(50.0),
        WidthInX = cms.double(100.0),
        LenghtInZ = cms.double(100.0)
    ),
    SeedsFromPositiveY = cms.bool(True),
    doClusterCheck = cms.bool(True),
    SeedMomentum = cms.double(5.0),
    maxSeeds = cms.int32(10000),
    CheckHitsAreOnDifferentLayers = cms.bool(False),
    ClusterCollectionLabel = cms.InputTag("siStripClusters"),
    requireBOFF = cms.bool(True)
)


process.cosmicseedfinderP5 = cms.EDFilter("CosmicSeedGenerator",
    maxSeeds = cms.int32(10000),
    originHalfLength = cms.double(90.0),
    originZPosition = cms.double(0.0),
    GeometricStructure = cms.untracked.string('STANDARD'),
    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
    MaxNumberOfCosmicClusters = cms.uint32(300),
    SeedPt = cms.double(5.0),
    HitsForSeeds = cms.untracked.string('pairs'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    ptMin = cms.double(0.9),
    rphirecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
    doClusterCheck = cms.bool(True),
    originRadius = cms.double(150.0),
    ClusterCollectionLabel = cms.InputTag("siStripClusters"),
    stereorecHits = cms.InputTag("siStripMatchedRecHits","stereoRecHit")
)


process.lhcMuonSeedBarrelOnly = cms.EDFilter("MuonSeedGenerator",
    SMB_21 = cms.vdouble(0.918425, -0.141199, 0.0, 0.254515, -0.111848, 
        0.0),
    SMB_20 = cms.vdouble(0.861314, -0.16233, 0.0, 0.248879, -0.113879, 
        0.0),
    SMB_22 = cms.vdouble(1.308565, -0.701634, 0.0, -0.302861, 0.675785, 
        0.0),
    OL_2213 = cms.vdouble(0.563218, -0.493991, 0.0, 0.943776, -0.591751, 
        0.0),
    SME_11 = cms.vdouble(2.39479, -0.888663, 0.0, -4.604546, 3.623464, 
        0.0),
    SME_13 = cms.vdouble(0.398851, 0.028176, 0.0, 0.567015, 2.623232, 
        0.0),
    SMB_31 = cms.vdouble(0.398661, -0.024853, 0.0, 0.863324, -0.413048, 
        0.0),
    SME_32 = cms.vdouble(-0.021912, -0.008995, 0.0, -49.779764, 30.780972, 
        0.0),
    SME_31 = cms.vdouble(-0.588188, 0.316961, 0.0, -95.261732, 45.444051, 
        0.0),
    OL_1213 = cms.vdouble(0.960544, -0.75644, 0.0, 0.1636, 0.114178, 
        0.0),
    crackEtas = cms.vdouble(0.2, 1.6, 1.7),
    DT_13 = cms.vdouble(0.298842, 0.076531, -0.14293, 0.219923, -0.145026, 
        0.155638),
    DT_12 = cms.vdouble(0.176182, 0.058535, -0.090549, 0.202363, -0.203126, 
        0.222219),
    DT_14 = cms.vdouble(0.388423, 0.068698, -0.145925, 0.159515, 0.124299, 
        -0.133269),
    OL_1232 = cms.vdouble(0.162626, 0.000843, 0.0, 0.396271, 0.002791, 
        0.0),
    CSC_23 = cms.vdouble(-0.095236, 0.122061, -0.029852, -11.396689, 15.933598, 
        -4.267065),
    CSC_24 = cms.vdouble(-0.049769, 0.063087, -0.011029, -13.765978, 16.296143, 
        -4.241835),
    CSC_03 = cms.vdouble(0.498992, -0.086235, -0.025772, 2.761006, -2.667607, 
        0.72802),
    CSC_01 = cms.vdouble(0.155906, -0.000406, 0.0, 0.194022, -0.010181, 
        0.0),
    SMB_32 = cms.vdouble(0.421649, -0.111654, 0.0, -0.044613, 1.134858, 
        0.0),
    SMB_30 = cms.vdouble(0.399628, 0.014922, 0.0, 0.665622, 0.358439, 
        0.0),
    OL_2222 = cms.vdouble(0.087587, 0.005729, 0.0, 0.535169, -0.087675, 
        0.0),
    crackWindow = cms.double(0.04),
    EnableDTMeasurement = cms.bool(True),
    SMB_10 = cms.vdouble(1.160532, 0.148991, 0.0, 0.182785, -0.093776, 
        0.0),
    SMB_11 = cms.vdouble(1.289468, -0.139653, 0.0, 0.137191, 0.01217, 
        0.0),
    SMB_12 = cms.vdouble(1.923091, -0.913204, 0.0, 0.161556, 0.020215, 
        0.0),
    DT_23 = cms.vdouble(0.120647, 0.034743, -0.070855, 0.302427, -0.21417, 
        0.261012),
    DT_24 = cms.vdouble(0.189527, 0.037328, -0.088523, 0.251936, 0.032411, 
        0.010984),
    SME_21 = cms.vdouble(0.64895, -0.148762, 0.0, -5.07676, 6.284227, 
        0.0),
    SME_22 = cms.vdouble(-0.624708, 0.641043, 0.0, 32.581295, -19.604264, 
        0.0),
    CSCRecSegmentLabel = cms.InputTag("cscSegments"),
    CSC_34 = cms.vdouble(0.144321, -0.142283, 0.035636, 190.260708, -180.888643, 
        43.430395),
    DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
    SME_41 = cms.vdouble(-0.187116, 0.076415, 0.0, -58.552583, 27.933864, 
        0.0),
    SME_12 = cms.vdouble(-0.277294, 0.7616, 0.0, -0.243326, 1.446792, 
        0.0),
    EnableCSCMeasurement = cms.bool(False),
    DT_34 = cms.vdouble(0.049146, -0.003494, -0.010099, 0.672095, 0.36459, 
        -0.304346),
    CSC_14 = cms.vdouble(0.952517, -0.532733, 0.084601, 1.615881, -1.630744, 
        0.514139),
    OL_1222 = cms.vdouble(0.215915, 0.002556, 0.0, 0.313596, -0.021465, 
        0.0),
    CSC_02 = cms.vdouble(0.600235, -0.205683, 0.001113, 0.655625, -0.682129, 
        0.253916),
    CSC_13 = cms.vdouble(1.22495, -1.792358, 0.711378, 5.271848, -6.280625, 
        2.0142),
    CSC_12 = cms.vdouble(-0.363549, 0.569552, -0.173186, 7.777069, -10.203618, 
        3.478874)
)


process.roadSearchCloudsP5 = cms.EDFilter("RoadSearchCloudMaker",
    MinimalFractionOfUsedLayersPerCloud = cms.double(0.3),
    pixelRecHits = cms.InputTag("siPixelRecHits"),
    MergingFraction = cms.double(0.8),
    MaxDetHitsInCloudPerDetId = cms.uint32(32),
    SeedProducer = cms.InputTag("roadSearchSeedsP5"),
    DoCloudCleaning = cms.bool(True),
    IncreaseMaxNumberOfConsecutiveMissedLayersPerCloud = cms.uint32(0),
    rphiStripRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
    UseStereoRecHits = cms.bool(True),
    ZPhiRoadSize = cms.double(0.06),
    MaximalFractionOfConsecutiveMissedLayersPerCloud = cms.double(0.35),
    stereoStripRecHits = cms.InputTag("siStripMatchedRecHits","stereoRecHit"),
    MaximalFractionOfMissedLayersPerCloud = cms.double(0.8),
    scalefactorRoadSeedWindow = cms.double(150),
    UsePixelsinRS = cms.bool(True),
    IncreaseMaxNumberOfMissedLayersPerCloud = cms.uint32(0),
    RoadsLabel = cms.string('P5'),
    MaxRecHitsInCloud = cms.int32(100),
    UseRphiRecHits = cms.bool(True),
    StraightLineNoBeamSpotCloud = cms.bool(True),
    RPhiRoadSize = cms.double(5.0),
    matchedStripRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
    MinimumHalfRoad = cms.double(3.3)
)


process.rsTrackCandidatesP5 = cms.EDFilter("RoadSearchTrackCandidateMaker",
    NumHitCut = cms.int32(4),
    InitialVertexErrorXY = cms.double(0.2),
    HitChi2Cut = cms.double(30.0),
    StraightLineNoBeamSpotCloud = cms.bool(True),
    nFoundMin = cms.int32(2),
    MinimumChunkLength = cms.int32(2),
    TTRHBuilder = cms.string('WithTrackAngle'),
    CosmicTrackMerging = cms.bool(True),
    MeasurementTrackerName = cms.string(''),
    CloudProducer = cms.InputTag("roadSearchCloudsP5"),
    CosmicSeedPt = cms.double(5.0),
    SplitMatchedHits = cms.bool(True)
)


process.ckfOutInTracksFromConversions = cms.EDFilter("TrackProducerWithSCAssociation",
    src = cms.InputTag("conversionTrackCandidates","outInTracksFromConversions"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    producer = cms.string('conversionTrackCandidates'),
    Fitter = cms.string('KFFitterForOutIn'),
    useHitsSplitting = cms.bool(False),
    trackCandidateSCAssociationCollection = cms.string('outInTrackCandidateSCAssociationCollection'),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    AlgorithmName = cms.string('undefAlgorithm'),
    ComponentName = cms.string('ckfOutInTracksFromConversions'),
    Propagator = cms.string('alongMomElePropagator'),
    recoTrackSCAssociationCollection = cms.string('outInTrackSCAssociationCollection')
)


process.siStripElectronToTrackAssociator = cms.EDFilter("SiStripElectronAssociator",
    siStripElectronCollection = cms.string(''),
    trackCollection = cms.string(''),
    electronsLabel = cms.string('siStripElectrons'),
    siStripElectronProducer = cms.string('siStripElectrons'),
    trackProducer = cms.string('egammaCTFFinalFitWithMaterial')
)


process.newCombinedSeeds = cms.EDFilter("SeedCombiner",
    TripletCollection = cms.InputTag("newSeedFromTriplets"),
    PairCollection = cms.InputTag("newSeedFromPairs")
)


process.secPixelRecHits = cms.EDFilter("SiPixelRecHitConverter",
    eff_charge_cut_lowY = cms.untracked.double(0.0),
    eff_charge_cut_lowX = cms.untracked.double(0.0),
    src = cms.InputTag("secClusters"),
    eff_charge_cut_highX = cms.untracked.double(1.0),
    eff_charge_cut_highY = cms.untracked.double(1.0),
    size_cutY = cms.untracked.double(3.0),
    size_cutX = cms.untracked.double(3.0),
    CPE = cms.string('PixelCPEGeneric'),
    VerboseLevel = cms.untracked.int32(0),
    TanLorentzAnglePerTesla = cms.double(0.106),
    Alpha2Order = cms.bool(True),
    speed = cms.int32(0)
)


process.siPixelRecHits = cms.EDFilter("SiPixelRecHitConverter",
    eff_charge_cut_lowY = cms.untracked.double(0.0),
    eff_charge_cut_lowX = cms.untracked.double(0.0),
    src = cms.InputTag("siPixelClusters"),
    eff_charge_cut_highX = cms.untracked.double(1.0),
    eff_charge_cut_highY = cms.untracked.double(1.0),
    size_cutY = cms.untracked.double(3.0),
    size_cutX = cms.untracked.double(3.0),
    CPE = cms.string('PixelCPEGeneric'),
    VerboseLevel = cms.untracked.int32(0),
    TanLorentzAnglePerTesla = cms.double(0.106),
    Alpha2Order = cms.bool(True),
    speed = cms.int32(0)
)


process.dtOfflineOccupancy = cms.EDAnalyzer("DTOfflineOccupancy",
    dtRecHitLabel = cms.InputTag("dt1DRecHits"),
    dtRecHit4DLabel = cms.InputTag("dt4DSegments"),
    rootFileName = cms.untracked.string('DTOfflineOccupancy_splash.root'),
    mode = cms.untracked.string(''),
    dtDigiLabel = cms.InputTag("dtunpacker")
)


process.tracksBeamHaloMuon = cms.Sequence(process.combinatorialbeamhaloseedfinder*process.ckfTrackCandidatesBeamHaloMuon*process.ctfWithMaterialTracksBeamHaloMuon)


process.STAmuontrackingforcosmics = cms.Sequence(process.CosmicMuonSeed*process.cosmicMuons)


process.allmuonsBarrelOnly = cms.Sequence(process.muonsBarrelOnly*process.STAMuonsBarrelOnly*process.GLBMuonsBarrelOnly)


process.hcalLocalRecoSequence = cms.Sequence(process.hbhereco+process.hfreco+process.horeco)


process.fourthStep = cms.Sequence(process.fourthClusters*process.fourthPixelRecHits*process.fourthStripRecHits*process.fourthPLSeeds*process.fourthTrackCandidates*process.fourthWithMaterialTracks)


process.secondStep = cms.Sequence(process.secClusters*process.secPixelRecHits*process.secStripRecHits*process.secTriplets*process.secTrackCandidates*process.secWithMaterialTracks*process.secStep)


process.doAlldEdXEstimatorsCTF = cms.Sequence(process.dedxTruncated40CTF+process.dedxMedianCTF+process.dedxHarmonic2CTF)


process.ecalLocalRecoSequence = cms.Sequence(process.ecalFixedAlphaBetaFitUncalibRecHit*process.ecalWeightUncalibRecHit*process.ecalRecHit+process.ecalPreshowerRecHit)


process.calolocalreco = cms.Sequence(process.ecalLocalRecoSequence+process.hcalLocalRecoSequence)


process.csclocalreco = cms.Sequence(process.csc2DRecHits*process.cscSegments)


process.allmuonsEndCapsOnly = cms.Sequence(process.muonsEndCapsOnly*process.STAMuonsEndCapsOnly*process.GLBMuonsEndCapsOnly)


process.muoncosmicreco = cms.Sequence(process.CosmicMuonSeed*process.cosmicMuons*process.globalCosmicMuons*process.muonsFromCosmics)


process.tracksWithQuality = cms.Sequence(process.withLooseQuality*process.withTightQuality*process.firstStepTracksWithQuality)


process.cosmicClusteringSequence = cms.Sequence(process.cosmicBasicClusters*process.cosmicSuperClusters)


process.dtlocalrecoNoDrift = cms.Sequence(process.dt1DRecHitsNoDrift*process.dt4DSegmentsNoDrift)


process.allmuons = cms.Sequence(process.muons*process.STAMuons*process.TKMuons*process.GLBMuons)


process.doAlldEdXEstimatorsRS = cms.Sequence(process.dedxTruncated40RS+process.dedxMedianRS+process.dedxHarmonic2RS)


process.dtlocalreco = cms.Sequence(process.dt1DRecHits*process.dt4DSegments)


process.rstracksP5 = cms.Sequence(process.roadSearchSeedsP5*process.roadSearchCloudsP5*process.rsTrackCandidatesP5*process.rsWithMaterialTracksP5)


process.pixelMatchGsfElectronSequence = cms.Sequence(process.electronPixelSeeds*process.egammaCkfTrackCandidates*process.pixelMatchGsfFit*process.pixelMatchGsfElectrons)


process.lhcMuonEndCapsOnly = cms.Sequence(process.lhcMuonSeedEndCapsOnly*process.lhcStandAloneMuonsEndCapsOnly)


process.recoCaloTowersGR = cms.Sequence(process.towerMaker+process.towerMakerWithHO)


process.ctftracksP5 = cms.Sequence(process.combinatorialcosmicseedfinderP5*process.simpleCosmicBONSeeds*process.combinedP5SeedsForCTF*process.ckfTrackCandidatesP5*process.ctfWithMaterialTracksP5)


process.muontrackingforcosmics = cms.Sequence(process.STAmuontrackingforcosmics*process.globalCosmicMuons)


process.striptrackerlocalreco = cms.Sequence(process.siStripZeroSuppression*process.siStripClusters*process.siStripMatchedRecHits)


process.muIsoDeposits_ParamGlobalMuons = cms.Sequence(process.muParamGlobalIsoDepositTk+process.muParamGlobalIsoDepositCalByAssociatorTowers+process.muParamGlobalIsoDepositJets)


process.photonIDSequence = cms.Sequence(process.PhotonIDProd)


process.muonlocalreco = cms.Sequence(process.dtlocalreco+process.csclocalreco+process.rpcRecHits)


process.trackCollectionMerging = cms.Sequence(process.mergeFirstTwoSteps*process.generalTracks)


process.STAmuonrecoforcosmics = cms.Sequence(process.STAmuontrackingforcosmics*process.STAMuons)


process.dtlocalreco_with_2DSegments = cms.Sequence(process.dt1DRecHits*process.dt2DSegments*process.dt4DSegments)


process.STAmuontrackingforcosmics1LegBarrelOnly = cms.Sequence(process.CosmicMuonSeedBarrelOnly*process.cosmicMuons1LegBarrelOnly)


process.muontracking = cms.Sequence(process.MuonSeed*process.standAloneMuons*process.globalMuons)


process.metreco = cms.Sequence(process.met+process.metNoHF+process.metHO+process.metNoHFHO+process.calotoweroptmaker+process.metOpt+process.metOptNoHF+process.calotoweroptmakerWithHO+process.metOptHO+process.metOptNoHFHO+process.htMetSC5+process.htMetSC7+process.htMetKT4+process.htMetKT6+process.htMetIC5)


process.muonlocalreco_with_2DSegments = cms.Sequence(process.dtlocalreco_with_2DSegments+process.csclocalreco+process.rpcRecHits)


process.lhcMuonBarrelOnly = cms.Sequence(process.lhcMuonSeedBarrelOnly*process.lhcStandAloneMuonsBarrelOnly)


process.ckfTracksFromConversions = cms.Sequence(process.conversionTrackCandidates*process.ckfOutInTracksFromConversions*process.ckfInOutTracksFromConversions)


process.doAlldEdXEstimatorsCosmicTF = cms.Sequence(process.dedxTruncated40CosmicTF+process.dedxMedianCosmicTF+process.dedxHarmonic2CosmicTF)


process.rstracks = cms.Sequence(process.roadSearchSeeds*process.roadSearchClouds*process.rsTrackCandidates*process.rsWithMaterialTracks)


process.newTracking = cms.Sequence(process.newSeedFromPairs*process.newSeedFromTriplets*process.newCombinedSeeds*process.newTrackCandidateMaker*process.preFilterFirstStepTracks*process.tracksWithQuality)


process.STAmuontrackingforcosmicsBarrelOnly = cms.Sequence(process.CosmicMuonSeedBarrelOnly*process.cosmicMuonsBarrelOnly)


process.allmuons1LegBarrelOnly = cms.Sequence(process.muons1LegBarrelOnly*process.STAMuons1LegBarrelOnly*process.GLBMuons1LegBarrelOnly)


process.muIsoDeposits_muons = cms.Sequence(process.muIsoDepositTk+process.muIsoDepositCalByAssociatorTowers+process.muIsoDepositJets)


process.muonrecoBeamHaloEndCapsOnly = cms.Sequence(process.globalBeamHaloMuonEndCapslOnly*process.muonsBeamHaloEndCapsOnly)


process.reco = cms.Sequence(process.dtunpacker+process.dt1DRecHits+process.dt4DSegments)


process.siStripElectronSequence = cms.Sequence(process.siStripElectrons*process.egammaCTFFinalFitWithMaterial*process.siStripElectronToTrackAssociator)


process.thirdStep = cms.Sequence(process.thClusters*process.thPixelRecHits*process.thStripRecHits*process.thPLSeeds*process.thTrackCandidates*process.thWithMaterialTracks*process.thStep)


process.cosmicPhotonSequence = cms.Sequence(process.photons)


process.pixeltrackerlocalreco = cms.Sequence(process.siPixelClusters*process.siPixelRecHits)


process.muonIdProducerSequence = cms.Sequence(process.muons*process.calomuons)


process.cosmictracksP5 = cms.Sequence(process.cosmicseedfinderP5*process.cosmictrackfinderP5)


process.hybridClusteringSequence = cms.Sequence(process.hybridSuperClusters*process.correctedHybridSuperClusters)


process.muontrackingforcosmicsBarrelOnly = cms.Sequence(process.STAmuontrackingforcosmicsBarrelOnly*process.globalCosmicMuonsBarrelOnly)


process.doAlldEdXEstimators = cms.Sequence(process.doAlldEdXEstimatorsCTF+process.doAlldEdXEstimatorsRS+process.doAlldEdXEstimatorsCosmicTF)


process.photonSequence = cms.Sequence(process.photons)


process.muonlocalrecoNoDrift = cms.Sequence(process.dtlocalrecoNoDrift+process.csclocalreco+process.rpcRecHits)


process.allmuonsNoDriftBarrelOnly = cms.Sequence(process.muonsNoDriftBarrelOnly*process.STAMuonsNoDriftBarrelOnly*process.GLBMuonsNoDriftBarrelOnly)


process.STAmuontrackingforcosmicsNoDriftBarrelOnly = cms.Sequence(process.CosmicMuonSeedNoDriftBarrelOnly*process.cosmicMuonsNoDriftBarrelOnly)


process.STAmuontrackingforcosmicsEnsCapsOnly = cms.Sequence(process.CosmicMuonSeedEndCapsOnly*process.cosmicMuonsEndCapsOnly)


process.recoJetsGR = cms.Sequence(process.iterativeCone15CaloJets+process.kt4CaloJets+process.kt6CaloJets+process.iterativeCone5CaloJets+process.sisCone5CaloJets+process.sisCone7CaloJets)


process.muIsoDeposits_ParamGlobalMuonsOld = cms.Sequence(process.muParamGlobalIsoDepositGsTk+process.muParamGlobalIsoDepositCalEcal+process.muParamGlobalIsoDepositCalHcal)


process.muonsLocalRecoCosmics = cms.Sequence(process.muonlocalreco+process.muonlocalrecoNoDrift)


process.muonrecocosmicLHCEndCapsOnly = cms.Sequence(process.lhcMuonEndCapsOnly*process.lhcSTAMuonsEndCapsOnly)


process.muIsolation_ParamGlobalMuonsOld = cms.Sequence(process.muIsoDeposits_ParamGlobalMuonsOld)


process.electronSequence = cms.Sequence(process.pixelMatchGsfElectronSequence)


process.STAmuonrecoforcosmicsNoDriftBarrelOnly = cms.Sequence(process.STAmuontrackingforcosmicsNoDriftBarrelOnly*process.STAMuonsNoDriftBarrelOnly)


process.muonrecocosmicLHCBarrelOnly = cms.Sequence(process.lhcMuonBarrelOnly*process.lhcSTAMuonsBarrelOnly)


process.ecalClusters = cms.Sequence(process.hybridClusteringSequence*process.cosmicClusteringSequence)


process.jetsCosmics = cms.Sequence(process.recoCaloTowersGR*process.recoJetsGR)


process.iterTracking = cms.Sequence(process.firstfilter*process.secondStep*process.thirdStep)


process.muontrackingforcosmicsEndCapsOnly = cms.Sequence(process.STAmuontrackingforcosmicsEnsCapsOnly*process.globalCosmicMuonsEndCapsOnly)


process.muonLocalRecoGR = cms.Sequence(process.muonlocalreco+process.muonlocalrecoNoDrift)


process.conversionSequence = cms.Sequence(process.ckfTracksFromConversions*process.conversions)


process.STAmuonrecoforcosmicsBarrelOnly = cms.Sequence(process.STAmuontrackingforcosmicsBarrelOnly*process.STAMuonsBarrelOnly)


process.ckftracks = cms.Sequence(process.newTracking*process.iterTracking*process.trackCollectionMerging)


process.muontrackingforcosmics1LegBarrelOnly = cms.Sequence(process.STAmuontrackingforcosmics1LegBarrelOnly*process.globalCosmicMuons1LegBarrelOnly)


process.muontracking_with_TeVRefinement = cms.Sequence(process.muontracking*process.tevMuons)


process.trackerlocalreco = cms.Sequence(process.pixeltrackerlocalreco*process.striptrackerlocalreco)


process.STAmuonrecoforcosmicsEndCapsOnly = cms.Sequence(process.STAmuontrackingforcosmicsEnsCapsOnly*process.STAMuonsEndCapsOnly)


process.muonrecoforcosmics = cms.Sequence(process.muontrackingforcosmics*process.allmuons)


process.muontrackingforcosmicsNoDriftBarrelOnly = cms.Sequence(process.STAmuontrackingforcosmicsNoDriftBarrelOnly*process.globalCosmicMuonsNoDriftBarrelOnly)


process.muonrecoforcosmicsBarrelOnly = cms.Sequence(process.muontrackingforcosmicsBarrelOnly*process.allmuonsBarrelOnly)


process.cosmicElectronSequence = cms.Sequence(process.electronSequence)


process.tracksP5 = cms.Sequence(process.cosmictracksP5*process.ctftracksP5*process.rstracksP5)


process.muonreco = cms.Sequence(process.muontracking*process.muonIdProducerSequence)


process.muIsolation_ParamGlobalMuons = cms.Sequence(process.muIsoDeposits_ParamGlobalMuons)


process.muonRecoLHC = cms.Sequence(process.muonrecocosmicLHCBarrelOnly*process.muonrecocosmicLHCEndCapsOnly)


process.muonRecoAllGR = cms.Sequence(process.muonrecoforcosmics)


process.muonrecoforcosmicsEndCapsOnly = cms.Sequence(process.muontrackingforcosmicsEndCapsOnly*process.allmuonsEndCapsOnly)


process.STAmuonrecoforcosmics1LegBarrelOnly = cms.Sequence(process.STAmuontrackingforcosmics1LegBarrelOnly*process.STAMuons1LegBarrelOnly)


process.cosmicConversionSequence = cms.Sequence(process.conversionSequence)


process.caloCosmics = cms.Sequence(process.calolocalreco*process.ecalClusters)


process.metrecoCosmics = cms.Sequence(process.metreco)


process.egammarecoCosmics = cms.Sequence(process.cosmicElectronSequence*process.cosmicConversionSequence*process.cosmicPhotonSequence*process.photonIDSequence)


process.muIsolation_muons = cms.Sequence(process.muIsoDeposits_muons)


process.muonrecowith_TeVRefinemen = cms.Sequence(process.muontracking_with_TeVRefinement*process.muonIdProducerSequence)


process.muonRecoEndCapsGR = cms.Sequence(process.muonrecoforcosmicsEndCapsOnly*process.muonrecoBeamHaloEndCapsOnly)


process.muonrecoforcosmics1LegBarrelOnly = cms.Sequence(process.muontrackingforcosmics1LegBarrelOnly*process.allmuons1LegBarrelOnly)


process.egammarecoCosmics_woElectrons = cms.Sequence(process.cosmicConversionSequence*process.cosmicPhotonSequence*process.photonIDSequence)


process.egammaCosmics = cms.Sequence(process.egammarecoCosmics_woElectrons)


process.muonrecoforcosmicsNoDriftBarrelOnly = cms.Sequence(process.muontrackingforcosmicsNoDriftBarrelOnly*process.allmuonsNoDriftBarrelOnly)


process.egammarecoCosmics_woConvPhotons = cms.Sequence(process.cosmicElectronSequence*process.cosmicPhotonSequence)


process.trackerCosmics = cms.Sequence(process.offlineBeamSpot*process.trackerlocalreco*process.tracksP5)


process.muIsolation = cms.Sequence(process.muIsolation_muons)


process.localReconstructionCosmics = cms.Sequence(process.trackerCosmics*process.caloCosmics*process.muonsLocalRecoCosmics)


process.muonRecoBarrelGR = cms.Sequence(process.muonrecoforcosmicsBarrelOnly+process.muonrecoforcosmics1LegBarrelOnly+process.muonrecoforcosmicsNoDriftBarrelOnly)


process.muonreco_plus_isolation = cms.Sequence(process.muonrecowith_TeVRefinemen*process.muIsolation)


process.muonRecoGR = cms.Sequence(process.muonRecoAllGR*process.muonRecoBarrelGR*process.muonRecoEndCapsGR*process.muonRecoLHC)


process.muonsCosmics = cms.Sequence(process.muonRecoGR)


process.reconstructionCosmics_woTkBHM = cms.Sequence(process.localReconstructionCosmics*process.muonsCosmics*process.jetsCosmics*process.metrecoCosmics*process.egammaCosmics)


process.reconstructionCosmics = cms.Sequence(process.localReconstructionCosmics*process.tracksBeamHaloMuon*process.muonsCosmics*process.jetsCosmics*process.metrecoCosmics*process.egammaCosmics*process.doAlldEdXEstimators)


process.reconstructionCosmics_woDeDx = cms.Sequence(process.localReconstructionCosmics*process.tracksBeamHaloMuon*process.muonsCosmics*process.jetsCosmics*process.metrecoCosmics*process.egammaCosmics)


process.dtVisPath = cms.Path(process.reco+process.dtOfflineOccupancy)


process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('*'),
    cout = cms.untracked.PSet(
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        DEBUG = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        DTNoiseAnalysisTest = cms.untracked.PSet(
            limit = cms.untracked.int32(100000000)
        ),
        threshold = cms.untracked.string('DEBUG'),
        noLineBreaks = cms.untracked.bool(False)
    ),
    categories = cms.untracked.vstring('DTNoiseAnalysisTest'),
    destinations = cms.untracked.vstring('cout')
)


process.UpdaterService = cms.Service("UpdaterService")


process.Chi2MeasurementEstimator = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    MaxChi2 = cms.double(30.0),
    nSigma = cms.double(3.0),
    ComponentName = cms.string('Chi2')
)


process.CaloGeometryBuilder = cms.ESProducer("CaloGeometryBuilder",
    SelectedCalos = cms.vstring('HCAL', 
        'ZDC', 
        'EcalBarrel', 
        'EcalEndcap', 
        'EcalPreshower', 
        'TOWER')
)


process.KFSmootherForRefitInsideOut = cms.ESProducer("KFTrajectorySmootherESProducer",
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3),
    ComponentName = cms.string('KFSmootherForRefitInsideOut'),
    Estimator = cms.string('Chi2EstimatorForRefit'),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('SmartPropagatorAnyRK')
)


process.SmartPropagatorAnyRK = cms.ESProducer("SmartPropagatorESProducer",
    Epsilon = cms.double(5.0),
    TrackerPropagator = cms.string('RKTrackerPropagator'),
    MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
    PropagationDirection = cms.string('alongMomentum'),
    ComponentName = cms.string('SmartPropagatorAnyRK')
)


process.siStripGainESProducerforSimulation = cms.ESProducer("SiStripGainESProducer",
    printDebug = cms.untracked.bool(False),
    appendToDataLabel = cms.string('fake'),
    APVGain = cms.string('fakeAPVGain'),
    AutomaticNormalization = cms.bool(False),
    NormalizationFactor = cms.double(1.0)
)


process.KFTrajectorySmootherForSTA = cms.ESProducer("KFTrajectorySmootherESProducer",
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3),
    ComponentName = cms.string('KFSmootherSTA'),
    Estimator = cms.string('Chi2STA'),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('SteppingHelixPropagatorOpposite')
)


process.BeamHaloSHPropagatorAny = cms.ESProducer("SteppingHelixPropagatorESProducer",
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('anyDirection'),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    endcapShiftInZNeg = cms.double(0.0),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    returnTangentPlane = cms.bool(True),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    ComponentName = cms.string('BeamHaloSHPropagatorAny'),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    endcapShiftInZPos = cms.double(0.0)
)


process.KFTrajectorySmootherBeamHalo = cms.ESProducer("KFTrajectorySmootherESProducer",
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3),
    ComponentName = cms.string('KFSmootherBH'),
    Estimator = cms.string('Chi2'),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('BeamHaloPropagatorAlong')
)


process.BeamHaloMPropagatorOpposite = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(10000),
    useRungeKutta = cms.bool(False),
    Mass = cms.double(0.105),
    PropagationDirection = cms.string('oppositeToMomentum'),
    ComponentName = cms.string('BeamHaloMPropagatorOpposite')
)


process.ttrhbwor = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    StripCPE = cms.string('Fake'),
    Matcher = cms.string('Fake'),
    PixelCPE = cms.string('Fake'),
    ComponentName = cms.string('WithoutRefit')
)


process.BeamHaloSHPropagatorOpposite = cms.ESProducer("SteppingHelixPropagatorESProducer",
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('oppositeToMomentum'),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    endcapShiftInZNeg = cms.double(0.0),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    returnTangentPlane = cms.bool(True),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    ComponentName = cms.string('BeamHaloSHPropagatorOpposite'),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    endcapShiftInZPos = cms.double(0.0)
)


process.roadsP5 = cms.ESProducer("RoadMapMakerESProducer",
    GeometryStructure = cms.string('P5'),
    ComponentName = cms.string('P5'),
    RingsLabel = cms.string('P5'),
    WriteOutRoadMapToAsciiFile = cms.untracked.bool(False),
    SeedingType = cms.string('TwoRingSeeds'),
    RoadMapAsciiFile = cms.untracked.string('roads.dat')
)


process.CloseComponentsMerger5D = cms.ESProducer("CloseComponentsMergerESProducer5D",
    ComponentName = cms.string('CloseComponentsMerger5D'),
    MaxComponents = cms.int32(12),
    DistanceMeasure = cms.string('KullbackLeiblerDistance5D')
)


process.CkfTrajectoryBuilder = cms.ESProducer("CkfTrajectoryBuilderESProducer",
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    trajectoryFilterName = cms.string('ckfBaseTrajectoryFilter'),
    maxCand = cms.int32(5),
    ComponentName = cms.string('CkfTrajectoryBuilder'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    MeasurementTrackerName = cms.string(''),
    estimator = cms.string('Chi2'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    updator = cms.string('KFUpdator'),
    alwaysUseInvalidHits = cms.bool(True),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0)
)


process.ringsP5 = cms.ESProducer("RingMakerESProducer",
    DumpDetIds = cms.untracked.bool(False),
    ComponentName = cms.string('P5'),
    RingAsciiFileName = cms.untracked.string('rings_p5.dat'),
    DetIdsDumpFileName = cms.untracked.string('tracker_detids.dat'),
    WriteOutRingsToAsciiFile = cms.untracked.bool(False),
    Configuration = cms.untracked.string('P5')
)


process.l1GtTriggerMenuXml = cms.ESProducer("L1GtTriggerMenuXmlProducer",
    VmeXmlFile = cms.string(''),
    DefXmlFile = cms.string('L1Menu2008_2E30.xml'),
    TriggerMenuLuminosity = cms.string('lumi1030')
)


process.EcalEndcapGeometryEP = cms.ESProducer("EcalEndcapGeometryEP",
    applyAlignment = cms.untracked.bool(False)
)


process.L1MuTriggerScales = cms.ESProducer("L1MuTriggerScalesProducer",
    signedPackingDTEta = cms.bool(True),
    offsetDTEta = cms.int32(32),
    nbinsDTEta = cms.int32(64),
    offsetFwdRPCEta = cms.int32(16),
    signedPackingBrlRPCEta = cms.bool(True),
    maxDTEta = cms.double(1.2),
    nbitPackingFwdRPCEta = cms.int32(6),
    nbinsBrlRPCEta = cms.int32(33),
    nbinsFwdRPCEta = cms.int32(33),
    nbitPackingGMTEta = cms.int32(6),
    minCSCEta = cms.double(0.9),
    nbinsPhi = cms.int32(144),
    nbitPackingPhi = cms.int32(8),
    nbitPackingDTEta = cms.int32(6),
    maxCSCEta = cms.double(2.5),
    nbinsGMTEta = cms.int32(31),
    minDTEta = cms.double(-1.2),
    nbitPackingCSCEta = cms.int32(6),
    signedPackingFwdRPCEta = cms.bool(True),
    offsetBrlRPCEta = cms.int32(16),
    scaleRPCEta = cms.vdouble(-2.1, -1.97, -1.85, -1.73, -1.61, 
        -1.48, -1.36, -1.24, -1.14, -1.04, 
        -0.93, -0.83, -0.72, -0.58, -0.44, 
        -0.27, -0.07, 0.07, 0.27, 0.44, 
        0.58, 0.72, 0.83, 0.93, 1.04, 
        1.14, 1.24, 1.36, 1.48, 1.61, 
        1.73, 1.85, 1.97, 2.1),
    signedPackingPhi = cms.bool(False),
    nbitPackingBrlRPCEta = cms.int32(6),
    nbinsCSCEta = cms.int32(32),
    maxPhi = cms.double(6.2831853),
    minPhi = cms.double(0.0),
    scaleGMTEta = cms.vdouble(0.0, 0.1, 0.2, 0.3, 0.4, 
        0.5, 0.6, 0.7, 0.8, 0.9, 
        1.0, 1.1, 1.2, 1.3, 1.4, 
        1.5, 1.6, 1.7, 1.75, 1.8, 
        1.85, 1.9, 1.95, 2.0, 2.05, 
        2.1, 2.15, 2.2, 2.25, 2.3, 
        2.35, 2.4)
)


process.hcalDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('HcalDetIdAssociator'),
    etaBinSize = cms.double(0.087),
    nEta = cms.int32(70),
    nPhi = cms.int32(72)
)


process.alongMomElePropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(1.6),
    useRungeKutta = cms.bool(False),
    Mass = cms.double(0.000511),
    PropagationDirection = cms.string('alongMomentum'),
    ComponentName = cms.string('alongMomElePropagator')
)


process.HcalHardcodeGeometryEP = cms.ESProducer("HcalHardcodeGeometryEP",
    applyAlignment = cms.untracked.bool(False)
)


process.TrackerDigiGeometryESModule = cms.ESProducer("TrackerDigiGeometryESModule",
    appendToDataLabel = cms.string(''),
    fromDDD = cms.bool(True),
    applyAlignment = cms.bool(True),
    alignmentsLabel = cms.string('')
)


process.fourthMeasurementTracker = cms.ESProducer("MeasurementTrackerESProducer",
    stripLazyGetterProducer = cms.string(''),
    StripCPE = cms.string('StripCPEfromTrackAngle'),
    OnDemand = cms.bool(False),
    UseStripAPVFiberQualityDB = cms.bool(True),
    DebugStripModuleQualityDB = cms.untracked.bool(False),
    ComponentName = cms.string('fourthMeasurementTracker'),
    stripClusterProducer = cms.string('fourthClusters'),
    Regional = cms.bool(False),
    UseStripModuleQualityDB = cms.bool(True),
    DebugStripAPVFiberQualityDB = cms.untracked.bool(False),
    HitMatcher = cms.string('StandardMatcher'),
    DebugStripStripQualityDB = cms.untracked.bool(False),
    pixelClusterProducer = cms.string('fourthClusters'),
    UseStripStripQualityDB = cms.bool(True),
    MaskBadAPVFibers = cms.bool(False),
    PixelCPE = cms.string('PixelCPEGeneric')
)


process.SteppingHelixPropagatorL2Any = cms.ESProducer("SteppingHelixPropagatorESProducer",
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('anyDirection'),
    useTuningForL2Speed = cms.bool(True),
    ComponentName = cms.string('SteppingHelixPropagatorL2Any'),
    useIsYokeFlag = cms.bool(True),
    endcapShiftInZNeg = cms.double(0.0),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    endcapShiftInZPos = cms.double(0.0),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    useMatVolumes = cms.bool(True),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    returnTangentPlane = cms.bool(True)
)


process.SmartPropagatorRK = cms.ESProducer("SmartPropagatorESProducer",
    Epsilon = cms.double(5.0),
    TrackerPropagator = cms.string('RKTrackerPropagator'),
    MuonPropagator = cms.string('SteppingHelixPropagatorAlong'),
    PropagationDirection = cms.string('alongMomentum'),
    ComponentName = cms.string('SmartPropagatorRK')
)


process.RKTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('RKFitter'),
    Estimator = cms.string('Chi2'),
    minHits = cms.int32(3),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.CaloTowerConstituentsMapBuilder = cms.ESProducer("CaloTowerConstituentsMapBuilder",
    MapFile = cms.untracked.string('Geometry/CaloTopology/data/CaloTowerEEGeometric.map.gz')
)


process.oppositeToMomElePropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(1.6),
    useRungeKutta = cms.bool(False),
    Mass = cms.double(0.000511),
    PropagationDirection = cms.string('oppositeToMomentum'),
    ComponentName = cms.string('oppositeToMomElePropagator')
)


process.ecalDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('EcalDetIdAssociator'),
    etaBinSize = cms.double(0.02),
    nEta = cms.int32(300),
    nPhi = cms.int32(360)
)


process.muonDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('MuonDetIdAssociator'),
    etaBinSize = cms.double(0.125),
    nEta = cms.int32(48),
    nPhi = cms.int32(48)
)


process.EcalBarrelGeometryEP = cms.ESProducer("EcalBarrelGeometryEP",
    applyAlignment = cms.untracked.bool(False)
)


process.bwdGsfElectronPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(1.6),
    useRungeKutta = cms.bool(False),
    Mass = cms.double(0.000511),
    PropagationDirection = cms.string('oppositeToMomentum'),
    ComponentName = cms.string('bwdGsfElectronPropagator')
)


process.TransientTrackBuilderESProducer = cms.ESProducer("TransientTrackBuilderESProducer",
    ComponentName = cms.string('TransientTrackBuilder')
)


process.KFFittingSmootherForInOut = cms.ESProducer("KFFittingSmootherESProducer",
    EstimateCut = cms.double(-1),
    Fitter = cms.string('KFFitterForInOut'),
    ComponentName = cms.string('KFFittingSmootherForInOut'),
    Smoother = cms.string('KFSmootherForInOut'),
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    MinNumberOfHits = cms.int32(3),
    NoInvalidHitsBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True)
)


process.EcalTrigTowerConstituentsMapBuilder = cms.ESProducer("EcalTrigTowerConstituentsMapBuilder",
    MapFile = cms.untracked.string('Geometry/EcalMapping/data/EndCap_TTMap.txt')
)


process.KFTrajectoryFitterForOutIn = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('KFFitterForOutIn'),
    Estimator = cms.string('Chi2ForOutIn'),
    minHits = cms.int32(3),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('alongMomElePropagator')
)


process.l1GtTriggerMaskVetoTechTrig = cms.ESProducer("L1GtTriggerMaskVetoTechTrigTrivialProducer",
    TriggerMask = cms.vuint32(0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0)
)


process.MuonDetLayerGeometryESProducer = cms.ESProducer("MuonDetLayerGeometryESProducer")


process.dttfluts = cms.ESProducer("DTTrackFinderConfig")


process.OppositeMaterialPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(1.6),
    useRungeKutta = cms.bool(False),
    Mass = cms.double(0.105),
    PropagationDirection = cms.string('oppositeToMomentum'),
    ComponentName = cms.string('PropagatorWithMaterialOpposite')
)


process.l1GtParameters = cms.ESProducer("L1GtParametersTrivialProducer",
    EvmActiveBoards = cms.uint32(65535),
    DaqActiveBoards = cms.uint32(65535),
    BstLengthBytes = cms.uint32(30),
    TotalBxInEvent = cms.int32(3)
)


process.l1CaloScales = cms.ESProducer("L1ScalesTrivialProducer",
    L1CaloEmEtScaleLSB = cms.double(0.5),
    L1CaloRegionEtScaleLSB = cms.double(0.5),
    L1CaloJetThresholds = cms.vdouble(0.0, 10.0, 12.0, 14.0, 15.0, 
        18.0, 20.0, 22.0, 24.0, 25.0, 
        28.0, 30.0, 32.0, 35.0, 37.0, 
        40.0, 45.0, 50.0, 55.0, 60.0, 
        65.0, 70.0, 75.0, 80.0, 85.0, 
        90.0, 100.0, 110.0, 120.0, 125.0, 
        130.0, 140.0, 150.0, 160.0, 170.0, 
        175.0, 180.0, 190.0, 200.0, 215.0, 
        225.0, 235.0, 250.0, 275.0, 300.0, 
        325.0, 350.0, 375.0, 400.0, 425.0, 
        450.0, 475.0, 500.0, 525.0, 550.0, 
        575.0, 600.0, 625.0, 650.0, 675.0, 
        700.0, 725.0, 750.0, 775.0),
    L1CaloEmThresholds = cms.vdouble(0.0, 1.0, 2.0, 3.0, 4.0, 
        5.0, 6.0, 7.0, 8.0, 9.0, 
        10.0, 11.0, 12.0, 13.0, 14.0, 
        15.0, 16.0, 17.0, 18.0, 19.0, 
        20.0, 21.0, 22.0, 23.0, 24.0, 
        25.0, 26.0, 27.0, 28.0, 29.0, 
        30.0, 31.0, 32.0, 33.0, 34.0, 
        35.0, 36.0, 37.0, 38.0, 39.0, 
        40.0, 41.0, 42.0, 43.0, 44.0, 
        45.0, 46.0, 47.0, 48.0, 49.0, 
        50.0, 51.0, 52.0, 53.0, 54.0, 
        55.0, 56.0, 57.0, 58.0, 59.0, 
        60.0, 61.0, 62.0, 63.0)
)


process.l1GtTriggerMaskTechTrig = cms.ESProducer("L1GtTriggerMaskTechTrigTrivialProducer",
    TriggerMask = cms.vuint32(0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0)
)


process.compositeTrajectoryFilterESProducer = cms.ESProducer("CompositeTrajectoryFilterESProducer",
    filterNames = cms.vstring(),
    ComponentName = cms.string('compositeTrajectoryFilter')
)


process.l1GtPrescaleFactorsTechTrig = cms.ESProducer("L1GtPrescaleFactorsTechTrigTrivialProducer",
    PrescaleFactorsSet = cms.VPSet(cms.PSet(
        PrescaleFactors = cms.vint32(1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1)
    ), 
        cms.PSet(
            PrescaleFactors = cms.vint32(1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 
                1, 1, 1, 1)
        ))
)


process.l1GtTriggerMaskVetoAlgoTrig = cms.ESProducer("L1GtTriggerMaskVetoAlgoTrigTrivialProducer",
    TriggerMask = cms.vuint32(0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0)
)


process.secMeasurementTracker = cms.ESProducer("MeasurementTrackerESProducer",
    stripLazyGetterProducer = cms.string(''),
    StripCPE = cms.string('StripCPEfromTrackAngle'),
    OnDemand = cms.bool(False),
    UseStripAPVFiberQualityDB = cms.bool(True),
    DebugStripModuleQualityDB = cms.untracked.bool(False),
    ComponentName = cms.string('secMeasurementTracker'),
    stripClusterProducer = cms.string('secClusters'),
    Regional = cms.bool(False),
    UseStripModuleQualityDB = cms.bool(True),
    DebugStripAPVFiberQualityDB = cms.untracked.bool(False),
    HitMatcher = cms.string('StandardMatcher'),
    DebugStripStripQualityDB = cms.untracked.bool(False),
    pixelClusterProducer = cms.string('secClusters'),
    UseStripStripQualityDB = cms.bool(True),
    MaskBadAPVFibers = cms.bool(False),
    PixelCPE = cms.string('PixelCPEGeneric')
)


process.KFSmootherForMuonTrackLoader = cms.ESProducer("KFTrajectorySmootherESProducer",
    errorRescaling = cms.double(10.0),
    minHits = cms.int32(3),
    ComponentName = cms.string('KFSmootherForMuonTrackLoader'),
    Estimator = cms.string('Chi2EstimatorForMuonTrackLoader'),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('SmartPropagatorAnyRK')
)


process.KFTrajectoryFitterForInOut = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('KFFitterForInOut'),
    Estimator = cms.string('Chi2ForInOut'),
    minHits = cms.int32(3),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('alongMomElePropagator')
)


process.ElectronMaterialEffects = cms.ESProducer("GsfMaterialEffectsESProducer",
    BetheHeitlerParametrization = cms.string('BetheHeitler_cdfmom_nC6_O5.par'),
    EnergyLossUpdator = cms.string('GsfBetheHeitlerUpdator'),
    ComponentName = cms.string('ElectronMaterialEffects'),
    MultipleScatteringUpdator = cms.string('MultipleScatteringUpdator'),
    Mass = cms.double(0.000511),
    BetheHeitlerCorrection = cms.int32(2)
)


process.KFSmootherForMuonTrackLoaderL3 = cms.ESProducer("KFTrajectorySmootherESProducer",
    errorRescaling = cms.double(10.0),
    minHits = cms.int32(3),
    ComponentName = cms.string('KFSmootherForMuonTrackLoaderL3'),
    Estimator = cms.string('Chi2EstimatorForMuonTrackLoader'),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('SmartPropagatorAnyOpposite')
)


process.SmartPropagatorAnyOpposite = cms.ESProducer("SmartPropagatorESProducer",
    Epsilon = cms.double(5.0),
    TrackerPropagator = cms.string('PropagatorWithMaterialOpposite'),
    MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
    PropagationDirection = cms.string('oppositeToMomentum'),
    ComponentName = cms.string('SmartPropagatorAnyOpposite')
)


process.KFUpdatorESProducer = cms.ESProducer("KFUpdatorESProducer",
    ComponentName = cms.string('KFUpdator')
)


process.newTrajectoryBuilder = cms.ESProducer("GroupedCkfTrajectoryBuilderESProducer",
    bestHitOnly = cms.bool(True),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    trajectoryFilterName = cms.string('newTrajectoryFilter'),
    maxCand = cms.int32(5),
    ComponentName = cms.string('newTrajectoryBuilder'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    MeasurementTrackerName = cms.string(''),
    minNrOfHitsForRebuild = cms.int32(5),
    lockHits = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    foundHitBonus = cms.double(5.0),
    updator = cms.string('KFUpdator'),
    alwaysUseInvalidHits = cms.bool(True),
    requireSeedHitsInRebuild = cms.bool(True),
    estimator = cms.string('Chi2'),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0)
)


process.KFTrajectorySmootherForInOut = cms.ESProducer("KFTrajectorySmootherESProducer",
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3),
    ComponentName = cms.string('KFSmootherForInOut'),
    Estimator = cms.string('Chi2ForInOut'),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('oppositeToMomElePropagator')
)


process.MaterialPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(1.6),
    useRungeKutta = cms.bool(False),
    Mass = cms.double(0.105),
    PropagationDirection = cms.string('alongMomentum'),
    ComponentName = cms.string('PropagatorWithMaterial')
)


process.myTTRHBuilderWithoutAngle4MixedTriplets = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    StripCPE = cms.string('Fake'),
    Matcher = cms.string('StandardMatcher'),
    PixelCPE = cms.string('PixelCPEGeneric'),
    ComponentName = cms.string('TTRHBuilderWithoutAngle4MixedTriplets')
)


process.BeamHaloPropagatorAny = cms.ESProducer("BeamHaloPropagatorESProducer",
    ComponentName = cms.string('BeamHaloPropagatorAny'),
    CrossingTrackerPropagator = cms.string('BeamHaloSHPropagatorAny'),
    PropagationDirection = cms.string('anyDirection'),
    EndCapTrackerPropagator = cms.string('BeamHaloMPropagatorAlong')
)


process.rings = cms.ESProducer("RingMakerESProducer",
    DumpDetIds = cms.untracked.bool(False),
    ComponentName = cms.string(''),
    RingAsciiFileName = cms.untracked.string('rings.dat'),
    DetIdsDumpFileName = cms.untracked.string('tracker_detids.dat'),
    WriteOutRingsToAsciiFile = cms.untracked.bool(False),
    Configuration = cms.untracked.string('FULL')
)


process.fourthCkfTrajectoryBuilder = cms.ESProducer("GroupedCkfTrajectoryBuilderESProducer",
    bestHitOnly = cms.bool(True),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    trajectoryFilterName = cms.string('fourthCkfTrajectoryFilter'),
    maxCand = cms.int32(5),
    ComponentName = cms.string('fourthCkfTrajectoryBuilder'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    MeasurementTrackerName = cms.string('fourthMeasurementTracker'),
    minNrOfHitsForRebuild = cms.int32(5),
    lockHits = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    foundHitBonus = cms.double(5.0),
    updator = cms.string('KFUpdator'),
    alwaysUseInvalidHits = cms.bool(True),
    requireSeedHitsInRebuild = cms.bool(True),
    estimator = cms.string('Chi2'),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0)
)


process.ZdcHardcodeGeometryEP = cms.ESProducer("ZdcHardcodeGeometryEP",
    applyAlignment = cms.untracked.bool(False)
)


process.KFFitterForRefitInsideOut = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('KFFitterForRefitInsideOut'),
    Estimator = cms.string('Chi2EstimatorForRefit'),
    minHits = cms.int32(3),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('SmartPropagatorAnyRK')
)


process.bwdAnalyticalPropagator = cms.ESProducer("AnalyticalPropagatorESProducer",
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('bwdAnalyticalPropagator'),
    PropagationDirection = cms.string('oppositeToMomentum')
)


process.ckfTrajectoryFilterBeamHaloMuon = cms.ESProducer("TrajectoryFilterESProducer",
    filterPset = cms.PSet(
        minimumNumberOfHits = cms.int32(4),
        minPt = cms.double(0.1),
        minHitsMinPt = cms.int32(3),
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        maxLostHits = cms.int32(3),
        maxNumberOfHits = cms.int32(-1),
        maxConsecLostHits = cms.int32(2),
        nSigmaMinPt = cms.double(5.0),
        chargeSignificance = cms.double(-1.0)
    ),
    ComponentName = cms.string('ckfTrajectoryFilterBeamHaloMuon')
)


process.Chi2MeasurementEstimatorForInOut = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    MaxChi2 = cms.double(100.0),
    nSigma = cms.double(3.0),
    ComponentName = cms.string('Chi2ForInOut')
)


process.RungeKuttaTrackerPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(1.6),
    useRungeKutta = cms.bool(True),
    Mass = cms.double(0.105),
    PropagationDirection = cms.string('alongMomentum'),
    ComponentName = cms.string('RungeKuttaTrackerPropagator')
)


process.Chi2MeasurementEstimatorForOutIn = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    MaxChi2 = cms.double(500.0),
    nSigma = cms.double(3.0),
    ComponentName = cms.string('Chi2ForOutIn')
)


process.Chi2EstimatorForMuRefit = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    MaxChi2 = cms.double(100000.0),
    nSigma = cms.double(3.0),
    ComponentName = cms.string('Chi2EstimatorForMuRefit')
)


process.TrajectoryBuilderForPixelMatchGsfElectrons = cms.ESProducer("CkfTrajectoryBuilderESProducer",
    propagatorAlong = cms.string('fwdGsfElectronPropagator'),
    trajectoryFilterName = cms.string('TrajectoryFilterForPixelMatchGsfElectrons'),
    maxCand = cms.int32(3),
    ComponentName = cms.string('TrajectoryBuilderForPixelMatchGsfElectrons'),
    propagatorOpposite = cms.string('bwdGsfElectronPropagator'),
    MeasurementTrackerName = cms.string(''),
    estimator = cms.string('gsfElectronChi2'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    updator = cms.string('KFUpdator'),
    alwaysUseInvalidHits = cms.bool(True),
    intermediateCleaning = cms.bool(False),
    lostHitPenalty = cms.double(30.0)
)


process.L1MuTriggerPtScale = cms.ESProducer("L1MuTriggerPtScaleProducer",
    nbitPackingPt = cms.int32(5),
    scalePt = cms.vdouble(-1.0, 0.0, 1.5, 2.0, 2.5, 
        3.0, 3.5, 4.0, 4.5, 5.0, 
        6.0, 7.0, 8.0, 10.0, 12.0, 
        14.0, 16.0, 18.0, 20.0, 25.0, 
        30.0, 35.0, 40.0, 45.0, 50.0, 
        60.0, 70.0, 80.0, 90.0, 100.0, 
        120.0, 140.0, 1000000.0),
    signedPackingPt = cms.bool(False),
    nbinsPt = cms.int32(32)
)


process.KFTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('KFFitter'),
    Estimator = cms.string('Chi2'),
    minHits = cms.int32(3),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('PropagatorWithMaterial')
)


process.RKFittingSmoother = cms.ESProducer("KFFittingSmootherESProducer",
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('RKFitter'),
    ComponentName = cms.string('RKFittingSmoother'),
    Smoother = cms.string('RKSmoother'),
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    MinNumberOfHits = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True)
)


process.KFFittingSmootherBeamHalo = cms.ESProducer("KFFittingSmootherESProducer",
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('KFFitterBH'),
    ComponentName = cms.string('KFFittingSmootherBH'),
    Smoother = cms.string('KFSmootherBH'),
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    MinNumberOfHits = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True)
)


process.KFTrajectoryFitterForSTA = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('KFFitterSTA'),
    Estimator = cms.string('Chi2STA'),
    minHits = cms.int32(3),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('SteppingHelixPropagatorAny')
)


process.mixedlayerpairs = cms.ESProducer("MixedLayerPairsESProducer",
    FPix = cms.PSet(
        hitErrorRZ = cms.double(0.0036),
        hitErrorRPhi = cms.double(0.0051),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4MixedPairs'),
        HitProducer = cms.string('siPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    layerList = cms.vstring('BPix1+BPix2', 
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
        'TEC2_neg+TEC3_neg'),
    TEC = cms.PSet(
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        minRing = cms.int32(1),
        maxRing = cms.int32(1)
    ),
    BPix = cms.PSet(
        hitErrorRZ = cms.double(0.006),
        hitErrorRPhi = cms.double(0.0027),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4MixedPairs'),
        HitProducer = cms.string('siPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    ComponentName = cms.string('MixedLayerPairs')
)


process.GroupedCkfTrajectoryBuilder = cms.ESProducer("GroupedCkfTrajectoryBuilderESProducer",
    bestHitOnly = cms.bool(True),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    trajectoryFilterName = cms.string('ckfBaseTrajectoryFilter'),
    maxCand = cms.int32(5),
    ComponentName = cms.string('GroupedCkfTrajectoryBuilder'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    MeasurementTrackerName = cms.string(''),
    minNrOfHitsForRebuild = cms.int32(5),
    lockHits = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    foundHitBonus = cms.double(5.0),
    updator = cms.string('KFUpdator'),
    alwaysUseInvalidHits = cms.bool(True),
    requireSeedHitsInRebuild = cms.bool(True),
    estimator = cms.string('Chi2'),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0)
)


process.secCkfTrajectoryFilter = cms.ESProducer("TrajectoryFilterESProducer",
    filterPset = cms.PSet(
        minimumNumberOfHits = cms.int32(3),
        minPt = cms.double(0.3),
        minHitsMinPt = cms.int32(3),
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        maxLostHits = cms.int32(1),
        maxNumberOfHits = cms.int32(-1),
        maxConsecLostHits = cms.int32(1),
        nSigmaMinPt = cms.double(5.0),
        chargeSignificance = cms.double(-1.0)
    ),
    ComponentName = cms.string('secCkfTrajectoryFilter')
)


process.thCkfTrajectoryBuilder = cms.ESProducer("GroupedCkfTrajectoryBuilderESProducer",
    bestHitOnly = cms.bool(True),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    trajectoryFilterName = cms.string('thCkfTrajectoryFilter'),
    maxCand = cms.int32(5),
    ComponentName = cms.string('thCkfTrajectoryBuilder'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    MeasurementTrackerName = cms.string('thMeasurementTracker'),
    minNrOfHitsForRebuild = cms.int32(5),
    lockHits = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    foundHitBonus = cms.double(5.0),
    updator = cms.string('KFUpdator'),
    alwaysUseInvalidHits = cms.bool(True),
    requireSeedHitsInRebuild = cms.bool(True),
    estimator = cms.string('Chi2'),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0)
)


process.BeamHaloPropagatorAlong = cms.ESProducer("BeamHaloPropagatorESProducer",
    ComponentName = cms.string('BeamHaloPropagatorAlong'),
    CrossingTrackerPropagator = cms.string('BeamHaloSHPropagatorAlong'),
    PropagationDirection = cms.string('alongMomentum'),
    EndCapTrackerPropagator = cms.string('BeamHaloMPropagatorAlong')
)


process.KFFittingSmootherWithOutliersRejectionAndRK = cms.ESProducer("KFFittingSmootherESProducer",
    EstimateCut = cms.double(20.0),
    Fitter = cms.string('RKFitter'),
    ComponentName = cms.string('KFFittingSmootherWithOutliersRejectionAndRK'),
    Smoother = cms.string('RKSmoother'),
    BreakTrajWith2ConsecutiveMissing = cms.bool(True),
    MinNumberOfHits = cms.int32(3),
    NoInvalidHitsBeginEnd = cms.bool(True),
    RejectTracks = cms.bool(True)
)


process.l1CaloGeometry = cms.ESProducer("L1CaloGeometryProd",
    gctEtaBinBoundaries = cms.vdouble(0.0, 0.348, 0.695, 1.044, 1.392, 
        1.74, 2.172, 3.0, 3.5, 4.0, 
        4.5, 5.0),
    numberGctEmJetPhiBins = cms.uint32(18),
    numberGctEtSumPhiBins = cms.uint32(72),
    gctEmJetPhiBinOffset = cms.double(-0.5),
    numberGctForwardEtaBinsPerHalf = cms.uint32(4),
    gctEtSumPhiBinOffset = cms.double(0.0),
    numberGctCentralEtaBinsPerHalf = cms.uint32(7),
    etaSignBitOffset = cms.uint32(8)
)


process.KFTrajectoryFitterBeamHalo = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('KFFitterBH'),
    Estimator = cms.string('Chi2'),
    minHits = cms.int32(3),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('BeamHaloPropagatorAlong')
)


process.PixelCPEParmErrorESProducer = cms.ESProducer("PixelCPEParmErrorESProducer",
    UseNewParametrization = cms.bool(True),
    ComponentName = cms.string('PixelCPEfromTrackAngle'),
    UseSigma = cms.bool(True),
    Alpha2Order = cms.bool(True),
    PixelErrorParametrization = cms.string('NOTcmsim')
)


process.CkfTrajectoryBuilderBeamHalo = cms.ESProducer("CkfTrajectoryBuilderESProducer",
    propagatorAlong = cms.string('BeamHaloPropagatorAlong'),
    trajectoryFilterName = cms.string('ckfTrajectoryFilterBeamHaloMuon'),
    maxCand = cms.int32(5),
    ComponentName = cms.string('CkfTrajectoryBuilderBH'),
    propagatorOpposite = cms.string('BeamHaloPropagatorOpposite'),
    MeasurementTrackerName = cms.string(''),
    estimator = cms.string('Chi2'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    updator = cms.string('KFUpdator'),
    alwaysUseInvalidHits = cms.bool(True),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0)
)


process.newTrajectoryFilter = cms.ESProducer("TrajectoryFilterESProducer",
    filterPset = cms.PSet(
        minimumNumberOfHits = cms.int32(3),
        minPt = cms.double(0.3),
        minHitsMinPt = cms.int32(3),
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        maxLostHits = cms.int32(1),
        maxNumberOfHits = cms.int32(-1),
        maxConsecLostHits = cms.int32(1),
        nSigmaMinPt = cms.double(5.0),
        chargeSignificance = cms.double(-1.0)
    ),
    ComponentName = cms.string('newTrajectoryFilter')
)


process.chi2CutForConversionTrajectoryBuilder = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    MaxChi2 = cms.double(100000.0),
    nSigma = cms.double(3.0),
    ComponentName = cms.string('eleLooseChi2')
)


process.DAFTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('DAFFitter'),
    Estimator = cms.string('MRHChi2'),
    minHits = cms.int32(3),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.l1GtBoardMaps = cms.ESProducer("L1GtBoardMapsTrivialProducer",
    ActiveBoardsDaqRecord = cms.vint32(-1, 0, 1, 2, 3, 
        4, 5, 6, 7, 8, 
        -1, -1),
    CableToPsbMap = cms.vint32(0, 0, 0, 0, 1, 
        1, 1, 1, 2, 2, 
        2, 2, 3, 3, 3, 
        3, 4, 4, 4, 4, 
        5, 5, 5, 5, 6, 
        6, 6, 6),
    BoardPositionDaqRecord = cms.vint32(1, 2, 3, 4, 5, 
        6, 7, 8, 9, 10, 
        -1, -1),
    BoardPositionEvmRecord = cms.vint32(1, 3, -1, -1, -1, 
        -1, -1, -1, -1, -1, 
        2, -1),
    BoardList = cms.vstring('GTFE', 
        'FDL', 
        'PSB', 
        'PSB', 
        'PSB', 
        'PSB', 
        'PSB', 
        'PSB', 
        'PSB', 
        'GMT', 
        'TCS', 
        'TIM'),
    CableList = cms.vstring('Free', 
        'Free', 
        'Free', 
        'TechTr', 
        'IsoEGQ', 
        'NoIsoEGQ', 
        'CenJetQ', 
        'ForJetQ', 
        'TauJetQ', 
        'ESumsQ', 
        'HfQ', 
        'Free', 
        'Free', 
        'Free', 
        'Free', 
        'Free', 
        'MQF4', 
        'MQF3', 
        'MQB2', 
        'MQB1', 
        'MQF8', 
        'MQF7', 
        'MQB6', 
        'MQB5', 
        'MQF12', 
        'MQF11', 
        'MQB10', 
        'MQB9'),
    BoardHexNameMap = cms.vint32(0, 253, 187, 187, 187, 
        187, 187, 187, 187, 221, 
        204, 173),
    ActiveBoardsEvmRecord = cms.vint32(-1, 1, -1, -1, -1, 
        -1, -1, -1, -1, -1, 
        0, -1),
    BoardSlotMap = cms.vint32(17, 10, 9, 13, 14, 
        15, 19, 20, 21, 18, 
        7, 16),
    BoardIndex = cms.vint32(0, 0, 0, 1, 2, 
        3, 4, 5, 6, 0, 
        0, 0)
)


process.PixelCPEGenericESProducer = cms.ESProducer("PixelCPEGenericESProducer",
    eff_charge_cut_lowY = cms.untracked.double(0.0),
    eff_charge_cut_lowX = cms.untracked.double(0.0),
    eff_charge_cut_highX = cms.untracked.double(1.0),
    eff_charge_cut_highY = cms.untracked.double(1.0),
    size_cutY = cms.untracked.double(3.0),
    size_cutX = cms.untracked.double(3.0),
    TanLorentzAnglePerTesla = cms.double(0.106),
    Alpha2Order = cms.bool(True),
    ComponentName = cms.string('PixelCPEGeneric'),
    PixelErrorParametrization = cms.string('NOTcmsim')
)


process.KFFitterForRefitOutsideIn = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('KFFitterForRefitOutsideIn'),
    Estimator = cms.string('Chi2EstimatorForRefit'),
    minHits = cms.int32(3),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('SmartPropagatorAnyRK')
)


process.Chi2EstimatorForMuonTrackLoader = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    MaxChi2 = cms.double(100000.0),
    nSigma = cms.double(3.0),
    ComponentName = cms.string('Chi2EstimatorForMuonTrackLoader')
)


process.CaloTowerHardcodeGeometryEP = cms.ESProducer("CaloTowerHardcodeGeometryEP")


process.myTTRHBuilderWithoutAngle4MixedPairs = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    StripCPE = cms.string('Fake'),
    Matcher = cms.string('StandardMatcher'),
    PixelCPE = cms.string('PixelCPEGeneric'),
    ComponentName = cms.string('TTRHBuilderWithoutAngle4MixedPairs')
)


process.pixellayertriplets = cms.ESProducer("PixelLayerTripletsESProducer",
    FPix = cms.PSet(
        hitErrorRZ = cms.double(0.0036),
        hitErrorRPhi = cms.double(0.0051),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelTriplets'),
        HitProducer = cms.string('siPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    layerList = cms.vstring('BPix1+BPix2+BPix3', 
        'BPix1+BPix2+FPix1_pos', 
        'BPix1+BPix2+FPix1_neg', 
        'BPix1+FPix1_pos+FPix2_pos', 
        'BPix1+FPix1_neg+FPix2_neg'),
    BPix = cms.PSet(
        hitErrorRZ = cms.double(0.006),
        hitErrorRPhi = cms.double(0.0027),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelTriplets'),
        HitProducer = cms.string('siPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    ComponentName = cms.string('PixelLayerTriplets')
)


process.siStripQualityESProducer = cms.ESProducer("SiStripQualityESProducer",
    appendToDataLabel = cms.string(''),
    ThresholdForReducedGranularity = cms.double(0.3),
    ReduceGranularity = cms.bool(True),
    ListOfRecordToMerge = cms.VPSet(cms.PSet(
        record = cms.string('SiStripDetCablingRcd'),
        tag = cms.string('')
    ), 
        cms.PSet(
            record = cms.string('SiStripBadChannelRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadFiberRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadModuleRcd'),
            tag = cms.string('')
        ))
)


process.SteppingHelixPropagatorOpposite = cms.ESProducer("SteppingHelixPropagatorESProducer",
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('oppositeToMomentum'),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    endcapShiftInZNeg = cms.double(0.0),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    returnTangentPlane = cms.bool(True),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    ComponentName = cms.string('SteppingHelixPropagatorOpposite'),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    endcapShiftInZPos = cms.double(0.0)
)


process.DTGeometryESModule = cms.ESProducer("DTGeometryESModule",
    appendToDataLabel = cms.string(''),
    applyAlignment = cms.bool(True),
    alignmentsLabel = cms.string('')
)


process.RKTrackerPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(1.6),
    useRungeKutta = cms.bool(True),
    Mass = cms.double(0.105),
    PropagationDirection = cms.string('alongMomentum'),
    ComponentName = cms.string('RKTrackerPropagator')
)


process.GroupedCkfTrajectoryBuilderP5 = cms.ESProducer("GroupedCkfTrajectoryBuilderESProducer",
    bestHitOnly = cms.bool(True),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    trajectoryFilterName = cms.string('ckfBaseTrajectoryFilterP5'),
    maxCand = cms.int32(5),
    ComponentName = cms.string('GroupedCkfTrajectoryBuilderP5'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    MeasurementTrackerName = cms.string(''),
    minNrOfHitsForRebuild = cms.int32(5),
    lockHits = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    foundHitBonus = cms.double(5.0),
    updator = cms.string('KFUpdator'),
    alwaysUseInvalidHits = cms.bool(True),
    requireSeedHitsInRebuild = cms.bool(True),
    estimator = cms.string('Chi2'),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0)
)


process.myTTRHBuilderWithoutAngle4PixelPairs = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    StripCPE = cms.string('Fake'),
    Matcher = cms.string('StandardMatcher'),
    PixelCPE = cms.string('PixelCPEGeneric'),
    ComponentName = cms.string('TTRHBuilderWithoutAngle4PixelPairs')
)


process.CaloTopologyBuilder = cms.ESProducer("CaloTopologyBuilder")


process.roads = cms.ESProducer("RoadMapMakerESProducer",
    GeometryStructure = cms.string('FullDetector'),
    ComponentName = cms.string(''),
    RingsLabel = cms.string(''),
    WriteOutRoadMapToAsciiFile = cms.untracked.bool(False),
    SeedingType = cms.string('FourRingSeeds'),
    RoadMapAsciiFile = cms.untracked.string('roads.dat')
)


process.KFFittingSmoother = cms.ESProducer("KFFittingSmootherESProducer",
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('KFFitter'),
    ComponentName = cms.string('KFFittingSmoother'),
    Smoother = cms.string('KFSmoother'),
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    MinNumberOfHits = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True)
)


process.RPCConeBuilder = cms.ESProducer("RPCConeBuilder",
    rollConnLP_17_4 = cms.vint32(0, 0, 0),
    rollConnT_14_4 = cms.vint32(-1, -1, -1),
    rollConnT_14_5 = cms.vint32(-1, -1, -1),
    rollConnT_14_0 = cms.vint32(13, 14, -1),
    rollConnT_14_1 = cms.vint32(13, -1, -1),
    rollConnT_14_2 = cms.vint32(14, 15, -1),
    rollConnT_14_3 = cms.vint32(15, 16, -1),
    rollConnT_12_4 = cms.vint32(-1, -1, -1),
    rollConnT_12_5 = cms.vint32(-1, -1, -1),
    rollConnT_12_2 = cms.vint32(12, 13, -1),
    rollConnT_12_3 = cms.vint32(13, 14, -1),
    rollConnT_12_0 = cms.vint32(10, 11, -1),
    rollConnT_12_1 = cms.vint32(11, -1, -1),
    rollConnLP_12_0 = cms.vint32(1, 1, 0),
    rollConnLP_0_3 = cms.vint32(0, 0, 0),
    rollConnT_0_4 = cms.vint32(-1, -1, -1),
    rollConnT_0_5 = cms.vint32(-1, -1, -1),
    rollConnLP_13_2 = cms.vint32(3, 3, 0),
    rollConnT_0_0 = cms.vint32(-1, -1, -1),
    rollConnLP_7_3 = cms.vint32(6, 6, 0),
    lpSizeTower14 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    lpSizeTower15 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    lpSizeTower16 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    lpSizeTower10 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    rollConnT_0_2 = cms.vint32(-1, -1, -1),
    lpSizeTower12 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    lpSizeTower13 = cms.vint32(72, 8, 40, 24, 0, 
        0),
    rollConnLP_7_1 = cms.vint32(3, -3, 0),
    rollConnLP_8_1 = cms.vint32(0, 0, 0),
    rollConnLP_10_4 = cms.vint32(0, 0, 0),
    rollConnLP_8_0 = cms.vint32(0, 5, 0),
    rollConnLP_8_3 = cms.vint32(4, 0, 0),
    rollConnT_16_2 = cms.vint32(-1, -1, -1),
    rollConnT_16_3 = cms.vint32(-1, -1, -1),
    rollConnT_16_0 = cms.vint32(15, 16, -1),
    rollConnT_16_1 = cms.vint32(15, -1, -1),
    rollConnLP_3_0 = cms.vint32(0, 0, 0),
    rollConnT_16_4 = cms.vint32(-1, -1, -1),
    rollConnT_16_5 = cms.vint32(-1, -1, -1),
    rollConnT_15_5 = cms.vint32(-1, -1, -1),
    rollConnT_15_4 = cms.vint32(-1, -1, -1),
    rollConnLP_6_5 = cms.vint32(4, 0, 0),
    rollConnLP_6_4 = cms.vint32(0, 0, 0),
    rollConnLP_6_3 = cms.vint32(0, 0, 0),
    rollConnLP_6_2 = cms.vint32(0, 0, 0),
    rollConnT_8_2 = cms.vint32(9, -9, -1),
    rollConnLP_6_0 = cms.vint32(0, 0, 0),
    rollConnT_13_5 = cms.vint32(-1, -1, -1),
    rollConnT_13_4 = cms.vint32(-1, -1, -1),
    rollConnT_13_3 = cms.vint32(14, 15, -1),
    rollConnT_13_2 = cms.vint32(13, 14, -1),
    rollConnT_13_1 = cms.vint32(12, -1, -1),
    rollConnT_13_0 = cms.vint32(11, 12, -1),
    rollConnLP_4_1 = cms.vint32(3, 0, 0),
    rollConnLP_4_0 = cms.vint32(1, 1, -5),
    rollConnLP_4_3 = cms.vint32(6, 6, 0),
    rollConnLP_4_2 = cms.vint32(5, 5, 5),
    rollConnLP_4_5 = cms.vint32(4, 4, 0),
    rollConnLP_4_4 = cms.vint32(2, 2, 0),
    rollConnT_10_0 = cms.vint32(8, -1, -1),
    rollConnLP_12_4 = cms.vint32(0, 0, 0),
    rollConnT_4_0 = cms.vint32(4, 5, -6),
    rollConnT_4_1 = cms.vint32(4, -1, -1),
    rollConnT_4_2 = cms.vint32(2, 3, 4),
    rollConnT_4_3 = cms.vint32(2, 3, -1),
    rollConnT_4_4 = cms.vint32(4, 5, -1),
    rollConnT_4_5 = cms.vint32(3, 4, -1),
    rollConnLP_8_5 = cms.vint32(0, 0, 0),
    rollConnLP_8_4 = cms.vint32(0, 0, 0),
    rollConnT_6_4 = cms.vint32(-1, -1, -1),
    rollConnT_6_5 = cms.vint32(6, -1, -1),
    rollConnT_6_2 = cms.vint32(-1, -1, -1),
    rollConnT_6_3 = cms.vint32(-1, -1, -1),
    rollConnT_6_0 = cms.vint32(-1, -1, -1),
    rollConnLP_8_2 = cms.vint32(3, -5, 0),
    rollConnLP_5_0 = cms.vint32(1, 1, 1),
    rollConnLP_9_4 = cms.vint32(0, 0, 0),
    rollConnLP_5_1 = cms.vint32(3, -3, 3),
    rollConnLP_3_1 = cms.vint32(3, 0, 0),
    rollConnLP_16_0 = cms.vint32(1, 1, 0),
    rollConnLP_5_2 = cms.vint32(5, 5, 0),
    rollConnT_15_3 = cms.vint32(16, -1, -1),
    rollConnT_2_1 = cms.vint32(2, -1, -1),
    rollConnLP_2_3 = cms.vint32(6, 6, 0),
    rollConnLP_2_2 = cms.vint32(5, 5, 0),
    rollConnLP_2_1 = cms.vint32(3, 0, 0),
    rollConnLP_2_0 = cms.vint32(1, 1, 1),
    rollConnLP_2_5 = cms.vint32(4, 4, 0),
    rollConnLP_2_4 = cms.vint32(2, 2, 2),
    rollConnT_11_1 = cms.vint32(10, -1, -1),
    rollConnT_11_0 = cms.vint32(10, -1, -1),
    rollConnT_11_3 = cms.vint32(12, 13, -1),
    rollConnT_11_2 = cms.vint32(11, 12, -1),
    rollConnT_11_5 = cms.vint32(-1, -1, -1),
    rollConnT_11_4 = cms.vint32(-1, -1, -1),
    rollConnLP_0_5 = cms.vint32(0, 0, 0),
    rollConnLP_0_4 = cms.vint32(0, 0, 0),
    rollConnT_17_1 = cms.vint32(16, -1, -1),
    rollConnT_17_0 = cms.vint32(16, -1, -1),
    rollConnLP_0_1 = cms.vint32(3, 0, 0),
    lpSizeTower6 = cms.vint32(56, 72, 40, 8, 24, 
        0),
    rollConnT_17_5 = cms.vint32(-1, -1, -1),
    rollConnLP_0_2 = cms.vint32(0, 0, 0),
    rollConnT_8_4 = cms.vint32(-1, -1, -1),
    rollConnLP_14_5 = cms.vint32(0, 0, 0),
    rollConnLP_14_4 = cms.vint32(0, 0, 0),
    rollConnLP_14_3 = cms.vint32(4, 4, 0),
    rollConnLP_14_2 = cms.vint32(3, 3, 0),
    rollConnLP_14_1 = cms.vint32(2, 0, 0),
    rollConnLP_14_0 = cms.vint32(1, 1, 0),
    rollConnT_9_5 = cms.vint32(-1, -1, -1),
    rollConnT_9_4 = cms.vint32(-1, -1, -1),
    rollConnLP_7_4 = cms.vint32(2, 2, 0),
    rollConnLP_7_5 = cms.vint32(4, 0, 0),
    rollConnT_9_1 = cms.vint32(8, -1, -1),
    rollConnT_0_1 = cms.vint32(0, -1, -1),
    rollConnT_9_3 = cms.vint32(10, 11, -1),
    rollConnT_0_3 = cms.vint32(-1, -1, -1),
    rollConnT_7_1 = cms.vint32(7, -7, -1),
    rollConnLP_16_1 = cms.vint32(2, 0, 0),
    rollConnT_15_1 = cms.vint32(14, -1, -1),
    rollConnLP_16_3 = cms.vint32(0, 0, 0),
    rollConnLP_16_2 = cms.vint32(0, 0, 0),
    rollConnLP_16_5 = cms.vint32(0, 0, 0),
    rollConnLP_16_4 = cms.vint32(0, 0, 0),
    rollConnT_15_0 = cms.vint32(14, 15, -1),
    rollConnT_2_2 = cms.vint32(1, 2, -1),
    rollConnT_2_3 = cms.vint32(1, 2, -1),
    rollConnT_2_0 = cms.vint32(2, 3, 4),
    rollConnLP_5_3 = cms.vint32(6, 0, 0),
    rollConnLP_5_4 = cms.vint32(2, 2, 2),
    rollConnLP_5_5 = cms.vint32(4, 0, 0),
    rollConnT_2_4 = cms.vint32(2, 3, 4),
    rollConnT_2_5 = cms.vint32(2, 3, -1),
    rollConnT_8_3 = cms.vint32(10, -1, -1),
    rollConnT_5_1 = cms.vint32(5, -6, 6),
    rollConnT_5_0 = cms.vint32(6, 7, 8),
    rollConnT_5_3 = cms.vint32(4, -1, -1),
    rollConnT_5_2 = cms.vint32(4, 5, -1),
    rollConnT_5_5 = cms.vint32(5, -1, -1),
    rollConnT_5_4 = cms.vint32(5, 6, 7),
    rollConnLP_15_1 = cms.vint32(2, 0, 0),
    rollConnT_9_0 = cms.vint32(7, 8, -1),
    rollEnd = cms.int32(17),
    rollConnLP_17_1 = cms.vint32(2, 0, 0),
    rollConnLP_9_1 = cms.vint32(4, 0, 0),
    hwPlaneEnd = cms.int32(5),
    rollConnLP_10_3 = cms.vint32(4, 4, 0),
    rollConnLP_10_2 = cms.vint32(3, 3, 0),
    rollConnLP_10_1 = cms.vint32(2, 0, 0),
    rollConnLP_10_0 = cms.vint32(3, 0, 0),
    rollConnLP_10_5 = cms.vint32(0, 0, 0),
    towerBeg = cms.int32(0),
    rollConnLP_3_2 = cms.vint32(0, 0, 0),
    rollConnLP_3_3 = cms.vint32(0, 0, 0),
    rollConnT_15_2 = cms.vint32(15, 16, -1),
    rollConnT_8_5 = cms.vint32(-1, -1, -1),
    rollConnLP_6_1 = cms.vint32(0, 0, 0),
    rollConnLP_3_4 = cms.vint32(0, 0, 0),
    rollConnLP_3_5 = cms.vint32(0, 0, 0),
    rollConnLP_12_5 = cms.vint32(0, 0, 0),
    rollConnT_10_1 = cms.vint32(9, -1, -1),
    rollConnT_10_2 = cms.vint32(10, 11, -1),
    rollConnT_10_3 = cms.vint32(11, 12, -1),
    rollConnT_10_4 = cms.vint32(-1, -1, -1),
    rollConnT_10_5 = cms.vint32(-1, -1, -1),
    rollConnLP_12_3 = cms.vint32(4, 4, 0),
    rollConnLP_12_2 = cms.vint32(3, 3, 0),
    rollConnLP_1_4 = cms.vint32(2, 2, -2),
    rollConnLP_1_5 = cms.vint32(4, 4, 0),
    rollBeg = cms.int32(0),
    rollConnLP_1_0 = cms.vint32(1, 1, -1),
    rollConnLP_1_1 = cms.vint32(3, 0, 0),
    rollConnLP_1_2 = cms.vint32(5, 5, 0),
    rollConnLP_1_3 = cms.vint32(6, 6, 0),
    rollConnT_9_2 = cms.vint32(9, -9, 10),
    rollConnLP_9_5 = cms.vint32(0, 0, 0),
    rollConnT_7_5 = cms.vint32(7, -1, -1),
    rollConnT_7_4 = cms.vint32(7, 8, -1),
    rollConnLP_9_0 = cms.vint32(5, 3, 0),
    rollConnT_7_2 = cms.vint32(5, 6, -1),
    rollConnLP_9_2 = cms.vint32(3, -5, 3),
    rollConnT_7_0 = cms.vint32(8, 9, -1),
    rollConnLP_13_0 = cms.vint32(1, 1, 0),
    rollConnLP_12_1 = cms.vint32(2, 0, 0),
    lpSizeTower3 = cms.vint32(72, 56, 8, 40, 40, 
        24),
    rollConnT_1_5 = cms.vint32(0, 1, -1),
    rollConnT_1_4 = cms.vint32(0, 1, -2),
    rollConnLP_17_2 = cms.vint32(0, 0, 0),
    rollConnLP_17_3 = cms.vint32(0, 0, 0),
    rollConnLP_9_3 = cms.vint32(4, 4, 0),
    rollConnLP_17_5 = cms.vint32(0, 0, 0),
    rollConnT_1_3 = cms.vint32(0, 1, -1),
    rollConnT_1_2 = cms.vint32(0, 1, -1),
    rollConnT_1_1 = cms.vint32(1, -1, -1),
    lpSizeTower1 = cms.vint32(72, 56, 8, 40, 40, 
        24),
    rollConnT_7_3 = cms.vint32(4, 5, -1),
    rollConnT_17_3 = cms.vint32(-1, -1, -1),
    rollConnLP_13_5 = cms.vint32(0, 0, 0),
    rollConnLP_7_2 = cms.vint32(5, 5, 0),
    rollConnT_17_2 = cms.vint32(-1, -1, -1),
    rollConnT_3_3 = cms.vint32(-1, -1, -1),
    rollConnT_3_2 = cms.vint32(-1, -1, -1),
    rollConnT_3_1 = cms.vint32(3, -1, -1),
    rollConnT_3_0 = cms.vint32(-1, -1, -1),
    rollConnT_6_1 = cms.vint32(-1, -1, -1),
    rollConnT_3_5 = cms.vint32(-1, -1, -1),
    rollConnT_3_4 = cms.vint32(-1, -1, -1),
    rollConnT_1_0 = cms.vint32(0, 1, -2),
    rollConnLP_17_0 = cms.vint32(1, 0, 0),
    rollConnLP_0_0 = cms.vint32(0, 0, 0),
    rollConnT_8_0 = cms.vint32(-1, 7, -1),
    hwPlaneBeg = cms.int32(0),
    rollConnT_17_4 = cms.vint32(-1, -1, -1),
    rollConnLP_11_2 = cms.vint32(3, 3, 0),
    rollConnLP_11_3 = cms.vint32(4, 4, 0),
    rollConnLP_11_0 = cms.vint32(1, 0, 0),
    rollConnLP_11_1 = cms.vint32(2, 0, 0),
    rollConnLP_11_4 = cms.vint32(0, 0, 0),
    rollConnLP_11_5 = cms.vint32(0, 0, 0),
    rollConnT_8_1 = cms.vint32(-1, -1, -1),
    rollConnLP_7_0 = cms.vint32(1, 1, 0),
    lpSizeTower8 = cms.vint32(72, 24, 40, 8, 0, 
        0),
    lpSizeTower9 = cms.vint32(72, 8, 40, 0, 0, 
        0),
    rollConnLP_13_4 = cms.vint32(0, 0, 0),
    lpSizeTower7 = cms.vint32(72, 56, 40, 8, 24, 
        0),
    lpSizeTower4 = cms.vint32(72, 56, 8, 40, 40, 
        24),
    lpSizeTower5 = cms.vint32(72, 56, 40, 8, 40, 
        24),
    lpSizeTower2 = cms.vint32(72, 56, 8, 40, 40, 
        24),
    rollConnLP_13_1 = cms.vint32(2, 0, 0),
    lpSizeTower0 = cms.vint32(72, 56, 8, 40, 40, 
        24),
    rollConnLP_13_3 = cms.vint32(4, 4, 0),
    rollConnLP_15_0 = cms.vint32(1, 1, 0),
    rollConnLP_15_4 = cms.vint32(0, 0, 0),
    rollConnLP_15_5 = cms.vint32(0, 0, 0),
    rollConnLP_15_2 = cms.vint32(3, 3, 0),
    rollConnLP_15_3 = cms.vint32(4, 0, 0),
    towerEnd = cms.int32(16),
    lpSizeTower11 = cms.vint32(72, 8, 40, 24, 0, 
        0)
)


process.SteppingHelixPropagatorL2Opposite = cms.ESProducer("SteppingHelixPropagatorESProducer",
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('oppositeToMomentum'),
    useTuningForL2Speed = cms.bool(True),
    ComponentName = cms.string('SteppingHelixPropagatorL2Opposite'),
    useIsYokeFlag = cms.bool(True),
    endcapShiftInZNeg = cms.double(0.0),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    endcapShiftInZPos = cms.double(0.0),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    useMatVolumes = cms.bool(True),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    returnTangentPlane = cms.bool(True)
)


process.PixelCPEInitialESProducer = cms.ESProducer("PixelCPEInitialESProducer",
    ComponentName = cms.string('PixelCPEInitial'),
    Alpha2Order = cms.bool(True),
    PixelErrorParametrization = cms.string('NOTcmsim')
)


process.ckfBaseTrajectoryFilterP5 = cms.ESProducer("TrajectoryFilterESProducer",
    filterPset = cms.PSet(
        minimumNumberOfHits = cms.int32(5),
        minPt = cms.double(0.5),
        minHitsMinPt = cms.int32(3),
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        maxLostHits = cms.int32(4),
        maxNumberOfHits = cms.int32(-1),
        maxConsecLostHits = cms.int32(3),
        nSigmaMinPt = cms.double(5.0),
        chargeSignificance = cms.double(-1.0)
    ),
    ComponentName = cms.string('ckfBaseTrajectoryFilterP5')
)


process.SmartPropagator = cms.ESProducer("SmartPropagatorESProducer",
    Epsilon = cms.double(5.0),
    TrackerPropagator = cms.string('PropagatorWithMaterial'),
    MuonPropagator = cms.string('SteppingHelixPropagatorAlong'),
    PropagationDirection = cms.string('alongMomentum'),
    ComponentName = cms.string('SmartPropagator')
)


process.pixellayerpairs = cms.ESProducer("PixelLayerPairsESProducer",
    FPix = cms.PSet(
        hitErrorRZ = cms.double(0.0036),
        hitErrorRPhi = cms.double(0.0051),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelPairs'),
        HitProducer = cms.string('siPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    layerList = cms.vstring('BPix1+BPix2', 
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
        'FPix1_neg+FPix2_neg'),
    BPix = cms.PSet(
        hitErrorRZ = cms.double(0.006),
        hitErrorRPhi = cms.double(0.0027),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelPairs'),
        HitProducer = cms.string('siPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    ComponentName = cms.string('PixelLayerPairs')
)


process.l1GtStableParameters = cms.ESProducer("L1GtStableParametersTrivialProducer",
    NumberL1IsoEG = cms.uint32(4),
    NumberL1JetCounts = cms.uint32(12),
    UnitLength = cms.int32(8),
    NumberL1ForJet = cms.uint32(4),
    IfCaloEtaNumberBits = cms.uint32(4),
    IfMuEtaNumberBits = cms.uint32(6),
    NumberL1TauJet = cms.uint32(4),
    NumberPsbBoards = cms.int32(7),
    NumberConditionChips = cms.uint32(2),
    NumberL1Mu = cms.uint32(4),
    NumberL1CenJet = cms.uint32(4),
    NumberPhysTriggers = cms.uint32(128),
    PinsOnConditionChip = cms.uint32(96),
    NumberTechnicalTriggers = cms.uint32(64),
    OrderConditionChip = cms.vint32(2, 1),
    NumberPhysTriggersExtended = cms.uint32(64),
    WordLength = cms.int32(64),
    NumberL1NoIsoEG = cms.uint32(4)
)


process.OppositeAnalyticalPropagator = cms.ESProducer("AnalyticalPropagatorESProducer",
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('AnalyticalPropagatorOpposite'),
    PropagationDirection = cms.string('oppositeToMomentum')
)


process.fourthCkfTrajectoryFilter = cms.ESProducer("TrajectoryFilterESProducer",
    filterPset = cms.PSet(
        minimumNumberOfHits = cms.int32(5),
        minPt = cms.double(0.9),
        minHitsMinPt = cms.int32(3),
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        maxLostHits = cms.int32(0),
        maxNumberOfHits = cms.int32(-1),
        maxConsecLostHits = cms.int32(1),
        nSigmaMinPt = cms.double(5.0),
        chargeSignificance = cms.double(-1.0)
    ),
    ComponentName = cms.string('fourthCkfTrajectoryFilter')
)


process.seclayertriplets = cms.ESProducer("PixelLayerTripletsESProducer",
    FPix = cms.PSet(
        hitErrorRZ = cms.double(0.0036),
        hitErrorRPhi = cms.double(0.0051),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelTriplets'),
        HitProducer = cms.string('secPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    layerList = cms.vstring('BPix1+BPix2+BPix3', 
        'BPix1+BPix2+FPix1_pos', 
        'BPix1+BPix2+FPix1_neg', 
        'BPix1+FPix1_pos+FPix2_pos', 
        'BPix1+FPix1_neg+FPix2_neg'),
    BPix = cms.PSet(
        hitErrorRZ = cms.double(0.006),
        hitErrorRPhi = cms.double(0.0027),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelTriplets'),
        HitProducer = cms.string('secPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    ComponentName = cms.string('SecLayerTriplets')
)


process.CSCGeometryESModule = cms.ESProducer("CSCGeometryESModule",
    appendToDataLabel = cms.string(''),
    debugV = cms.untracked.bool(False),
    useGangedStripsInME1a = cms.bool(True),
    alignmentsLabel = cms.string(''),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True),
    useCentreTIOffsets = cms.bool(False),
    applyAlignment = cms.bool(True)
)


process.KFSmootherForRefitOutsideIn = cms.ESProducer("KFTrajectorySmootherESProducer",
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3),
    ComponentName = cms.string('KFSmootherForRefitOutsideIn'),
    Estimator = cms.string('Chi2EstimatorForRefit'),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('SmartPropagatorRK')
)


process.navigationSchoolESProducer = cms.ESProducer("NavigationSchoolESProducer",
    ComponentName = cms.string('SimpleNavigationSchool')
)


process.SteppingHelixPropagatorAlong = cms.ESProducer("SteppingHelixPropagatorESProducer",
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('alongMomentum'),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    endcapShiftInZNeg = cms.double(0.0),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    returnTangentPlane = cms.bool(True),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    ComponentName = cms.string('SteppingHelixPropagatorAlong'),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    endcapShiftInZPos = cms.double(0.0)
)


process.GsfElectronFittingSmoother = cms.ESProducer("KFFittingSmootherESProducer",
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('GsfTrajectoryFitter'),
    ComponentName = cms.string('GsfElectronFittingSmoother'),
    Smoother = cms.string('GsfTrajectorySmoother'),
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    MinNumberOfHits = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True)
)


process.secCkfTrajectoryBuilder = cms.ESProducer("GroupedCkfTrajectoryBuilderESProducer",
    bestHitOnly = cms.bool(True),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    trajectoryFilterName = cms.string('secCkfTrajectoryFilter'),
    maxCand = cms.int32(5),
    ComponentName = cms.string('secCkfTrajectoryBuilder'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    MeasurementTrackerName = cms.string('secMeasurementTracker'),
    minNrOfHitsForRebuild = cms.int32(5),
    lockHits = cms.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    foundHitBonus = cms.double(5.0),
    updator = cms.string('KFUpdator'),
    alwaysUseInvalidHits = cms.bool(True),
    requireSeedHitsInRebuild = cms.bool(True),
    estimator = cms.string('Chi2'),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0)
)


process.siStripGainESProducer = cms.ESProducer("SiStripGainESProducer",
    printDebug = cms.untracked.bool(False),
    appendToDataLabel = cms.string(''),
    APVGain = cms.string(''),
    AutomaticNormalization = cms.bool(False),
    NormalizationFactor = cms.double(1.0)
)


process.Chi2EstimatorForRefit = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    MaxChi2 = cms.double(100000.0),
    nSigma = cms.double(3.0),
    ComponentName = cms.string('Chi2EstimatorForRefit')
)


process.RPCGeometryESModule = cms.ESProducer("RPCGeometryESModule",
    compatibiltyWith11 = cms.untracked.bool(True)
)


process.idealForDigiDTGeometry = cms.ESProducer("DTGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    applyAlignment = cms.bool(False),
    alignmentsLabel = cms.string('fakeForIdeal')
)


process.ttrhbwr = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    StripCPE = cms.string('StripCPEfromTrackAngle'),
    Matcher = cms.string('StandardMatcher'),
    PixelCPE = cms.string('PixelCPEGeneric'),
    ComponentName = cms.string('WithTrackAngle')
)


process.SmartPropagatorAny = cms.ESProducer("SmartPropagatorESProducer",
    Epsilon = cms.double(5.0),
    TrackerPropagator = cms.string('PropagatorWithMaterial'),
    MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
    PropagationDirection = cms.string('alongMomentum'),
    ComponentName = cms.string('SmartPropagatorAny')
)


process.TrackerRecoGeometryESProducer = cms.ESProducer("TrackerRecoGeometryESProducer")


process.GsfTrajectorySmoother = cms.ESProducer("GsfTrajectorySmootherESProducer",
    Merger = cms.string('CloseComponentsMerger5D'),
    ComponentName = cms.string('GsfTrajectorySmoother'),
    ErrorRescaling = cms.double(100.0),
    MaterialEffectsUpdator = cms.string('ElectronMaterialEffects'),
    GeometricalPropagator = cms.string('bwdAnalyticalPropagator')
)


process.TTRHBuilderAngleAndTemplate = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    StripCPE = cms.string('StripCPEfromTrackAngle'),
    Matcher = cms.string('StandardMatcher'),
    PixelCPE = cms.string('PixelCPETemplateReco'),
    ComponentName = cms.string('WithAngleAndTemplate')
)


process.DAFTrajectorySmoother = cms.ESProducer("KFTrajectorySmootherESProducer",
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3),
    ComponentName = cms.string('DAFSmoother'),
    Estimator = cms.string('MRHChi2'),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.l1RPCHwConfig = cms.ESProducer("RPCTriggerHwConfig",
    disableCrates = cms.vint32(),
    enableTowers = cms.vint32(),
    enableCrates = cms.vint32(),
    disableAll = cms.bool(False),
    lastBX = cms.int32(0),
    firstBX = cms.int32(0),
    disableTowers = cms.vint32()
)


process.SiStripRecHitMatcherESProducer = cms.ESProducer("SiStripRecHitMatcherESProducer",
    ComponentName = cms.string('StandardMatcher'),
    NSigmaInside = cms.double(3.0)
)


process.L1CaloInputScalesProducer = cms.ESProducer("L1CaloInputScalesProducer",
    L1HcalEtThresholds = (cms.vdouble(0.0, 0.7, 0.9, 1.1, 1.2, 1.4, 1.6, 1.8, 1.9, 2.1, 2.3, 2.6, 2.9, 3.2, 3.4, 3.6, 4.0, 4.3, 4.7, 5.0, 5.3, 5.8, 6.3, 6.5, 6.9, 7.4, 7.8, 8.2, 8.8, 9.2, 9.8, 10.3, 10.8, 11.3, 11.5, 11.8, 12.4, 12.8, 13.4, 14.0, 14.4, 14.9, 15.4, 15.9, 16.4, 17.0, 17.5, 17.9, 18.5, 18.9, 19.5, 19.9, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.6, 24.2, 24.9, 25.6, 26.1, 27.0, 27.6, 28.1, 28.9, 29.4, 30.1, 30.9, 31.4, 32.2, 32.7, 33.3, 34.2, 34.7, 35.4, 36.3, 37.0, 37.5, 38.4, 39.2, 39.8, 40.5, 41.4, 42.0, 42.6, 43.5, 44.4, 44.9, 45.5, 46.5, 47.4, 47.9, 48.5, 49.5, 50.4, 51.1, 51.7, 52.5, 53.4, 54.4, 55.0, 55.5, 56.4, 57.4, 58.4, 58.9, 59.4, 60.4, 61.4, 62.2, 63.0, 63.7, 64.4, 65.3, 66.2, 67.2, 67.7, 67.9, 68.4, 69.4, 70.4, 71.4, 72.1, 72.6, 73.4, 74.4, 75.3, 76.2, 76.7, 77.4, 78.3, 79.2, 80.2, 80.9, 81.4, 82.2, 83.2, 84.2, 85.1, 85.6, 86.2, 87.2, 88.1, 89.0, 89.7, 90.3, 91.1, 92.0, 93.0, 93.9, 94.4, 95.0, 96.0, 96.9, 97.9, 98.6, 99.1, 99.9, 100.9, 101.9, 102.7, 103.3, 103.9, 104.9, 105.7, 106.7, 107.4, 108.0, 108.8, 109.7, 110.7, 111.6, 112.1, 112.7, 113.7, 114.6, 115.6, 116.3, 116.8, 117.6, 118.6, 119.5, 120.4, 121.0, 121.6, 122.5, 123.4, 124.4, 125.1, 125.6, 126.4, 127.4, 128.4, 129.3, 130.2, 131.2, 131.7, 132.4, 133.3, 134.2, 135.2, 136.2, 137.0, 138.0, 139.0, 139.9, 140.5, 141.1, 142.0, 142.9, 143.9, 144.8, 145.7, 146.7, 147.7, 148.5, 149.2, 149.9, 150.7, 151.5, 152.5, 153.5, 154.4, 155.3, 156.3, 157.2, 158.0, 158.6, 159.3, 160.2, 161.2, 162.2, 163.0, 164.0, 165.0, 165.9, 166.8, 167.4, 168.0, 168.9, 169.8, 170.8, 171.7, 172.7, 173.6, 174.5, 175.5, 176.1, 176.7, 177.5, 178.5, 179.5, 180.4)+cms.vdouble(180.9, 0.0, 0.7, 0.9, 1.1, 1.2, 1.4, 1.6, 1.8, 1.9, 2.1, 2.3, 2.5, 2.9, 3.2, 3.3, 3.6, 3.9, 4.3, 4.7, 4.9, 5.3, 5.8, 6.2, 6.5, 6.8, 7.4, 7.7, 8.2, 8.7, 9.1, 9.7, 10.2, 10.7, 11.2, 11.4, 11.8, 12.3, 12.7, 13.3, 13.9, 14.3, 14.8, 15.3, 15.8, 16.2, 16.8, 17.4, 17.8, 18.3, 18.8, 19.3, 19.7, 20.4, 20.9, 21.3, 21.9, 22.3, 22.8, 23.4, 24.0, 24.7, 25.4, 25.9, 26.8, 27.4, 27.9, 28.7, 29.2, 29.9, 30.6, 31.2, 31.9, 32.5, 33.1, 34.0, 34.5, 35.1, 36.1, 36.7, 37.2, 38.1, 38.9, 39.5, 40.2, 41.1, 41.7, 42.3, 43.2, 44.1, 44.6, 45.2, 46.2, 47.0, 47.6, 48.2, 49.1, 50.0, 50.7, 51.3, 52.1, 53.0, 54.0, 54.6, 55.1, 56.0, 57.0, 57.9, 58.4, 59.0, 59.9, 60.9, 61.8, 62.6, 63.2, 63.9, 64.8, 65.7, 66.7, 67.2, 67.4, 67.9, 68.9, 69.9, 70.8, 71.5, 72.0, 72.8, 73.8, 74.8, 75.6, 76.2, 76.8, 77.7, 78.6, 79.6, 80.3, 80.8, 81.6, 82.6, 83.5, 84.4, 84.9, 85.6, 86.5, 87.4, 88.4, 89.1, 89.6, 90.4, 91.3, 92.3, 93.2, 93.7, 94.3, 95.3, 96.2, 97.1, 97.8, 98.4, 99.2, 100.1, 101.1, 102.0, 102.5, 103.1, 104.1, 105.0, 105.9, 106.6, 107.1, 107.9, 108.9, 109.9, 110.7, 111.3, 111.9, 112.8, 113.7, 114.7, 115.4, 115.9, 116.7, 117.7, 118.6, 119.5, 120.0, 120.7, 121.6, 122.5, 123.5, 124.2, 124.7, 125.5, 126.5, 127.4, 128.3, 129.3, 130.2, 130.8, 131.4, 132.3, 133.2, 134.2, 135.1, 136.0, 137.0, 137.9, 138.8, 139.4, 140.1, 140.9, 141.8, 142.8, 143.7, 144.6, 145.6, 146.5, 147.4, 148.1, 148.7, 149.5, 150.4, 151.4, 152.3, 153.2, 154.2, 155.1, 156.0, 156.8, 157.4, 158.1, 159.0, 160.0, 160.9, 161.8, 162.8, 163.7, 164.6, 165.5, 166.1, 166.7, 167.6, 168.6, 169.5, 170.4, 171.4, 172.3, 173.2, 174.2, 174.8, 175.3, 176.2, 177.2, 178.1)+cms.vdouble(179.0, 179.5, 0.0, 0.7, 0.9, 1.0, 1.2, 1.4, 1.6, 1.7, 1.9, 2.1, 2.2, 2.5, 2.9, 3.1, 3.3, 3.5, 3.9, 4.2, 4.6, 4.8, 5.2, 5.7, 6.1, 6.4, 6.7, 7.3, 7.6, 8.0, 8.6, 9.0, 9.6, 10.0, 10.5, 11.1, 11.2, 11.6, 12.1, 12.5, 13.1, 13.7, 14.1, 14.6, 15.0, 15.6, 16.0, 16.6, 17.1, 17.5, 18.1, 18.5, 19.0, 19.5, 20.1, 20.6, 21.0, 21.5, 22.0, 22.5, 23.1, 23.7, 24.4, 25.0, 25.5, 26.4, 27.0, 27.5, 28.3, 28.8, 29.5, 30.2, 30.7, 31.5, 32.0, 32.6, 33.5, 34.0, 34.6, 35.5, 36.1, 36.7, 37.5, 38.3, 38.9, 39.6, 40.5, 41.1, 41.7, 42.5, 43.4, 43.9, 44.5, 45.5, 46.3, 46.9, 47.5, 48.4, 49.3, 50.0, 50.6, 51.3, 52.2, 53.2, 53.8, 54.3, 55.2, 56.1, 57.1, 57.6, 58.1, 59.0, 60.0, 60.9, 61.6, 62.2, 62.9, 63.8, 64.7, 65.7, 66.2, 66.4, 66.9, 67.9, 68.8, 69.8, 70.5, 71.0, 71.8, 72.7, 73.7, 74.5, 75.0, 75.6, 76.6, 77.5, 78.4, 79.1, 79.6, 80.4, 81.3, 82.3, 83.2, 83.7, 84.3, 85.2, 86.1, 87.1, 87.7, 88.3, 89.0, 90.0, 90.9, 91.8, 92.3, 92.9, 93.9, 94.7, 95.7, 96.4, 96.9, 97.7, 98.6, 99.6, 100.5, 101.0, 101.6, 102.5, 103.4, 104.3, 105.0, 105.6, 106.3, 107.3, 108.2, 109.1, 109.6, 110.2, 111.2, 112.0, 113.0, 113.7, 114.2, 115.0, 115.9, 116.9, 117.7, 118.3, 118.9, 119.8, 120.7, 121.6, 122.3, 122.8, 123.6, 124.6, 125.5, 126.4, 127.3, 128.3, 128.8, 129.4, 130.4, 131.2, 132.2, 133.1, 134.0, 134.9, 135.9, 136.8, 137.4, 138.0, 138.8, 139.7, 140.6, 141.6, 142.5, 143.4, 144.4, 145.2, 145.9, 146.5, 147.3, 148.2, 149.1, 150.1, 150.9, 151.9, 152.8, 153.7, 154.5, 155.1, 155.8, 156.6, 157.6, 158.5, 159.4, 160.4, 161.3, 162.2, 163.0, 163.6, 164.2, 165.1, 166.1, 167.0, 167.9, 168.8, 169.8, 170.6, 171.6, 172.2, 172.7, 173.6, 174.5)+cms.vdouble(175.5, 176.4, 176.9, 0.0, 0.7, 0.8, 1.0, 1.2, 1.4, 1.5, 1.7, 1.9, 2.0, 2.2, 2.5, 2.8, 3.0, 3.2, 3.5, 3.8, 4.1, 4.5, 4.7, 5.1, 5.6, 6.0, 6.3, 6.6, 7.1, 7.4, 7.9, 8.4, 8.8, 9.4, 9.8, 10.3, 10.8, 11.0, 11.3, 11.8, 12.3, 12.9, 13.4, 13.8, 14.3, 14.7, 15.2, 15.6, 16.2, 16.7, 17.2, 17.7, 18.1, 18.6, 19.0, 19.6, 20.1, 20.5, 21.1, 21.5, 22.0, 22.6, 23.2, 23.8, 24.4, 24.9, 25.8, 26.4, 26.9, 27.6, 28.2, 28.8, 29.5, 30.0, 30.8, 31.3, 31.9, 32.7, 33.2, 33.8, 34.7, 35.3, 35.8, 36.7, 37.5, 38.0, 38.7, 39.6, 40.2, 40.8, 41.6, 42.4, 43.0, 43.5, 44.5, 45.3, 45.8, 46.4, 47.3, 48.2, 48.9, 49.5, 50.2, 51.1, 52.0, 52.6, 53.1, 53.9, 54.9, 55.8, 56.3, 56.8, 57.7, 58.7, 59.5, 60.3, 60.9, 61.6, 62.4, 63.3, 64.3, 64.8, 64.9, 65.4, 66.4, 67.3, 68.2, 68.9, 69.4, 70.2, 71.1, 72.0, 72.9, 73.4, 74.0, 74.9, 75.8, 76.7, 77.4, 77.9, 78.6, 79.6, 80.5, 81.3, 81.8, 82.4, 83.4, 84.2, 85.1, 85.8, 86.3, 87.1, 88.0, 88.9, 89.8, 90.3, 90.9, 91.8, 92.7, 93.6, 94.3, 94.8, 95.5, 96.5, 97.4, 98.2, 98.8, 99.3, 100.3, 101.1, 102.1, 102.7, 103.2, 104.0, 104.9, 105.9, 106.7, 107.2, 107.8, 108.7, 109.6, 110.5, 111.2, 111.7, 112.5, 113.4, 114.3, 115.2, 115.7, 116.3, 117.2, 118.0, 119.0, 119.6, 120.1, 120.9, 121.8, 122.8, 123.6, 124.5, 125.5, 126.0, 126.6, 127.5, 128.3, 129.3, 130.2, 131.1, 132.0, 132.9, 133.8, 134.3, 134.9, 135.8, 136.6, 137.6, 138.5, 139.3, 140.3, 141.2, 142.0, 142.7, 143.3, 144.1, 144.9, 145.8, 146.8, 147.6, 148.6, 149.5, 150.3, 151.1, 151.7, 152.4, 153.2, 154.1, 155.1, 155.9, 156.8, 157.8, 158.6, 159.5, 160.1, 160.6, 161.5, 162.4, 163.4, 164.2, 165.1, 166.1, 166.9, 167.8, 168.4, 168.9, 169.8)+cms.vdouble(170.7, 171.6, 172.5, 173.0, 0.0, 0.7, 0.8, 1.0, 1.1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.4, 2.7, 3.0, 3.1, 3.4, 3.7, 4.0, 4.4, 4.6, 4.9, 5.4, 5.8, 6.1, 6.4, 6.9, 7.2, 7.6, 8.1, 8.5, 9.1, 9.5, 10.0, 10.5, 10.7, 11.0, 11.5, 11.9, 12.5, 13.0, 13.4, 13.9, 14.3, 14.8, 15.2, 15.8, 16.3, 16.7, 17.2, 17.6, 18.1, 18.5, 19.1, 19.5, 20.0, 20.4, 20.9, 21.4, 21.9, 22.5, 23.2, 23.7, 24.2, 25.0, 25.6, 26.1, 26.9, 27.3, 28.0, 28.7, 29.2, 29.9, 30.4, 31.0, 31.8, 32.3, 32.9, 33.8, 34.3, 34.8, 35.6, 36.4, 37.0, 37.6, 38.4, 39.0, 39.6, 40.4, 41.2, 41.7, 42.3, 43.2, 44.0, 44.5, 45.1, 46.0, 46.8, 47.5, 48.0, 48.8, 49.6, 50.5, 51.1, 51.6, 52.4, 53.3, 54.2, 54.7, 55.2, 56.1, 57.0, 57.8, 58.6, 59.1, 59.8, 60.6, 61.5, 62.4, 62.9, 63.1, 63.6, 64.5, 65.4, 66.3, 66.9, 67.4, 68.2, 69.1, 70.0, 70.8, 71.3, 71.9, 72.8, 73.6, 74.5, 75.1, 75.6, 76.4, 77.3, 78.2, 79.0, 79.5, 80.1, 81.0, 81.8, 82.7, 83.4, 83.9, 84.6, 85.5, 86.4, 87.2, 87.7, 88.3, 89.2, 90.0, 90.9, 91.6, 92.1, 92.8, 93.7, 94.6, 95.4, 95.9, 96.5, 97.4, 98.2, 99.1, 99.8, 100.3, 101.0, 101.9, 102.8, 103.6, 104.1, 104.7, 105.6, 106.4, 107.3, 108.0, 108.5, 109.2, 110.1, 111.0, 111.9, 112.3, 112.9, 113.8, 114.6, 115.6, 116.2, 116.7, 117.4, 118.3, 119.2, 120.1, 121.0, 121.9, 122.4, 122.9, 123.8, 124.7, 125.6, 126.5, 127.3, 128.2, 129.1, 129.9, 130.5, 131.1, 131.9, 132.7, 133.6, 134.5, 135.3, 136.2, 137.1, 138.0, 138.6, 139.2, 139.9, 140.8, 141.7, 142.6, 143.4, 144.3, 145.2, 146.0, 146.8, 147.3, 148.0, 148.8, 149.7, 150.6, 151.4, 152.3, 153.2, 154.1, 154.9, 155.5, 156.0, 156.9, 157.8, 158.7, 159.5, 160.4, 161.3, 162.1, 163.0, 163.6, 164.1)+cms.vdouble(164.9, 165.8, 166.7, 167.5, 168.0, 0.0, 0.6, 0.8, 1.0, 1.1, 1.3, 1.4, 1.6, 1.7, 1.9, 2.1, 2.3, 2.6, 2.9, 3.0, 3.2, 3.6, 3.9, 4.2, 4.4, 4.8, 5.2, 5.6, 5.9, 6.2, 6.7, 7.0, 7.4, 7.8, 8.2, 8.8, 9.2, 9.7, 10.1, 10.3, 10.6, 11.1, 11.5, 12.0, 12.5, 12.9, 13.4, 13.8, 14.3, 14.7, 15.2, 15.7, 16.1, 16.6, 17.0, 17.4, 17.8, 18.4, 18.9, 19.3, 19.7, 20.1, 20.6, 21.2, 21.7, 22.3, 22.9, 23.4, 24.2, 24.7, 25.2, 25.9, 26.4, 27.0, 27.7, 28.1, 28.8, 29.3, 29.9, 30.7, 31.1, 31.7, 32.6, 33.1, 33.6, 34.4, 35.1, 35.7, 36.3, 37.1, 37.6, 38.2, 39.0, 39.8, 40.3, 40.8, 41.7, 42.5, 43.0, 43.5, 44.4, 45.2, 45.8, 46.4, 47.1, 47.9, 48.7, 49.3, 49.8, 50.6, 51.4, 52.3, 52.8, 53.3, 54.1, 55.0, 55.8, 56.5, 57.1, 57.7, 58.5, 59.4, 60.2, 60.7, 60.9, 61.3, 62.2, 63.1, 64.0, 64.6, 65.1, 65.8, 66.7, 67.5, 68.3, 68.8, 69.3, 70.2, 71.0, 71.9, 72.5, 73.0, 73.7, 74.6, 75.4, 76.2, 76.7, 77.3, 78.1, 78.9, 79.8, 80.4, 80.9, 81.6, 82.5, 83.4, 84.2, 84.6, 85.2, 86.1, 86.9, 87.7, 88.4, 88.8, 89.6, 90.4, 91.3, 92.1, 92.6, 93.1, 94.0, 94.8, 95.7, 96.3, 96.8, 97.5, 98.4, 99.2, 100.0, 100.5, 101.0, 101.9, 102.7, 103.6, 104.2, 104.7, 105.4, 106.3, 107.1, 107.9, 108.4, 109.0, 109.8, 110.6, 111.5, 112.1, 112.6, 113.3, 114.2, 115.1, 115.9, 116.7, 117.6, 118.1, 118.6, 119.5, 120.3, 121.2, 122.0, 122.8, 123.7, 124.6, 125.4, 125.9, 126.5, 127.3, 128.1, 128.9, 129.8, 130.6, 131.5, 132.4, 133.1, 133.8, 134.3, 135.0, 135.8, 136.7, 137.6, 138.4, 139.2, 140.1, 140.9, 141.6, 142.2, 142.8, 143.6, 144.5, 145.3, 146.1, 147.0, 147.9, 148.7, 149.5, 150.0, 150.6, 151.4, 152.2, 153.1, 153.9, 154.8, 155.7, 156.4, 157.3, 157.9)+cms.vdouble(158.3, 159.1, 160.0, 160.9, 161.7, 162.2, 0.0, 0.6, 0.8, 0.9, 1.1, 1.2, 1.4, 1.5, 1.7, 1.8, 2.0, 2.2, 2.5, 2.7, 2.9, 3.1, 3.4, 3.7, 4.0, 4.3, 4.6, 5.0, 5.4, 5.6, 5.9, 6.4, 6.7, 7.1, 7.5, 7.9, 8.4, 8.8, 9.3, 9.7, 9.9, 10.2, 10.6, 11.0, 11.6, 12.0, 12.4, 12.8, 13.2, 13.7, 14.1, 14.6, 15.1, 15.4, 15.9, 16.3, 16.7, 17.1, 17.6, 18.1, 18.5, 18.9, 19.3, 19.8, 20.3, 20.8, 21.4, 22.0, 22.4, 23.2, 23.7, 24.2, 24.9, 25.3, 25.9, 26.5, 27.0, 27.7, 28.1, 28.7, 29.4, 29.9, 30.4, 31.2, 31.8, 32.2, 33.0, 33.7, 34.2, 34.8, 35.6, 36.1, 36.6, 37.4, 38.2, 38.6, 39.1, 40.0, 40.7, 41.2, 41.7, 42.6, 43.3, 43.9, 44.5, 45.2, 45.9, 46.8, 47.3, 47.7, 48.5, 49.3, 50.2, 50.6, 51.1, 51.9, 52.8, 53.5, 54.2, 54.7, 55.3, 56.1, 56.9, 57.8, 58.2, 58.4, 58.8, 59.7, 60.5, 61.3, 62.0, 62.4, 63.1, 63.9, 64.8, 65.5, 66.0, 66.5, 67.4, 68.1, 68.9, 69.6, 70.0, 70.7, 71.5, 72.4, 73.1, 73.6, 74.1, 75.0, 75.7, 76.5, 77.2, 77.6, 78.3, 79.1, 80.0, 80.7, 81.2, 81.7, 82.6, 83.3, 84.2, 84.8, 85.2, 85.9, 86.7, 87.6, 88.3, 88.8, 89.3, 90.2, 90.9, 91.8, 92.4, 92.8, 93.5, 94.3, 95.2, 95.9, 96.4, 96.9, 97.8, 98.5, 99.4, 100.0, 100.4, 101.1, 101.9, 102.8, 103.5, 104.0, 104.5, 105.4, 106.1, 107.0, 107.6, 108.0, 108.7, 109.5, 110.4, 111.1, 112.0, 112.8, 113.3, 113.8, 114.6, 115.4, 116.2, 117.1, 117.8, 118.7, 119.5, 120.3, 120.8, 121.3, 122.1, 122.8, 123.7, 124.5, 125.3, 126.1, 126.9, 127.7, 128.3, 128.9, 129.5, 130.3, 131.1, 132.0, 132.7, 133.6, 134.4, 135.2, 135.8, 136.4, 137.0, 137.7, 138.6, 139.4, 140.2, 141.0, 141.8, 142.6, 143.4, 143.9, 144.4, 145.2, 146.0, 146.9, 147.6, 148.5, 149.3, 150.1, 150.9)+cms.vdouble(151.4, 151.9, 152.6, 153.5, 154.3, 155.1, 155.5, 0.0, 0.6, 0.7, 0.9, 1.0, 1.2, 1.3, 1.5, 1.6, 1.7, 1.9, 2.1, 2.4, 2.6, 2.8, 3.0, 3.3, 3.6, 3.8, 4.1, 4.4, 4.8, 5.1, 5.4, 5.7, 6.1, 6.4, 6.7, 7.2, 7.5, 8.0, 8.4, 8.8, 9.3, 9.4, 9.7, 10.2, 10.5, 11.0, 11.5, 11.8, 12.3, 12.6, 13.1, 13.4, 13.9, 14.4, 14.7, 15.2, 15.5, 16.0, 16.3, 16.8, 17.3, 17.6, 18.1, 18.4, 18.9, 19.4, 19.9, 20.4, 21.0, 21.4, 22.1, 22.6, 23.1, 23.7, 24.1, 24.7, 25.3, 25.7, 26.4, 26.8, 27.3, 28.1, 28.5, 29.0, 29.8, 30.3, 30.7, 31.5, 32.1, 32.6, 33.2, 33.9, 34.4, 34.9, 35.7, 36.4, 36.8, 37.3, 38.1, 38.9, 39.3, 39.8, 40.6, 41.3, 41.9, 42.4, 43.1, 43.8, 44.6, 45.1, 45.5, 46.3, 47.1, 47.9, 48.3, 48.7, 49.5, 50.3, 51.0, 51.7, 52.2, 52.8, 53.5, 54.3, 55.1, 55.5, 55.7, 56.1, 56.9, 57.7, 58.5, 59.1, 59.5, 60.2, 61.0, 61.8, 62.5, 62.9, 63.4, 64.2, 65.0, 65.8, 66.3, 66.8, 67.4, 68.2, 69.0, 69.8, 70.2, 70.7, 71.5, 72.2, 73.0, 73.6, 74.0, 74.7, 75.5, 76.3, 77.0, 77.4, 77.9, 78.7, 79.5, 80.3, 80.8, 81.3, 81.9, 82.7, 83.5, 84.3, 84.7, 85.2, 86.0, 86.7, 87.5, 88.1, 88.5, 89.2, 90.0, 90.8, 91.5, 91.9, 92.4, 93.2, 94.0, 94.8, 95.3, 95.8, 96.4, 97.2, 98.0, 98.8, 99.2, 99.7, 100.5, 101.2, 102.0, 102.6, 103.0, 103.7, 104.5, 105.3, 106.0, 106.8, 107.6, 108.0, 108.5, 109.3, 110.1, 110.9, 111.7, 112.4, 113.2, 114.0, 114.7, 115.2, 115.7, 116.4, 117.2, 118.0, 118.8, 119.5, 120.3, 121.1, 121.8, 122.4, 122.9, 123.6, 124.3, 125.1, 125.9, 126.6, 127.4, 128.2, 128.9, 129.6, 130.1, 130.7, 131.4, 132.2, 133.0, 133.7, 134.5, 135.3, 136.0, 136.8, 137.3, 137.8, 138.5, 139.3, 140.1, 140.8, 141.6, 142.4, 143.1)+cms.vdouble(143.9, 144.4, 144.9, 145.6, 146.4, 147.2, 147.9, 148.4, 0.0, 0.6, 0.7, 0.8, 1.0, 1.1, 1.2, 1.4, 1.5, 1.7, 1.8, 2.0, 2.3, 2.5, 2.6, 2.8, 3.1, 3.4, 3.6, 3.9, 4.1, 4.5, 4.9, 5.1, 5.4, 5.8, 6.1, 6.4, 6.8, 7.2, 7.6, 8.0, 8.4, 8.8, 8.9, 9.2, 9.6, 10.0, 10.5, 10.9, 11.2, 11.6, 12.0, 12.4, 12.7, 13.2, 13.6, 14.0, 14.4, 14.7, 15.1, 15.5, 16.0, 16.4, 16.7, 17.1, 17.5, 17.9, 18.4, 18.9, 19.4, 19.9, 20.3, 21.0, 21.5, 21.9, 22.5, 22.9, 23.5, 24.0, 24.4, 25.0, 25.5, 25.9, 26.6, 27.0, 27.5, 28.3, 28.8, 29.2, 29.9, 30.5, 31.0, 31.5, 32.2, 32.7, 33.2, 33.9, 34.5, 35.0, 35.4, 36.2, 36.9, 37.3, 37.8, 38.5, 39.2, 39.8, 40.3, 40.9, 41.6, 42.3, 42.8, 43.2, 43.9, 44.7, 45.4, 45.8, 46.2, 47.0, 47.8, 48.4, 49.1, 49.5, 50.1, 50.8, 51.5, 52.3, 52.7, 52.8, 53.3, 54.0, 54.8, 55.5, 56.1, 56.5, 57.1, 57.9, 58.6, 59.3, 59.7, 60.2, 61.0, 61.7, 62.4, 63.0, 63.4, 64.0, 64.8, 65.5, 66.2, 66.6, 67.1, 67.8, 68.5, 69.3, 69.8, 70.3, 70.9, 71.6, 72.4, 73.1, 73.5, 74.0, 74.7, 75.4, 76.2, 76.7, 77.1, 77.8, 78.5, 79.3, 80.0, 80.4, 80.9, 81.6, 82.3, 83.1, 83.6, 84.0, 84.6, 85.4, 86.2, 86.8, 87.3, 87.7, 88.5, 89.2, 89.9, 90.5, 90.9, 91.5, 92.3, 93.0, 93.7, 94.1, 94.6, 95.4, 96.1, 96.8, 97.4, 97.8, 98.4, 99.2, 99.9, 100.6, 101.4, 102.1, 102.5, 103.0, 103.8, 104.5, 105.2, 106.0, 106.7, 107.4, 108.2, 108.9, 109.3, 109.8, 110.5, 111.2, 112.0, 112.7, 113.4, 114.2, 114.9, 115.6, 116.2, 116.6, 117.3, 117.9, 118.7, 119.5, 120.1, 120.9, 121.7, 122.3, 123.0, 123.4, 124.0, 124.7, 125.4, 126.2, 126.9, 127.6, 128.4, 129.1, 129.8, 130.3, 130.7, 131.4, 132.2, 132.9, 133.6, 134.4, 135.1)+cms.vdouble(135.8, 136.6, 137.1, 137.5, 138.2, 138.9, 139.7, 140.4, 140.8, 0.0, 0.5, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.4, 1.6, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9, 3.2, 3.4, 3.6, 3.9, 4.3, 4.6, 4.8, 5.1, 5.5, 5.7, 6.0, 6.4, 6.8, 7.2, 7.5, 7.9, 8.3, 8.5, 8.7, 9.1, 9.4, 9.9, 10.3, 10.6, 11.0, 11.3, 11.7, 12.0, 12.5, 12.9, 13.2, 13.6, 13.9, 14.3, 14.6, 15.1, 15.5, 15.8, 16.2, 16.5, 16.9, 17.4, 17.8, 18.3, 18.8, 19.2, 19.8, 20.3, 20.7, 21.3, 21.6, 22.2, 22.7, 23.1, 23.7, 24.1, 24.5, 25.2, 25.5, 26.0, 26.7, 27.2, 27.6, 28.2, 28.8, 29.3, 29.8, 30.4, 30.9, 31.3, 32.0, 32.6, 33.0, 33.5, 34.2, 34.8, 35.2, 35.7, 36.4, 37.1, 37.6, 38.0, 38.6, 39.3, 40.0, 40.4, 40.8, 41.5, 42.2, 42.9, 43.3, 43.7, 44.4, 45.1, 45.8, 46.3, 46.8, 47.3, 48.0, 48.7, 49.4, 49.8, 49.9, 50.3, 51.0, 51.7, 52.5, 53.0, 53.4, 54.0, 54.7, 55.4, 56.0, 56.4, 56.9, 57.6, 58.2, 59.0, 59.5, 59.9, 60.5, 61.2, 61.9, 62.5, 62.9, 63.4, 64.1, 64.7, 65.5, 66.0, 66.4, 67.0, 67.7, 68.4, 69.0, 69.4, 69.9, 70.6, 71.2, 72.0, 72.5, 72.9, 73.5, 74.2, 74.9, 75.5, 75.9, 76.4, 77.1, 77.7, 78.5, 79.0, 79.4, 80.0, 80.7, 81.4, 82.0, 82.4, 82.9, 83.6, 84.2, 85.0, 85.5, 85.9, 86.5, 87.2, 87.9, 88.5, 88.9, 89.4, 90.1, 90.7, 91.5, 92.0, 92.4, 93.0, 93.7, 94.4, 95.0, 95.8, 96.5, 96.9, 97.3, 98.0, 98.7, 99.4, 100.1, 100.8, 101.5, 102.2, 102.8, 103.3, 103.7, 104.4, 105.0, 105.8, 106.5, 107.1, 107.8, 108.6, 109.2, 109.7, 110.2, 110.8, 111.4, 112.1, 112.8, 113.5, 114.2, 114.9, 115.6, 116.2, 116.6, 117.1, 117.8, 118.5, 119.2, 119.9, 120.6, 121.3, 121.9, 122.6, 123.1, 123.5, 124.2, 124.9, 125.6, 126.2, 127.0)+cms.vdouble(127.7, 128.3, 129.0, 129.5, 129.9, 130.5, 131.2, 132.0, 132.6, 133.0, 0.0, 0.5, 0.6, 0.7, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.3, 2.5, 2.8, 3.0, 3.2, 3.4, 3.7, 4.0, 4.3, 4.5, 4.8, 5.1, 5.4, 5.7, 6.1, 6.4, 6.8, 7.1, 7.5, 7.8, 8.0, 8.2, 8.6, 8.9, 9.3, 9.7, 10.0, 10.3, 10.6, 11.0, 11.3, 11.7, 12.1, 12.4, 12.8, 13.1, 13.5, 13.8, 14.2, 14.6, 14.9, 15.2, 15.5, 15.9, 16.3, 16.8, 17.2, 17.7, 18.0, 18.7, 19.1, 19.4, 20.0, 20.4, 20.9, 21.3, 21.7, 22.3, 22.6, 23.1, 23.7, 24.0, 24.5, 25.1, 25.6, 25.9, 26.5, 27.1, 27.5, 28.0, 28.6, 29.0, 29.5, 30.1, 30.7, 31.1, 31.5, 32.2, 32.8, 33.1, 33.6, 34.2, 34.9, 35.3, 35.8, 36.3, 36.9, 37.6, 38.0, 38.4, 39.0, 39.7, 40.4, 40.7, 41.1, 41.8, 42.4, 43.1, 43.6, 44.0, 44.5, 45.1, 45.8, 46.5, 46.8, 47.0, 47.3, 48.0, 48.7, 49.4, 49.8, 50.2, 50.8, 51.4, 52.1, 52.7, 53.1, 53.5, 54.2, 54.8, 55.5, 56.0, 56.3, 56.9, 57.5, 58.2, 58.8, 59.2, 59.6, 60.3, 60.9, 61.6, 62.1, 62.4, 63.0, 63.7, 64.3, 64.9, 65.3, 65.7, 66.4, 67.0, 67.7, 68.2, 68.6, 69.1, 69.8, 70.5, 71.1, 71.4, 71.9, 72.5, 73.1, 73.8, 74.3, 74.7, 75.2, 75.9, 76.6, 77.2, 77.5, 78.0, 78.6, 79.3, 79.9, 80.4, 80.8, 81.3, 82.0, 82.7, 83.3, 83.7, 84.1, 84.8, 85.4, 86.0, 86.5, 86.9, 87.5, 88.1, 88.8, 89.4, 90.1, 90.8, 91.1, 91.6, 92.2, 92.8, 93.5, 94.2, 94.8, 95.5, 96.1, 96.8, 97.2, 97.6, 98.2, 98.8, 99.5, 100.2, 100.8, 101.5, 102.1, 102.7, 103.2, 103.7, 104.2, 104.8, 105.5, 106.2, 106.8, 107.5, 108.1, 108.7, 109.3, 109.7, 110.2, 110.8, 111.5, 112.2, 112.8, 113.4, 114.1, 114.7, 115.3, 115.8, 116.2, 116.8, 117.5, 118.2, 118.8)+cms.vdouble(119.4, 120.1, 120.7, 121.4, 121.8, 122.2, 122.8, 123.5, 124.2, 124.8, 125.1, 0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.3, 1.4, 1.5, 1.7, 1.9, 2.1, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.8, 4.1, 4.2, 4.5, 4.8, 5.0, 5.3, 5.7, 6.0, 6.4, 6.7, 7.0, 7.3, 7.5, 7.7, 8.0, 8.3, 8.7, 9.1, 9.3, 9.7, 10.0, 10.3, 10.6, 11.0, 11.4, 11.6, 12.0, 12.3, 12.6, 12.9, 13.3, 13.6, 13.9, 14.3, 14.6, 14.9, 15.3, 15.7, 16.2, 16.6, 16.9, 17.5, 17.9, 18.2, 18.7, 19.1, 19.5, 20.0, 20.4, 20.9, 21.2, 21.6, 22.2, 22.5, 22.9, 23.6, 24.0, 24.3, 24.9, 25.4, 25.8, 26.3, 26.8, 27.2, 27.6, 28.2, 28.8, 29.1, 29.5, 30.2, 30.7, 31.1, 31.5, 32.1, 32.7, 33.1, 33.5, 34.1, 34.6, 35.3, 35.7, 36.0, 36.6, 37.2, 37.8, 38.2, 38.5, 39.2, 39.8, 40.4, 40.9, 41.3, 41.7, 42.3, 42.9, 43.6, 43.9, 44.0, 44.4, 45.0, 45.6, 46.3, 46.7, 47.1, 47.6, 48.2, 48.8, 49.4, 49.8, 50.2, 50.8, 51.4, 52.0, 52.5, 52.8, 53.3, 53.9, 54.6, 55.2, 55.5, 55.9, 56.5, 57.1, 57.7, 58.2, 58.5, 59.1, 59.7, 60.3, 60.9, 61.2, 61.6, 62.3, 62.8, 63.5, 63.9, 64.3, 64.8, 65.4, 66.0, 66.6, 67.0, 67.4, 68.0, 68.6, 69.2, 69.7, 70.0, 70.5, 71.1, 71.8, 72.4, 72.7, 73.1, 73.7, 74.3, 74.9, 75.4, 75.7, 76.3, 76.9, 77.5, 78.1, 78.4, 78.8, 79.5, 80.0, 80.7, 81.1, 81.5, 82.0, 82.6, 83.2, 83.8, 84.4, 85.1, 85.4, 85.8, 86.5, 87.0, 87.7, 88.3, 88.9, 89.5, 90.1, 90.7, 91.1, 91.5, 92.1, 92.6, 93.3, 93.9, 94.5, 95.1, 95.7, 96.3, 96.8, 97.2, 97.7, 98.3, 98.9, 99.5, 100.1, 100.7, 101.4, 101.9, 102.5, 102.9, 103.3, 103.9, 104.5, 105.1, 105.7, 106.3, 107.0, 107.6, 108.1, 108.5, 108.9, 109.5, 110.1, 110.8)+cms.vdouble(111.3, 112.0, 112.6, 113.2, 113.8, 114.2, 114.5, 115.1, 115.8, 116.4, 117.0, 117.3, 0.0, 0.4, 0.5, 0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.6, 1.8, 1.9, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5, 4.7, 5.0, 5.3, 5.6, 5.9, 6.2, 6.5, 6.9, 7.0, 7.2, 7.5, 7.8, 8.1, 8.5, 8.7, 9.1, 9.3, 9.6, 9.9, 10.3, 10.6, 10.9, 11.2, 11.5, 11.8, 12.1, 12.4, 12.8, 13.0, 13.3, 13.6, 13.9, 14.3, 14.7, 15.1, 15.5, 15.8, 16.3, 16.7, 17.0, 17.5, 17.8, 18.3, 18.7, 19.0, 19.5, 19.8, 20.2, 20.7, 21.1, 21.4, 22.0, 22.4, 22.7, 23.3, 23.7, 24.1, 24.5, 25.1, 25.4, 25.8, 26.4, 26.9, 27.2, 27.6, 28.2, 28.7, 29.0, 29.4, 30.0, 30.5, 31.0, 31.3, 31.8, 32.4, 32.9, 33.3, 33.6, 34.2, 34.8, 35.4, 35.7, 36.0, 36.6, 37.2, 37.7, 38.2, 38.6, 39.0, 39.5, 40.1, 40.7, 41.0, 41.1, 41.5, 42.1, 42.6, 43.2, 43.7, 44.0, 44.5, 45.1, 45.6, 46.2, 46.5, 46.9, 47.5, 48.0, 48.6, 49.0, 49.3, 49.8, 50.4, 51.0, 51.5, 51.9, 52.2, 52.8, 53.4, 53.9, 54.4, 54.7, 55.2, 55.8, 56.4, 56.9, 57.2, 57.6, 58.2, 58.7, 59.3, 59.7, 60.1, 60.5, 61.1, 61.7, 62.3, 62.6, 62.9, 63.5, 64.1, 64.7, 65.1, 65.4, 65.9, 66.5, 67.1, 67.6, 67.9, 68.3, 68.9, 69.4, 70.0, 70.4, 70.8, 71.3, 71.8, 72.4, 73.0, 73.3, 73.7, 74.3, 74.8, 75.4, 75.8, 76.1, 76.6, 77.2, 77.8, 78.3, 78.9, 79.5, 79.8, 80.2, 80.8, 81.3, 81.9, 82.5, 83.0, 83.6, 84.2, 84.8, 85.1, 85.5, 86.0, 86.6, 87.2, 87.8, 88.3, 88.9, 89.5, 90.0, 90.4, 90.8, 91.3, 91.8, 92.4, 93.0, 93.5, 94.1, 94.7, 95.3, 95.7, 96.1, 96.5, 97.1, 97.7, 98.3, 98.8, 99.4, 100.0, 100.5, 101.0, 101.4, 101.8, 102.3, 102.9)+cms.vdouble(103.5, 104.0, 104.6, 105.2, 105.8, 106.3, 106.7, 107.0, 107.6, 108.2, 108.8, 109.3, 109.6, 0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.6, 1.8, 1.9, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.3, 3.5, 3.7, 3.9, 4.2, 4.4, 4.6, 4.9, 5.2, 5.5, 5.8, 6.1, 6.4, 6.5, 6.7, 7.0, 7.2, 7.6, 7.9, 8.1, 8.4, 8.7, 9.0, 9.2, 9.6, 9.9, 10.1, 10.4, 10.7, 11.0, 11.2, 11.6, 11.9, 12.1, 12.4, 12.7, 13.0, 13.3, 13.7, 14.1, 14.4, 14.7, 15.2, 15.6, 15.9, 16.3, 16.6, 17.0, 17.4, 17.7, 18.2, 18.5, 18.8, 19.3, 19.6, 20.0, 20.5, 20.9, 21.2, 21.7, 22.1, 22.5, 22.9, 23.4, 23.7, 24.1, 24.6, 25.1, 25.4, 25.7, 26.3, 26.8, 27.1, 27.4, 28.0, 28.5, 28.9, 29.2, 29.7, 30.2, 30.7, 31.1, 31.4, 31.9, 32.4, 32.9, 33.2, 33.5, 34.1, 34.6, 35.1, 35.6, 35.9, 36.3, 36.8, 37.4, 37.9, 38.2, 38.3, 38.6, 39.2, 39.7, 40.3, 40.7, 41.0, 41.4, 42.0, 42.5, 43.0, 43.3, 43.7, 44.2, 44.7, 45.3, 45.7, 46.0, 46.4, 47.0, 47.5, 48.0, 48.3, 48.7, 49.2, 49.7, 50.3, 50.7, 51.0, 51.4, 52.0, 52.5, 53.0, 53.3, 53.7, 54.2, 54.7, 55.3, 55.7, 56.0, 56.4, 57.0, 57.5, 58.0, 58.3, 58.7, 59.2, 59.7, 60.3, 60.7, 61.0, 61.4, 62.0, 62.5, 63.0, 63.3, 63.7, 64.2, 64.7, 65.2, 65.6, 65.9, 66.4, 66.9, 67.5, 68.0, 68.3, 68.6, 69.2, 69.7, 70.2, 70.6, 70.9, 71.4, 71.9, 72.5, 73.0, 73.5, 74.1, 74.4, 74.7, 75.3, 75.8, 76.3, 76.9, 77.4, 77.9, 78.5, 79.0, 79.3, 79.7, 80.2, 80.7, 81.2, 81.8, 82.3, 82.8, 83.4, 83.9, 84.3, 84.6, 85.1, 85.6, 86.1, 86.7, 87.2, 87.7, 88.3, 88.8, 89.2, 89.6, 90.0, 90.5, 91.0, 91.6, 92.1, 92.6, 93.2, 93.7, 94.2, 94.5, 94.9, 95.4)+cms.vdouble(95.9, 96.5, 96.9, 97.5, 98.0, 98.5, 99.1, 99.4, 99.7, 100.2, 100.8, 101.3, 101.8, 102.1, 0.0, 0.4, 0.5, 0.6, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.7, 1.8, 1.9, 2.1, 2.3, 2.5, 2.6, 2.8, 3.1, 3.3, 3.4, 3.6, 3.9, 4.1, 4.3, 4.6, 4.8, 5.2, 5.4, 5.7, 5.9, 6.0, 6.2, 6.5, 6.7, 7.1, 7.3, 7.6, 7.8, 8.1, 8.4, 8.6, 8.9, 9.2, 9.4, 9.7, 9.9, 10.2, 10.4, 10.8, 11.0, 11.3, 11.6, 11.8, 12.1, 12.4, 12.7, 13.1, 13.4, 13.7, 14.2, 14.5, 14.8, 15.2, 15.5, 15.8, 16.2, 16.5, 16.9, 17.2, 17.5, 18.0, 18.2, 18.6, 19.1, 19.4, 19.7, 20.1, 20.6, 20.9, 21.3, 21.7, 22.0, 22.4, 22.8, 23.3, 23.6, 23.9, 24.4, 24.9, 25.2, 25.5, 26.0, 26.5, 26.8, 27.1, 27.6, 28.0, 28.5, 28.9, 29.1, 29.6, 30.1, 30.6, 30.9, 31.2, 31.7, 32.2, 32.7, 33.1, 33.4, 33.8, 34.2, 34.8, 35.3, 35.5, 35.6, 35.9, 36.4, 36.9, 37.5, 37.8, 38.1, 38.5, 39.0, 39.5, 40.0, 40.3, 40.6, 41.1, 41.6, 42.1, 42.5, 42.7, 43.2, 43.7, 44.2, 44.6, 44.9, 45.2, 45.8, 46.2, 46.7, 47.1, 47.4, 47.8, 48.3, 48.8, 49.3, 49.6, 49.9, 50.4, 50.9, 51.4, 51.7, 52.0, 52.4, 53.0, 53.5, 53.9, 54.2, 54.5, 55.0, 55.5, 56.0, 56.4, 56.7, 57.1, 57.6, 58.1, 58.6, 58.8, 59.2, 59.7, 60.1, 60.7, 61.0, 61.3, 61.7, 62.2, 62.7, 63.2, 63.5, 63.8, 64.3, 64.8, 65.3, 65.7, 65.9, 66.4, 66.9, 67.4, 67.8, 68.4, 68.9, 69.1, 69.5, 70.0, 70.4, 71.0, 71.5, 71.9, 72.4, 73.0, 73.4, 73.7, 74.1, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.3, 78.7, 79.1, 79.5, 80.1, 80.6, 81.0, 81.5, 82.1, 82.5, 82.9, 83.3, 83.6, 84.1, 84.6, 85.1, 85.6, 86.1, 86.6, 87.1, 87.5, 87.9, 88.2)+cms.vdouble(88.6, 89.2, 89.7, 90.1, 90.6, 91.1, 91.6, 92.1, 92.4, 92.7, 93.2, 93.7, 94.2, 94.7, 95.0, 0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.9, 1.0, 1.1, 1.2, 1.4, 1.5, 1.6, 1.8, 1.9, 2.1, 2.3, 2.4, 2.6, 2.8, 3.1, 3.2, 3.4, 3.6, 3.8, 4.0, 4.3, 4.5, 4.8, 5.0, 5.3, 5.5, 5.6, 5.8, 6.0, 6.2, 6.5, 6.8, 7.0, 7.3, 7.5, 7.7, 8.0, 8.3, 8.5, 8.7, 9.0, 9.2, 9.5, 9.7, 10.0, 10.2, 10.5, 10.7, 10.9, 11.2, 11.5, 11.8, 12.1, 12.4, 12.7, 13.1, 13.4, 13.7, 14.1, 14.3, 14.7, 15.0, 15.3, 15.7, 15.9, 16.2, 16.7, 16.9, 17.2, 17.7, 18.0, 18.3, 18.7, 19.1, 19.4, 19.7, 20.1, 20.4, 20.8, 21.2, 21.6, 21.9, 22.2, 22.6, 23.1, 23.3, 23.6, 24.1, 24.5, 24.9, 25.2, 25.6, 26.0, 26.5, 26.8, 27.0, 27.5, 27.9, 28.4, 28.7, 28.9, 29.4, 29.9, 30.3, 30.7, 31.0, 31.3, 31.8, 32.2, 32.7, 33.0, 33.1, 33.3, 33.8, 34.3, 34.7, 35.1, 35.3, 35.7, 36.2, 36.7, 37.1, 37.4, 37.7, 38.1, 38.6, 39.0, 39.4, 39.7, 40.0, 40.5, 41.0, 41.4, 41.7, 42.0, 42.4, 42.9, 43.4, 43.7, 44.0, 44.3, 44.8, 45.3, 45.7, 46.0, 46.3, 46.8, 47.2, 47.7, 48.0, 48.3, 48.6, 49.1, 49.6, 50.0, 50.3, 50.6, 51.1, 51.5, 52.0, 52.3, 52.6, 53.0, 53.4, 53.9, 54.3, 54.6, 54.9, 55.4, 55.8, 56.3, 56.6, 56.9, 57.3, 57.7, 58.2, 58.6, 58.9, 59.2, 59.7, 60.1, 60.6, 60.9, 61.2, 61.6, 62.0, 62.5, 62.9, 63.4, 63.9, 64.1, 64.4, 64.9, 65.4, 65.8, 66.3, 66.7, 67.2, 67.7, 68.1, 68.4, 68.7, 69.1, 69.6, 70.0, 70.5, 71.0, 71.4, 71.9, 72.3, 72.7, 73.0, 73.4, 73.8, 74.3, 74.7, 75.2, 75.6, 76.1, 76.5, 76.9, 77.2, 77.6, 78.0, 78.5, 79.0, 79.4, 79.9, 80.3, 80.8, 81.2, 81.5)+cms.vdouble(81.8, 82.2, 82.7, 83.2, 83.6, 84.1, 84.6, 85.0, 85.5, 85.8, 86.0, 86.4, 86.9, 87.4, 87.8, 88.1, 0.0, 0.3, 0.4, 0.5, 0.6, 0.6, 0.7, 0.8, 0.9, 1.0, 1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.4, 2.6, 2.8, 3.0, 3.1, 3.3, 3.5, 3.7, 3.9, 4.1, 4.4, 4.6, 4.9, 5.1, 5.2, 5.3, 5.6, 5.8, 6.1, 6.3, 6.5, 6.7, 6.9, 7.2, 7.4, 7.7, 7.9, 8.1, 8.3, 8.5, 8.8, 9.0, 9.2, 9.5, 9.7, 9.9, 10.1, 10.4, 10.6, 10.9, 11.2, 11.5, 11.8, 12.2, 12.4, 12.7, 13.0, 13.3, 13.6, 13.9, 14.2, 14.5, 14.8, 15.0, 15.4, 15.7, 15.9, 16.4, 16.7, 16.9, 17.3, 17.7, 17.9, 18.3, 18.7, 18.9, 19.2, 19.6, 20.0, 20.3, 20.5, 21.0, 21.4, 21.6, 21.9, 22.3, 22.7, 23.0, 23.3, 23.7, 24.1, 24.5, 24.8, 25.0, 25.4, 25.9, 26.3, 26.6, 26.8, 27.2, 27.7, 28.1, 28.4, 28.7, 29.0, 29.4, 29.9, 30.3, 30.5, 30.6, 30.9, 31.3, 31.7, 32.2, 32.5, 32.7, 33.1, 33.5, 34.0, 34.4, 34.6, 34.9, 35.3, 35.7, 36.2, 36.5, 36.7, 37.1, 37.5, 38.0, 38.4, 38.6, 38.9, 39.3, 39.7, 40.1, 40.5, 40.7, 41.1, 41.5, 41.9, 42.3, 42.6, 42.9, 43.3, 43.7, 44.1, 44.5, 44.7, 45.0, 45.5, 45.9, 46.3, 46.6, 46.8, 47.3, 47.7, 48.1, 48.4, 48.7, 49.0, 49.5, 49.9, 50.3, 50.6, 50.8, 51.3, 51.7, 52.1, 52.4, 52.7, 53.0, 53.5, 53.9, 54.3, 54.5, 54.8, 55.3, 55.7, 56.1, 56.4, 56.7, 57.0, 57.4, 57.9, 58.3, 58.7, 59.2, 59.4, 59.7, 60.1, 60.5, 61.0, 61.4, 61.8, 62.2, 62.7, 63.1, 63.3, 63.6, 64.0, 64.4, 64.9, 65.3, 65.7, 66.1, 66.6, 67.0, 67.3, 67.6, 67.9, 68.3, 68.8, 69.2, 69.6, 70.0, 70.5, 70.9, 71.2, 71.5, 71.8, 72.2, 72.7, 73.1, 73.5, 74.0, 74.4, 74.8, 75.2)+cms.vdouble(75.5, 75.7, 76.1, 76.6, 77.0, 77.4, 77.9, 78.3, 78.7, 79.1, 79.4, 79.7, 80.1, 80.5, 80.9, 81.3, 81.6, 0.0, 0.3, 0.4, 0.4, 0.5, 0.6, 0.7, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 1.8, 2.0, 2.1, 2.2, 2.4, 2.6, 2.7, 2.9, 3.1, 3.2, 3.4, 3.6, 3.8, 4.1, 4.3, 4.5, 4.7, 4.8, 4.9, 5.2, 5.3, 5.6, 5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.6, 8.8, 9.0, 9.2, 9.4, 9.6, 9.8, 10.1, 10.4, 10.7, 10.9, 11.2, 11.5, 11.7, 12.1, 12.3, 12.6, 12.9, 13.1, 13.4, 13.6, 13.9, 14.3, 14.5, 14.7, 15.1, 15.4, 15.6, 16.0, 16.3, 16.6, 16.9, 17.3, 17.5, 17.8, 18.1, 18.5, 18.7, 19.0, 19.4, 19.8, 20.0, 20.2, 20.6, 21.0, 21.3, 21.6, 21.9, 22.3, 22.7, 22.9, 23.1, 23.5, 23.9, 24.3, 24.5, 24.8, 25.2, 25.6, 26.0, 26.3, 26.5, 26.8, 27.2, 27.6, 28.0, 28.2, 28.3, 28.5, 28.9, 29.3, 29.7, 30.0, 30.3, 30.6, 31.0, 31.4, 31.8, 32.0, 32.3, 32.7, 33.0, 33.4, 33.7, 33.9, 34.3, 34.7, 35.1, 35.5, 35.7, 35.9, 36.3, 36.7, 37.1, 37.4, 37.6, 38.0, 38.4, 38.8, 39.1, 39.4, 39.6, 40.0, 40.4, 40.8, 41.1, 41.3, 41.7, 42.1, 42.5, 42.8, 43.1, 43.3, 43.7, 44.1, 44.5, 44.8, 45.0, 45.3, 45.7, 46.1, 46.5, 46.7, 47.0, 47.4, 47.8, 48.2, 48.5, 48.7, 49.0, 49.4, 49.8, 50.2, 50.4, 50.7, 51.1, 51.5, 51.9, 52.2, 52.4, 52.7, 53.1, 53.5, 53.9, 54.3, 54.7, 54.9, 55.2, 55.6, 56.0, 56.4, 56.8, 57.1, 57.5, 57.9, 58.3, 58.6, 58.8, 59.2, 59.6, 60.0, 60.4, 60.7, 61.2, 61.6, 61.9, 62.2, 62.5, 62.8, 63.2, 63.6, 64.0, 64.4, 64.8, 65.2, 65.5, 65.9, 66.1, 66.4, 66.8, 67.2, 67.6, 68.0, 68.4, 68.8, 69.2)+cms.vdouble(69.5, 69.8, 70.0, 70.4, 70.8, 71.2, 71.6, 72.0, 72.4, 72.8, 73.2, 73.4, 73.6, 74.0, 74.4, 74.8, 75.2, 75.4, 0.0, 0.3, 0.3, 0.4, 0.5, 0.5, 0.6, 0.7, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 1.8, 1.9, 2.0, 2.2, 2.4, 2.5, 2.7, 2.9, 3.0, 3.2, 3.4, 3.5, 3.8, 3.9, 4.2, 4.4, 4.4, 4.6, 4.8, 4.9, 5.2, 5.4, 5.5, 5.8, 5.9, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.5, 8.6, 8.8, 9.1, 9.3, 9.6, 9.8, 10.0, 10.4, 10.6, 10.8, 11.1, 11.3, 11.6, 11.9, 12.1, 12.4, 12.6, 12.8, 13.2, 13.4, 13.6, 14.0, 14.2, 14.4, 14.8, 15.1, 15.3, 15.6, 15.9, 16.2, 16.4, 16.7, 17.1, 17.3, 17.5, 17.9, 18.2, 18.4, 18.7, 19.1, 19.4, 19.7, 19.9, 20.2, 20.6, 20.9, 21.2, 21.4, 21.7, 22.1, 22.5, 22.7, 22.9, 23.2, 23.6, 24.0, 24.3, 24.5, 24.8, 25.1, 25.5, 25.9, 26.1, 26.1, 26.3, 26.7, 27.1, 27.5, 27.7, 27.9, 28.3, 28.6, 29.0, 29.3, 29.5, 29.8, 30.2, 30.5, 30.9, 31.1, 31.3, 31.7, 32.0, 32.4, 32.7, 32.9, 33.2, 33.6, 33.9, 34.3, 34.5, 34.8, 35.1, 35.4, 35.8, 36.1, 36.4, 36.6, 37.0, 37.3, 37.7, 38.0, 38.2, 38.5, 38.8, 39.2, 39.6, 39.8, 40.0, 40.4, 40.7, 41.1, 41.4, 41.6, 41.9, 42.2, 42.6, 43.0, 43.2, 43.4, 43.8, 44.1, 44.5, 44.8, 45.0, 45.3, 45.6, 46.0, 46.4, 46.6, 46.8, 47.2, 47.5, 47.9, 48.2, 48.4, 48.7, 49.0, 49.4, 49.8, 50.1, 50.5, 50.7, 51.0, 51.3, 51.7, 52.0, 52.4, 52.8, 53.1, 53.5, 53.8, 54.1, 54.3, 54.7, 55.0, 55.4, 55.8, 56.1, 56.5, 56.8, 57.2, 57.5, 57.7, 58.0, 58.3, 58.7, 59.1, 59.4, 59.8, 60.2, 60.5, 60.8, 61.1, 61.3, 61.7, 62.0, 62.4, 62.8, 63.1, 63.5)+cms.vdouble(63.9, 64.2, 64.4, 64.7, 65.0, 65.4, 65.8, 66.1, 66.5, 66.8, 67.2, 67.6, 67.8, 68.0, 68.3, 68.7, 69.1, 69.4, 69.6, 0.0, 0.3, 0.3, 0.4, 0.4, 0.5, 0.6, 0.6, 0.7, 0.8, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 1.8, 1.9, 2.1, 2.2, 2.3, 2.4, 2.6, 2.8, 2.9, 3.1, 3.3, 3.5, 3.6, 3.8, 4.0, 4.1, 4.2, 4.4, 4.6, 4.8, 5.0, 5.1, 5.3, 5.5, 5.7, 5.8, 6.0, 6.2, 6.4, 6.6, 6.7, 6.9, 7.1, 7.3, 7.5, 7.6, 7.8, 8.0, 8.2, 8.4, 8.6, 8.9, 9.1, 9.3, 9.6, 9.8, 10.0, 10.3, 10.5, 10.7, 11.0, 11.1, 11.4, 11.6, 11.8, 12.1, 12.3, 12.6, 12.9, 13.1, 13.3, 13.6, 13.9, 14.1, 14.4, 14.7, 14.9, 15.1, 15.4, 15.8, 15.9, 16.2, 16.5, 16.8, 17.0, 17.2, 17.6, 17.9, 18.1, 18.4, 18.6, 19.0, 19.3, 19.5, 19.7, 20.0, 20.4, 20.7, 20.9, 21.1, 21.4, 21.8, 22.1, 22.4, 22.6, 22.9, 23.2, 23.5, 23.9, 24.0, 24.1, 24.3, 24.6, 25.0, 25.3, 25.6, 25.8, 26.1, 26.4, 26.7, 27.1, 27.2, 27.5, 27.8, 28.1, 28.5, 28.7, 28.9, 29.2, 29.5, 29.9, 30.2, 30.4, 30.6, 31.0, 31.3, 31.6, 31.9, 32.1, 32.3, 32.7, 33.0, 33.3, 33.5, 33.7, 34.1, 34.4, 34.8, 35.0, 35.2, 35.5, 35.8, 36.2, 36.5, 36.7, 36.9, 37.2, 37.5, 37.9, 38.1, 38.3, 38.6, 39.0, 39.3, 39.6, 39.8, 40.0, 40.4, 40.7, 41.0, 41.3, 41.5, 41.8, 42.1, 42.4, 42.8, 42.9, 43.2, 43.5, 43.8, 44.2, 44.4, 44.6, 44.9, 45.2, 45.6, 45.9, 46.2, 46.6, 46.8, 47.0, 47.3, 47.7, 48.0, 48.3, 48.7, 49.0, 49.4, 49.7, 49.9, 50.1, 50.4, 50.7, 51.1, 51.4, 51.7, 52.1, 52.4, 52.7, 53.0, 53.2, 53.5, 53.8, 54.2, 54.5, 54.8, 55.2, 55.5, 55.8, 56.1, 56.3, 56.6, 56.9, 57.2, 57.6, 57.9, 58.2)+cms.vdouble(58.6, 58.9, 59.2, 59.4, 59.6, 60.0, 60.3, 60.7, 61.0, 61.3, 61.7, 62.0, 62.3, 62.5, 62.7, 63.0, 63.4, 63.7, 64.0, 64.2, 0.0, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.4, 1.6, 1.8, 2.0, 2.1, 2.4, 2.5, 2.7, 2.8, 3.1, 3.4, 3.6, 3.7, 3.8, 4.0, 4.3, 4.6, 4.8, 5.0, 5.1, 5.4, 5.7, 5.9, 6.1, 6.3, 6.6, 6.9, 7.0, 7.2, 7.5, 7.8, 8.1, 8.5, 8.8, 9.1, 9.5, 9.8, 10.2, 10.5, 10.8, 11.1, 11.5, 11.9, 12.2, 12.7, 13.1, 13.5, 13.9, 14.3, 14.7, 15.1, 15.5, 15.9, 16.5, 16.8, 17.3, 17.7, 18.1, 18.7, 19.1, 19.4, 20.0, 20.5, 20.9, 21.4, 21.9, 22.1, 22.4, 22.9, 23.4, 23.7, 24.3, 24.8, 25.1, 25.7, 26.2, 26.6, 27.1, 27.6, 28.0, 28.5, 29.1, 29.4, 29.9, 30.4, 30.8, 31.3, 31.9, 32.2, 32.6, 33.3, 33.6, 34.0, 34.7, 35.0, 35.4, 36.1, 36.4, 36.8, 37.4, 37.8, 38.2, 38.8, 39.2, 39.6, 40.2, 40.7, 41.1, 41.6, 42.2, 42.7, 43.1, 43.6, 44.2, 44.8, 45.5, 45.9, 46.2, 46.9, 47.5, 48.1, 48.6, 48.9, 49.5, 50.1, 50.8, 51.4, 51.7, 52.2, 52.8, 53.4, 54.1, 54.4, 54.8, 55.5, 56.1, 56.7, 57.2, 57.6, 58.1, 58.8, 59.4, 60.0, 60.4, 60.8, 61.4, 62.0, 62.7, 63.3, 63.8, 64.2, 64.7, 65.3, 66.0, 66.6, 67.2, 67.9, 68.3, 68.6, 69.3, 69.9, 70.5, 71.2, 71.8, 72.4, 72.7, 73.2, 73.8, 74.5, 75.1, 75.7, 76.4, 76.8, 77.2, 77.8, 78.3, 79.0, 79.6, 80.2, 80.9, 81.5, 81.9, 82.3, 82.9, 83.5, 84.2, 84.8, 85.4, 86.1, 86.7, 87.4, 87.7, 88.1, 88.7, 89.4, 90.0, 90.6, 91.3, 91.9, 92.6, 93.2, 93.6, 93.9, 94.6, 95.2, 95.8, 96.5, 97.1, 97.8, 98.4, 99.0, 99.7, 100.1, 100.4, 101.0, 101.7, 102.3, 103.0, 103.6, 104.2, 104.9, 105.5, 106.1, 106.8)+cms.vdouble(107.2, 107.6, 108.2, 108.8, 109.4, 110.1, 110.7, 111.3, 112.0, 112.6, 113.2, 113.8, 114.3, 114.5, 114.8, 115.3, 116.0, 116.6, 117.2, 117.9, 118.2, 0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.3, 2.4, 2.6, 2.9, 3.1, 3.3, 3.4, 3.5, 3.6, 3.9, 4.2, 4.4, 4.5, 4.7, 5.0, 5.2, 5.4, 5.5, 5.8, 6.0, 6.3, 6.4, 6.6, 6.9, 7.1, 7.4, 7.8, 8.0, 8.3, 8.7, 8.9, 9.3, 9.6, 9.9, 10.1, 10.5, 10.9, 11.2, 11.6, 11.9, 12.4, 12.7, 13.0, 13.4, 13.8, 14.1, 14.5, 15.0, 15.4, 15.8, 16.2, 16.5, 17.1, 17.4, 17.7, 18.3, 18.7, 19.1, 19.6, 20.0, 20.2, 20.4, 21.0, 21.4, 21.7, 22.2, 22.6, 23.0, 23.5, 24.0, 24.3, 24.8, 25.2, 25.5, 26.0, 26.6, 26.9, 27.3, 27.8, 28.1, 28.6, 29.1, 29.5, 29.8, 30.4, 30.7, 31.1, 31.7, 32.0, 32.4, 32.9, 33.3, 33.6, 34.2, 34.6, 34.9, 35.5, 35.8, 36.2, 36.7, 37.2, 37.5, 38.0, 38.5, 39.0, 39.4, 39.8, 40.4, 41.0, 41.5, 41.9, 42.2, 42.8, 43.4, 44.0, 44.4, 44.7, 45.2, 45.8, 46.4, 46.9, 47.2, 47.7, 48.2, 48.8, 49.4, 49.7, 50.1, 50.7, 51.3, 51.8, 52.3, 52.6, 53.1, 53.7, 54.3, 54.8, 55.2, 55.5, 56.1, 56.7, 57.3, 57.9, 58.3, 58.6, 59.1, 59.7, 60.3, 60.9, 61.4, 62.0, 62.4, 62.7, 63.3, 63.9, 64.5, 65.0, 65.6, 66.1, 66.5, 66.9, 67.5, 68.0, 68.6, 69.2, 69.8, 70.2, 70.5, 71.1, 71.6, 72.2, 72.7, 73.3, 73.9, 74.5, 74.9, 75.2, 75.8, 76.3, 76.9, 77.5, 78.1, 78.7, 79.2, 79.8, 80.1, 80.5, 81.1, 81.7, 82.2, 82.8, 83.4, 84.0, 84.6, 85.1, 85.5, 85.8, 86.4, 87.0, 87.6, 88.2, 88.7, 89.3, 89.9, 90.5, 91.1, 91.4, 91.7, 92.3, 92.9, 93.5, 94.1, 94.6, 95.2, 95.8, 96.4, 97.0)+cms.vdouble(97.6, 97.9, 98.3, 98.8, 99.4, 100.0, 100.6, 101.1, 101.7, 102.3, 102.9, 103.5, 104.0, 104.4, 104.6, 104.9, 105.4, 105.9, 106.5, 107.1, 107.7, 108.0, 0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.0, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.6, 2.8, 3.0, 3.1, 3.1, 3.3, 3.5, 3.8, 4.0, 4.1, 4.2, 4.5, 4.7, 4.9, 5.0, 5.2, 5.4, 5.7, 5.8, 6.0, 6.2, 6.4, 6.7, 7.0, 7.2, 7.5, 7.8, 8.1, 8.4, 8.6, 8.9, 9.2, 9.5, 9.8, 10.1, 10.4, 10.8, 11.2, 11.4, 11.8, 12.1, 12.5, 12.8, 13.1, 13.6, 13.9, 14.3, 14.6, 14.9, 15.4, 15.7, 16.0, 16.5, 16.9, 17.2, 17.7, 18.1, 18.2, 18.4, 18.9, 19.3, 19.6, 20.1, 20.4, 20.7, 21.2, 21.6, 21.9, 22.4, 22.8, 23.1, 23.5, 24.0, 24.3, 24.6, 25.1, 25.4, 25.8, 26.3, 26.6, 26.9, 27.5, 27.7, 28.1, 28.6, 28.9, 29.2, 29.7, 30.0, 30.4, 30.9, 31.2, 31.6, 32.0, 32.4, 32.7, 33.2, 33.6, 33.9, 34.3, 34.8, 35.2, 35.6, 35.9, 36.5, 37.0, 37.5, 37.8, 38.1, 38.7, 39.2, 39.7, 40.1, 40.4, 40.8, 41.4, 41.9, 42.4, 42.7, 43.0, 43.6, 44.1, 44.6, 44.9, 45.2, 45.8, 46.3, 46.8, 47.2, 47.5, 47.9, 48.5, 49.0, 49.5, 49.8, 50.1, 50.7, 51.2, 51.7, 52.2, 52.6, 53.0, 53.4, 53.9, 54.4, 55.0, 55.5, 56.0, 56.3, 56.6, 57.1, 57.7, 58.2, 58.7, 59.2, 59.7, 60.0, 60.4, 60.9, 61.4, 62.0, 62.5, 63.0, 63.3, 63.7, 64.2, 64.6, 65.2, 65.7, 66.2, 66.7, 67.3, 67.6, 67.9, 68.4, 68.9, 69.4, 70.0, 70.5, 71.0, 71.5, 72.1, 72.4, 72.7, 73.2, 73.7, 74.3, 74.8, 75.3, 75.8, 76.4, 76.9, 77.2, 77.5, 78.0, 78.5, 79.1, 79.6, 80.1, 80.6, 81.2, 81.7, 82.2, 82.6, 82.8, 83.4, 83.9, 84.4, 84.9, 85.5, 86.0, 86.5, 87.0)+cms.vdouble(87.6, 88.1, 88.4, 88.7, 89.2, 89.7, 90.3, 90.8, 91.3, 91.8, 92.4, 92.9, 93.4, 93.9, 94.3, 94.5, 94.7, 95.1, 95.7, 96.2, 96.7, 97.2, 97.5, 0.0, 0.2, 0.3, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.8, 0.9, 1.1, 1.2, 1.3, 1.4, 1.6, 1.7, 1.9, 2.0, 2.1, 2.3, 2.5, 2.6, 2.7, 2.8, 2.9, 3.1, 3.3, 3.5, 3.6, 3.8, 4.0, 4.2, 4.3, 4.5, 4.6, 4.8, 5.0, 5.2, 5.3, 5.5, 5.7, 5.9, 6.2, 6.4, 6.7, 7.0, 7.2, 7.5, 7.7, 7.9, 8.1, 8.4, 8.7, 9.0, 9.3, 9.6, 9.9, 10.2, 10.5, 10.8, 11.1, 11.4, 11.7, 12.1, 12.3, 12.7, 13.0, 13.3, 13.7, 14.0, 14.2, 14.7, 15.1, 15.3, 15.7, 16.1, 16.2, 16.4, 16.8, 17.2, 17.4, 17.9, 18.2, 18.4, 18.9, 19.2, 19.5, 19.9, 20.3, 20.5, 20.9, 21.3, 21.6, 21.9, 22.3, 22.6, 22.9, 23.4, 23.7, 24.0, 24.4, 24.7, 25.0, 25.4, 25.7, 26.0, 26.5, 26.7, 27.0, 27.5, 27.8, 28.1, 28.5, 28.8, 29.1, 29.5, 29.8, 30.1, 30.5, 31.0, 31.3, 31.6, 32.0, 32.4, 32.9, 33.4, 33.7, 33.9, 34.4, 34.9, 35.3, 35.7, 35.9, 36.3, 36.8, 37.3, 37.7, 37.9, 38.3, 38.8, 39.2, 39.7, 39.9, 40.2, 40.7, 41.2, 41.6, 42.0, 42.3, 42.7, 43.1, 43.6, 44.0, 44.3, 44.6, 45.1, 45.5, 46.0, 46.5, 46.8, 47.1, 47.5, 48.0, 48.4, 48.9, 49.4, 49.8, 50.1, 50.4, 50.8, 51.3, 51.8, 52.2, 52.7, 53.1, 53.4, 53.7, 54.2, 54.7, 55.1, 55.6, 56.1, 56.3, 56.6, 57.1, 57.5, 58.0, 58.4, 58.9, 59.4, 59.8, 60.1, 60.4, 60.8, 61.3, 61.8, 62.2, 62.7, 63.2, 63.6, 64.1, 64.4, 64.7, 65.1, 65.6, 66.1, 66.5, 67.0, 67.5, 67.9, 68.4, 68.7, 68.9, 69.4, 69.9, 70.3, 70.8, 71.3, 71.7, 72.2, 72.7, 73.1, 73.4, 73.7, 74.2, 74.6, 75.1, 75.6, 76.0, 76.5, 77.0)+cms.vdouble(77.4, 77.9, 78.4, 78.7, 78.9, 79.4, 79.8, 80.3, 80.8, 81.2, 81.7, 82.2, 82.6, 83.1, 83.5, 83.9, 84.0, 84.2, 84.6, 85.1, 85.6, 86.0, 86.5, 86.7, 0.0, 0.1, 0.2, 0.3, 0.4, 0.4, 0.5, 0.6, 0.7, 0.7, 0.8, 0.9, 1.0, 1.1, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0, 2.2, 2.3, 2.4, 2.4, 2.6, 2.7, 2.9, 3.1, 3.2, 3.3, 3.5, 3.7, 3.8, 3.9, 4.0, 4.2, 4.4, 4.5, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.4, 7.6, 7.8, 8.1, 8.4, 8.7, 8.9, 9.1, 9.4, 9.7, 9.9, 10.2, 10.5, 10.8, 11.1, 11.4, 11.6, 12.0, 12.2, 12.4, 12.8, 13.1, 13.4, 13.7, 14.0, 14.1, 14.3, 14.7, 15.0, 15.2, 15.6, 15.9, 16.1, 16.5, 16.8, 17.0, 17.4, 17.7, 17.9, 18.2, 18.6, 18.8, 19.1, 19.5, 19.7, 20.0, 20.4, 20.7, 20.9, 21.3, 21.5, 21.8, 22.2, 22.4, 22.7, 23.1, 23.3, 23.6, 24.0, 24.2, 24.5, 24.9, 25.1, 25.4, 25.8, 26.1, 26.3, 26.6, 27.0, 27.4, 27.6, 27.9, 28.3, 28.7, 29.1, 29.4, 29.6, 30.0, 30.4, 30.8, 31.1, 31.3, 31.7, 32.1, 32.5, 32.9, 33.1, 33.4, 33.8, 34.2, 34.6, 34.9, 35.1, 35.5, 35.9, 36.3, 36.6, 36.9, 37.2, 37.6, 38.0, 38.4, 38.7, 38.9, 39.3, 39.7, 40.2, 40.6, 40.9, 41.1, 41.5, 41.9, 42.3, 42.7, 43.1, 43.5, 43.7, 44.0, 44.4, 44.8, 45.2, 45.6, 46.0, 46.4, 46.6, 46.9, 47.3, 47.7, 48.1, 48.5, 48.9, 49.2, 49.4, 49.8, 50.2, 50.6, 51.0, 51.4, 51.8, 52.2, 52.5, 52.7, 53.1, 53.5, 53.9, 54.3, 54.7, 55.1, 55.6, 56.0, 56.2, 56.4, 56.8, 57.3, 57.7, 58.1, 58.5, 58.9, 59.3, 59.7, 60.0, 60.2, 60.6, 61.0, 61.4, 61.8, 62.2, 62.6, 63.0, 63.4, 63.8, 64.1, 64.3, 64.7, 65.1, 65.5, 66.0, 66.4, 66.8)+cms.vdouble(67.2, 67.6, 68.0, 68.4, 68.7, 68.9, 69.3, 69.7, 70.1, 70.5, 70.9, 71.3, 71.7, 72.1, 72.5, 72.9, 73.2, 73.4, 73.5, 73.9, 74.3, 74.7, 75.1, 75.5, 75.7, 0.0, 0.1, 0.2, 0.3, 0.3, 0.4, 0.4, 0.5, 0.6, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.4, 1.5, 1.7, 1.9, 2.0, 2.0, 2.1, 2.2, 2.3, 2.5, 2.6, 2.7, 2.8, 3.0, 3.1, 3.2, 3.3, 3.4, 3.6, 3.7, 3.8, 3.9, 4.1, 4.3, 4.4, 4.6, 4.8, 5.0, 5.2, 5.3, 5.5, 5.7, 5.9, 6.0, 6.3, 6.5, 6.7, 6.9, 7.1, 7.4, 7.6, 7.8, 8.0, 8.3, 8.4, 8.7, 9.0, 9.2, 9.4, 9.7, 9.9, 10.2, 10.4, 10.6, 10.9, 11.2, 11.4, 11.7, 11.9, 12.0, 12.2, 12.5, 12.8, 13.0, 13.3, 13.5, 13.7, 14.0, 14.3, 14.5, 14.8, 15.1, 15.3, 15.5, 15.8, 16.0, 16.3, 16.6, 16.8, 17.0, 17.4, 17.6, 17.8, 18.1, 18.3, 18.6, 18.9, 19.1, 19.3, 19.7, 19.9, 20.1, 20.4, 20.6, 20.9, 21.2, 21.4, 21.6, 21.9, 22.2, 22.4, 22.7, 23.0, 23.3, 23.5, 23.8, 24.1, 24.5, 24.8, 25.0, 25.2, 25.6, 25.9, 26.2, 26.5, 26.7, 27.0, 27.3, 27.7, 28.0, 28.2, 28.5, 28.8, 29.1, 29.5, 29.7, 29.9, 30.2, 30.6, 30.9, 31.2, 31.4, 31.7, 32.0, 32.4, 32.7, 32.9, 33.1, 33.5, 33.8, 34.2, 34.5, 34.8, 35.0, 35.3, 35.6, 36.0, 36.3, 36.7, 37.0, 37.2, 37.4, 37.8, 38.1, 38.5, 38.8, 39.2, 39.5, 39.7, 39.9, 40.3, 40.6, 41.0, 41.3, 41.7, 41.9, 42.1, 42.4, 42.7, 43.1, 43.4, 43.8, 44.1, 44.5, 44.7, 44.9, 45.2, 45.6, 45.9, 46.3, 46.6, 46.9, 47.3, 47.6, 47.8, 48.1, 48.4, 48.7, 49.1, 49.4, 49.8, 50.1, 50.5, 50.8, 51.0, 51.2, 51.6, 51.9, 52.3, 52.6, 53.0, 53.3, 53.7, 54.0, 54.4, 54.6, 54.8, 55.1, 55.5, 55.8, 56.1, 56.5)+cms.vdouble(56.8, 57.2, 57.5, 57.9, 58.2, 58.4, 58.7, 59.0, 59.3, 59.7, 60.0, 60.4, 60.7, 61.1, 61.4, 61.8, 62.1, 62.3, 62.5, 62.6, 62.9, 63.2, 63.6, 63.9, 64.3, 64.5, 0.0, 0.1, 0.3, 0.4, 0.5, 0.7, 0.8, 0.9, 1.1, 1.2, 1.3, 1.5, 1.6, 1.7, 1.9, 2.0, 2.1, 2.3, 2.4, 2.5, 2.7, 2.8, 2.9, 3.1, 3.2, 3.4, 3.6, 3.8, 4.1, 4.4, 4.6, 4.8, 5.0, 5.2, 5.6, 6.0, 6.2, 6.4, 6.8, 7.2, 7.4, 7.8, 8.2, 8.5, 9.0, 9.3, 9.8, 10.2, 10.3, 10.6, 11.1, 11.4, 11.8, 12.2, 12.5, 13.0, 13.3, 13.8, 14.2, 14.5, 15.0, 15.3, 15.7, 16.1, 16.5, 17.0, 17.3, 17.8, 18.1, 18.5, 19.0, 19.4, 19.8, 20.3, 20.9, 21.4, 22.0, 22.5, 22.9, 23.5, 24.0, 24.6, 25.1, 25.5, 26.2, 26.6, 27.1, 27.7, 28.1, 28.8, 29.3, 29.8, 30.5, 31.2, 31.7, 32.2, 32.9, 33.4, 33.9, 34.6, 35.3, 35.7, 36.3, 37.1, 37.7, 38.1, 38.7, 39.5, 40.2, 40.7, 41.2, 41.9, 42.7, 43.2, 43.6, 44.4, 45.2, 45.9, 46.4, 46.8, 47.6, 48.4, 49.1, 49.6, 50.1, 50.8, 51.5, 52.3, 52.9, 53.1, 53.5, 54.1, 54.9, 55.7, 56.2, 56.7, 57.4, 58.1, 58.9, 59.5, 60.0, 60.6, 61.3, 62.1, 62.8, 63.3, 63.8, 64.5, 65.3, 66.1, 66.5, 67.0, 67.7, 68.5, 69.4, 69.8, 70.2, 71.0, 71.8, 72.5, 73.0, 73.4, 74.2, 75.0, 75.7, 76.3, 76.7, 77.4, 78.2, 78.9, 79.5, 80.0, 80.6, 81.4, 82.2, 82.8, 83.3, 83.8, 84.6, 85.4, 86.1, 86.6, 87.0, 87.8, 88.6, 89.3, 89.8, 90.3, 91.1, 91.8, 92.5, 93.1, 93.5, 94.2, 94.9, 95.8, 96.4, 96.8, 97.4, 98.2, 99.0, 99.8, 100.5, 101.2, 101.7, 102.2, 103.0, 103.7, 104.5, 105.3, 106.1, 106.8, 107.5, 108.1, 108.6, 109.3, 110.0, 110.8, 111.6, 112.3, 113.0, 113.8, 114.6, 115.1, 115.5, 116.3, 117.1, 117.9, 118.6)+cms.vdouble(119.3, 120.1, 120.9, 121.5, 121.9, 122.6, 123.4, 124.2, 124.9, 125.6, 126.4, 127.2, 128.0, 128.4, 128.9, 129.7, 130.5, 131.2, 131.9, 132.7, 133.5, 134.2, 134.8, 135.3, 136.0, 136.7, 137.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 3.9, 4.1, 4.4, 4.7, 4.8, 5.0, 5.3, 5.6, 5.8, 6.1, 6.4, 6.6, 7.0, 7.3, 7.6, 8.0, 8.1, 8.3, 8.6, 8.9, 9.2, 9.5, 9.8, 10.1, 10.4, 10.8, 11.1, 11.4, 11.7, 12.0, 12.3, 12.6, 12.9, 13.2, 13.5, 13.9, 14.1, 14.4, 14.8, 15.2, 15.5, 15.8, 16.3, 16.7, 17.2, 17.6, 17.9, 18.4, 18.7, 19.2, 19.6, 19.9, 20.5, 20.8, 21.2, 21.6, 22.0, 22.5, 22.9, 23.3, 23.8, 24.4, 24.7, 25.1, 25.7, 26.1, 26.5, 27.0, 27.6, 27.9, 28.3, 28.9, 29.4, 29.8, 30.2, 30.8, 31.4, 31.7, 32.2, 32.7, 33.3, 33.7, 34.1, 34.7, 35.3, 35.8, 36.2, 36.6, 37.2, 37.8, 38.3, 38.7, 39.1, 39.6, 40.2, 40.8, 41.3, 41.4, 41.7, 42.3, 42.8, 43.5, 43.9, 44.2, 44.8, 45.3, 46.0, 46.4, 46.8, 47.3, 47.9, 48.5, 49.0, 49.4, 49.8, 50.4, 51.0, 51.6, 51.9, 52.3, 52.9, 53.5, 54.1, 54.5, 54.8, 55.4, 56.0, 56.6, 57.0, 57.3, 57.9, 58.5, 59.1, 59.5, 59.9, 60.4, 61.0, 61.6, 62.1, 62.5, 62.9, 63.5, 64.1, 64.6, 65.0, 65.4, 66.1, 66.6, 67.2, 67.6, 67.9, 68.6, 69.1, 69.7, 70.1, 70.5, 71.1, 71.7, 72.2, 72.7, 73.0, 73.5, 74.1, 74.7, 75.2, 75.6, 76.1, 76.6, 77.3, 77.9, 78.5, 79.0, 79.3, 79.8, 80.4, 81.0, 81.5, 82.2, 82.8, 83.4, 83.9, 84.4, 84.7, 85.3, 85.9, 86.5, 87.1, 87.7, 88.2, 88.9, 89.4, 89.8, 90.2, 90.7, 91.4, 92.0)+cms.vdouble(92.6, 93.2, 93.8, 94.4, 94.8, 95.1, 95.7, 96.3, 96.9, 97.5, 98.1, 98.7, 99.3, 99.9, 100.2, 100.6, 101.2, 101.8, 102.4, 103.0, 103.6, 104.2, 104.8, 105.2, 105.6, 106.1, 106.7, 107.0, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0, 54.5, 55.0, 55.5, 56.0, 56.5, 57.0, 57.5, 58.0, 58.5, 59.0, 59.5, 60.0, 60.5, 61.0, 61.5, 62.0, 62.5, 63.0, 63.5, 64.0, 64.5, 65.0, 65.5, 66.0, 66.5, 67.0, 67.5, 68.0, 68.5, 69.0, 69.5, 70.0, 70.5, 71.0, 71.5, 72.0, 72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.5, 79.0, 79.5, 80.0, 80.5, 81.0, 81.5, 82.0, 82.5, 83.0, 83.5, 84.0, 84.5, 85.0, 85.5, 86.0, 86.5, 87.0, 87.5, 88.0, 88.5, 89.0, 89.5, 90.0, 90.5, 91.0, 91.5, 92.0, 92.5, 93.0, 93.5, 94.0, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 101.0, 101.5, 102.0, 102.5, 103.0, 103.5, 104.0, 104.5, 105.0, 105.5, 106.0, 106.5, 107.0, 107.5, 108.0, 108.5, 109.0, 109.5, 110.0, 110.5, 111.0, 111.5, 112.0, 112.5, 113.0)+cms.vdouble(113.5, 114.0, 114.5, 115.0, 115.5, 116.0, 116.5, 117.0, 117.5, 118.0, 118.5, 119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0, 125.5, 126.0, 126.5, 127.0, 127.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0, 54.5, 55.0, 55.5, 56.0, 56.5, 57.0, 57.5, 58.0, 58.5, 59.0, 59.5, 60.0, 60.5, 61.0, 61.5, 62.0, 62.5, 63.0, 63.5, 64.0, 64.5, 65.0, 65.5, 66.0, 66.5, 67.0, 67.5, 68.0, 68.5, 69.0, 69.5, 70.0, 70.5, 71.0, 71.5, 72.0, 72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.5, 79.0, 79.5, 80.0, 80.5, 81.0, 81.5, 82.0, 82.5, 83.0, 83.5, 84.0, 84.5, 85.0, 85.5, 86.0, 86.5, 87.0, 87.5, 88.0, 88.5, 89.0, 89.5, 90.0, 90.5, 91.0, 91.5, 92.0, 92.5, 93.0, 93.5, 94.0, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 101.0, 101.5, 102.0, 102.5, 103.0, 103.5, 104.0, 104.5, 105.0, 105.5, 106.0, 106.5, 107.0, 107.5, 108.0, 108.5, 109.0, 109.5, 110.0, 110.5, 111.0, 111.5, 112.0, 112.5)+cms.vdouble(113.0, 113.5, 114.0, 114.5, 115.0, 115.5, 116.0, 116.5, 117.0, 117.5, 118.0, 118.5, 119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0, 125.5, 126.0, 126.5, 127.0, 127.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0, 54.5, 55.0, 55.5, 56.0, 56.5, 57.0, 57.5, 58.0, 58.5, 59.0, 59.5, 60.0, 60.5, 61.0, 61.5, 62.0, 62.5, 63.0, 63.5, 64.0, 64.5, 65.0, 65.5, 66.0, 66.5, 67.0, 67.5, 68.0, 68.5, 69.0, 69.5, 70.0, 70.5, 71.0, 71.5, 72.0, 72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.5, 79.0, 79.5, 80.0, 80.5, 81.0, 81.5, 82.0, 82.5, 83.0, 83.5, 84.0, 84.5, 85.0, 85.5, 86.0, 86.5, 87.0, 87.5, 88.0, 88.5, 89.0, 89.5, 90.0, 90.5, 91.0, 91.5, 92.0, 92.5, 93.0, 93.5, 94.0, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 101.0, 101.5, 102.0, 102.5, 103.0, 103.5, 104.0, 104.5, 105.0, 105.5, 106.0, 106.5, 107.0, 107.5, 108.0, 108.5, 109.0, 109.5, 110.0, 110.5, 111.0, 111.5, 112.0)+cms.vdouble(112.5, 113.0, 113.5, 114.0, 114.5, 115.0, 115.5, 116.0, 116.5, 117.0, 117.5, 118.0, 118.5, 119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0, 125.5, 126.0, 126.5, 127.0, 127.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 44.0, 44.5, 45.0, 45.5, 46.0, 46.5, 47.0, 47.5, 48.0, 48.5, 49.0, 49.5, 50.0, 50.5, 51.0, 51.5, 52.0, 52.5, 53.0, 53.5, 54.0, 54.5, 55.0, 55.5, 56.0, 56.5, 57.0, 57.5, 58.0, 58.5, 59.0, 59.5, 60.0, 60.5, 61.0, 61.5, 62.0, 62.5, 63.0, 63.5, 64.0, 64.5, 65.0, 65.5, 66.0, 66.5, 67.0, 67.5, 68.0, 68.5, 69.0, 69.5, 70.0, 70.5, 71.0, 71.5, 72.0, 72.5, 73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0, 76.5, 77.0, 77.5, 78.0, 78.5, 79.0, 79.5, 80.0, 80.5, 81.0, 81.5, 82.0, 82.5, 83.0, 83.5, 84.0, 84.5, 85.0, 85.5, 86.0, 86.5, 87.0, 87.5, 88.0, 88.5, 89.0, 89.5, 90.0, 90.5, 91.0, 91.5, 92.0, 92.5, 93.0, 93.5, 94.0, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 101.0, 101.5, 102.0, 102.5, 103.0, 103.5, 104.0, 104.5, 105.0, 105.5, 106.0, 106.5, 107.0, 107.5, 108.0, 108.5, 109.0, 109.5, 110.0, 110.5, 111.0, 111.5)+cms.vdouble(112.0, 112.5, 113.0, 113.5, 114.0, 114.5, 115.0, 115.5, 116.0, 116.5, 117.0, 117.5, 118.0, 118.5, 119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0, 124.5, 125.0, 125.5, 126.0, 126.5, 127.0, 127.5)),
    L1EcalEtThresholdsNegativeEta = (cms.vdouble(0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625)+cms.vdouble(119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375)+cms.vdouble(119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125)+cms.vdouble(118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625)+cms.vdouble(118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875)+cms.vdouble(117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875)+cms.vdouble(117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25)+cms.vdouble(116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125)+cms.vdouble(116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125)+cms.vdouble(115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375)+cms.vdouble(115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375)+cms.vdouble(114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625)+cms.vdouble(114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375)+cms.vdouble(113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875)+cms.vdouble(113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5)+cms.vdouble(112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125)+cms.vdouble(112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625)+cms.vdouble(112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375)+cms.vdouble(111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625)+cms.vdouble(111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625)+cms.vdouble(110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875)+cms.vdouble(110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875)+cms.vdouble(109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75)+cms.vdouble(109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125)+cms.vdouble(108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125)+cms.vdouble(108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375)+cms.vdouble(107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875)+cms.vdouble(107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625)+cms.vdouble(106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125)),
    L1EcalEtThresholdsPositiveEta = (cms.vdouble(0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625)+cms.vdouble(119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375)+cms.vdouble(119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125)+cms.vdouble(118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625)+cms.vdouble(118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875)+cms.vdouble(117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875)+cms.vdouble(117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25)+cms.vdouble(116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125)+cms.vdouble(116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125)+cms.vdouble(115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375)+cms.vdouble(115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375)+cms.vdouble(114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625)+cms.vdouble(114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375)+cms.vdouble(113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875)+cms.vdouble(113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5)+cms.vdouble(112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125)+cms.vdouble(112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625)+cms.vdouble(112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375)+cms.vdouble(111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625)+cms.vdouble(111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625)+cms.vdouble(110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875)+cms.vdouble(110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875)+cms.vdouble(109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125, 108.75)+cms.vdouble(109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125, 108.28125)+cms.vdouble(108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375, 107.8125)+cms.vdouble(108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875, 107.34375)+cms.vdouble(107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625, 106.875)+cms.vdouble(107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125, 0.0, 0.46875, 0.9375, 1.40625, 1.875, 2.34375, 2.8125, 3.28125, 3.75, 4.21875, 4.6875, 5.15625, 5.625, 6.09375, 6.5625, 7.03125, 7.5, 7.96875, 8.4375, 8.90625, 9.375, 9.84375, 10.3125, 10.78125, 11.25, 11.71875, 12.1875, 12.65625, 13.125, 13.59375, 14.0625, 14.53125, 15.0, 15.46875, 15.9375, 16.40625, 16.875, 17.34375, 17.8125, 18.28125, 18.75, 19.21875, 19.6875, 20.15625, 20.625, 21.09375, 21.5625, 22.03125, 22.5, 22.96875, 23.4375, 23.90625, 24.375, 24.84375, 25.3125, 25.78125, 26.25, 26.71875, 27.1875, 27.65625, 28.125, 28.59375, 29.0625, 29.53125, 30.0, 30.46875, 30.9375, 31.40625, 31.875, 32.34375, 32.8125, 33.28125, 33.75, 34.21875, 34.6875, 35.15625, 35.625, 36.09375, 36.5625, 37.03125, 37.5, 37.96875, 38.4375, 38.90625, 39.375, 39.84375, 40.3125, 40.78125, 41.25, 41.71875, 42.1875, 42.65625, 43.125, 43.59375, 44.0625, 44.53125, 45.0, 45.46875, 45.9375, 46.40625, 46.875, 47.34375, 47.8125, 48.28125, 48.75, 49.21875, 49.6875, 50.15625, 50.625, 51.09375, 51.5625, 52.03125, 52.5, 52.96875, 53.4375, 53.90625, 54.375, 54.84375, 55.3125, 55.78125, 56.25, 56.71875, 57.1875, 57.65625, 58.125, 58.59375, 59.0625, 59.53125, 60.0, 60.46875, 60.9375, 61.40625, 61.875, 62.34375, 62.8125, 63.28125, 63.75, 64.21875, 64.6875, 65.15625, 65.625, 66.09375, 66.5625, 67.03125, 67.5, 67.96875, 68.4375, 68.90625, 69.375, 69.84375, 70.3125, 70.78125, 71.25, 71.71875, 72.1875, 72.65625, 73.125, 73.59375, 74.0625, 74.53125, 75.0, 75.46875, 75.9375, 76.40625, 76.875, 77.34375, 77.8125, 78.28125, 78.75, 79.21875, 79.6875, 80.15625, 80.625, 81.09375, 81.5625, 82.03125, 82.5, 82.96875, 83.4375, 83.90625, 84.375, 84.84375, 85.3125, 85.78125, 86.25, 86.71875, 87.1875, 87.65625, 88.125, 88.59375, 89.0625, 89.53125, 90.0, 90.46875, 90.9375, 91.40625, 91.875, 92.34375, 92.8125, 93.28125, 93.75, 94.21875, 94.6875, 95.15625, 95.625, 96.09375, 96.5625, 97.03125, 97.5, 97.96875, 98.4375, 98.90625, 99.375, 99.84375, 100.3125, 100.78125, 101.25, 101.71875, 102.1875, 102.65625, 103.125, 103.59375, 104.0625, 104.53125, 105.0, 105.46875, 105.9375, 106.40625)+cms.vdouble(106.875, 107.34375, 107.8125, 108.28125, 108.75, 109.21875, 109.6875, 110.15625, 110.625, 111.09375, 111.5625, 112.03125, 112.5, 112.96875, 113.4375, 113.90625, 114.375, 114.84375, 115.3125, 115.78125, 116.25, 116.71875, 117.1875, 117.65625, 118.125, 118.59375, 119.0625, 119.53125))
)


process.DAFFittingSmoother = cms.ESProducer("KFFittingSmootherESProducer",
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('DAFFitter'),
    ComponentName = cms.string('DAFFittingSmoother'),
    Smoother = cms.string('DAFSmoother'),
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    MinNumberOfHits = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True)
)


process.gsfElectronChi2 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    MaxChi2 = cms.double(100000.0),
    nSigma = cms.double(3.0),
    ComponentName = cms.string('gsfElectronChi2')
)


process.fwdGsfElectronPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(1.6),
    useRungeKutta = cms.bool(False),
    Mass = cms.double(0.000511),
    PropagationDirection = cms.string('alongMomentum'),
    ComponentName = cms.string('fwdGsfElectronPropagator')
)


process.l1CSCTFConfig = cms.ESProducer("CSCTFConfigProducer",
    registersSP9 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP8 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP1 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP3 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP2 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP5 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP4 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP7 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP6 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP11 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP10 = cms.vstring('CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    registersSP12 = cms.vstring('CSR_LQE F1 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F1 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F2 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F3 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F4 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M1 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M2 0xFFFF # Allow LCT of any quality', 
        'CSR_LQE F5 M3 0xFFFF # Allow LCT of any quality', 
        'CSR_KFL SP MA 0x0000 # Kill no fiber link', 
        'CSR_REQ SP MA 0x801F # Triggering on singles and running the core', 
        'DAT_FTR SP MA 0xFF   # Charge Quality and Rank of fake track, produced from singles', 
        'CSR_SFC SP MA 0x1000 # Output muon pT to spy on', 
        'CSR_SCC SP MA 0x0230 # Core settings (i.e. [0:1] BXA_depth=0, [4:5] Q=1,2, [7] MB, [8:9] Pretrigger=2)', 
        'CNT_ETA SP MA 0x0    # Reset ETA counter to set EtaMin, EtaMax, and EtaWin', 
        'DAT_ETA SP MA 0x0    # EtaMin[0] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[1] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[2] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[3] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[4] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[5] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[6] = 0', 
        'DAT_ETA SP MA 0x0    # EtaMin[7] = 0', 
        'DAT_ETA SP MA 0x7F   # EtaMax[0] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[1] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[2] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[3] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[4] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[5] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[6] = 127', 
        'DAT_ETA SP MA 0x7F   # EtaMax[7] = 127', 
        'DAT_ETA SP MA 0x5    # EtaWin[0] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[1] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[2] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[3] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[4] = 5', 
        'DAT_ETA SP MA 0x5    # EtaWin[5] = 5', 
        'DAT_ETA SP MA 0x2    # mindphip     = 2', 
        'DAT_ETA SP MA 0x4    # mindeta_accp = 4', 
        'DAT_ETA SP MA 0x10   # maxdeta_accp = 16', 
        'DAT_ETA SP MA 0x40   # maxdphi_accp = 128'),
    ptLUT_path = cms.string(''),
    alignment = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 
        0.0, 0.0, 0.0, 0.0, 0.0, 
        0.0, 0.0, 0.0, 0.0, 0.0, 
        0.0)
)


process.thCkfTrajectoryFilter = cms.ESProducer("TrajectoryFilterESProducer",
    filterPset = cms.PSet(
        minimumNumberOfHits = cms.int32(3),
        minPt = cms.double(0.3),
        minHitsMinPt = cms.int32(3),
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        maxLostHits = cms.int32(0),
        maxNumberOfHits = cms.int32(-1),
        maxConsecLostHits = cms.int32(1),
        nSigmaMinPt = cms.double(5.0),
        chargeSignificance = cms.double(-1.0)
    ),
    ComponentName = cms.string('thCkfTrajectoryFilter')
)


process.BeamHaloPropagatorOpposite = cms.ESProducer("BeamHaloPropagatorESProducer",
    ComponentName = cms.string('BeamHaloPropagatorOpposite'),
    CrossingTrackerPropagator = cms.string('BeamHaloSHPropagatorOpposite'),
    PropagationDirection = cms.string('oppositeToMomentum'),
    EndCapTrackerPropagator = cms.string('BeamHaloMPropagatorOpposite')
)


process.l1GtPrescaleFactorsAlgoTrig = cms.ESProducer("L1GtPrescaleFactorsAlgoTrigTrivialProducer",
    PrescaleFactorsSet = cms.VPSet(cms.PSet(
        PrescaleFactors = cms.vint32(1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 
            1, 1, 1)
    ))
)


process.myTTRHBuilderWithoutAngle4PixelTriplets = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    StripCPE = cms.string('Fake'),
    Matcher = cms.string('StandardMatcher'),
    PixelCPE = cms.string('PixelCPEGeneric'),
    ComponentName = cms.string('TTRHBuilderWithoutAngle4PixelTriplets')
)


process.SteppingHelixPropagatorAny = cms.ESProducer("SteppingHelixPropagatorESProducer",
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('anyDirection'),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    endcapShiftInZNeg = cms.double(0.0),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    returnTangentPlane = cms.bool(True),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    ComponentName = cms.string('SteppingHelixPropagatorAny'),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    endcapShiftInZPos = cms.double(0.0)
)


process.GsfTrajectoryFitter = cms.ESProducer("GsfTrajectoryFitterESProducer",
    Merger = cms.string('CloseComponentsMerger5D'),
    ComponentName = cms.string('GsfTrajectoryFitter'),
    MaterialEffectsUpdator = cms.string('ElectronMaterialEffects'),
    GeometricalPropagator = cms.string('fwdAnalyticalPropagator')
)


process.cosmicsNavigationSchoolESProducer = cms.ESProducer("SkippingLayerCosmicNavigationSchoolESProducer",
    noPXB = cms.bool(False),
    noTID = cms.bool(False),
    noPXF = cms.bool(False),
    noTIB = cms.bool(False),
    ComponentName = cms.string('CosmicNavigationSchool'),
    allSelf = cms.bool(True),
    noTEC = cms.bool(False),
    noTOB = cms.bool(False),
    selfSearch = cms.bool(True)
)


process.hoDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('HODetIdAssociator'),
    etaBinSize = cms.double(0.087),
    nEta = cms.int32(30),
    nPhi = cms.int32(72)
)


process.l1csctpconf = cms.ESProducer("L1CSCTriggerPrimitivesConfigProducer",
    alctParam = cms.PSet(
        alctAccelMode = cms.uint32(1),
        alctTrigMode = cms.uint32(3),
        alctDriftDelay = cms.uint32(3),
        alctNplanesHitAccelPretrig = cms.uint32(2),
        alctL1aWindowWidth = cms.uint32(5),
        alctNplanesHitPattern = cms.uint32(4),
        alctNplanesHitAccelPattern = cms.uint32(4),
        alctFifoTbins = cms.uint32(16),
        alctNplanesHitPretrig = cms.uint32(2),
        alctFifoPretrig = cms.uint32(10)
    ),
    isTMB07 = cms.bool(True),
    clctParamMTCC2 = cms.PSet(
        clctDriftDelay = cms.uint32(2),
        clctMinSeparation = cms.uint32(10),
        clctPidThreshPretrig = cms.uint32(2),
        clctFifoTbins = cms.uint32(12),
        clctNplanesHitPretrig = cms.uint32(4),
        clctHitPersist = cms.uint32(6),
        clctFifoPretrig = cms.uint32(7),
        clctNplanesHitPattern = cms.uint32(1)
    ),
    isMTCC = cms.bool(False),
    clctParam = cms.PSet(
        clctDriftDelay = cms.uint32(2),
        clctMinSeparation = cms.uint32(10),
        clctPidThreshPretrig = cms.uint32(2),
        clctFifoTbins = cms.uint32(12),
        clctNplanesHitPretrig = cms.uint32(2),
        clctHitPersist = cms.uint32(6),
        clctFifoPretrig = cms.uint32(7),
        clctNplanesHitPattern = cms.uint32(4)
    ),
    alctParamMTCC2 = cms.PSet(
        alctAccelMode = cms.uint32(0),
        alctTrigMode = cms.uint32(2),
        alctDriftDelay = cms.uint32(2),
        alctNplanesHitAccelPretrig = cms.uint32(2),
        alctL1aWindowWidth = cms.uint32(7),
        alctNplanesHitPattern = cms.uint32(4),
        alctNplanesHitAccelPattern = cms.uint32(4),
        alctFifoTbins = cms.uint32(16),
        alctNplanesHitPretrig = cms.uint32(2),
        alctFifoPretrig = cms.uint32(10)
    )
)


process.RCTConfigProducers = cms.ESProducer("RCTConfigProducers",
    eGammaHCalScaleFactors = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0),
    eMaxForFGCut = cms.double(50.0),
    noiseVetoHB = cms.bool(False),
    jscQuietThresholdEndcap = cms.uint32(3),
    hOeCut = cms.double(0.05),
    eGammaECalScaleFactors = cms.vdouble(1.0, 1.01, 1.02, 1.02, 1.02, 
        1.06, 1.04, 1.04, 1.05, 1.09, 
        1.1, 1.1, 1.15, 1.2, 1.27, 
        1.29, 1.32, 1.52, 1.52, 1.48, 
        1.4, 1.32, 1.26, 1.21, 1.17, 
        1.15, 1.15, 1.15),
    eMinForHoECut = cms.double(3.0),
    jscQuietThresholdBarrel = cms.uint32(3),
    jetMETHCalScaleFactors = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0),
    jetMETECalScaleFactors = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        1.0, 1.0, 1.0),
    hActivityCut = cms.double(3.0),
    noiseVetoHEplus = cms.bool(False),
    eicIsolationThreshold = cms.uint32(3),
    jetMETLSB = cms.double(0.5),
    eActivityCut = cms.double(3.0),
    eMinForFGCut = cms.double(3.0),
    eGammaLSB = cms.double(0.5),
    eMaxForHoECut = cms.double(60.0),
    hMinForHoECut = cms.double(3.0),
    noiseVetoHEminus = cms.bool(False)
)


process.BeamHaloSHPropagatorAlong = cms.ESProducer("SteppingHelixPropagatorESProducer",
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('alongMomentum'),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    endcapShiftInZNeg = cms.double(0.0),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    returnTangentPlane = cms.bool(True),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    ComponentName = cms.string('BeamHaloSHPropagatorAlong'),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    endcapShiftInZPos = cms.double(0.0)
)


process.EcalElectronicsMappingBuilder = cms.ESProducer("EcalElectronicsMappingBuilder",
    MapFile = cms.untracked.string('Geometry/EcalMapping/data/EEMap.txt')
)


process.StripCPEfromTrackAngleESProducer = cms.ESProducer("StripCPEfromTrackAngleESProducer",
    ComponentName = cms.string('StripCPEfromTrackAngle')
)


process.FittingSmootherRKP5 = cms.ESProducer("KFFittingSmootherESProducer",
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('RKFitter'),
    ComponentName = cms.string('FittingSmootherRKP5'),
    Smoother = cms.string('RKSmoother'),
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    MinNumberOfHits = cms.int32(4),
    NoInvalidHitsBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True)
)


process.SteppingHelixPropagatorL2Along = cms.ESProducer("SteppingHelixPropagatorESProducer",
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('alongMomentum'),
    useTuningForL2Speed = cms.bool(True),
    ComponentName = cms.string('SteppingHelixPropagatorL2Along'),
    useIsYokeFlag = cms.bool(True),
    endcapShiftInZNeg = cms.double(0.0),
    SetVBFPointer = cms.bool(False),
    AssumeNoMaterial = cms.bool(False),
    endcapShiftInZPos = cms.double(0.0),
    useInTeslaFromMagField = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    useEndcapShiftsInZ = cms.bool(False),
    sendLogWarning = cms.bool(False),
    useMatVolumes = cms.bool(True),
    debug = cms.bool(False),
    ApplyRadX0Correction = cms.bool(True),
    useMagVolumes = cms.bool(True),
    returnTangentPlane = cms.bool(True)
)


process.GlobalTrackingGeometryESProducer = cms.ESProducer("GlobalTrackingGeometryESProducer")


process.RKTrajectorySmoother = cms.ESProducer("KFTrajectorySmootherESProducer",
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3),
    ComponentName = cms.string('RKSmoother'),
    Estimator = cms.string('Chi2'),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('RungeKuttaTrackerPropagator')
)


process.thlayerpairs = cms.ESProducer("MixedLayerPairsESProducer",
    FPix = cms.PSet(
        hitErrorRZ = cms.double(0.0036),
        hitErrorRPhi = cms.double(0.0051),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4MixedPairs'),
        HitProducer = cms.string('thPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    layerList = cms.vstring('BPix1+BPix2', 
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
        'TEC2_neg+TEC3_neg'),
    TEC = cms.PSet(
        matchedRecHits = cms.InputTag("thStripRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        minRing = cms.int32(1),
        maxRing = cms.int32(1)
    ),
    BPix = cms.PSet(
        hitErrorRZ = cms.double(0.006),
        hitErrorRPhi = cms.double(0.0027),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4MixedPairs'),
        HitProducer = cms.string('thPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    ComponentName = cms.string('ThLayerPairs')
)


process.EcalLaserCorrectionService = cms.ESProducer("EcalLaserCorrectionService")


process.L1GctConfigProducers = cms.ESProducer("L1GctConfigProducers",
    JetFinderCentralJetSeed = cms.uint32(1),
    CalibrationStyle = cms.string('PowerSeries'),
    HfLutBitCountThresholds = cms.vuint32(1, 2, 3, 4, 5, 
        6, 7),
    HfLutEtSumThresholds = cms.vuint32(2, 4, 6, 8, 10, 
        12, 14),
    L1CaloHtScaleLsbInGeV = cms.double(1.0),
    PowerSeriesCoefficients = cms.PSet(
        nonTauJetCalib10 = cms.vdouble(1.0),
        nonTauJetCalib1 = cms.vdouble(1.0),
        tauJetCalib0 = cms.vdouble(1.0),
        nonTauJetCalib5 = cms.vdouble(1.0),
        nonTauJetCalib7 = cms.vdouble(1.0),
        nonTauJetCalib2 = cms.vdouble(1.0),
        nonTauJetCalib8 = cms.vdouble(1.0),
        nonTauJetCalib9 = cms.vdouble(1.0),
        nonTauJetCalib4 = cms.vdouble(1.0),
        nonTauJetCalib3 = cms.vdouble(1.0),
        tauJetCalib4 = cms.vdouble(1.0),
        tauJetCalib5 = cms.vdouble(1.0),
        tauJetCalib6 = cms.vdouble(1.0),
        nonTauJetCalib0 = cms.vdouble(1.0),
        nonTauJetCalib6 = cms.vdouble(1.0),
        tauJetCalib1 = cms.vdouble(1.0),
        tauJetCalib2 = cms.vdouble(1.0),
        tauJetCalib3 = cms.vdouble(1.0)
    ),
    JetFinderForwardJetSeed = cms.uint32(1),
    OrcaStyleCoefficients = cms.PSet(
        tauJetCalib0 = cms.vdouble(47.4, -20.7, 0.7922, 9.53e-05),
        nonTauJetCalib1 = cms.vdouble(49.4, -22.5, 0.7867, 9.6e-05),
        nonTauJetCalib10 = cms.vdouble(9.3, 1.3, 0.2719, 0.003418),
        tauJetCalib3 = cms.vdouble(49.3, -22.9, 0.7331, 0.0001221),
        tauJetCalib1 = cms.vdouble(49.4, -22.5, 0.7867, 9.6e-05),
        tauJetCalib4 = cms.vdouble(48.2, -24.5, 0.7706, 0.000128),
        nonTauJetCalib8 = cms.vdouble(13.1, -4.5, 0.7071, 7.26e-05),
        nonTauJetCalib9 = cms.vdouble(12.4, -3.8, 0.6558, 0.000489),
        tauJetCalib2 = cms.vdouble(47.1, -22.2, 0.7645, 0.0001209),
        tauJetCalib5 = cms.vdouble(42.0, -23.9, 0.7945, 0.0001458),
        nonTauJetCalib2 = cms.vdouble(47.1, -22.2, 0.7645, 0.0001209),
        nonTauJetCalib3 = cms.vdouble(49.3, -22.9, 0.7331, 0.0001221),
        tauJetCalib6 = cms.vdouble(33.8, -22.1, 0.8202, 0.0001403),
        nonTauJetCalib0 = cms.vdouble(47.4, -20.7, 0.7922, 9.53e-05),
        nonTauJetCalib6 = cms.vdouble(33.8, -22.1, 0.8202, 0.0001403),
        nonTauJetCalib7 = cms.vdouble(17.1, -6.6, 0.6958, 6.88e-05),
        nonTauJetCalib4 = cms.vdouble(48.2, -24.5, 0.7706, 0.000128),
        nonTauJetCalib5 = cms.vdouble(42.0, -23.9, 0.7945, 0.0001458)
    ),
    ConvertEtValuesToEnergy = cms.bool(False),
    jetCounterSetup = cms.PSet(
        jetCountersNegativeWheel = cms.VPSet(cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_1')
        ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_1', 
                    'JC_centralEta_6')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_11')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_11', 
                    'JC_centralEta_6')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_19')
            )),
        jetCountersPositiveWheel = cms.VPSet(cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_1')
        ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_1', 
                    'JC_centralEta_6')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_11')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_11', 
                    'JC_centralEta_6')
            ), 
            cms.PSet(
                cutDescriptionList = cms.vstring('JC_minRank_19')
            ))
    ),
    PiecewiseCubicCoefficients = cms.PSet(
        tauJetCalib0 = cms.vdouble(500.0, 100.0, 17.7409, 0.351901, -0.000701462, 
            5.77204e-07, 5.0, 0.720604, 1.25179, -0.0150777, 
            7.13711e-05),
        nonTauJetCalib1 = cms.vdouble(500.0, 100.0, 20.0549, 0.321867, -0.00064901, 
            5.50042e-07, 5.0, 1.30465, 1.2774, -0.0159193, 
            7.64496e-05),
        nonTauJetCalib10 = cms.vdouble(150.0, 80.0, 1.70475, -0.142171, 0.00104963, 
            -1.62214e-05, 5.0, 1.70475, -0.142171, 0.00104963, 
            -1.62214e-05),
        tauJetCalib3 = cms.vdouble(500.0, 100.0, 27.7822, 0.155986, -0.000266441, 
            6.69814e-08, 5.0, 2.64613, 1.30745, -0.0180964, 
            8.83567e-05),
        tauJetCalib1 = cms.vdouble(500.0, 100.0, 20.0549, 0.321867, -0.00064901, 
            5.50042e-07, 5.0, 1.30465, 1.2774, -0.0159193, 
            7.64496e-05),
        tauJetCalib4 = cms.vdouble(500.0, 100.0, 26.6384, 0.0567369, -0.000416292, 
            2.60929e-07, 5.0, 2.63299, 1.16558, -0.0170351, 
            7.95703e-05),
        nonTauJetCalib8 = cms.vdouble(250.0, 150.0, 1.38861, 0.0362661, 0.0, 
            0.0, 5.0, 1.87993, 0.0329907, 0.0, 
            0.0),
        nonTauJetCalib9 = cms.vdouble(200.0, 80.0, 35.0095, -0.669677, 0.00208498, 
            -1.50554e-06, 5.0, 3.16074, -0.114404, 0.0, 
            0.0),
        tauJetCalib2 = cms.vdouble(500.0, 100.0, 24.3454, 0.257989, -0.000450184, 
            3.09951e-07, 5.0, 2.1034, 1.32441, -0.0173659, 
            8.50669e-05),
        tauJetCalib5 = cms.vdouble(500.0, 100.0, 29.5396, 0.001137, -0.000145232, 
            6.91445e-08, 5.0, 4.16752, 1.08477, -0.016134, 
            7.69652e-05),
        nonTauJetCalib2 = cms.vdouble(500.0, 100.0, 24.3454, 0.257989, -0.000450184, 
            3.09951e-07, 5.0, 2.1034, 1.32441, -0.0173659, 
            8.50669e-05),
        nonTauJetCalib3 = cms.vdouble(500.0, 100.0, 27.7822, 0.155986, -0.000266441, 
            6.69814e-08, 5.0, 2.64613, 1.30745, -0.0180964, 
            8.83567e-05),
        tauJetCalib6 = cms.vdouble(500.0, 100.0, 30.1405, -0.14281, 0.000555849, 
            -7.52446e-07, 5.0, 4.79283, 0.672125, -0.00879174, 
            3.65776e-05),
        nonTauJetCalib0 = cms.vdouble(500.0, 100.0, 17.7409, 0.351901, -0.000701462, 
            5.77204e-07, 5.0, 0.720604, 1.25179, -0.0150777, 
            7.13711e-05),
        nonTauJetCalib6 = cms.vdouble(500.0, 100.0, 30.1405, -0.14281, 0.000555849, 
            -7.52446e-07, 5.0, 4.79283, 0.672125, -0.00879174, 
            3.65776e-05),
        nonTauJetCalib7 = cms.vdouble(300.0, 80.0, 30.2715, -0.539688, 0.00499898, 
            -1.2204e-05, 5.0, 1.97284, 0.0610729, 0.00671548, 
            -7.22583e-05),
        nonTauJetCalib4 = cms.vdouble(500.0, 100.0, 26.6384, 0.0567369, -0.000416292, 
            2.60929e-07, 5.0, 2.63299, 1.16558, -0.0170351, 
            7.95703e-05),
        nonTauJetCalib5 = cms.vdouble(500.0, 100.0, 29.5396, 0.001137, -0.000145232, 
            6.91445e-08, 5.0, 4.16752, 1.08477, -0.016134, 
            7.69652e-05)
    ),
    L1CaloJetZeroSuppressionThresholdInGeV = cms.double(5.0)
)


process.beamHaloNavigationSchoolESProducer = cms.ESProducer("NavigationSchoolESProducer",
    ComponentName = cms.string('BeamHaloNavigationSchool')
)


process.MeasurementTracker = cms.ESProducer("MeasurementTrackerESProducer",
    stripLazyGetterProducer = cms.string(''),
    StripCPE = cms.string('StripCPEfromTrackAngle'),
    OnDemand = cms.bool(False),
    UseStripAPVFiberQualityDB = cms.bool(True),
    DebugStripModuleQualityDB = cms.untracked.bool(False),
    ComponentName = cms.string(''),
    stripClusterProducer = cms.string('siStripClusters'),
    Regional = cms.bool(False),
    UseStripModuleQualityDB = cms.bool(True),
    DebugStripAPVFiberQualityDB = cms.untracked.bool(False),
    HitMatcher = cms.string('StandardMatcher'),
    DebugStripStripQualityDB = cms.untracked.bool(False),
    pixelClusterProducer = cms.string('siPixelClusters'),
    UseStripStripQualityDB = cms.bool(True),
    MaskBadAPVFibers = cms.bool(False),
    PixelCPE = cms.string('PixelCPEGeneric')
)


process.SmartPropagatorOpposite = cms.ESProducer("SmartPropagatorESProducer",
    Epsilon = cms.double(5.0),
    TrackerPropagator = cms.string('PropagatorWithMaterialOpposite'),
    MuonPropagator = cms.string('SteppingHelixPropagatorOpposite'),
    PropagationDirection = cms.string('oppositeToMomentum'),
    ComponentName = cms.string('SmartPropagatorOpposite')
)


process.TrajectoryFilterForPixelMatchGsfElectrons = cms.ESProducer("TrajectoryFilterESProducer",
    filterPset = cms.PSet(
        minimumNumberOfHits = cms.int32(5),
        minHitsMinPt = cms.int32(-1),
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        maxLostHits = cms.int32(1),
        maxNumberOfHits = cms.int32(-1),
        maxConsecLostHits = cms.int32(1),
        chargeSignificance = cms.double(-1.0),
        nSigmaMinPt = cms.double(5.0),
        minPt = cms.double(3.0)
    ),
    ComponentName = cms.string('TrajectoryFilterForPixelMatchGsfElectrons')
)


process.mixedlayertriplets = cms.ESProducer("MixedLayerTripletsESProducer",
    layerList = cms.vstring('BPix1+BPix2+BPix3', 
        'BPix1+BPix2+FPix1_pos', 
        'BPix1+BPix2+FPix1_neg', 
        'BPix1+FPix1_pos+FPix2_pos', 
        'BPix1+FPix1_neg+FPix2_neg', 
        'BPix1+BPix2+TIB1', 
        'BPix1+BPix3+TIB1', 
        'BPix2+BPix3+TIB1', 
        'BPix1+FPix1_pos+TID1_pos', 
        'BPix1+FPix1_neg+TID1_neg', 
        'BPix1+FPix1_pos+TID2_pos', 
        'BPix1+FPix1_neg+TID2_neg', 
        'FPix1_pos+FPix2_pos+TEC1_pos', 
        'FPix1_neg+FPix2_neg+TEC1_neg', 
        'FPix1_pos+FPix2_pos+TEC2_pos', 
        'FPix1_neg+FPix2_neg+TEC2_neg'),
    ComponentName = cms.string('MixedLayerTriplets'),
    TEC = cms.PSet(
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        TTRHBuilder = cms.string('WithTrackAngle')
    ),
    FPix = cms.PSet(
        hitErrorRZ = cms.double(0.0036),
        hitErrorRPhi = cms.double(0.0051),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4MixedTriplets'),
        HitProducer = cms.string('siPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    TID = cms.PSet(
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        TTRHBuilder = cms.string('WithTrackAngle')
    ),
    BPix = cms.PSet(
        hitErrorRZ = cms.double(0.006),
        hitErrorRPhi = cms.double(0.0027),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4MixedTriplets'),
        HitProducer = cms.string('siPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    TIB = cms.PSet(
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        TTRHBuilder = cms.string('WithTrackAngle')
    )
)


process.l1GtTriggerMaskAlgoTrig = cms.ESProducer("L1GtTriggerMaskAlgoTrigTrivialProducer",
    TriggerMask = cms.vuint32(0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 
        0, 0, 0)
)


process.BeamHaloMPropagatorAlong = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(10000),
    useRungeKutta = cms.bool(False),
    Mass = cms.double(0.105),
    PropagationDirection = cms.string('alongMomentum'),
    ComponentName = cms.string('BeamHaloMPropagatorAlong')
)


process.GlbMuKFFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('GlbMuKFFitter'),
    Estimator = cms.string('Chi2EstimatorForMuRefit'),
    minHits = cms.int32(3),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('SmartPropagatorAnyRK')
)


process.rpcconf = cms.ESProducer("RPCTriggerConfig",
    filedir = cms.untracked.string('L1Trigger/RPCTrigger/data/Eff90PPT12/'),
    PACsPerTower = cms.untracked.int32(12)
)


process.ckfBaseTrajectoryFilter = cms.ESProducer("TrajectoryFilterESProducer",
    filterPset = cms.PSet(
        minimumNumberOfHits = cms.int32(5),
        minPt = cms.double(0.9),
        minHitsMinPt = cms.int32(3),
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        maxLostHits = cms.int32(1),
        maxNumberOfHits = cms.int32(-1),
        maxConsecLostHits = cms.int32(1),
        nSigmaMinPt = cms.double(5.0),
        chargeSignificance = cms.double(-1.0)
    ),
    ComponentName = cms.string('ckfBaseTrajectoryFilter')
)


process.templates = cms.ESProducer("PixelCPETemplateRecoESProducer",
    ComponentName = cms.string('PixelCPETemplateReco'),
    TanLorentzAnglePerTesla = cms.double(0.106),
    Alpha2Order = cms.bool(True),
    speed = cms.int32(0),
    PixelErrorParametrization = cms.string('NOTcmsim'),
    UseClusterSplitter = cms.bool(False)
)


process.idealForDigiCSCGeometry = cms.ESProducer("CSCGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    debugV = cms.untracked.bool(False),
    useGangedStripsInME1a = cms.bool(True),
    alignmentsLabel = cms.string('fakeForIdeal'),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True),
    useCentreTIOffsets = cms.bool(False),
    applyAlignment = cms.bool(False)
)


process.fourthlayerpairs = cms.ESProducer("PixelLessLayerPairsESProducer",
    layerList = cms.vstring('TIB1+TIB2', 
        'TIB1+TID1_pos', 
        'TIB1+TID2_pos', 
        'TIB1+TID1_neg', 
        'TIB1+TID2_neg', 
        'TID1_pos+TID2_pos', 
        'TID2_pos+TID3_pos', 
        'TID3_pos+TEC2_pos', 
        'TEC2_pos+TEC3_pos', 
        'TID1_neg+TID2_neg', 
        'TID2_neg+TID3_neg', 
        'TID3_neg+TEC2_neg', 
        'TEC2_neg+TEC3_neg'),
    TID1 = cms.PSet(
        useSimpleRphiHitsCleaner = cms.untracked.bool(False),
        minRing = cms.int32(1),
        matchedRecHits = cms.InputTag("fourthStripRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("fourthStripRecHits","rphiRecHit"),
        maxRing = cms.int32(2)
    ),
    TID3 = cms.PSet(
        useSimpleRphiHitsCleaner = cms.untracked.bool(False),
        minRing = cms.int32(1),
        matchedRecHits = cms.InputTag("fourthStripRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("fourthStripRecHits","rphiRecHit"),
        maxRing = cms.int32(2)
    ),
    TID2 = cms.PSet(
        useSimpleRphiHitsCleaner = cms.untracked.bool(False),
        minRing = cms.int32(1),
        matchedRecHits = cms.InputTag("fourthStripRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("fourthStripRecHits","rphiRecHit"),
        maxRing = cms.int32(3)
    ),
    ComponentName = cms.string('FourthLayerPairs'),
    TEC = cms.PSet(
        matchedRecHits = cms.InputTag("fourthStripRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        minRing = cms.int32(1),
        maxRing = cms.int32(2)
    ),
    TIB = cms.PSet(
        TTRHBuilder = cms.string('WithTrackAngle'),
        matchedRecHits = cms.InputTag("fourthStripRecHits","matchedRecHit"),
        useSimpleRphiHitsCleaner = cms.untracked.bool(False),
        rphiRecHits = cms.InputTag("fourthStripRecHits","rphiRecHit")
    )
)


process.hcal_db_producer = cms.ESProducer("HcalDbProducer",
    file = cms.untracked.string(''),
    dump = cms.untracked.vstring('')
)


process.trajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('TrajectoryCleanerBySharedHits')
)


process.fwdAnalyticalPropagator = cms.ESProducer("AnalyticalPropagatorESProducer",
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('fwdAnalyticalPropagator'),
    PropagationDirection = cms.string('alongMomentum')
)


process.EstimatorForSTA = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    MaxChi2 = cms.double(1000.0),
    nSigma = cms.double(3.0),
    ComponentName = cms.string('Chi2STA')
)


process.StripCPEESProducer = cms.ESProducer("StripCPEESProducer",
    ComponentName = cms.string('SimpleStripCPE')
)


process.TrajectoryFilterForConversions = cms.ESProducer("TrajectoryFilterESProducer",
    filterPset = cms.PSet(
        minimumNumberOfHits = cms.int32(3),
        minHitsMinPt = cms.int32(-1),
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        maxLostHits = cms.int32(1),
        maxNumberOfHits = cms.int32(-1),
        maxConsecLostHits = cms.int32(1),
        chargeSignificance = cms.double(-1.0),
        nSigmaMinPt = cms.double(5.0),
        minPt = cms.double(0.9)
    ),
    ComponentName = cms.string('TrajectoryFilterForConversions')
)


process.caloDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('CaloDetIdAssociator'),
    etaBinSize = cms.double(0.087),
    nEta = cms.int32(70),
    nPhi = cms.int32(72)
)


process.KullbackLeiblerDistance5D = cms.ESProducer("DistanceBetweenComponentsESProducer5D",
    ComponentName = cms.string('KullbackLeiblerDistance5D'),
    DistanceMeasure = cms.string('KullbackLeibler')
)


process.MuonNumberingInitialization = cms.ESProducer("MuonNumberingInitialization")


process.HcalTopologyIdealEP = cms.ESProducer("HcalTopologyIdealEP")


process.sistripconn = cms.ESProducer("SiStripConnectivity")


process.AnyDirectionAnalyticalPropagator = cms.ESProducer("AnalyticalPropagatorESProducer",
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('AnyDirectionAnalyticalPropagator'),
    PropagationDirection = cms.string('anyDirection')
)


process.MuonTransientTrackingRecHitBuilderESProducer = cms.ESProducer("MuonTransientTrackingRecHitBuilderESProducer",
    ComponentName = cms.string('MuonRecHitBuilder')
)


process.fakeForIdealAlignment = cms.ESProducer("FakeAlignmentProducer",
    appendToDataLabel = cms.string('fakeForIdeal')
)


process.KFFittingSmootheForSTA = cms.ESProducer("KFFittingSmootherESProducer",
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('KFFitterSTA'),
    ComponentName = cms.string('KFFitterSmootherSTA'),
    Smoother = cms.string('KFSmootherSTA'),
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    MinNumberOfHits = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True)
)


process.L1MuGMTScales = cms.ESProducer("L1MuGMTScalesProducer",
    minDeltaPhi = cms.double(-0.1963495),
    signedPackingDeltaPhi = cms.bool(True),
    maxOvlEtaDT = cms.double(1.3),
    nbitPackingOvlEtaCSC = cms.int32(4),
    scaleReducedEtaDT = cms.vdouble(0.0, 0.22, 0.27, 0.58, 0.77, 
        0.87, 0.92, 1.24, 1.3),
    scaleReducedEtaFwdRPC = cms.vdouble(1.04, 1.24, 1.36, 1.48, 1.61, 
        1.73, 1.85, 1.97, 2.1),
    nbitPackingOvlEtaFwdRPC = cms.int32(4),
    nbinsDeltaEta = cms.int32(15),
    minOvlEtaCSC = cms.double(0.9),
    scaleReducedEtaCSC = cms.vdouble(0.9, 1.06, 1.26, 1.46, 1.66, 
        1.86, 2.06, 2.26, 2.5),
    nbinsOvlEtaFwdRPC = cms.int32(7),
    nbitPackingReducedEta = cms.int32(4),
    scaleOvlEtaRPC = cms.vdouble(0.72, 0.83, 0.93, 1.04, 1.14, 
        1.24, 1.36, 1.48),
    signedPackingDeltaEta = cms.bool(True),
    nbinsOvlEtaDT = cms.int32(7),
    offsetDeltaPhi = cms.int32(4),
    nbinsReducedEta = cms.int32(8),
    nbitPackingDeltaPhi = cms.int32(3),
    offsetDeltaEta = cms.int32(7),
    nbitPackingOvlEtaBrlRPC = cms.int32(4),
    nbinsDeltaPhi = cms.int32(8),
    nbinsOvlEtaBrlRPC = cms.int32(7),
    minDeltaEta = cms.double(-0.3),
    maxDeltaPhi = cms.double(0.1527163),
    maxOvlEtaCSC = cms.double(1.25),
    scaleReducedEtaBrlRPC = cms.vdouble(0.0, 0.06, 0.25, 0.41, 0.54, 
        0.7, 0.83, 0.93, 1.04),
    nbinsOvlEtaCSC = cms.int32(7),
    nbitPackingDeltaEta = cms.int32(4),
    maxDeltaEta = cms.double(0.3),
    minOvlEtaDT = cms.double(0.73125),
    nbitPackingOvlEtaDT = cms.int32(4)
)


process.thMeasurementTracker = cms.ESProducer("MeasurementTrackerESProducer",
    stripLazyGetterProducer = cms.string(''),
    StripCPE = cms.string('StripCPEfromTrackAngle'),
    OnDemand = cms.bool(False),
    UseStripAPVFiberQualityDB = cms.bool(True),
    DebugStripModuleQualityDB = cms.untracked.bool(False),
    ComponentName = cms.string('thMeasurementTracker'),
    stripClusterProducer = cms.string('thClusters'),
    Regional = cms.bool(False),
    UseStripModuleQualityDB = cms.bool(True),
    DebugStripAPVFiberQualityDB = cms.untracked.bool(False),
    HitMatcher = cms.string('StandardMatcher'),
    DebugStripStripQualityDB = cms.untracked.bool(False),
    pixelClusterProducer = cms.string('thClusters'),
    UseStripStripQualityDB = cms.bool(True),
    MaskBadAPVFibers = cms.bool(False),
    PixelCPE = cms.string('PixelCPEGeneric')
)


process.TrackerGeometricDetESModule = cms.ESProducer("TrackerGeometricDetESModule",
    fromDDD = cms.bool(True)
)


process.L1MuGMTParameters = cms.ESProducer("L1MuGMTParametersProducer",
    MergeMethodSRKFwd = cms.string('takeCSC'),
    SubsystemMask = cms.uint32(0),
    HaloOverwritesMatchedFwd = cms.bool(True),
    PhiWeight_barrel = cms.double(1.0),
    MergeMethodISOSpecialUseANDBrl = cms.bool(True),
    HaloOverwritesMatchedBrl = cms.bool(True),
    CDLConfigWordbRPCCSC = cms.uint32(16),
    IsolationCellSizeEta = cms.int32(2),
    MergeMethodEtaFwd = cms.string('Special'),
    EtaPhiThreshold_COU = cms.double(0.127),
    EtaWeight_barrel = cms.double(0.028),
    MergeMethodMIPBrl = cms.string('Special'),
    EtaPhiThreshold_barrel = cms.double(0.062),
    IsolationCellSizePhi = cms.int32(2),
    MergeMethodChargeBrl = cms.string('takeDT'),
    VersionSortRankEtaQLUT = cms.uint32(2),
    MergeMethodPtBrl = cms.string('byMinPt'),
    CaloTrigger = cms.bool(True),
    MergeMethodPtFwd = cms.string('byMinPt'),
    PropagatePhi = cms.bool(False),
    EtaWeight_endcap = cms.double(0.13),
    MergeMethodEtaBrl = cms.string('Special'),
    CDLConfigWordfRPCDT = cms.uint32(1),
    CDLConfigWordDTCSC = cms.uint32(2),
    MergeMethodChargeFwd = cms.string('takeCSC'),
    DoOvlRpcAnd = cms.bool(False),
    EtaWeight_COU = cms.double(0.316),
    MergeMethodISOSpecialUseANDFwd = cms.bool(True),
    MergeMethodMIPFwd = cms.string('Special'),
    MergeMethodPhiBrl = cms.string('takeDT'),
    EtaPhiThreshold_endcap = cms.double(0.062),
    CDLConfigWordCSCDT = cms.uint32(3),
    MergeMethodMIPSpecialUseANDFwd = cms.bool(False),
    MergeMethodPhiFwd = cms.string('takeCSC'),
    MergeMethodISOFwd = cms.string('Special'),
    PhiWeight_COU = cms.double(1.0),
    MergeMethodISOBrl = cms.string('Special'),
    PhiWeight_endcap = cms.double(1.0),
    SortRankOffsetBrl = cms.uint32(10),
    MergeMethodSRKBrl = cms.string('takeDT'),
    MergeMethodMIPSpecialUseANDBrl = cms.bool(False),
    SortRankOffsetFwd = cms.uint32(10)
)


process.EcalPreshowerGeometryEP = cms.ESProducer("EcalPreshowerGeometryEP",
    applyAlignment = cms.untracked.bool(False)
)


process.KFTrajectorySmoother = cms.ESProducer("KFTrajectorySmootherESProducer",
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3),
    ComponentName = cms.string('KFSmoother'),
    Estimator = cms.string('Chi2'),
    Updator = cms.string('KFUpdator'),
    Propagator = cms.string('PropagatorWithMaterial')
)


process.AnalyticalPropagator = cms.ESProducer("AnalyticalPropagatorESProducer",
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('AnalyticalPropagator'),
    PropagationDirection = cms.string('alongMomentum')
)


process.TrajectoryBuilderForConversions = cms.ESProducer("CkfTrajectoryBuilderESProducer",
    propagatorAlong = cms.string('alongMomElePropagator'),
    trajectoryFilterName = cms.string('TrajectoryFilterForConversions'),
    maxCand = cms.int32(5),
    ComponentName = cms.string('TrajectoryBuilderForConversions'),
    propagatorOpposite = cms.string('oppositeToMomElePropagator'),
    MeasurementTrackerName = cms.string(''),
    estimator = cms.string('eleLooseChi2'),
    TTRHBuilder = cms.string('WithTrackAngle'),
    updator = cms.string('KFUpdator'),
    alwaysUseInvalidHits = cms.bool(True),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0)
)


process.idealForDigiTrackerGeometry = cms.ESProducer("TrackerDigiGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    fromDDD = cms.bool(True),
    applyAlignment = cms.bool(False),
    alignmentsLabel = cms.string('fakeForIdeal')
)


process.L1DTConfig = cms.ESProducer("DTConfigTrivialProducer",
    DTTPGMap = cms.untracked.PSet(
        wh0st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se4 = cms.untracked.vint32(72, 48, 72, 18),
        whm2st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se3 = cms.untracked.vint32(72, 48, 72, 18),
        whm1st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        whm2st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        whm2st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        whm1st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm1st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh1st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm1st1se3 = cms.untracked.vint32(50, 48, 50, 13),
        whm1st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se4 = cms.untracked.vint32(60, 48, 60, 15),
        wh1st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        wh2st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        whm2st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        wh0st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh0st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh2st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        wh2st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh2st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm1st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se3 = cms.untracked.vint32(60, 48, 60, 15),
        whm1st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh0st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh0st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm1st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh1st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh1st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st1se4 = cms.untracked.vint32(50, 48, 50, 13),
        wh1st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh1st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se8 = cms.untracked.vint32(72, 58, 72, 18)
    ),
    DTTPGParameters = cms.PSet(
        SectCollParameters = cms.PSet(
            SCCSP5 = cms.int32(0),
            SCCSP2 = cms.int32(0),
            SCCSP3 = cms.int32(0),
            SCECF4 = cms.bool(False),
            SCCSP1 = cms.int32(0),
            SCECF2 = cms.bool(False),
            SCECF3 = cms.bool(False),
            SCCSP4 = cms.int32(0),
            SCECF1 = cms.bool(False),
            Debug = cms.untracked.bool(False)
        ),
        Debug = cms.untracked.bool(False),
        TUParameters = cms.PSet(
            TracoParameters = cms.PSet(
                SPRGCOMP = cms.int32(2),
                FHTMSK = cms.int32(0),
                DD = cms.int32(18),
                SSLMSK = cms.int32(0),
                LVALIDIFH = cms.int32(0),
                Debug = cms.untracked.int32(0),
                FSLMSK = cms.int32(0),
                SHTPRF = cms.int32(1),
                SHTMSK = cms.int32(0),
                TRGENB3 = cms.int32(1),
                SHISM = cms.int32(0),
                IBTIOFF = cms.int32(0),
                KPRGCOM = cms.int32(255),
                KRAD = cms.int32(0),
                FLTMSK = cms.int32(0),
                LTS = cms.int32(0),
                SLTMSK = cms.int32(0),
                FPRGCOMP = cms.int32(2),
                TRGENB9 = cms.int32(1),
                TRGENB8 = cms.int32(1),
                FHTPRF = cms.int32(1),
                LTF = cms.int32(0),
                TRGENB1 = cms.int32(1),
                TRGENB0 = cms.int32(1),
                FHISM = cms.int32(0),
                TRGENB2 = cms.int32(1),
                TRGENB5 = cms.int32(1),
                TRGENB4 = cms.int32(1),
                TRGENB7 = cms.int32(1),
                TRGENB6 = cms.int32(1),
                TRGENB15 = cms.int32(1),
                TRGENB14 = cms.int32(1),
                TRGENB11 = cms.int32(1),
                TRGENB10 = cms.int32(1),
                TRGENB13 = cms.int32(1),
                TRGENB12 = cms.int32(1),
                REUSEO = cms.int32(1),
                REUSEI = cms.int32(1),
                BTIC = cms.int32(32)
            ),
            TSPhiParameters = cms.PSet(
                TSMNOE1 = cms.bool(True),
                TSMNOE2 = cms.bool(False),
                TSSMSK1 = cms.int32(312),
                TSTREN9 = cms.bool(True),
                TSTREN8 = cms.bool(True),
                TSTREN11 = cms.bool(True),
                TSTREN3 = cms.bool(True),
                TSTREN2 = cms.bool(True),
                TSTREN1 = cms.bool(True),
                TSTREN0 = cms.bool(True),
                TSTREN7 = cms.bool(True),
                TSTREN6 = cms.bool(True),
                TSTREN5 = cms.bool(True),
                TSTREN4 = cms.bool(True),
                TSSCCE1 = cms.bool(True),
                TSSCCE2 = cms.bool(False),
                TSMCCE2 = cms.bool(False),
                TSTREN19 = cms.bool(True),
                TSMCCE1 = cms.bool(True),
                TSTREN17 = cms.bool(True),
                TSTREN16 = cms.bool(True),
                TSTREN15 = cms.bool(True),
                TSTREN14 = cms.bool(True),
                TSTREN13 = cms.bool(True),
                TSTREN12 = cms.bool(True),
                TSSMSK2 = cms.int32(312),
                TSTREN10 = cms.bool(True),
                TSMMSK2 = cms.int32(312),
                TSMMSK1 = cms.int32(312),
                TSMHSP = cms.int32(1),
                TSSNOE2 = cms.bool(False),
                TSSNOE1 = cms.bool(True),
                TSSCGS2 = cms.bool(True),
                TSSCCEC = cms.bool(False),
                TSMCCEC = cms.bool(False),
                TSMHTE2 = cms.bool(False),
                Debug = cms.untracked.bool(False),
                TSSHTE2 = cms.bool(False),
                TSMCGS1 = cms.bool(True),
                TSMCGS2 = cms.bool(True),
                TSSHTE1 = cms.bool(True),
                TSTREN22 = cms.bool(True),
                TSSNOEC = cms.bool(False),
                TSTREN20 = cms.bool(True),
                TSTREN21 = cms.bool(True),
                TSMGS1 = cms.int32(1),
                TSMGS2 = cms.int32(1),
                TSSHTEC = cms.bool(False),
                TSMWORD = cms.int32(255),
                TSMHTEC = cms.bool(False),
                TSSCGS1 = cms.bool(True),
                TSTREN23 = cms.bool(True),
                TSSGS2 = cms.int32(1),
                TSMNOEC = cms.bool(False),
                TSSGS1 = cms.int32(1),
                TSTREN18 = cms.bool(True),
                TSMHTE1 = cms.bool(True)
            ),
            TSThetaParameters = cms.PSet(
                Debug = cms.untracked.bool(False)
            ),
            Debug = cms.untracked.bool(False),
            DIGIOFFSET = cms.int32(500),
            SINCROTIME = cms.int32(0),
            BtiParameters = cms.PSet(
                KACCTHETA = cms.int32(1),
                WEN8 = cms.int32(1),
                ACH = cms.int32(1),
                DEAD = cms.int32(31),
                ACL = cms.int32(2),
                PTMS20 = cms.int32(1),
                Debug = cms.untracked.int32(0),
                PTMS22 = cms.int32(1),
                PTMS23 = cms.int32(1),
                PTMS24 = cms.int32(1),
                PTMS25 = cms.int32(1),
                PTMS26 = cms.int32(1),
                PTMS27 = cms.int32(1),
                PTMS28 = cms.int32(1),
                PTMS29 = cms.int32(1),
                SET = cms.int32(7),
                RON = cms.bool(True),
                WEN2 = cms.int32(1),
                LL = cms.int32(2),
                LH = cms.int32(21),
                WEN3 = cms.int32(1),
                RE43 = cms.int32(2),
                WEN0 = cms.int32(1),
                RL = cms.int32(42),
                WEN1 = cms.int32(1),
                RH = cms.int32(61),
                LTS = cms.int32(3),
                CH = cms.int32(41),
                CL = cms.int32(22),
                PTMS15 = cms.int32(1),
                PTMS14 = cms.int32(1),
                PTMS17 = cms.int32(1),
                PTMS16 = cms.int32(1),
                PTMS11 = cms.int32(1),
                PTMS10 = cms.int32(1),
                PTMS13 = cms.int32(1),
                PTMS12 = cms.int32(1),
                XON = cms.bool(False),
                WEN7 = cms.int32(1),
                WEN4 = cms.int32(1),
                WEN5 = cms.int32(1),
                PTMS19 = cms.int32(1),
                PTMS18 = cms.int32(1),
                PTMS31 = cms.int32(0),
                PTMS30 = cms.int32(0),
                PTMS5 = cms.int32(1),
                PTMS4 = cms.int32(1),
                PTMS7 = cms.int32(1),
                PTMS6 = cms.int32(1),
                PTMS1 = cms.int32(0),
                PTMS0 = cms.int32(0),
                PTMS3 = cms.int32(0),
                WEN6 = cms.int32(1),
                PTMS2 = cms.int32(0),
                PTMS9 = cms.int32(1),
                PTMS8 = cms.int32(1),
                ST43 = cms.int32(42),
                AC2 = cms.int32(3),
                AC1 = cms.int32(0),
                KMAX = cms.int32(64),
                PTMS21 = cms.int32(1)
            )
        )
    )
)


process.L1MuCSCPtLutRcdSrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuCSCPtLutRcd'),
    firstValid = cms.vuint32(1)
)


process.jetrcdsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1JetEtScaleRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtBoardMapsRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtBoardMapsRcd'),
    firstValid = cms.vuint32(1)
)


process.dttfpar = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTTFParametersRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtTriggerMenuRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtTriggerMenuRcd'),
    firstValid = cms.vuint32(1)
)


process.SiStripPedestalsFakeESSource = cms.ESSource("SiStripPedestalsFakeESSource",
    HighThValue = cms.double(5.0),
    printDebug = cms.untracked.bool(False),
    PedestalsValue = cms.uint32(30),
    file = cms.FileInPath('CalibTracker/SiStripCommon/data/SiStripDetInfo.dat'),
    LowThValue = cms.double(2.0)
)


process.l1GctParamsRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GctJetFinderParamsRcd'),
    firstValid = cms.vuint32(1)
)


process.l1CaloEcalScaleRecord = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1CaloEcalScaleRcd'),
    firstValid = cms.vuint32(1)
)


process.l1CaloGeomRecordSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1CaloGeometryRecord'),
    firstValid = cms.vuint32(1)
)


process.philut = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTPhiLutRcd'),
    firstValid = cms.vuint32(1)
)


process.rpcconesrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RPCConeBuilderRcd'),
    firstValid = cms.vuint32(1)
)


process.l1GctJcPosParsRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GctJetCounterPositiveEtaRcd'),
    firstValid = cms.vuint32(1)
)


process.XMLIdealGeometryESSource = cms.ESSource("XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring('Geometry/CMSCommonData/data/materials.xml', 
        'Geometry/CMSCommonData/data/rotations.xml', 
        'Geometry/CMSCommonData/data/normal/cmsextent.xml', 
        'Geometry/CMSCommonData/data/cms.xml', 
        'Geometry/CMSCommonData/data/cmsMother.xml', 
        'Geometry/CMSCommonData/data/cmsTracker.xml', 
        'Geometry/CMSCommonData/data/caloBase.xml', 
        'Geometry/CMSCommonData/data/cmsCalo.xml', 
        'Geometry/CMSCommonData/data/muonBase.xml', 
        'Geometry/CMSCommonData/data/cmsMuon.xml', 
        'Geometry/CMSCommonData/data/mgnt.xml', 
        'Geometry/CMSCommonData/data/beampipe.xml', 
        'Geometry/CMSCommonData/data/cmsBeam.xml', 
        'Geometry/CMSCommonData/data/muonMB.xml', 
        'Geometry/CMSCommonData/data/muonMagnet.xml', 
        'Geometry/TrackerCommonData/data/pixfwdMaterials.xml', 
        'Geometry/TrackerCommonData/data/pixfwdCommon.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq1x2.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq1x5.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x3.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x4.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x5.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPanelBase.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPanel.xml', 
        'Geometry/TrackerCommonData/data/pixfwdBlade.xml', 
        'Geometry/TrackerCommonData/data/pixfwdNipple.xml', 
        'Geometry/TrackerCommonData/data/pixfwdDisk.xml', 
        'Geometry/TrackerCommonData/data/pixfwdCylinder.xml', 
        'Geometry/TrackerCommonData/data/pixfwd.xml', 
        'Geometry/TrackerCommonData/data/pixbarmaterial.xml', 
        'Geometry/TrackerCommonData/data/pixbarladder.xml', 
        'Geometry/TrackerCommonData/data/pixbarladderfull.xml', 
        'Geometry/TrackerCommonData/data/pixbarladderhalf.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer0.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer1.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer2.xml', 
        'Geometry/TrackerCommonData/data/pixbar.xml', 
        'Geometry/TrackerCommonData/data/tibtidcommonmaterial.xml', 
        'Geometry/TrackerCommonData/data/tibmaterial.xml', 
        'Geometry/TrackerCommonData/data/tibmodpar.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0a.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0b.xml', 
        'Geometry/TrackerCommonData/data/tibmodule2.xml', 
        'Geometry/TrackerCommonData/data/tibstringpar.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring0lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring0.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring1lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring1.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring2lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring2.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring3lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring3.xml', 
        'Geometry/TrackerCommonData/data/tiblayerpar.xml', 
        'Geometry/TrackerCommonData/data/tiblayer0.xml', 
        'Geometry/TrackerCommonData/data/tiblayer1.xml', 
        'Geometry/TrackerCommonData/data/tiblayer2.xml', 
        'Geometry/TrackerCommonData/data/tiblayer3.xml', 
        'Geometry/TrackerCommonData/data/tib.xml', 
        'Geometry/TrackerCommonData/data/tidmaterial.xml', 
        'Geometry/TrackerCommonData/data/tidmodpar.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0r.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0l.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1r.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1l.xml', 
        'Geometry/TrackerCommonData/data/tidmodule2.xml', 
        'Geometry/TrackerCommonData/data/tidringpar.xml', 
        'Geometry/TrackerCommonData/data/tidring0.xml', 
        'Geometry/TrackerCommonData/data/tidring0f.xml', 
        'Geometry/TrackerCommonData/data/tidring0b.xml', 
        'Geometry/TrackerCommonData/data/tidring1.xml', 
        'Geometry/TrackerCommonData/data/tidring1f.xml', 
        'Geometry/TrackerCommonData/data/tidring1b.xml', 
        'Geometry/TrackerCommonData/data/tidring2.xml', 
        'Geometry/TrackerCommonData/data/tid.xml', 
        'Geometry/TrackerCommonData/data/tidf.xml', 
        'Geometry/TrackerCommonData/data/tidb.xml', 
        'Geometry/TrackerCommonData/data/tibtidservices.xml', 
        'Geometry/TrackerCommonData/data/tibtidservicesf.xml', 
        'Geometry/TrackerCommonData/data/tibtidservicesb.xml', 
        'Geometry/TrackerCommonData/data/tobmaterial.xml', 
        'Geometry/TrackerCommonData/data/tobmodpar.xml', 
        'Geometry/TrackerCommonData/data/tobmodule0.xml', 
        'Geometry/TrackerCommonData/data/tobmodule2.xml', 
        'Geometry/TrackerCommonData/data/tobmodule4.xml', 
        'Geometry/TrackerCommonData/data/tobrodpar.xml', 
        'Geometry/TrackerCommonData/data/tobrod0c.xml', 
        'Geometry/TrackerCommonData/data/tobrod0l.xml', 
        'Geometry/TrackerCommonData/data/tobrod0h.xml', 
        'Geometry/TrackerCommonData/data/tobrod0.xml', 
        'Geometry/TrackerCommonData/data/tobrod1l.xml', 
        'Geometry/TrackerCommonData/data/tobrod1h.xml', 
        'Geometry/TrackerCommonData/data/tobrod1.xml', 
        'Geometry/TrackerCommonData/data/tobrod2c.xml', 
        'Geometry/TrackerCommonData/data/tobrod2l.xml', 
        'Geometry/TrackerCommonData/data/tobrod2h.xml', 
        'Geometry/TrackerCommonData/data/tobrod2.xml', 
        'Geometry/TrackerCommonData/data/tobrod3l.xml', 
        'Geometry/TrackerCommonData/data/tobrod3h.xml', 
        'Geometry/TrackerCommonData/data/tobrod3.xml', 
        'Geometry/TrackerCommonData/data/tobrod4c.xml', 
        'Geometry/TrackerCommonData/data/tobrod4l.xml', 
        'Geometry/TrackerCommonData/data/tobrod4h.xml', 
        'Geometry/TrackerCommonData/data/tobrod4.xml', 
        'Geometry/TrackerCommonData/data/tobrod5l.xml', 
        'Geometry/TrackerCommonData/data/tobrod5h.xml', 
        'Geometry/TrackerCommonData/data/tobrod5.xml', 
        'Geometry/TrackerCommonData/data/tob.xml', 
        'Geometry/TrackerCommonData/data/tecmaterial.xml', 
        'Geometry/TrackerCommonData/data/tecmodpar.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule2.xml', 
        'Geometry/TrackerCommonData/data/tecmodule3.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule5.xml', 
        'Geometry/TrackerCommonData/data/tecmodule6.xml', 
        'Geometry/TrackerCommonData/data/tecpetpar.xml', 
        'Geometry/TrackerCommonData/data/tecring0.xml', 
        'Geometry/TrackerCommonData/data/tecring1.xml', 
        'Geometry/TrackerCommonData/data/tecring2.xml', 
        'Geometry/TrackerCommonData/data/tecring3.xml', 
        'Geometry/TrackerCommonData/data/tecring4.xml', 
        'Geometry/TrackerCommonData/data/tecring5.xml', 
        'Geometry/TrackerCommonData/data/tecring6.xml', 
        'Geometry/TrackerCommonData/data/tecring0f.xml', 
        'Geometry/TrackerCommonData/data/tecring1f.xml', 
        'Geometry/TrackerCommonData/data/tecring2f.xml', 
        'Geometry/TrackerCommonData/data/tecring3f.xml', 
        'Geometry/TrackerCommonData/data/tecring4f.xml', 
        'Geometry/TrackerCommonData/data/tecring5f.xml', 
        'Geometry/TrackerCommonData/data/tecring6f.xml', 
        'Geometry/TrackerCommonData/data/tecring0b.xml', 
        'Geometry/TrackerCommonData/data/tecring1b.xml', 
        'Geometry/TrackerCommonData/data/tecring2b.xml', 
        'Geometry/TrackerCommonData/data/tecring3b.xml', 
        'Geometry/TrackerCommonData/data/tecring4b.xml', 
        'Geometry/TrackerCommonData/data/tecring5b.xml', 
        'Geometry/TrackerCommonData/data/tecring6b.xml', 
        'Geometry/TrackerCommonData/data/tecpetalf.xml', 
        'Geometry/TrackerCommonData/data/tecpetalb.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal6f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal6b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal8f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal8b.xml', 
        'Geometry/TrackerCommonData/data/tecwheel.xml', 
        'Geometry/TrackerCommonData/data/tecwheela.xml', 
        'Geometry/TrackerCommonData/data/tecwheelb.xml', 
        'Geometry/TrackerCommonData/data/tecwheelc.xml', 
        'Geometry/TrackerCommonData/data/tecwheeld.xml', 
        'Geometry/TrackerCommonData/data/tecwheel6.xml', 
        'Geometry/TrackerCommonData/data/tecservices.xml', 
        'Geometry/TrackerCommonData/data/tecbackplate.xml', 
        'Geometry/TrackerCommonData/data/tec.xml', 
        'Geometry/TrackerCommonData/data/trackermaterial.xml', 
        'Geometry/TrackerCommonData/data/tracker.xml', 
        'Geometry/TrackerCommonData/data/trackerpixbar.xml', 
        'Geometry/TrackerCommonData/data/trackerpixfwd.xml', 
        'Geometry/TrackerCommonData/data/trackertibtidservices.xml', 
        'Geometry/TrackerCommonData/data/trackertib.xml', 
        'Geometry/TrackerCommonData/data/trackertid.xml', 
        'Geometry/TrackerCommonData/data/trackertob.xml', 
        'Geometry/TrackerCommonData/data/trackertec.xml', 
        'Geometry/TrackerCommonData/data/trackerbulkhead.xml', 
        'Geometry/TrackerCommonData/data/trackerother.xml', 
        'Geometry/EcalCommonData/data/eregalgo.xml', 
        'Geometry/EcalCommonData/data/ebalgo.xml', 
        'Geometry/EcalCommonData/data/ebcon.xml', 
        'Geometry/EcalCommonData/data/ebrot.xml', 
        'Geometry/EcalCommonData/data/eecon.xml', 
        'Geometry/EcalCommonData/data/eefixed.xml', 
        'Geometry/EcalCommonData/data/eehier.xml', 
        'Geometry/EcalCommonData/data/eealgo.xml', 
        'Geometry/EcalCommonData/data/escon.xml', 
        'Geometry/EcalCommonData/data/esalgo.xml', 
        'Geometry/EcalCommonData/data/eeF.xml', 
        'Geometry/EcalCommonData/data/eeB.xml', 
        'Geometry/HcalCommonData/data/hcalrotations.xml', 
        'Geometry/HcalCommonData/data/hcalalgo.xml', 
        'Geometry/HcalCommonData/data/hcalbarrelalgo.xml', 
        'Geometry/HcalCommonData/data/hcalendcapalgo.xml', 
        'Geometry/HcalCommonData/data/hcalouteralgo.xml', 
        'Geometry/HcalCommonData/data/hcalforwardalgo.xml', 
        'Geometry/HcalCommonData/data/hcalforwardfibre.xml', 
        'Geometry/HcalCommonData/data/hcalforwardmaterial.xml', 
        'Geometry/MuonCommonData/data/mbCommon.xml', 
        'Geometry/MuonCommonData/data/mb1.xml', 
        'Geometry/MuonCommonData/data/mb2.xml', 
        'Geometry/MuonCommonData/data/mb3.xml', 
        'Geometry/MuonCommonData/data/mb4.xml', 
        'Geometry/MuonCommonData/data/muonYoke.xml', 
        'Geometry/MuonCommonData/data/mf.xml', 
        'Geometry/ForwardCommonData/data/forward.xml', 
        'Geometry/ForwardCommonData/data/forwardshield.xml', 
        'Geometry/ForwardCommonData/data/brmrotations.xml', 
        'Geometry/ForwardCommonData/data/brm.xml', 
        'Geometry/ForwardCommonData/data/totemMaterials.xml', 
        'Geometry/ForwardCommonData/data/totemRotations.xml', 
        'Geometry/ForwardCommonData/data/totemt1.xml', 
        'Geometry/ForwardCommonData/data/totemt2.xml', 
        'Geometry/ForwardCommonData/data/ionpump.xml', 
        'Geometry/MuonCommonData/data/muonNumbering.xml', 
        'Geometry/TrackerCommonData/data/trackerStructureTopology.xml', 
        'Geometry/TrackerSimData/data/trackersens.xml', 
        'Geometry/TrackerRecoData/data/trackerRecoMaterial.xml', 
        'Geometry/EcalSimData/data/ecalsens.xml', 
        'Geometry/HcalCommonData/data/hcalsens.xml', 
        'Geometry/HcalSimData/data/CaloUtil.xml', 
        'Geometry/MuonSimData/data/muonSens.xml', 
        'Geometry/DTGeometryBuilder/data/dtSpecsFilter.xml', 
        'Geometry/CSCGeometryBuilder/data/cscSpecsFilter.xml', 
        'Geometry/CSCGeometryBuilder/data/cscSpecs.xml', 
        'Geometry/RPCGeometryBuilder/data/RPCSpecs.xml', 
        'Geometry/ForwardCommonData/data/brmsens.xml', 
        'Geometry/HcalSimData/data/HcalProdCuts.xml', 
        'Geometry/EcalSimData/data/EcalProdCuts.xml', 
        'Geometry/TrackerSimData/data/trackerProdCuts.xml', 
        'Geometry/TrackerSimData/data/trackerProdCutsBEAM.xml', 
        'Geometry/MuonSimData/data/muonProdCuts.xml', 
        'Geometry/CMSCommonData/data/FieldParameters.xml'),
    rootNodeName = cms.string('cms:OCMS')
)


process.eegeom = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('EcalMappingRcd'),
    firstValid = cms.vuint32(1)
)


process.emrcdsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1EmEtScaleRcd'),
    firstValid = cms.vuint32(1)
)


process.l1GctJcNegParsRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GctJetCounterNegativeEtaRcd'),
    firstValid = cms.vuint32(1)
)


process.l1GctChanMaskRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GctChannelMaskRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtStableParametersRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtStableParametersRcd'),
    firstValid = cms.vuint32(1)
)


process.qualut = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTQualPatternLutRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtTriggerMaskVetoAlgoTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtTriggerMaskVetoAlgoTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.L1MuTriggerPtScaleRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuTriggerPtScaleRcd'),
    firstValid = cms.vuint32(1)
)


process.rcdsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('DTConfigManagerRcd'),
    firstValid = cms.vuint32(1)
)


process.es_hardcode = cms.ESSource("HcalHardcodeCalibrations",
    toGet = cms.untracked.vstring('GainWidths', 
        'channelQuality', 
        'ZSThresholds')
)


process.L1MuGMTParametersRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuGMTParametersRcd'),
    firstValid = cms.vuint32(1)
)


process.L1MuTriggerScalesRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuTriggerScalesRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtTriggerMaskVetoTechTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtTriggerMaskVetoTechTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.siStripBadModuleFakeESSource = cms.ESSource("SiStripBadModuleFakeESSource",
    appendToDataLabel = cms.string('')
)


process.L1GtTriggerMaskAlgoTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtTriggerMaskAlgoTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtParametersRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtParametersRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtTriggerMaskTechTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtTriggerMaskTechTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.l1RctMaskRcds = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RCTChannelMaskRcd'),
    firstValid = cms.vuint32(1)
)


process.l1CaloHcalScaleRecord = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1CaloHcalScaleRcd'),
    firstValid = cms.vuint32(1)
)


process.ptalut = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTPtaLutRcd'),
    firstValid = cms.vuint32(1)
)


process.DTFakeVDriftESProducer = cms.ESSource("DTFakeVDriftESProducer",
    reso = cms.double(0.05),
    vDrift = cms.double(0.00543)
)


process.siStripGainFakeESSource = cms.ESSource("SiStripGainFakeESSource",
    appendToDataLabel = cms.string('fakeAPVGain'),
    file = cms.FileInPath('CalibTracker/SiStripCommon/data/SiStripDetInfo.dat')
)


process.L1MuCSCAlignmentRcdSrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuCSCTFAlignmentRcd'),
    firstValid = cms.vuint32(1)
)


process.siStripLAFakeESSourceforSimulation = cms.ESSource("SiStripLAFakeESSource",
    appendToDataLabel = cms.string('fake'),
    TemperatureError = cms.double(10.0),
    Temperature = cms.double(297.0),
    HoleRHAllParameter = cms.double(0.7),
    ChargeMobility = cms.double(480.0),
    HoleBeta = cms.double(1.213),
    HoleSaturationVelocity = cms.double(8370000.0),
    file = cms.FileInPath('CalibTracker/SiStripCommon/data/SiStripDetInfo.dat'),
    AppliedVoltage = cms.double(150.0)
)


process.L1GtPrescaleFactorsTechTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtPrescaleFactorsTechTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.l1GctConfigRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GctHfLutSetupRcd'),
    firstValid = cms.vuint32(1)
)


process.rpcconfsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RPCConfigRcd'),
    firstValid = cms.vuint32(1)
)


process.siStripBadFiberFakeESSource = cms.ESSource("SiStripBadFiberFakeESSource",
    appendToDataLabel = cms.string('')
)


process.GlobalTag = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string('.'),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        connectionRetrialPeriod = cms.untracked.int32(10)
    ),
    BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    connect = cms.string('frontier://FrontierProd/CMS_COND_21X_GLOBALTAG'),
    globaltag = cms.string('CRAFT_V3P::All')
)


process.L1TriggerKeyRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1TriggerKeyRcd'),
    firstValid = cms.vuint32(1)
)


process.L1MuCSCTFConfigurationRcdSrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuCSCTFConfigurationRcd'),
    firstValid = cms.vuint32(1)
)


process.L1TriggerKeyListRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1TriggerKeyListRcd'),
    firstValid = cms.vuint32(1)
)


process.etalut = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTEtaPatternLutRcd'),
    firstValid = cms.vuint32(1)
)


process.L1MuGMTScalesRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuGMTScalesRcd'),
    firstValid = cms.vuint32(1)
)


process.siStripBadChannelFakeESSource = cms.ESSource("SiStripBadChannelFakeESSource",
    appendToDataLabel = cms.string('')
)


process.rpchwconfsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RPCHwConfigRcd'),
    firstValid = cms.vuint32(1)
)


process.l1csctpconfsrc = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('CSCL1TPParametersRcd'),
    firstValid = cms.vuint32(0)
)


process.l1RctParamsRecords = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RCTParametersRcd'),
    firstValid = cms.vuint32(1)
)


process.extlut = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1MuDTExtLutRcd'),
    firstValid = cms.vuint32(1)
)


process.L1GtPrescaleFactorsAlgoTrigRcdSource = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1GtPrescaleFactorsAlgoTrigRcd'),
    firstValid = cms.vuint32(1)
)


process.prefer("GlobalTag")

process.MuonTrackLoaderForGLB = cms.PSet(
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorOpposite'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(True),
        VertexConstraint = cms.bool(False)
    )
)

process.TC_ME1234 = cms.PSet(
    dPhiFineMax = cms.double(0.02),
    verboseInfo = cms.untracked.bool(True),
    SegmentSorting = cms.int32(1),
    chi2Max = cms.double(6000.0),
    dPhiMax = cms.double(0.003),
    chi2ndfProbMin = cms.double(0.0001),
    minLayersApart = cms.int32(2),
    dRPhiFineMax = cms.double(6.0),
    dRPhiMax = cms.double(1.2)
)

process.ptSeedParameterization = cms.PSet(
    SMB_21 = cms.vdouble(0.918425, -0.141199, 0.0, 0.254515, -0.111848, 
        0.0),
    SMB_20 = cms.vdouble(0.861314, -0.16233, 0.0, 0.248879, -0.113879, 
        0.0),
    SMB_22 = cms.vdouble(1.308565, -0.701634, 0.0, -0.302861, 0.675785, 
        0.0),
    OL_2213 = cms.vdouble(0.563218, -0.493991, 0.0, 0.943776, -0.591751, 
        0.0),
    SME_11 = cms.vdouble(2.39479, -0.888663, 0.0, -4.604546, 3.623464, 
        0.0),
    SME_13 = cms.vdouble(0.398851, 0.028176, 0.0, 0.567015, 2.623232, 
        0.0),
    SMB_31 = cms.vdouble(0.398661, -0.024853, 0.0, 0.863324, -0.413048, 
        0.0),
    SME_32 = cms.vdouble(-0.021912, -0.008995, 0.0, -49.779764, 30.780972, 
        0.0),
    SME_31 = cms.vdouble(-0.588188, 0.316961, 0.0, -95.261732, 45.444051, 
        0.0),
    OL_1213 = cms.vdouble(0.960544, -0.75644, 0.0, 0.1636, 0.114178, 
        0.0),
    DT_13 = cms.vdouble(0.298842, 0.076531, -0.14293, 0.219923, -0.145026, 
        0.155638),
    DT_12 = cms.vdouble(0.176182, 0.058535, -0.090549, 0.202363, -0.203126, 
        0.222219),
    DT_14 = cms.vdouble(0.388423, 0.068698, -0.145925, 0.159515, 0.124299, 
        -0.133269),
    OL_1232 = cms.vdouble(0.162626, 0.000843, 0.0, 0.396271, 0.002791, 
        0.0),
    CSC_23 = cms.vdouble(-0.095236, 0.122061, -0.029852, -11.396689, 15.933598, 
        -4.267065),
    CSC_24 = cms.vdouble(-0.049769, 0.063087, -0.011029, -13.765978, 16.296143, 
        -4.241835),
    CSC_03 = cms.vdouble(0.498992, -0.086235, -0.025772, 2.761006, -2.667607, 
        0.72802),
    CSC_01 = cms.vdouble(0.155906, -0.000406, 0.0, 0.194022, -0.010181, 
        0.0),
    SMB_32 = cms.vdouble(0.421649, -0.111654, 0.0, -0.044613, 1.134858, 
        0.0),
    SMB_30 = cms.vdouble(0.399628, 0.014922, 0.0, 0.665622, 0.358439, 
        0.0),
    OL_2222 = cms.vdouble(0.087587, 0.005729, 0.0, 0.535169, -0.087675, 
        0.0),
    SMB_10 = cms.vdouble(1.160532, 0.148991, 0.0, 0.182785, -0.093776, 
        0.0),
    SMB_11 = cms.vdouble(1.289468, -0.139653, 0.0, 0.137191, 0.01217, 
        0.0),
    SMB_12 = cms.vdouble(1.923091, -0.913204, 0.0, 0.161556, 0.020215, 
        0.0),
    DT_23 = cms.vdouble(0.120647, 0.034743, -0.070855, 0.302427, -0.21417, 
        0.261012),
    DT_24 = cms.vdouble(0.189527, 0.037328, -0.088523, 0.251936, 0.032411, 
        0.010984),
    SME_21 = cms.vdouble(0.64895, -0.148762, 0.0, -5.07676, 6.284227, 
        0.0),
    SME_22 = cms.vdouble(-0.624708, 0.641043, 0.0, 32.581295, -19.604264, 
        0.0),
    CSC_34 = cms.vdouble(0.144321, -0.142283, 0.035636, 190.260708, -180.888643, 
        43.430395),
    CSC_02 = cms.vdouble(0.600235, -0.205683, 0.001113, 0.655625, -0.682129, 
        0.253916),
    SME_41 = cms.vdouble(-0.187116, 0.076415, 0.0, -58.552583, 27.933864, 
        0.0),
    SME_12 = cms.vdouble(-0.277294, 0.7616, 0.0, -0.243326, 1.446792, 
        0.0),
    DT_34 = cms.vdouble(0.049146, -0.003494, -0.010099, 0.672095, 0.36459, 
        -0.304346),
    CSC_14 = cms.vdouble(0.952517, -0.532733, 0.084601, 1.615881, -1.630744, 
        0.514139),
    OL_1222 = cms.vdouble(0.215915, 0.002556, 0.0, 0.313596, -0.021465, 
        0.0),
    CSC_13 = cms.vdouble(1.22495, -1.792358, 0.711378, 5.271848, -6.280625, 
        2.0142),
    CSC_12 = cms.vdouble(-0.363549, 0.569552, -0.173186, 7.777069, -10.203618, 
        3.478874)
)

process.IconeJetParameters = cms.PSet(
    seedThreshold = cms.double(1.0),
    debugLevel = cms.untracked.int32(0)
)

process.TSPhiParametersBlock = cms.PSet(
    TSPhiParameters = cms.PSet(
        TSMNOE1 = cms.bool(True),
        TSMNOE2 = cms.bool(False),
        TSSMSK1 = cms.int32(312),
        TSTREN9 = cms.bool(True),
        TSTREN8 = cms.bool(True),
        TSTREN11 = cms.bool(True),
        TSTREN3 = cms.bool(True),
        TSTREN2 = cms.bool(True),
        TSTREN1 = cms.bool(True),
        TSTREN0 = cms.bool(True),
        TSTREN7 = cms.bool(True),
        TSTREN6 = cms.bool(True),
        TSTREN5 = cms.bool(True),
        TSTREN4 = cms.bool(True),
        TSSCCE1 = cms.bool(True),
        TSSCCE2 = cms.bool(False),
        TSMCCE2 = cms.bool(False),
        TSTREN19 = cms.bool(True),
        TSMCCE1 = cms.bool(True),
        TSTREN17 = cms.bool(True),
        TSTREN16 = cms.bool(True),
        TSTREN15 = cms.bool(True),
        TSTREN14 = cms.bool(True),
        TSTREN13 = cms.bool(True),
        TSTREN12 = cms.bool(True),
        TSSMSK2 = cms.int32(312),
        TSTREN10 = cms.bool(True),
        TSMMSK2 = cms.int32(312),
        TSMMSK1 = cms.int32(312),
        TSMHSP = cms.int32(1),
        TSSNOE2 = cms.bool(False),
        TSSNOE1 = cms.bool(True),
        TSSCGS2 = cms.bool(True),
        TSSCCEC = cms.bool(False),
        TSMCCEC = cms.bool(False),
        TSMHTE2 = cms.bool(False),
        Debug = cms.untracked.bool(False),
        TSSHTE2 = cms.bool(False),
        TSMCGS1 = cms.bool(True),
        TSMCGS2 = cms.bool(True),
        TSSHTE1 = cms.bool(True),
        TSTREN22 = cms.bool(True),
        TSSNOEC = cms.bool(False),
        TSTREN20 = cms.bool(True),
        TSTREN21 = cms.bool(True),
        TSMGS1 = cms.int32(1),
        TSMGS2 = cms.int32(1),
        TSSHTEC = cms.bool(False),
        TSMWORD = cms.int32(255),
        TSMHTEC = cms.bool(False),
        TSSCGS1 = cms.bool(True),
        TSTREN23 = cms.bool(True),
        TSSGS2 = cms.int32(1),
        TSMNOEC = cms.bool(False),
        TSSGS1 = cms.int32(1),
        TSTREN18 = cms.bool(True),
        TSMHTE1 = cms.bool(True)
    )
)

process.TECi = cms.PSet(
    minRing = cms.int32(1),
    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
    useRingSlector = cms.untracked.bool(True),
    TTRHBuilder = cms.string('WithTrackAngle'),
    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
    maxRing = cms.int32(2)
)

process.MIsoDepositParamGlobalViewMultiIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
    MultipleDepositsFlag = cms.bool(True),
    MuonTrackRefType = cms.string('bestTrkSta'),
    InputType = cms.string('MuonCollection')
)

process.MIsoTrackAssociatorDefault = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(1.0),
        dREcal = cms.double(1.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(1.0),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(1.0),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    )
)

process.MuonUpdatorAtVertexAnyDirection = cms.PSet(
    MuonUpdatorAtVertexParameters = cms.PSet(
        MaxChi2 = cms.double(1000000.0),
        BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
        Propagator = cms.string('SteppingHelixPropagatorAny'),
        BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
    )
)

process.TSThetaParametersBlock = cms.PSet(
    TSThetaParameters = cms.PSet(
        Debug = cms.untracked.bool(False)
    )
)

process.MIsoJetExtractorBlock = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(0.5),
        dREcal = cms.double(0.5),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(0.5),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.5),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    ),
    PrintTimeReport = cms.untracked.bool(False),
    ExcludeMuonVeto = cms.bool(True),
    ComponentName = cms.string('JetExtractor'),
    DR_Max = cms.double(1.0),
    PropagatorName = cms.string('SteppingHelixPropagatorAny'),
    JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
    DR_Veto = cms.double(0.1),
    Threshold = cms.double(5.0)
)

process.MIsoTrackAssociatorTowers = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(1.0),
        dREcal = cms.double(1.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(1.0),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(1.0),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    )
)

process.MIdIsoExtractorPSetBlock = cms.PSet(
    CaloExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        DR_Max = cms.double(1.0),
        DepositInstanceLabels = cms.vstring('ecal', 
            'hcal', 
            'ho'),
        Noise_HE = cms.double(0.2),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_HB = cms.double(0.2),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        DepositLabel = cms.untracked.string('Cal'),
        UseRecHitsFlag = cms.bool(False),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(1.0),
            dREcal = cms.double(1.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(1.0),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(1.0),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        Threshold_HO = cms.double(0.5),
        Noise_EE = cms.double(0.1),
        Noise_EB = cms.double(0.025),
        DR_Veto_H = cms.double(0.1),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        Threshold_H = cms.double(0.5),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_HO = cms.double(0.1),
        Threshold_E = cms.double(0.2),
        Noise_HO = cms.double(0.2)
    ),
    TrackExtractorPSet = cms.PSet(
        Diff_z = cms.double(0.2),
        inputTrackCollection = cms.InputTag("generalTracks"),
        BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        Diff_r = cms.double(0.1),
        Chi2Prob_Min = cms.double(-1.0),
        DR_Veto = cms.double(0.01),
        NHits_Min = cms.uint32(0),
        Chi2Ndof_Max = cms.double(1e+64),
        Pt_Min = cms.double(-1.0),
        DepositLabel = cms.untracked.string(''),
        BeamlineOption = cms.string('BeamSpotFromEvent')
    ),
    JetExtractorPSet = cms.PSet(
        PrintTimeReport = cms.untracked.bool(False),
        ExcludeMuonVeto = cms.bool(True),
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(0.5),
            dREcal = cms.double(0.5),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(False),
            dREcalPreselection = cms.double(0.5),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(False),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.5),
            useMuon = cms.bool(False),
            useCalo = cms.bool(True),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(False)
        ),
        ComponentName = cms.string('JetExtractor'),
        TrackAssociatorParameterBlock = cms.PSet(
            TrackAssociatorParameters = cms.PSet(
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
                dRHcal = cms.double(9999.0),
                dREcal = cms.double(9999.0),
                CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
                useEcal = cms.bool(True),
                dREcalPreselection = cms.double(0.05),
                HORecHitCollectionLabel = cms.InputTag("horeco"),
                dRMuon = cms.double(9999.0),
                crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                useHO = cms.bool(True),
                accountForTrajectoryChangeCalo = cms.bool(False),
                DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
                EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                dRHcalPreselection = cms.double(0.2),
                useMuon = cms.bool(True),
                useCalo = cms.bool(False),
                EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                dRMuonPreselection = cms.double(0.2),
                truthMatch = cms.bool(False),
                HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
                useHcal = cms.bool(True)
            )
        ),
        DR_Max = cms.double(1.0),
        PropagatorName = cms.string('SteppingHelixPropagatorAny'),
        JetCollectionLabel = cms.InputTag("sisCone5CaloJets"),
        DR_Veto = cms.double(0.1),
        Threshold = cms.double(5.0)
    )
)

process.MIsoDepositParamGlobalViewIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
    MultipleDepositsFlag = cms.bool(False),
    MuonTrackRefType = cms.string('bestTrkSta'),
    InputType = cms.string('MuonCollection')
)

process.MIsoDepositGlobalMultiIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("globalMuons"),
    MultipleDepositsFlag = cms.bool(True),
    MuonTrackRefType = cms.string('track'),
    InputType = cms.string('TrackCollection')
)

process.TrackAssociatorParameterBlock = cms.PSet(
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(9999.0),
        dREcal = cms.double(9999.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(0.05),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        propagateAllDirections = cms.bool(True),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.2),
        useMuon = cms.bool(True),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    )
)

process.MuonTrackingRegionCommon = cms.PSet(
    MuonTrackingRegionBuilder = cms.PSet(
        EtaR_UpperLimit_Par1 = cms.double(0.25),
        Eta_fixed = cms.double(0.2),
        OnDemand = cms.double(-1.0),
        Rescale_Dz = cms.double(3.0),
        Eta_min = cms.double(0.1),
        Rescale_phi = cms.double(3.0),
        EtaR_UpperLimit_Par2 = cms.double(0.15),
        DeltaZ_Region = cms.double(15.9),
        Rescale_eta = cms.double(3.0),
        PhiR_UpperLimit_Par2 = cms.double(0.2),
        vertexCollection = cms.InputTag("pixelVertices"),
        Phi_fixed = cms.double(0.2),
        DeltaR = cms.double(0.2),
        EscapePt = cms.double(1.5),
        UseFixedRegion = cms.bool(False),
        PhiR_UpperLimit_Par1 = cms.double(0.6),
        Phi_min = cms.double(0.1),
        UseVertex = cms.bool(False),
        beamSpot = cms.InputTag("offlineBeamSpot")
    )
)

process.GlobalTrajectoryBuilderCommon = cms.PSet(
    MuonTrackingRegionBuilder = cms.PSet(
        EtaR_UpperLimit_Par1 = cms.double(0.25),
        Eta_fixed = cms.double(0.2),
        OnDemand = cms.double(-1.0),
        Rescale_Dz = cms.double(3.0),
        Eta_min = cms.double(0.1),
        Rescale_phi = cms.double(3.0),
        EtaR_UpperLimit_Par2 = cms.double(0.15),
        DeltaZ_Region = cms.double(15.9),
        Rescale_eta = cms.double(3.0),
        PhiR_UpperLimit_Par2 = cms.double(0.2),
        vertexCollection = cms.InputTag("pixelVertices"),
        Phi_fixed = cms.double(0.2),
        DeltaR = cms.double(0.2),
        EscapePt = cms.double(1.5),
        UseFixedRegion = cms.bool(False),
        PhiR_UpperLimit_Par1 = cms.double(0.6),
        Phi_min = cms.double(0.1),
        UseVertex = cms.bool(False),
        beamSpot = cms.InputTag("offlineBeamSpot")
    ),
    Chi2ProbabilityCut = cms.double(30.0),
    Direction = cms.int32(0),
    Chi2CutCSC = cms.double(150.0),
    HitThreshold = cms.int32(1),
    MuonHitsOption = cms.int32(1),
    Chi2CutRPC = cms.double(1.0),
    DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
    TrackRecHitBuilder = cms.string('WithTrackAngle'),
    CSCRecSegmentLabel = cms.InputTag("cscSegments"),
    Chi2CutDT = cms.double(10.0),
    TrackTransformer = cms.PSet(
        Fitter = cms.string('KFFitterForRefitInsideOut'),
        TrackerRecHitBuilder = cms.string('WithTrackAngle'),
        Smoother = cms.string('KFSmootherForRefitInsideOut'),
        MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
        RefitDirection = cms.string('insideOut'),
        RefitRPCHits = cms.bool(True)
    ),
    GlobalMuonTrackMatcher = cms.PSet(
        MinP = cms.double(2.5),
        DeltaDCut = cms.double(10.0),
        DeltaRCut = cms.double(0.2),
        Chi2Cut = cms.double(50.0),
        MinPt = cms.double(1.0)
    ),
    PtCut = cms.double(1.0),
    TrackerPropagator = cms.string('SteppingHelixPropagatorAny'),
    RPCRecSegmentLabel = cms.InputTag("rpcRecHits")
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.DF_ME1A = cms.PSet(
    preClustering = cms.untracked.bool(False),
    maxRatioResidualPrune = cms.double(3.0),
    dPhiFineMax = cms.double(0.025),
    chi2Max = cms.double(5000.0),
    dXclusBoxMax = cms.double(8.0),
    tanThetaMax = cms.double(1.2),
    tanPhiMax = cms.double(0.5),
    minHitsPerSegment = cms.int32(3),
    minHitsForPreClustering = cms.int32(30),
    minLayersApart = cms.int32(2),
    dRPhiFineMax = cms.double(8.0),
    nHitsPerClusterIsShower = cms.int32(20),
    CSCSegmentDebug = cms.untracked.bool(False),
    Pruning = cms.untracked.bool(False),
    dYclusBoxMax = cms.double(8.0)
)

process.MuonTrackLoaderForCosmic = cms.PSet(
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorAny'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTrajectoryIntoEvent = cms.untracked.bool(False),
        AllowNoVertex = cms.untracked.bool(True),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(False)
    )
)

process.MIsoTrackExtractorBlock = cms.PSet(
    Diff_z = cms.double(0.2),
    inputTrackCollection = cms.InputTag("generalTracks"),
    BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
    ComponentName = cms.string('TrackExtractor'),
    DR_Max = cms.double(1.0),
    Diff_r = cms.double(0.1),
    Chi2Prob_Min = cms.double(-1.0),
    DR_Veto = cms.double(0.01),
    NHits_Min = cms.uint32(0),
    Chi2Ndof_Max = cms.double(1e+64),
    Pt_Min = cms.double(-1.0),
    DepositLabel = cms.untracked.string(''),
    BeamlineOption = cms.string('BeamSpotFromEvent')
)

process.MuonTrackLoaderForSTA = cms.PSet(
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorOpposite'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        Smoother = cms.string('KFSmootherForMuonTrackLoader'),
        DoSmoothing = cms.bool(False),
        VertexConstraint = cms.bool(True)
    )
)

process.CSCSegAlgoDF = cms.PSet(
    chamber_types = cms.vstring('ME1/a', 
        'ME1/b', 
        'ME1/2', 
        'ME1/3', 
        'ME2/1', 
        'ME2/2', 
        'ME3/1', 
        'ME3/2', 
        'ME4/1'),
    algo_name = cms.string('CSCSegAlgoDF'),
    parameters_per_chamber_type = cms.vint32(3, 1, 2, 2, 1, 
        2, 1, 2, 1),
    algo_psets = cms.VPSet(cms.PSet(
        tanThetaMax = cms.double(1.2),
        maxRatioResidualPrune = cms.double(3.0),
        dPhiFineMax = cms.double(0.025),
        tanPhiMax = cms.double(0.5),
        dXclusBoxMax = cms.double(8.0),
        preClustering = cms.untracked.bool(False),
        chi2Max = cms.double(5000.0),
        minHitsPerSegment = cms.int32(3),
        minHitsForPreClustering = cms.int32(10),
        minLayersApart = cms.int32(2),
        dRPhiFineMax = cms.double(8.0),
        nHitsPerClusterIsShower = cms.int32(20),
        CSCSegmentDebug = cms.untracked.bool(False),
        Pruning = cms.untracked.bool(False),
        dYclusBoxMax = cms.double(8.0)
    ), 
        cms.PSet(
            tanThetaMax = cms.double(2.0),
            maxRatioResidualPrune = cms.double(3.0),
            dPhiFineMax = cms.double(0.025),
            tanPhiMax = cms.double(0.8),
            dXclusBoxMax = cms.double(8.0),
            preClustering = cms.untracked.bool(False),
            chi2Max = cms.double(5000.0),
            minHitsPerSegment = cms.int32(3),
            minHitsForPreClustering = cms.int32(10),
            minLayersApart = cms.int32(2),
            dRPhiFineMax = cms.double(12.0),
            nHitsPerClusterIsShower = cms.int32(20),
            CSCSegmentDebug = cms.untracked.bool(False),
            Pruning = cms.untracked.bool(False),
            dYclusBoxMax = cms.double(12.0)
        ), 
        cms.PSet(
            tanThetaMax = cms.double(1.2),
            maxRatioResidualPrune = cms.double(3.0),
            dPhiFineMax = cms.double(0.025),
            tanPhiMax = cms.double(0.5),
            dXclusBoxMax = cms.double(8.0),
            preClustering = cms.untracked.bool(False),
            chi2Max = cms.double(5000.0),
            minHitsPerSegment = cms.int32(3),
            minHitsForPreClustering = cms.int32(30),
            minLayersApart = cms.int32(2),
            dRPhiFineMax = cms.double(8.0),
            nHitsPerClusterIsShower = cms.int32(20),
            CSCSegmentDebug = cms.untracked.bool(False),
            Pruning = cms.untracked.bool(False),
            dYclusBoxMax = cms.double(8.0)
        ))
)

process.TC_ME1A = cms.PSet(
    dPhiFineMax = cms.double(0.013),
    verboseInfo = cms.untracked.bool(True),
    SegmentSorting = cms.int32(1),
    chi2Max = cms.double(6000.0),
    dPhiMax = cms.double(0.00198),
    chi2ndfProbMin = cms.double(0.0001),
    minLayersApart = cms.int32(2),
    dRPhiFineMax = cms.double(3.0),
    dRPhiMax = cms.double(0.6)
)

process.KtJetParameters = cms.PSet(
    Strategy = cms.string('Best')
)

process.SK_ME1234 = cms.PSet(
    dPhiFineMax = cms.double(0.025),
    verboseInfo = cms.untracked.bool(True),
    chi2Max = cms.double(99999.0),
    dPhiMax = cms.double(0.003),
    wideSeg = cms.double(3.0),
    minLayersApart = cms.int32(2),
    dRPhiFineMax = cms.double(8.0),
    dRPhiMax = cms.double(8.0)
)

process.MaxConsecLostHitsTrajectoryFilter_block = cms.PSet(
    ComponentType = cms.string('MaxConsecLostHitsTrajectoryFilter'),
    maxConsecLostHits = cms.int32(1)
)

process.MIsoTrackAssociatorJets = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(0.5),
        dREcal = cms.double(0.5),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(0.5),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(0.5),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    )
)

process.MIsoDepositParamGlobalIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
    MultipleDepositsFlag = cms.bool(False),
    MuonTrackRefType = cms.string('track'),
    InputType = cms.string('MuonCollection')
)

process.MuonCaloCompatibilityBlock = cms.PSet(
    MuonCaloCompatibility = cms.PSet(
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_allPt_2_0_norm.root'),
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_allPt_2_0_norm.root')
    )
)

process.MuonUpdatorAtVertex = cms.PSet(
    MuonUpdatorAtVertexParameters = cms.PSet(
        MaxChi2 = cms.double(1000000.0),
        BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
        Propagator = cms.string('SteppingHelixPropagatorOpposite'),
        BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
    )
)

process.GlobalMuonRefitter = cms.PSet(
    Chi2ProbabilityCut = cms.double(30.0),
    Direction = cms.int32(0),
    Chi2CutCSC = cms.double(150.0),
    HitThreshold = cms.int32(1),
    MuonHitsOption = cms.int32(1),
    Chi2CutRPC = cms.double(1.0),
    Fitter = cms.string('KFFitterForRefitInsideOut'),
    DTRecSegmentLabel = cms.InputTag("dt4DSegments"),
    TrackerRecHitBuilder = cms.string('WithTrackAngle'),
    Smoother = cms.string('KFSmootherForRefitInsideOut'),
    MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
    RefitDirection = cms.string('insideOut'),
    CSCRecSegmentLabel = cms.InputTag("cscSegments"),
    RefitRPCHits = cms.bool(True),
    Chi2CutDT = cms.double(10.0),
    PtCut = cms.double(1.0),
    RPCRecSegmentLabel = cms.InputTag("rpcRecHits"),
    Propagator = cms.string('SmartPropagatorAnyRK')
)

process.CaloJetParameters = cms.PSet(
    src = cms.InputTag("towerMaker"),
    verbose = cms.untracked.bool(False),
    jetPtMin = cms.double(0.0),
    inputEtMin = cms.double(0.5),
    jetType = cms.untracked.string('CaloJet'),
    inputEMin = cms.double(0.0)
)

process.MIsoTrackExtractorGsBlock = cms.PSet(
    Diff_z = cms.double(0.2),
    inputTrackCollection = cms.InputTag("ctfGSWithMaterialTracks"),
    BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
    ComponentName = cms.string('TrackExtractor'),
    DR_Max = cms.double(1.0),
    Diff_r = cms.double(0.1),
    Chi2Prob_Min = cms.double(-1.0),
    DR_Veto = cms.double(0.01),
    NHits_Min = cms.uint32(0),
    Chi2Ndof_Max = cms.double(1e+64),
    Pt_Min = cms.double(-1.0),
    DepositLabel = cms.untracked.string(''),
    BeamlineOption = cms.string('BeamSpotFromEvent')
)

process.MIsoCaloExtractorHLTBlock = cms.PSet(
    DR_Veto_H = cms.double(0.1),
    Vertex_Constraint_Z = cms.bool(False),
    Threshold_H = cms.double(0.5),
    ComponentName = cms.string('CaloExtractor'),
    Threshold_E = cms.double(0.2),
    DR_Max = cms.double(1.0),
    DR_Veto_E = cms.double(0.07),
    Weight_E = cms.double(1.5),
    Vertex_Constraint_XY = cms.bool(False),
    DepositLabel = cms.untracked.string('EcalPlusHcal'),
    CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
    Weight_H = cms.double(1.0)
)

process.FastjetParameters = cms.PSet(

)

process.MuonServiceProxy = cms.PSet(
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny', 
            'SteppingHelixPropagatorAlong', 
            'SteppingHelixPropagatorOpposite', 
            'SteppingHelixPropagatorL2Any', 
            'SteppingHelixPropagatorL2Along', 
            'SteppingHelixPropagatorL2Opposite', 
            'PropagatorWithMaterial', 
            'PropagatorWithMaterialOpposite', 
            'SmartPropagator', 
            'SmartPropagatorOpposite', 
            'SmartPropagatorAnyOpposite', 
            'SmartPropagatorAny', 
            'SmartPropagatorRK', 
            'SmartPropagatorAnyRK'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    )
)

process.PixelTripletHLTGenerator = cms.PSet(
    useBending = cms.bool(True),
    useFixedPreFiltering = cms.bool(False),
    ComponentName = cms.string('PixelTripletHLTGenerator'),
    extraHitRPhitolerance = cms.double(0.032),
    useMultScattering = cms.bool(True),
    phiPreFiltering = cms.double(0.3),
    extraHitRZtolerance = cms.double(0.037)
)

process.CSCSegAlgoST = cms.PSet(
    chamber_types = cms.vstring('ME1/a', 
        'ME1/b', 
        'ME1/2', 
        'ME1/3', 
        'ME2/1', 
        'ME2/2', 
        'ME3/1', 
        'ME3/2', 
        'ME4/1'),
    algo_name = cms.string('CSCSegAlgoST'),
    parameters_per_chamber_type = cms.vint32(2, 1, 1, 1, 1, 
        1, 1, 1, 1),
    algo_psets = cms.VPSet(cms.PSet(
        preClustering = cms.untracked.bool(True),
        minHitsPerSegment = cms.untracked.int32(3),
        yweightPenaltyThreshold = cms.untracked.double(1.0),
        curvePenalty = cms.untracked.double(2.0),
        dXclusBoxMax = cms.untracked.double(4.0),
        hitDropLimit5Hits = cms.untracked.double(0.8),
        yweightPenalty = cms.untracked.double(1.5),
        BrutePruning = cms.untracked.bool(False),
        curvePenaltyThreshold = cms.untracked.double(0.85),
        hitDropLimit4Hits = cms.untracked.double(0.6),
        hitDropLimit6Hits = cms.untracked.double(0.3333),
        maxRecHitsInCluster = cms.untracked.int32(20),
        CSCDebug = cms.untracked.bool(False),
        onlyBestSegment = cms.untracked.bool(False),
        Pruning = cms.untracked.bool(False),
        dYclusBoxMax = cms.untracked.double(8.0)
    ), 
        cms.PSet(
            preClustering = cms.untracked.bool(True),
            minHitsPerSegment = cms.untracked.int32(3),
            yweightPenaltyThreshold = cms.untracked.double(1.0),
            curvePenalty = cms.untracked.double(2.0),
            dXclusBoxMax = cms.untracked.double(4.0),
            hitDropLimit5Hits = cms.untracked.double(0.8),
            yweightPenalty = cms.untracked.double(1.5),
            BrutePruning = cms.untracked.bool(False),
            curvePenaltyThreshold = cms.untracked.double(0.85),
            hitDropLimit4Hits = cms.untracked.double(0.6),
            hitDropLimit6Hits = cms.untracked.double(0.3333),
            maxRecHitsInCluster = cms.untracked.int32(24),
            CSCDebug = cms.untracked.bool(False),
            onlyBestSegment = cms.untracked.bool(False),
            Pruning = cms.untracked.bool(False),
            dYclusBoxMax = cms.untracked.double(8.0)
        ))
)

process.CSCSegAlgoSK = cms.PSet(
    chamber_types = cms.vstring('ME1/a', 
        'ME1/b', 
        'ME1/2', 
        'ME1/3', 
        'ME2/1', 
        'ME2/2', 
        'ME3/1', 
        'ME3/2', 
        'ME4/1'),
    algo_name = cms.string('CSCSegAlgoSK'),
    parameters_per_chamber_type = cms.vint32(2, 1, 1, 1, 1, 
        1, 1, 1, 1),
    algo_psets = cms.VPSet(cms.PSet(
        dPhiFineMax = cms.double(0.025),
        verboseInfo = cms.untracked.bool(True),
        chi2Max = cms.double(99999.0),
        dPhiMax = cms.double(0.003),
        wideSeg = cms.double(3.0),
        minLayersApart = cms.int32(2),
        dRPhiFineMax = cms.double(8.0),
        dRPhiMax = cms.double(8.0)
    ), 
        cms.PSet(
            dPhiFineMax = cms.double(0.025),
            verboseInfo = cms.untracked.bool(True),
            chi2Max = cms.double(99999.0),
            dPhiMax = cms.double(0.025),
            wideSeg = cms.double(3.0),
            minLayersApart = cms.int32(2),
            dRPhiFineMax = cms.double(3.0),
            dRPhiMax = cms.double(8.0)
        ))
)

process.DF_ME1234_1 = cms.PSet(
    preClustering = cms.untracked.bool(False),
    maxRatioResidualPrune = cms.double(3.0),
    dPhiFineMax = cms.double(0.025),
    chi2Max = cms.double(5000.0),
    dXclusBoxMax = cms.double(8.0),
    tanThetaMax = cms.double(1.2),
    tanPhiMax = cms.double(0.5),
    minHitsPerSegment = cms.int32(3),
    minHitsForPreClustering = cms.int32(10),
    minLayersApart = cms.int32(2),
    dRPhiFineMax = cms.double(8.0),
    nHitsPerClusterIsShower = cms.int32(20),
    CSCSegmentDebug = cms.untracked.bool(False),
    Pruning = cms.untracked.bool(False),
    dYclusBoxMax = cms.double(8.0)
)

process.MIsoTrackExtractorCtfBlock = cms.PSet(
    Diff_z = cms.double(0.2),
    inputTrackCollection = cms.InputTag("generalTracks"),
    BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
    ComponentName = cms.string('TrackExtractor'),
    DR_Max = cms.double(1.0),
    Diff_r = cms.double(0.1),
    Chi2Prob_Min = cms.double(-1.0),
    DR_Veto = cms.double(0.01),
    NHits_Min = cms.uint32(0),
    Chi2Ndof_Max = cms.double(1e+64),
    Pt_Min = cms.double(-1.0),
    DepositLabel = cms.untracked.string(''),
    BeamlineOption = cms.string('BeamSpotFromEvent')
)

process.MIsoTrackAssociatorHits = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(1.0),
        dREcal = cms.double(1.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(1.0),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(1.0),
        useMuon = cms.bool(False),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    )
)

process.DF_ME1234_2 = cms.PSet(
    preClustering = cms.untracked.bool(False),
    maxRatioResidualPrune = cms.double(3.0),
    dPhiFineMax = cms.double(0.025),
    chi2Max = cms.double(5000.0),
    dXclusBoxMax = cms.double(8.0),
    tanThetaMax = cms.double(2.0),
    tanPhiMax = cms.double(0.8),
    minHitsPerSegment = cms.int32(3),
    minHitsForPreClustering = cms.int32(10),
    minLayersApart = cms.int32(2),
    dRPhiFineMax = cms.double(12.0),
    nHitsPerClusterIsShower = cms.int32(20),
    CSCSegmentDebug = cms.untracked.bool(False),
    Pruning = cms.untracked.bool(False),
    dYclusBoxMax = cms.double(12.0)
)

process.MinHitsTrajectoryFilter_block = cms.PSet(
    ComponentType = cms.string('MinHitsTrajectoryFilter'),
    minimumNumberOfHits = cms.int32(5)
)

process.MIsoDepositGlobalIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("globalMuons"),
    MultipleDepositsFlag = cms.bool(False),
    MuonTrackRefType = cms.string('track'),
    InputType = cms.string('TrackCollection')
)

process.DTTPGParametersBlock = cms.PSet(
    DTTPGParameters = cms.PSet(
        SectCollParameters = cms.PSet(
            SCCSP5 = cms.int32(0),
            SCCSP2 = cms.int32(0),
            SCCSP3 = cms.int32(0),
            SCECF4 = cms.bool(False),
            SCCSP1 = cms.int32(0),
            SCECF2 = cms.bool(False),
            SCECF3 = cms.bool(False),
            SCCSP4 = cms.int32(0),
            SCECF1 = cms.bool(False),
            Debug = cms.untracked.bool(False)
        ),
        Debug = cms.untracked.bool(False),
        TUParameters = cms.PSet(
            TracoParameters = cms.PSet(
                SPRGCOMP = cms.int32(2),
                FHTMSK = cms.int32(0),
                DD = cms.int32(18),
                SSLMSK = cms.int32(0),
                LVALIDIFH = cms.int32(0),
                Debug = cms.untracked.int32(0),
                FSLMSK = cms.int32(0),
                SHTPRF = cms.int32(1),
                SHTMSK = cms.int32(0),
                TRGENB3 = cms.int32(1),
                SHISM = cms.int32(0),
                IBTIOFF = cms.int32(0),
                KPRGCOM = cms.int32(255),
                KRAD = cms.int32(0),
                FLTMSK = cms.int32(0),
                LTS = cms.int32(0),
                SLTMSK = cms.int32(0),
                FPRGCOMP = cms.int32(2),
                TRGENB9 = cms.int32(1),
                TRGENB8 = cms.int32(1),
                FHTPRF = cms.int32(1),
                LTF = cms.int32(0),
                TRGENB1 = cms.int32(1),
                TRGENB0 = cms.int32(1),
                FHISM = cms.int32(0),
                TRGENB2 = cms.int32(1),
                TRGENB5 = cms.int32(1),
                TRGENB4 = cms.int32(1),
                TRGENB7 = cms.int32(1),
                TRGENB6 = cms.int32(1),
                TRGENB15 = cms.int32(1),
                TRGENB14 = cms.int32(1),
                TRGENB11 = cms.int32(1),
                TRGENB10 = cms.int32(1),
                TRGENB13 = cms.int32(1),
                TRGENB12 = cms.int32(1),
                REUSEO = cms.int32(1),
                REUSEI = cms.int32(1),
                BTIC = cms.int32(32)
            ),
            TSPhiParameters = cms.PSet(
                TSMNOE1 = cms.bool(True),
                TSMNOE2 = cms.bool(False),
                TSSMSK1 = cms.int32(312),
                TSTREN9 = cms.bool(True),
                TSTREN8 = cms.bool(True),
                TSTREN11 = cms.bool(True),
                TSTREN3 = cms.bool(True),
                TSTREN2 = cms.bool(True),
                TSTREN1 = cms.bool(True),
                TSTREN0 = cms.bool(True),
                TSTREN7 = cms.bool(True),
                TSTREN6 = cms.bool(True),
                TSTREN5 = cms.bool(True),
                TSTREN4 = cms.bool(True),
                TSSCCE1 = cms.bool(True),
                TSSCCE2 = cms.bool(False),
                TSMCCE2 = cms.bool(False),
                TSTREN19 = cms.bool(True),
                TSMCCE1 = cms.bool(True),
                TSTREN17 = cms.bool(True),
                TSTREN16 = cms.bool(True),
                TSTREN15 = cms.bool(True),
                TSTREN14 = cms.bool(True),
                TSTREN13 = cms.bool(True),
                TSTREN12 = cms.bool(True),
                TSSMSK2 = cms.int32(312),
                TSTREN10 = cms.bool(True),
                TSMMSK2 = cms.int32(312),
                TSMMSK1 = cms.int32(312),
                TSMHSP = cms.int32(1),
                TSSNOE2 = cms.bool(False),
                TSSNOE1 = cms.bool(True),
                TSSCGS2 = cms.bool(True),
                TSSCCEC = cms.bool(False),
                TSMCCEC = cms.bool(False),
                TSMHTE2 = cms.bool(False),
                Debug = cms.untracked.bool(False),
                TSSHTE2 = cms.bool(False),
                TSMCGS1 = cms.bool(True),
                TSMCGS2 = cms.bool(True),
                TSSHTE1 = cms.bool(True),
                TSTREN22 = cms.bool(True),
                TSSNOEC = cms.bool(False),
                TSTREN20 = cms.bool(True),
                TSTREN21 = cms.bool(True),
                TSMGS1 = cms.int32(1),
                TSMGS2 = cms.int32(1),
                TSSHTEC = cms.bool(False),
                TSMWORD = cms.int32(255),
                TSMHTEC = cms.bool(False),
                TSSCGS1 = cms.bool(True),
                TSTREN23 = cms.bool(True),
                TSSGS2 = cms.int32(1),
                TSMNOEC = cms.bool(False),
                TSSGS1 = cms.int32(1),
                TSTREN18 = cms.bool(True),
                TSMHTE1 = cms.bool(True)
            ),
            TSThetaParameters = cms.PSet(
                Debug = cms.untracked.bool(False)
            ),
            Debug = cms.untracked.bool(False),
            DIGIOFFSET = cms.int32(500),
            SINCROTIME = cms.int32(0),
            BtiParameters = cms.PSet(
                KACCTHETA = cms.int32(1),
                WEN8 = cms.int32(1),
                ACH = cms.int32(1),
                DEAD = cms.int32(31),
                ACL = cms.int32(2),
                PTMS20 = cms.int32(1),
                Debug = cms.untracked.int32(0),
                PTMS22 = cms.int32(1),
                PTMS23 = cms.int32(1),
                PTMS24 = cms.int32(1),
                PTMS25 = cms.int32(1),
                PTMS26 = cms.int32(1),
                PTMS27 = cms.int32(1),
                PTMS28 = cms.int32(1),
                PTMS29 = cms.int32(1),
                SET = cms.int32(7),
                RON = cms.bool(True),
                WEN2 = cms.int32(1),
                LL = cms.int32(2),
                LH = cms.int32(21),
                WEN3 = cms.int32(1),
                RE43 = cms.int32(2),
                WEN0 = cms.int32(1),
                RL = cms.int32(42),
                WEN1 = cms.int32(1),
                RH = cms.int32(61),
                LTS = cms.int32(3),
                CH = cms.int32(41),
                CL = cms.int32(22),
                PTMS15 = cms.int32(1),
                PTMS14 = cms.int32(1),
                PTMS17 = cms.int32(1),
                PTMS16 = cms.int32(1),
                PTMS11 = cms.int32(1),
                PTMS10 = cms.int32(1),
                PTMS13 = cms.int32(1),
                PTMS12 = cms.int32(1),
                XON = cms.bool(False),
                WEN7 = cms.int32(1),
                WEN4 = cms.int32(1),
                WEN5 = cms.int32(1),
                PTMS19 = cms.int32(1),
                PTMS18 = cms.int32(1),
                PTMS31 = cms.int32(0),
                PTMS30 = cms.int32(0),
                PTMS5 = cms.int32(1),
                PTMS4 = cms.int32(1),
                PTMS7 = cms.int32(1),
                PTMS6 = cms.int32(1),
                PTMS1 = cms.int32(0),
                PTMS0 = cms.int32(0),
                PTMS3 = cms.int32(0),
                WEN6 = cms.int32(1),
                PTMS2 = cms.int32(0),
                PTMS9 = cms.int32(1),
                PTMS8 = cms.int32(1),
                ST43 = cms.int32(42),
                AC2 = cms.int32(3),
                AC1 = cms.int32(0),
                KMAX = cms.int32(64),
                PTMS21 = cms.int32(1)
            )
        )
    )
)

process.CondDBSetup = cms.PSet(
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string('.'),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        connectionRetrialPeriod = cms.untracked.int32(10)
    )
)

process.SISConeJetParameters = cms.PSet(
    protojetPtMin = cms.double(0.0),
    JetPtMin = cms.double(1.0),
    coneOverlapThreshold = cms.double(0.75),
    caching = cms.bool(False),
    maxPasses = cms.int32(0),
    splitMergeScale = cms.string('pttilde')
)

process.MuonTrackLoaderForL3 = cms.PSet(
    TrackLoaderParameters = cms.PSet(
        MuonUpdatorAtVertexParameters = cms.PSet(
            MaxChi2 = cms.double(1000000.0),
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            Propagator = cms.string('SteppingHelixPropagatorOpposite'),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3)
        ),
        PutTkTrackIntoEvent = cms.untracked.bool(True),
        SmoothTkTrack = cms.untracked.bool(False),
        MuonSeededTracksInstance = cms.untracked.string('L2Seeded'),
        Smoother = cms.string('KFSmootherForMuonTrackLoaderL3'),
        VertexConstraint = cms.bool(False),
        DoSmoothing = cms.bool(True)
    )
)

process.electronPixelSeedConfiguration = cms.PSet(
    searchInTIDTEC = cms.bool(True),
    HighPtThreshold = cms.double(35.0),
    r2MinF = cms.double(-0.15),
    DeltaPhi1Low = cms.double(0.23),
    DeltaPhi1High = cms.double(0.08),
    ePhiMin1 = cms.double(-0.125),
    PhiMin2 = cms.double(-0.002),
    LowPtThreshold = cms.double(5.0),
    z2MinB = cms.double(-0.09),
    dynamicPhiRoad = cms.bool(True),
    ePhiMax1 = cms.double(0.075),
    DeltaPhi2 = cms.double(0.004),
    SizeWindowENeg = cms.double(0.675),
    rMaxI = cms.double(0.2),
    rMinI = cms.double(-0.2),
    preFilteredSeeds = cms.bool(False),
    r2MaxF = cms.double(0.15),
    pPhiMin1 = cms.double(-0.075),
    initialSeeds = cms.InputTag("newCombinedSeeds"),
    pPhiMax1 = cms.double(0.125),
    SCEtCut = cms.double(4.0),
    z2MaxB = cms.double(0.09),
    fromTrackerSeeds = cms.bool(True),
    hcalRecHits = cms.InputTag("hbhereco"),
    maxHOverE = cms.double(0.1),
    PhiMax2 = cms.double(0.002)
)

process.jcSetup1 = cms.PSet(
    jetCountersNegativeWheel = cms.VPSet(cms.PSet(
        cutDescriptionList = cms.vstring('JC_minRank_1')
    ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_1', 
                'JC_centralEta_6')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_11')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_11', 
                'JC_centralEta_6')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_19')
        )),
    jetCountersPositiveWheel = cms.VPSet(cms.PSet(
        cutDescriptionList = cms.vstring('JC_minRank_1')
    ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_1', 
                'JC_centralEta_6')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_11')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_11', 
                'JC_centralEta_6')
        ), 
        cms.PSet(
            cutDescriptionList = cms.vstring('JC_minRank_19')
        ))
)

process.DTCombinatorialPatternReco4DAlgo_LinearDriftFromDB_CosmicData = cms.PSet(
    Reco4DAlgoName = cms.string('DTCombinatorialPatternReco4D'),
    Reco4DAlgoConfig = cms.PSet(
        Reco2DAlgoConfig = cms.PSet(
            recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
            recAlgoConfig = cms.PSet(
                debug = cms.untracked.bool(False),
                minTime = cms.double(-3.0),
                maxTime = cms.double(420.0),
                tTrigModeConfig = cms.PSet(
                    vPropWire = cms.double(24.4),
                    doTOFCorrection = cms.bool(False),
                    tofCorrType = cms.int32(0),
                    kFactor = cms.double(-1.3),
                    wirePropCorrType = cms.int32(0),
                    doWirePropCorrection = cms.bool(False),
                    doT0Correction = cms.bool(True),
                    debug = cms.untracked.bool(False)
                ),
                tTrigMode = cms.string('DTTTrigSyncFromDB')
            ),
            T0SegCorrectionDebug = cms.untracked.bool(False),
            segmCleanerMode = cms.int32(1),
            nSharedHitsMax = cms.int32(2),
            AlphaMaxPhi = cms.double(100.0),
            hit_afterT0_resolution = cms.double(0.03),
            MaxAllowedHits = cms.uint32(50),
            performT0_vdriftSegCorrection = cms.bool(False),
            AlphaMaxTheta = cms.double(100.0),
            debug = cms.untracked.bool(False),
            nUnSharedHitsMin = cms.int32(2),
            performT0SegCorrection = cms.bool(False)
        ),
        Reco2DAlgoName = cms.string('DTCombinatorialPatternReco'),
        recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
        recAlgoConfig = cms.PSet(
            debug = cms.untracked.bool(False),
            minTime = cms.double(-3.0),
            maxTime = cms.double(420.0),
            tTrigModeConfig = cms.PSet(
                vPropWire = cms.double(24.4),
                doTOFCorrection = cms.bool(False),
                tofCorrType = cms.int32(0),
                kFactor = cms.double(-1.3),
                wirePropCorrType = cms.int32(0),
                doWirePropCorrection = cms.bool(False),
                doT0Correction = cms.bool(True),
                debug = cms.untracked.bool(False)
            ),
            tTrigMode = cms.string('DTTTrigSyncFromDB')
        ),
        T0SegCorrectionDebug = cms.untracked.bool(False),
        segmCleanerMode = cms.int32(2),
        nSharedHitsMax = cms.int32(2),
        hit_afterT0_resolution = cms.double(0.03),
        performT0_vdriftSegCorrection = cms.bool(False),
        debug = cms.untracked.bool(False),
        nUnSharedHitsMin = cms.int32(2),
        AllDTRecHits = cms.bool(True),
        performT0SegCorrection = cms.bool(False)
    )
)

process.CSCSegAlgoTC = cms.PSet(
    chamber_types = cms.vstring('ME1/a', 
        'ME1/b', 
        'ME1/2', 
        'ME1/3', 
        'ME2/1', 
        'ME2/2', 
        'ME3/1', 
        'ME3/2', 
        'ME4/1'),
    algo_name = cms.string('CSCSegAlgoTC'),
    parameters_per_chamber_type = cms.vint32(2, 1, 1, 1, 1, 
        1, 1, 1, 1),
    algo_psets = cms.VPSet(cms.PSet(
        dPhiFineMax = cms.double(0.02),
        verboseInfo = cms.untracked.bool(True),
        SegmentSorting = cms.int32(1),
        chi2Max = cms.double(6000.0),
        dPhiMax = cms.double(0.003),
        chi2ndfProbMin = cms.double(0.0001),
        minLayersApart = cms.int32(2),
        dRPhiFineMax = cms.double(6.0),
        dRPhiMax = cms.double(1.2)
    ), 
        cms.PSet(
            dPhiFineMax = cms.double(0.013),
            verboseInfo = cms.untracked.bool(True),
            SegmentSorting = cms.int32(1),
            chi2Max = cms.double(6000.0),
            dPhiMax = cms.double(0.00198),
            chi2ndfProbMin = cms.double(0.0001),
            minLayersApart = cms.int32(2),
            dRPhiFineMax = cms.double(3.0),
            dRPhiMax = cms.double(0.6)
        ))
)

process.TracoParametersBlock = cms.PSet(
    TracoParameters = cms.PSet(
        SPRGCOMP = cms.int32(2),
        FHTMSK = cms.int32(0),
        DD = cms.int32(18),
        SSLMSK = cms.int32(0),
        LVALIDIFH = cms.int32(0),
        Debug = cms.untracked.int32(0),
        FSLMSK = cms.int32(0),
        SHTPRF = cms.int32(1),
        SHTMSK = cms.int32(0),
        TRGENB3 = cms.int32(1),
        SHISM = cms.int32(0),
        IBTIOFF = cms.int32(0),
        KPRGCOM = cms.int32(255),
        KRAD = cms.int32(0),
        FLTMSK = cms.int32(0),
        LTS = cms.int32(0),
        SLTMSK = cms.int32(0),
        FPRGCOMP = cms.int32(2),
        TRGENB9 = cms.int32(1),
        TRGENB8 = cms.int32(1),
        FHTPRF = cms.int32(1),
        LTF = cms.int32(0),
        TRGENB1 = cms.int32(1),
        TRGENB0 = cms.int32(1),
        FHISM = cms.int32(0),
        TRGENB2 = cms.int32(1),
        TRGENB5 = cms.int32(1),
        TRGENB4 = cms.int32(1),
        TRGENB7 = cms.int32(1),
        TRGENB6 = cms.int32(1),
        TRGENB15 = cms.int32(1),
        TRGENB14 = cms.int32(1),
        TRGENB11 = cms.int32(1),
        TRGENB10 = cms.int32(1),
        TRGENB13 = cms.int32(1),
        TRGENB12 = cms.int32(1),
        REUSEO = cms.int32(1),
        REUSEI = cms.int32(1),
        BTIC = cms.int32(32)
    )
)

process.RegionPSetWithVerticesBlock = cms.PSet(
    RegionPSet = cms.PSet(
        precise = cms.bool(True),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        useFixedError = cms.bool(True),
        originRadius = cms.double(0.2),
        sigmaZVertex = cms.double(3.0),
        fixedError = cms.double(0.2),
        VertexCollection = cms.InputTag("pixelVertices"),
        ptMin = cms.double(0.9),
        useFoundVertices = cms.bool(True),
        nSigmaZ = cms.double(3.0)
    )
)

process.MIsoDepositViewIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("muons"),
    MultipleDepositsFlag = cms.bool(False),
    MuonTrackRefType = cms.string('bestTrkSta'),
    InputType = cms.string('MuonCollection')
)

process.MaxHitsTrajectoryFilter_block = cms.PSet(
    ComponentType = cms.string('MaxHitsTrajectoryFilter'),
    maxNumberOfHits = cms.int32(-1)
)

process.SiPixelGainCalibrationServiceParameters = cms.PSet(

)

process.FastjetNoPU = cms.PSet(
    Active_Area_Repeats = cms.int32(0),
    GhostArea = cms.double(1.0),
    Ghost_EtaMax = cms.double(0.0),
    UE_Subtraction = cms.string('no')
)

process.TUParamsBlock = cms.PSet(
    Debug = cms.untracked.bool(False),
    DIGIOFFSET = cms.int32(500),
    SINCROTIME = cms.int32(0)
)

process.MIsoDepositViewMultiIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("muons"),
    MultipleDepositsFlag = cms.bool(True),
    MuonTrackRefType = cms.string('bestTrkSta'),
    InputType = cms.string('MuonCollection')
)

process.DTLinearDriftFromDBAlgo_CosmicData = cms.PSet(
    recAlgoConfig = cms.PSet(
        debug = cms.untracked.bool(False),
        minTime = cms.double(-3.0),
        maxTime = cms.double(420.0),
        tTrigModeConfig = cms.PSet(
            vPropWire = cms.double(24.4),
            doTOFCorrection = cms.bool(False),
            tofCorrType = cms.int32(0),
            kFactor = cms.double(-0.7),
            wirePropCorrType = cms.int32(0),
            doWirePropCorrection = cms.bool(False),
            doT0Correction = cms.bool(True),
            debug = cms.untracked.bool(False)
        ),
        tTrigMode = cms.string('DTTTrigSyncFromDB')
    ),
    recAlgo = cms.string('DTLinearDriftFromDBAlgo')
)

process.layerInfo = cms.PSet(
    TEC4 = cms.PSet(
        minRing = cms.int32(1),
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
        maxRing = cms.int32(2)
    ),
    TEC5 = cms.PSet(
        minRing = cms.int32(1),
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
        maxRing = cms.int32(2)
    ),
    TEC6 = cms.PSet(
        minRing = cms.int32(1),
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
        maxRing = cms.int32(2)
    ),
    TEC = cms.PSet(
        minRing = cms.int32(5),
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(False),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
        maxRing = cms.int32(7)
    ),
    TEC1 = cms.PSet(
        minRing = cms.int32(1),
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
        maxRing = cms.int32(2)
    ),
    TEC2 = cms.PSet(
        minRing = cms.int32(1),
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
        maxRing = cms.int32(2)
    ),
    TEC3 = cms.PSet(
        minRing = cms.int32(1),
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
        maxRing = cms.int32(2)
    ),
    FPix = cms.PSet(
        hitErrorRZ = cms.double(0.0036),
        hitErrorRPhi = cms.double(0.0051),
        TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelPairs'),
        HitProducer = cms.string('siPixelRecHits'),
        useErrorsFromParam = cms.untracked.bool(True)
    ),
    TID = cms.PSet(
        matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
        useRingSlector = cms.untracked.bool(False),
        TTRHBuilder = cms.string('WithTrackAngle'),
        rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit")
    )
)

process.CompositeTrajectoryFilter_block = cms.PSet(
    ComponentType = cms.string('CompositeTrajectoryFilter'),
    filters = cms.VPSet()
)

process.BtiParametersBlock = cms.PSet(
    BtiParameters = cms.PSet(
        KACCTHETA = cms.int32(1),
        WEN8 = cms.int32(1),
        ACH = cms.int32(1),
        DEAD = cms.int32(31),
        ACL = cms.int32(2),
        PTMS20 = cms.int32(1),
        Debug = cms.untracked.int32(0),
        PTMS22 = cms.int32(1),
        PTMS23 = cms.int32(1),
        PTMS24 = cms.int32(1),
        PTMS25 = cms.int32(1),
        PTMS26 = cms.int32(1),
        PTMS27 = cms.int32(1),
        PTMS28 = cms.int32(1),
        PTMS29 = cms.int32(1),
        SET = cms.int32(7),
        RON = cms.bool(True),
        WEN2 = cms.int32(1),
        LL = cms.int32(2),
        LH = cms.int32(21),
        WEN3 = cms.int32(1),
        RE43 = cms.int32(2),
        WEN0 = cms.int32(1),
        RL = cms.int32(42),
        WEN1 = cms.int32(1),
        RH = cms.int32(61),
        LTS = cms.int32(3),
        CH = cms.int32(41),
        CL = cms.int32(22),
        PTMS15 = cms.int32(1),
        PTMS14 = cms.int32(1),
        PTMS17 = cms.int32(1),
        PTMS16 = cms.int32(1),
        PTMS11 = cms.int32(1),
        PTMS10 = cms.int32(1),
        PTMS13 = cms.int32(1),
        PTMS12 = cms.int32(1),
        XON = cms.bool(False),
        WEN7 = cms.int32(1),
        WEN4 = cms.int32(1),
        WEN5 = cms.int32(1),
        PTMS19 = cms.int32(1),
        PTMS18 = cms.int32(1),
        PTMS31 = cms.int32(0),
        PTMS30 = cms.int32(0),
        PTMS5 = cms.int32(1),
        PTMS4 = cms.int32(1),
        PTMS7 = cms.int32(1),
        PTMS6 = cms.int32(1),
        PTMS1 = cms.int32(0),
        PTMS0 = cms.int32(0),
        PTMS3 = cms.int32(0),
        WEN6 = cms.int32(1),
        PTMS2 = cms.int32(0),
        PTMS9 = cms.int32(1),
        PTMS8 = cms.int32(1),
        ST43 = cms.int32(42),
        AC2 = cms.int32(3),
        AC1 = cms.int32(0),
        KMAX = cms.int32(64),
        PTMS21 = cms.int32(1)
    )
)

process.TrackAssociatorParameters = cms.PSet(
    muonMaxDistanceSigmaX = cms.double(0.0),
    muonMaxDistanceSigmaY = cms.double(0.0),
    CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
    dRHcal = cms.double(9999.0),
    dREcal = cms.double(9999.0),
    CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
    useEcal = cms.bool(True),
    dREcalPreselection = cms.double(0.05),
    HORecHitCollectionLabel = cms.InputTag("horeco"),
    dRMuon = cms.double(9999.0),
    crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
    propagateAllDirections = cms.bool(True),
    muonMaxDistanceX = cms.double(5.0),
    muonMaxDistanceY = cms.double(5.0),
    useHO = cms.bool(True),
    accountForTrajectoryChangeCalo = cms.bool(False),
    DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
    EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    dRHcalPreselection = cms.double(0.2),
    useMuon = cms.bool(True),
    useCalo = cms.bool(False),
    EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    dRMuonPreselection = cms.double(0.2),
    truthMatch = cms.bool(False),
    HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
    useHcal = cms.bool(True)
)

process.DTCombinatorialPatternReco2DAlgo_LinearDriftFromDB_CosmicData = cms.PSet(
    Reco2DAlgoConfig = cms.PSet(
        recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
        recAlgoConfig = cms.PSet(
            debug = cms.untracked.bool(False),
            minTime = cms.double(-3.0),
            maxTime = cms.double(420.0),
            tTrigModeConfig = cms.PSet(
                vPropWire = cms.double(24.4),
                doTOFCorrection = cms.bool(False),
                tofCorrType = cms.int32(0),
                kFactor = cms.double(-1.3),
                wirePropCorrType = cms.int32(0),
                doWirePropCorrection = cms.bool(False),
                doT0Correction = cms.bool(True),
                debug = cms.untracked.bool(False)
            ),
            tTrigMode = cms.string('DTTTrigSyncFromDB')
        ),
        T0SegCorrectionDebug = cms.untracked.bool(False),
        segmCleanerMode = cms.int32(2),
        nSharedHitsMax = cms.int32(2),
        AlphaMaxPhi = cms.double(100.0),
        hit_afterT0_resolution = cms.double(0.03),
        MaxAllowedHits = cms.uint32(30),
        performT0_vdriftSegCorrection = cms.bool(False),
        AlphaMaxTheta = cms.double(100.0),
        debug = cms.untracked.bool(False),
        nUnSharedHitsMin = cms.int32(2),
        performT0SegCorrection = cms.bool(False)
    ),
    Reco2DAlgoName = cms.string('DTCombinatorialPatternReco')
)

process.ST_ME1A = cms.PSet(
    curvePenaltyThreshold = cms.untracked.double(0.85),
    minHitsPerSegment = cms.untracked.int32(3),
    yweightPenaltyThreshold = cms.untracked.double(1.0),
    curvePenalty = cms.untracked.double(2.0),
    dXclusBoxMax = cms.untracked.double(4.0),
    hitDropLimit5Hits = cms.untracked.double(0.8),
    yweightPenalty = cms.untracked.double(1.5),
    BrutePruning = cms.untracked.bool(False),
    preClustering = cms.untracked.bool(True),
    hitDropLimit4Hits = cms.untracked.double(0.6),
    Pruning = cms.untracked.bool(False),
    maxRecHitsInCluster = cms.untracked.int32(24),
    CSCDebug = cms.untracked.bool(False),
    onlyBestSegment = cms.untracked.bool(False),
    hitDropLimit6Hits = cms.untracked.double(0.3333),
    dYclusBoxMax = cms.untracked.double(8.0)
)

process.MIsoCaloExtractorEcalBlock = cms.PSet(
    DR_Veto_H = cms.double(0.1),
    Vertex_Constraint_Z = cms.bool(False),
    Threshold_H = cms.double(0.5),
    ComponentName = cms.string('CaloExtractor'),
    Threshold_E = cms.double(0.2),
    DR_Max = cms.double(1.0),
    DR_Veto_E = cms.double(0.07),
    Weight_E = cms.double(1.0),
    Vertex_Constraint_XY = cms.bool(False),
    DepositLabel = cms.untracked.string('EcalPlusHcal'),
    CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
    Weight_H = cms.double(0.0)
)

process.MIsoCaloExtractorHcalBlock = cms.PSet(
    DR_Veto_H = cms.double(0.1),
    Vertex_Constraint_Z = cms.bool(False),
    Threshold_H = cms.double(0.5),
    ComponentName = cms.string('CaloExtractor'),
    Threshold_E = cms.double(0.2),
    DR_Max = cms.double(1.0),
    DR_Veto_E = cms.double(0.07),
    Weight_E = cms.double(0.0),
    Vertex_Constraint_XY = cms.bool(False),
    DepositLabel = cms.untracked.string('EcalPlusHcal'),
    CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
    Weight_H = cms.double(1.0)
)

process.ST_ME1234 = cms.PSet(
    curvePenaltyThreshold = cms.untracked.double(0.85),
    minHitsPerSegment = cms.untracked.int32(3),
    yweightPenaltyThreshold = cms.untracked.double(1.0),
    curvePenalty = cms.untracked.double(2.0),
    dXclusBoxMax = cms.untracked.double(4.0),
    hitDropLimit5Hits = cms.untracked.double(0.8),
    yweightPenalty = cms.untracked.double(1.5),
    BrutePruning = cms.untracked.bool(False),
    preClustering = cms.untracked.bool(True),
    hitDropLimit4Hits = cms.untracked.double(0.6),
    Pruning = cms.untracked.bool(False),
    maxRecHitsInCluster = cms.untracked.int32(20),
    CSCDebug = cms.untracked.bool(False),
    onlyBestSegment = cms.untracked.bool(False),
    hitDropLimit6Hits = cms.untracked.double(0.3333),
    dYclusBoxMax = cms.untracked.double(8.0)
)

process.FastjetWithPU = cms.PSet(
    Active_Area_Repeats = cms.int32(5),
    GhostArea = cms.double(0.01),
    Ghost_EtaMax = cms.double(6.0),
    UE_Subtraction = cms.string('yes')
)

process.cscRecHitDParameters = cms.PSet(
    XTasymmetry_ME1b = cms.untracked.double(0.0),
    XTasymmetry_ME1a = cms.untracked.double(0.0),
    ConstSyst_ME1a = cms.untracked.double(0.022),
    ConstSyst_ME41 = cms.untracked.double(0.0),
    XTasymmetry_ME41 = cms.untracked.double(0.0),
    XTasymmetry_ME22 = cms.untracked.double(0.0),
    XTasymmetry_ME21 = cms.untracked.double(0.0),
    ConstSyst_ME21 = cms.untracked.double(0.0),
    ConstSyst_ME22 = cms.untracked.double(0.0),
    XTasymmetry_ME31 = cms.untracked.double(0.0),
    NoiseLevel_ME13 = cms.untracked.double(8.0),
    NoiseLevel_ME12 = cms.untracked.double(9.0),
    NoiseLevel_ME32 = cms.untracked.double(9.0),
    NoiseLevel_ME31 = cms.untracked.double(9.0),
    XTasymmetry_ME32 = cms.untracked.double(0.0),
    ConstSyst_ME1b = cms.untracked.double(0.007),
    XTasymmetry_ME13 = cms.untracked.double(0.0),
    XTasymmetry_ME12 = cms.untracked.double(0.0),
    ConstSyst_ME12 = cms.untracked.double(0.0),
    ConstSyst_ME13 = cms.untracked.double(0.0),
    ConstSyst_ME32 = cms.untracked.double(0.0),
    ConstSyst_ME31 = cms.untracked.double(0.0),
    NoiseLevel_ME1a = cms.untracked.double(7.0),
    NoiseLevel_ME1b = cms.untracked.double(8.0),
    NoiseLevel_ME21 = cms.untracked.double(9.0),
    NoiseLevel_ME22 = cms.untracked.double(9.0),
    NoiseLevel_ME41 = cms.untracked.double(9.0)
)

process.MIsoDepositParamGlobalMultiIOBlock = cms.PSet(
    ExtractForCandidate = cms.bool(False),
    inputMuonCollection = cms.InputTag("paramMuons","ParamGlobalMuons"),
    MultipleDepositsFlag = cms.bool(True),
    MuonTrackRefType = cms.string('track'),
    InputType = cms.string('MuonCollection')
)

process.ThresholdPtTrajectoryFilter_block = cms.PSet(
    ComponentType = cms.string('ThresholdPtTrajectoryFilter'),
    nSigmaThresholdPt = cms.double(5.0),
    minHitsThresholdPt = cms.int32(3),
    thresholdPt = cms.double(10.0)
)

process.DTTPGMapBlock = cms.PSet(
    DTTPGMap = cms.untracked.PSet(
        wh0st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se4 = cms.untracked.vint32(72, 48, 72, 18),
        whm2st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se3 = cms.untracked.vint32(72, 48, 72, 18),
        whm1st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        whm2st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        whm2st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        whm1st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm1st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        whm2st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh1st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm1st1se3 = cms.untracked.vint32(50, 48, 50, 13),
        whm1st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se4 = cms.untracked.vint32(60, 48, 60, 15),
        wh1st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        wh1st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        wh2st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        whm2st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se1 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se2 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se4 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        wh0st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh0st4se4 = cms.untracked.vint32(72, 0, 72, 18),
        wh0st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh2st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        wh2st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh2st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh2st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se5 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se7 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st4se8 = cms.untracked.vint32(92, 0, 92, 23),
        whm1st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        whm1st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se7 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st1se8 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st1se11 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se10 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se12 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st4se6 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st1se5 = cms.untracked.vint32(50, 58, 50, 13),
        whm1st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se3 = cms.untracked.vint32(60, 48, 60, 15),
        whm1st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se7 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se6 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se4 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se2 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se1 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh2st2se9 = cms.untracked.vint32(60, 58, 60, 15),
        wh2st2se8 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh0st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh0st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        whm1st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        whm2st1se3 = cms.untracked.vint32(50, 58, 50, 13),
        wh0st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st4se10 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st4se11 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh1st4se13 = cms.untracked.vint32(72, 0, 72, 18),
        wh1st4se14 = cms.untracked.vint32(60, 0, 60, 15),
        wh1st1se4 = cms.untracked.vint32(50, 48, 50, 13),
        wh1st1se7 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se6 = cms.untracked.vint32(50, 58, 50, 13),
        wh1st1se9 = cms.untracked.vint32(50, 58, 50, 13),
        whm2st3se10 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st2se3 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st3se11 = cms.untracked.vint32(72, 58, 72, 18),
        whm2st3se12 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se12 = cms.untracked.vint32(92, 0, 92, 23),
        wh1st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st4se9 = cms.untracked.vint32(48, 0, 48, 12),
        wh1st3se8 = cms.untracked.vint32(72, 58, 72, 18),
        wh0st4se2 = cms.untracked.vint32(96, 0, 96, 24),
        wh2st3se1 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se2 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se3 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se4 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se5 = cms.untracked.vint32(72, 58, 72, 18),
        wh2st3se6 = cms.untracked.vint32(72, 58, 72, 18),
        wh1st4se3 = cms.untracked.vint32(96, 0, 96, 24),
        whm2st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        wh1st4se1 = cms.untracked.vint32(96, 0, 96, 24),
        whm1st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se11 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se10 = cms.untracked.vint32(60, 58, 60, 15),
        whm2st2se12 = cms.untracked.vint32(60, 58, 60, 15),
        wh0st2se5 = cms.untracked.vint32(60, 58, 60, 15),
        whm1st3se9 = cms.untracked.vint32(72, 58, 72, 18),
        whm1st3se8 = cms.untracked.vint32(72, 58, 72, 18)
    )
)

process.SectCollParametersBlock = cms.PSet(
    SectCollParameters = cms.PSet(
        SCCSP5 = cms.int32(0),
        SCCSP2 = cms.int32(0),
        SCCSP3 = cms.int32(0),
        SCECF4 = cms.bool(False),
        SCCSP1 = cms.int32(0),
        SCECF2 = cms.bool(False),
        SCECF3 = cms.bool(False),
        SCCSP4 = cms.int32(0),
        SCECF1 = cms.bool(False),
        Debug = cms.untracked.bool(False)
    )
)

process.ChargeSignificanceTrajectoryFilter_block = cms.PSet(
    ComponentType = cms.string('ChargeSignificanceTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0)
)

process.MinPtTrajectoryFilter_block = cms.PSet(
    ComponentType = cms.string('MinPtTrajectoryFilter'),
    nSigmaMinPt = cms.double(5.0),
    minHitsMinPt = cms.int32(3),
    minPt = cms.double(1.0)
)

process.SK_ME1A = cms.PSet(
    dPhiFineMax = cms.double(0.025),
    verboseInfo = cms.untracked.bool(True),
    chi2Max = cms.double(99999.0),
    dPhiMax = cms.double(0.025),
    wideSeg = cms.double(3.0),
    minLayersApart = cms.int32(2),
    dRPhiFineMax = cms.double(3.0),
    dRPhiMax = cms.double(8.0)
)

process.MIsoCaloExtractorByAssociatorHitsBlock = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(1.0),
        dREcal = cms.double(1.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(True),
        dREcalPreselection = cms.double(1.0),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(True),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(1.0),
        useMuon = cms.bool(False),
        useCalo = cms.bool(False),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(True)
    ),
    PropagatorName = cms.string('SteppingHelixPropagatorAny'),
    NoiseTow_EB = cms.double(0.04),
    Noise_EE = cms.double(0.1),
    PrintTimeReport = cms.untracked.bool(False),
    DR_Veto_E = cms.double(0.07),
    NoiseTow_EE = cms.double(0.15),
    Threshold_HO = cms.double(0.1),
    ComponentName = cms.string('CaloExtractorByAssociator'),
    Noise_HO = cms.double(0.2),
    DR_Max = cms.double(1.0),
    Noise_EB = cms.double(0.025),
    Threshold_E = cms.double(0.025),
    Noise_HB = cms.double(0.2),
    UseRecHitsFlag = cms.bool(True),
    Threshold_H = cms.double(0.1),
    DR_Veto_H = cms.double(0.1),
    DepositLabel = cms.untracked.string('Cal'),
    Noise_HE = cms.double(0.2),
    DR_Veto_HO = cms.double(0.1),
    DepositInstanceLabels = cms.vstring('ecal', 
        'hcal', 
        'ho')
)

process.MIsoCaloExtractorByAssociatorTowersBlock = cms.PSet(
    TrackAssociatorParameterBlock = cms.PSet(
        TrackAssociatorParameters = cms.PSet(
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
            dRHcal = cms.double(9999.0),
            dREcal = cms.double(9999.0),
            CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
            useEcal = cms.bool(True),
            dREcalPreselection = cms.double(0.05),
            HORecHitCollectionLabel = cms.InputTag("horeco"),
            dRMuon = cms.double(9999.0),
            crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            useHO = cms.bool(True),
            accountForTrajectoryChangeCalo = cms.bool(False),
            DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
            EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
            dRHcalPreselection = cms.double(0.2),
            useMuon = cms.bool(True),
            useCalo = cms.bool(False),
            EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
            dRMuonPreselection = cms.double(0.2),
            truthMatch = cms.bool(False),
            HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
            useHcal = cms.bool(True)
        )
    ),
    TrackAssociatorParameters = cms.PSet(
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        CSCSegmentCollectionLabel = cms.InputTag("cscSegments"),
        dRHcal = cms.double(1.0),
        dREcal = cms.double(1.0),
        CaloTowerCollectionLabel = cms.InputTag("towerMaker"),
        useEcal = cms.bool(False),
        dREcalPreselection = cms.double(1.0),
        HORecHitCollectionLabel = cms.InputTag("horeco"),
        dRMuon = cms.double(9999.0),
        crossedEnergyType = cms.string('SinglePointAlongTrajectory'),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        useHO = cms.bool(False),
        accountForTrajectoryChangeCalo = cms.bool(False),
        DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments"),
        EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
        dRHcalPreselection = cms.double(1.0),
        useMuon = cms.bool(False),
        useCalo = cms.bool(True),
        EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
        dRMuonPreselection = cms.double(0.2),
        truthMatch = cms.bool(False),
        HBHERecHitCollectionLabel = cms.InputTag("hbhereco"),
        useHcal = cms.bool(False)
    ),
    PropagatorName = cms.string('SteppingHelixPropagatorAny'),
    NoiseTow_EB = cms.double(0.04),
    Noise_EE = cms.double(0.1),
    PrintTimeReport = cms.untracked.bool(False),
    DR_Veto_E = cms.double(0.07),
    NoiseTow_EE = cms.double(0.15),
    Threshold_HO = cms.double(0.5),
    ComponentName = cms.string('CaloExtractorByAssociator'),
    Noise_HO = cms.double(0.2),
    DR_Max = cms.double(1.0),
    Noise_EB = cms.double(0.025),
    Threshold_E = cms.double(0.2),
    Noise_HB = cms.double(0.2),
    UseRecHitsFlag = cms.bool(False),
    Threshold_H = cms.double(0.5),
    DR_Veto_H = cms.double(0.1),
    DepositLabel = cms.untracked.string('Cal'),
    Noise_HE = cms.double(0.2),
    DR_Veto_HO = cms.double(0.1),
    DepositInstanceLabels = cms.vstring('ecal', 
        'hcal', 
        'ho')
)

process.RegionPSetBlock = cms.PSet(
    RegionPSet = cms.PSet(
        precise = cms.bool(True),
        originHalfLength = cms.double(15.9),
        originZPos = cms.double(0.0),
        originYPos = cms.double(0.0),
        ptMin = cms.double(0.9),
        originXPos = cms.double(0.0),
        originRadius = cms.double(0.2)
    )
)

process.MaxLostHitsTrajectoryFilter_block = cms.PSet(
    ComponentType = cms.string('MaxLostHitsTrajectoryFilter'),
    maxLostHits = cms.int32(1)
)

process.CkfBaseTrajectoryFilter_block = cms.PSet(
    minimumNumberOfHits = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    maxLostHits = cms.int32(1),
    maxNumberOfHits = cms.int32(-1),
    maxConsecLostHits = cms.int32(1),
    chargeSignificance = cms.double(-1.0),
    nSigmaMinPt = cms.double(5.0),
    minPt = cms.double(0.9)
)

