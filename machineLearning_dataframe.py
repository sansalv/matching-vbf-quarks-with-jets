# Machine learning stuff starts here
# Every event is divided into jetPairs where one is strong jetPair and one is VBFC
# This code can be used also without VBFC and without viljaFiltered (=False)
# Feutures used here: pt, eta, deltaEta, mjj
# *****************************************
# Pandas dataframe

columns = ['Jet_pt', 'Jet_eta', 'bJet_pt', 'bJet_eta', 'JetPair_mjjs']
if viljaFiltered:
    columns += ['VBFCandidates_pt', 'VBFCandidates_eta']
npdf = df0.AsNumpy(columns)
pddf = pd.DataFrame(npdf)
# *****************************************
# Division into jetPairs

def returnJetPairs(jets):
    n = len(jets)
    l = []
    for i in range(n-1):
        for j in range(i+1, n, 1):
            l.append([jets[i], jets[j]])
    return l
# *****************************************
# Making feuture values for every jetPair

JetPairs_eta = [returnJetPairs(jets) for jets in pddf['Jet_eta']]
JetPairs_pt = [returnJetPairs(jets) for jets in pddf['Jet_pt']]

n = len(JetPairs_pt)
listOfPddfs = []
for j in range(n):
    pddf_pt_j = pd.DataFrame(JetPairs_pt[j], columns = ['Pt0', 'Pt1'])
    pddf_eta_j = pd.DataFrame(JetPairs_eta[j], columns = ['Eta0', 'Eta1'])
    pddf_both_j = pd.concat([pddf_pt_j, pddf_eta_j], axis=1)
    listOfPddfs.append(pddf_both_j)
pddf_t = pd.concat(listOfPddfs, keys=list(range(j+1)))

pddf_t['DeltaEta'] = pddf_t.apply(lambda row: abs(row.Eta0 - row.Eta1), axis = 1)
# *****************************************
# Feuture mjj (invarian mass) is calculated in c++ code

ROOT.gInterpreter.Declare("""

using namespace ROOT::VecOps;

const RVec<float> RVecOfMjjs(const RVec<float>& jet_pt, const RVec<float>& jet_eta, const RVec<float>& jet_phi,
                                        const RVec<float>& jet_mass){

    std::size_t n = jet_pt.size();
    
    RVec<RVec<std::size_t>> jetPairs_idx;
    
    for (std::size_t i=0; i < n-1; i++) {
        for (std::size_t j=i+1; j < n; j++) {
            jetPairs_idx.push_back({i,j});
        }
    }
    
    std::size_t m = jetPairs_idx.size();
    RVec<float> mjjs(m);
    
    for (std::size_t i=0; i<m; i++) {
        mjjs[i] = InvariantMass(Take(jet_pt, jetPairs_idx[i]), Take(jet_eta, jetPairs_idx[i]), Take(jet_phi, jetPairs_idx[i]), Take(jet_mass, jetPairs_idx[i]));
    }
    
    return mjjs;
};
""")
df0 = df0.Define('JetPair_mjjs', 'RVecOfMjjs(Jet_pt, Jet_eta, Jet_phi, Jet_mass)')
pddf_t['Mjj'] = 0.0
for index, rows in pddf_t.iterrows():
    pddf_t.loc[index[0]].at[index[1],'Mjj'] = pddf['JetPair_mjjs'][index[0]][index[1]]
# *****************************************
# Create 0 or 1 columns depending if jetPair is strong and/or VBFC

pddf_bEta = pd.DataFrame(list(pddf['bJet_eta']), columns=['bEta0', 'bEta1'])
if viljaFiltered:
    pddf_VBFCEta = pd.DataFrame(list(pddf['VBFCandidates_eta']), columns=['VBFCEta0', 'VBFCEta1'])
pddf_t['Strong Jets'] = 0
if viljaFiltered:
    pddf_t['VBFC Jets'] = 0
    
n = len(JetPairs_pt)
for j in range(n):
    bEtaList_j = [pddf_bEta['bEta0'][j], pddf_bEta['bEta1'][j]]
    a = (pddf_t.loc[j]['Eta0'] == bEtaList_j[0]) & (pddf_t.loc[j]['Eta1'] == bEtaList_j[1])
    b = (pddf_t.loc[j]['Eta0'] == bEtaList_j[1]) & (pddf_t.loc[j]['Eta1'] == bEtaList_j[0])
    idx = pddf_t.loc[j][a | b].index[0]
    pddf_t.loc[j].at[idx,'Strong Jets'] = 1
    if viljaFiltered:
        VBFCEtaList_j = [pddf_VBFCEta['VBFCEta0'][j], pddf_VBFCEta['VBFCEta1'][j]]
        a = (pddf_t.loc[j]['Eta0'] == VBFCEtaList_j[0]) & (pddf_t.loc[j]['Eta1'] == VBFCEtaList_j[1])
        b = (pddf_t.loc[j]['Eta0'] == VBFCEtaList_j[1]) & (pddf_t.loc[j]['Eta1'] == VBFCEtaList_j[0])
        idx = pddf_t.loc[j][a | b].index[0]
        pddf_t.loc[j].at[idx, 'VBFC Jets'] = 1
# *****************************************
# Different dataframe where the event index is a column instead of key

pddf_s = pddf_t.reset_index()
pddf_s = pddf_s.rename(columns={'level_0': 'Event'}).drop(columns=['level_1'])
# ***************************************** 
# X = feutures and y = target result

X = pddf_s.iloc[:,1:7]
X = X.apply(zscore)
y = pddf_s.iloc[:,7]
if viljaFiltered:
    y2 = pddf_s.iloc[:3000,8]
# *****************************************
# Split the data into training and testing

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
# ***************************************** 
# Statistics of the data

print('Overall number of category instances:')

print('Not VBF Jet: ' + str(len(y[y==0])))
print('VBF Jet:     ' + str(len(y[y==1])))
if viljaFiltered:
    print('Wrong VBFC:  ' + str(len(y2[y2==1][y==0])))
    print('Right VBFC:  ' + str(len(y2[y2==1][y==1])))
# *****************************************
# Print the pddf_t dataframe

pddf_t.head()