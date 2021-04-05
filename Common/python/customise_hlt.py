import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.ak4PFClusterJets_cfi import ak4PFClusterJets as _ak4PFClusterJets
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi as _ak4PFJetsPuppi
from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJetsPuppi as _ak8PFJetsPuppi
from CommonTools.PileupAlgos.Puppi_cff import puppi as _puppi, puppiNoLep as _puppiNoLep
from JMETriggerAnalysis.Common.multiplicityValueProducerFromNestedCollectionEdmNewDetSetVectorSiPixelClusterDouble_cfi\
 import multiplicityValueProducerFromNestedCollectionEdmNewDetSetVectorSiPixelClusterDouble as _nSiPixelClusters

def addPaths_MC_JMECalo(process):
    process.hltPreMCJMECalo = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    ## MET Type-1
    process.hltCaloMETCorrection = cms.EDProducer('CaloJetMETcorrInputProducer',
      jetCorrEtaMax = cms.double(9.9),
      jetCorrLabel = cms.InputTag('hltAK4CaloCorrector'),
      jetCorrLabelRes = cms.InputTag('hltAK4CaloCorrector'),
      offsetCorrLabel = cms.InputTag('hltAK4CaloFastJetCorrector'),
      skipEM = cms.bool(True),
      skipEMfractionThreshold = cms.double(0.9),
      src = cms.InputTag('hltAK4CaloJets'),
      type1JetPtThreshold = cms.double(30.0),
    )

    process.hltCaloMETTypeOne = cms.EDProducer('CorrectedCaloMETProducer',
      src = cms.InputTag('hltMet'),
      srcCorrections = cms.VInputTag('hltCaloMETCorrection:type1'),
    )

    ## Path
    process.MC_JMECalo_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCJMECalo
      + process.HLTDoCaloSequence
      ## AK{4,8} Jets
      + process.hltAK4CaloJets
      + process.HLTAK4CaloJetsCorrectionSequence
      + process.hltAK8CaloJets
      + process.HLTAK8CaloJetsCorrectionSequence
      ## MET
      + process.hltMet
      ## MET Type-1
      + process.hltCaloMETCorrection
      + process.hltCaloMETTypeOne
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().append(process.MC_JMECalo_v1)

    return process

