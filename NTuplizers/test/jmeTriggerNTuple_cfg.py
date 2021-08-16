import os
import fnmatch

from CondCore.CondDB.CondDB_cfi import CondDB as _CondDB

###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

#opts.register('globalTag', None,
#              vpo.VarParsing.multiplicity.singleton,
#              vpo.VarParsing.varType.string,
#              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT_Run3TRK',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword to define HLT reconstruction')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.register('keepPFPuppi', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'keep full collection of PFlow and PFPuppi candidates')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

#opts.register('printSummaries', False,
#              vpo.VarParsing.multiplicity.singleton,
#              vpo.VarParsing.varType.bool,
#              'show summaries from HLT services')

opts.parseArguments()

###
### HLT configuration
###
if opts.reco == 'HLT_GRun_oldJECs':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_0_0_HLT_V4_configDump import cms, process
  update_jmeCalibs = False

elif opts.reco == 'HLT_GRun':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_0_0_HLT_V4_configDump import cms, process
  update_jmeCalibs = True

elif opts.reco == 'HLT_Run3TRK':
  # (a) Run-3 tracking: standard
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_0_0_HLT_V4_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTforRun3Tracking import customizeHLTforRun3Tracking
  process = customizeHLTforRun3Tracking(process)
  update_jmeCalibs = True

elif opts.reco == 'HLT_Run3TRKWithPU':
  # (b) Run-3 tracking: all pixel vertices
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_0_0_HLT_V4_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTforRun3Tracking import customizeHLTforRun3TrackingAllPixelVertices
  process = customizeHLTforRun3TrackingAllPixelVertices(process)
  update_jmeCalibs = True

else:
  raise RuntimeError('keyword "reco = '+opts.reco+'" not recognised')

# remove cms.OutputModule objects from HLT config-dump
for _modname in process.outputModules_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.OutputModule:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print('> removed cms.OutputModule:', _modname)

# remove cms.EndPath objects from HLT config-dump
for _modname in process.endpaths_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.EndPath:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print('> removed cms.EndPath:', _modname)

# remove selected cms.Path objects from HLT config-dump
print('-'*108)
print('{:<99} | {:<4} |'.format('cms.Path', 'keep'))
print('-'*108)

# list of patterns to determine paths to keep
keepPaths = [
  'MC_*Jets*',
  'MC_*MET*',
  'MC_*AK8Calo*',
  'HLT_PFJet*_v*',
  'HLT_AK4PFJet*_v*',
  'HLT_AK8PFJet*_v*',
  'HLT_PFHT*_v*',
  'HLT_PFMET*_PFMHT*_v*',
]

vetoPaths = [
  'HLT_*ForPPRef_v*',
]

# list of paths that are kept
listOfPaths = []

for _modname in sorted(process.paths_()):
    _keepPath = False
    for _tmpPatt in keepPaths:
      _keepPath = fnmatch.fnmatch(_modname, _tmpPatt)
      if _keepPath: break

    if _keepPath:
      for _tmpPatt in vetoPaths:
        if fnmatch.fnmatch(_modname, _tmpPatt):
          _keepPath = False
          break

    if _keepPath:
      print('{:<99} | {:<4} |'.format(_modname, '+'))
      listOfPaths.append(_modname)
      continue
    _mod = getattr(process, _modname)
    if type(_mod) == cms.Path:
      process.__delattr__(_modname)
      print('{:<99} | {:<4} |'.format(_modname, ''))
print('-'*108)

# remove FastTimerService
if hasattr(process, 'FastTimerService'):
  del process.FastTimerService

# remove MessageLogger
if hasattr(process, 'MessageLogger'):
  del process.MessageLogger

###
### customisations
###

## customised JME collections
from JMETriggerAnalysis.Common.customise_hlt import *
process = addPaths_MC_JMECalo(process)
process = addPaths_MC_JMEPFCluster(process)
process = addPaths_MC_JMEPF(process)
process = addPaths_MC_JMEPFCHS(process)
process = addPaths_MC_JMEPFPuppi(process)

