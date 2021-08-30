# Event filters and variable definitions done by Vilja. Focus on the cuts that happens on Jets.

# This is the original version and untouched by me. That's why it's not commented but I think the line are quite clear.
# I recommend using the viljaFiltered_SalomaaMod.py since it's the most suitable for this coding project.

def filtersAndcuts(df,nall,xsec):
        fj_cuts = 'FatJet_pt > 400 && abs(FatJet_eta) < 2.4 && FatJet_jetId & 2'
        df1 = df.Filter("nFatJet >= 2", "Events with >=2 AK8 jets")\
                .Filter('FatJet_pt[0] > 350','Preselection of subleading jet pt')\
                .Filter('FatJet_pt[1] > 300','Preselection of leading jet pt')\
                .Define('passTrigger','HLT_AK8PFHT800_TrimMass50 || HLT_PFHT1050 || HLT_AK8PFJet400_TrimMass30 || HLT_AK8PFJet500 || HLT_PFJet500')\
                .Filter('passTrigger == 1','Events passing at least one trigger')

#GoodFatJets pt
        df2 = df1.Define('GoodFatJet_pt','FatJet_pt[%s]'%fj_cuts)\
                .Filter("Sum(GoodFatJet_pt > 400.0)>=2", "Events with >=2 good AK8 jets with pT > 400 GeV")\
                .Filter("Sum(GoodFatJet_pt > 500.0)>0", "Events with >0 good AK8 jets with pT > 500 GeV")\
                .Define("GoodFatJetPtLeading", "GoodFatJet_pt[0]")

#GFJ DeltaEta
        dfe = df2.Define("GoodFatJet_eta","FatJet_eta[%s]"%fj_cuts)
        dfde = dfe.Define("GoodFatJetDeltaEta",'abs(GoodFatJet_eta[0]-GoodFatJet_eta[1])')
        dfde_filter = dfde.Filter('GoodFatJetDeltaEta < 2.0', 'Events with >=2 good AK8 jets with deltaEta < 2.0')

#GFJ DeltaPhi
        dfp = dfde_filter.Define("GoodFatJet_phi","FatJet_phi[%s]"%fj_cuts)
        dfdp = dfp.Define("GoodFatJetDeltaPhi",'ROOT::VecOps::DeltaPhi(GoodFatJet_phi[0],GoodFatJet_phi[1])')
        dfdp_filter = dfdp.Filter('abs(GoodFatJetDeltaPhi) > 2.6', 'Events with >=2 good AK8 jets with deltaPhi > 2.6')

#GoodFatJets mass
#       df21 = dfdp_filter.Define('GoodFatJet_m','FatJet_mass[%s]'%fj_cuts)
#       df21_cut_ak8m = df21.Filter("Sum(GoodFatJet_m > 100.0)>=2", "Events with >=2 good AK8 jets with m > 100 GeV")
#       df21_cut_leadingak8m = df21_cut_ak8m.Filter("Sum(GoodFatJet_m > 110.0)>0", "Events with >0 good AK8 jets with m > 110 GeV")
#       df21_define_leadingak8m = df21_cut_leadingak8m.Define("GoodFatJetMLeading", "GoodFatJet_m[0]")

#GoodFatJets msoftdrop
        df22 = dfdp_filter.Define('GoodFatJet_ms','FatJet_msoftdrop[%s]'%fj_cuts)
        df22_cut_ak8ms = df22.Filter("GoodFatJet_ms[1] > 100.0 && GoodFatJet_ms[1] < 145.0", "Events with >=2 good AK8 jets with 145 > ms > 100 GeV")
        df22_cut_leadingak8ms = df22_cut_ak8ms.Filter("GoodFatJet_ms[0] > 110.0 && GoodFatJet_ms[0] < 150.0", "Events with >0 good AK8 jets with 150 > ms > 110 GeV")
        df22_define_leadingak8ms = df22_cut_leadingak8ms.Define("GoodFatJetMsLeading", "GoodFatJet_ms[0]")

        df22_final = df22_define_leadingak8ms