def addPaths_MC_JMEPFCluster(process):
    process.hltPreMCJMEPFCluster = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    process.HLTParticleFlowClusterSequence = cms.Sequence(
        process.HLTDoFullUnpackingEgammaEcalWithoutPreshowerSequence
      + process.HLTDoLocalHcalSequence
      + process.HLTPreshowerSequence
      + process.hltParticleFlowRecHitECALUnseeded
      + process.hltParticleFlowRecHitHBHE
      + process.hltParticleFlowRecHitHF
      + process.hltParticleFlowRecHitPSUnseeded
      + process.hltParticleFlowClusterECALUncorrectedUnseeded
      + process.hltParticleFlowClusterPSUnseeded
      + process.hltParticleFlowClusterECALUnseeded
      + process.hltParticleFlowClusterHBHE
      + process.hltParticleFlowClusterHCAL
      + process.hltParticleFlowClusterHF
    )

    process.hltParticleFlowClusterRefsECALUnseeded = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('hltParticleFlowClusterECALUnseeded'),
      particleType = cms.string('pi+')
    )

    process.hltParticleFlowClusterRefsHCAL = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('hltParticleFlowClusterHCAL'),
      particleType = cms.string('pi+')
    )

    process.hltParticleFlowClusterRefsHF = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('hltParticleFlowClusterHF'),
      particleType = cms.string('pi+')
    )

    process.hltParticleFlowClusterRefs = cms.EDProducer('PFClusterRefCandidateMerger',
      src = cms.VInputTag(
        'hltParticleFlowClusterRefsECALUnseeded',
        'hltParticleFlowClusterRefsHCAL',
        'hltParticleFlowClusterRefsHF',
      )
    )

    process.HLTParticleFlowClusterRefsSequence = cms.Sequence(
        process.hltParticleFlowClusterRefsECALUnseeded
      + process.hltParticleFlowClusterRefsHCAL
      + process.hltParticleFlowClusterRefsHF
      + process.hltParticleFlowClusterRefs
    )

    ## AK4 Jets
    process.hltAK4PFClusterJets = _ak4PFClusterJets.clone(
      src = 'hltParticleFlowClusterRefs',
      doAreaDiskApprox = True,
      doPVCorrection = False,
    )

    process.hltAK4PFClusterJetCorrectorL1 = cms.EDProducer('L1FastjetCorrectorProducer',
      algorithm = cms.string('AK4PFClusterHLT'),
      level = cms.string('L1FastJet'),
      srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'),#!!
    )

    process.hltAK4PFClusterJetCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFClusterHLT'),
      level = cms.string('L2Relative'),
    )

    process.hltAK4PFClusterJetCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFClusterHLT'),
      level = cms.string('L3Absolute'),
    )

    process.hltAK4PFClusterJetCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK4PFClusterJetCorrectorL1',
        'hltAK4PFClusterJetCorrectorL2',
        'hltAK4PFClusterJetCorrectorL3',
      ),
    )

    process.hltAK4PFClusterJetsCorrected = cms.EDProducer('CorrectedPFClusterJetProducer',
      src = cms.InputTag('hltAK4PFClusterJets'),
      correctors = cms.VInputTag('hltAK4PFClusterJetCorrector'),
    )

    ## AK8 Jets
    process.hltAK8PFClusterJets = _ak4PFClusterJets.clone(
      src = 'hltParticleFlowClusterRefs',
      doAreaDiskApprox = True,
      doPVCorrection = False,
      rParam = 0.8,
    )

    process.hltAK8PFClusterJetCorrectorL1 = cms.EDProducer('L1FastjetCorrectorProducer',
      algorithm = cms.string('AK8PFClusterHLT'),
      level = cms.string('L1FastJet'),
      srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'),
    )

    process.hltAK8PFClusterJetCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFClusterHLT'),
      level = cms.string('L2Relative'),
    )

    process.hltAK8PFClusterJetCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFClusterHLT'),
      level = cms.string('L3Absolute'),
    )

    process.hltAK8PFClusterJetCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK8PFClusterJetCorrectorL1',
        'hltAK8PFClusterJetCorrectorL2',
        'hltAK8PFClusterJetCorrectorL3',
      ),
    )

    process.hltAK8PFClusterJetsCorrected = cms.EDProducer('CorrectedPFClusterJetProducer',
      src = cms.InputTag('hltAK8PFClusterJets'),
      correctors = cms.VInputTag('hltAK8PFClusterJetCorrector'),
    )

    ## MET
    process.hltPFClusterMET = cms.EDProducer('PFClusterMETProducer',
      src = cms.InputTag('hltParticleFlowClusterRefs'),
      globalThreshold = cms.double(0.0),
      alias = cms.string(''),
    )

    ## MET Type-1
    process.hltPFClusterMETCorrection = cms.EDProducer('PFClusterJetMETcorrInputProducer',
      jetCorrEtaMax = cms.double(9.9),
      jetCorrLabel = cms.InputTag('hltAK4PFClusterJetCorrector'),
      jetCorrLabelRes = cms.InputTag('hltAK4PFClusterJetCorrector'),
      offsetCorrLabel = cms.InputTag('hltAK4PFClusterJetCorrectorL1'),
      skipEM = cms.bool(True),
      skipEMfractionThreshold = cms.double(0.9),
      src = cms.InputTag('hltAK4PFClusterJets'),
      type1JetPtThreshold = cms.double(30.0),
    )

    process.hltPFClusterMETTypeOne = cms.EDProducer('CorrectedPFClusterMETProducer',
      src = cms.InputTag('hltPFClusterMET'),
      srcCorrections = cms.VInputTag('hltPFClusterMETCorrection:type1'),
    )

    process.MC_JMEPFCluster_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCJMEPFCluster
      + process.HLTParticleFlowClusterSequence
      + process.HLTParticleFlowClusterRefsSequence
      ## AK4 Jets
      + process.hltAK4PFClusterJets
      + process.hltAK4PFClusterJetCorrectorL1
      + process.hltAK4PFClusterJetCorrectorL2
      + process.hltAK4PFClusterJetCorrectorL3
      + process.hltAK4PFClusterJetCorrector
      + process.hltAK4PFClusterJetsCorrected
      ## AK8 Jets
      + process.hltAK8PFClusterJets
      + process.hltAK8PFClusterJetCorrectorL1
      + process.hltAK8PFClusterJetCorrectorL2
      + process.hltAK8PFClusterJetCorrectorL3
      + process.hltAK8PFClusterJetCorrector
      + process.hltAK8PFClusterJetsCorrected
      ## MET
      + process.hltPFClusterMET
      ## MET Type-1
      + process.hltPFClusterMETCorrection
      + process.hltPFClusterMETTypeOne
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().append(process.MC_JMEPFCluster_v1)

    return process