if update_jmeCalibs:
  ## ES modules for PF-Hadron Calibrations
  process.pfhcESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/data/PFHC_Run3Winter20_HLT_v01.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('PFCalibrationRcd'),
        tag = cms.string('PFCalibration_HLT_mcRun3_2021'),
        label = cms.untracked.string('HLT'),
      ),
    ),
  )
  process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')
  #process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

  ## ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/data/JESC_Run3Winter20_V2_MC.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4CaloHLT'),
        label = cms.untracked.string('AK4CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFClusterHLT'),
        label = cms.untracked.string('AK4PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFHLT'),
        label = cms.untracked.string('AK4PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFHLT'),#!!
        label = cms.untracked.string('AK4PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFPuppiHLT'),
        label = cms.untracked.string('AK4PFPuppiHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8CaloHLT'),
        label = cms.untracked.string('AK8CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFClusterHLT'),
        label = cms.untracked.string('AK8PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFHLT'),
        label = cms.untracked.string('AK8PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFHLT'),#!!
        label = cms.untracked.string('AK8PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFPuppiHLT'),
        label = cms.untracked.string('AK8PFPuppiHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

else:
  ## ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/data/JESC_Run3Winter20_V2_MC.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFClusterHLT'),
        label = cms.untracked.string('AK4PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFHLT'),#!!
        label = cms.untracked.string('AK4PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFPuppiHLT'),
        label = cms.untracked.string('AK4PFPuppiHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFClusterHLT'),
        label = cms.untracked.string('AK8PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFHLT'),#!!
        label = cms.untracked.string('AK8PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFPuppiHLT'),
        label = cms.untracked.string('AK8PFPuppiHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

## Output NTuple
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',
  TTreeName = cms.string('Events'),
  TriggerResults = cms.InputTag('TriggerResults'),
  TriggerResultsFilterOR = cms.vstring(),
  TriggerResultsFilterAND = cms.vstring(),
  TriggerResultsCollections = cms.vstring(
    sorted(list(set([(_tmp[:_tmp.rfind('_v')] if '_v' in _tmp else _tmp) for _tmp in listOfPaths])))
  ),
  outputBranchesToBeDropped = cms.vstring(),

  HepMCProduct = cms.InputTag('generatorSmeared'),
  GenEventInfoProduct = cms.InputTag('generator'),
  PileupSummaryInfo = cms.InputTag('addPileupInfo'),

  doubles = cms.PSet(

    hltFixedGridRhoFastjetAllCalo = cms.InputTag('hltFixedGridRhoFastjetAllCalo'),
    hltFixedGridRhoFastjetAllPFCluster = cms.InputTag('hltFixedGridRhoFastjetAllPFCluster'),
    hltFixedGridRhoFastjetAll = cms.InputTag('hltFixedGridRhoFastjetAll'),
    offlineFixedGridRhoFastjetAll = cms.InputTag('fixedGridRhoFastjetAll::RECO'),

    hltPixelClustersMultiplicity = cms.InputTag('hltPixelClustersMultiplicity'),
  ),

  vdoubles = cms.PSet(
  ),

  recoVertexCollections = cms.PSet(

    hltPixelVertices = cms.InputTag('hltPixelVertices'),
    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    hltVerticesPF = cms.InputTag('hltVerticesPF'),
    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  recoPFCandidateCollections = cms.PSet(
  ),

  recoGenJetCollections = cms.PSet(

    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
    hltAK4CaloJetsCorrected = cms.InputTag('hltAK4CaloJetsCorrected'),

    hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
    hltAK8CaloJetsCorrected = cms.InputTag('hltAK8CaloJetsCorrected'),
  ),

  recoPFClusterJetCollections = cms.PSet(

    hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
    hltAK4PFClusterJetsCorrected = cms.InputTag('hltAK4PFClusterJetsCorrected'),

    hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
    hltAK8PFClusterJetsCorrected = cms.InputTag('hltAK8PFClusterJetsCorrected'),
  ),

  recoPFJetCollections = cms.PSet(

    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),

    hltAK4PFCHSJets = cms.InputTag('hltAK4PFCHSJets'),
    hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),

    hltAK4PFPuppiJets = cms.InputTag('hltAK4PFPuppiJets'),
    hltAK4PFPuppiJetsCorrected = cms.InputTag('hltAK4PFPuppiJetsCorrected'),

    hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),

    hltAK8PFCHSJets = cms.InputTag('hltAK8PFCHSJets'),
    hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),

    hltAK8PFPuppiJets = cms.InputTag('hltAK8PFPuppiJets'),
    hltAK8PFPuppiJetsCorrected = cms.InputTag('hltAK8PFPuppiJetsCorrected'),
  ),

  patJetCollections = cms.PSet(

    offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    offlineAK4PFPuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
    offlineAK8PFPuppiJetsCorrected = cms.InputTag('slimmedJetsAK8'),
  ),

  recoGenMETCollections = cms.PSet(

    genMETCalo = cms.InputTag('genMetCalo::HLT'),
    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(

    hltCaloMET = cms.InputTag('hltMet'),
    hltCaloMETTypeOne = cms.InputTag('hltCaloMETTypeOne'),
  ),

  recoPFClusterMETCollections = cms.PSet(

    hltPFClusterMET = cms.InputTag('hltPFClusterMET'),
    hltPFClusterMETTypeOne = cms.InputTag('hltPFClusterMETTypeOne'),
  ),

  recoPFMETCollections = cms.PSet(

    hltPFMET = cms.InputTag('hltPFMETProducer'),
    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),

    hltPFCHSMET = cms.InputTag('hltPFCHSMET'),
    hltPFCHSMETTypeOne = cms.InputTag('hltPFCHSMETTypeOne'),

    hltPFPuppiMET = cms.InputTag('hltPFPuppiMET'),
    hltPFPuppiMETTypeOne = cms.InputTag('hltPFPuppiMETTypeOne'),
  ),

  patMETCollections = cms.PSet(

    offlinePFMET = cms.InputTag('slimmedMETs'),
    offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),
)

