pdgIdDir = {
    1: 'd',
    2: 'u',
    3: 's',
    4: 'c',
    5: 'b',
    #6: 't',
    #7: 'b^',
    #8: 't^',
    
    11: 'e-',
    12: 'v_e',
    13: 'mu-',
    14: 'v_mu',
    #15: 'tau-',
    16: 'v_tau',
    #17: 'tau^',
    #18: 'v_tau^',
    
    21: 'g',
    22: 'photon',
    #23: 'Z^0',
    #24: 'W^+',
    #25: 'H^0',
    
    #32: 'Z^',
    #33: 'Z^^',
    #34: 'W^',
    #35: 'H^02',
    #36: 'H^03',
    #37: 'H^+',
    
    111: 'pi^0',
    211: 'pi^+',
    
    411: 'D^+',
    421: 'D^0',
    431: 'D^+s',
    
    441: 'eta_c(1s)',
    443: 'J/psi(1s)',
    
    511: 'B^0',
    521: 'B^+',
    531: 'B^0s',
    
    4122: 'Lambda^+c',
    4132: 'Xi^0_c',
    4232: 'Xi^+_c',
    
    4332: 'Omega^0c'
}
#******************************************************************************************************
statusFlagsDir = {
    0: 'isPrompt',
    1: 'isDecayedLeptonHadron',
    2: 'isTauDecayProduct',
    3: 'isPromptTauDecayProduct',
    4: 'isDirectTauDecayProduct',
    5: 'isDirectPromptTauDecayProduct',
    6: 'isDirectHadronDecayProduct',
    7: 'isHardProcess',
    8: 'fromHardProcess',
    9: 'isHardProcessTauDecayProduct',
    10: 'isDirectHardProcessTauDecayProduct',
    11: 'fromHardProcessBeforeFSR',
    12: 'isFirstCopy',
    13: 'isLastCopy',
    14: 'isLastCopyBeforeFSR'
}
#******************************************************************************************************
eventStuffList = ['nGenPart', 'GenPart_pdgId', 'GenPart_genPartIdxMother', 'GenPart_status', 'GenPart_statusFlags_intRVec',
                  'nB_weak', 'bGenJet_deltaR_lowerThan04', 'bJet_deltaR_lowerThan04',
                  'bGenPart_eta', 'bGenPart_phi', 'bGenPart_pt', 'bGenPart_pdgId',
                  'bGenJet_eta', 'bGenJet_phi', 'bGenJet_pt',
                  'bJet_eta', 'bJet_phi', 'bJet_pt', 'bJet_mass',
                  'bJet_jetId', 'bJet_puId', 'bJet_mjj', 'bJet_deltaEta',
                  'bJet_closestHiggsCandidateDeltaR', 'bJet_closestMuonDeltaR', 'bJet_closestElectronDeltaR',
                  'GenPart_eta', 'GenPart_phi', 'GenPart_pt',
                  'GenJet_eta', 'GenJet_phi', 'GenJet_pt',
                  'Jet_eta', 'Jet_phi', 'Jet_pt',
                  'VBFCandidates_eta', 'VBFCandidates_phi', 'VBFCandidates_pt', 'VBFCandidates_mjj',
                  'nMuonsForCleaning', 'GoodJet_FatJetCleaned_closestMuonDeltaR',
                  'nElectronsForCleaning', 'GoodJet_closestElectronDeltaR',
                  'HiggsCandidate_pt', 'GoodJet_closestHiggsCandidateDeltaR',
                  'VBFCandidates_jetId', 'VBFCandidates_puId',
                  'GoodJet_closestHiggsCandidateDeltaR']
#******************************************************************************************************
npdf=df0.AsNumpy(eventStuffList)
#******************************************************************************************************
m = len(npdf['nGenPart'])

nGenPart = list(npdf['nGenPart'])
nB_weak = list(npdf['nB_weak'])

weakStatus = []
strongStatus = []

pdgList = []
idxMother = []
status = []
statusFlags = []

eta = []
phi = []
pt = []
coordinate = []

bGenPart_eta = []
bGenPart_phi = []
bGenPart_pt = []
bGenPart_coordinate = []
bGenPart_pdgId = []

bGenJet_eta = []
bGenJet_phi = []
bGenJet_pt = []
bGenJet_coordinate = []

bJet_eta = []
bJet_phi = []
bJet_pt = []
bJet_coordinate = []
bJet_mass = []

bJet_jetId = []
bJet_puId = []
bJet_mjj = []
bJet_deltaEta = []

bJet_closestHiggsCandidateDeltaR = []
bJet_closestMuonDeltaR = []
bJet_closestElectronDeltaR = []

GenJet_eta = []
GenJet_phi = []
GenJet_pt = []
GenJet_coordinate = []

Jet_eta = []
Jet_phi = []
Jet_pt = []
Jet_coordinate = []

