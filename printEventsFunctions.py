import ROOT

# Functions for the last one printEvents()
# It MIGHT be easier to follow this bottom to up sice the major functions are at the bottom and they are build by the smaller functions before them
# ******************************************************************************************************
# Parameter is event number and this function figures if the bJet and VBFCs are the same or not
# Returns bool list and the VBFCs in the correct order compared to bJets

def bJet_VBFC_match_VBFCList(event):

    j0 = bJet_coordinate[event][0]
    j1 = bJet_coordinate[event][1]
    
    v0 = VBFCandidates_coordinate[event][0]
    v1 = VBFCandidates_coordinate[event][1]
    
    if j0 == v1 or j1 == v0:
        vx = v1
        v1 = v0
        v0 = vx
        
    if v0 == j0 and v1 == j1:
        bJet_VBFC_match = [True, True]
    elif v0 == j0 and v1 != j1:
        bJet_VBFC_match = [True, False]
    elif v0 != j0 and v1 == j1:
        bJet_VBFC_match = [False, True]
    else:
        bJet_VBFC_match = [False, False]
        
    return bJet_VBFC_match, [v0, v1]
# ******************************************************************************************************
# This c++ function is used in the statusFlags where the (binary coded flag) integers are transformed into integer lists where the integers are the flags
# So basically one big integer that has the flags in the binary form is transformed into integer lists where every integer is separate flag
# Combining this with statusFlagsDir dictionary in printEventsGlobVariables.py gives the flag explanation :-)
# Example: {18, 32, ...} --> {10010, 100000, ...} --> {{2,5}, {6}, ...}

ROOT.gInterpreter.Declare("""

using namespace ROOT::VecOps;

const ROOT::RVec<RVec<std::size_t>> intRVec_to_intRVecRVec(const ROOT::RVec<std::size_t>& rvec){

    std::size_t N = rvec.size();
    RVec<RVec<std::size_t>> L(N);
    
    for(std::size_t i = 0; i < N; i++) {
    
        std::size_t n = rvec[i];
        
        std::size_t m = n;
        std::size_t s = 0;
        while (m > 0) {
            if(m%2 == 1){
                s++;
            }
            m = m/2;
        }
        
        RVec<std::size_t> l(s);
        std::size_t j = 0;
        std::size_t k = 0;
        m = n;
        while (m > 0) {
            if(m%2 == 1){
                l[k]=j;
                k++;
            }   
            m = m/2;
            j++;
        }

        L[i] = l;
    }

    return L;
};
""")
#******************************************************************************************************
# Transforms pdgId into string using pdgIdDir dictionary in printEventsGlobVariables.py
# The negative number gets "anti_" in front of the string, for example "anti_electron" means positron

def getPdgId(i):
    string = ''
    if (i in pdgIdDir) or (-i in pdgIdDir):
        if i < 0:
            string = string + 'anti_'
            i = - i
        string = string + pdgIdDir[i]
    else:
        string = str(i)
    return string
#******************************************************************************************************
# This functions print the index paths in the events. So basically you see how the last GenParts get formed. Also, status and coordinates are printed depending on printIdxStatus, printCoordinateAndPt = True/False, in printEvents()

def printIdxStuff(event, motherPathsQ, printIdxStatus, printCoordinateAndPt):
    print('-------------------------------------------')
    print('-------------------------------------------')
    print('Index paths:')
    for i in range(len(motherPathsQ[0])):
        print(motherPathsQ[0][i])
    for i in range(len(motherPathsQ[1])):
        print(motherPathsQ[1][i])
    print('-------------------------------------------')
    
    for q in motherPathsQ:
        for mp in q:
            lastIndex = mp[-1]
            print('-------------------------------------------')
            print(str(mp) + ':')
            print('Last index (' + str(lastIndex)+') stats:')
            print('pdgId:       ' + getPdgId(pdgList[event][lastIndex]))
            if printIdxStatus:
                print('status:      ' +  str(status[event][lastIndex]) + '\n' +
                      'statusFlags: ', end='')
                statusFlags_readable = [statusFlagsDir[flag] for flag in statusFlags[event][lastIndex]]
                print(statusFlags_readable)
            if printCoordinateAndPt:
                lastIdxCoordinates = coordinate[event][lastIndex]
                lastIdxCoordinates_round = (round(lastIdxCoordinates[0],2), round(lastIdxCoordinates[1],2),
                                            int(round(lastIdxCoordinates[2])))
                print('coordinates: ' + str(lastIdxCoordinates_round))
        print('-------------------------------------------')

