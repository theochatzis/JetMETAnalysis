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

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT_TRKv06p1_TICL',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining reconstruction methods for JME inputs')

opts.register('txtFilesPrefix', '',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'common part of paths to JESC .txt files')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

opts.parseArguments()

###
### base configuration file
###
opt_reco = opts.reco

if opt_reco == 'HLT_TRKv00':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv00_cfg import cms, process

elif opt_reco == 'HLT_TRKv00_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv00_TICL_cfg import cms, process

elif opt_reco == 'HLT_TRKv02':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv02_cfg import cms, process

elif opt_reco == 'HLT_TRKv02_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv02_TICL_cfg import cms, process

elif opt_reco == 'HLT_TRKv06':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06_cfg import cms, process

elif opt_reco == 'HLT_TRKv06_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06_TICL_cfg import cms, process

elif opt_reco == 'HLT_TRKv06p1':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p1_cfg import cms, process

elif opt_reco == 'HLT_TRKv06p1_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p1_TICL_cfg import cms, process

elif opt_reco == 'HLT_TRKv06p3':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p3_cfg import cms, process

elif opt_reco == 'HLT_TRKv06p3_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p3_TICL_cfg import cms, process

elif opt_reco == 'HLT_TRKv07p2':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv07p2_cfg import cms, process

elif opt_reco == 'HLT_TRKv07p2_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv07p2_TICL_cfg import cms, process

else:
  raise RuntimeError('invalid argument for option "reco": "'+opt_reco+'"')

###
### GlobalTag
###
# update process.GlobalTag.globaltag
if opts.globalTag is not None:
   from Configuration.AlCa.GlobalTag import GlobalTag
   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

# fix for AK4PF Phase-2 JECs
process.GlobalTag.toGet.append(cms.PSet(
  record = cms.string('JetCorrectionsRecord'),
  tag = cms.string('JetCorrectorParametersCollection_PhaseIIFall17_V5b_MC_AK4PF'),
  label = cms.untracked.string('AK4PF'),
))

from CondCore.CondDB.CondDB_cfi import CondDB as _CondDB
process.jescESSource = cms.ESSource('PoolDBESSource',
  _CondDB.clone(connect = 'sqlite_file:/afs/cern.ch/work/m/missirol/public/phase2/JESC/Phase2HLTTDR_V5_MC/Phase2HLTTDR_V5_MC.db'),
  toGet = cms.VPSet(
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Phase2HLTTDR_V5_MC_AK4PFPuppiHLT'),
      label = cms.untracked.string('AK4PFPuppiHLT')
    ),
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Phase2HLTTDR_V5_MC_AK8PFPuppiHLT'),
      label = cms.untracked.string('AK8PFPuppiHLT')
    ),
  ),
)
process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

###
### JESC analyzers
###
import os
process.hltJESCAnalysisSeq = cms.Sequence()

for [rawJetsMod, jetCorrMod, jecAlgo] in [
  ['hltAK4PFPuppiJets', 'hltAK4PFPuppiJetCorrector', 'AK4PFPuppiHLT'],
  ['hltAK8PFPuppiJets', 'hltAK8PFPuppiJetCorrector', 'AK8PFPuppiHLT'],
]:
  if hasattr(process, rawJetsMod+'JESCAnalyzer'):
    raise RuntimeError('module "'+rawJetsMod+'JESCAnalyzer" already exists')

  for _tmp in getattr(process, jetCorrMod).correctors:
    getattr(process, _tmp).algorithm = jecAlgo

  _txtFiles = []
  for _tmp in [
    'L1FastJet',
    'L2Relative',
    'L3Absolute',
  ]:
    _txtFile = opts.txtFilesPrefix+_tmp+'_'+jecAlgo+'.txt'
    if not os.path.isfile(_txtFile):
      raise RuntimeError('target .txt file not found: '+_txtFile)
    _txtFiles.append(os.path.relpath(os.path.abspath(_txtFile), os.environ['CMSSW_BASE']+'/src'))

  setattr(process, rawJetsMod+'JESCAnalyzer', cms.EDAnalyzer('CorrectedPFJetAnalyzer',
    src = cms.InputTag(rawJetsMod),
    correctors = cms.VInputTag(jetCorrMod),
    textFiles = cms.vstring(_txtFiles),
    useRho = cms.bool(True),
    rho = cms.InputTag('fixedGridRhoFastjetAllTmp'),
    verbose = cms.bool(True),
  ))

  process.hltJESCAnalysisSeq += getattr(process, rawJetsMod+'JESCAnalyzer')

process.hltJESCAnalysisEndPath = cms.EndPath(process.hltJESCAnalysisSeq)
process.setSchedule_(cms.Schedule(process.MC_JME, process.hltJESCAnalysisEndPath))
process.prune()

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# EDM Input Files
if opts.inputFiles and opts.secondaryInputFiles:
   process.source.fileNames = opts.inputFiles
   process.source.secondaryFileNames = opts.secondaryInputFiles
elif opts.inputFiles:
   process.source.fileNames = opts.inputFiles
   process.source.secondaryFileNames = []
else:
   process.source.fileNames = [
     '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v2/280000/015FB6F1-59B4-304C-B540-2392A983A97D.root',
   ]
   process.source.secondaryFileNames = []

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())
