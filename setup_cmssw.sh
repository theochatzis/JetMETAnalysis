#!/bin/bash

#
# recipe to set up local CMSSW area
#
# Notes:
#  - do not use aliases (e.g. cmsrel, cmsenv),
#    so that the recipe can also work in non-interactive shells
#  - do not compile with scram inside this script
#

scram project CMSSW_12_0_0_pre4
cd CMSSW_12_0_0_pre4/src
eval `scram runtime -sh`
git cms-addpkg HLTrigger/Configuration
git cms-addpkg CommonTools/RecoAlgos
git cms-remote add mmasciov
git fetch mmasciov
git diff a0c27eab5ee^^ a0c27eab5ee | git apply