#******************************************************************************************************      
# This stuff is printed if we are interested in the matching of the bJets and VBFCs

def VBFC_match_print(Q, event, bJet_VBFC_match, VBFCandidates_coordinate_fixed, VBFCandidates_coordinate_round):
    
    if bJet_VBFC_match[Q]:
        print('| ===> RIGHT VBFC:   ' + str(VBFCandidates_coordinate_round[Q]))
        return [0]*10
    else:
        print('|')
        print('| ===> WRONG VBFC:   ' + str(VBFCandidates_coordinate_round[Q]))
        print('|')
        print('| The cause(s) of wrong VBFC (notice that one is already enough for incorrect match):')
        i = 1
        
        # This is made to calculate the reasons why bJet and VBFC are not the same
        smallerPt, smallMjj, smallEta, bigEta, smallDeltaEta, jetIdWrong, puIdWrong, tooCloseHiggs, tooCloseMuon, tooCloseElectron = (0,)*10
        
        # This finds and prints the reason(s). Check the viljaFilter(_SalomaaMod).py to see the filters of the bJets
        if bJet_pt[event][Q] < VBFCandidates_coordinate_fixed[Q][2]:
            smallerPt = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet pT < VBFC pT:')
            i += 1
            print('|     ' + str(round(bJet_pt[event][Q], 1)) + ' < ' + str(round(VBFCandidates_coordinate_fixed[Q][2], 1)))
            
        if bJet_mjj[event] <= 500:
            smallMjj = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet mjj <= 500:')
            i += 1
            print('| bJet mjj:      ' + str(round(bJet_mjj[event])))
        if abs(bJet_eta[event][Q]) <= 1.5:
            smallEta = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet |eta| <= 1.5:')
            i += 1
            print('|     bJet |eta|  = ' + str(round(abs(bJet_eta[event][Q]), 1)))
            print('|     VBFC |eta|  = ' + str(round(abs(VBFCandidates_coordinate_fixed[Q][0]), 1)))
        if abs(bJet_eta[event][Q]) >= 4.7:
            bigEta = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet |eta| >= 4.7:')
            i += 1
            print('|     bJet |eta|  = ' + str(round(abs(bJet_eta[event][Q]), 1)))
            print('|     VBFC |eta|  = ' + str(round(abs(VBFCandidates_coordinate_fixed[Q][0]), 1)))
        if bJet_deltaEta[event] <= 4:
            smallDeltaEta = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet |deltaEta| <= 4.0:')
            i += 1
            print('|     bJet |deltaEta|  = ' + str(round(bJet_deltaEta[event], 1)))
            print('|     VBFC |deltaEta|  = ' + str(round(abs(VBFCandidates_coordinate_fixed[0][0]-VBFCandidates_coordinate_fixed[1][0]), 1)))
        if not bJet_jetId[event][Q] & 2:
            jetIdWrong = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet jetId != x1x:')
            i += 1
            jetId = "{0:b}".format(bJet_jetId[event][Q])
            jetId = '0'*(3-len(jetId)) + jetId
            print('|     bJet jetId  = ' + jetId)
        if (not bJet_puId[event][Q] & 2) and (bJet_pt[event][Q] <= 50):
            puIdWrong = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('(bJet puId != x1x) AND (bJet pT <= 50.0):')
            i += 1
            puId = "{0:b}".format(bJet_puId[event][Q])
            puId = '0'*(3-len(puId)) + puId
            print('|     (bJet puId  = ' + puId + ') AND (bJet pT  = ' + str(round(bJet_pt[event][Q], 1)) + ')')
        if bJet_closestHiggsCandidateDeltaR[event][Q] <= 1.2:
            tooCloseHiggs = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet closestHiggsCandidateDeltaR <= 1.2:')
            i += 1
            print('|     bJet closestHiggsCandidateDeltaR  = '  + str(round(bJet_closestHiggsCandidateDeltaR[event][Q],1)))
        if bJet_closestMuonDeltaR[event][Q] <= 0.4:
            tooCloseMuon = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet closestMuonDeltaR <= 0.4:')
            i += 1
            print('|     bJet closestMuonDeltaR  = '  + str(round(bJet_closestMuonDeltaR[event][Q],1)))
        if bJet_closestElectronDeltaR[event][Q] <= 0.4:
            tooCloseElectron = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet closestElectronDeltaR <= 0.4:')
            i += 1
            print('|     bJet closestElectronDeltaR  = '  + str(round(bJet_closestElectronDeltaR[event][Q],1)))
        if i == 1:
            print('| ************ERROR:************')
            print('| ******************************')
            print('| The cause was not found... :-(')
            print('| ******************************')
            
        # Gathering the reasons of failure into a list (which is returned)
        checkList = [smallerPt, smallMjj, smallEta, bigEta, smallDeltaEta, jetIdWrong, puIdWrong, tooCloseHiggs, tooCloseMuon, tooCloseElectron]
        
        return checkList
