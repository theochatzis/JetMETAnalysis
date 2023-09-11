import FWCore.ParameterSet.Config as cms

stdClusteringAlgorithms = [
  'ak',
]
stdJetTypes = [
# 'caloHLT',
# 'pfHLT',
# 'pfchsHLT',
  'pfpuppiHLT',
]
stdCorrectionLevels = {
#  'l1'     : 'L1',
#  'l2l3'   : 'L2L3',
#  'l1l2l3' : 'L1FastL2L3'
}

stdGenJetsDict = {}
stdRecJetsDict = {}
corrJetsDict = {}

jetColl = {
  'ak4pfHLT': 'hltAK4PFJets',
  'ak4pfpuppiHLT': 'hltAK4PFPuppiJets',

  'ak8pfHLT': 'hltAK8PFJets',
  'ak8pfpuppiHLT': 'hltAK8PFPuppiJets',
}

for ca in stdClusteringAlgorithms:
    for jt in stdJetTypes:
        for r in [4, 8]:
            alg_size_type = str(ca)+str(r)+str(jt)

            ## Generator Jets
#           tmpString = str(ca)+str(r)+"GenJets"
            tmpString = str(ca)+str(r)+"GenJetsNoNu"
            stdGenJetsDict[alg_size_type] = tmpString

            ## Reconstructed Jets
            stdRecJetsDict[alg_size_type] = jetColl[ca+str(r)+jt]

            ## Corrected Jets
            for cl in stdCorrectionLevels :
                if ca == 'kt': continue
                if jt == 'calo' and not r in [4,7]: continue
                alg_size_type_corr = alg_size_type+cl
                if jt == 'calo' :
                    tmpString = str(ca)+str(r)+str(jt).capitalize()+'Jets'+str(stdCorrectionLevels[cl])
                else :
                    tmpString = str(ca)+str(r)+str(jt).upper()+'Jets'+str(stdCorrectionLevels[cl])
                corrJetsDict[alg_size_type_corr] = (tmpString,eval(tmpString))

