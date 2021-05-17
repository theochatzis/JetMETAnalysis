This directory contains tools and instructions
to derive Jet Energy Scale Corrections
for the jets used in the High-Level Trigger (HLT).

#### Setup

Instructions to set up the CMSSW area to produce JRA NTuples, and derive JESCs:
```
scram p CMSSW CMSSW_11_2_0_Patatrack
cd CMSSW_11_2_0_Patatrack/src
eval `scram runtime -sh`
git cms-init
git clone https://github.com/missirol/JetMETAnalysis.git -o missirol -b devel_hlt2
git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b run3
scram b -j 8
```

#### Produce JRA NTuples with HLT Jets

 * How to run the JRA step locally and with crab
 * Which samples to use, how to find them in DAS
 * What to do if a sample is not available at a Tier-2 (transfer request, Rucio rule)

#### Derive Jet Energy Scale Corrections from JRA NTuples

Once JRA NTuples have been produced,
JESCs can be derived from them by running
the executables of the `JetMETAnalysis` package.

An example of how to do this is given below:
```
cd ${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/
./fitJESCs -o output_tmp1 -n -1
```
The `fitJESCs` script is an example of
a wrapper executing the various steps of the JESCs derivation
(caveat: the script presently includes several hard-coded parameters).

##### To derive `preliminary_jecs_may`

The JRA NTuples used for these corrections can be found here:

```
/eos/cms/store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/npv_fix_noPU/npvFix_noPU.root
/eos/cms/store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/npv_fix_flatPU/npvFix_flatPU.root
```

This preliminary jecs were derived with the following parameters for the L1 and L2 fits (which can be found within the `fitJECs` wrapper script)
for all jet types excep for `ak8puppiHLT`:

```bash
# For L1 Fit
jet_synchfit_x__hlt -algo1 <jet-type> -algo2 ak4caloHLT -functionType standard  -era Run3Winter20_V2_MC -inputDir ./ -outputDir ./
...
# For L2 Fit
jet_l2_correction_x -algs <jet-type> -era Run3Winter20_V2_MC -l2l3 true -input plots_step04/histogram_<jet-type>l1_step04.root -outputDir ./ -output l2p3.root -makeCanvasVariable AbsCorVsJetPt:JetEta -batch true -histMet median -l2pffit standard+gaussian -maxFitIter 50 -ptclipfit true
```

For `ak8puppiHLT` only the L2 correction was applied, with the following parameters:

```bash
jet_l2_correction_x -algs ak8puppiHLT -era Run3Winter20_V2_MC -l2l3 true -input plots_step01/histogram_ak8puppiHLTl1_step01.root -outputDir ./ -output l2p3.root -makeCanvasVariable AbsCorVsJetPt:JetEta -batch true -histMet median -l2pffit standard+Gaussian -maxFitIter 50 -ptclipfit false
```

