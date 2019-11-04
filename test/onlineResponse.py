import ROOT
from DataFormats.FWLite import Events, Handle
import math
import array

def deltaPhi(phi1, phi2):
     PHI = abs(phi1-phi2)
     if (PHI<=3.14159265):
         return PHI
     else:        
         return 2*3.14159265-PHI

def deltaR(eta1, phi1, eta2, phi2) :
    deta = eta1-eta2
    dphi = deltaPhi(phi1,phi2)
    return math.sqrt(deta*deta + dphi*dphi)




#xbin = [10,15,18,20,22,25,30,35,40,45,50,60,75,100,160]
xbin = [5,10,15,17,18,19,20,25,30,35,40,45,50,55,60,80,100,150,200]
xbins = array.array('d',xbin)
jetType = "Puppi"#empty or "Corrected" or CHS or CHSCorrected or Puppi for offline

def histograms(fileName):
     events = Events(fileName)
     HLTJetHandle = Handle('std::vector<reco::PFJet>')
     GenJetHandle = Handle('std::vector<reco::GenJet>')
     deltaRMin = ROOT.TH1F("deltaRMin","",100,0.,1.0)
     
     
     
     #eta_thresholds = [0]
     #color={0:ROOT.kBlack, 1.3:ROOT.kBlue, 2.5:ROOT.kRed, 3:ROOT.kMagenta}
     eta_thresholds = [0.0,1.0] # you can put here whatever interval you wish
     resp = {}
     thresholds = [10**(x/10.) for x in range(10,25)]
     respvseta = ROOT.TProfile("responsevseta", "", 20, -5.,5.,0.1,1.5)
     for eta_th in eta_thresholds:
         resp[eta_th] = ROOT.TProfile("response", "response", len(thresholds)-1, array.array('d', thresholds) )
         resp[eta_th].SetName("response "+str(eta_th))
         
     for event in events:
          event.getByLabel(("ak4GenJets"), GenJetHandle)        
          genJets = GenJetHandle.product()
          event.getByLabel(("ak4PFJetsCHSCorrected"),HLTJetHandle)
          l2Jets = HLTJetHandle.product()
          for genJet in genJets:  
               if  genJet.pt() < 10: continue
               deltaR_min = 0.4
               jetEt = -1000
               for jet in l2Jets:
                    deltar = deltaR(genJet.eta(), genJet.phi(), jet.eta(),jet.phi()) 
                    if deltar < deltaR_min:
                         deltaR_min = deltar
                         jetEt = jet.et()
               deltaRMin.Fill(deltaR_min)
               if jetEt < -20: continue
               if abs(genJet.eta()) > eta_thresholds[0] and abs(genJet.eta()) < eta_thresholds[1]:
                         resp[eta_thresholds[0]].Fill(genJet.et(), jetEt / (genJet.et()))
               respvseta.Fill(genJet.eta(), jetEt / (genJet.et()) )

                              

     c1 = ROOT.TCanvas()
     resp[eta_thresholds[0]].Draw()
     c1.SaveAs("pippo"+str(eta_thresholds[0])+jetType+".png")
          
     c2=ROOT.TCanvas()
     deltaRMin.Draw()
     c2.SaveAs("deltaR_"+jetType+".png")
     respvseta.GetYaxis().SetRangeUser(0.1,1.5)
     respvseta.Draw()
     c2.SaveAs("resVsEta_"+jetType+".png")

     mylist = [deltaRMin, respvseta] 
     mylist.append(resp[eta_thresholds[0]])
     return mylist


# just to avoid opening windows
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)



#file = "root://xrootd-cms.infn.it//store/mc/PhaseIITDRSpring19DR/QCD_Pt-15to3000_EMEnriched_TuneCP5_13TeV_pythia8/AODSIM/PU200_106X_upgrade2023_realistic_v3-v1/50000/7B3A058C-0CE2-1343-8304-D3EADE243D5E.root"
file = "hltoutput_hlt.root"

myhistos = histograms(file)
newfile = ROOT.TFile("jets.root","RECREATE")
for i in range(len(myhistos)):
     myhistos[i].Write()
newfile.Close()     