def addAlgorithm(process, alg_size_type_corr, Defaults):
    """ 
    addAlgorithm takes the following parameters:
    ============================================
    it will then create a complete sequence within an executable path
    to kinematically select references and jets, select partons and match
    them to the references, match references and jets, and finally execute
    the JetResponseAnalyzer.
    """
    ## deterine algorithm, size, type (Calo|PF|Track|JPT), and wether to apply jec
    alg_size      = ''
    type          = ''
    alg_size_type = ''
    correctl1     = False
    correctl1off  = False
    correctl2l3   = False
    if (alg_size_type_corr.find('caloHLT') > 0) :
        alg_size      = alg_size_type_corr[0:alg_size_type_corr.find('caloHLT')]
        type          = 'CaloHLT'
        alg_size_type = alg_size + 'caloHLT'
    elif (alg_size_type_corr.find('calo') > 0) :
        alg_size      = alg_size_type_corr[0:alg_size_type_corr.find('calo')]
        type          = 'Calo'
        alg_size_type = alg_size + 'calo'
    elif (alg_size_type_corr.find('pfHLT') > 0) :
        alg_size      = alg_size_type_corr[0:alg_size_type_corr.find('pfHLT')]
        type          = 'PFHLT'
        alg_size_type = alg_size + 'pfHLT'
    elif (alg_size_type_corr.find('puppiHLT') > 0) :
        alg_size      = alg_size_type_corr[0:alg_size_type_corr.find('puppiHLT')]
        type          = 'PuppiHLT'
        alg_size_type = alg_size + 'puppiHLT'
    elif (alg_size_type_corr.find('pfchsHLT') > 0) :
        alg_size      = alg_size_type_corr[0:alg_size_type_corr.find('pfchsHLT')]
        type          = 'PFchsHLT'
        alg_size_type = alg_size + 'pfchsHLT'
    elif (alg_size_type_corr.find('pfchs') > 0) :
        alg_size      = alg_size_type_corr[0:alg_size_type_corr.find('pfchs')]
        type          = 'PFchs'
        alg_size_type = alg_size + 'pfchs'
    elif (alg_size_type_corr.find('pf') > 0) :
        alg_size      = alg_size_type_corr[0:alg_size_type_corr.find('pf')]
        type          = 'PF'
        alg_size_type = alg_size + 'pf'
    elif (alg_size_type_corr.find('puppi') > 0) :
        alg_size      = alg_size_type_corr[0:alg_size_type_corr.find('puppi')]
        type          = 'PUPPI'
        alg_size_type = alg_size + 'puppi'
    else:
        raise ValueError("Can't identify valid jet type: calo|caloHLT|pf|pfchs|pfHLT|jpt|trk|tau|puppi")
        
    if (alg_size_type_corr.find('l1') > 0):
        correctl1 = True
        if (alg_size_type_corr.find('l1off') > 0):
            correctl1off = True

    if (alg_size_type_corr.find('l2l3') > 0):
        correctl2l3 = True


    ## check that alg_size_type_corr refers to valid jet configuration
    try:
        list(stdGenJetsDict.keys()).index(alg_size_type)
        list(stdRecJetsDict.keys()).index(alg_size_type)
    except ValueError:
        raise ValueError("Algorithm unavailable in standard format: " + alg_size_type)

    try:
        correctl2l3 and list(corrJetsDict.keys()).index(alg_size_type_corr)
    except ValueError:
        raise ValueError("Invalid jet correction: " + alg_size_type_corr)
        
    ## reference (genjet) kinematic selection
    refPtEta = cms.EDFilter('EtaPtMinCandViewRefSelector',
        Defaults.RefPtEta,
        src = cms.InputTag(stdGenJetsDict[alg_size_type]),
    )

    setattr(process, alg_size_type + 'GenPtEta', refPtEta)

    ## reco jet kinematic selection
    jetPtEta = cms.EDFilter('EtaPtMinCandViewRefSelector',
        Defaults.JetPtEta,
        src = cms.InputTag(stdRecJetsDict[alg_size_type]),
    )

    setattr(process, alg_size_type_corr + 'PtEta', jetPtEta)
    
    ## create the sequence
    sequence = cms.Sequence(refPtEta * jetPtEta)

    jetPtEtaUncor = jetPtEta.clone()
    setattr(process, alg_size_type_corr + 'PtEtaUncor', jetPtEtaUncor)
    sequence = cms.Sequence(sequence * jetPtEtaUncor)

    ## correct jets
    corrLabel = ''
    if correctl1 or correctl2l3:
        process.load('JetMETAnalysis.JetAnalyzers.JetCorrection_cff')
        (corrLabel, corrJets) = corrJetsDict[alg_size_type_corr]
        setattr(process, corrLabel, corrJets)
        sequence = cms.Sequence(eval(corrLabel.replace("Jets","")+"CorrectorChain") * corrJets * sequence)

    ## add pu density calculation
    if not correctl1 and not correctl1off:
       pass