def addPaths_MC_JMEPF(process):
    process.hltPreMCJMEPF = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    ## Path
    process.MC_JMEPF_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCJMEPF
      ## MET Type-1
      + process.hltcorrPFMETTypeOne
      + process.hltPFMETTypeOne
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().append(process.MC_JMEPF_v1)

    return process

def addPaths_MC_JMEPFPuppi(process):

    process.hltPreMCJMEPFPuppi = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    process.hltPixelClustersMultiplicity = _nSiPixelClusters.clone(src = 'hltSiPixelClusters', defaultValue = -1.)

    process.hltPFPuppi = _puppi.clone(
      candName = 'hltParticleFlow',
      vertexName = 'hltVerticesPF',
      usePUProxyValue = True,
      PUProxyValue = 'hltPixelClustersMultiplicity',
    )

    process.HLTPFPuppiSequence = cms.Sequence(
        process.HLTDoCaloSequencePF
      + process.HLTL2muonrecoSequence
      + process.HLTL3muonrecoSequence
      + process.HLTTrackReconstructionForPF
      + process.HLTParticleFlowSequence
      + process.hltVerticesPF
      + process.hltPixelClustersMultiplicity
      + process.hltPFPuppi
    )

    ## AK4
    process.hltAK4PFPuppiJets = _ak4PFJetsPuppi.clone(
      src = 'hltParticleFlow',
      srcWeights = 'hltPFPuppi',
      applyWeight = True,
    )

    process.hltAK4PFPuppiJetCorrectorL1 = cms.EDProducer('L1FastjetCorrectorProducer',
      algorithm = cms.string('AK4PFPuppiHLT'),
      level = cms.string('L1FastJet'),
      srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'),
    )

    process.hltAK4PFPuppiJetCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFPuppiHLT'),
      level = cms.string('L2Relative')
    )

    process.hltAK4PFPuppiJetCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFPuppiHLT'),
      level = cms.string('L3Absolute')
    )

    process.hltAK4PFPuppiJetCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK4PFPuppiJetCorrectorL1',
        'hltAK4PFPuppiJetCorrectorL2',
        'hltAK4PFPuppiJetCorrectorL3',
      ),
    )

    process.hltAK4PFPuppiJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag('hltAK4PFPuppiJets'),
      correctors = cms.VInputTag('hltAK4PFPuppiJetCorrector'),
    )

    process.HLTAK4PFPuppiJetsSequence = cms.Sequence(
        process.hltAK4PFPuppiJets
      + process.hltAK4PFPuppiJetCorrectorL1
      + process.hltAK4PFPuppiJetCorrectorL2
      + process.hltAK4PFPuppiJetCorrectorL3
      + process.hltAK4PFPuppiJetCorrector
      + process.hltAK4PFPuppiJetsCorrected
    )

    ## AK8
    process.hltAK8PFPuppiJets = _ak8PFJetsPuppi.clone(
      src = 'hltParticleFlow',
      srcWeights = 'hltPFPuppi',
      applyWeight = True,
    )

    process.hltAK8PFPuppiJetCorrectorL1 = cms.EDProducer('L1FastjetCorrectorProducer',
      algorithm = cms.string('AK8PFPuppiHLT'),
      level = cms.string('L1FastJet'),
      srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'),
    )

    process.hltAK8PFPuppiJetCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFPuppiHLT'),
      level = cms.string('L2Relative')
    )

    process.hltAK8PFPuppiJetCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFPuppiHLT'),
      level = cms.string('L3Absolute')
    )

    process.hltAK8PFPuppiJetCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK8PFPuppiJetCorrectorL1',
        'hltAK8PFPuppiJetCorrectorL2',
        'hltAK8PFPuppiJetCorrectorL3',
      ),
    )

    process.hltAK8PFPuppiJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag('hltAK8PFPuppiJets'),
      correctors = cms.VInputTag('hltAK8PFPuppiJetCorrector'),
    )

    process.HLTAK8PFPuppiJetsSequence = cms.Sequence(
        process.hltAK8PFPuppiJets
      + process.hltAK8PFPuppiJetCorrectorL1
      + process.hltAK8PFPuppiJetCorrectorL2
      + process.hltAK8PFPuppiJetCorrectorL3
      + process.hltAK8PFPuppiJetCorrector
      + process.hltAK8PFPuppiJetsCorrected
    )

    ## MET
    process.hltPFPuppiNoLep = _puppiNoLep.clone(
      candName = 'hltParticleFlow',
      vertexName = 'hltVerticesPF',
      usePUProxyValue = True,
      PUProxyValue = 'hltPixelClustersMultiplicity',
    )

    process.hltPFPuppiMET = cms.EDProducer('PFMETProducer',
      alias = cms.string(''),
      applyWeight = cms.bool(True),
      calculateSignificance = cms.bool(False),
      globalThreshold = cms.double(0.0),
      parameters = cms.PSet(),
      src = cms.InputTag('hltParticleFlow'),
      srcWeights = cms.InputTag('hltPFPuppiNoLep'),
    )

    process.HLTPFPuppiMETSequence = cms.Sequence(
        process.hltPFPuppiNoLep
      + process.hltPFPuppiMET
    )

    ## MET Type-1
    process.hltPFPuppiMETCorrection = cms.EDProducer('PFJetMETcorrInputProducer',
      jetCorrEtaMax = cms.double(9.9),
      jetCorrLabel = cms.InputTag('hltAK4PFPuppiJetCorrector'),
      jetCorrLabelRes = cms.InputTag('hltAK4PFPuppiJetCorrector'),
      offsetCorrLabel = cms.InputTag('hltAK4PFPuppiJetCorrectorL1'),
      skipEM = cms.bool(True),
      skipEMfractionThreshold = cms.double(0.9),
      skipMuonSelection = cms.string('isGlobalMuon | isStandAloneMuon'),
      skipMuons = cms.bool(True),
      src = cms.InputTag('hltAK4PFPuppiJets'),
      type1JetPtThreshold = cms.double(30.0),
    )

    process.hltPFPuppiMETTypeOne = cms.EDProducer('CorrectedPFMETProducer',
      src = cms.InputTag('hltPFPuppiMET'),
      srcCorrections = cms.VInputTag('hltPFPuppiMETCorrection:type1'),
    )

    ## Modifications to PUPPI parameters
    for mod_i in [process.hltPFPuppi, process.hltPFPuppiNoLep]:
      for algo_idx in range(len(mod_i.algos)):
        if len(mod_i.algos[algo_idx].MinNeutralPt) != len(mod_i.algos[algo_idx].MinNeutralPtSlope):
          raise RuntimeError('instance of PuppiProducer is misconfigured:\n\n'+str(mod_i)+' = '+mod_i.dumpPython())

        for algoReg_idx in range(len(mod_i.algos[algo_idx].MinNeutralPt)):
          mod_i.algos[algo_idx].MinNeutralPt[algoReg_idx] += 2.56 * mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx]
          mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx] *= 0.00271

    ## Path
    process.MC_JMEPFPuppi_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCJMEPFPuppi
      ## AK{4,8} Jets
      + process.HLTPFPuppiSequence
      + process.HLTAK4PFPuppiJetsSequence
      + process.HLTAK8PFPuppiJetsSequence
      ## MET
      + process.HLTPFPuppiMETSequence
      ## MET Type-1
      + process.hltPFPuppiMETCorrection
      + process.hltPFPuppiMETTypeOne
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().append(process.MC_JMEPFPuppi_v1)

    return process