#XbbVsQCD 
        dfx = df22_final.Define('FatJet_ParticleNetMD_probQCD','FatJet_ParticleNetMD_probQCDb + FatJet_ParticleNetMD_probQCDbb + FatJet_ParticleNetMD_probQCDc + FatJet_ParticleNetMD_probQCDcc + FatJet_ParticleNetMD_probQCDothers')\
                .Define('FatJet_ParticleNetMD_XbbVsQCD','FatJet_ParticleNetMD_probXbb/(FatJet_ParticleNetMD_probXbb+FatJet_ParticleNetMD_probQCD)')
        dfx2 = dfx.Define('GoodFatJet_ParticleNetMD_XbbVsQCD','FatJet_ParticleNetMD_XbbVsQCD[%s]'%fj_cuts)
        dfx_cut = dfx2.Filter('GoodFatJet_ParticleNetMD_XbbVsQCD[1] > 0.9', 'Events with >= 2 good AK8 Jets with XbbVsQCD > 0.9')
        dfx_cut_leading = dfx_cut.Filter('GoodFatJet_ParticleNetMD_XbbVsQCD[0] > 0.9', 'Events with > 0 good AK8 Jets with XbbVsQCD > 0.9')
        dfx_define_leadingXbb = dfx_cut_leading.Define('GoodFatJetXbbVsQCDLeading','GoodFatJet_ParticleNetMD_XbbVsQCD[0]')

#AK4 Jets
        df10 = dfx_define_leadingXbb.Filter("nJet >= 2", "Events with >=2 AK4 jets")
        gj_cuts = 'Jet_pt > 25 && abs(Jet_eta) < 4.7 && Jet_jetId & 2 && (Jet_puId & 2 or Jet_pt > 50.0)'

#GoodJets pt
        df23 = df10.Define('GoodJet_pt','Jet_pt[%s]'%gj_cuts)
        df2_define_leadingak4pt = df23.Define("GoodJetPtLeading", "GoodJet_pt[0]")
#nGoodJet
        df23n = df2_define_leadingak4pt.Define('nGoodJet','GoodJet_pt.size()')

#GJ Eta
        dfe1 = df23n.Define("GoodJet_eta","Jet_eta[%s]"%gj_cuts)\
                .Define('GoodJet_mass','Jet_mass[%s]'%gj_cuts)
        dfde1 = dfe1.Define("GoodJetDeltaEta",'abs(GoodJet_eta[0]-GoodJet_eta[1])')

#GJ Phi
        dfp1 = dfde1.Define("GoodJet_phi","Jet_phi[%s]"%gj_cuts)
        dfdp1 = dfp1.Define("GoodJetDeltaPhi",'ROOT::VecOps::DeltaPhi(GoodJet_phi[0],GoodJet_phi[1])')

        dfdp1_final = dfdp1

#GoodElectron pt
        dfe2 = dfdp1_final.Define('GoodElectron_pt','Electron_pt[Electron_pt > 10 && abs(Electron_eta) < 2.5 && abs(Electron_dxy) < 0.05 && abs(Electron_dz) < 0.2 && Electron_mvaFall17V2noIso_WPL && Electron_miniPFRelIso_all < 0.4]')
#nGoodElectron
        dfe25 = dfe2.Define('nGoodElectron','GoodElectron_pt.size()')
        dfe3 = dfe25.Filter('nGoodElectron == 0', 'Events with 0 good electrons')

#GoodMuon pt
        dfm2 = dfe3.Define('GoodMuon_pt','Muon_pt[Muon_pt > 10 && abs(Muon_eta) < 2.4 && abs(Muon_dxy) < 0.05 && abs(Muon_dz) < 0.2 && Muon_looseId && Muon_miniPFRelIso_all < 0.4]')
#nGoodMuon
        dfm25 = dfm2.Define('nGoodMuon','GoodMuon_pt.size()')
        dfm3 = dfm25.Filter('nGoodMuon == 0','Events with 0 good muons')

        dfm_final = dfm3

#HiggsCandidates
        dfh = dfm3.Define('HiggsCandidate_pt','ROOT::VecOps::Take(GoodFatJet_pt,{0,1})')
#nHiggs
        dfhn = dfh.Define('nHiggsCandidate','HiggsCandidate_pt.size()')
#HiggsPhi
        dfhp = dfhn.Define('HiggsCandidate_phi','ROOT::VecOps::Take(GoodFatJet_phi,{0,1})')
