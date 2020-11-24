# newDir.py
'''
Simple script to create a copy of an ntuple with the TDirectories ak4puppiHLT and ak8puppiHLT
renamed to ak4puppi and ak8puppi preserving the TTree named 't' inside. This allows
the usage of tools in JetMETAnalysis.

This script takes an HLT JRA NTuple (see https://github.com/missirol/JMETriggerAnalysis/tree/phase2) 
as input, and it will output two files, one for each jet type.
ex:

python /path/to/newDir.py /path/to/hlt_jra_ntuple.root
'''
import ROOT
import argparse

parser = argparse.ArgumentParser(description='Change TDirectory name.')
parser.add_argument('infile', metavar='f', type=str,help='root file name')
args = parser.parse_args()
f_name = args.infile
print "creating new file from "+f_name+" with TDirectory named ak4puppi"
#
# Open JRA ntuple file and get TTree 
#
infile = ROOT.TFile(f_name)
t = infile.Get('ak4puppiHLT/t')
#
# Open output file for ak4 jets, create new TDirecotry,
# clone TTree, and close file
#
outfile = ROOT.TFile('ak4puppi.root','RECREATE')
outfile.mkdir("ak4puppi")
outfile.cd("ak4puppi")
newt = t.CloneTree()
outfile.Write()
outfile.Close()
#
# Open output file for ak8 jets, create new TDirecotry,
# clone TTree, and close file
#
print "creating new file from "+f_name+" with TDirectory named ak8puppi"
ot = infile.Get('ak8puppiHLT/t')
ofile = ROOT.TFile('ak8puppi.root','RECREATE')
ofile.mkdir("ak8puppi")
ofile.cd("ak8puppi")
newot = ot.CloneTree()
ofile.Write()
ofile.Close()
#
# Close JRA ntuple file
#
infile.Close()