#******************************************************************************************************
# Prints all kind of stuff that for example concludes one event decays into bGenParts
    
def printDecayConclusion(event, showVBFCandidates, initialQuarks, initialCoordinates_round, finalStuff, finalCoordinates_round,
                         printCoordinateAndPt):
    print('-------------------------------------------')
    print('Decay conclusion:\n')
    print(initialQuarks[0] + ' ---> ' + str(finalStuff[0]) + ' ---> ' + str(getPdgId(bGenPart_pdgId[event][0])))
    print(initialQuarks[1] + ' ---> ' + str(finalStuff[1]) + ' ---> ' + str(getPdgId(bGenPart_pdgId[event][1])))
    print('\nStatus info (quark[0], quark[1]):')
    print('Weak match:   ', end='')
    print(weakStatus[event])
    print('Strong match: ', end='')
    print(strongStatus[event])

    # Using the first function to get the boolean list of bJet vs. VBFC match (for example [True, False])
    # and the correct ordering of the VBFCs ("fixed" by bJet matches)
    if showVBFCandidates:
        bJet_VBFC_match, VBFCandidates_coordinate_fixed = bJet_VBFC_match_VBFCList(event)
        bJet_VBFC_match_int = [int(b) for b in bJet_VBFC_match]
        print('VBFCandidate: ' + str(bJet_VBFC_match_int))

    # Prints coordinate stuff of the GenParts, bGenParts, bGenJets, bJets and VBFCs
    if printCoordinateAndPt:
        print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -')
        
        bGenPart_coordinate_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in bGenPart_coordinate[event]]
        bGenJet_coordinate_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in bGenJet_coordinate[event]]
        bJet_coordinate_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in bJet_coordinate[event]]
        #---------------------------------------------------------------
        if showVBFCandidates:
            VBFCandidates_coordinate_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in VBFCandidates_coordinate_fixed]
            if VBFCandidates_coordinate_fixed[0] == VBFCandidates_coordinate[event][1]:
                VBFCandidates_mjjx = VBFCandidates_mjj[0]
                VBFCandidates_mjj[0] = VBFCandidates_mjj[1]
                VBFCandidates_mjj[1] = VBFCandidates_mjjx
        #---------------------------------------------------------------
        print('with coordinates:')
        print('')
        
        # Deals both quark decays and matches separately
        for Q in range(2):
            
            print('Quark[' + str(Q) + '] coordinates (eta, phi, pT):')
            print('| Final state quark: ' + str(initialCoordinates_round[Q])  + ', {pdgId: ' + initialQuarks[Q] + '}')
            if len(finalCoordinates_round[Q]) != 1:
                print('| Final GenParts:   ', end='')
                print(finalCoordinates_round[Q])
            print('| ---> bGenPart:     ' + str(bGenPart_coordinate_round[Q]) + ', {pdgId: ' + str(getPdgId(bGenPart_pdgId[event][Q])) + '}')
            print('| ===> bGenJet:      ' + str(bGenJet_coordinate_round[Q]))
            print('| ===> bJet:         ' + str(bJet_coordinate_round[Q]))
            #---------------------------------------------------------------
            if showVBFCandidates:
                checkList = VBFC_match_print(Q, event, bJet_VBFC_match, VBFCandidates_coordinate_fixed, VBFCandidates_coordinate_round)
                print('')
            #---------------------------------------------------------------
        print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -')
        print('All GenJet coordinates:')
        GenJet_coordinate[event].sort(key = lambda a: a[2], reverse = True)
        GenJet_coordinates = GenJet_coordinate[event]
        GenJet_coordinates_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in GenJet_coordinates]
        print(GenJet_coordinates_round)
            
        print('All Jet coordinates:')
        Jet_coordinate[event].sort(key = lambda a: a[2], reverse = True)
        Jet_coordinates = Jet_coordinate[event]
        Jet_coordinates_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in Jet_coordinates]
        print(Jet_coordinates_round)
            
    print('-------------------------------------------')
    print('**************************************************************************************')
    return checkList
