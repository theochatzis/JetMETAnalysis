import FWCore.ParameterSet.Config as cms

_JetPtEta = cms.PSet( 
  etaMin = cms.double(-5.5),
  etaMax = cms.double(5.5),
  ptMin = cms.double(1.0)
)

_RefPtEta = cms.PSet(
  etaMin = cms.double(-5.5),
  etaMax = cms.double(5.5),
  ptMin = cms.double(1.0)
)

_JetResponseParameters = cms.PSet(
  # record flavor information, consider both RefPt and JetPt
  doComposition   = cms.bool(True),
  doFlavor        = cms.bool(False),
  doRefPt         = cms.bool(True),
  doJetPt         = cms.bool(True),
  saveCandidates  = cms.bool(False),
  # MATCHING MODE: deltaR(ref,jet)
  deltaRMax       = cms.double(0.2),
  # deltaR(ref,parton) IF doFlavor is True
  deltaRPartonMax = cms.double(0.2),
  # consider all matched references
  nRefMax         = cms.uint32(0),
  # is the sample an HLT sample
  doHLT           = cms.bool(False)
)

def addAlgorithm(process, moduleNamePrefix):
    ## reference (genjet) kinematic selection
    refPtEta = cms.EDFilter('EtaPtMinCandViewRefSelector', _RefPtEta, src = cms.InputTag(''))
    setattr(process, moduleNamePrefix + 'GenPtEta', refPtEta)

    ## reco jet kinematic selection
    jetPtEta = cms.EDFilter('EtaPtMinCandViewRefSelector', _JetPtEta, src = cms.InputTag(''))
    setattr(process, moduleNamePrefix + 'PtEta', jetPtEta)

    jetPtEtaUncor = jetPtEta.clone()
    setattr(process, moduleNamePrefix + 'PtEtaUncor', jetPtEtaUncor)

    ## reference to jet matching
    jetToRef = cms.EDProducer('MatchRecToGen',
      srcGen = cms.InputTag(refPtEta.label()),
      srcRec = cms.InputTag(jetPtEta.label())
    )
    setattr(process,moduleNamePrefix + 'JetToRef', jetToRef)

    jetToUncorJet = cms.EDProducer('MatchRecToGen',
      srcGen = cms.InputTag(jetPtEtaUncor.label()),
      srcRec = cms.InputTag(jetPtEta.label())
    )
    setattr(process,moduleNamePrefix + 'JetToUncorJet', jetToUncorJet)

    ## jet response analyzer
    jra = cms.EDAnalyzer('JetResponseAnalyzer',
      _JetResponseParameters,
      srcRefToJetMap = cms.InputTag(jetToRef.label(), 'gen2rec'),
      srcRef = cms.InputTag(refPtEta.label()),
      jecLabel = cms.string(''),
      srcRhos = cms.InputTag(''),
      srcRho = cms.InputTag(''),
      srcRhoHLT = cms.InputTag(''),
      srcVtx = cms.InputTag('hltPixelVertices'),
      applyVtxCuts = cms.bool(False),
      srcJetToUncorJetMap = cms.InputTag(''),
      srcPFCandidates = cms.InputTag(''),
      srcGenParticles = cms.InputTag('genParticles')
    )
    setattr(process,moduleNamePrefix,jra)

    ## sequence, path, schedule
    sequence = cms.Sequence(
        refPtEta
      * jetPtEta
      * jetPtEtaUncor
      * jetToRef
      * jetToUncorJet
      * jra
    )
    setattr(process, moduleNamePrefix + 'Sequence', sequence)
    setattr(process, moduleNamePrefix + 'Path', cms.Path(sequence))

    if moduleNamePrefix.startswith('ak4'):
      refPtEta.src = 'ak4GenJetsNoNu'
      jetPtEta.src = ''
    elif moduleNamePrefix.startswith('ak8'):
      refPtEta.src = 'ak8GenJetsNoNu'
      jetPtEta.src = ''
    else: raise RuntimeError('')

    jetPtEtaUncor.src = jetPtEta.src

    if process.schedule_() is not None:
      process.schedule_().append(getattr(process, moduleNamePrefix + 'Path'))
