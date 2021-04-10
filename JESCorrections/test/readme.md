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
git clone https://github.com/missirol/JetMETAnalysis.git -o missirol -b devel_hlt
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