#        if type == 'CaloHLT': #added 02/15/2012
#            process.kt6CaloJets = kt6CaloJets 
#            process.kt6CaloJets.doRhoFastjet = True
#            process.kt6CaloJets.Ghost_EtaMax = Defaults.kt6CaloJetParameters.Ghost_EtaMax.value()
#            process.kt6CaloJets.Rho_EtaMax   = Defaults.kt6CaloJetParameters.Rho_EtaMax
#            sequence = cms.Sequence(process.kt6CaloJets * sequence)
#        elif type == 'PFchsHLT':
#            process.kt6PFJets = kt6PFJets
#            process.kt6PFJets.doRhoFastjet = True
#            process.kt6PFJets.Ghost_EtaMax = Defaults.kt6PFJetParameters.Ghost_EtaMax.value()
#            process.kt6PFJets.Rho_EtaMax   = Defaults.kt6PFJetParameters.Rho_EtaMax
#            sequence = cms.Sequence(process.kt6PFJets * sequence)
#        elif type == 'PFHLT':
#            process.kt6PFJets = kt6PFJets
#            process.kt6PFJets.doRhoFastjet = True
#            process.kt6PFJets.Ghost_EtaMax = Defaults.kt6PFJetParameters.Ghost_EtaMax.value()
#            process.kt6PFJets.Rho_EtaMax   = Defaults.kt6PFJetParameters.Rho_EtaMax
#            sequence = cms.Sequence(process.kt6PFJets * sequence)
    elif correctl1 and not correctl1off:  #modified 10/10/2011
        if type == 'CaloHLT': #added 02/15/2012
            process.kt6CaloJets = kt6CaloJets 
            process.kt6CaloJets.doRhoFastjet = True
            process.kt6CaloJets.Ghost_EtaMax = Defaults.kt6PFJetParameters.Ghost_EtaMax.value()
            process.kt6CaloJets.Rho_EtaMax   = Defaults.kt6PFJetParameters.Rho_EtaMax
            sequence = cms.Sequence(process.kt6CaloJets * sequence)
        elif type == 'PFchs':
            process.kt6PFJets = kt6PFJets
            process.kt6PFJets.doRhoFastjet = True
            process.kt6PFJets.Ghost_EtaMax = Defaults.kt6PFJetParameters.Ghost_EtaMax.value()
            process.kt6PFJets.Rho_EtaMax   = Defaults.kt6PFJetParameters.Rho_EtaMax
            sequence = cms.Sequence(process.kt6PFJets * sequence)
        elif type == 'PFHLT':
            process.kt6PFJets = kt6PFJets
            process.kt6PFJets.doRhoFastjet = True
            process.kt6PFJets.Ghost_EtaMax = Defaults.kt6PFJetParameters.Ghost_EtaMax.value()
            process.kt6PFJets.Rho_EtaMax   = Defaults.kt6PFJetParameters.Rho_EtaMax
            sequence = cms.Sequence(process.kt6PFJets * sequence)
        elif type == 'PFchsHLT':
            process.kt6PFJets = kt6PFJets
            process.kt6PFJets.doRhoFastjet = True
            process.kt6PFJets.Ghost_EtaMax = Defaults.kt6PFJetParameters.Ghost_EtaMax.value()
            process.kt6PFJets.Rho_EtaMax   = Defaults.kt6PFJetParameters.Rho_EtaMax
            sequence = cms.Sequence(process.kt6PFJets * sequence)
        elif type == 'PF':
            process.kt6PFJets = kt6PFJets
            process.kt6PFJets.doRhoFastjet = True
            process.kt6PFJets.Ghost_EtaMax = Defaults.kt6PFJetParameters.Ghost_EtaMax.value()
            process.kt6PFJets.Rho_EtaMax   = Defaults.kt6PFJetParameters.Rho_EtaMax
            sequence = cms.Sequence(process.kt6PFJets * sequence)

    ## reference to jet matching
    jetToRef = cms.EDProducer('MatchRecToGen',
        srcGen = cms.InputTag(refPtEta.label()),
        srcRec = cms.InputTag(jetPtEta.label())
    )
    setattr(process,alg_size_type_corr + 'JetToRef', jetToRef)
    sequence = cms.Sequence(sequence * jetToRef)

    jetToUncorJet = cms.EDProducer('MatchRecToGen',
        srcGen = cms.InputTag(jetPtEtaUncor.label()),
        srcRec = cms.InputTag(jetPtEta.label())
    )
    setattr(process,alg_size_type_corr + 'JetToUncorJet', jetToUncorJet)
    sequence = cms.Sequence(sequence * jetToUncorJet)

    ## jet response analyzer
    jraAnalyzer = 'JetResponseAnalyzer'
    jra = cms.EDAnalyzer(jraAnalyzer,
                         Defaults.JetResponseParameters,
                         srcRefToJetMap    = cms.InputTag(jetToRef.label(), 'gen2rec'),
                         srcRef            = cms.InputTag(refPtEta.label()),
                         jecLabel          = cms.string(''),
                         srcRhos           = cms.InputTag(''),
                         srcRho            = cms.InputTag(''),
                         srcRhoHLT         = cms.InputTag(''),
                         srcVtx            = cms.InputTag('offlinePrimaryVertices'),
                         srcJetToUncorJetMap = cms.InputTag(jetToUncorJet.label(), 'rec2gen'),
                         srcPFCandidates   = cms.InputTag(''),
                         srcGenParticles   = cms.InputTag('genParticles')
                        )

    if type == 'CaloHLT':
        jra.srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
        jra.srcRhoHLT = cms.InputTag("fixedGridRhoFastjetAllCalo")
    elif type == 'Calo':
        jra.srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
    elif type == 'PFchs':
        process.kt6PFchsJetsRhos = kt6PFJets.clone(src = 'pfNoPileUpJME',
                                                   doFastJetNonUniform = cms.bool(True),
                                                   puCenters = cms.vdouble(-5,-4,-3,-2,-1,0,1,2,3,4,5), 
                                                   puWidth = cms.double(.8),
                                                   nExclude = cms.uint32(2))
        sequence = cms.Sequence(process.kt6PFchsJetsRhos * sequence)
        jra.srcRhos = cms.InputTag("kt6PFchsJetsRhos", "rhos")
        jra.srcRho = cms.InputTag("fixedGridRhoFastjetAll")
        jra.srcPFCandidates = cms.InputTag('pfNoPileUpJME')
    elif type == 'PFHLT':
        jra.srcRho = 'fixedGridRhoFastjetAll'
        jra.srcRhoHLT = 'fixedGridRhoFastjetAll'
    elif type == 'PuppiHLT':
        jra.srcRho = 'fixedGridRhoFastjetAll'
        jra.srcRhoHLT = 'fixedGridRhoFastjetAll'
    elif type == 'PFchsHLT':
        jra.srcRho = ak4PFchsL1Fastjet.srcRho #added 02/15/2012
        jra.srcRhoHLT = ak5PFchsHLTL1Fastjet.srcRho
    elif type == 'PF':
        process.kt6PFJetsRhos = kt6PFJets.clone(doFastJetNonUniform = cms.bool(True),
                                                puCenters = cms.vdouble(-5,-4,-3,-2,-1,0,1,2,3,4,5),
                                                puWidth = cms.double(.8), 
                                                nExclude = cms.uint32(2))
        sequence = cms.Sequence(process.kt6PFJetsRhos * sequence)
        jra.srcRhos = cms.InputTag("kt6PFJetsRhos", "rhos")
        jra.srcRho = cms.InputTag("fixedGridRhoFastjetAll")
        jra.srcPFCandidates = cms.InputTag('particleFlow')
    elif type == 'PUPPI':
        process.kt6PFJetsRhos = kt6PFJets.clone(doFastJetNonUniform = cms.bool(True),
                                                puCenters = cms.vdouble(-5,-4,-3,-2,-1,0,1,2,3,4,5),
                                                puWidth = cms.double(.8), nExclude = cms.uint32(2))
        sequence = cms.Sequence(process.kt6PFJetsRhos * sequence)
        jra.srcRhos = cms.InputTag("kt6PFJetsRhos", "rhos")
        jra.srcRho = cms.InputTag("fixedGridRhoFastjetAll")
        jra.srcPFCandidates = cms.InputTag('puppi')

    if correctl1 or correctl2l3:
        jra.jecLabel = corrJets.correctors[0].replace("Corrector","")

    setattr(process,alg_size_type_corr,jra)
    sequence = cms.Sequence(sequence * jra)

    ## create the path and put in the sequence
    sequence = cms.Sequence(sequence)
    setattr(process, alg_size_type_corr + 'Sequence', sequence)
    path = cms.Path( sequence )
    setattr(process, alg_size_type_corr + 'Path', path)

    if process.schedule_() is not None:
       process.schedule_().append(getattr(process, alg_size_type_corr + 'Path'))
