import ROOT
#******************************************************************************************************
# c++ function that is used to find closest GenJet/Jet in weak/strong match
# returns index rvec of the object indixes for both bGenPart/bGenJet, for example: {3, 10}

ROOT.gInterpreter.Declare("""

using namespace ROOT::VecOps;

const ROOT::RVec<std::size_t> FindClosest(const ROOT::RVec<float>& ref_phi, const ROOT::RVec<float>& ref_eta,
                                            const ROOT::RVec<float>& obj_phi, const ROOT::RVec<float>& obj_eta){
    if (ref_phi.size() != ref_eta.size()){
        cout << "FindClosest: ERROR: ref_phi and ref_eta must have same size!" << endl;
    }
    if (obj_phi.size() != obj_eta.size()){
        cout << "FindClosest: ERROR: ref_phi and ref_eta must have same size!" << endl;
    }

    std::size_t Ni = ref_phi.size();
    std::size_t Nj = obj_phi.size();
   
    if (Nj == 0) {
        cout << "FindClosest: ERROR: nObjJet == 0 case" << endl;
    }else if (Nj == 1) {
        cout << "FindClosest: ERROR: nObjJet == 1 case (not necessarily error but only one to choose from)" << endl;
    }
    
    RVec<std::size_t> minDeltaRindices(Ni);
    for (std::size_t i=0; i<Ni; i++) {
        double dr_min = 999;
        std::size_t idx_dr_min = 0;
        for(std::size_t j=0; j<Nj; j++) {
            const double dr = DeltaR(ref_eta[i], obj_eta[j], ref_phi[i], obj_phi[j]);
            if (dr < dr_min){
                dr_min = dr;
                idx_dr_min = j;
            }
        }
        minDeltaRindices[i] = idx_dr_min;
    }
    
    return minDeltaRindices;
};
""")
#******************************************************************************************************
# c++ function made by Vilja that is similar to the one above but returns deltaRs instead of indices.
# This is used at least in viljaFilters (for example viljaFilter.py)
# I just noticed that this returns RVec<std::size_t> instead of RVec<float> which might be better since deltaR is continuous variable and not a natural number. I recommend checking this.

ROOT.gInterpreter.Declare("""
using namespace ROOT::VecOps;
const ROOT::RVec<std::size_t> FindClosestDeltaR(const ROOT::RVec<float>& ref_phi, ROOT::RVec<float>& ref_eta,
                                                        const ROOT::RVec<float>& obj_phi, const ROOT::RVec<float>& obj_eta){
    if(ref_phi.size() != ref_eta.size()){
        cout << "FindClosest: ERROR: ref_phi and ref_eta must have same size!" << endl;
    }
    if(obj_phi.size() != obj_eta.size()){
        cout << "FindClosest: ERROR: ref_phi and ref_eta must have same size!" << endl;
    }

    std::size_t Ni = ref_phi.size();
    std::size_t Nj = obj_phi.size();
    RVec<std::size_t> deltaR(Ni);
    RVec<std::size_t> minDeltaRindices(Ni);

    for(std::size_t i=0; i<Ni; i++) {
             double dr_min = 999;
             std::size_t idx_dr_min = 0;
             for(std::size_t j=0; j<Nj; j++) {
                    const double dr = DeltaR(ref_eta[i], obj_eta[j], ref_phi[i], obj_phi[j]);
                    if (dr < dr_min){
                             dr_min = dr;
                             idx_dr_min = j;
                        }
             }
             deltaR[i] = dr_min;
    }
    return deltaR;
};
""")