if opts.keepPFPuppi:
  process.hltPFPuppi.puppiDiagnostics = True
  process.JMETriggerNTuple.vdoubles = cms.PSet(
    hltPFPuppi_PuppiRawAlphas = cms.InputTag('hltPFPuppi:PuppiRawAlphas'),
    hltPFPuppi_PuppiAlphas = cms.InputTag('hltPFPuppi:PuppiAlphas'),
    hltPFPuppi_PuppiAlphasMed = cms.InputTag('hltPFPuppi:PuppiAlphasMed'),
    hltPFPuppi_PuppiAlphasRms = cms.InputTag('hltPFPuppi:PuppiAlphasRms'),
  )
  process.JMETriggerNTuple.recoPFCandidateCollections = cms.PSet(
    hltParticleFlow = cms.InputTag('hltParticleFlow'),
    hltPFPuppi = cms.InputTag('hltPFPuppi'),
  )

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
#process.HLTSchedule.extend([process.analysisNTupleEndPath])

#if opts.printSummaries:
#   process.FastTimerService.printEventSummary = False
#   process.FastTimerService.printRunSummary = False
#   process.FastTimerService.printJobSummary = True
#   process.ThroughputService.printEventSummary = False

###
### standard options
###

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = max(opts.numThreads, 1)
process.options.numberOfStreams = max(opts.numStreams, 0)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

## update process.GlobalTag.globaltag
#if opts.globalTag is not None:
#   from Configuration.AlCa.GlobalTag import GlobalTag
#   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# input EDM files [primary]
if opts.inputFiles:
  process.source.fileNames = opts.inputFiles
else:
  process.source.fileNames = [
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/MINIAODSIM/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/CE60A1DD-226B-B742-98E9-A09249BEFDA2.root'
  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/00E83D67-63EB-EB43-8989-68ACAD981A10.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/12D114E8-BBFF-574F-806A-3BE5C5FDBFB8.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/12DC883A-082B-4642-A445-868ECDDF3FA5.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/16972812-2808-314B-B5AA-54D41CC37285.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/1D58BA9D-EC39-7347-9CED-CA99D82D2206.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/388752E2-8A49-4E43-9869-D14BC0203087.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/48A588A8-36DE-1948-9AE6-DD458C1509F2.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/495788FC-5DC6-4A44-8B63-B591C19EB674.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/56AAD83C-751C-424D-B964-3556C93A595F.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/6A51016A-C628-9A4E-B007-50084FDBFC80.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/7F69AE21-49DD-7846-A809-FFADAAC3F4A9.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/871ECE14-7F8F-0E4A-A36A-6142B769A4D7.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/878DE7C3-CEC9-0747-9CB4-B8BC6E85DD4E.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/90035F4A-1F74-0643-8C75-D1AEC46E4A15.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/9B3E1268-7673-954A-AEA5-7D0BE6D94FEB.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/A56F1704-6E6B-674E-BA4E-F36C000204C7.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/B033B4EA-0733-4840-82FF-8EC14547383C.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/BEFB2C90-4912-3240-943F-8FFFAD875C32.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/C9939A7C-C9B8-F441-9041-62349DF7B092.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/CB5EE5CF-B0BE-6940-9B92-274556053F77.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/CE3B3CB9-AE21-B441-9412-91553043B444.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/D2F54AC7-7964-B54B-B9E6-43ABED588830.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/DB690341-0817-1E46-9B0B-CE1D4B552FA6.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/DF55BDEA-D820-F647-A9A5-B15D006DD6A2.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/EAB306EE-5E34-FF4A-A3B1-74C6116F75FC.root',
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/250000/F7CA9145-CC3D-5E4C-9610-33C17F15CC5F.root',
  ]

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# printouts
if opts.verbosity > 0:
   print('--- jmeTriggerNTuple_cfg.py ---')
   print('')
   print('option: output =', opts.output)
   print('option: reco =', opts.reco)
   print('option: dumpPython =', opts.dumpPython)
   print('')
   print('process.GlobalTag =', process.GlobalTag.dumpPython())
   print('process.source =', process.source.dumpPython())
   print('process.maxEvents =', process.maxEvents.dumpPython())
   print('process.options =', process.options.dumpPython())
   print('-------------------------------')