#******************************************************************************************************
# Printing method that depends on the boolean parameters (first row) and gets some information (second row)

def printIfWanted(showVBFCandidates, onlyNotWeaks, onlyNotWeaks_and_bigPt, printShort, printIdx, printIdxStatus, printCoordinateAndPt,
                  event, motherPathsQ, initialQuarks, finalStuff, finalCoordinates_round):
    #-------------------------------------------------------------------------
    # Skip weak events if onlyNotWeaks=True
    weakEvent = (nB_weak[event] == 2)
    if onlyNotWeaks:
        if weakEvent:
            # return checkList where no reasons of failure to VBFC vs. bJet matches
            return [0]*10
        elif onlyNotWeaks_and_bigPt:
            for q in range(2):
                if weakStatus[event][q] == 0 and bGenPart_coordinate[event][q][2] > 12:
                    break
                if q == 0:
                    continue
                else:
                    return [0]*10
    #-------------------------------------------------------------------------
    # Prints event number
    
    if printShort:
        print('Event ' + str(event) + ':')
    #-------------------------------------------------------------------------
    # Print final state quarks and coordinates if wanted
    # (notice that "initialQuarks" are "final state quarks" since they decay into GenParts still)
    
    if printIdx or printCoordinateAndPt:
        print('-------------------------------------------')
        print('Final state quarks: ')
        print(initialQuarks)
    initialCoordinates = coordinate[event][4:6]
    initialCoordinates_round = [(round(c[0], 2), round(c[1], 2), int(round(c[2]))) for c in initialCoordinates]
    if printCoordinateAndPt and printIdx:
        print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -')
        print('with GenPart coordinates (eta, phi, pT):')
        print(initialCoordinates_round)
        
    #-------------------------------------------------------------------------
    # The printing method printIdxStuff() defined above
    
    if printIdx:
        printIdxStuff(event, motherPathsQ, printIdxStatus, printCoordinateAndPt)
    #-------------------------------------------------------------------------
    # checkList expained above (returned from the previous function)
    
    checkList = printDecayConclusion(event, showVBFCandidates, initialQuarks, initialCoordinates_round, finalStuff, finalCoordinates_round, printCoordinateAndPt)
    
    return checkList
#******************************************************************************************************
# This is the loop that runs all events wanted (depending on r)
# This is a difficult bit of code so go slowly and try to understand the steps
# Understanding (and maybe visualization) of GenPart_genPartIdxMother variable (made of index lists) is necessary

