#!/bin/bash

#
# recipe to set up local CMSSW area
#
# Notes:
#  - do not use aliases (e.g. cmsrel, cmsenv),
#    so that the recipe can also work in non-interactive shells
#  - do not compile with scram inside this script
#

scram project CMSSW_11_2_0_Patatrack
cd CMSSW_11_2_0_Patatrack/src
eval `scram runtime -sh`

git cms-merge-topic missirol:devel_1120pa_kineParticleFilter -u
git cms-merge-topic missirol:devel_puppiPUProxy_1120patatrack -u
git cms-merge-topic mmasciov:tracking-allPVs -u
