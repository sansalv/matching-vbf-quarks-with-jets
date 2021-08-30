import ROOT
#******************************************************************************************************
# Mostly variable definitions regarding bGenPart
#******************************************************************************************************
def defbVariables(df):
    # New variable: abs(eta)
    df = df.Define('GenJet_absEta', 'abs(GenJet_eta)')
    #******************************************************************************************************
    # bGenPart variables (using functions defined in bGenPartFunctions.py):
    #------------------------------------------------------------------------------------------------------
    df = df.Define('bestChildren_idxLists',
                   'FindBestChildren_indices(nGenPart, GenPart_pt, GenPart_genPartIdxMother)')
    df = df.Define('bestChildren_indices',
                   'ChooseBestChildren_indices(bestChildren_idxLists, GenPart_eta, GenPart_phi,GenJet_eta, GenJet_phi, GenPart_pdgId)')
    #------------------------------------------------------------------------------------------------------
    # Basic variables:
    df = df.Define('bGenPart_eta', 'Take(GenPart_eta, bestChildren_indices)')\
           .Define('bGenPart_absEta', 'abs(bGenPart_eta)')\
           .Define('bGenPart_phi', 'Take(GenPart_phi, bestChildren_indices)')\
           .Define('bGenPart_pt', 'Take(GenPart_pt, bestChildren_indices)')\
           .Define('bGenPart_mass', 'Take(GenPart_mass, bestChildren_indices)')\
           .Define('bGenPart_mjj', 'InvariantMass(bGenPart_pt, bGenPart_eta, bGenPart_phi, bGenPart_mass)')\
           .Define('bGenPart_pdgId', 'Take(GenPart_pdgId, bestChildren_indices)')
    #******************************************************************************************************
    # c++ function that gives 1 if match is close enough (deltaR < 0.4) and 0 if not
    # This function is not that important. Sometimes it's nice to see or print this matching "status"
    # returns rvec, for example: {0,1}
    
    ROOT.gInterpreter.Declare("""
    
    using namespace ROOT::VecOps;    
        const ROOT::RVec<std::size_t> GiveBinVecOfQuarkStatus(const ROOT::RVec<float>& deltaR){
        
        RVec<std::size_t> binVec(2);
        
        for(std::size_t i=0; i<2; i++) {
            if(deltaR[i] < 0.4){
                binVec[i] = 1;
            }else{
                binVec[i] = 0;
            }
        }
        
        return binVec;
    };
    """)
    #******************************************************************************************************
    # Find closest GenJet (bGenJet) for every bGenPart
    # bGenPart --> bGenJet:
    #------------------------------------------------------------------------------------------------------
    df = df.Define('bGenJet_idx','FindClosest(bGenPart_phi, bGenPart_eta, GenJet_phi, GenJet_eta)')

    df = df.Define('bGenJet_eta', 'Take(GenJet_eta, bGenJet_idx)')\
           .Define('bGenJet_absEta', 'abs(bGenJet_eta)')\
           .Define('bGenJet_phi', 'Take(GenJet_phi, bGenJet_idx)')\
           .Define('bGenJet_pt', 'Take(GenJet_pt, bGenJet_idx)')\
           .Define('bGenJet_mass', 'Take(GenJet_mass, bestChildren_indices)')\
           .Define('bGenJet_mjj', 'InvariantMass(bGenJet_pt, bGenJet_eta, bGenJet_phi, bGenJet_mass)')\
           .Define('bGenJet_deltaR', 'DeltaR(bGenPart_eta, bGenJet_eta, bGenPart_phi, bGenJet_phi)')\
           .Define('bGenJet_deltaR_lowerThan04', 'GiveBinVecOfQuarkStatus(bGenJet_deltaR)')
    #******************************************************************************************************
    # Weak match variables:
    #------------------------------------------------------------------------------------------------------
    a = '[bGenJet_deltaR < 0.4]'
    df = df.Define('bGenPart_eta_weak', 'bGenPart_eta'+a)\
           .Define('bGenPart_absEta_weak', 'abs(bGenPart_eta_weak)')\
           .Define('bGenPart_phi_weak', 'bGenPart_phi'+a)\
           .Define('bGenPart_pt_weak', 'bGenPart_pt'+a)\
           .Define('bGenPart_pdgId_weak', 'bGenPart_pdgId'+a)\
           .Define('bGenJet_eta_weak', 'bGenJet_eta'+a)\
           .Define('bGenJet_absEta_weak', 'abs(bGenJet_eta_weak)')\
           .Define('bGenJet_phi_weak', 'bGenJet_phi'+a)\
           .Define('bGenJet_pt_weak', 'bGenJet_pt'+a)
    #------------------------------------------------------------------------------------------------------
    a = '[bGenJet_deltaR >= 0.4]'
    df = df.Define('bGenPart_eta_noWeak', 'bGenPart_eta'+a)\
           .Define('bGenPart_absEta_noWeak', 'abs(bGenPart_eta_noWeak)')\
           .Define('bGenPart_phi_noWeak', 'bGenPart_phi'+a)\
           .Define('bGenPart_pt_noWeak', 'bGenPart_pt'+a)\
           .Define('bGenPart_pdgId_noWeak', 'bGenPart_pdgId'+a)\
           .Define('bGenJet_eta_noWeak', 'bGenJet_eta'+a)\
           .Define('bGenJet_absEta_noWeak', 'abs(bGenJet_eta_noWeak)')\
           .Define('bGenJet_phi_noWeak', 'bGenJet_phi'+a)\
           .Define('bGenJet_pt_noWeak', 'bGenJet_pt'+a)
    #******************************************************************************************************
    # bGetJet_weak --> bJet:
    #------------------------------------------------------------------------------------------------------
    df = df.Define('bJet_idx','FindClosest(bGenJet_phi_weak, bGenJet_eta_weak, Jet_phi, Jet_eta)')\
           .Define('bJet_eta', 'Take(Jet_eta, bJet_idx)')\
           .Define('bJet_absEta', 'abs(bJet_eta)')\
           .Define('bJet_phi', 'Take(Jet_phi, bJet_idx)')\
           .Define('bJet_pt', 'Take(Jet_pt, bJet_idx)')\
           .Define('bJet_mass', 'Take(Jet_mass, bJet_idx)')\
           .Define('bJet_jetId', 'Take(Jet_jetId, bJet_idx)')\
           .Define('bJet_puId', 'Take(Jet_puId, bJet_idx)')\
           .Define('bJet_mjj', 'InvariantMass(bJet_pt, bJet_eta, bJet_phi, bJet_mass)')\
           .Define('bJet_deltaEta','abs(bJet_eta[0]-bJet_eta[1])')\
           .Define('bJet_closestHiggsCandidateIdx', 'FindClosest(bJet_phi, bJet_eta, HiggsCandidate_phi, HiggsCandidate_eta)')\
           .Define('bJet_closestHiggsCandidateEta', 'Take(HiggsCandidate_eta, bJet_closestHiggsCandidateIdx)')\
           .Define('bJet_closestHiggsCandidatePhi', 'Take(HiggsCandidate_phi, bJet_closestHiggsCandidateIdx)')\
           .Define('bJet_closestHiggsCandidateDeltaR',
                   'DeltaR(bJet_eta, bJet_closestHiggsCandidateEta, bJet_phi, bJet_closestHiggsCandidatePhi)')\
           .Define('bJet_closestMuonDeltaR',
                   'FindClosestDeltaR(bJet_phi, bJet_eta, MuonsForCleaning_phi, MuonsForCleaning_eta)')\
           .Define('bJet_closestElectronDeltaR',
                   'FindClosestDeltaR(bJet_phi, bJet_eta, ElectronsForCleaning_phi, ElectronsForCleaning_eta)')\
           .Define('bJet_deltaR', 'DeltaR(bGenJet_eta_weak, bJet_eta, bGenJet_phi_weak, bJet_phi)')\
           .Define('bJet_deltaR_lowerThan04', 'GiveBinVecOfQuarkStatus(bJet_deltaR)')

    df = df.Define('bJet_idx_all','FindClosest(bGenJet_phi, bGenJet_eta, Jet_phi, Jet_eta)')\
           .Define('bJet_eta_all', 'Take(Jet_eta, bJet_idx_all)')\
           .Define('bJet_phi_all', 'Take(Jet_phi, bJet_idx_all)')\
           .Define('bJet_deltaR_all', 'DeltaR(bGenJet_eta, bJet_eta_all, bGenJet_phi, bJet_phi_all)')
    #******************************************************************************************************
    # Strong match variables:
    #------------------------------------------------------------------------------------------------------
    a = '[bJet_deltaR < 0.4]'
    df = df.Define('bGenPart_eta_strong', 'bGenPart_eta_weak'+a)\
           .Define('bGenPart_absEta_strong', 'abs(bGenPart_eta_strong)')\
           .Define('bGenPart_phi_strong', 'bGenPart_phi_weak'+a)\
           .Define('bGenPart_pt_strong', 'bGenPart_pt_weak'+a)\
           .Define('bGenJet_eta_strong', 'bGenJet_eta_weak'+a)\
           .Define('bGenJet_absEta_strong', 'abs(bGenJet_eta_strong)')\
           .Define('bGenJet_phi_strong', 'bGenJet_phi_weak'+a)\
           .Define('bGenJet_pt_strong', 'bGenJet_pt_weak'+a)\
           .Define('bJet_eta_strong', 'bJet_eta'+a)\
           .Define('bJet_absEta_strong', 'abs(bJet_eta_strong)')\
           .Define('bJet_phi_strong', 'bJet_phi'+a)\
           .Define('bJet_pt_strong', 'bJet_pt'+a)
    #------------------------------------------------------------------------------------------------------
    a = '[bJet_deltaR >= 0.4]'
    df = df.Define('bGenPart_eta_noStrong', 'bGenPart_eta_weak'+a)\
           .Define('bGenPart_absEta_noStrong', 'abs(bGenPart_eta_noStrong)')\
           .Define('bGenPart_phi_noStrong', 'bGenPart_phi_weak'+a)\
           .Define('bGenPart_pt_noStrong', 'bGenPart_pt_weak'+a)\
           .Define('bGenJet_eta_noStrong', 'bGenJet_eta_weak'+a)\
           .Define('bGenJet_absEta_noStrong', 'abs(bGenJet_eta_noStrong)')\
           .Define('bGenJet_phi_noStrong', 'bGenJet_phi_weak'+a)\
           .Define('bGenJet_pt_noStrong', 'bGenJet_pt_weak'+a)\
           .Define('bJet_eta_noStrong', 'bJet_eta'+a)\
           .Define('bJet_absEta_noStrong', 'abs(bJet_eta_noStrong)')\
           .Define('bJet_phi_noStrong', 'bJet_phi'+a)\
           .Define('bJet_pt_noStrong', 'bJet_pt'+a)
    #******************************************************************************************************
    # Separate variables for Q1 and Q2:
    #------------------------------------------------------------------------------------------------------
    # eta
    df = df.Define('bGenPart_eta_0', 'bGenPart_eta[0]')\
           .Define('bGenPart_eta_1', 'bGenPart_eta[1]')\
           .Define('bGenJet_eta_0', 'bGenJet_eta[0]')\
           .Define('bGenJet_eta_1', 'bGenJet_eta[1]')\
           .Define('bJet_eta_0', 'bJet_eta[0]')\
           .Define('bJet_eta_1', 'bJet_eta[1]')
    # abs(eta)
    df = df.Define('bGenPart_absEta_0', 'abs(bGenPart_eta[0])')\
           .Define('bGenPart_absEta_1', 'abs(bGenPart_eta[1])')\
           .Define('bGenJet_absEta_0', 'abs(bGenJet_eta[0])')\
           .Define('bGenJet_absEta_1', 'abs(bGenJet_eta[1])')\
           .Define('bJet_absEta_0', 'abs(bJet_eta[0])')\
           .Define('bJet_absEta_1', 'abs(bJet_eta[1])')
    # phi
    df = df.Define('bGenPart_phi_0', 'bGenPart_phi[0]')\
           .Define('bGenPart_phi_1', 'bGenPart_phi[1]')\
           .Define('bGenJet_phi_0', 'bGenJet_phi[0]')\
           .Define('bGenJet_phi_1', 'bGenJet_phi[1]')\
           .Define('bJet_phi_0', 'bJet_phi[0]')\
           .Define('bJet_phi_1', 'bJet_phi[1]')
    # pt
    df = df.Define('bGenPart_pt_0', 'bGenPart_pt[0]')\
           .Define('bGenPart_pt_1', 'bGenPart_pt[1]')\
           .Define('bGenJet_pt_0', 'bGenJet_pt[0]')\
           .Define('bGenJet_pt_1', 'bGenJet_pt[1]')\
           .Define('bJet_pt_0', 'bJet_pt[0]')\
           .Define('bJet_pt_1', 'bJet_pt[1]')
    #******************************************************************************************************
    # Number of matched quarks (0-2)
    #------------------------------------------------------------------------------------------------------
    df = df.Define('nB','bGenPart_phi.size()')\
           .Define('nB_weak','bGenPart_phi_weak.size()')\
           .Define('nB_strong','bGenPart_phi_strong.size()')\
           .Define('nB_etaDetectable', 'Sum(bGenPart_absEta < 5.1 && bGenJet_absEta < 5.1)')\
           .Define('nB_etaDetectable_weak', 'Sum(bGenPart_absEta < 5.1 && bGenJet_absEta < 5.1 && bGenJet_deltaR < 0.4)')\
           .Define('nB_etaDetectable_strong', 'Sum(bGenPart_absEta < 5.1 && bGenJet_absEta < 5.1 && bGenJet_deltaR < 0.4 && bJet_deltaR_all < 0.4)')\
           .Define('nB_GenJetDetectable', 'Sum(bGenPart_pt > 10)')\
           .Define('nB_GenJetDetectable_weak', 'Sum(bGenPart_pt > 10 && bGenJet_deltaR < 0.4)')\
           .Define('nB_GenJetDetectable_strong', 'Sum(bGenPart_pt > 10 && bGenJet_deltaR < 0.4 && bJet_deltaR_all < 0.4)')\
           .Define('nB_JetDetectable', 'Sum(bGenPart_pt > 10 && bGenJet_pt > 15 && bGenPart_absEta < 5.1 && bGenJet_absEta < 5.1)')\
           .Define('nB_JetDetectable_weak', 'Sum(bGenPart_pt > 10 && bGenJet_pt > 15 && bGenPart_absEta < 5.1 && bGenJet_absEta < 5.1 && bGenJet_deltaR < 0.4)')\
           .Define('nB_JetDetectable_strong', 'Sum(bGenPart_pt > 10 && bGenJet_pt > 15 && bGenPart_absEta < 5.1 && bGenJet_absEta < 5.1 && bGenJet_deltaR < 0.4 && bJet_deltaR_all < 0.4)')
    #******************************************************************************************************
    # Delta variables (for comparing variables in different matchings):
    #******************************************************************************************************
    # 'etaDiff'
    #------------------------------------------------------------------------------------------------------
    df = df.Define('etaDiff_bGenJet_bGenPart', 'bGenJet_eta-bGenPart_eta')\
           .Define('etaDiff_bGenJet_bGenPart_weak', 'bGenJet_eta_weak-bGenPart_eta_weak')\
           .Define('etaDiff_bGenJet_bGenPart_strong', 'bGenJet_eta_strong-bGenPart_eta_strong')\
           .Define('etaDiff_bJet_bGenJet_weak', 'bJet_eta-bGenJet_eta_weak')\
           .Define('etaDiff_bJet_bGenJet_strong', 'bJet_eta_strong-bGenJet_eta_strong')\
           .Define('etaDiff_bJet_bGenPart_weak', 'bJet_eta-bGenPart_eta_weak')\
           .Define('etaDiff_bJet_bGenPart_strong', 'bJet_eta_strong-bGenPart_eta_strong')
    #******************************************************************************************************
    # 'etaAbsDiff'
    #------------------------------------------------------------------------------------------------------
    df = df.Define('etaAbsDiff_bGenJet_bGenPart', 'abs(etaDiff_bGenJet_bGenPart)')\
           .Define('etaAbsDiff_bGenJet_bGenPart_weak', 'abs(etaDiff_bGenJet_bGenPart_weak)')\
           .Define('etaAbsDiff_bGenJet_bGenPart_strong', 'abs(etaDiff_bGenJet_bGenPart_strong)')\
           .Define('etaAbsDiff_bJet_bGenJet_weak', 'abs(etaDiff_bJet_bGenJet_weak)')\
           .Define('etaAbsDiff_bJet_bGenJet_strong', 'abs(etaDiff_bJet_bGenJet_strong)')\
           .Define('etaAbsDiff_bJet_bGenPart_weak', 'abs(etaDiff_bJet_bGenPart_weak)')\
           .Define('etaAbsDiff_bJet_bGenPart_strong', 'abs(etaDiff_bJet_bGenPart_strong)')
    #******************************************************************************************************
    # 'phiDiff' with DeltaPhi()
    #------------------------------------------------------------------------------------------------------
    df = df.Define('phiDiff_bGenJet_bGenPart', 'DeltaPhi(bGenJet_phi, bGenPart_phi)')\
           .Define('phiDiff_bGenJet_bGenPart_weak', 'DeltaPhi(bGenJet_phi_weak, bGenPart_phi_weak)')\
           .Define('phiDiff_bGenJet_bGenPart_strong', 'DeltaPhi(bGenJet_phi_strong, bGenPart_phi_strong)')\
           .Define('phiDiff_bJet_bGenJet_weak', 'DeltaPhi(bJet_phi, bGenJet_phi_weak)')\
           .Define('phiDiff_bJet_bGenJet_strong', 'DeltaPhi(bJet_phi_strong, bGenJet_phi_strong)')\
           .Define('phiDiff_bJet_bGenPart_weak', 'DeltaPhi(bJet_phi, bGenPart_phi_weak)')\
           .Define('phiDiff_bJet_bGenPart_strong', 'DeltaPhi(bJet_phi_strong, bGenPart_phi_strong)')
    #******************************************************************************************************
    # 'phiAbsDiff' with |DeltaPhi()|
    #------------------------------------------------------------------------------------------------------
    df = df.Define('phiAbsDiff_bGenJet_bGenPart', 'abs(phiDiff_bGenJet_bGenPart)')\
           .Define('phiAbsDiff_bGenJet_bGenPart_weak', 'abs(phiDiff_bGenJet_bGenPart_weak)')\
           .Define('phiAbsDiff_bGenJet_bGenPart_strong', 'abs(phiDiff_bGenJet_bGenPart_strong)')\
           .Define('phiAbsDiff_bJet_bGenJet_weak', 'abs(phiDiff_bJet_bGenJet_weak)')\
           .Define('phiAbsDiff_bJet_bGenJet_strong', 'abs(phiDiff_bJet_bGenJet_strong)')\
           .Define('phiAbsDiff_bJet_bGenPart_weak', 'abs(phiDiff_bJet_bGenPart_weak)')\
           .Define('phiAbsDiff_bJet_bGenPart_strong', 'abs(phiDiff_bJet_bGenPart_strong)')
    #******************************************************************************************************
    # 'ptDiff'
    #------------------------------------------------------------------------------------------------------
    df = df.Define('ptDiff_bGenJet_bGenPart', 'bGenJet_pt-bGenPart_pt')\
           .Define('ptDiff_bGenJet_bGenPart_weak', 'bGenJet_pt_weak-bGenPart_pt_weak')\
           .Define('ptDiff_bGenJet_bGenPart_strong', 'bGenJet_pt_strong-bGenPart_pt_strong')\
           .Define('ptDiff_bJet_bGenJet_weak', 'bJet_pt-bGenJet_pt_weak')\
           .Define('ptDiff_bJet_bGenJet_strong', 'bJet_pt_strong-bGenJet_pt_strong')\
           .Define('ptDiff_bJet_bGenPart_weak', 'bJet_pt-bGenPart_pt_weak')\
           .Define('ptDiff_bJet_bGenPart_strong', 'bJet_pt_strong-bGenPart_pt_strong')
    #******************************************************************************************************
    # 'ptRelDiff'
    #------------------------------------------------------------------------------------------------------
    df = df.Define('ptRelDiff_bGenJet_bGenPart', 'ptDiff_bGenJet_bGenPart/bGenPart_pt')\
           .Define('ptRelDiff_bGenJet_bGenPart_weak', 'ptDiff_bGenJet_bGenPart_weak/bGenPart_pt_weak')\
           .Define('ptRelDiff_bGenJet_bGenPart_strong', 'ptDiff_bGenJet_bGenPart_strong/bGenPart_pt_strong')\
           .Define('ptRelDiff_bJet_bGenJet_weak', 'ptDiff_bJet_bGenJet_weak/bGenJet_pt_weak')\
           .Define('ptRelDiff_bJet_bGenJet_strong', 'ptDiff_bJet_bGenJet_strong/bGenJet_pt_strong')\
           .Define('ptRelDiff_bJet_bGenPart_weak', 'ptDiff_bJet_bGenPart_weak/bGenPart_pt_weak')\
           .Define('ptRelDiff_bJet_bGenPart_strong', 'ptDiff_bJet_bGenPart_strong/bGenPart_pt_strong')
    #******************************************************************************************************
    return df