#HiggsEta
        dfhe = dfhp.Define('HiggsCandidate_eta','ROOT::VecOps::Take(GoodFatJet_eta,{0,1})')\
                .Define('nHiggsCandidatephi','HiggsCandidate_phi.size()')\
                .Define('HiggsCandidate_mass','ROOT::VecOps::Take(GoodFatJet_ms,{0,1})')

        dfr = dfhe.Filter("nHiggsCandidate == 2", "Double-check that we have exactly two Higgs candidates")\
                .Filter("nGoodJet >0", "Double-check that we have at last one GoodJet")\
                .Define("GoodJet_closestHiggsCandidateIdx","FindClosest(GoodJet_phi,GoodJet_eta,HiggsCandidate_phi,HiggsCandidate_eta)")\
                .Define("GoodJet_closestHiggsCandidateEta", "Take(HiggsCandidate_eta, GoodJet_closestHiggsCandidateIdx)")\
                .Define("GoodJet_closestHiggsCandidatePhi", "Take(HiggsCandidate_phi, GoodJet_closestHiggsCandidateIdx)")\
                .Define("GoodJet_closestHiggsCandidateDeltaR", "ROOT::VecOps::DeltaR(GoodJet_eta,GoodJet_closestHiggsCandidateEta,GoodJet_phi,GoodJet_closestHiggsCandidatePhi)") # For each GoodJet, calculate the DeltaR distance w.r.t. the closest HiggsCandidate
        dfr0 = dfr.Define('GoodJet_closestHiggsCandidateDeltaRL','GoodJet_closestHiggsCandidateDeltaR[0]')\
                .Define('nGoodJet_closestHiggsCandidatePhi','GoodJet_closestHiggsCandidatePhi.size()')

        dfc0 = dfr0.Define('GoodJet_FatJetCleaned_pt','GoodJet_pt[GoodJet_closestHiggsCandidateDeltaR > 1.2]')\
                .Define('GoodJet_FatJetCleaned_phi','GoodJet_phi[GoodJet_closestHiggsCandidateDeltaR > 1.2]')\
                .Define('GoodJet_FatJetCleaned_eta','GoodJet_eta[GoodJet_closestHiggsCandidateDeltaR > 1.2]')\
                .Define('GoodJet_FatJetCleaned_mass','GoodJet_mass[GoodJet_closestHiggsCandidateDeltaR > 1.2]')
        dfc = dfc0.Define('nGoodJet_FatJetCleaned','GoodJet_FatJetCleaned_pt.size()')

