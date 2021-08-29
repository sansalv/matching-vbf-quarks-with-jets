import ROOT

ROOT.gInterpreter.Declare("""
using namespace ROOT::VecOps;

const bool isNeutrino(const Int_t& idx, const ROOT::RVec<std::size_t>& pdgId){

    ROOT::RVec<Int_t> pdgId_neutrino = {-12, -14, -16, -18, 12, 14, 16, 18};
    
    return (std::find(pdgId_neutrino.begin(), pdgId_neutrino.end(), pdgId[idx]) != pdgId_neutrino.end());
    
};
""")
#******************************************************************************************************
ROOT.gInterpreter.Declare("""

using namespace ROOT::VecOps;

const ROOT::RVec<ROOT::RVec<std::size_t>> FindBestChildren_indices(const std::size_t& nGenPart, const ROOT::RVec<float>& pt,
                                                        const ROOT::RVec<Int_t>& idxMother){
    
    ROOT::RVec<ROOT::RVec<std::size_t>> bestChildren_indices(2);
    ROOT::RVec<std::size_t> allMothers;
    Int_t mother;
    ROOT::RVec<std::size_t> q1_children;
    ROOT::RVec<std::size_t> q2_children;
    bool isMother;
    
    for(std::size_t i = nGenPart; i --> 0; ){
        mother = idxMother[i];
        isMother = (std::find(allMothers.begin(), allMothers.end(), i) != allMothers.end());
        
        if(isMother == false){
            while((mother != 0) && (mother != -1)){
                allMothers.push_back(mother);
                if(mother == 4){
                    q1_children.push_back(i);
                    break;
                }
                if(mother == 5){
                    q2_children.push_back(i);
                    break;
                }
                mother = idxMother[mother]; 
            }
        }
    }
    
    if(!(q1_children.size() > 0 && q2_children.size() > 0)){
        if(q1_children.size() == 0){
            q1_children.push_back(4);
        }
        if(q2_children.size() == 0){
            q2_children.push_back(5);
        }
    }
    
    
    ROOT::RVec<std::size_t> q1_children_sorted = q1_children;
    ROOT::RVec<std::size_t> q2_children_sorted = q2_children;
    
    if (q1_children.size() > 1){
        q1_children_sorted = Sort(q1_children, [pt](std::size_t idx1, std::size_t idx2) {return pt[idx1] > pt[idx2];});
    }
    if (q2_children.size() > 1){
        q2_children_sorted = Sort(q2_children, [pt](std::size_t idx1, std::size_t idx2) {return pt[idx1] > pt[idx2];});
    }

    bestChildren_indices = {q1_children_sorted, q2_children_sorted};
    
    return bestChildren_indices;
};
""")
#******************************************************************************************************
ROOT.gInterpreter.Declare("""

using namespace ROOT::VecOps;

const ROOT::RVec<std::size_t> ChooseBestChildren_indices(const ROOT::RVec<ROOT::RVec<std::size_t>>& bestChildren_idxLists,
                                                                const ROOT::RVec<float>& GenPart_eta, const ROOT::RVec<float>& GenPart_phi,
                                                                const ROOT::RVec<float>& GenJet_eta, const ROOT::RVec<float>& GenJet_phi,
                                                                const ROOT::RVec<std::size_t>& pdgId){
                                                                
    ROOT::RVec<std::size_t> q1_children_sorted = bestChildren_idxLists[0];
    ROOT::RVec<std::size_t> q2_children_sorted = bestChildren_idxLists[1];
    
    std::size_t i = 0;
    std::size_t q1_idx = q1_children_sorted[0];
    std::size_t GenJet_idx;
    float deltaR;
    
    while( (i == 0) || ((deltaR >= 0.4 || isNeutrino(q1_idx, pdgId)) && i < q1_children_sorted.size()) )
    {
        q1_idx = q1_children_sorted[i];
        GenJet_idx = FindClosest({GenPart_phi[q1_idx]}, {GenPart_eta[q1_idx]}, GenJet_phi, GenJet_eta)[0];
        deltaR = DeltaR(GenPart_eta[q1_idx], GenJet_eta[GenJet_idx], GenPart_phi[q1_idx], GenJet_phi[GenJet_idx]);
        i++;
    }
    if (deltaR >= 0.4 || isNeutrino(q1_idx, pdgId)){
        q1_idx = q1_children_sorted[0];
        if (isNeutrino(q1_idx, pdgId)){
            i = 0;
            while (isNeutrino(q1_idx, pdgId) && i < q1_children_sorted.size()){
                q1_idx = q1_children_sorted[i];
                i++;
            }
        }
    }
    
    i = 0;
    std::size_t q2_idx = q2_children_sorted[0];
    
    while( (i == 0) || ((deltaR >= 0.4 || isNeutrino(q2_idx, pdgId)) && i < q2_children_sorted.size()) )
    {
        q2_idx = q2_children_sorted[i];
        GenJet_idx = FindClosest({GenPart_phi[q2_idx]}, {GenPart_eta[q2_idx]}, GenJet_phi, GenJet_eta)[0];
        deltaR = DeltaR(GenPart_eta[q2_idx], GenJet_eta[GenJet_idx], GenPart_phi[q2_idx], GenJet_phi[GenJet_idx]);
        i++;
    }
    if (deltaR >= 0.4 || isNeutrino(q2_idx, pdgId)){
        q2_idx = q2_children_sorted[0];
        if (isNeutrino(q2_idx, pdgId)){
            i = 0;
            while (isNeutrino(q2_idx, pdgId) && i < q2_children_sorted.size()){
                q2_idx = q2_children_sorted[i];
                i++;
            }
        }
    }
    
    
    return {q1_idx, q2_idx};
};
""")