def eventLoop(r, showVBFCandidates, onlyNotWeaks, onlyNotWeaks_and_bigPt, printShort, printIdx, printIdxStatus, printCoordinateAndPt):
    
    # All different bGenPart particle types (pdgIds) are collected (and at the end, printed)
    allFinalStuff = []
    # Own list for antiparticles
    allFinalStuff_anti = []
    
    # Collect and add all checkLists into overallList (the reasons why VBFC and bJet match fails)
    overallList = [0]*10
    
    for event in r:
        #-------------------------------------------------------------------------
        # Final state quarks (="initialQuarks") ---> GenParts ---> final GenParts (=finalStuff)
        initialQuarks = [getPdgId(pdgList[event][4]), getPdgId(pdgList[event][5])]
        finalStuff = [[], []]
        #-------------------------------------------------------------------------
        allMothers = []
        # F8 means it's regarding the final state quarks
        allF8MotherPaths = []
        # Mother index paths starting from final state quarks
        motherPathsQ = [[], []]
        #-------------------------------------------------------------------------
        # Check the idxMother list backwards.
        # This way we start with final childs and with their mothers until we get Higgs, final state quarks or initial state quarks
        # These are the oldest grandmothers where all GenParts come from.
        # Notice that the numbers here are indices of the GenParts.
        for i in range(nGenPart[event]-1, -1, -1):
            mother = idxMother[event][i]
            iMothers = []
            if i not in allMothers:
                # Stop when Higgs or initial state quark is the mother
                while mother not in [0, -1]:
                    iMothers.append(mother)
                    allMothers.append(mother)
                    mother = idxMother[event][mother]
                # The index path list with last member and reversed that it starts from the final state quark
                l=([i]+iMothers)[::-1]
                # 4 and 5 are the indexes of the final state quarks {initQ, initQ, Higgs, Higgs, finalQ (4th), finalQ (5th), ...}
                # We are interested only on these
                if (len(iMothers) != 0) and (l[0] in [4, 5]):
                    allF8MotherPaths.append(l)
        #-------------------------------------------------------------------------
        allF8MotherPaths = sorted(allF8MotherPaths)
        finalCoordinates = [[], []]
        finalCoordinates_round = [[], []]
        #-------------------------------------------------------------------------
        for path in allF8MotherPaths:
            if path[0] == 4:
                # idx = 0 --> from quark[0]
                idx = 0
            else:
                # idx = 1 --> from quark[1]
                idx = 1
            
            motherPathsQ[idx].append(path)
            lastIndex = path[-1]
            
            pdgid = getPdgId(pdgList[event][lastIndex])
            finalStuff[idx].append(pdgid)
            
            coordinate0 = coordinate[event][lastIndex]
            coordinate0_round = (round(coordinate0[0],2), round(coordinate0[1],2), int(round(coordinate0[2])))
            finalCoordinates[idx].append(coordinate0)
            finalCoordinates_round[idx].append(coordinate0_round)
            #-------------------------------------------------------------------------
            # sort lists by pT
            
            sortedZip = sorted(zip(finalCoordinates[idx], finalStuff[idx]), key=lambda coord: coord[0][2], reverse = True)
            finalStuff[idx] = [x for _,x in sortedZip]

            finalCoordinates[idx].sort(key = lambda coord: coord[2], reverse = True)
            finalCoordinates_round[idx].sort(key = lambda coord: coord[2], reverse = True)
            #-------------------------------------------------------------------------
            # Collect the particle data into allFinalStuff list
            
            if pdgid not in (allFinalStuff+allFinalStuff_anti):
                if 'anti' in pdgid:
                    allFinalStuff_anti.append(pdgid)
                else:
                    allFinalStuff.append(pdgid)
                    
        motherPathsQ[0].sort(key=len)
        motherPathsQ[1].sort(key=len)
        
        # PRINTING STARTS
        #-----------------
        checkList = printIfWanted(showVBFCandidates, onlyNotWeaks, onlyNotWeaks_and_bigPt, printShort, printIdx, printIdxStatus, printCoordinateAndPt, event, motherPathsQ, initialQuarks, finalStuff, finalCoordinates_round)
        #print(str(type(checkList)))
        overallList = [x + y for x, y in zip(checkList, overallList)]
        #-----------------
        # PRINTING ENDS
        
    return allFinalStuff, allFinalStuff_anti, overallList
#******************************************************************************************************
# This is the "main function" what is called and run with the boolean parameters
# First all VBFC filters are explained, then eventLoop() is done and at the end small conclusion of everything

def printEvents(r, showVBFCandidates, onlyNotWeaks, onlyNotWeaks_and_bigPt, printShort, printIdx, printIdxStatus, printCoordinateAndPt):
    print('**************************************************************************************')
    if showVBFCandidates:
        print('Filters:')
        print('mjj > 500 GeV                                                    || sum of both Jets invariant masses > 500 GeV')
        print('1.5 < |eta| < 4.7')
        print('|deltaEta| > 4.0')
        print('jetId == x1x                                                     || bit2 is tight')
        print('(puId == x1x) OR (pT > 50.0 GeV)                                 || puId = Pilup ID flags with 80X (2016) training')
        print('no electrons, muons or Higgs jets nearby (deltaR > 0.4)')
        print('---> choose two biggest Jets')
        print('**************************************************************************************')
    if type(r) == tuple:
        r = range(r[0], r[1])
    elif type(r) == list:
        r = r
    else:
        r = range(r) 
        
    # Event loop starts
    # -----------------
    allFinalStuff, allFinalStuff_anti, overallList = eventLoop(r, showVBFCandidates, onlyNotWeaks, onlyNotWeaks_and_bigPt, printShort, printIdx, printIdxStatus, printCoordinateAndPt)
    # Event loop ends
    # -----------------
    if showVBFCandidates:
        print('Reason calculator why the VBFC vs. bJet match fails:')
        print('overallList = [smallerPt, smallMjj, smallEta, bigEta, smallDeltaEta, jetIdWrong, puIdWrong, tooCloseHiggs, tooCloseMuon, tooCloseElectron]:')
        print('overallList = ' + str(overallList))
        print('-------------------------------------------')
    # All final particles (pdgIds)
    print('All ' + str(len(allFinalStuff)) + ' final particles:')
    print(sorted(allFinalStuff, key=len))
    print('-------------------------------------------')
    print('All ' + str(len(allFinalStuff_anti)) + ' final anti-particles:')
    print(sorted(allFinalStuff_anti, key=len))
    print('-------------------------------------------')
    
    print('**************************************************************************************')