VBFCandidates_eta = []
VBFCandidates_phi = []
VBFCandidates_pt = []
VBFCandidates_coordinate = []
VBFCandidates_mjj = []
VBFCandidates_jetId = []
VBFCandidates_puId = []

for i in range(m):
    pdgList.append(list(npdf['GenPart_pdgId'][i]))
    idxMother.append(list(npdf['GenPart_genPartIdxMother'][i]))
    status.append(list(npdf['GenPart_status'][i]))
    statusFlags.append(list(npdf['GenPart_statusFlags_intRVec'][i]))
    
    eta.append(list(npdf['GenPart_eta'][i]))
    phi.append(list(npdf['GenPart_phi'][i]))
    pt.append(list(npdf['GenPart_pt'][i]))
    coordinate.append([(eta[i][j], phi[i][j], pt[i][j]) for j in range(len(eta[i]))])
    
    bGenPart_eta.append(list(npdf['bGenPart_eta'][i]))
    bGenPart_phi.append(list(npdf['bGenPart_phi'][i]))
    bGenPart_pt.append(list(npdf['bGenPart_pt'][i]))
    bGenPart_coordinate.append([(bGenPart_eta[i][j], bGenPart_phi[i][j], bGenPart_pt[i][j]) for j in range(len(bGenPart_eta[i]))])
    bGenPart_pdgId.append(list(npdf['bGenPart_pdgId'][i]))
    
    bGenJet_eta.append(list(npdf['bGenJet_eta'][i]))
    bGenJet_phi.append(list(npdf['bGenJet_phi'][i]))
    bGenJet_pt.append(list(npdf['bGenJet_pt'][i]))
    bGenJet_coordinate.append([(bGenJet_eta[i][j], bGenJet_phi[i][j], bGenJet_pt[i][j]) for j in range(len(bGenJet_eta[i]))])
    weakStatus.append(list(npdf['bGenJet_deltaR_lowerThan04'][i]))
    
    bJet_eta.append(list(npdf['bJet_eta'][i]))
    bJet_phi.append(list(npdf['bJet_phi'][i]))
    bJet_pt.append(list(npdf['bJet_pt'][i]))
    bJet_coordinate.append([(bJet_eta[i][j], bJet_phi[i][j], bJet_pt[i][j]) for j in range(len(bJet_eta[i]))])
    bJet_mass.append(list(npdf['bJet_mass'][i]))
    bJet_jetId.append(list(npdf['bJet_jetId'][i]))
    bJet_puId.append(list(npdf['bJet_puId'][i]))
    bJet_mjj.append(npdf['bJet_mjj'][i])
    bJet_deltaEta.append(npdf['bJet_deltaEta'][i])
    strongStatus.append(list(npdf['bJet_deltaR_lowerThan04'][i]))
    
    bJet_closestHiggsCandidateDeltaR.append(list(npdf['bJet_closestHiggsCandidateDeltaR'][i]))
    bJet_closestMuonDeltaR.append(list(npdf['bJet_closestMuonDeltaR'][i]))
    bJet_closestElectronDeltaR.append(list(npdf['bJet_closestElectronDeltaR'][i]))
    
    GenJet_eta.append(list(npdf['GenJet_eta'][i]))
    GenJet_phi.append(list(npdf['GenJet_phi'][i]))
    GenJet_pt.append(list(npdf['GenJet_pt'][i]))
    GenJet_coordinate.append([(GenJet_eta[i][j], GenJet_phi[i][j], GenJet_pt[i][j]) for j in range(len(GenJet_eta[i]))])
    
    Jet_eta.append(list(npdf['Jet_eta'][i]))
    Jet_phi.append(list(npdf['Jet_phi'][i]))
    Jet_pt.append(list(npdf['Jet_pt'][i]))
    Jet_coordinate.append([(Jet_eta[i][j], Jet_phi[i][j], Jet_pt[i][j]) for j in range(len(Jet_eta[i]))])
    
    VBFCandidates_eta.append(list(npdf['VBFCandidates_eta'][i]))
    VBFCandidates_phi.append(list(npdf['VBFCandidates_phi'][i]))
    VBFCandidates_pt.append(list(npdf['VBFCandidates_pt'][i]))
    VBFCandidates_coordinate.append([(VBFCandidates_eta[i][j], VBFCandidates_phi[i][j], VBFCandidates_pt[i][j]) for j in
                                     range(len(VBFCandidates_eta[i]))])
    VBFCandidates_mjj.append(npdf['VBFCandidates_mjj'][i])
    VBFCandidates_jetId.append(list(npdf['VBFCandidates_jetId'][i]))
    VBFCandidates_puId.append(list(npdf['VBFCandidates_puId'][i]))
    #VBFCandidates_closestHiggsCandidateDeltaR.append(list(npdf['GoodJet_closestHiggsCandidateDeltaR'][i]))