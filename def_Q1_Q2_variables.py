# Special new variables explained in main.ipynb and the pdf

def define_Q1_Q2_variables(df):
    # eta
    df = df.Define('bGenPart_etaDiff01', 'bGenPart_eta_0-bGenPart_eta_1')\
           .Define('bGenJet_etaDiff01', 'bGenJet_eta_0-bGenJet_eta_1')\
           .Define('bJet_etaDiff01', 'bJet_eta_0-bJet_eta_1')\
           .Define('bGenPart_etaAbsDiff01', 'abs(bGenPart_etaDiff01)')\
           .Define('bGenJet_etaAbsDiff01', 'abs(bGenJet_etaDiff01)')\
           .Define('bJet_etaAbsDiff01', 'abs(bJet_etaDiff01)')\
           .Define('bGenPart_absEtaDiff01', 'bGenPart_absEta_0-bGenPart_absEta_1')\
           .Define('bGenJet_absEtaDiff01', 'bGenJet_absEta_0-bGenJet_absEta_1')\
           .Define('bJet_absEtaDiff01', 'bJet_absEta_0-bJet_absEta_1')\
           .Define('bGenPart_absEtaAbsDiff01', 'abs(bGenPart_absEtaDiff01)')\
           .Define('bGenJet_absEtaAbsDiff01', 'abs(bGenJet_absEtaDiff01)')\
           .Define('bJet_absEtaAbsDiff01', 'abs(bJet_absEtaDiff01)')
    # phi
    df = df.Define('bGenPart_phiDiff01', 'DeltaPhi(bGenPart_phi_0,bGenPart_phi_1)')\
           .Define('bGenJet_phiDiff01', 'DeltaPhi(bGenJet_phi_0,bGenJet_phi_1)')\
           .Define('bJet_phiDiff01', 'DeltaPhi(bJet_phi_0,bJet_phi_1)')\
           .Define('bGenPart_phiAbsDiff01', 'abs(bGenPart_phiDiff01)')\
           .Define('bGenJet_phiAbsDiff01', 'abs(bGenJet_phiDiff01)')\
           .Define('bJet_phiAbsDiff01', 'abs(bJet_phiDiff01)')
    # pT
    df = df.Define('bGenPart_ptDiff01', 'bGenPart_pt_0-bGenPart_pt_1')\
           .Define('bGenJet_ptDiff01', 'bGenJet_pt_0-bGenJet_pt_1')\
           .Define('bJet_ptDiff01', 'bJet_pt_0-bJet_pt_1')\
           .Define('bGenPart_ptAbsDiff01', 'abs(bGenPart_ptDiff01)')\
           .Define('bGenJet_ptAbsDiff01', 'abs(bGenJet_ptDiff01)')\
           .Define('bJet_ptAbsDiff01', 'abs(bJet_ptDiff01)')\
           .Define('bGenPart_ptAbsDiff01rel1', 'abs(bGenPart_ptDiff01/bGenPart_pt_1)')\
           .Define('bGenJet_ptAbsDiff01rel1', 'abs(bGenJet_ptDiff01/bGenJet_pt_1)')\
           .Define('bJet_ptAbsDiff01rel1', 'abs(bJet_ptDiff01/bJet_pt_1)')\
           .Define('bGenPart_relPt0', 'bGenPart_pt_0/(bGenPart_pt_0+bGenPart_pt_1)')\
           .Define('bGenJet_relPt0', 'bGenJet_pt_0/(bGenJet_pt_0+bGenJet_pt_1)')\
           .Define('bJet_relPt0', 'bJet_pt_0/(bJet_pt_0+bJet_pt_1)')\
           .Define('bGenPart_relPt1', 'bGenPart_pt_1/(bGenPart_pt_0+bGenPart_pt_1)')\
           .Define('bGenJet_relPt1', 'bGenJet_pt_1/(bGenJet_pt_0+bGenJet_pt_1)')\
           .Define('bJet_relPt1', 'bJet_pt_1/(bJet_pt_0+bJet_pt_1)')\
           .Define('bGenPart_relPt', 'min(bGenPart_relPt0, bGenPart_relPt1)')\
           .Define('bGenJet_relPt', 'min(bGenJet_relPt0, bGenJet_relPt1)')\
           .Define('bJet_relPt', 'min(bJet_relPt0, bJet_relPt1)')\
           .Define('bGenPart_oppositeEtaSigns', 'bGenPart_eta_0*bGenPart_eta_1<0')\
           .Define('bGenJet_oppositeEtaSigns', 'bGenJet_eta_0*bGenJet_eta_1<0')\
           .Define('bJet_oppositeEtaSigns', 'bJet_eta_0*bJet_eta_1<0')
    return df