#Muons&ElectronsForCleaning
        mu_cuts = 'Muon_pt > 5 && abs(Muon_eta) < 2.4 && abs(Muon_dxy) < 0.05 && abs(Muon_dz) < 0.2'
        el_cuts = 'Electron_pt > 7 && abs(Electron_eta) < 2.5 && abs(Electron_dxy) < 0.05 && abs(Electron_dz) < 0.2'

        dfmc0 = dfc.Define('MuonsForCleaning_pt','Muon_pt[%s]'%mu_cuts)\
                .Define('MuonsForCleaning_eta','Muon_eta[%s]'%mu_cuts)\
                .Define('MuonsForCleaning_phi','Muon_phi[%s]'%mu_cuts)\
                .Define('nMuonsForCleaning','MuonsForCleaning_eta.size()')

        dfmc = dfmc0.Define('GoodJet_FatJetCleaned_closestMuonDeltaR','FindClosestDeltaR(GoodJet_FatJetCleaned_phi,GoodJet_FatJetCleaned_eta,MuonsForCleaning_phi,MuonsForCleaning_eta)')\
                .Define('nGoodJet_FatJetCleaned_closestMuonDeltaR','GoodJet_FatJetCleaned_closestMuonDeltaR.size()')\
                .Define('GoodJet_FatJetAndMuonCleaned_pt','GoodJet_FatJetCleaned_pt[GoodJet_FatJetCleaned_closestMuonDeltaR > 0.4]')\
                .Define('GoodJet_FatJetAndMuonCleaned_phi','GoodJet_FatJetCleaned_phi[GoodJet_FatJetCleaned_closestMuonDeltaR > 0.4]')\
                .Define('GoodJet_FatJetAndMuonCleaned_eta','GoodJet_FatJetCleaned_eta[GoodJet_FatJetCleaned_closestMuonDeltaR > 0.4]')\
                .Define('GoodJet_FatJetAndMuonCleaned_mass','GoodJet_FatJetCleaned_mass[GoodJet_FatJetCleaned_closestMuonDeltaR > 0.4]')\
                .Define('nGoodJet_FatJetAndMuonCleaned','GoodJet_FatJetAndMuonCleaned_pt.size()')

        dfec = dfmc.Define('ElectronsForCleaning_pt','Electron_pt[%s]'%el_cuts)\
                .Define('ElectronsForCleaning_eta','Electron_eta[%s]'%el_cuts)\
                .Define('ElectronsForCleaning_phi','Electron_phi[%s]'%el_cuts)\
                .Define('nElectronsForCleaning','ElectronsForCleaning_pt.size()')\
                .Define('GoodJet_closestElectronDeltaR','FindClosestDeltaR(GoodJet_FatJetAndMuonCleaned_phi,GoodJet_FatJetAndMuonCleaned_eta,ElectronsForCleaning_phi,ElectronsForCleaning_eta)')

        dflc = dfec.Define('GoodJet_FatJetAndLeptonCleaned_pt','GoodJet_FatJetAndMuonCleaned_pt[GoodJet_closestElectronDeltaR > 0.4]')\
                .Define('GoodJet_FatJetAndLeptonCleaned_phi','GoodJet_FatJetAndMuonCleaned_phi[GoodJet_closestElectronDeltaR > 0.4]')\
                .Define('GoodJet_FatJetAndLeptonCleaned_eta','GoodJet_FatJetAndMuonCleaned_eta[GoodJet_closestElectronDeltaR > 0.4]')\
                .Define('GoodJet_FatJetAndLeptonCleaned_mass','GoodJet_FatJetAndMuonCleaned_mass[GoodJet_closestElectronDeltaR > 0.4]')\
                .Define('nGoodJet_FatJetAndLeptonCleaned','GoodJet_FatJetAndLeptonCleaned_pt.size()')\
                .Filter('nGoodJet_FatJetAndLeptonCleaned >= 2','Events with >= 2 good jets cleaned of fat jets and leptons')
        sum0 = df.Sum('genWeight')

        dfvbf = dflc.Define('VBFCandidates_pt','ROOT::VecOps::Take(GoodJet_FatJetAndLeptonCleaned_pt,{0,1})')\
                .Define('VBFCandidates_phi','ROOT::VecOps::Take(GoodJet_FatJetAndLeptonCleaned_phi,{0,1})')\
                .Define('VBFCandidates_eta','ROOT::VecOps::Take(GoodJet_FatJetAndLeptonCleaned_eta,{0,1})')\
                .Define('VBFCandidates_mass','ROOT::VecOps::Take(GoodJet_FatJetAndLeptonCleaned_mass,{0,1})')\
                .Filter('abs(VBFCandidates_eta[0]) > 1.5 && abs(VBFCandidates_eta[1]) > 1.5','VBF eta > 1.5')\
                .Define('VBFCandidatesDeltaEta','abs(VBFCandidates_eta[0]-VBFCandidates_eta[1])')\
                .Filter('VBFCandidatesDeltaEta > 4.0','VBF jet candidates with DeltaEta > 4.0')\
                .Define('VBFCandidates_mjj','ROOT::VecOps::InvariantMass(VBFCandidates_pt, VBFCandidates_eta, VBFCandidates_phi, VBFCandidates_mass)')\
                .Filter('VBFCandidates_mjj > 500.0','VBF jet candidates with invariant mass > 500')\
                .Define('HiggsCandidate_mjj','ROOT::VecOps::InvariantMass(HiggsCandidate_pt, HiggsCandidate_eta, HiggsCandidate_phi, HiggsCandidate_mass)')\
                .Define('normWeight','%f*59740/%f'%(xsec,nall))\
                .Define('sumgenWeight','%f'%sum0.GetValue())\
                .Define('normgenWeight','genWeight*%f*59740/(sumgenWeight)'%xsec)
        return dfvbf